################################################################################

Summary:              Enables SQLite to support spatial data
Name:                 libspatialite
Version:              4.3.0a
Release:              2%{?dist}
License:              MPLv1.1 or GPLv2+ or LGPLv2+
Group:                System Environment/Libraries
URL:                  https://www.gaia-gis.it/fossil/libspatialite

Source:               http://www.gaia-gis.it/gaia-sins/libspatialite-sources/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc

BuildRequires:        freexl-devel geos-devel proj-devel sqlite-devel >= 3.18
BuildRequires:        zlib-devel libxml2-devel

Requires:             sqlite >= 3.18

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
SpatiaLite is a a library extending the basic SQLite core
in order to get a full fledged Spatial DBMS, really simple
and lightweight, but mostly OGC-SFS compliant.

################################################################################

%package devel
Summary:            Development libraries and headers for SpatiaLite
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%prep
%setup -q

%build
%configure \
    --disable-static \
    --enable-lwgeom=no \
    --enable-libxml2=yes \
    --disable-geosadvanced \
    --enable-geocallbacks

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/%{name}.la
rm -f %{buildroot}%{_libdir}/mod_spatialite.la

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files 
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_libdir}/%{name}.so.*
%{_libdir}/mod_spatialite.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/spatialite.h
%{_includedir}/spatialite
%{_libdir}/%{name}.so
%{_libdir}/mod_spatialite.so
%{_libdir}/pkgconfig/spatialite.pc

################################################################################

%changelog
* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 4.3.0a-2
- Initial build for kaos repository
