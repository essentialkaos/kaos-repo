###############################################################################

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

%define shortname         node

###############################################################################

Summary:            Platform for server side programming on JavaScript
Name:               nodejs
Version:            6.10.1
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                http://nodejs.org

Source0:            http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           zlib

BuildRequires:      make gcc clang python >= 2.6 openssl-devel zlib-devel
BuildRequires:      gcc-c++ libstdc++-devel

Provides:           %{name} = %{version}-%{release} 
Provides:           %{shortname} = %{version}-%{release} 
Provides:           npm = %{version}-%{release} 

###############################################################################

%description
Node.js is a platform built on Chromes JavaScript runtime for 
easily building fast, scalable network applications. Node.js 
uses an event-driven, non-blocking I/O model that makes it 
lightweight and efficient, perfect for data-intensive 
real-time applications that run across distributed devices.

###############################################################################

%package devel

Summary:            Header files for nodejs
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

BuildArch:          noarch

%description devel
This package provides the header files for nodejs.

###############################################################################

%prep
%setup -q -n %{shortname}-v%{version}

%build
export CC=clang
export CXX=clang++

%{_configure} --prefix=%{_prefix} \
              --shared-zlib \
              --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%{_bindir}/%{shortname}
%{_bindir}/npm
%{_docdir}/%{shortname}/gdbinit
%{_mandir}/man1/%{shortname}.1.gz
%{_libdir32}/%{shortname}_modules
%{_datadir}/systemtap/tapset/%{shortname}.stp

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*

###############################################################################

%changelog
* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 6.10.1-0
- performance: The performance of several APIs has been improved
- IPC: Batched writes have been enabled for process IPC on platforms that
  support Unix Domain Sockets
- http: Control characters are now always rejected when using http.request()
- http: Debug messages have been added for cases when headers contain
  invalid values
- node: Heap statistics now support values larger than 4GB
- timers: Timer callbacks now always maintain order when interacting with
  domain error handling

* Sat Mar 11 2017 Anton Novojilov <andy@essentialkaos.com> - 6.10.0-0
- crypto: allow adding extra certs to well-known CA's
- deps: Upgrade INTL ICU to version 58
- process: add process.memoryUsage.external
- src: add wrapper for process.emitWarning()
- fs: cache non-symlinks in realpathSync
- repl: allow autocompletion for scoped packages

* Mon Feb 20 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.9.5-0
- deps: upgrade openssl sources to 1.0.2k

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.9.4-0
- N/A

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.9.3-0
- build: shared library support is now working for AIX builds
- npm: upgrade npm to 3.10.10
- V8: Destructuring of arrow function arguments via computed property no longer throws
- inspector: /json/version returns object, not an object wrapped in an array
- module: using --debug-brk and --eval together now works as expected
- process: improve performance of nextTick up to 20%
- repl: the division operator will no longer be accidentally parsed as regex
- repl: improved support for generator functions
- timers: Re canceling a cancelled timers will no longer throw

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 6.9.2-0
- buffer: coerce slice parameters consistently
- npm: upgrade npm to 3.10.9
- V8: Various fixes to destructuring edge cases
- gtest: the test reporter now outputs tap comments as yamlish
- inspector: inspector now prompts user to use 127.0.0.1 rather than localhost
- tls: fix memory leak when writing data to TLSWrap instance during handshake

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 6.9.1-0
- streams: Fix a regression introduced in v6.8.0 in readable stream that
  caused unpipe to remove the wrong stream
