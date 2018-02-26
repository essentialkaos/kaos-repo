################################################################################

Summary:              GeoTIFF format library
Name:                 libgeotiff
Version:              1.4.2
Release:              0%{?dist}
License:              MIT
Group:                System Environment/Libraries
URL:                  https://trac.osgeo.org/geotiff/

Source:               http://download.osgeo.org/geotiff/%{name}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc gcc-c++ doxygen chrpath
BuildRequires:        libtiff-devel libjpeg-devel proj-devel zlib-devel

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

################################################################################

%package devel
Summary:            Development library and header for the GeoTIFF file format library
Group:              Development/Libraries

Requires:           pkgconfig libtiff-devel
Requires:           %{name} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

################################################################################

%prep
%setup -q -n %{name}-%{version}

%build
# disable -g flag removal
sed -i 's| \| sed \"s\/-g \/\/\"||g' configure

# use gcc -shared instead of ld -shared to build with -fstack-protector
sed -i 's|LD_SHARED=@LD_SHARED@|LD_SHARED=@CC@ -shared|' Makefile.in

%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}/ \
        --with-proj \
        --with-tiff \
        --with-jpeg \
        --with-zip

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

# install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

install -dm 755 %{buildroot}%{_libdir}/pkgconfig/
install -pm 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la
echo "" >> %{buildroot}%{_datadir}/epsg_csv/codes.csv

chrpath --delete %{buildroot}%{_bindir}/applygeo
chrpath --delete %{buildroot}%{_bindir}/geotifcp
chrpath --delete %{buildroot}%{_bindir}/listgeo

pushd docs
  doxygen .
popd

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README
%doc docs/manual.txt docs/html
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo
%{_libdir}/%{name}.so.*
%{_mandir}/man1/*.gz
%{_datadir}/epsg_csv/csv2c.py*
%{_datadir}/epsg_csv/csv_tools.py*
%dir %{_datadir}/epsg_csv
%attr(0644,root,root) %{_datadir}/epsg_csv/*.csv

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/*.inc
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Initial build for kaos repository
