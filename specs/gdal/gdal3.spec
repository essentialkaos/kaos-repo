################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$

%global libcurl_min_ver %(rpm -q --quiet libcurl-devel && rpm -q --qf '%{VERSION}' libcurl-devel || echo "7")

################################################################################

%define realname         gdal
%define fullname         %{realname}3
%define install_dir      %{_prefix}/%{fullname}
%define install_bin_dir  %{install_dir}/bin
%define install_lib_dir  %{install_dir}/lib
%define install_inc_dir  %{install_dir}/include
%define install_man_dir  %{install_dir}/share/man/man1

# The oldest supported PG version
%define pg_short_ver  10
%define pg_lib_dir    %{_prefix}/pgsql-%{pg_short_ver}/lib

################################################################################

Summary:        A translator library for raster and vector geospatial data formats
Name:           %{fullname}
Version:        3.2.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://www.gdal.org

Source0:        https://download.osgeo.org/%{realname}/%{version}/%{realname}-%{version}.tar.gz
Source1:        %{name}.pc
Source2:        %{name}-pgdg-libs.conf

Patch1:         %{name}-perl.patch
Patch2:         %{name}-sfgcal-linker.patch

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf >= 2.52 automake gcc-c++ doxygen >= 1.4.2
BuildRequires:  geos-devel >= 3 libstdc++-devel expat-devel
BuildRequires:  libgeotiff-devel libjpeg-turbo-devel libpng-devel
BuildRequires:  hdf-devel hdf5-devel libtiff-devel
BuildRequires:  libtool netcdf-devel blas-devel lapack-devel
BuildRequires:  ruby-devel sqlite-devel >= 3 swig
BuildRequires:  unixODBC-devel zlib-devel xerces-c-devel
BuildRequires:  proj-devel m4 chrpath perl-ExtUtils-MakeMaker
BuildRequires:  freexl-devel postgresql%{pg_short_ver}-devel
BuildRequires:  libcurl-devel >= %{libcurl_min_ver}

Requires:       geos libstdc++ expat libgeotiff libjpeg libpng hdf hdf5
Requires:       libtiff netcdf blas lapack sqlite unixODBC zlib xerces-c
Requires:       proj freexl libcurl >= %{libcurl_min_ver}

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

%package devel
Summary:   GDAL library header files
Group:     Development/Libraries

Requires:  %{name} = %{version}-%{release}

Requires:  expat-devel geos-devel >= 3 hdf-devel hdf5-devel
Requires:  netcdf-devel libstdc++-devel
Requires:  postgresql%{pg_short_ver}-devel sqlite-devel >= 3
Requires:  unixODBC-devel freexl-devel xerces-c-devel
Requires:  libcurl-devel >= %{libcurl_min_ver}

%description devel
Development Libraries for the GDAL file format library

################################################################################

%package perl
Summary:        Perl bindings for GDAL
Group:          Development/Languages

BuildRequires:  perl-devel

Requires:       perl perl-ExtUtils-MakeMaker
Requires:       %{name} = %{version}-%{release}

Conflicts:      %{realname}-perl

%description perl
Perl bindings for GDAL - Geo::GDAL, Geo::OGR and Geo::OSR modules.

################################################################################

%package python
Summary:        GDAL Python module
Group:          Development/Languages

BuildRequires:  python-devel python-setuptools python2-numpy

Requires:       python
Requires:       %{name} = %{version}-%{release}

Conflicts:      %{realname}-python

%description python
The GDAL python modules provide support to handle multiple GIS file formats.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%patch1 -p1
%patch2 -p0

%build
# Sanitize linebreaks
set +x
for f in $(find . -type f) ; do
  if file "$f" | grep -q CRLF ; then
    sed -i -e 's#\r##g' "$f"
  fi
done
set -x

%{__autoconf}

export CFLAGS="%{optflags} -fpic"

