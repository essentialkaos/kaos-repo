################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

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

%define datumgrid_ver     1.8

################################################################################

Summary:            Cartographic projection software (PROJ)
Name:               proj
Version:            6.2.1
Release:            0%{?dist}
License:            MIT
Group:              Applications/Engineering
URL:                http://proj.osgeo.org

Source0:            https://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:            https://download.osgeo.org/%{name}/%{name}-datumgrid-%{datumgrid_ver}.tar.gz
Source2:            FindPROJ4.cmake

Source100:          checksum.sha512

Patch0:             %{name}-removeinclude.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc-c++ sqlite-devel libtool

Requires(post):     %{__ldconfig}
Requires(postun):   %{__ldconfig}

Requires:           %{name}-datumgrid = %{datumgrid_ver}-%{release}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.

################################################################################

%package devel
Summary:            Development files for PROJ
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.

################################################################################

%package static
Summary:        Development files for PROJ
Group:          Development/Libraries

%description static
This package contains libproj static library.

################################################################################

%package datumgrid
Summary:        Additional datum shift grids for PROJ
Group:          Development/Tools
License:        CC-BY and Freely Distributable and Ouverte and Public Domain

Version:        %{datumgrid_ver}

BuildArch:      noarch

%description datumgrid
This package contains additional datum shift grids.

################################################################################

%prep
%{crc_check}

%setup -q

%patch0 -p1

mkdir nad
tar xvf %{SOURCE1} -C nad | \
  sed -e "s!^!%{_datadir}/%{name}/!" \
      -e "/README/s!^!%%doc !" > datumgrid.files

%build
%configure

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

chmod -x %{buildroot}%{_libdir}/libproj.la
install -pm 644 nad/* %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/cmake/Modules/
install -pm 644 %{SOURCE2} %{buildroot}%{_datadir}/cmake/Modules/FindPROJ4.cmake
sed -i "s/!PROJ_VERSION!/%{version}/" %{buildroot}%{_datadir}/cmake/Modules/FindPROJ4.cmake

%check
%if %{?_with_check:1}%{?_without_check:0}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
  %{__make} PROJ_LIB=%{buildroot}%{_datadir}/%{name} check || ( cat src/test-suite.log; exit 1 )
%endif

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
%dir %{_datadir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/libproj.so.15*
%{_datadir}/%{name}/*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_includedir}/proj/
%{_includedir}/proj_json_streaming_writer.hpp
%{_datadir}/proj/projjson.schema.json
%{_libdir}/libproj.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/Modules/FindPROJ4.cmake
%exclude %{_libdir}/*.a
%exclude %{_libdir}/libproj.la

%files static
%defattr(-,root,root,-)
%{_libdir}/libproj.a
%{_libdir}/libproj.la

%files datumgrid -f datumgrid.files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}

################################################################################

%changelog
* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 6.2.1-0
- Updated to the latest stable release

* Sat Mar 11 2017 Anton Novojilov <andy@essentialkaos.com> - 4.9.3-0
- Initial build for kaos repository
