################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:         C library for handling ESRI Shapefiles
Name:            shapelib
Version:         1.5.0
Release:         0%{?dist}
License:         (LGPLv2+ or MIT) and GPLv2+ and Public Domain
Group:           Development/Libraries
URL:             http://shapelib.maptools.org/

Source0:         https://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc-c++ make chrpath

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

################################################################################

%package devel
Summary:         Development files for shapelib
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

%description devel
This package contains libshp and the appropriate header files.

################################################################################

%package tools
Summary:         shapelib utility programs
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

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
%doc README README.tree ChangeLog web/*.html COPYING
%{_libdir}/libshp.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/shapefil.h
%{_libdir}/libshp.so
%{_libdir}/pkgconfig/%{name}.pc

%files tools
%defattr(-,root,root,-)
%doc contrib/doc/
%{_bindir}/*

################################################################################

%changelog
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