%configure \
    --prefix=%{install_dir} \
    --bindir=%{install_dir}/bin \
    --sbindir=%{install_dir}/sbin \
    --libdir=%{install_dir}/lib \
    --includedir=%{install_dir}/include \
    --datadir=%{install_dir}/share  \
    --datarootdir=%{install_dir}/share  \
    --disable-static \
    --disable-driver-elastic \
    --enable-shared \
    --with-threads \
    --with-armadillo \
    --with-curl \
    --with-expat \
    --with-freexl \
    --with-geos \
    --with-geotiff \
    --with-gif \
    --with-gta \
    --with-hdf4 \
    --with-hdf5 \
    --with-jpeg \
    --with-liblzma \
    --with-libtiff \
    --with-libz \
    --with-netcdf \
    --with-odbc \
    --with-ogdi \
    --with-openjpeg \
    --with-pcraster \
    --with-perl \
    --with-pg \
    --with-png \
    --with-python \
    --with-sqlite3 \
    --with-webp \
    --with-xerces=yes \
    --with-xerces-lib="-lxerces-c" \
    --with-xerces-inc=%{_includedir}/xercesc \
    --without-grass \
    --without-java \
    --without-jpeg12 \
    --without-libgrass \
    --without-pcraster \
    --with-cfitsio=no \
    --with-jpeg12=no

sed -i 's#^hardcode_libdir_flag_spec=.*#hardcode_libdir_flag_spec=""#g' libtool
sed -i 's#^runpath_var=LD_RUN_PATH#runpath_var=DIE_RPATH_DIE#g' libtool

# Fix linking with PG
sed -i "s#-Wl,-z,relro#-Wl,-z,relro,-rpath,%{pg_lib_dir}#" GDALmake.opt

%{__make} %{?_smp_mflags} lib-target apps-target

pushd swig/perl
  %{__make}
popd

pushd swig/python
  %{py_build}
popd

%install
rm -rf %{buildroot}

# Fix python installation path
sed -i "s#setup.py install#setup.py install --prefix=%{_prefix} --root=%{buildroot}#" swig/python/GNUmakefile

%{make_install}

rm -rf %{buildroot}%{install_lib_dir}/pkgconfig

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -pm 644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/

# Update configuration values
sed -i "s#{{VERSION}}#%{version}#g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i "s#{{PREFIX}}#%{install_dir}#g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i "s#{{LIBDIR}}#%{install_dir}/lib#g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i "s#{{INCLUDEDIR}}#%{install_dir}/include#g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Install linker configuration file
install -dm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-libs.conf

