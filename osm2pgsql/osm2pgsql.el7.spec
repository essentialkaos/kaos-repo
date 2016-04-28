###############################################################################

Summary:              OpenStreetMap data to PostgreSQL converter
Name:                 osm2pgsql
Version:              0.90.0
Release:              0%{?dist}
License:              GPL
Group:                Development/Tools
URL:                  http://wiki.openstreetmap.org/wiki/Osm2pgsql

Source:               https://github.com/openstreetmap/%{name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        cmake gcc-c++ boost-devel expat-devel geos-devel
BuildRequires:        zlib-devel bzip2-devel postgresql-devel proj-devel
BuildRequires:        proj-epsg lua-devel python-psycopg2

###############################################################################

%description
osm2pgsql is a tool for loading OpenStreetMap data into a PostgreSQL / PostGIS
database suitable for applications like rendering into a map, geocoding with
Nominatim, or general analysis.

###############################################################################

%prep
%setup -q

%build
mkdir -p build
pushd build
    cmake .. -G "Unix Makefiles" \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_TESTS=OFF
    %{__make} %{?_smp_mflags}
popd

%install
%{__rm} -rf %{buildroot}
pushd build
    %{make_install} DESTDIR=%{buildroot}
popd

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,0755)
%doc AUTHORS CONTRIBUTING.md ChangeLog COPYING README.md
%doc %{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/*.style

###############################################################################

%changelog
* Thu Apr 28 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.90.0-0
- Initial build.

