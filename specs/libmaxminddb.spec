################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

%define __ldconfig        %{_sbin}/ldconfig

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         C library for the MaxMind DB file format
Name:            libmaxminddb
Version:         1.6.0
Release:         0%{?dist}
License:         Apache-2.0
Group:           Development/Libraries
URL:             https://github.com/maxmind/libmaxminddb

Source0:         https://github.com/maxmind/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc chrpath

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The libmaxminddb library provides a C library for reading MaxMind DB files,
including the GeoIP2 databases from MaxMind. This is a custom binary format
designed to facilitate fast lookups of IP addresses while allowing for great
flexibility in the type of data associated with an address.

################################################################################

%package devel
Summary:         Development headers and libraries for libmaxminddb
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}

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

%post
%{__ldconfig}

%postun
%{__ldconfig}

%clean
rm -rf %{buildroot}

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
* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Initial build for EK repository
