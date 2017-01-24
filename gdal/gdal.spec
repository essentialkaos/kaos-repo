########################################################################################

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

%define _pyinclude        %{_includedir}/python2.6
%define _smp_mflags       -j1

########################################################################################

Summary:           GDAL/OGR - a translator library for raster and vector geospatial data formats
Name:              gdal
Version:           1.10.0
Release:           1%{?dist}
License:           MIT and BSD-3-Clause
Group:             Development/Libraries
URL:               http://www.gdal.org

Source0:           http://download.osgeo.org/%{name}/%{version}/%{name}-%{version}.tar.gz

Patch0:            %{name}-python_install.patch
Patch1:            %{name}-perl.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf >= 2.52 automake gcc-c++ doxygen >= 1.4.2 expat-devel
BuildRequires:     geos-devel >= 3 giflib-devel hdf-devel >= 4.0 libgeotiff-devel
BuildRequires:     libjpeg-turbo-devel libpng-devel libstdc++-devel libtiff-devel >= 3.6.0
BuildRequires:     libtool netcdf-devel blas-devel lapack-devel mysql-devel postgresql92-devel
BuildRequires:     libspatialite-devel python-setuptools ruby-devel sqlite-devel swig
BuildRequires:     unixODBC-devel libcurl-devel zlib-devel >= 1.1.4 xerces-c-devel
BuildRequires:     proj-devel m4 chrpath perl-ExtUtils-MakeMaker

Requires:          xerces-c

Provides:          %{name} = %{version}-%{release}

########################################################################################

%description
GDAL is a translator library for raster geospatial data formats that
is released under an Open Source license. As a library, it presents a
single abstract data model to the calling application for all
supported formats. The related OGR library (which lives within the
GDAL source tree) provides a similar capability for simple features
vector data.

########################################################################################

%package devel
Summary:           GDAL library header files
Group:             Development/Libraries
Requires:          %{name} = %{version}-%{release}

Requires:          hdf-devel >= 4.0 expat-devel geos-devel >= 3 libgeotiff-devel >= 1.2.1
Requires:          libjpeg-turbo-devel libpng-devel libstdc++-devel libtiff-devel
Requires:          netcdf-devel libspatialite-devel mysql-devel libcurl-devel
Requires:          postgresql92-devel sqlite-devel >= 3 unixODBC-devel xerces-c-devel
Requires:          giflib-devel 

%description devel
Development Libraries for the GDAL file format library

########################################################################################

%package perl
Summary:           Perl bindings for GDAL
Group:             Development/Languages
Requires:          %{name} = %{version}-%{release}

Requires:          perl perl-base perl-ExtUtils-MakeMaker

%description perl
Perl bindings for GDAL - Geo::GDAL, Geo::OGR and Geo::OSR modules.

########################################################################################

%package python
Summary:           GDAL Python module
Group:             Development/Languages
Requires:          %{name} = %{version}-%{release}

%description python
The GDAL python modules provide support to handle multiple GIS file formats.

########################################################################################

%prep
%setup -q

%patch0 -p1
%patch1 -p1

rm -rf man

%build
export PYTHON_INCLUDES=-I%{_pyinclude}

%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}

%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name} \
        --datadir=%{_datadir}/%{name}       \
        --with-rename-internal-libtiff-symbols=yes    \
        --with-rename-internal-libgeotiff-symbols=yes \
        --with-threads            \
        --disable-static          \
        --with-geotiff            \
        --with-libtiff            \
        --with-libz               \
        --with-cfitsio=no         \
        --with-netcdf             \
        --with-hdf4               \
        --with-geos               \
        --with-expat              \
        --with-png                \
        --with-gif                \
        --with-jpeg               \
        --with-odbc               \
        --with-mysql              \
        --with-spatialite         \
        --with-python             \
        --with-curl               \
        --with-pg                 \
        --with-ogdi               \
        --with-perl               \
        --with-xerces=yes         \
        --with-xerces-lib="-lxerces-c"         \
        --with-xerces-inc=/usr/include/xercesc \
        --without-pcraster  \
        --with-jpeg12=no    \
        --without-libgrass  \
        --without-grass     \
        --enable-shared

%{__make} %{?_smp_mflags} -C swig/perl generate
%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} docs
%{__make} %{?_smp_mflags} man

%install
rm -rf %{buildroot}

%{__make} %{?_smp_mflags} install install-man DESTDIR=%{buildroot} INST_MAN=%{_mandir}

rm -rf _html
cp -a html _html
cp -a ogr/html _html/ogr

# fix python installation path
sed -i 's|setup.py install|setup.py install --prefix=%{_prefix} --root=%{buildroot}|' swig/python/GNUmakefile

%{__make} DESTDIR=%{buildroot} install
%{__make} DESTDIR=%{buildroot} INST_MAN=%{_mandir} install-man

