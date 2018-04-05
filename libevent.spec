################################################################################

Summary:              Abstract asynchronous event notification library
Name:                 libevent
Version:              1.4.15
Release:              0%{?dist}
License:              BSD
Group:                System Environment/Libraries
URL:                  http://libevent.org/

Source:               https://github.com/libevent/libevent/archive/release-%{version}-stable.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc make automake libtool doxygen openssl-devel

################################################################################

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

################################################################################

%package devel
Summary:              Header files, libraries and development documentation for %{name}
Group:                Development/Libraries
Requires:             %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

################################################################################

%package doc
Summary:              Development documentation for %{name}
Group:                Development/Libraries
Requires:             %{name}-devel = %{version}-%{release}
BuildArch:            noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}-devel, you will
need to install %{name}-doc.

################################################################################

%prep
%setup -qn %{name}-release-%{version}-stable

%build
./autogen.sh

%configure --disable-dependency-tracking --disable-static

%{__make} %{?_smp_mflags} all

%{__make} doxygen

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la

install -dm 755 %{buildroot}%{_docdir}/%{name}-devel-%{version}/html
install -dm 755 %{buildroot}%{_docdir}/%{name}-devel-%{version}/sample

chmod +x doxygen/html

cp -r doxygen/html/* %{buildroot}%{_docdir}/%{name}-devel-%{version}/html/
cp -r sample/*.c %{buildroot}%{_docdir}/%{name}-devel-%{version}/sample/
cp -r sample/Makefile* %{buildroot}%{_docdir}/%{name}-devel-%{version}/sample/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/%{name}-*.so.*
%{_libdir}/%{name}_core-*.so.*
%{_libdir}/%{name}_extra-*.so.*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}_core.so
%{_libdir}/%{name}_extra.so
%{_includedir}/event-config.h
%{_mandir}/man3/evdns.3.gz
%{_mandir}/man3/event.3.gz
%{_bindir}/event_rpcgen.*

%files doc
%defattr(-,root,root,0644)
%{_docdir}/%{name}-devel-%{version}/html/*
%{_docdir}/%{name}-devel-%{version}/sample/*

################################################################################

%changelog
* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.15-0
- Avoid integer overflow bugs in evbuffer_add() and related functions.
  See CVE-2014-6272 advisory for more information.
- Pass flags to fcntl(F_SETFL) as int, not long
- Backport and tweak the LICENSE file for 1.4
- set close-on-exec bit for filedescriptors created by dns subsystem
- Replace unused case of FD_CLOSEONEXEC with a proper null statement.
- Fix kqueue correctness test on x84_64
- Avoid deadlock when activating signals.
- Backport doc fix for evhttp_bind_socket.
- Fix an issue with forking and signal socketpairs in select/poll backends
- Fix compilation on Visual Studio 2010
- Defensive programming to prevent (hopefully impossible) stack-stomping
- Check for POLLERR, POLLHUP and POLLNVAL for Solaris event ports
- Fix a bug that could allow dns requests with duplicate tx ids
- Avoid truncating huge values for content-length
- Take generated files out of git; add correct m4 magic for libtool to
  auto* files
- Prefer autoregen -ivf to manual autogen.sh

* Tue Feb 11 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.14b-1
- Rebuild with github releases url

* Sun Jul 21 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.14b-0
- Created spec