################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Library providing BSD-compatible functions for portability
Name:           libbsd
Version:        0.12.2
Release:        0%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            https://libbsd.freedesktop.org

Source0:        https://libbsd.freedesktop.org/releases/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ automake libtool autoconf >= 2.67 libmd-devel

Requires:       libmd

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

################################################################################

%package devel
Summary:  Header files for libbsd package
Group:    Development/Libraries

Requires:  %{name} = %{version}
Requires:  libmd-devel

%description devel
Header files and package configs for libbsd package.

################################################################################

%package ctor-static
Summary:  Development files for libbsd
Group:    Development/Libraries

Requires:  %{name} = %{version}
Requires:  %{name}-devel = %{version}

%description ctor-static
The libbsd-ctor static library is required if setproctitle() is to be used
when libbsd is loaded via dlopen() from a threaded program.  This can be
configured using "pkg-config --libs libbsd-ctor".

################################################################################

%prep
%{crc_check}

%setup -q
echo %{version} > .dist-version

%build
./autogen
%configure --disable-static

%{__make} CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
rm -rf %{buildroot}

%{make_install} libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot}

find %{buildroot}%{_libdir} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING
%{_libdir}/%{name}.so
%{_libdir}/%{name}.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-overlay.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%files ctor-static
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}-ctor.pc
%{_libdir}/%{name}-ctor.a

################################################################################

%changelog
* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 0.12.2-0
- https://gitlab.freedesktop.org/libbsd/libbsd/-/compare/0.11.7...0.12.2

* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 0.11.7-0
- https://gitlab.freedesktop.org/libbsd/libbsd/-/compare/0.11.6...0.11.7

* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 0.11.6-0
- https://gitlab.freedesktop.org/libbsd/libbsd/-/compare/0.10.0...0.11.6

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- Updated to the latest stable release

* Mon Aug 06 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.9.1-0
- Initial build