# cleanup junks
rm -rf %{buildroot}%{_includedir}/%{name}/%{name}
rm -rf %{buildroot}%{_bindir}/%{name}_sieve.dox
rm -rf %{buildroot}%{_bindir}/%{name}_fillnodata.dox

for junk in {.exists,.cvsignore} ; do
  find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/GDAL.so
chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/OGR/OGR.so
chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/OSR/OSR.so

chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/GDAL.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/OGR/OGR.so
chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/OSR/OSR.so

chrpath --delete %{buildroot}%{_bindir}/gdal_contour
chrpath --delete %{buildroot}%{_bindir}/gdallocationinfo
chrpath --delete %{buildroot}%{_bindir}/gdal_grid
chrpath --delete %{buildroot}%{_bindir}/gdal_rasterize
chrpath --delete %{buildroot}%{_bindir}/gdal_translate
chrpath --delete %{buildroot}%{_bindir}/gdaladdo
chrpath --delete %{buildroot}%{_bindir}/gdalbuildvrt
chrpath --delete %{buildroot}%{_bindir}/gdaldem
chrpath --delete %{buildroot}%{_bindir}/gdalenhance
chrpath --delete %{buildroot}%{_bindir}/gdalinfo
chrpath --delete %{buildroot}%{_bindir}/gdalmanage
chrpath --delete %{buildroot}%{_bindir}/gdalsrsinfo
chrpath --delete %{buildroot}%{_bindir}/gdaltindex
chrpath --delete %{buildroot}%{_bindir}/gdaltransform
chrpath --delete %{buildroot}%{_bindir}/gdalwarp
chrpath --delete %{buildroot}%{_bindir}/gdalserver
chrpath --delete %{buildroot}%{_bindir}/nearblack
chrpath --delete %{buildroot}%{_bindir}/ogr2ogr
chrpath --delete %{buildroot}%{_bindir}/ogrinfo
chrpath --delete %{buildroot}%{_bindir}/ogrtindex
chrpath --delete %{buildroot}%{_bindir}/testepsg

cp %{buildroot}%{python_sitearch}/osgeo/gdalnumeric.py* %{buildroot}%{python_sitearch}/

