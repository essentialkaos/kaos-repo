################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:           GEOS is a C++ port of the Java Topology Suite
Name:              geos
Version:           3.9.1
Release:           0%{?dist}
License:           LGPLv2
Group:             Applications/Engineering
URL:               https://trac.osgeo.org/geos

Source0:           https://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     doxygen libtool python-devel gcc-c++ make swig m4

################################################################################

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

################################################################################

%package devel
Summary:           Development files for GEOS
Group:             Development/Libraries
Requires:          %{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

################################################################################

%prep
%{crc_check}

%setup -q

%build
# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'` ; do
  sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

%configure --disable-static \
           --disable-dependency-tracking

%{__make} %{?_smp_mflags}
cd doc
%{__make} doxygen-html

%install
rm -rf %{buildroot}
%{make_install}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README.md
%{_libdir}/lib%{name}-%{version}.so
%{_libdir}/lib%{name}_c.so.*
%exclude %{_libdir}/*.a

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{_bindir}/%{name}-config
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_c.so
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%{_libdir}/pkgconfig/geos.pc

################################################################################

%changelog
* Thu Feb 11 2021 Anton Novojilov <andy@essentialkaos.com> - 3.9.1-0
- Updated to the latest release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.6.2-0
- Updated to the latest release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.6.1-0
- Updated to the latest release

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.0-0
- Updated to latest release

* Sat Sep 06 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.2-0
- Initial build