# Install prebuilt man files
install -dm 755 %{buildroot}%{install_man_dir}
install -pm 644 man/man1/* %{buildroot}%{install_man_dir}/

# Move Perl libs
mkdir -p %{buildroot}%{perl_vendorarch}
mv %{buildroot}%{_libdir32}/perl5/x86_64-linux-thread-multi/auto \
   %{buildroot}%{perl_vendorarch}/

rm -rf %{buildroot}%{_libdir32}/perl5/x86_64-linux-thread-multi

# Delete junk
find %{buildroot}%{perl_vendorarch}/auto -name '.packlist' -delete
find %{buildroot}%{perl_vendorarch}/auto -name '*.bs' -delete
find %{buildroot}%{perl_vendorarch}/auto -name '*.so' -exec chmod 0755 {} \;

# Install Perl pm files
mkdir %{buildroot}%{perl_vendorarch}/Geo
cp -rp swig/perl/lib/* %{buildroot}%{perl_vendorarch}/Geo/
find %{buildroot}%{perl_vendorarch}/Geo/ -name '*.dox' -delete

# Move Python package
mv %{buildroot}%{install_dir}/%{_lib}/python* \
   %{buildroot}%{_libdir}/

find %{buildroot}%{python_sitearch}/osgeo -name '*.so' -exec chmod 0755 {} \;

# Remove lib64 dir if empty
find %{buildroot}%{install_dir} -maxdepth 1 -type d -empty -delete

chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/GDAL.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GNM/GNM.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/OGR/OGR.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/OSR/OSR.so

chrpath --delete %{buildroot}%{install_bin_dir}/gdaladdo
chrpath --delete %{buildroot}%{install_bin_dir}/gdalbuildvrt
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_contour
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_create
chrpath --delete %{buildroot}%{install_bin_dir}/gdaldem
chrpath --delete %{buildroot}%{install_bin_dir}/gdalenhance
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_grid
chrpath --delete %{buildroot}%{install_bin_dir}/gdalinfo
chrpath --delete %{buildroot}%{install_bin_dir}/gdallocationinfo
chrpath --delete %{buildroot}%{install_bin_dir}/gdalmanage
chrpath --delete %{buildroot}%{install_bin_dir}/gdalmdiminfo
chrpath --delete %{buildroot}%{install_bin_dir}/gdalmdimtranslate
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_rasterize
chrpath --delete %{buildroot}%{install_bin_dir}/gdalsrsinfo
chrpath --delete %{buildroot}%{install_bin_dir}/gdaltindex
chrpath --delete %{buildroot}%{install_bin_dir}/gdaltransform
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_translate
chrpath --delete %{buildroot}%{install_bin_dir}/gdal_viewshed
chrpath --delete %{buildroot}%{install_bin_dir}/gdalwarp
chrpath --delete %{buildroot}%{install_bin_dir}/gnmanalyse
chrpath --delete %{buildroot}%{install_bin_dir}/gnmmanage
chrpath --delete %{buildroot}%{install_bin_dir}/nearblack
chrpath --delete %{buildroot}%{install_bin_dir}/ogr2ogr
chrpath --delete %{buildroot}%{install_bin_dir}/ogrinfo
chrpath --delete %{buildroot}%{install_bin_dir}/ogrlineref
chrpath --delete %{buildroot}%{install_bin_dir}/ogrtindex
chrpath --delete %{buildroot}%{install_bin_dir}/testepsg

chrpath --delete %{buildroot}%{install_lib_dir}/libgdal.so.*

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc NEWS PROVENANCE.TXT
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-libs.conf
%{install_dir}/share/%{realname}
%{install_bin_dir}/epsg_tr.py
%{install_bin_dir}/esri2wkt.py
%{install_bin_dir}/gcps2vec.py
%{install_bin_dir}/gcps2wld.py
%{install_bin_dir}/gdal-config
%{install_bin_dir}/gdal2tiles.py
%{install_bin_dir}/gdal2xyz.py
%{install_bin_dir}/gdal_auth.py
%{install_bin_dir}/gdal_calc.py
%{install_bin_dir}/gdal_contour
%{install_bin_dir}/gdal_create
%{install_bin_dir}/gdal_edit.py
%{install_bin_dir}/gdal_fillnodata.py
%{install_bin_dir}/gdal_grid
%{install_bin_dir}/gdal_merge.py
%{install_bin_dir}/gdal_pansharpen.py
%{install_bin_dir}/gdal_polygonize.py
%{install_bin_dir}/gdal_proximity.py
%{install_bin_dir}/gdal_rasterize
%{install_bin_dir}/gdal_retile.py
%{install_bin_dir}/gdal_sieve.py
%{install_bin_dir}/gdal_translate
%{install_bin_dir}/gdal_viewshed
%{install_bin_dir}/gdaladdo
%{install_bin_dir}/gdalbuildvrt
%{install_bin_dir}/gdalchksum.py
%{install_bin_dir}/gdalcompare.py
%{install_bin_dir}/gdaldem
%{install_bin_dir}/gdalenhance
%{install_bin_dir}/gdalident.py
%{install_bin_dir}/gdalimport.py
%{install_bin_dir}/gdalinfo
%{install_bin_dir}/gdallocationinfo
%{install_bin_dir}/gdalmanage
%{install_bin_dir}/gdalmdiminfo
%{install_bin_dir}/gdalmdimtranslate
%{install_bin_dir}/gdalmove.py
%{install_bin_dir}/gdalsrsinfo
%{install_bin_dir}/gdaltindex
%{install_bin_dir}/gdaltransform
%{install_bin_dir}/gdalwarp
%{install_bin_dir}/gnmanalyse
%{install_bin_dir}/gnmmanage
%{install_bin_dir}/mkgraticule.py
%{install_bin_dir}/nearblack
%{install_bin_dir}/ogr2ogr
%{install_bin_dir}/ogrinfo
%{install_bin_dir}/ogrlineref
%{install_bin_dir}/ogrmerge.py
%{install_bin_dir}/ogrtindex
%{install_bin_dir}/pct2rgb.py
%{install_bin_dir}/rgb2pct.py
%{install_bin_dir}/testepsg
%{install_lib_dir}/libgdal.so.*
%{install_man_dir}/%{realname}2tiles.1*
%{install_man_dir}/%{realname}addo.1*
%{install_man_dir}/%{realname}buildvrt.1*
%{install_man_dir}/%{realname}_calc.1*
%{install_man_dir}/%{realname}compare.1*
%{install_man_dir}/%{realname}_contour.1*
%{install_man_dir}/%{realname}_create.1*
%{install_man_dir}/%{realname}dem.1*
%{install_man_dir}/%{realname}_edit.1*
%{install_man_dir}/%{realname}_fillnodata.1*
%{install_man_dir}/%{realname}_grid.1*
%{install_man_dir}/%{realname}info.1*
%{install_man_dir}/%{realname}locationinfo.1*
%{install_man_dir}/%{realname}manage.1*
%{install_man_dir}/%{realname}mdiminfo.1*
%{install_man_dir}/%{realname}mdimtranslate.1*
%{install_man_dir}/%{realname}_merge.1*
%{install_man_dir}/%{realname}move.1*
%{install_man_dir}/%{realname}_pansharpen.1*
%{install_man_dir}/%{realname}_polygonize.1*
%{install_man_dir}/%{realname}_proximity.1*
%{install_man_dir}/%{realname}_rasterize.1*
%{install_man_dir}/%{realname}_retile.1*
%{install_man_dir}/%{realname}_sieve.1*
%{install_man_dir}/%{realname}srsinfo.1*
%{install_man_dir}/%{realname}tindex.1*
%{install_man_dir}/%{realname}transform.1*
%{install_man_dir}/%{realname}_translate.1*
%{install_man_dir}/%{realname}_viewshed.1*
%{install_man_dir}/%{realname}warp.1*
%{install_man_dir}/gnmanalyse.1*
%{install_man_dir}/gnmmanage.1*
%{install_man_dir}/nearblack.1*
%{install_man_dir}/ogr2ogr.1*
%{install_man_dir}/ogrinfo.1*
%{install_man_dir}/ogrlineref.1*
%{install_man_dir}/ogrmerge.1*
%{install_man_dir}/ogrtindex.1*
%{install_man_dir}/pct2rgb.1*
%{install_man_dir}/rgb2pct.1*

%files devel
%defattr(-,root,root)
%{install_bin_dir}/%{realname}-config
%{install_lib_dir}/libgdal.so
%{install_lib_dir}/libgdal.la
%{install_inc_dir}/*.h
%{install_man_dir}/%{realname}-config.1*
%{_libdir}/pkgconfig/%{name}.pc

%files perl
%defattr(-,root,root)
%{perl_vendorarch}/Geo
%{perl_vendorarch}/auto
%{_mandir}/man3/*

%files python
%defattr(-,root,root)
%{python_sitearch}/GDAL-*.egg-info
%{python_sitearch}/osgeo

################################################################################

%changelog
* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-1
- Minor spec improvements

* Sat Feb 13 2021 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Initial build
