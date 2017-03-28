###############################################################################

%{!?_without_check: %define _with_check 1}

###############################################################################

Summary:         Library for country/city/organization to IP address or hostname mapping
Name:            GeoIP
Version:         1.6.9
Release:         0%{?dist}
Group:           Development/Libraries
License:         LGPLv2+
URL:             http://www.maxmind.com/app/c

Source0:         https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc zlib-devel

Requires:        MMGeoIP MMGeoIP-IPV6

Obsoletes:       geoip < %{version}-%{release}
Provides:        geoip = %{version}-%{release}
Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from.

It uses file based databases that can optionally be updated on a weekly basis
by installing the geoipupdate-cron (IPv4) and/or geoipupdate-cron6 (IPv6)
packages.

###############################################################################

%package devel
Summary:         Development headers and libraries for GeoIP
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}

%if 0%{?fedora} < 11 || 0%{?rhel} < 6
Requires:        pkgconfig
%endif

Provides:        geoip-devel = %{version}-%{release}
Obsoletes:       geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications.

###############################################################################

%prep
%setup -q

%build
%configure --disable-static --disable-dependency-tracking

# Kill bogus rpaths
sed -i -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
  -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

# nix the stuff we don't need like .la files.
rm -f %{buildroot}%{_libdir}/*.la

%check
%if %{?_with_check:1}%{?_without_check:0}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%{__make} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

###############################################################################

%files
%doc COPYING AUTHORS ChangeLog NEWS.md README.md
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1
%{_libdir}/libGeoIP.so.1.*
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*

%files devel
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc

###############################################################################

%changelog
* Sat Mar 25 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6.9-0
- Initial build for kaos repository
