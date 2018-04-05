################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

################################################################################

Summary:            Cartographic projection software (PROJ.4)
Name:               proj
Version:            4.9.3
Release:            0%{?dist}
License:            MIT
Group:              Applications/Engineering
URL:                http://proj.osgeo.org

Source0:            http://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:            http://download.osgeo.org/%{name}/%{name}-datumgrid-1.6.zip

Patch0:             %{name}-removeinclude.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc libtool

Requires(post):     %{__ldconfig}
Requires(postun):   %{__ldconfig}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.

################################################################################

%package devel
Summary:            Development files for PROJ.4
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.

################################################################################

%package static
Summary:        Development files for PROJ.4
Group:          Development/Libraries

%description static
This package contains libproj static library.

################################################################################

%package nad
Summary:        US and Canadian datum shift grids for PROJ.4
Group:          Applications/Engineering

Requires:       %{name} = %{version}-%{release}

%description nad
This package contains additional US and Canadian datum shift grids.

################################################################################

%package epsg
Summary:        EPSG dataset for PROJ.4
Group:          Applications/Engineering

Requires:       %{name} = %{version}-%{release}

%description epsg
This package contains additional EPSG dataset.

################################################################################

%prep
%setup -q

%patch0 -p0

# Disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
  sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

# Prepare nad
pushd nad
  unzip %{SOURCE1}
popd

# Fix shebag header of scripts
for script in `find nad/ -type f -perm -a+x`; do
  sed -i -e '1,1s|:|#!/bin/bash|' $script
done

%build

# Fix version info to respect new ABI
sed -i -e 's|5\:4\:5|6\:4\:6|' src/Makefile*

%configure

%{__make} OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{makeinstall}

install -pm 0644 nad/pj_out27.dist nad/pj_out83.dist nad/td_out.dist \
                 %{buildroot}%{_datadir}/%{name}

install -pm 0755 nad/test27 nad/test83 nad/testvarious \
                 %{buildroot}%{_datadir}/%{name}

install -pm 0644 nad/epsg \
                 %{buildroot}%{_datadir}/%{name}


# Install projects.h manually
install -pm 0644 src/projects.h \
                 %{buildroot}%{_includedir}/

%check
pushd nad
  # Set test enviroment for proj
  export PROJ_LIB=%{buildroot}%{_datadir}/%{name}
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH%{buildroot}%{_libdir}

  # Run tests for proj
  ./test27      %{buildroot}%{_bindir}/%{name} || :
  ./test83      %{buildroot}%{_bindir}/%{name} || :
  ./testIGNF    %{buildroot}%{_bindir}/%{name} || :
  ./testntv2    %{buildroot}%{_bindir}/%{name} || :
  ./testvarious %{buildroot}%{_bindir}/%{name} || :
popd

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%defattr(-,root,root,-)
%doc NEWS AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_libdir}/*.so
%exclude %{_libdir}/*.a
%exclude %{_libdir}/libproj.la

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/libproj.la

%files nad
%defattr(-,root,root,-)
%doc nad/README
%attr(0755,root,root) %{_datadir}/%{name}/test27
%attr(0755,root,root) %{_datadir}/%{name}/test83
%attr(0755,root,root) %{_datadir}/%{name}/testvarious
%attr(0755,root,root) %{_libdir}/pkgconfig/%{name}.pc
%exclude %{_datadir}/%{name}/epsg
%{_datadir}/%{name}

%files epsg
%defattr(-,root,root,-)
%doc nad/README
%attr(0644,root,root) %{_datadir}/%{name}/epsg

################################################################################

%changelog
* Sat Mar 11 2017 Anton Novojilov <andy@essentialkaos.com> - 4.9.3-0
- Initial build for kaos repository
