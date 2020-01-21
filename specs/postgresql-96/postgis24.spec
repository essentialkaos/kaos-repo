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

%{!?utils:%define utils 1}
%{!?raster:%define raster 1}

%define maj_ver           2.4
%define pg_comb_ver       96
%define pg_maj_ver        9.6
%define pg_low_fullver    9.6.0
%define pg_dir            %{_prefix}/pgsql-%{pg_maj_ver}
%define realname          postgis
%define fullname          %{realname}24

%define _smp_mflags       -j1

%define __perl_requires   filter-requires-perl-Pg.sh

################################################################################

Summary:           Geographic Information Systems Extensions to PostgreSQL %{pg_comb_ver}
Name:              %{fullname}_%{pg_comb_ver}
Version:           2.4.8
Release:           0%{?dist}
License:           GPLv2+
Group:             Applications/Databases
URL:               https://www.postgis.net

Source0:           https://download.osgeo.org/%{realname}/source/%{realname}-%{version}.tar.gz
Source1:           https://download.osgeo.org/%{realname}/docs/%{realname}-%{version}.pdf
Source2:           filter-requires-perl-Pg.sh

Patch0:            %{fullname}-gdalfpic.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     postgresql%{pg_comb_ver}-devel = %{pg_low_fullver}
BuildRequires:     postgresql%{pg_comb_ver}-libs = %{pg_low_fullver}

BuildRequires:     geos-devel >= 3.6 chrpath make gcc pcre-devel hdf5-devel
BuildRequires:     proj-devel libtool flex json-c-devel libxml2-devel

%if %raster
BuildRequires:     gdal-devel >= 1.9.0
%endif

Requires:          postgresql%{pg_comb_ver} geos >= 3.6 proj hdf5 json-c pcre
Requires:          %{fullname}_%{pg_comb_ver}-client = %{version}-%{release}

Requires(post):    %{_sbindir}/update-alternatives

Obsoletes:         %{realname}2_%{pg_comb_ver} <= 2.4.4

Conflicts:         %{realname}25

Provides:          %{realname} = %{version}-%{release}

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
Summary:           Client tools and their libraries of PostGIS
Group:             Applications/Databases
Requires:          %{name} = %{version}-%{release}

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

################################################################################

%package devel
Summary:           Development headers and libraries for PostGIS
Group:             Development/Libraries
Requires:          %{name} = %{version}-%{release}

%description devel
The postgis-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

################################################################################

%package docs
Summary:           Extra documentation for PostGIS
Group:             Applications/Databases

%description docs
The postgis-docs package includes PDF documentation of PostGIS.

################################################################################

%if %utils
%package utils
Summary:           The utils for PostGIS
Group:             Applications/Databases
Requires:          %{name} = %{version}-%{release} perl-DBD-Pg

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

################################################################################

%prep
%setup -qn %{realname}-%{version}

# Copy .pdf file to top directory before installing
cp -p %{SOURCE1} .

%patch0 -p0

%build
# We need the below for GDAL:
export LD_LIBRARY_PATH=%{pg_dir}/lib

%configure --with-pgconfig=%{pg_dir}/bin/pg_config \
%if !%raster
           --without-raster \
%endif
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

mkdir -p %{buildroot}%{pg_dir}/bin/%{realname}-%{maj_ver}

chrpath --delete %{buildroot}%{pg_dir}/bin/pgsql2shp
chrpath --delete %{buildroot}%{pg_dir}/bin/shp2pgsql
chrpath --delete %{buildroot}%{pg_dir}/bin/raster2pgsql

mv %{buildroot}%{pg_dir}/bin/pgsql2shp \
   %{buildroot}%{pg_dir}/bin/shp2pgsql \
   %{buildroot}%{pg_dir}/bin/raster2pgsql \
   %{buildroot}%{pg_dir}/bin/%{realname}-%{maj_ver}/

%if %utils
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -pm 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

%post
%{__ldconfig}

%{_sbindir}/update-alternatives --install %{_bindir}/pgsql2shp postgis-pgsql2shp       %{pg_dir}/bin/%{realname}-%{maj_ver}/pgsql2shp    %{pg_comb_ver}0
%{_sbindir}/update-alternatives --install %{_bindir}/shp2pgsql postgis-shp2pgsql       %{pg_dir}/bin/%{realname}-%{maj_ver}/shp2pgsql    %{pg_comb_ver}0
%{_sbindir}/update-alternatives --install %{_bindir}/raster2pgsql postgis-raster2pgsql %{pg_dir}/bin/%{realname}-%{maj_ver}/raster2pgsql %{pg_comb_ver}0

%postun
%{__ldconfig}

if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
  %{_sbindir}/update-alternatives --remove postgis-pgsql2shp     %{pg_dir}/bin/%{realname}-%{maj_ver}/pgsql2shp
  %{_sbindir}/update-alternatives --remove postgis-shp2pgsql     %{pg_dir}/bin/%{realname}-%{maj_ver}/shp2pgsql
  %{_sbindir}/update-alternatives --remove postgis-raster2pgsql  %{pg_dir}/bin/%{realname}-%{maj_ver}/raster2pgsql
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{realname} doc/html loader/README.* doc/%{realname}.xml doc/ZMSgeoms.txt
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/*legacy*.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis_comments.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis_for_extension.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis_proc_set_search_path.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis_restore.pl
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/postgis_upgrade*.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/raster_comments.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/sfcgal_comments.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/spatial*.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/topology*.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/uninstall_postgis.sql
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/uninstall_topology.sql
%{pg_dir}/share/extension/%{realname}*
%{pg_dir}/share/extension/address_standardizer*
%attr(755,root,root) %{pg_dir}/lib/%{realname}-*.so
%{pg_dir}/lib/liblwgeom*.so*
%if %raster
%{pg_dir}/share/contrib/%{realname}-%{maj_ver}/*rtpostgis*.sql
%{pg_dir}/lib/address_standardizer.so
%{pg_dir}/lib/postgis_topology-%{maj_ver}.so
%{pg_dir}/lib/rtpostgis-%{maj_ver}.so
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pg_dir}/bin/*

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
%{pg_dir}/lib/liblwgeom*.a
%{pg_dir}/lib/liblwgeom*.la

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc %{realname}-%{version}.pdf
%doc %{pg_dir}/doc/extension/README.address_standardizer

################################################################################

%changelog
* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.8-0
- Updated to the latest stable release

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.5-0
- Initial build
