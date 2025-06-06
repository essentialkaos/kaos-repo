################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?utils:%global utils 1}
%{!?raster:%global raster 1}
%{!?llvm:%global llvm 1}

%define __perl_requires  filter-requires-perl-Pg.sh

################################################################################

%define maj_ver   3.5
%define lib_ver   3
%define pg_ver    %{?_pg}%{!?_pg:99}
%define pg_dir    %{_prefix}/pgsql-%{pg_ver}
%define realname  postgis
%define pkgname   %{realname}-%{maj_ver}
%define fullname  %{realname}35

%define min_geos_ver  3.12

################################################################################

Summary:         Geographic Information Systems Extensions to PostgreSQL %{pg_ver}
Name:            %{fullname}_%{pg_ver}
Version:         3.5.2
Release:         0%{?dist}
License:         GPLv2+
Group:           Applications/Databases
URL:             https://www.postgis.net

Source0:         https://download.osgeo.org/%{realname}/source/%{realname}-%{version}.tar.gz
Source1:         filter-requires-perl-Pg.sh

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   postgresql%{pg_ver}-devel postgresql%{pg_ver}-libs
BuildRequires:   geos-devel >= %{min_geos_ver}
BuildRequires:   gcc-c++ chrpath make pcre-devel hdf5-devel
BuildRequires:   proj-devel libtool flex json-c-devel libxml2-devel
BuildRequires:   sqlite-devel libgeotiff-devel libpng-devel libtiff-devel

%if %llvm
BuildRequires:   llvm-devel >= 13.0 clang-devel >= 13.0
%endif

%if %raster
BuildRequires:   gdal-devel
Requires:        gdal-libs
%endif

Requires:        postgresql%{pg_ver} proj hdf5 json-c pcre
Requires:        %{fullname}_%{pg_ver}-client = %{version}-%{release}
Requires:        geos >= %{min_geos_ver}

Requires(post):  chkconfig

Provides:        %{realname} = %{version}-%{release}

################################################################################

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

################################################################################

%package client
Summary:  Client tools and their libraries of PostGIS
Group:    Applications/Databases

Requires:  %{name} = %{version}-%{release}

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

################################################################################

%package scripts
Summary:  Installing and upgrading scripts for PostGIS
Group:    Applications/Databases

Requires:  %{name} = %{version}-%{release}

%description scripts
This package postgis-scripts contains the SQL scripts for installing PostGIS
in a PostgreSQL database, and for upgrading from earlier PostGIS versions.

################################################################################

%if %utils
%package utils
Summary:  The utils for PostGIS
Group:    Applications/Databases

Requires:  %{name} = %{version}-%{release} perl-DBD-Pg

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

################################################################################

%prep
%crc_check
%autosetup -n %{realname}-%{version}

if [[ -z "%{_pg}" ]] ; then
  echo "PostgreSQL version is not set"
  exit 1
fi

%build
# We need the below for GDAL
export LD_LIBRARY_PATH=%{pg_dir}/lib
export LIBGDAL_CFLAGS=""

%configure \
           --with-pgconfig=%{pg_dir}/bin/pg_config \
           --with-gdalconfig=%{_bindir}/gdal-config \
%if !%raster
           --without-raster \
%endif
%if %llvm
           --with-llvm \
%endif
           --without-protobuf \
           --disable-rpath \
           --libdir=%{pg_dir}/lib

%{__make} %{?_smp_mflags} LPATH=$(%{pg_dir}/bin/pg_config --pkglibdir) shlib="%{name}.so"
%{__make} -C extensions

%if %utils
%{__make} -C utils
%endif

%install
rm -rf %{buildroot}

%{make_install}
%{make_install} -C extensions

rm -rf %{buildroot}%{pg_dir}/doc

mkdir -p %{buildroot}%{pg_dir}/bin/%{pkgname}

chrpath --delete %{buildroot}%{_bindir}/pgsql2shp
chrpath --delete %{buildroot}%{_bindir}/raster2pgsql
chrpath --delete %{buildroot}%{_bindir}/shp2pgsql

