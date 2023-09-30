################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global sqlite_min_ver %(rpm -q --quiet sqlite-devel && rpm -q --qf '%{VERSION}' sqlite-devel || echo "3")
%global libcurl_min_ver %(rpm -q --quiet libcurl-devel && rpm -q --qf '%{VERSION}' libcurl-devel || echo "7")

################################################################################

%define realname  gdal

%if 0%{?rhel} <= 7
%define fullname  %{realname}3
%else
%define fullname  %{realname}
%endif

# The oldest supported PG version
%define pg_short_ver  10
%define pg_lib_dir    %{_prefix}/pgsql-%{pg_short_ver}/lib

################################################################################

Summary:        A translator library for raster and vector geospatial data formats
Name:           %{fullname}
Version:        3.7.2
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://www.gdal.org

Source0:        https://download.osgeo.org/%{realname}/%{version}/%{realname}-%{version}.tar.gz
Source1:        %{realname}3-pgdg-libs.conf

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} <= 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake swig
%endif

BuildRequires:  gcc-c++ bison expat-devel freexl-devel geos-devel hdf-devel
BuildRequires:  hdf5-devel libgeotiff-devel libjpeg-devel libpng-devel
BuildRequires:  libtiff-devel libzstd-devel libwebp-devel netcdf-devel
BuildRequires:  openexr-devel openjpeg2-devel proj-devel
BuildRequires:  xerces-c-devel xz-devel zlib-devel giflib-devel
BuildRequires:  postgresql%{pg_short_ver}-devel

BuildRequires:  sqlite-devel >= %{sqlite_min_ver}
BuildRequires:  libcurl-devel >= %{libcurl_min_ver}

Requires:       libcurl >= %{libcurl_min_ver}
Requires:       sqlite-libs >= %{sqlite_min_ver}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
GDAL is a translator library for raster geospatial data formats that
is released under an Open Source license. As a library, it presents a
single abstract data model to the calling application for all
supported formats. The related OGR library (which lives within the
GDAL source tree) provides a similar capability for simple features
vector data.

################################################################################

%package libs
Summary:   GDAL file format library
Group:     Development/Libraries

%description libs
This package contains the GDAL file format library.

################################################################################

%package devel
Summary:   GDAL library header files
Group:     Development/Libraries

Requires:  %{name}-libs = %{version}-%{release}

Requires:  libcurl-devel >= %{libcurl_min_ver}
Requires:  postgresql%{pg_short_ver}-devel

%description devel
Development Libraries for the GDAL file format library.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%build
%{cmake3} \
  -DCMAKE_INSTALL_INCLUDEDIR=include/%{fullname} \
  -DGDAL_USE_JPEG12_INTERNAL=OFF \
  -DBUILD_PYTHON_BINDINGS=OFF \
  -DENABLE_DEFLATE64=OFF

%{cmake3_build}

%install
rm -rf %{buildroot}

%{cmake3_install}

# Install linker configuration file
install -dm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-libs.conf

%clean
rm -rf %{buildroot}

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc README.md NEWS.md PROVENANCE.TXT LICENSE.TXT SECURITY.md CODE_OF_CONDUCT.md
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-libs.conf
%exclude %{_mandir}/man1/%{realname}-config.1*
%exclude %{_bindir}/%{realname}-config*
%exclude %{_datadir}/bash-completion/completions/*.py
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/*

%files libs
%defattr(-,root,root)
%{_libdir}/lib%{realname}.so.*
%{_datadir}/%{realname}/
%{_libdir}/%{realname}plugins/

%files devel
%defattr(-,root,root)
%{_bindir}/%{realname}-config*
%{_includedir}/%{name}/
%{_libdir}/lib%{realname}.so
%{_libdir}/cmake/%{realname}/
%{_libdir}/pkgconfig/%{realname}.pc
%{_mandir}/man1/%{realname}-config.1*

################################################################################

%changelog
* Tue Sep 19 2023 Anton Novojilov <andy@essentialkaos.com> - 3.7.2-0
- https://github.com/OSGeo/gdal/blob/v3.7.2/NEWS.md

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-1
- Minor spec improvements

* Sat Feb 13 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Initial build
