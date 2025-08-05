################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global sqlite_ver   %(rpm -q --quiet sqlite-devel && rpm -q --qf '%%{version}' sqlite-devel || echo "3")
%global libcurl_ver  %(rpm -q --quiet libcurl-devel && rpm -q --qf '%%{version}' libcurl-devel || echo "8")
%global hdf5_ver     %(rpm -q --quiet hdf5-devel && rpm -q --qf '%%{version}' hdf5-devel || echo "1.14")

################################################################################

# The oldest supported PG version
%define pg_short_ver  13
%define pg_lib_dir    %{_prefix}/pgsql-%{pg_short_ver}/lib

################################################################################

Summary:        A translator library for raster and vector geospatial data formats
Name:           gdal
Version:        3.10.3
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://www.gdal.org

Source0:        https://download.osgeo.org/%{name}/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake swig
BuildRequires:  gcc-c++ bison expat-devel freexl-devel geos-devel hdf-devel
BuildRequires:  libgeotiff-devel libjpeg-turbo-devel libpng-devel
BuildRequires:  libtiff-devel libzstd-devel libwebp-devel netcdf-devel
BuildRequires:  openexr-devel openjpeg2-devel proj-devel
BuildRequires:  xerces-c-devel xz-devel zlib-devel giflib-devel
BuildRequires:  postgresql%{pg_short_ver}-devel

BuildRequires:  sqlite-devel >= %{sqlite_ver}
BuildRequires:  libcurl-devel >= %{libcurl_ver}
BuildRequires:  hdf5-devel >= %{hdf5_ver}

Requires:       libcurl >= %{libcurl_ver}
Requires:       sqlite-libs >= %{sqlite_ver}
Requires:       hdf5 >= %{hdf5_ver}

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

Requires:  postgresql%{pg_short_ver}-devel
Requires:  libcurl-devel >= %{libcurl_ver}
Requires:  hdf5-devel = %{hdf5_ver}

%description devel
Development Libraries for the GDAL file format library.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
%{cmake3} \
  -DCMAKE_INSTALL_INCLUDEDIR=include/%{name} \
  -DGDAL_USE_TIFF_INTERNAL=ON \
  -DGDAL_USE_GEOTIFF_INTERNAL=ON \
  -DGDAL_USE_JPEG12_INTERNAL=OFF \
  -DGDAL_USE_OPENEXR=OFF \
  -DBUILD_PYTHON_BINDINGS=OFF \
  -DENABLE_DEFLATE64=OFF

%{cmake3_build}

%install
rm -rf %{buildroot}

%{cmake3_install}

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
%exclude %{_mandir}/man1/%{name}-config.1*
%exclude %{_bindir}/%{name}-config*
%exclude %{_datadir}/bash-completion/completions/*.py
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/*

%files libs
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
%{_datadir}/%{name}/
%{_libdir}/%{name}plugins/

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config*
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man1/%{name}-config.1*

################################################################################

%changelog
* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 3.10.3-0
- https://github.com/OSGeo/gdal/blob/v3.10.3/NEWS.md

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 3.9.1-0
- https://github.com/OSGeo/gdal/blob/v3.9.1/NEWS.md

* Sat Dec 09 2023 Anton Novojilov <andy@essentialkaos.com> - 3.7.3-0
- https://github.com/OSGeo/gdal/blob/v3.7.3/NEWS.md

* Tue Oct 10 2023 Anton Novojilov <andy@essentialkaos.com> - 3.7.2-1
- Spec refactoring

* Tue Sep 19 2023 Anton Novojilov <andy@essentialkaos.com> - 3.7.2-0
- https://github.com/OSGeo/gdal/blob/v3.7.2/NEWS.md

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-1
- Minor spec improvements

* Sat Feb 13 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Initial build