mv %{buildroot}%{_bindir}/* \
   %{buildroot}%{pg_dir}/bin/%{pkgname}/

%if %utils
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -pm 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

%post
/sbin/ldconfig

update-alternatives --install %{_bindir}/pgsql2shp       postgis-pgsql2shp       %{pg_dir}/bin/%{pkgname}/pgsql2shp       %{pg_ver}0
update-alternatives --install %{_bindir}/pgtopo_export   postgis-pgtopo_export   %{pg_dir}/bin/%{pkgname}/pgtopo_export   %{pg_ver}0
update-alternatives --install %{_bindir}/pgtopo_import   postgis-pgtopo_import   %{pg_dir}/bin/%{pkgname}/pgtopo_import   %{pg_ver}0
update-alternatives --install %{_bindir}/postgis         postgis-postgis         %{pg_dir}/bin/%{pkgname}/postgis         %{pg_ver}0
update-alternatives --install %{_bindir}/postgis_restore postgis-postgis_restore %{pg_dir}/bin/%{pkgname}/postgis_restore %{pg_ver}0
update-alternatives --install %{_bindir}/raster2pgsql    postgis-raster2pgsql    %{pg_dir}/bin/%{pkgname}/raster2pgsql    %{pg_ver}0
update-alternatives --install %{_bindir}/shp2pgsql       postgis-shp2pgsql       %{pg_dir}/bin/%{pkgname}/shp2pgsql       %{pg_ver}0

%postun
/sbin/ldconfig

if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system
  update-alternatives --remove postgis-pgsql2shp       %{pg_dir}/bin/%{pkgname}/pgsql2shp
  update-alternatives --remove postgis-pgtopo_export   %{pg_dir}/bin/%{pkgname}/pgtopo_export
  update-alternatives --remove postgis-pgtopo_import   %{pg_dir}/bin/%{pkgname}/pgtopo_import
  update-alternatives --remove postgis-postgis         %{pg_dir}/bin/%{pkgname}/postgis
  update-alternatives --remove postgis-postgis_restore %{pg_dir}/bin/%{pkgname}/postgis_restore
  update-alternatives --remove postgis-raster2pgsql    %{pg_dir}/bin/%{pkgname}/raster2pgsql
  update-alternatives --remove postgis-shp2pgsql       %{pg_dir}/bin/%{pkgname}/shp2pgsql
fi

################################################################################

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{realname} doc/html
%doc loader/README.* doc/%{realname}.xml doc/ZMSgeoms.txt
%{pg_dir}/lib/address_standardizer-%{lib_ver}.so
%{pg_dir}/lib/postgis-%{lib_ver}.so
%{pg_dir}/lib/postgis_topology-%{lib_ver}.so
%if %raster
%{pg_dir}/lib/postgis_raster-%{lib_ver}.so
%endif
%{_mandir}/man1/*

%files client
%defattr(-,root,root)
%{pg_dir}/bin/%{pkgname}/pgsql2shp
%{pg_dir}/bin/%{pkgname}/pgtopo_export
%{pg_dir}/bin/%{pkgname}/pgtopo_import
%{pg_dir}/bin/%{pkgname}/postgis
%{pg_dir}/bin/%{pkgname}/postgis_restore
%{pg_dir}/bin/%{pkgname}/raster2pgsql
%{pg_dir}/bin/%{pkgname}/shp2pgsql

%files scripts
%defattr(-,root,root)
%{pg_dir}/share/contrib/%{pkgname}/legacy_gist.sql
%{pg_dir}/share/contrib/%{pkgname}/legacy_minimal.sql
%{pg_dir}/share/contrib/%{pkgname}/legacy.sql
%{pg_dir}/share/contrib/%{pkgname}/postgis_comments.sql
%{pg_dir}/share/contrib/%{pkgname}/postgis.sql
%{pg_dir}/share/contrib/%{pkgname}/postgis_upgrade.sql
%{pg_dir}/share/contrib/%{pkgname}/raster_comments.sql
%{pg_dir}/share/contrib/%{pkgname}/sfcgal_comments.sql
%{pg_dir}/share/contrib/%{pkgname}/spatial_ref_sys.sql
%{pg_dir}/share/contrib/%{pkgname}/topology_comments.sql
%{pg_dir}/share/contrib/%{pkgname}/topology.sql
%{pg_dir}/share/contrib/%{pkgname}/topology_upgrade.sql
%{pg_dir}/share/contrib/%{pkgname}/uninstall_legacy.sql
%{pg_dir}/share/contrib/%{pkgname}/uninstall_postgis.sql
%{pg_dir}/share/contrib/%{pkgname}/uninstall_topology.sql
%{pg_dir}/share/extension/address_standardizer*.control
%{pg_dir}/share/extension/address_standardizer*.sql
%{pg_dir}/share/extension/postgis*.control
%{pg_dir}/share/extension/postgis*.sql
%if %raster
%{pg_dir}/share/contrib/%{pkgname}/rtpostgis.sql
%{pg_dir}/share/contrib/%{pkgname}/rtpostgis_legacy.sql
%{pg_dir}/share/contrib/%{pkgname}/rtpostgis_upgrade.sql
%{pg_dir}/share/contrib/%{pkgname}/uninstall_rtpostgis.sql
%endif
%if %llvm
%{pg_dir}/lib/bitcode/*
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/create_extension_unpackage.pl
%attr(755,root,root) %{_datadir}/%{name}/create_or_replace_to_create.pl
%attr(755,root,root) %{_datadir}/%{name}/create_skip_signatures.pl
%attr(755,root,root) %{_datadir}/%{name}/create_spatial_ref_sys_config_dump.pl
%attr(755,root,root) %{_datadir}/%{name}/create_uninstall.pl
%attr(755,root,root) %{_datadir}/%{name}/create_unpackaged.pl
%attr(755,root,root) %{_datadir}/%{name}/create_upgrade.pl
%attr(755,root,root) %{_datadir}/%{name}/postgis_restore.pl
%attr(755,root,root) %{_datadir}/%{name}/profile_intersects.pl
%attr(755,root,root) %{_datadir}/%{name}/read_scripts_version.pl
%attr(755,root,root) %{_datadir}/%{name}/repo_revision.pl
%attr(755,root,root) %{_datadir}/%{name}/test_estimation.pl
%attr(755,root,root) %{_datadir}/%{name}/test_geography_estimation.pl
%attr(755,root,root) %{_datadir}/%{name}/test_geography_joinestimation.pl
%attr(755,root,root) %{_datadir}/%{name}/test_joinestimation.pl
%endif

################################################################################

%changelog
* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5.2-0
- https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.2/NEWS

* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5.1-0
- https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.1/NEWS

* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5.0-0
- https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.0/NEWS
