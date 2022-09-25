################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:           GEOS is a C++ port of the Java Topology Suite
Name:              geos
Version:           3.11.0
Release:           0%{?dist}
License:           LGPLv2
Group:             Applications/Engineering
URL:               https://trac.osgeo.org/geos

Source0:           https://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make cmake3 gcc-c++

Provides:          %{name} = %{version}-%{release}

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
mkdir _build
pushd _build

cmake3 .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}

%{__make} %{?_smp_mflags}

popd

%install
rm -rf %{buildroot}

pushd _build
%{make_install}
popd

%check
%if %{?_with_check:1}%{?_without_check:0}
pushd _build
%{__make} %{?_smp_mflags} check
popd
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md DEVELOPER-NOTES.md
%{_bindir}/%{name}op
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}_c.so.*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%{_bindir}/%{name}-config
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_c.so
%{_libdir}/cmake/GEOS/*
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sun Sep 25 2022 Anton Novojilov <andy@essentialkaos.com> - 3.11.0-0
- Updated to the latest release

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
