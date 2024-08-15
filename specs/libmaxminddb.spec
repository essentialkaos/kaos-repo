################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        C library for the MaxMind DB file format
Name:           libmaxminddb
Version:        1.10.0
Release:        0%{?dist}
License:        Apache-2.0
Group:          Development/Libraries
URL:            https://github.com/maxmind/libmaxminddb

Source0:        https://github.com/maxmind/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc chrpath

%if 0%{?rhel} == 9
BuildRequires:  perl-FindBin
%endif

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
The libmaxminddb library provides a C library for reading MaxMind DB files,
including the GeoIP2 databases from MaxMind. This is a custom binary format
designed to facilitate fast lookups of IP addresses while allowing for great
flexibility in the type of data associated with an address.

################################################################################

%package devel
Summary:  Development headers and libraries for libmaxminddb
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
Development headers and static libraries for building libmaxminddb-based
applications.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

# Remove hardcoded rpath from binary
chrpath --delete %{buildroot}%{_bindir}/mmdblookup

%check
%if %{?_with_check:1}%{?_without_check:0}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%{__make} check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc LICENSE AUTHORS NOTICE Changes.md README.md
%{_bindir}/mmdblookup
%{_libdir}/%{name}.so.*
%{_mandir}/man1/mmdblookup.1.gz
%{_mandir}/man3/MMDB_*.3.gz
%{_mandir}/man3/%{name}.3.gz

%files devel
%defattr(-,root,root)
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_libdir}/%{name}.a
%{_libdir}/%{name}.la
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- https://github.com/maxmind/libmaxminddb/releases/tag/1.10.0

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- https://github.com/maxmind/libmaxminddb/releases/tag/1.9.1

* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- https://github.com/maxmind/libmaxminddb/releases/tag/1.7.1

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Initial build for EK repository
