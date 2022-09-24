################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:         Main loop abstraction library
Name:            libverto
Version:         0.3.2
Release:         0%{?dist}
License:         MIT
Group:           Development/Libraries
URL:             https://github.com/latchset/libverto

Source:          https://github.com/latchset/libverto/releases/download/%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc glib2-devel libevent-devel libev-devel chrpath

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
libverto provides a way for libraries to expose asynchronous interfaces
without having to choose a particular event loop, offloading this
decision to the end application which consumes the library.

If you are packaging an application, not library, based on libverto,
you should depend either on a specific implementation module or you
can depend on the virtual provides 'libverto-module-base'. This will
ensure that you have at least one module installed that provides io,
timeout and signal functionality. Currently glib is the only module
that does not provide these three because it lacks signal. However,
glib will support signal in the future.

################################################################################

%package devel

Summary:         Development files for %{name}
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%package glib

Summary:         glib module for %{name}
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

%description glib
Module for %{name} which provides integration with glib.

This package does NOT yet provide %{name}-module-base.

################################################################################

%package glib-devel

Summary:         Development files for %{name}-glib
Group:           Development/Libraries

Requires:        %{name}-glib = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}
Requires:        pkgconfig(glib-2.0)

%description    glib-devel
The %{name}-glib-devel package contains libraries and header files for
developing applications that use %{name}-glib.

################################################################################

%package libevent

Summary:         libevent module for %{name}
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}
Provides:        %{name}-module-base = %{version}-%{release}

%description libevent
Module for %{name} which provides integration with libevent.

################################################################################

%package libevent-devel

Summary:         Development files for %{name}-libevent
Group:           Development/Libraries

Requires:        %{name}-libevent = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}
Requires:        pkgconfig(libevent)

%description libevent-devel
The %{name}-libevent-devel package contains libraries and header files for
developing applications that use %{name}-libevent.

################################################################################

%package libev

Summary:         libev module for %{name}
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}
Provides:        %{name}-module-base = %{version}-%{release}

%description libev
Module for %{name} which provides integration with libev.

################################################################################

%package libev-devel

Summary:         Development files for %{name}-libev
Group:           Development/Libraries
Requires:        %{name}-libev = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}
Requires:        pkgconfig(libev)

%description libev-devel
The %{name}-libev-devel package contains libraries and header files for
developing applications that use %{name}-libev.

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

chrpath --delete %{buildroot}%{_libdir}/*.so.*

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%post glib
/sbin/ldconfig
%postun glib
/sbin/ldconfig

%post libevent
/sbin/ldconfig
%postun libevent
/sbin/ldconfig

%post libev
/sbin/ldconfig
%postun libev
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/verto.h
%{_includedir}/verto-module.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files glib
%defattr(-,root,root)
%{_libdir}/%{name}-glib.so.*

%files glib-devel
%defattr(-,root,root)
%{_includedir}/verto-glib.h
%{_libdir}/%{name}-glib.so
%{_libdir}/pkgconfig/%{name}-glib.pc

%files libevent
%defattr(-,root,root)
%{_libdir}/%{name}-libevent.so.*

%files libevent-devel
%defattr(-,root,root)
%{_includedir}/verto-libevent.h
%{_libdir}/%{name}-libevent.so
%{_libdir}/pkgconfig/%{name}-libevent.pc

%files libev
%defattr(-,root,root)
%{_libdir}/%{name}-libev.so.*

%files libev-devel
%defattr(-,root,root)
%{_includedir}/verto-libev.h
%{_libdir}/%{name}-libev.so
%{_libdir}/pkgconfig/%{name}-libev.pc

################################################################################

%changelog
* Thu Sep 22 2022 Anton Novojilov <andy@essentialkaos.com> - 0.3.2-0
- Fix use-after-free in verto_reinitialize()
- Fix use-after-free in verto_free()
- Remove broken tevent support

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 0.3.1-1
- Rebuilt with the latest version of libevent

* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 0.3.1-0
- Fix rare leak of DSO in module_load
- Turn off -Wcast-function-type
- Work around libev not being c89-compliant

* Fri Dec 08 2017 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-1
- Improved spec

* Wed Nov 22 2017 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- Initial build for kaos-repo
