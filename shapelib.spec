###############################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0002

###############################################################################

Summary:         C library for handling ESRI Shapefiles
Name:            shapelib
Version:         1.4.0
Release:         0%{?dist}
License:         (LGPLv2+ or MIT) and GPLv2+ and Public Domain
Group:           Development/Libraries
URL:             http://shapelib.maptools.org/

Source:          http://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc-c++ make proj-devel

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

###############################################################################

%package devel
Summary:         Development files for shapelib
Requires:        %{name} = %{version}-%{release}

%description devel
This package contains libshp and the appropriate header files.

###############################################################################

%package tools
Summary:         shapelib utility programs
Requires:        %{name} = %{version}-%{release}

%description tools
This package contains various utility programs distributed with shapelib.

###############################################################################

%prep
%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install}

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

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

###############################################################################

%changelog
* Thu Sep 07 2017 Gleb Goncharov <inbox@gongled.ru> - 1.4.0-0
- Initial build.

