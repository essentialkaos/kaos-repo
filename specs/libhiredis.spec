################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define realname  hiredis

################################################################################

Summary:        Minimalistic C client for Redis
Name:           lib%{realname}
Version:        1.2.0
Release:        0%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            https://github.com/redis/hiredis

Source0:        https://github.com/redis/%{realname}/archive/refs/tags/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Hiredis is a minimalistic C client library for the Redis database.

################################################################################

%package devel
Summary:  Header files and libraries for hiredis C development
Group:    Development/Libraries

Requires:  %{name} = %{version}

%description devel
The %{name}-devel package contains the header files and
libraries to develop applications using a Redis database.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%build
%{__make} %{?_smp_mflags} OPTIMIZATION="%{optflags}"

%install
rm -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix} INSTALL_LIBRARY_PATH=%{buildroot}%{_libdir} LIBRARY_PATH=%{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{realname}/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/%{realname}.pc

################################################################################

%changelog
* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- https://github.com/redis/hiredis/releases/tag/v1.2.0

* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- https://github.com/redis/hiredis/releases/tag/v1.1.0

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 0.14.0-0
- Make string2ll static to fix conflict with Redis
- Use -dynamiclib instead of -shared for OSX
- Use string2ll from Redis w/added tests
- Makefile - OSX compilation fixes
- Remove redundant NULL checks
- Fix bulk and multi-bulk length truncation
- Fix SIGSEGV in OpenBSD by checking for NULL before calling freeaddrinfo
- Several POSIX compatibility fixes
- Makefile - Compatibility fixes
- Makefile - Fix make install on FreeBSD
- Makefile - don't assume $(INSTALL) is cp
- Separate side-effect causing function from assert and small cleanup
- Don't send negative values to __redisAsyncCommand
- Fix leak if setsockopt fails
- Fix libevent leak
- Clean up GCC warning
- Keep track of errno in __redisSetErrorFromErrno() as snprintf may use it
- Solaris compilation fix
- Reorder linker arguments when building examples
- Keep track of subscriptions in case of rapid subscribe/unsubscribe
- libuv use after free fix
- Properly close socket fd on reconnect attempt
- Skip valgrind in OSX tests
- Various updates for Travis testing OSX
- Update libevent
- Change sds.h for building in C++ projects
- Use proper format specifier in redisFormatSdsCommandArgv
- Better handling of NULL reply in example code
- Prevent overflow when formatting an error
- Compatibility fix for strerror_r
- Properly detect integer parse/overflow errors
- Adds CI for Windows and cygwin fixes
- Catch a buffer overflow when formatting the error message
- Import latest upstream sds. This breaks applications that are linked against
  the old hiredis v0.13
- Fix warnings, when compiled with -Wshadow
- Make hiredis compile in Cygwin on Windows, now CI-tested

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
- Remove possibility of multiple close on same fd
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
