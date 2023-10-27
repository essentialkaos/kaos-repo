################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        GeoTIFF format library
Name:           libgeotiff
Version:        1.7.1
Release:        0%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            https://trac.osgeo.org/geotiff/

Source0:        https://download.osgeo.org/geotiff/%{name}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ doxygen chrpath
BuildRequires:  libtiff-devel libjpeg-turbo-devel zlib-devel proj-devel >= 6

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

################################################################################

%package devel
Summary:  Development library and header for the GeoTIFF file format library
Group:    Development/Libraries

Requires:  pkgconfig libtiff-devel proj-devel
Requires:  %{name} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
# Disable -g flag removal
sed -i 's| \| sed \"s\/-g \/\/\"||g' configure
# Use gcc -shared instead of ld -shared to build with -fstack-protector
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

# Install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# Create pkgconfig file
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

# Clean up junks
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

chrpath --delete --keepgoing %{buildroot}%{_bindir}/* || :

pushd docs
  doxygen .
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

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

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/*.inc
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- https://github.com/OSGeo/libgeotiff/releases/tag/1.7.1

* Thu Dec 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Updated to the latest stable release

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to the latest stable release

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- Updated to the latest stable release

* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Initial build for kaos repository
