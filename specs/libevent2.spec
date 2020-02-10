################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define realname      libevent

%if 0%{?rhel} >= 7
%define pkgname       libevent
%else
%define pkgname       libevent2
%endif

################################################################################

Summary:              Abstract asynchronous event notification library
Name:                 %{pkgname}
Version:              2.1.11
Release:              0%{?dist}
License:              BSD
Group:                System Environment/Libraries
URL:                  https://libevent.org

Source0:              https://github.com/%{realname}/%{realname}/archive/release-%{version}-stable.tar.gz

Source100:            checksum.sha512

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc make automake libtool openssl-devel zlib-devel

# For CentOS7/RHEL7 libevent2 = libevent
%if 0%{?rhel} >= 7
Provides:             %{realname}2 = %{version}-%{release}
%endif

################################################################################

%description
The libevent API provides a mechanism to execute a callback function when
a specific event occurs on a file descriptor or after a timeout has been
reached. Furthermore, libevent also support callbacks due to signals or regular
timeouts.

################################################################################

%package devel
Group:                System Environment/Libraries
Summary:              Development files for %{name}
Requires:             %{name} = %{version}

# For CentOS7/RHEL7 libevent2 = libevent
%if 0%{?rhel} >= 7
Provides:             %{realname}2-devel = %{version}-%{release}
%endif

%description devel
Development files for %{name}

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-release-%{version}-stable

%build
./autogen.sh

%configure \
 --disable-static \
 LDFLAGS="-Wl,--as-needed -Wl,--strip-all"

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc LICENSE README.md ChangeLog-2.0
%{_libdir}/%{realname}*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/event_rpcgen.py
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_includedir}/event2/
%{_libdir}/%{realname}*.so

################################################################################

%changelog
* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 2.1.11-0
- Protect min_heap_push_ against integer overflow
- Revert "Protect min_heap_push_ against integer overflow."
- evdns: add new options -- so-rcvbuf/so-sndbuf
- Change autoconf version to 2.62 and automake version to 1.11.2
- cmake: install shared library only if it was requested
- Missing <winerror.h> on win7/MinGW(MINGW32_NT-6.1)/MSYS
- cmake: set library names to be the same as with autotools
- Enable _GNU_SOURCE for Android
- Enable kqueue for APPLE targets
- autotools: do not install bufferevent_ssl.h under --disable-openssl
- cmake: link against shell32.lib/advapi32.lib
- Add README.md into dist archive
- cmake: add missing autotools targets (doxygen, uninstall, event_rpcgen.py)
- m4/libevent_openssl.m4: fix detection of openssl
- Fix detection of the __has_attribute() for apple clang [ci skip]
- buffer: fix possible NULL dereference in evbuffer_setcb() on ENOMEM
- Warn if forked from the event loop during event_reinit()
- evutil: set the have_checked_interfaces in evutil_check_interfaces()
- https-client: correction error checking

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.1.10-0
- This release contains mostly fixes (some evbuffer oddity, AF_UNIX handling in
  http server, some UB fixes and others) but also some new functionality
  (without ABI breakage as usual) and now dist archive can be used for building
  on windows (getopt had been added into it)

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.1.8-0
- Libevent 2.1.8-stable, it contains openssl fixes for resetting fd and using
  bufferevent_openssl_filter_new(). vagrant fixes, some build fixes, increased
  timeout for some tests (to reduce number of failures due to timing issues),
  date in RFC1123 format and running tests in parallel

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0.22-2
- Avoid integer overflow bugs in evbuffer_add() and related functions.
  See CVE-2014-6272 advisory for more information.
- fix 73 and fix http_connection_fail_test to catch it (crash fix)
- Avoid racy bufferevent activation
- Fix compilation with WIN32_HAVE_CONDITION_VARIABLES enabled
- Fix missing AC_PROG_SED on older Autoconfs
- Backport libevent to vanilla Autoconf 2.59 (as used in RHEL5)
- Use AC_CONFIG_HEADERS in place of AM_CONFIG_HEADERS for autmake 1.13 compat
- Rename configure.in to configure.ac to appease newer autoconfs
- Avoid using top_srcdir in TESTS: new automakes do not like this
- Use windows vsnprintf fixup logic on all windows environments
- Fix a compiler warning when checking for arc4random_buf linker breakage.
- Fix another arc4random_buf-related warning
- Add -Qunused-arguments for clang on macos
- Avoid leaking fds on evconnlistener with no callback set
- Avoid double-close on getsockname error in evutil_ersatz_socketpair
- Fix a locking error in bufferevent_socket_get_dns_error.
- libevent/win32_dealloc() : fix sizeof(pointer) vs sizeof(*pointer)
- bufferevent_pair: don't call downcast(NULL)
- Consistently check for failure from evbuffer_pullup()
- Fix race caused by event_active
- Avoid redundant invocations of init_extension_functions for IOCP
- Typo fixes from Linus Nordberg
- Add a few files created by "make verify" to .gitignore.
- regress_buffer: fix 'memcmp' compare size
- Fix bufferevent setwatermark suspend_read
- Fix evbuffer_peek() with len==-1 and start_at non-NULL.
- Checking request nameserver for NULL, before using it.
- Fix SEGFAULT after evdns_base_resume if no nameservers installed.
- Fix a crash in evdns related to shutting down evdns
- Check does arch have the epoll_create and __NR_epoll_wait syscalls.
- Avoid other RNG initialization FS reads when urandom file is specified
- When we seed from /proc/sys/kernel/random/uuid, count it as success
- Document that arc4random is not a great cryptographic PRNG.
- Add evutil_secure_rng_set_urandom_device_file
- Really remove RNG seeds from the stack
- Fix a mistake in evbuffer_remove() arguments in example http server code
- Fix a typo in a comment in buffer.h. Spotted by Alt_F4
- Clarify event_base_loop exit conditions
- Use FindClose for handle from FindFirstFile in http-server.c
- Fix a typo in a doxygen comment.

* Tue Feb 11 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.21-1
- Rebuild with github releases url
- Fixed build process

* Sun Jul 21 2013 Anton Novojilov <andy@essentialkaos.com> - 2.0.21-0
- Created spec
