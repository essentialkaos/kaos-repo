###############################################################################

Summary:         Main loop abstraction library
Name:            libverto
Version:         0.3.0
Release:         0%{?dist}
License:         MIT
Group:           Development/Libraries
URL:             https://github.com/latchset/libverto

Source:          https://github.com/latchset/libverto/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc glib2-devel libtevent-devel chrpath

%if !0%{?rhel}
BuildRequires:   libev-devel
%endif

%if 0%{?rhel} <= 6
BuildRequires:   libevent2-devel
%else
BuildRequires:   libevent-devel
%endif

Provides:        %{name} = %{version}-%{release}

###############################################################################

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

###############################################################################

%package devel

Summary:         Development files for %{name}
Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

###############################################################################

%package glib

Summary:         glib module for %{name}
Requires:        %{name} = %{version}-%{release}

%description glib
Module for %{name} which provides integration with glib.

This package does NOT yet provide %{name}-module-base.

###############################################################################

%package glib-devel

Summary:         Development files for %{name}-glib
Requires:        %{name}-glib = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}

%description    glib-devel
The %{name}-glib-devel package contains libraries and header files for
developing applications that use %{name}-glib.

###############################################################################

%package libevent

Summary:         libevent module for %{name}
Requires:        %{name} = %{version}-%{release}
Provides:        %{name}-module-base = %{version}-%{release}

%description libevent
Module for %{name} which provides integration with libevent.

###############################################################################

%package libevent-devel

Summary:         Development files for %{name}-libevent
Requires:        %{name}-libevent = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}

%description libevent-devel
The %{name}-libevent-devel package contains libraries and header files for
developing applications that use %{name}-libevent.

###############################################################################

%package tevent

Summary:         tevent module for %{name}
Requires:        %{name} = %{version}-%{release}
Provides:        %{name}-module-base = %{version}-%{release}

%description tevent
Module for %{name} which provides integration with tevent.

This package provides %{name}-module-base since it supports io, timeout
and signal.

###############################################################################

%package tevent-devel

Summary:         Development files for %{name}-tevent
Requires:        %{name}-tevent = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}

%description tevent-devel
The %{name}-tevent-devel package contains libraries and header files for
developing applications that use %{name}-tevent.

###############################################################################

%if !0%{?rhel}
%package libev

Summary:         libev module for %{name}
Requires:        %{name} = %{version}-%{release}
Provides:        %{name}-module-base = %{version}-%{release}

%description libev
Module for %{name} which provides integration with libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

###############################################################################

%package libev-devel

Summary:         Development files for %{name}-libev
Requires:        %{name}-libev = %{version}-%{release}
Requires:        %{name}-devel = %{version}-%{release}

%description libev-devel
The %{name}-libev-devel package contains libraries and header files for
developing applications that use %{name}-libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.
%endif

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

%post tevent
/sbin/ldconfig
%postun tevent
/sbin/ldconfig

%if !0%{?rhel}
%post libev
/sbin/ldconfig
%postun libev
/sbin/ldconfig
%endif

###############################################################################

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

%files tevent
%defattr(-,root,root)
%{_libdir}/%{name}-tevent.so.*

%files tevent-devel
%defattr(-,root,root)
%{_includedir}/verto-tevent.h
%{_libdir}/%{name}-tevent.so
%{_libdir}/pkgconfig/%{name}-tevent.pc

%if !0%{?rhel}
%files libev
%defattr(-,root,root)
%{_libdir}/%{name}-libev.so.*

%files libev-devel
%defattr(-,root,root)
%{_includedir}/verto-libev.h
%{_libdir}/%{name}-libev.so
%{_libdir}/pkgconfig/%{name}-libev.pc
%endif

###############################################################################

%changelog
* Wed Nov 22 2017 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- Initial build for kaos-repo
