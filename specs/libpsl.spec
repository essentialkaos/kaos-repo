################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        C library for the Publix Suffix List
Name:           libpsl
Version:        0.21.2
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://rockdaboot.github.io/libpsl

Source0:        https://github.com/rockdaboot/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make autoconf automake gettext-devel glib2-devel
BuildRequires:  libicu-devel libtool libxslt chrpath python3

Provides:       %{name} = %{version}-%{release}

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
Summary:  Development files for %{name}
Group:    Development/Tools

Requires:  %{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%package -n psl
Summary:  Commandline utility to explore the Public Suffix List
Group:    Development/Tools

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
[[ -f configure ]] || autoreconf -fiv

%configure --disable-silent-rules \
           --disable-static \
           --enable-man

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} -name '*.la' -delete -print

chrpath --delete %{buildroot}%{_bindir}/psl

%check
%if %{?_with_check:1}%{?_without_check:0}
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
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libpsl.so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS NEWS
%{_datadir}/gtk-doc/html/libpsl/
%{_includedir}/libpsl.h
%{_libdir}/libpsl.so
%{_libdir}/pkgconfig/libpsl.pc

%files -n psl
%defattr(-,root,root,-)
%doc AUTHORS NEWS COPYING
%{_bindir}/psl
%{_mandir}/man1/psl*

################################################################################

%changelog
* Sat Oct 14 2023 Anton Novojilov <andy@essentialkaos.com> - 0.21.2-0
- https://github.com/rockdaboot/libpsl/releases/tag/0.21.2

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.21.1-0
- https://github.com/rockdaboot/libpsl/releases/tag/0.21.1

* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.20.2-0
- https://github.com/rockdaboot/libpsl/releases/tag/0.20.2

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.17.0-0
- https://github.com/rockdaboot/libpsl/releases/tag/0.17.0

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 0.15.0-0
- Initial build for kaos repo
