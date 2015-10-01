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
Version:            4.0.0
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                http://nodejs.org
Vendor:             Joyent Inc.

Source0:            %{url}/dist/v%{version}/node-v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ python >= 2.6 openssl-devel zlib-devel libstdc++-devel

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
              --shared-openssl --shared-openssl-includes=%{_includedir} \
              --shared-zlib --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{_bindir}/%{shortname}
%{_bindir}/npm
%{_mandir}/man1/%{shortname}.1.gz
%{_libdir32}/%{shortname}_modules
%{_datadir}/systemtap/tapset/%{shortname}.stp

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*

###############################################################################

%changelog
* Wed Sep  9 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- child_process: ChildProcess.prototype.send() and process.send() operate 
asynchronously across all platforms so an optional callback parameter has 
been introduced that will be invoked once the message has been sent, i.e. 
.send(message[, sendHandle][, callback]).
- node: Rename "io.js" code to "Node.js".
- node-gyp: This release bundles an updated version of node-gyp that works 
with all versions of Node.js and io.js including nightly and release 
candidate builds. From io.js v3 and Node.js v4 onward, it will only 
download a headers tarball when building addons rather than the entire source.
- npm: Upgrade to version 2.14.2 from 2.13.3, includes a security update, 
see https://github.com/npm/npm/releases/tag/v2.14.2 for more details.
- timers: Improved timer performance from porting the 0.12 implementation, 
plus minor fixes.
- util: The util.is*() functions have been deprecated, beginning with 
deprecation warnings in the documentation for this release, users are 
encouraged to seek more robust alternatives in the npm registry.
- v8: Upgrade to version 4.5.103.30 from 4.4.63.30.

* Fri Jul 10 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.7-0
- openssl: upgrade to 1.0.1p
- npm: upgrade to 2.11.3
- V8: cherry-pick JitCodeEvent patch from upstream (Ben Noordhuis)
- win,msi: create npm folder in AppData directory (Steven Rockarts)

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.6-0
- V8: fix out-of-band write in utf8 decoder

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.5-0
- openssl: upgrade to 1.0.1o (Addressing multiple CVEs)
- npm: upgrade to 2.11.2
- uv: upgrade to 1.6.1
- V8: avoid deadlock when profiling is active (Dmitri Melikyan)
- install: fix source path for openssl headers (Oguz Bastemur)
- install: make sure opensslconf.h is overwritten (Oguz Bastemur)
- timers: fix timeout when added in timer's callback (Julien Gilli)
- windows: broadcast WM_SETTINGCHANGE after install (Mathias Küsel)

* Mon May 25 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.4-0
- npm: upgrade to 2.10.1
- V8: revert v8 Array.prototype.values() removal (cjihrig)
- win: bring back xp/2k3 support (Bert Belder)

* Fri May 15 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.3-0
- V8: update to 3.28.71.19
- uv: upgrade to 1.5.0
- npm: upgrade to 2.9.1
- V8: don't busy loop in v8 cpu profiler thread (Mike Tunnicliffe)
- V8: fix issue with let bindings in for loops (adamk)
- debugger: don't spawn child process in remote mode (Jackson Tian)
- net: do not set V4MAPPED on FreeBSD (Julien Gilli)
- repl: make 'Unexpected token' errors recoverable (Julien Gilli)
- src: backport ignore ENOTCONN on shutdown race (Ben Noordhuis)
- src: fix backport of SIGINT crash fix on FreeBSD (Julien Gilli) 

* Wed Apr 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.2-0
- uv: Upgrade to 1.4.2
- npm: Upgrade to 2.7.4
- V8: do not add extra newline in log file (Julien Gilli)
- V8: Fix --max_old_space_size=4096 integer overflow (Andrei Sedoi)
- asyncwrap: fix constructor condition for early ret (Trevor Norris)
- buffer: align chunks on 8-byte boundary (Fedor Indutny)
- buffer: fix pool offset adjustment (Trevor Norris)
- build: fix use of strict aliasing (Trevor Norris)
- console: allow Object.prototype fields as labels (Colin Ihrig)
- fs: make F_OK/R_OK/W_OK/X_OK not writable (Jackson Tian)
- fs: properly handle fd passed to truncate() (Bruno Jouhier)
- http: fix assert on data/end after socket error (Fedor Indutny)
- lib: fix max size check in Buffer constructor (Ben Noordhuis)
- lib: fix stdio/ipc sync i/o regression (Ben Noordhuis)
- module: replace NativeModule.require (Herbert Vojčík)
- net: allow port 0 in connect() (cjihrig)
- net: unref timer in parent sockets (Fedor Indutny)
- path: refactor for performance and consistency (Nathan Woltman)
- smalloc: extend user API (Trevor Norris)
- src: fix for SIGINT crash on FreeBSD (Fedor Indutny)
- src: fix builtin modules failing with --use-strict (Julien Gilli)
- watchdog: fix timeout for early polling return (Saúl Ibarra Corretgé)

* Tue Mar 24 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.1-0
- openssl: upgrade to 1.0.1m (Addressing multiple CVES)

* Sat Feb 07 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-0
- npm: Upgrade to 2.5.1
- mdb_v8: update for v0.12 (Dave Pacheco)
