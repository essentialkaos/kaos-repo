################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        GEOS is a C++ port of the Java Topology Suite
Name:           geos
Version:        3.13.1
Release:        1%{?dist}
License:        LGPLv2
Group:          Applications/Engineering
URL:            https://libgeos.org

Source0:        https://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make cmake3 gcc-c++

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

################################################################################

%package devel
Summary:  Development files for GEOS
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

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

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a

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

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md DEVELOPER-NOTES.md
%{_bindir}/%{name}op
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}_c.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_includedir}/%{name}_c.h
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_c.so
%{_libdir}/cmake/GEOS/*
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Wed Oct 22 2025 Anton Novojilov <andy@essentialkaos.com> - 3.13.1-1
- Spec refactoring

* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 3.13.1-0
- https://github.com/libgeos/geos/blob/3.13.1/NEWS.md

* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 3.13.0-0
- https://github.com/libgeos/geos/blob/3.13.0/NEWS.md

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 3.12.2-0
- https://github.com/libgeos/geos/blob/3.12.2/NEWS.md

* Tue Sep 19 2023 Anton Novojilov <andy@essentialkaos.com> - 3.12.0-0
- https://github.com/libgeos/geos/blob/3.12.0/NEWS.md

* Tue Sep 19 2023 Anton Novojilov <andy@essentialkaos.com> - 3.11.2-0
- https://github.com/libgeos/geos/blob/3.11.2/NEWS.md

* Sun Sep 25 2022 Anton Novojilov <andy@essentialkaos.com> - 3.11.0-0
- https://github.com/libgeos/geos/blob/3.11.0/NEWS.md

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
