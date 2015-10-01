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

###############################################################################

%define realname       hiredis
%define minor_ver      13
%define rel            3

###############################################################################

Summary:             Minimalistic C client for Redis
Name:                lib%{realname}
Version:             0.%{minor_ver}.%{rel}
Release:             0%{?dist}
License:             BSD
Group:               System Environment/Libraries
URL:                 https://github.com/redis/hiredis

Source0:             https://github.com/redis/%{realname}/archive/v0.%{minor_ver}.%{rel}.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       gcc make

###############################################################################

%description 
Hiredis is a minimalistic C client library for the Redis database.

###############################################################################

%package devel
Summary:             Header files and libraries for hiredis C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel 
The %{name}-devel package contains the header files and 
libraries to develop applications using a Redis database.

###############################################################################

%prep
%setup -qn %{realname}-0.%{minor_ver}.%{rel}

%build
%{__make} %{?_smp_mflags} OPTIMIZATION="%{optflags}" 

%install
%{__rm} -rf %{buildroot}
%{__make} install PREFIX=%{buildroot}%{_prefix} INSTALL_LIBRARY_PATH=%{buildroot}%{_libdir} LIBRARY_PATH=%{buildroot}%{_libdir}

ln -s %{_libdir}/%{name}.so.0.%{minor_ver} %{buildroot}%{_libdir}/%{name}.so.0

%clean 
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.0.%{minor_ver}
%{_libdir}/%{name}.so.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{realname}/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/%{realname}.pc

###############################################################################

%changelog
* Thu Sep 17 2015 Anton Novojilov <andy@essentialkaos.com> - 0.13.3-0
- Revert "Clear REDIS_CONNECTED flag when connection is closed".
- Make tests pass on FreeBSD (Thanks, Giacomo Olgeni)

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.13.2-0
- Prevent crash on pending replies in async code (Thanks, @switch-st)
- Clear REDIS_CONNECTED flag when connection is closed (Thanks, Jerry Jacobs)
- Add MacOS X addapter (Thanks, @dizzus)
- Add Qt adapter (Thanks, Pietro Cerutti)
- Add Ivykis adapter (Thanks, Gergely Nagy)

* Thu Jul 02 2015 Anton Novojilov <andy@essentialkaos.com> - 0.13.1-0
- Windows compatibility layer for parser code (tzickel)
- Properly escape data printed to PKGCONF file (Dan Skorupski)
- Fix tests when assert() undefined (Keith Bennett, Matt Stancliff)
- Implement a reconnect method for the client context, this changes 
  the structure of redisContext (Aaron Bedra)
- Fix memory leak in async reply handling (Salvatore Sanfilippo)
- Rename struct member to avoid name clash with pre-c99 
  code (Alex Balashov, ncopa)

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.1-0
- Fix `make install`: DESTDIR support, install all required files, install 
  PKGCONF in proper location
- Fix `make test` as 32 bit build on 64 bit platform

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-0
- Add optional KeepAlive support
- Try again on EINTR errors
- Add libuv adapter
- Add IPv6 support
- Remove possiblity of multiple close on same fd
- Add ability to bind source address on connect
- Add redisConnectFd() and redisFreeKeepFd()
- Fix getaddrinfo() memory leak
- Free string if it is unused (fixes memory leak)
- Improve redisAppendCommandArgv performance 2.5x
- Add support for SO_REUSEADDR
- Fix redisvFormatCommand format parsing
- Add GLib 2.0 adapter
- Refactor reading code into read.c
- Fix errno error buffers to not clobber errors
- Generate pkgconf during build
- Silence _BSD_SOURCE warnings
- Improve digit counting for multibulk creation

* Mon Nov 24 2014 Anton Novojilov <andy@essentialkaos.com> - 0.11.0-1
- Initial rebuild