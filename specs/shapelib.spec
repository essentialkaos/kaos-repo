################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        C library for handling ESRI Shapefiles
Name:           shapelib
Version:        1.6.1
Release:        0%{?dist}
License:        (LGPLv2+ or MIT) and GPLv2+ and Public Domain
Group:          Development/Libraries
URL:            http://shapelib.maptools.org

Source0:        https://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++ make chrpath

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
The Shapefile C Library provides the ability to write simple C programs for
reading, writing and updating (to a limited extent) ESRI Shapefiles, and
the associated attribute file (.dbf).

################################################################################

%package devel
Summary:  Development files for shapelib
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
This package contains libshp and the appropriate header files.

################################################################################

%package tools
Summary:  shapelib utility programs
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description tools
This package contains various utility programs distributed with shapelib.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} -name '*.la' -exec rm -f {} ';'

chrpath --delete %{buildroot}%{_bindir}/*
chrpath --delete %{buildroot}%{_libdir}/*.so*

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc README README.tree ChangeLog web/*.html LICENSE-LGPL LICENSE-MIT
%{_libdir}/libshp.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/shapefil.h
%{_libdir}/libshp.so
%{_libdir}/pkgconfig/%{name}.pc

%files tools
%defattr(-,root,root,-)
%doc contrib/doc/
%{_bindir}/csv2shp
%{_bindir}/dbfadd
%{_bindir}/dbfcat
%{_bindir}/dbfcreate
%{_bindir}/dbfdump
%{_bindir}/dbfinfo
%{_bindir}/Shape_PointInPoly
%{_bindir}/shpadd
%{_bindir}/shpcat
%{_bindir}/shpcentrd
%{_bindir}/shpcreate
%{_bindir}/shpdata
%{_bindir}/shpdump
%{_bindir}/shpdxf
%{_bindir}/shpfix
%{_bindir}/shpinfo
%{_bindir}/shprewind
%{_bindir}/shpsort
%{_bindir}/shptreedump
%{_bindir}/shputils
%{_bindir}/shpwkb

################################################################################

%changelog
* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- DBFIsValueNULL(): accept empty string as NULL Date
- DBFIsValueNULL(): Accept string containing of width times "0" as NULL Date
- Only test for _WIN32 for Windows detection
- Windows: Fix UTF8 hook functions
- Various compiler warning fixes
- contrib/csv2shp.c: fix resource leaks
- Detect byte order at compile time
- shapefil.h: various const-correctness improvements
- shapefil.h: Remove SHPTreeRemoveShapeId not being implemented
- shapefil.h: Fix API call of SHPSearchDiskTreeEx
- Add API functions for read/write of date attributes:
  DBFReadDateAttribute/DBFWriteDateAttribute
- DBFWriteAttribute/DBFWriteLogicalAttribute: no longer silently accpets
  invalid input, but returns false
- DBFCloneEmpty: consider the SAHooks
- Move endian defines to shapefil_private.h
- Fix test execution by complete refactoring.
- Add C++ unit testing
- SBNOpenDiskTree(): make it work with node descriptors with non-increasing
  nBinStart
- sbnsearch.c: avoid potential integer overflows on corrupted files
- dbfdump: dump date and logical fields
- dbfinfo: print date and logical fields
- dbfcat: various fixes
- Fix -Werror=calloc-transposed-args with gcc 14
- SHPOpenLL(): avoid GDAL specific error message when .shx is missing
- CMake: generate pkg-config file
- CMake: Fix install interface include dir
- CMake: Make building executables optional with CMake (set BUILD_APPS to OFF)
- CMake: Remove duplicated shapefil.h installation in include_dir/shapelib
- CMake: Remove INSTALL_NAME_DIR from target
- CMake: Fix contrib.cmake
- CMake: (>= 3.21) Fix ctest paths for shared libs (MSVC and CygWin)
- CMake: Add GoogleTestAdapter (GTA) Run Settings

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- shapefil.h: add SHAPELIB_VERSION_MAJOR/MINOR/MICRO, SHAPELIB_VERSION_NUMBER,
  and SHAPELIB_AT_LEAST macros
- Compiler warning fixes and various code cleanups
- SAHooks: add a void *pvUserData member. ABI change
- SAHooks.FOpen and FClose callbacks: add a void *pvUserData parameter. API and
  ABI change
- SAHooks.FWrite: make first parameter a const void*. API change
- Distribute LICENSE-LGPL and LICENSE-MIT files instead of COPYING file. Do not
  distribute INSTALL file
- Use standard integer data types
- Changes to allow building with cmake -DCMAKE_UNITY_BUILD=ON
- Polygon writing: avoid considering rings slightly overlapping as inner-outer
  rings of others
- Polygon writing: consider rings at non-constant Z as outer rings
  (fixes OSGeo/gdal#5315) As noted in code comments, this is an approximation of
  more complicated tests we'd likely have to do, that would take into account
  real co-planar testing, to allow detecting inner rings of outer rings in an
  oblique plane.
- shpopen.c: Communicate why the file size cannot be reached when appending
  features. Clearly state why the file size cannot be reached.
  This is important in order to correctly inform the user and prevent him/her
  from looking for other reasons.
- SHPWriteObject(): prevent potential overflows on 64-bit platforms on huge
  geometries
- SHPRestoreSHX: update SHX content length even if error occurred
- In creation, uses w+b file opening mode instead of wb followed by r+b, to
  support network file systems having sequential write only and when using
  CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE=YES
- Fix adding features in a .dbf without columns
- Have matching SOVERSION for CMake and autotools
- Code reformatting
- Enable contrib/csv2shp build with MSVC
- Build contributed utilities via CMake
- Use the the standard BUILD_TESTING CMake variable
- Remove double free() in contrib/shpsrt (CVE-2022-0699)
- SHPRestoreSHX: fix for (64 bit) big endian
- Add config-style support for find_package(shapefile)
- Prevent no-op FSeeks writing dbf & shp records for network filesystem
  performance

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Add FTDate entry in DBFFieldType
- Remove PROJ.4 dependency and functionality, causing removal of SHPProject(),
  SHPSetProjection() and SHPFreeProjection() from contrib/shpgeo.h, and removal
  of the contrib shpproj utility
- shpopen.c: avoid being dependent on correctness of file size field in .shp

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- Fix a regression regarding re-writing the last shape of a file

* Thu Sep 07 2017 Gleb Goncharov <inbox@gongled.ru> - 1.4.0-0
- Initial build
