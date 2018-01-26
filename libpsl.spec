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

################################################################################

Summary:            C library for the Publix Suffix List
Name:               libpsl
Version:            0.17.0
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://rockdaboot.github.io/libpsl

Source0:            https://github.com/rockdaboot/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make autoconf automake gettext-devel glib2-devel gtk-doc
BuildRequires:      libicu-devel libtool libxslt chrpath

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

################################################################################

%package devel
Summary:            Development files for %{name}
Group:              Development/Tools
Requires:           %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%package -n psl
Summary:            Commandline utility to explore the Public Suffix List
Group:              Development/Tools

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
[ -f configure ] || autoreconf -fiv
%configure --disable-silent-rules \
           --disable-static \
           --enable-man \
           --enable-gtk-doc

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} -name '*.la' -delete -print

chrpath --delete %{buildroot}%{_bindir}/psl

%check
%{__make} check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

################################################################################

%files
%defattr(-, root, root, -)
%doc COPYING
%{_libdir}/libpsl.so.*

%files devel
%defattr(-, root, root, -)
%doc AUTHORS NEWS
%{_datadir}/gtk-doc/html/libpsl/
%{_includedir}/libpsl.h
%{_libdir}/libpsl.so
%{_libdir}/pkgconfig/libpsl.pc
%{_mandir}/man3/libpsl.3*

%files -n psl
%defattr(-, root, root, -)
%doc AUTHORS NEWS COPYING
%{_bindir}/psl
%{_mandir}/man1/psl*

################################################################################

%changelog
* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.17.0-0
- Updated to latest stable release

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 0.15.0-0
- Initial build for kaos repo