rm -f %{buildroot}%{_mandir}/man1/_*_BUILD_gdal*
rm -f %{buildroot}/usr/man/man1/*.1.gz

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

########################################################################################

%files
%defattr(-,root,root)
%doc NEWS PROVENANCE.TXT
%attr(755,root,root) %{_bindir}/epsg_tr.py
%attr(755,root,root) %{_bindir}/esri2wkt.py
%attr(755,root,root) %{_bindir}/gcps2vec.py
%attr(755,root,root) %{_bindir}/gcps2wld.py
%attr(755,root,root) %{_bindir}/gdal2tiles.py
%attr(755,root,root) %{_bindir}/gdal_edit.py
%attr(755,root,root) %{_bindir}/gdalmove.py
%attr(755,root,root) %{_bindir}/gdal_auth.py
%attr(755,root,root) %{_bindir}/gdal2xyz.py
%attr(755,root,root) %{_bindir}/gdal_calc.py
%attr(755,root,root) %{_bindir}/gdal_fillnodata.py
%attr(755,root,root) %{_bindir}/gdal_merge.py
%attr(755,root,root) %{_bindir}/gdal_polygonize.py
%attr(755,root,root) %{_bindir}/gdal_proximity.py
%attr(755,root,root) %{_bindir}/gdal_retile.py
%attr(755,root,root) %{_bindir}/gdal_sieve.py
%attr(755,root,root) %{_bindir}/gdalchksum.py
%attr(755,root,root) %{_bindir}/gdalident.py
%attr(755,root,root) %{_bindir}/gdalimport.py
%attr(755,root,root) %{_bindir}/mkgraticule.py
%attr(755,root,root) %{_bindir}/pct2rgb.py
%attr(755,root,root) %{_bindir}/rgb2pct.py
%attr(755,root,root) %{_bindir}/gdal_contour
%attr(755,root,root) %{_bindir}/gdallocationinfo
%attr(755,root,root) %{_bindir}/gdal_grid
%attr(755,root,root) %{_bindir}/gdal_rasterize
%attr(755,root,root) %{_bindir}/gdal_translate
%attr(755,root,root) %{_bindir}/gdaladdo
%attr(755,root,root) %{_bindir}/gdalbuildvrt
%attr(755,root,root) %{_bindir}/gdaldem
%attr(755,root,root) %{_bindir}/gdalenhance
%attr(755,root,root) %{_bindir}/gdalinfo
%attr(755,root,root) %{_bindir}/gdalmanage
%attr(755,root,root) %{_bindir}/gdalsrsinfo
%attr(755,root,root) %{_bindir}/gdaltindex
%attr(755,root,root) %{_bindir}/gdaltransform
%attr(755,root,root) %{_bindir}/gdalwarp
%attr(755,root,root) %{_bindir}/gdalserver
%attr(755,root,root) %{_bindir}/nearblack
%attr(755,root,root) %{_bindir}/ogr2ogr
%attr(755,root,root) %{_bindir}/ogrinfo
%attr(755,root,root) %{_bindir}/ogrtindex
%attr(755,root,root) %{_bindir}/testepsg
%{_datadir}/%{name}
%{_mandir}/man1/gdalmanage.1*
%{_mandir}/man1/gdal_edit.1*
%{_mandir}/man1/gdal_polygonize.1*
%{_mandir}/man1/gdal_proximity.1*
%{_mandir}/man1/gdalbuildvrt.1*
%{_mandir}/man1/gdalmove.1*
%{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/gdal_contour.1*
%{_mandir}/man1/gdal_fillnodata.1*
%{_mandir}/man1/gdal_grid.1*
%{_mandir}/man1/gdal_merge.1*
%{_mandir}/man1/gdal_rasterize.1*
%{_mandir}/man1/gdal_retile.1*
%{_mandir}/man1/gdal_sieve.1*
%{_mandir}/man1/gdal_translate.1*
%{_mandir}/man1/gdal_utilities.1*
%{_mandir}/man1/gdallocationinfo.1*
%{_mandir}/man1/gdaladdo.1*
%{_mandir}/man1/gdaldem.1*
%{_mandir}/man1/gdalinfo.1*
%{_mandir}/man1/gdaltindex.1*
%{_mandir}/man1/gdaltransform.1*
%{_mandir}/man1/gdalwarp.1*
%{_mandir}/man1/nearblack.1*
%{_mandir}/man1/ogr2ogr.1*
%{_mandir}/man1/ogr_utilities.1*
%{_mandir}/man1/ogrinfo.1*
%{_mandir}/man1/ogrtindex.1*
%{_mandir}/man1/pct2rgb.1*
%{_mandir}/man1/rgb2pct.1*
%{_libdir}/libgdal.so.*

%files devel
%defattr(-,root,root)
%doc _html/*
%attr(755,root,root) %{_bindir}/%{name}-config
%attr(755,root,root) %{_libdir}/libgdal.so
%{_libdir}/libgdal.la
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_mandir}/man1/%{name}-config.1*
%{_mandir}/man1/gdalsrsinfo.1.gz

%files perl
%defattr(-,root,root)
%{perl_vendorarch}/Geo/GDAL.pm
%dir %{perl_vendorarch}/Geo/GDAL
%{perl_vendorarch}/Geo/GDAL/Const.pm
%{perl_vendorarch}/Geo/OGR.pm
%{perl_vendorarch}/Geo/OSR.pm
%attr(755,root,root) %{_bindir}/*.dox
%dir %{perl_vendorarch}/Geo
%dir %{perl_vendorarch}/auto/Geo
%dir %{perl_vendorarch}/auto/Geo/GDAL
%attr(755,root,root) %{perl_vendorarch}/auto/Geo/GDAL/GDAL.so
%dir %{perl_vendorarch}/auto/Geo/GDAL/Const
%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
%dir %{perl_vendorarch}/auto/Geo/OGR
%{perl_vendorarch}/auto/Geo/GDAL/GDAL.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Geo/OGR/OGR.so
%dir %{perl_vendorarch}/auto/Geo/OSR
%{perl_vendorarch}/auto/Geo/OSR/OSR.bs
%{perl_vendorarch}/auto/Geo/OGR/OGR.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Geo/OSR/OSR.so
%exclude %{perl_archlib}/perllocal.pod
%exclude %{perl_vendorarch}/auto/Geo/*/.packlist
%exclude %{perl_vendorarch}/auto/Geo/GDAL/Const/.packlist

%files python
%defattr(-,root,root)
%{python_sitearch}/%{name}.py*
%{python_sitearch}/gdalconst.py*
%{python_sitearch}/gdalnumeric.py*
%{python_sitearch}/ogr.py*
%{python_sitearch}/osr.py*
%{python_sitearch}/GDAL-*.egg-info
%dir %{python_sitearch}/osgeo
%attr(755,root,root) %{python_sitearch}/osgeo/_gdal.so
%attr(755,root,root) %{python_sitearch}/osgeo/_gdalconst.so
%attr(755,root,root) %{python_sitearch}/osgeo/_ogr.so
%attr(755,root,root) %{python_sitearch}/osgeo/_osr.so
%{python_sitearch}/osgeo/*.py*

########################################################################################

%changelog
* Sat Nov 14 2015 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-2
- Spec improvements

* Tue Sep 16 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-1
- Small fixes in spec file

* Sat Sep 06 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- Initial build
