################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%global sqlite_min_ver %(rpm -q --quiet sqlite-devel && rpm -q --qf '%{VERSION}' sqlite-devel || echo "3")
%global libcurl_min_ver %(rpm -q --quiet libcurl-devel && rpm -q --qf '%{VERSION}' libcurl-devel || echo "7")

################################################################################

%define data_version  1.18

################################################################################

Summary:           Cartographic projection software (PROJ)
Name:              proj
Version:           9.4.1
Release:           0%{?dist}
License:           MIT
Group:             Applications/Engineering
URL:               https://www.osgeo.org/projects/proj/

Source0:           https://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:           https://download.osgeo.org/%{name}/%{name}-data-%{data_version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     cmake3 gcc-c++ sqlite libtiff-devel
BuildRequires:     sqlite-devel >= %{sqlite_min_ver}
BuildRequires:     libcurl-devel >= %{libcurl_min_ver}

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

Requires:          %{name}-data = %{version}-%{release}

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.

################################################################################

%package devel
Summary:  Development files for PROJ
Group:    Development/Libraries

Requires:  sqlite-devel >= %{sqlite_min_ver}
Requires:  libcurl-devel >= %{libcurl_min_ver}

Requires:  %{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.

################################################################################

%package static
Summary:  Development files for PROJ
Group:    Development/Libraries

%description static
This package contains libproj static library.

################################################################################

%package data
Summary:  Proj data files
Group:    Development/Tools
License:  CC-BY and Freely Distributable and Ouverte and Public Domain

BuildArch:  noarch

%description data
Proj arch independent data files.

################################################################################

%package data-world
Summary:  Countries datum grids for Proj
Group:    Development/Tools
License:  CC-BY and Freely Distributable and Ouverte and Public Domain

BuildArch:  noarch

Requires:  %{name}-data = %{version}-%{release}

%description data-world
Countries datum grids for Proj.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%cmake3 -DBUILD_TESTING=OFF
%cmake3_build

%install
rm -rf %{buildroot}

%cmake3_install

mkdir -p %{buildroot}%{_datadir}/%{name}
tar -xf %{SOURCE1} --directory %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/libproj.so.*
%{_mandir}/man1/*.1*
%{_defaultdocdir}/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_includedir}/proj/
%{_libdir}/libproj.so
%{_libdir}/cmake/proj/
%{_libdir}/cmake/proj4/
%{_libdir}/pkgconfig/%{name}.pc

%files data
%defattr(-,root,root,-)
%{_datadir}/%{name}/CH
%{_datadir}/%{name}/GL27
%{_datadir}/%{name}/ITRF2000
%{_datadir}/%{name}/ITRF2008
%{_datadir}/%{name}/ITRF2014
%{_datadir}/%{name}/nad.lst
%{_datadir}/%{name}/nad27
%{_datadir}/%{name}/nad83
%{_datadir}/%{name}/other.extra
%{_datadir}/%{name}/proj.db
%{_datadir}/%{name}/proj.ini
%{_datadir}/%{name}/world
%{_datadir}/%{name}/README.DATA
%{_datadir}/%{name}/copyright_and_licenses.csv
%{_datadir}/%{name}/deformation_model.schema.json
%{_datadir}/%{name}/projjson.schema.json
%{_datadir}/%{name}/triangulation.schema.json

%files data-world
%defattr(-,root,root,-)
%{_datadir}/%{name}/ar_*
%{_datadir}/%{name}/at_*
%{_datadir}/%{name}/au_*
%{_datadir}/%{name}/be_*
%{_datadir}/%{name}/br_*
%{_datadir}/%{name}/ca_*
%{_datadir}/%{name}/ch_*
%{_datadir}/%{name}/cz_*
%{_datadir}/%{name}/de_*
%{_datadir}/%{name}/DK
%{_datadir}/%{name}/dk_*
%{_datadir}/%{name}/es_*
%{_datadir}/%{name}/eur_*
%{_datadir}/%{name}/fi_*
%{_datadir}/%{name}/FO
%{_datadir}/%{name}/fr_*
%{_datadir}/%{name}/is_*
%{_datadir}/%{name}/ISL
%{_datadir}/%{name}/jp_*
%{_datadir}/%{name}/mx_*
%{_datadir}/%{name}/nc_*
%{_datadir}/%{name}/NKG
%{_datadir}/%{name}/nl_*
%{_datadir}/%{name}/no_*
%{_datadir}/%{name}/nz_*
%{_datadir}/%{name}/pl_*
%{_datadir}/%{name}/pt_*
%{_datadir}/%{name}/se_*
%{_datadir}/%{name}/si_*
%{_datadir}/%{name}/sk_*
%{_datadir}/%{name}/uk_*
%{_datadir}/%{name}/us_*
%{_datadir}/%{name}/za_*

################################################################################

%changelog
* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 9.4.1-0
- https://proj.org/en/9.4/news.html

* Wed Sep 27 2023 Anton Novojilov <andy@essentialkaos.com> - 9.3.0-0
- https://proj.org/en/9.3/news.html

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 6.2.1-0
- Updated to the latest stable release

* Sat Mar 11 2017 Anton Novojilov <andy@essentialkaos.com> - 4.9.3-0
- Initial build for kaos repository
