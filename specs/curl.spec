################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

%{!?_without_nss: %{!?_with_nss: %define _with_nss --with-nss}}
%{?_with_nss:     %define is_nss_enabled 1}
%{?_without_nss:  %define is_nss_enabled 0}

%if 0%{?fedora} > 15 || 0%{?rhel} > 5
%define is_nss_supported 1
%else
%define is_nss_supported 0
%endif

%if 0%{?is_nss_supported} && 0%{?is_nss_enabled}
%define use_nss 1
%define ssl_provider nss
%define ssl_version_req >= 3.14.0
%else
%define use_nss 0
%define ssl_provider openssl
%define ssl_version_req    %{nil}
%endif

%if 0%{?fedora} > 11 || 0%{?rhel} > 6
%define use_threads_posix  1
%else
%define use_threads_posix  0
%endif

# Require at least the version of libssh2/c-ares that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%define libssh2_version   %(pkg-config --modversion libssh2 2>/dev/null || echo 0)
%define cares_version     %(pkg-config --modversion libcares 2>/dev/null || echo 0)

################################################################################

Summary:              Utility for getting files from remote servers
Name:                 curl
Version:              7.68.0
Release:              0%{?dist}
License:              MIT
Group:                Applications/Internet
URL:                  https://curl.haxx.se

Source0:              https://curl.haxx.se/download/%{name}-%{version}.tar.bz2

Source100:            checksum.sha512

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:             webclient = %{version}-%{release}

Requires:             c-ares libmetalink >= 0.1.3 libnghttp2 >= 1.16.0

BuildRequires:        make gcc libidn-devel krb5-devel
BuildRequires:        pkgconfig zlib-devel openldap-devel
BuildRequires:        libmetalink-devel libssh2-devel >= 1.2 groff
BuildRequires:        %{ssl_provider}-devel %{ssl_version_req}
BuildRequires:        openssh-clients openssh-server stunnel perl python
BuildRequires:        perl(Cwd) perl(Digest::MD5) perl(Exporter) perl(vars)
BuildRequires:        perl(File::Basename) perl(File::Copy) perl(File::Spec)
BuildRequires:        perl(IPC::Open2) perl(MIME::Base64) perl(warnings)
BuildRequires:        perl(strict) perl(Time::Local) perl(Time::HiRes)

%if ! %{use_threads_posix}
BuildRequires:        c-ares-devel >= 1.6.0
%endif

%if 0%{?fedora} > 22 || 0%{?rhel} > 5
BuildRequires:        libnghttp2-devel nghttp2
%endif

%if 0%{?fedora} > 18 || 0%{?rhel} > 6
BuildRequires:        libpsl-devel
%endif

Requires:             libcurl%{?_isa} = %{version}-%{release}
%if ! %{use_nss}
Requires:             %{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%endif

################################################################################

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks.

################################################################################

%package -n libcurl
Summary:              A library for getting files from web servers
Group:                System Environment/Libraries

%if 0%{?fedora} > 24 || 0%{?rhel} > 7
BuildRequires:        nss-pem
%endif

Requires:             libssh2%{?_isa} >= %{libssh2_version}
Requires:             libmetalink >= 0.1.3 libnghttp2 >= 1.16.0

%if 0%{?fedora} > 24 || 0%{?rhel} > 7
Requires:             nss-pem
%endif

%if ! %{use_threads_posix}
Requires:             c-ares%{?_isa} >= %{cares_version}
%endif

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, HTTP proxy tunneling and more.

################################################################################

%package -n libcurl-devel
Summary:              Files needed for building applications with libcurl
Group:                Development/Libraries

Requires:             libcurl%{?_isa} = %{version}-%{release}
Requires:             %{ssl_provider}-devel %{ssl_version_req}
Requires:             libssh2-devel

Provides:             curl-devel = %{version}-%{release}
Provides:             curl-devel%{?_isa} = %{version}-%{release}

Obsoletes:            curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs that use the libcurl library. It contains the API
documentation of the library, too.

################################################################################

%prep
%{crc_check}

%setup -qn curl-%{version}

%build
%if ! 0%{?use_nss}
export CPPFLAGS="$(pkg-config --cflags openssl)"
%endif

[ -x %{_usr}/kerberos/bin/krb5-config ] && KRB5_PREFIX="=%{_usr}/kerberos"

%configure \
%if 0%{?use_nss}
        --without-ssl \
        --with-nss \
%else
        --with-ssl \
%endif
        --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
%if 0%{?use_threads_posix}
        --enable-threaded-resolver \
%else
        --enable-ares \
%endif
        --enable-symbol-hiding \
        --enable-ipv6 \
        --enable-ldaps \
        --with-gssapi${KRB5_PREFIX} \
        --with-libidn \
        --with-libmetalink \
%if 0%{?fedora} > 22 || 0%{?rhel} > 5
        --with-nghttp2 \
%endif
%if 0%{?fedora} > 18 || 0%{?rhel} > 6
        --with-libpsl \
%endif
        --with-libssh2 \
        --enable-manual \
        --disable-static

sed -i \
        -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
        -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

install -dm 0755 %{buildroot}%{_datadir}/aclocal

install -pm 0644 docs/libcurl/libcurl.m4 %{buildroot}%{_datadir}/aclocal

%clean
rm -rf %{buildroot}

%post -n libcurl
/sbin/ldconfig

%postun -n libcurl
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES README*
%doc docs/BUGS docs/FAQ docs/FEATURES docs/TODO docs/HTTP2.md
%doc docs/SSL-PROBLEMS.md docs/THANKS docs/KNOWN_BUGS docs/FEATURES
%doc docs/RESOURCES docs/TheArtOfHttpScripting
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n libcurl
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CHECKSRC.md docs/CONTRIBUTE.md docs/libcurl/ABI docs/CODE_STYLE.md
%{_bindir}/curl-config
%{_includedir}/curl/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcurl.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4
%exclude %{_libdir}/libcurl.la

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.68.0-0
- TLS: add BearSSL vtls implementation
- XFERINFOFUNCTION: support CURL_PROGRESSFUNC_CONTINUE
- curl: add --etag-compare and --etag-save
- curl: add --parallel-immediate
- multi: add curl_multi_wakeup()
- openssl: CURLSSLOPT_NO_PARTIALCHAIN can disable partial cert chains
- CVE-2019-15601: file: on Windows, refuse paths that start with \\
- Azure Pipelines: add several builds
- CMake: add support for building with the NSS vtls backend
- CURL-DISABLE: initial docs for the CURL_DISABLE_* defines
- CURLOPT_HEADERFUNCTION.3: Document that size is always 1
- CURLOPT_QUOTE.3: fix typos
- CURLOPT_READFUNCTION.3: fix the example
- CURLOPT_URL.3: "curl supports SMB version 1 (only)"
- CURLOPT_VERBOSE.3: see also ERRORBUFFER
- HISTORY: added cmake, HTTP/3 and parallel downloads with curl
- HISTORY: the SMB(S) support landed in 2014
- INSTALL.md: provide Android build instructions
- KNOWN_BUGS: Connection information when using TCP Fast Open
- KNOWN_BUGS: LDAP on Windows doesn't work correctly
- KNOWN_BUGS: TLS session cache doesn't work with TFO
- OPENSOCKETFUNCTION.3: correct the purpose description
- TrackMemory tests: always remove CR before LF
- altsvc: bump to h3-24
- altsvc: make the save function ignore NULL filenames
- build: Disable Visual Studio warning "conditional expression is constant"
- build: fix for CURL_DISABLE_DOH
- checksrc.bat: Add a check for vquic and vssh directories
- checksrc: repair the copyrightyear check
- cirrus-ci: enable clang sanitizers on freebsd 13
- cirrus: Drop the FreeBSD 10.4 build
- config-win32: cpu-machine-OS for Windows on ARM
- configure: avoid unportable `==' test(1) operator
- configure: enable IPv6 support without `getaddrinfo`
- configure: fix typo in help text
- conncache: CONNECT_ONLY connections assumed always in-use
- conncache: fix multi-thread use of shared connection cache
- copyrights: fix copyright year range
- create_conn: prefer multiplexing to using new connections
- curl -w: handle a blank input file correctly
- curl.h: add two missing defines for "pre ISO C" compilers
- curl/parseconfig: fix mem-leak
- curl/parseconfig: use curl_free() to free memory allocated by libcurl
- curl: cleanup multi handle on failure
- curl: fix --upload-file . hangs if delay in STDIN
- curl: fix -T globbing
- curl: improved cleanup in upload error path
- curl: make a few char pointers point to const char instead
- curl: properly free mimepost data
- curl: show better error message when no homedir is found
- curl: show error for --http3 if libcurl lacks support
- curl_setup_once: consistently use WHILE_FALSE in macros
- define: remove HAVE_ENGINE_LOAD_BUILTIN_ENGINES, not used anymore
- docs: Change 'experiemental' to 'experimental'
- docs: TLS SRP doesn't work with TLS 1.3
- docs: fix several typos
- docs: mention CURL_MAX_INPUT_LENGTH restrictions
- doh: improved both encoding and decoding
- doh: make it behave when built without proxy support
- examples/postinmemory.c: Call curl_global_cleanup always
- examples/url2file.c: corrected erroneous comment
- examples: add multi-poll.c
- global_init: undo the "intialized" bump in case of failure
- hostip: suppress compiler warning
- http_ntlm: Remove duplicate NSS initialisation
- lib: Move lib/ssh.h -> lib/vssh/ssh.h
- lib: fix compiler warnings with `CURL_DISABLE_VERBOSE_STRINGS`
- lib: fix warnings found when porting to NuttX
- lib: remove ASSIGNWITHINCONDITION exceptions, use our code style
- lib: remove erroneous +x file permission on some c files
- libssh2: add support for ECDSA and ed25519 knownhost keys
- multi.h: remove INITIAL_MAX_CONCURRENT_STREAMS from public header
- multi: free sockhash on OOM
- multi_poll: avoid busy-loop when called without easy handles attached
- ngtcp2: Support the latest update key callback type
- ngtcp2: fix thread-safety bug in error-handling
- ngtcp2: free used resources on disconnect
- ngtcp2: handle key updates as ngtcp2 master branch tells us
- ngtcp2: increase QUIC window size when data is consumed
- ngtcp2: use overflow buffer for extra HTTP/3 data
- ntlm: USE_WIN32_CRYPTO check removed to get USE_NTLM2SESSION set
- ntlm_wb: fix double-free in OOM
- openssl: Revert to less sensitivity for SYSCALL errors
- openssl: improve error message for SYSCALL during connect
- openssl: prevent recursive function calls from ctx callbacks
- openssl: retrieve reported LibreSSL version at runtime
- openssl: set X509_V_FLAG_PARTIAL_CHAIN by default
- parsedate: offer a getdate_capped() alternative
- pause: avoid updating socket if done was already called
- projects: Fix Visual Studio projects SSH builds
- projects: Fix Visual Studio wolfSSL configurations
- quiche: reject HTTP/3 headers in the wrong order
- remove_handle: clear expire timers after multi_done()
- runtests: --repeat=[num] to repeat tests
- runtests: introduce --shallow to reduce huge torture tests
- schannel: fix --tls-max for when min is --tlsv1 or default
- setopt: Fix ALPN / NPN user option when built without HTTP2
- strerror: Add Curl_winapi_strerror for Win API specific errors
- strerror: Fix an error looking up some Windows error strings
- strerror: Fix compiler warning "empty expression"
- system.h: fix for MCST lcc compiler
- test/sws: search for "Testno:" header unconditionally if no testno
- test1175: verify symbols-in-versions and libcurl-errors.3 in sync
- test1270: a basic -w redirect_url test
- test1456: remove the use of a fixed local port number
- test1558: use double slash after file:
- test1560: require IPv6 for IPv6 aware URL parsing
- tests/lib1557: fix mem-leak in OOM
- tests/lib1559: fix mem-leak in OOM
- tests/lib1591: free memory properly on OOM, in the trailers callback
- tests/unit1607: fix mem-leak in OOM
- tests/unit1609: fix mem-leak in OOM
- tests/unit1620: fix bad free in OOM
- tests: Change NTLM tests to require SSL
- tests: Fix bounce requests with truncated writes
- tests: fix build with `CURL_DISABLE_DOH`
- tests: fix permissions of ssh keys in WSL
- tests: make it possible to set executable extensions
- tests: make sure checksrc runs on header files too
- tests: set LC_ALL=en_US.UTF-8 instead of blank in several tests
- tests: use DoH feature for DoH tests
- tests: use \r\n for log messages in WSL
- tool_operate: fix mem leak when failed config parse
- travis: Fix error detection
- travis: abandon coveralls, it is not reliable
- travis: build ngtcp2 with --enable-lib-only
- travis: export the CC/CXX variables when set
- vtls: make BearSSL possible to set with CURL_SSL_BACKEND
- winbuild: Define CARES_STATICLIB when WITH_CARES=static
- winbuild: Document CURL_STATICLIB requirement for static libcurl

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.67.0-0
- curl: added --no-progress-meter
- setopt: CURLMOPT_MAX_CONCURRENT_STREAMS is new
- urlapi: CURLU_NO_AUTHORITY allows empty authority/host part
- BINDINGS: five new bindings addded
- CURLOPT_TIMEOUT.3: Clarify transfer timeout time includes queue time
- CURLOPT_TIMEOUT.3: remove the mention of "minutes"
- ESNI: initial build/setup support
- FTP: FTPFILE_NOCWD: avoid redundant CWDs
- FTP: allow "rubbish" prepended to the SIZE response
- FTP: remove trailing slash from path for LIST/MLSD
- FTP: skip CWD to entry dir when target is absolute
- FTP: url-decode path before evaluation
- HTTP3.md: move -p for mkdir, remove -j for make
- HTTP3: fix invalid use of sendto for connected UDP socket
- HTTP3: fix ngtcp2 Windows build
- HTTP3: fix prefix parameter for ngtcp2 build
- HTTP3: fix typo somehere1 > somewhere1
- HTTP3: show an --alt-svc using example too
- INSTALL: add missing space for configure commands
- INSTALL: add vcpkg installation instructions
- README: minor grammar fix
- altsvc: accept quoted ma and persist values
- altsvc: both backends run h3-23 now
- appveyor: Add MSVC ARM64 build
- appveyor: Use two parallel compilation on appveyor with CMake
- appveyor: add --disable-proxy autotools build
- appveyor: add 32-bit MinGW-w64 build
- appveyor: add a winbuild
- appveyor: add a winbuild that uses VS2017
- appveyor: make winbuilds with DEBUG=no/yes and VS 2015/2017
- appveyor: publish artifacts on appveyor
- appveyor: upgrade VS2017 to VS2019
- asyn-thread: make use of Curl_socketpair() where available
- asyn-thread: s/AF_LOCAL/AF_UNIX for Solaris
- build: Remove unused HAVE_LIBSSL and HAVE_LIBCRYPTO defines
- checksrc: fix uninitialized variable warning
- chunked-encoding: stop hiding the CURLE_BAD_CONTENT_ENCODING error
- cirrus: Increase the git clone depth
- cirrus: Switch the FreeBSD 11.x build to 11.3 and add a 13.0 build
- cirrus: switch off blackhole status on the freebsd CI machines
- cleanups: 21 various PVS-Studio warnings
- configure: only say ipv6 enabled when the variable is set
- configure: remove all cyassl references
- conn-reuse: requests wanting NTLM can reuse non-NTLM connections
- connect: return CURLE_OPERATION_TIMEDOUT for errno == ETIMEDOUT
- connect: silence sign-compare warning
- cookie: avoid harmless use after free
- cookie: pass in the correct cookie amount to qsort()
- cookies: change argument type for Curl_flush_cookies
- cookies: using a share with cookies shouldn't enable the cookie engine
- copyrights: update copyright notices to 2019
- curl: create easy handles on-demand and not ahead of time
- curl: ensure HTTP 429 triggers --retry
- curl: exit the create_transfers loop on errors
- curl: fix memory leaked by parse_metalink()
- curl: load large files with -d @ much faster
- docs/HTTP3: fix `--with-ssl` ngtcp2 configure flag
- docs: added multi-event.c example
- docs: disambiguate CURLUPART_HOST is for host name (ie no port)
- docs: note on failed handles not being counted by curl_multi_perform
- doh: allow only http and https in debug mode
- doh: avoid truncating DNS QTYPE to lower octet
- doh: clean up dangling DOH memory on easy close
- doh: fix (harmless) buffer overrun
- doh: fix undefined behaviour and open up for gcc and clang optimization
- doh: return early if there is no time left
- examples/sslbackend: fix -Wchar-subscripts warning
- examples: remove the "this exact code has not been verified"
- git: add tests/server/disabled to .gitignore
- gnutls: make gnutls_bye() not wait for response on shutdown
- http2: expire a timeout at end of stream
- http2: prevent dup'ed handles to send dummy PRIORITY frames
- http2: relax verification of :authority in push promise requests
- http2_recv: a closed stream trumps pause state
- http: lowercase headernames for HTTP/2 and HTTP/3
- ldap: Stop using wide char version of ldapp_err2string
- ldap: fix OOM error on missing query string
- mbedtls: add error message for cert validity starting in the future
- mime: when disabled, avoid C99 macro
- ngtcp2: adapt to API change
- ngtcp2: compile with latest ngtcp2 + nghttp3 draft-23
- ngtcp2: remove fprintf() calls
- openssl: close_notify on the FTP data connection doesn't mean closure
- openssl: fix compiler warning with LibreSSL
- openssl: use strerror on SSL_ERROR_SYSCALL
- os400: getpeername() and getsockname() return ebcdic AF_UNIX sockaddr
- parsedate: fix date parsing disabled builds
- quiche: don't close connection at end of stream
- quiche: persist connection details (fixes -I with --http3)
- quiche: set 'drain' when returning without having drained the queues
- quiche: update HTTP/3 config creation to new API
- redirect: handle redirects to absolute URLs containing spaces
- runtests: get textaware info from curl instead of perl
- schannel: reverse the order of certinfo insertions
- schannel_verify: Fix concurrent openings of CA file
- security: silence conversion warning
- setopt: handle ALTSVC set to NULL
- setopt: make it easier to add new enum values
- setopt: store CURLOPT_RTSP_SERVER_CSEQ correctly
- smb: check for full size message before reading message details
- smbserver: fix Python 3 compatibility
- socks: Fix destination host shown on SOCKS5 error
- test1162: disable MSYS2's POSIX path conversion
- test1591: fix spelling of http feature
- tests: add `connect to non-listen` keywords
- tests: fix narrowing conversion warnings
- tests: fix the test 3001 cert failures
- tests: makes tests succeed when using --disable-proxy
- tests: use %%FILE_PWD for file:// URLs
- tests: use port 2 instead of 60000 for a safer non-listening port
- tool_operate: Fix retry sleep time shown to user when Retry-After
- travis: Add an ARM64 build
- url: Curl_free_request_state() should also free doh handles
- url: don't set appconnect time for non-ssl/non-ssh connections
- url: fix the NULL hostname compiler warning
- url: normalize CURLINFO_EFFECTIVE_URL
- url: only reuse TLS connections with matching pinning
- urlapi: avoid index underflow for short ipv6 hostnames
- urlapi: fix URL encoding when setting a full URL
- urlapi: fix unused variable warning
- urlapi: question mark within fragment is still fragment
- urldata: use 'bool' for the bit type on MSVC compilers
- vtls: Fix comment typo about macosx-version-min compiler flag
- vtls: fix narrowing conversion warnings
- winbuild/MakefileBuild.vc: Add vssh
- winbuild/MakefileBuild.vc: Fix line endings
- winbuild: Add manifest to curl.exe for proper OS version detection
- winbuild: add ENABLE_UNICODE option

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.66.0-0
- CURLINFO_RETRY_AFTER: parse the Retry-After header value
- HTTP3: initial (experimental still not working) support
- curl: --sasl-authzid added to support CURLOPT_SASL_AUTHZID from the tool
- curl: support parallel transfers with -Z
- curl_multi_poll: a sister to curl_multi_wait() that waits more
- sasl: Implement SASL authorisation identity via CURLOPT_SASL_AUTHZID
- CVE-2019-5481: FTP-KRB double-free
- CVE-2019-5482: TFTP small blocksize heap buffer overflow
- CI: remove duplicate configure flag for LGTM.com
- CMake: remove needless newlines at end of gss variables
- CMake: use platform dependent name for dlopen() library
- CURLINFO docs: mention that in redirects times are added
- CURLOPT_ALTSVC.3: use a "" file name to not load from a file
- CURLOPT_ALTSVC_CTRL.3: remove CURLALTSVC_ALTUSED
- CURLOPT_HEADERFUNCTION.3: clarify
- CURLOPT_HTTP_VERSION: seting this to 3 forces HTTP/3 use directly
- CURLOPT_READFUNCTION.3: provide inline example
- CURLOPT_SSL_VERIFYHOST: treat the value 1 as 2
- Curl_addr2string: take an addrlen argument too
- Curl_fillreadbuffer: avoid double-free trailer buf on error
- HTTP: use chunked Transfer-Encoding for HTTP_POST if size unknown
- alt-svc: add protocol version selection masking
- alt-svc: fix removal of expired cache entry
- alt-svc: make it use h3-22 with ngtcp2 as well
- alt-svc: more liberal ALPN name parsing
- alt-svc: send Alt-Used: in redirected requests
- alt-svc: with quiche, use the quiche h3 alpn string
- appveyor: pass on -k to make
- asyn-thread: create a socketpair to wait on
- build-openssl: fix build with Visual Studio 2019
- cleanup: move functions out of url.c and make them static
- cleanup: remove the 'numsocks' argument used in many places
- configure: avoid undefined check_for_ca_bundle
- curl.h: add CURL_HTTP_VERSION_3 to the version enum
- curl.h: fix outdated comment
- curl: cap the maximum allowed values for retry time arguments
- curl: handle a libcurl build without netrc support
- curl: make use of CURLINFO_RETRY_AFTER when retrying
- curl: remove outdated comment
- curl: use .curlrc (with a dot) on Windows
- curl: use CURLINFO_PROTOCOL to check for HTTP(s)
- curl_global_init_mem.3: mention it was added in 7.12.0
- curl_version: bump string buffer size to 250
- curl_version_info.3: mentioned ALTSVC and HTTP3
- curl_version_info: offer quic (and h3) library info
- curl_version_info: provide nghttp2 details
- defines: avoid underscore-prefixed defines
- docs/ALTSVC: remove what works and the experimental explanation
- docs/EXPERIMENTAL: explain what it means and what is experimental now
- docs/MANUAL.md: converted to markdown from plain text
- docs/examples/curlx: fix errors
- docs: s/curl_debug/curl_dbg_debug in comments and docs
- easy: resize receive buffer on easy handle reset
- examples: Avoid reserved names in hiperfifo examples
- examples: add http3.c, altsvc.c and http3-present.c
- getenv: support up to 4K environment variable contents on windows
- http09: disable HTTP/0.9 by default in both tool and library
- http2: when marked for closure and wanted to close == OK
- http2_recv: trigger another read when the last data is returned
- http: fix use of credentials from URL when using HTTP proxy
- http_negotiate: improve handling of gss_init_sec_context() failures
- md4: Use our own MD4 when no crypto libraries are available
- multi: call detach_connection before Curl_disconnect
- netrc: make the code try ".netrc" on Windows
- nss: use TLSv1.3 as default if supported
- openssl: build warning free with boringssl
- openssl: use SSL_CTX_set__proto_version() when available
- plan9: add support for running on Plan 9
- progress: reset download/uploaded counter between transfers
- readwrite_data: repair setting the TIMER_STARTTRANSFER stamp
- scp: fix directory name length used in memcpy
- smb: init *msg to NULL in smb_send_and_recv()
- smtp: check for and bail out on too short EHLO response
- source: remove names from source comments
- spnego_sspi: add typecast to fix build warning
- src/makefile: fix uncompressed hugehelp.c generation
- ssh-libssh: do not specify O_APPEND when not in append mode
- ssh: move code into vssh for SSH backends
- sspi: fix memory leaks
- tests: Replace outdated test case numbering documentation
- tftp: return error when packet is too small for options
- timediff: make it 64 bit (if possible) even with 32 bit time_t
- travis: reduce number of torture tests in 'coverage'
- url: make use of new HTTP version if alt-svc has one
- urlapi: verify the IPv6 numerical address
- urldata: avoid 'generic', use dedicated pointers
- vauth: Use CURLE_AUTH_ERROR for auth function errors

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.3-0
- progress: make the progress meter appear again

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.2-0
- CIPHERS.md: Explain Schannel error SEC_E_ALGORITHM_MISMATCH
- CMake: Convert errant elseif() to else()
- CMake: Fix finding Brotli on case-sensitive file systems
- CURLMOPT_SOCKETFUNCTION.3: clarified
- CURLMOPT_SOCKETFUNCTION.3: fix typo
- CURLOPT_CAINFO.3: polished wording
- CURLOPT_HEADEROPT.3: Fix example
- CURLOPT_RANGE.3: Caution against using it for HTTP PUT
- CURLOPT_SEEKDATA.3: fix variable name
- DEPRECATE: fixup versions and spelling
- bindlocal: detect and avoid IP version mismatches in bind()
- build: fix Codacy warnings
- buildconf.bat: fix header filename
- c-ares: honor port numbers in CURLOPT_DNS_SERVERS
- config-os400: add getpeername and getsockname defines
- configure: --disable-progress-meter
- configure: fix --disable-code-coverage
- configure: fix typo '--disable-http-uath'
- configure: more --disable switches to toggle off individual features
- configure: remove CURL_DISABLE_TLS_SRP
- conn_maxage: move the check to prune_dead_connections()
- curl: skip CURLOPT_PROXY_CAPATH for disabled-proxy builds
- curl_multi_wait.3: escape backslash in example
- docs: Explain behavior change in --tlsv1. options since 7.54
- docs: Fix links to OpenSSL docs
- docs: fix string suggesting HTTP/2 is not the default
- examples/fopen: fix comparison
- examples/htmltitle: use C++ casts between pointer types
- headers: Remove no longer exported functions
- http2: call done_sending on end of upload
- http2: don't call stream-close on already closed streams
- http2: remove CURL_DISABLE_TYPECHECK define
- http: allow overriding timecond with custom header
- http: clarify header buffer size calculation
- krb5: fix compiler warning
- lib: Use UTF-8 encoding in comments
- libcurl-tutorial.3: Fix small typo (mutipart -> multipart)
- libcurl: Restrict redirect schemes to HTTP, HTTPS, FTP and FTPS
- multi: enable multiplexing by default (again)
- multi: fix the transfer hashes in the socket hash entries
- multi: make sure 'data' can present in several sockhash entries
- netrc: Return the correct error code when out of memory
- nss: don't set unused parameter
- nss: inspect returnvalue of token check
- nss: only cache valid CRL entries
- nss: support using libnss on macOS
- openssl: define HAVE_SSL_GET_SHUTDOWN based on version number
- openssl: disable engine if OPENSSL_NO_UI_CONSOLE is defined
- openssl: fix pubkey/signature algorithm detection in certinfo
- openssl: remove outdated comment
- os400: make vsetopt() non-static as Curl_vsetopt() for os400 support
- quote.d: asterisk prefix works for SFTP as well
- runtests: keep logfiles around by default
- runtests: report single test time + total duration
- smb: Use the correct error code for access denied on file open
- sws: remove unused variables
- system_win32: fix clang warning
- system_win32: fix typo
- test1165: verify that CURL_DISABLE_ symbols are in sync
- test1521: adapt to SLISTPOINT
- test1523: test CURLOPT_LOW_SPEED_LIMIT
- test153: fix content-length to avoid occasional hang
- test188/189: fix Content-Length
- tests: have runtests figure out disabled features
- tests: support non-localhost HOSTIP for dict/smb servers
- tests: update fixed IP for hostip/clientip split
- tool_cb_prg: Fix integer overflow in progress bar
- travis: disable threaded resolver for coverage build
- travis: enable alt-svc for coverage build
- travis: enable brotli for all xenial jobs
- travis: enable libssh2 for coverage build
- travis: enable warnings-as-errors for coverage build
- travis: update scan-build job to xenial
- typecheck: CURLOPT_CONNECT_TO takes an slist too
- typecheck: add 3 missing strings and a callback data pointer
- unit1654: cleanup on memory failure
- unpause: trigger a timeout for event-based transfers
- url: Fix CURLOPT_MAXAGE_CONN time comparison
- win32: make DLL loading a no-op for UWP
- winbuild: Change Makefile to honor ENABLE_OPENSSL_AUTO_LOAD_CONFIG
- winbuild: use WITH_PREFIX if given
- wolfssl: refer to it as wolfSSL only
- Added CRC check for all sources

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.1-0
- CURLOPT_LOW_SPEED_* repaired
- NTLM: reset proxy "multipass" state when CONNECT request is done
- PolarSSL: deprecate support step 1. Removed from configure
- appveyor: add Visual Studio solution build
- cmake: check for if_nametoindex()
- cmake: support CMAKE_OSX_ARCHITECTURES when detecting SIZEOF variables
- config-win32: add support for if_nametoindex and getsockname
- conncache: Remove the DEBUGASSERT on length check
- conncache: make "bundles" per host name when doing proxy tunnels
- curl-win32.h: Enable Unix Domain Sockets based on the Windows SDK version
- curl_share_setopt.3: improve wording
- dump-header.d: spell out that no headers == empty file
- example/http2-download: fix format specifier
- examples: cleanups and compiler warning fixes
- http2: Stop drain from being permanently set
- http: don't parse body-related headers in bodyless responses
- md4: build correctly with openssl without MD4
- md4: include the mbedtls config.h to get the MD4 info
- multi: track users of a socket better
- nss: allow to specify TLS 1.3 ciphers if supported by NSS
- parse_proxy: make sure portptr is initialized
- parse_proxy: use the IPv6 zone id if given
- sectransp: handle errSSLPeerAuthCompleted from SSLRead()
- singlesocket: use separate variable for inner loop
- ssl: Update outdated "openssl-only" comments for supported backends
- tests: add HAProxy keywords
- tests: add support to test against OpenSSH for Windows
- tests: make test 1420 and 1406 work with rtsp-disabled libcurl
- tls13-docs: mention it is only for OpenSSL >= 1.1.1
- tool_parse_cfg: Avoid 2 fopen() for WIN32
- tool_setopt: for builds with disabled-proxy, skip all proxy setopts()
- url: Load if_nametoindex() dynamically from iphlpapi.dll on Windows
- url: fix bad feature-disable #ifdef
- url: use correct port in ConnectionExists()
- winbuild: Use two space indentation

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.0-0
- CURLOPT_DNS_USE_GLOBAL_CACHE: removed
- CURLOPT_MAXAGE_CONN: set the maximum allowed age for conn reuse
- pipelining: removed
- CVE-2019-5435: Integer overflows in curl_url_set
- CVE-2019-5436: tftp: use the current blksize for recvfrom()
- --config: clarify that initial : and = might need quoting
- AppVeyor: enable testing for WinSSL build
- CURLMOPT_TIMERFUNCTION.3: warn about the recursive risk
- CURLOPT_ADDRESS_SCOPE: fix range check and more
- CURLOPT_CAINFO.3: with Schannel, you want Windows 8 or later
- CURLOPT_CHUNK_BGN_FUNCTION.3: document the struct and time value
- CURLOPT_READFUNCTION.3: see also CURLOPT_UPLOAD_BUFFERSIZE
- CURL_MAX_INPUT_LENGTH: largest acceptable string input size
- Curl_disconnect: treat all CONNECT_ONLY connections as "dead"
- INTERNALS: Add code highlighting
- OS400/ccsidcurl: replace use of Curl_vsetopt
- OpenSSL: Report -fips in version if OpenSSL is built with FIPS
- README.md: fix no-consecutive-blank-lines Codacy warning
- VC15 project: remove MinimalRebuild
- VS projects: use Unicode for VC10+
- WRITEFUNCTION: add missing set_in_callback around callback
- altsvc: Fix building with cookies disabled
- auth: Rename the various authentication clean up functions
- base64: build conditionally if there are users
- build-openssl.bat: Fixed support for OpenSSL v1.1.0+
- build: fix "clarify calculation precedence" warnings
- checksrc.bat: ignore snprintf warnings in docs/examples
- cirrus: Customize the disabled tests per FreeBSD version
- cleanup: remove FIXME and TODO comments
- cmake: avoid linking executable for some tests with cmake 3.6+
- cmake: clear CMAKE_REQUIRED_LIBRARIES after each use
- cmake: rename CMAKE_USE_DARWINSSL to CMAKE_USE_SECTRANSP
- cmake: set SSL_BACKENDS
- configure: avoid unportable `==' test(1) operator
- configure: error out if OpenSSL wasn't detected when asked for
- configure: fix default location for fish completions
- cookie: Guard against possible NULL ptr deref
- curl: make code work with protocol-disabled libcurl
- curl: report error for "--no-" on non-boolean options
- curl_easy_getinfo.3: fix minor formatting mistake
- curlver.h: use parenthesis in CURL_VERSION_BITS macro
- docs/BUG-BOUNTY: bug bounty time
- docs/INSTALL: fix broken link
- docs/RELEASE-PROCEDURE: link to live iCalendar
- documentation: Fix several typos
- doh: acknowledge CURL_DISABLE_DOH
- doh: disable DOH for the cases it doesn't work
- examples: remove unused variables
- ftplistparser: fix LGTM alert "Empty block without comment"
- hostip: acknowledge CURL_DISABLE_SHUFFLE_DNS
- http: Ignore HTTP/2 prior knowledge setting for HTTP proxies
- http: acknowledge CURL_DISABLE_HTTP_AUTH
- http: mark bundle as not for multiuse on < HTTP/2 response
- http_digest: Don't expose functions when HTTP and Crypto Auth are disabled
- http_negotiate: do not treat failure of gss_init_sec_context() as fatal
- http_ntlm: Corrected the name of the include guard
- http_ntlm_wb: Handle auth for only a single request
- http_ntlm_wb: Return the correct error on receiving an empty auth message
- lib509: add missing include for strdup
- lib557: initialize variables
- makedebug: Fix ERRORLEVEL detection after running where.exe
- mbedtls: enable use of EC keys
- mime: acknowledge CURL_DISABLE_MIME
- multi: improved HTTP_1_1_REQUIRED handling
- netrc: acknowledge CURL_DISABLE_NETRC
- nss: allow fifos and character devices for certificates
- nss: provide more specific error messages on failed init
- ntlm: Fix misaligned function comments for Curl_auth_ntlm_cleanup
- ntlm: Support the NT response in the type-3 when OpenSSL doesn't include MD4
- openssl: mark connection for close on TLS close_notify
- openvms: Remove pre-processor for SecureTransport
- openvms: Remove pre-processors for Windows
- parse_proxy: use the URL parser API
- parsedate: disabled on CURL_DISABLE_PARSEDATE
- pingpong: disable more when no pingpong protocols are enabled
- polarssl_threadlock: remove conditionally unused code
- progress: acknowledge CURL_DISABLE_PROGRESS_METER
- proxy: acknowledge DISABLE_PROXY more
- resolve: apply Happy Eyeballs philosophy to parallel c-ares queries
- revert "multi: support verbose conncache closure handle"
- sasl: Don't send authcid as authzid for the PLAIN mechanism as per RFC 4616
- sasl: only enable if there's a protocol enabled using it
- scripts: fix typos
- singleipconnect: show port in the verbose "Trying ..." message
- smtp: fix compiler warning
- socks5: user name and passwords must be shorter than 256
- socks: fix error message
- socksd: new SOCKS 4+5 server for tests
- spnego_gssapi: fix return code on gss_init_sec_context() failure
- ssh-libssh: remove unused variable
- ssh: define USE_SSH if SSH is enabled (any backend)
- ssh: move variable declaration to where it's used
- test1002: correct the name
- test2100: Fix typos in test description
- tests/server/util: fix Windows Unicode build
- tests: Run global cleanup at end of tests
- tests: make Impacket (SMB server) Python 3 compatible
- tool_cb_wrt: fix bad-function-cast warning
- tool_formparse: remove redundant assignment
- tool_help: Warn if curl and libcurl versions do not match
- tool_help: include for strcasecmp
- transfer: fix LGTM alert "Comparison is always true"
- travis: add an osx http-only build
- travis: allow builds on branches named "ci"
- travis: install dependencies only when needed
- travis: update some builds do Xenial
- travis: updated mesalink builds
- url: always clone the CUROPT_CURLU handle
- url: convert the zone id from a IPv6 URL to correct scope id
- urlapi: add CURLUPART_ZONEID to set and get
- urlapi: increase supported scheme length to 40 bytes
- urlapi: require a non-zero host name length when parsing URL
- urlapi: stricter CURLUPART_PORT parsing
- urlapi: strip off zone id from numerical IPv6 addresses
- urlapi: urlencode characters above 0x7f correctly
- vauth/cleartext: update the PLAIN login to match RFC 4616
- vauth/oauth2: Fix OAUTHBEARER token generation
- vauth: Fix incorrect function description for Curl_auth_user_contains_domain
- vtls: fix potential ssl_buffer stack overflow
- wildcard: disable from build when FTP isn't present
- winbuild: Support MultiSSL builds
- xattr: skip unittest on unsupported platforms

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.1-0
- alt-svc: experiemental support added
- configure: add --with-amissl
- AppVeyor: add MinGW-w64 and classic Mingw builds
- AppVeyor: switch VS 2015 builds to VS 2017 image
- CURLU: fix NULL dereference when used over proxy
- Curl_easy: remove req.maxfd - never used!
- Curl_now: figure out windows version in win32_init:
- Curl_resolv: fix a gcc -Werror=maybe-uninitialized warning
- DoH: inherit some SSL options from user's easy handle
- Secure Transport: no more "darwinssl"
- Secure Transport: tvOS 11 is required for ALPN support
- cirrus: Added FreeBSD builds using Cirrus CI
- cleanup: make local functions static
- cli tool: do not use mime.h private structures
- cmdline-opts/proxytunnel.d: the option tunnnels all protocols
- configure: add additional libraries to check for LDAP support
- configure: remove the unused fdopen macro
- configure: show features as well in the final summary
- conncache: use conn->data to know if a transfer owns it
- connection: never reuse CONNECT_ONLY connections
- connection_check: restore original conn->data after the check
- connection_check: set ->data to the transfer doing the check
- cookie: Add support for cookie prefixes
- cookies: dotless names can set cookies again
- cookies: fix NULL dereference if flushing cookies with no CookieInfo set
- curl.1: --user and --proxy-user are hidden from ps output
- curl.1: mark the argument to --cookie as
- curl.h: use __has_declspec_attribute for shared builds
- curl: display --version features sorted alphabetically
- curl: fix FreeBSD compiler warning in the --xattr code
- curl: remove MANUAL from -M output
- curl_easy_duphandle.3: clarify that a duped handle has no shares
- curl_multi_remove_handle.3: use at any time, just not from within callbacks
- curl_url.3: this API is not experimental anymore
- dns: release sharelock as soon as possible
- docs: update max-redirs.d phrasing
- easy: fix win32 init to work without CURL_GLOBAL_WIN32
- examples/10-at-a-time.c: improve readability and simplify
- examples/cacertinmem.c: use multiple certificates for loading CA-chain
- examples/crawler: Fix the Accept-Encoding setting
- examples/ephiperfifo.c: various fixes
- examples/externalsocket: add missing close socket calls
- examples/http2-download: cleaned up
- examples/http2-serverpush: add some sensible error checks
- examples/http2-upload: cleaned up
- examples/httpcustomheader: Value stored to 'res' is never read
- examples/postinmemory: Potential leak of memory pointed to by 'chunk.memory'
- examples/sftpuploadresume: Value stored to 'result' is never read
- examples: only include
- examples: remove recursive calls to curl_multi_socket_action
- examples: remove superfluous null-pointer checks
- file: fix "Checking if unsigned variable 'readcount' is less than zero."
- fnmatch: disable if FTP is disabled
- gnutls: remove call to deprecated gnutls_compression_get_name
- gopher: remove check for path == NULL
- gssapi: fix deprecated header warnings
- hostip: make create_hostcache_id avoid alloc + free
- http2: multi_connchanged() moved from multi.c, only used for h2
- http2: verify :athority in push promise requests
- http: make adding a blank header thread-safe
- http: send payload when (proxy) authentication is done
- http: set state.infilesize when sending multipart formposts
- makefile: make checksrc and hugefile commands "silent"
- mbedtls: make it build even if MBEDTLS_VERSION_C isn't set
- mbedtls: release sessionid resources on error
- memdebug: log pointer before freeing its data
- memdebug: make debug-specific functions use curl_dbg_ prefix
- mime: put the boundary buffer into the curl_mime struct
- multi: call multi_done on connect timeouts, fixes CURLINFO_TOTAL_TIME
- multi: remove verbose "Expire in" ... messages
- multi: removed unused code for request retries
- multi: support verbose conncache closure handle
- negotiate: fix for HTTP POST with Negotiate
- openssl: add support for TLS ASYNC state
- openssl: if cert type is ENG and no key specified, key is ENG too
- pretransfer: don't strlen() POSTFIELDS set for GET requests
- rand: Fix a mismatch between comments in source and header
- runtests: detect "schannel" as an alias for "winssl"
- schannel: be quiet - remove verbose output
- schannel: close TLS before removing conn from cache
- schannel: support CALG_ECDH_EPHEM algorithm
- scripts/completion.pl: also generate fish completion file
- singlesocket: fix the 'sincebefore' placement
- source: fix two 'nread' may be used uninitialized warnings
- ssh: fix Condition '!status' is always true
- ssh: loop the state machine if not done and not blocking
- strerror: make the strerror function use local buffers
- system_win32: move win32_init here from easy.c
- test578: make it read data from the correct test
- tests: Fixed XML validation errors in some test files
- tests: add stderr comparison to the test suite
- tests: fix multiple may be used uninitialized warnings
- threaded-resolver: shutdown the resolver thread without error message
- tool_cb_wrt: fix writing to Windows null device NUL
- tool_getpass: termios.h is present on AmigaOS 3, but no tcgetattr/tcsetattr
- tool_operate: build on AmigaOS
- tool_operate: fix typecheck warning
- transfer.c: do not compute length of undefined hex buffer
- travis: add build using gnutls
- travis: add scan-build
- travis: bump the used wolfSSL version to 4.0.0
- travis: enable valgrind for the iconv tests
- travis: use updated compiler versions: clang 7 and gcc 8
- unit1307: require FTP support
- unit1651: survive curl_easy_init() fails
- url/idnconvert: remove scan for <= 32 ascii values
- url: change conn shutdown order to ensure SOCKETFUNCTION callbacks
- urlapi: reduce variable scope, remove unreachable 'break'
- urldata: convert bools to bitfields and move to end
- urldata: simplify bytecounters
- urlglob: Argument with 'nonnull' attribute passed null
- version.c: silent scan-build even when librtmp is not enabled
- vtls: rename some of the SSL functions
- wolfssl: stop custom-adding curves
- x509asn1: "Dereference of null pointer"
- x509asn1: cleanup and unify code layout
- zsh.pl: escape ':' character
- zsh.pl: update regex to better match curl -h output

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.0-0
- cookies: leave secure cookies alone
- hostip: support wildcard hosts
- http: Implement trailing headers for chunked transfers
- http: added options for allowing HTTP/0.9 responses
- timeval: Use high resolution timestamps on Windows
- CVE-2018-16890: NTLM type-2 out-of-bounds buffer read
- CVE-2019-3822: NTLMv2 type-3 header stack buffer overflow
- CVE-2019-3823: SMTP end-of-response out-of-bounds read
- FAQ: remove mention of sourceforge for github
- OS400: handle memory error in list conversion
- OS400: upgrade ILE/RPG binding.
- README: add codacy code quality badge
- Revert http_negotiate: do not close connection
- THANKS: added several missing names from year <= 2000
- build: make 'tidy' target work for metalink builds
- cmake: added checks for variadic macros
- cmake: updated check for HAVE_POLL_FINE to match autotools
- cmake: use lowercase for function name like the rest of the code
- configure: detect xlclang separately from clang
- configure: fix recv/send/select detection on Android
- configure: rewrite --enable-code-coverage
- conncache_unlock: avoid indirection by changing input argument type
- cookie: fix comment typo
- cookies: allow secure override when done over HTTPS
- cookies: extend domain checks to non psl builds
- cookies: skip custom cookies when redirecting cross-site
- curl --xattr: strip credentials from any URL that is stored
- curl -J: refuse to append to the destination file
- curl/urlapi.h: include "curl.h" first
- curl_multi_remove_handle() don't block terminating c-ares requests
- darwinssl: accept setting max-tls with default min-tls
- disconnect: separate connections and easy handles better
- disconnect: set conn->data for protocol disconnect
- docs/version.d: mention MultiSSL
- docs: fix the --tls-max description
- docs: use $(INSTALL_DATA) to install man page
- docs: use meaningless port number in CURLOPT_LOCALPORT example
- gopher: always include the entire gopher-path in request
- http2: clear pause stream id if it gets closed
- if2ip: remove unused function Curl_if_is_interface_name
- libssh: do not let libssh create socket
- libssh: enable CURLOPT_SSH_KNOWNHOSTS and CURLOPT_SSH_KEYFUNCTION for libssh
- libssh: free sftp_canonicalize_path() data correctly
- libtest/stub_gssapi: use "real" snprintf
- mbedtls: use VERIFYHOST
- multi: multiplexing improvements
- multi: set the EXPIRE_*TIMEOUT timers at TIMER_STARTSINGLE time
- ntlm: fix NTMLv2 compliance
- ntlm_sspi: add support for channel binding
- openssl: adapt to 3.0.0, OpenSSL_version_num() is deprecated
- openssl: fix the SSL_get_tlsext_status_ocsp_resp call
- openvms: fix OpenSSL discovery on VAX
- openvms: fix typos in documentation
- os400: add a missing closing bracket
- os400: fix extra parameter syntax error
- pingpong: change default response timeout to 120 seconds
- pingpong: ignore regular timeout in disconnect phase
- printf: fix format specifiers
- runtests.pl: Fix perl call to include srcdir
- schannel: fix compiler warning
- schannel: preserve original certificate path parameter
- schannel: stop calling it "winssl"
- sigpipe: if mbedTLS is used, ignore SIGPIPE
- smb: fix incorrect path in request if connection reused
- ssh: log the libssh2 error message when ssh session startup fails
- test1558: verify CURLINFO_PROTOCOL on file:// transfer
- test1561: improve test name
- test1653: make it survive torture tests
- tests: allow tests to pass by 2037-02-12
- tests: move objnames-* from lib into tests
- timediff: fix math for unsigned time_t
- timeval: Disable MSVC Analyzer GetTickCount warning
- tool_cb_prg: avoid integer overflow
- travis: added cmake build for osx
- urlapi: Fix port parsing of eol colon
- urlapi: distinguish possibly empty query
- urlapi: fix parsing ipv6 with zone index
- urldata: rename easy_conn to just conn
- winbuild: conditionally use /DZLIB_WINAPI
- wolfssl: fix memory-leak in threaded use
- spnego_sspi: add support for channel binding

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 7.63.0-0
- curl: add %%{stderr} and %%{stdout} for --write-out
- curl: add undocumented option --dump-module-paths for win32
- setopt: add CURLOPT_CURLU
- (lib)curl.rc: fixup for minor bugs
- CURLINFO_REDIRECT_URL: extract the Location: header field unvalidated
- CURLOPT_HEADERFUNCTION.3: match 'nitems' name in synopsis and description
- CURLOPT_WRITEFUNCTION.3: spell out that it gets called many times
- Curl_follow: accept non-supported schemes for "fake" redirects
- KNOWN_BUGS: add --proxy-any connection issue
- NTLM: Remove redundant ifdef USE_OPENSSL
- NTLM: force the connection to HTTP/1.1
- OS400: add URL API ccsid wrappers and sync ILE/RPG bindings
- SECURITY-PROCESS: bountygraph shuts down again
- TODO: Have the URL API offer IDN decoding
- ares: remove fd from multi fd set when ares is about to close the fd
- axtls: removed
- checksrc: add COPYRIGHTYEAR check
- cmake: fix MIT/Heimdal Kerberos detection
- configure: include all libraries in ssl-libs fetch
- configure: show CFLAGS, LDFLAGS etc in summary
- connect: fix building for recent versions of Minix
- cookies: create the cookiejar even if no cookies to save
- cookies: expire "Max-Age=0" immediately
- curl: --local-port range was not "including"
- curl: fix --local-port integer overflow
- curl: fix memory leak reading --writeout from file
- curl: fixed UTF-8 in current console code page (Windows)
- curl_easy_perform: fix timeout handling
- curl_global_sslset(): id == -1 is not necessarily an error
- curl_multibyte: fix a malloc overcalculation
- curle: move deprecated error code to ifndef block
- docs: curl_formadd field and file names are now escaped
- docs: escape "\n" codes
- doh: fix memory leak in OOM situation
- doh: make it work for h2-disabled builds too
- examples/ephiperfifo: report error when epoll_ctl fails
- ftp: avoid two unsigned int overflows in FTP listing parser
- host names: allow trailing dot in name resolve, then strip it
- http2: Upon HTTP_1_1_REQUIRED, retry the request with HTTP/1.1
- http: don't set CURLINFO_CONDITION_UNMET for http status code 204
- http: fix HTTP Digest auth to include query in URI
- http_negotiate: do not close connection until negotiation is completed
- impacket: add LICENSE
- infof: clearly indicate truncation
- ldap: fix LDAP URL parsing regressions
- libcurl: stop reading from paused transfers
- mprintf: avoid unsigned integer overflow warning
- netrc: don't ignore the login name specified with "--user"
- nss: Fall back to latest supported SSL version
- nss: Fix compatibility with nss versions 3.14 to 3.15
- nss: fix fallthrough comment to fix picky compiler warning
- nss: remove version selecting dead code
- nss: set default max-tls to 1.3/1.2
- openssl: Remove SSLEAY leftovers
- openssl: do not log excess "TLS app data" lines for TLS 1.3
- openssl: do not use file BIOs if not requested
- openssl: fix unused variable compiler warning with old openssl
- openssl: support session resume with TLS 1.3
- openvms: fix example name
- os400: Add curl_easy_conn_upkeep() to ILE/RPG binding
- os400: add CURLOPT_CURLU to ILE/RPG binding
- os400: fix return type of curl_easy_pause() in ILE/RPG binding
- packages: remove old leftover files and dirs
- pop3: only do APOP with a valid timestamp
- runtests: use the local curl for verifying
- schannel: be consistent in Schannel capitalization
- schannel: better CURLOPT_CERTINFO support
- schannel: use Curl_ prefix for global private symbols
- snprintf: renamed and we now only use msnprintf()
- ssl: fix compilation with OpenSSL 0.9.7
- ssl: replace all internal uses of CURLE_SSL_CACERT
- symbols-in-versions: add missing CURLU_ symbols
- test328: verify Content-Encoding: none
- tests: disable SO_EXCLUSIVEADDRUSE for stunnel on Windows
- tests: drop http_pipe.py script no longer used
- tool_cb_wrt: Silence function cast compiler warning
- tool_doswin: Fix uninitialized field warning
- travis: build with clang sanitizers
- travis: remove curl before a normal build
- url: a short host name + port is not a scheme
- url: fix IPv6 numeral address parser
- urlapi: only skip encoding the first '=' with APPENDQUERY set

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 7.62.0-0
- multiplex: enable by default
- url: default to CURL_HTTP_VERSION_2TLS if built h2-enabled
- setopt: add CURLOPT_DOH_URL
- curl: --doh-url added
- setopt: add CURLOPT_UPLOAD_BUFFERSIZE: set upload buffer size
- imap: change from "FETCH" to "UID FETCH"
- configure: add option to disable automatic OpenSSL config loading
- upkeep: add a connection upkeep API: curl_easy_upkeep()
- URL-API: added five new functions
- vtls: MesaLink is a new TLS backend
- CVE-2018-16839: SASL password overflow via integer overflow
- CVE-2018-16840: use-after-free in handle close
- CVE-2018-16842: warning message out-of-buffer read
- CURLOPT_DNS_USE_GLOBAL_CACHE: deprecated
- Curl_dedotdotify(): always nul terminate returned string
- Curl_follow: Always free the passed new URL
- Curl_http2_done: fix memleak in error path
- Curl_retry_request: fix memory leak
- Curl_saferealloc: Fixed typo in docblock
- FILE: fix CURLOPT_NOBODY and CURLOPT_HEADER output
- GnutTLS: TLS 1.3 support
- SECURITY-PROCESS: mention the bountygraph program
- VS projects: add USE_IPV6:
- Windows: fixes for MinGW targeting Windows Vista
- anyauthput: fix compiler warning on 64-bit Windows
- appveyor: add WinSSL builds
- appveyor: run test suite (on Windows!)
- certs: generate tests certs with sha256 digest algorithm
- checksrc: enable strict mode and warnings
- checksrc: handle zero scoped ignore commands
- cmake: Backport to work with CMake 3.0 again
- cmake: Improve config installation
- cmake: add support for transitive ZLIB target
- cmake: disable -Wpedantic-ms-format
- cmake: don't require OpenSSL if USE_OPENSSL=OFF
- cmake: fixed path used in generation of docs/tests
- cmake: remove unused *SOCKLEN_T variables
- cmake: suppress MSVC warning C4127 for libtest
- cmake: test and set missed defines during configuration
- comment: Fix multiple typos in function parameters
- config: Remove unused SIZEOF_VOIDP
- config_win32: enable LDAPS
- configure: force-use -lpthreads on HPUX
- configure: remove CURL_CONFIGURE_CURL_SOCKLEN_T
- configure: s/AC_RUN_IFELSE/CURL_RUN_IFELSE
- cookies: Remove redundant expired check
- cookies: fix leak when writing cookies to file
- curl-config.in: remove dependency on bc
- curl.1: --ipv6 mutexes ipv4 (fixed typo)
- curl: enabled Windows VT Support and UTF-8 output
- curl: update the documentation of --tlsv1.0
- curl_multi_wait: call getsock before figuring out timeout
- curl_ntlm_wb: check aprintf() return codes
- curl_threads: fix classic MinGW compile break
- darwinssl: Fix realloc memleak
- darwinssl: more specific and unified error codes
- data-binary.d: clarify default content-type is x-www-form-urlencoded
- docs/BUG-BOUNTY: explain the bounty program
- docs/CIPHERS: Mention the options used to set TLS 1.3 ciphers
- docs/CIPHERS: fix the TLS 1.3 cipher names
- docs/CIPHERS: mention the colon separation for OpenSSL
- docs/examples: URL updates
- docs: add "see also" links for SSL options
- example/asiohiper: insert warning comment about its status
- example/htmltidy: fix include paths of tidy libraries
- examples/Makefile.m32: sync with core
- examples/http2-pushinmemory: receive HTTP/2 pushed files in memory
- examples/parseurl.c: show off the URL API
- examples: Fix memory leaks from realloc errors
- examples: do not wait when no transfers are running
- ftp: include command in Curl_ftpsend sendbuffer
- gskit: make sure to terminate version string
- gtls: Values stored to but never read
- hostip: fix check on Curl_shuffle_addr return value
- http2: fix memory leaks on error-path
- http: fix memleak in rewind error path
- krb5: fix memory leak in krb_auth
- ldap: show precise LDAP call in error message on Windows
- lib: fix gcc8 warning on Windows
- memory: add missing curl_printf header
- memory: ensure to check allocation results
- multi: Fix error handling in the SENDPROTOCONNECT state
- multi: fix memory leak in content encoding related error path
- multi: make the closure handle "inherit" CURLOPT_NOSIGNAL
- netrc: free temporary strings if memory allocation fails
- nss: fix nssckbi module loading on Windows
- nss: try to connect even if libnssckbi.so fails to load
- ntlm_wb: Fix memory leaks in ntlm_wb_response
- ntlm_wb: bail out if the response gets overly large
- openssl: assume engine support in 0.9.8 or later
- openssl: enable TLS 1.3 post-handshake auth
- openssl: fix gcc8 warning
- openssl: load built-in engines too
- openssl: make 'done' a proper boolean
- openssl: output the correct cipher list on TLS 1.3 error
- openssl: return CURLE_PEER_FAILED_VERIFICATION on failure to parse issuer
- openssl: show "proper" version number for libressl builds
- pipelining: deprecated
- rand: add comment to skip a clang-tidy false positive
- rtmp: fix for compiling with lwIP
- runtests: ignore disabled even when ranges are given
- runtests: skip ld_preload tests on macOS
- runtests: use Windows paths for Windows curl
- schannel: unified error code handling
- sendf: Fix whitespace in infof/failf concatenation
- ssh: free the session on init failures
- ssl: deprecate CURLE_SSL_CACERT in favour of a unified error code
- system.h: use proper setting with Sun C++ as well
- test1299: use single quotes around asterisk
- test1452: mark as flaky
- test1651: unit test Curl_extract_certinfo()
- test320: strip out more HTML when comparing
- tests/negtelnetserver.py: fix Python2-ism in neg TELNET server
- tests: add unit tests for url.c
- timeval: fix use of weak symbol clock_gettime() on Apple platforms
- tool_cb_hdr: handle failure of rename()
- travis: add a "make tidy" build that runs clang-tidy
- travis: add build for "configure --disable-verbose"
- travis: bump the Secure Transport build to use xcode
- travis: make distcheck scan for BOM markers
- unit1300: fix stack-use-after-scope AddressSanitizer warning
- urldata: Fix "connecting" comment
- urlglob: improve error message on bad globs
- vtls: fix ssl version "or later" behavior change for many backends
- x509asn1: Fix SAN IP address verification
- x509asn1: always check return code from getASN1Element()
- x509asn1: return CURLE_PEER_FAILED_VERIFICATION on failure to parse cert
- x509asn1: suppress left shift on signed value

* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.1-0
- security advisory (CVE-2018-14618): NTLM password overflow via integer
  overflow
- CURLINFO_SIZE_UPLOAD: fix missing counter update
- CURLOPT_ACCEPT_ENCODING.3: list them comma-separated
- CURLOPT_SSL_CTX_FUNCTION.3: might cause accidental connection reuse
- Curl_getoff_all_pipelines: improved for multiplexed
- DEPRECATE: remove release date from 7.62.0
- HTTP: Don't attempt to needlessly decompress redirect body
- INTERNALS: require GnuTLS >= 2.11.3
- README.md: add LGTM.com code quality grade for C/C++
- SSLCERTS: improve the openssl command line
- Silence GCC 8 cast-function-type warnings
- ares: check for NULL in completed-callback
- asyn-thread: Remove unused macro
- auth: only pick CURLAUTH_BEARER if we *have* a Bearer token
- auth: pick Bearer authentication whenever a token is available
- cmake: CMake config files are defining CURL_STATICLIB for static builds
- cmake: Respect BUILD_SHARED_LIBS
- cmake: Update scripts to use consistent style
- cmake: bumped minimum version to 3.4
- cmake: link curl to the OpenSSL targets instead of lib absolute paths
- configure: conditionally enable pedantic-errors
- configure: fix for -lpthread detection with OpenSSL and pkg-config
- conn: remove the boolean 'inuse' field
- content_encoding: accept up to 4 unknown trailer bytes after raw deflate data
- cookie tests: treat files as text
- cookies: support creation-time attribute for cookies
- curl: Fix segfault when -H @headerfile is empty
- curl: add http code 408 to transient list for --retry
- curl: fix time-of-check, time-of-use race in dir creation
- curl: use Content-Disposition before the "URL end" for -OJ
- curl: warn the user if a given file name looks like an option
- curl_threads: silence bad-function-cast warning
- darwinssl: add support for ALPN negotiation
- docs/CURLOPT_URL: fix indentation
- docs/CURLOPT_WRITEFUNCTION: size is always 1
- docs/SECURITY-PROCESS: mention bounty, drop pre-notify
- docs/examples: add hiperfifo example using linux epoll/timerfd
- docs: add disallow-username-in-url.d and haproxy-protocol.d to dist
- docs: clarify NO_PROXY env variable functionality
- docs: improved the manual pages of some callbacks
- docs: mention NULL is fine input to several functions
- formdata: Remove unused macro HTTPPOST_CONTENTTYPE_DEFAULT
- gopher: Do not translate `?' to `%09'
- header output: switch off all styles, not just unbold
- hostip: fix unused variable warning
- http2: Use correct format identifier for stream_id
- http2: abort the send_callback if not setup yet
- http2: avoid set_stream_user_data() before stream is assigned
- http2: check nghttp2_session_set_stream_user_data return code
- http2: clear the drain counter in Curl_http2_done
- http2: make sure to send after RST_STREAM
- http2: separate easy handle from connections better
- http: fix for tiny "HTTP/0.9" response
- http_proxy: Remove unused macro SELECT_TIMEOUT
- lib/Makefile: only do symbol hiding if told to
- lib1502: fix memory leak in torture test
- lib1522: fix curl_easy_setopt argument type
- libcurl-thread.3: expand somewhat on the NO_SIGNAL motivation
- mime: check Curl_rand_hex's return code
- multi: always do the COMPLETED procedure/state
- openssl: assume engine support in 1.0.0 or later
- openssl: fix debug messages
- projects: Improve Windows perl detection in batch scripts
- retry: return error if rewind was necessary but didn't happen
- reuse_conn(): memory leak - free old_conn->options
- schannel: client certificate store opening fix
- schannel: enable CALG_TLS1PRF for w32api >= 5.1
- schannel: fix MinGW compile break
- sftp: don't send post-qoute sequence when retrying a connection
- smb: fix memory leak on early failure
- smb: fix memory-leak in URL parse error path
- smb_getsock: always wait for write socket too
- ssh-libssh: fix infinite connect loop on invalid private key
- ssh-libssh: reduce excessive verbose output about pubkey auth
- ssh-libssh: use FALLTHROUGH to silence gcc8
- ssl: set engine implicitly when a PKCS#11 URI is provided
- sws: handle EINTR when calling select()
- system_win32: fix version checking
- telnet: Remove unused macros TELOPTS and TELCMDS
- test1143: disable MSYS2's POSIX path conversion
- test1148: disable if decimal separator is not point
- test1307: (fnmatch testing) disabled
- test1422: add required file feature
- test1531: Add timeout
- test1540: Remove unused macro TEST_HANG_TIMEOUT
- test214: disable MSYS2's POSIX path conversion for URL
- test320: treat curl320.out file as binary
- tests/http_pipe.py: Use /usr/bin/env to find python
- tests: Don't use Windows path %%PWD for SSH tests
- tests: fixes for Windows line endlings
- tool_operate: Fix setting proxy TLS 1.3 ciphers
- travis: build darwinssl on macos 10.12 to fix linker errors
- travis: execute "set -eo pipefail" for coverage build
- travis: run a 'make checksrc' too
- travis: update to GCC-8
- travis: verify that man pages can be regenerated
- upload: allocate upload buffer on-demand
- upload: change default UPLOAD_BUFSIZE to 64KB
- urldata: remove unused pipe_broke struct field
- vtls: reinstantiate engine on duplicated handles
- windows: implement send buffer tuning
- wolfSSL/CyaSSL: Fix memory leak in Curl_cyassl_random

* Thu Aug 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.0-0
- getinfo: add microsecond precise timers for seven intervals
- curl: show headers in bold, switch off with --no-styled-output
- httpauth: add support for Bearer tokens
- Add CURLOPT_TLS13_CIPHERS and CURLOPT_PROXY_TLS13_CIPHERS
- curl: --tls13-ciphers and --proxy-tls13-ciphers
- Add CURLOPT_DISALLOW_USERNAME_IN_URL
- curl: --disallow-username-in-url
- CVE-2018-0500: smtp: fix SMTP send buffer overflow
- schannel: disable client cert option if APIs not available
- schannel: disable manual verify if APIs not available
- tests/libtest/Makefile: Do not unconditionally add gcc-specific flags
- openssl: acknowledge --tls-max for default version too
- stub_gssapi: fix 'unused parameter' warnings
- examples/progressfunc: make it build on both new and old libcurls
- docs: mention it is HA Proxy protocol "version 1"
- curl_fnmatch: only allow two asterisks for matching
- docs: clarify CURLOPT_HTTPGET
- configure: replace a AC_TRY_RUN with CURL_RUN_IFELSE
- configure: do compile-time SIZEOF checks instead of run-time
- checksrc: make sure sizeof() is used *with* parentheses
- CURLOPT_ACCEPT_ENCODING.3: add brotli and clarify a bit
- schannel: make CAinfo parsing resilient to CR/LF
- tftp: make sure error is zero terminated before printfing it
- http resume: skip body if http code 416 (range error) is ignored
- configure: add basic test of --with-ssl prefix
- cmake: set -d postfix for debug builds
- multi: provide a socket to wait for in Curl_protocol_getsock
- content_encoding: handle zlib versions too old for Z_BLOCK
- winbuild: only delete OUTFILE if it exists
- winbuild: In MakefileBuild.vc fix typo DISTDIR->DIRDIST
- schannel: add failf calls for client certificate failures
- cmake: Fix the test for fsetxattr and strerror_r
- curl.1: Fix cmdline-opts reference errors
- cmdline-opts/gen.pl: warn if mutexes: or see-also: list non-existing options
- cmake: check for getpwuid_r
- configure: fix ssh2 linking when built with a static mbedtls
- psl: use latest psl and refresh it periodically
- fnmatch: insist on escaped bracket to match
- KNOWN_BUGS: restore text regarding #2101
- INSTALL: LDFLAGS=-Wl,-R/usr/local/ssl/lib
- configure: override AR_FLAGS to silence warning
- os400: implement mime api EBCDIC wrappers
- curl.rc: embed manifest for correct Windows version detection
- strictness: correct {infof, failf} format specifiers
- tests: update .gitignore for libtests
- configure: check for declaration of getpwuid_r
- fnmatch: use the system one if available
- CURLOPT_RESOLVE: always purge old entry first
- multi: remove a potentially bad DEBUGF()
- curl_addrinfo: use same #ifdef conditions in source as header
- build: remove the Borland specific makefiles
- axTLS: not considered fit for use
- cmdline-opts/cert-type.d: mention "p12" as a recognized type
- system.h: add support for IBM xlc C compiler
- tests/libtest: Add lib1521 to nodist_SOURCES
- mk-ca-bundle.pl: leave certificate name untouched
- boringssl + schannel: undef X509_NAME in lib/schannel.h
- openssl: assume engine support in 1.0.1 or later
- cppcheck: fix warnings
- test 46: make test pass after year 2025
- schannel: support selecting ciphers
- Curl_debug: remove dead printhost code
- test 1455: unflakified
- Curl_init_do: handle NULL connection pointer passed in
- progress: remove a set of unused defines
- mk-ca-bundle.pl: make -u delete certdata.txt if found not changed
- GOVERNANCE.md: explains how this project is run
- configure: use pkg-config for c-ares detection
- configure: enhance ability to build with static openssl
- maketgz: fix sed issues on OSX
- multi: fix memory leak when stopped during name resolve
- CURLOPT_INTERFACE.3: interface names not supported on Windows
- url: fix dangling conn->data pointer
- cmake: allow multiple SSL backends
- system.h: fix for gcc on 32 bit OpenServer
- ConnectionExists: make sure conn->data is set when "taking" a connection
- multi: fix crash due to dangling entry in connect-pending list
- CURLOPT_SSL_VERIFYPEER.3: Add performance note
- netrc: use a larger buffer to support longer passwords
- url: check Curl_conncache_add_conn return code
- configure: Add dependent libraries after crypto
- easy_perform: faster local name resolves by using *multi_timeout()
- getnameinfo: not used, removed all configure checks
- travis: add a build using the synchronous name resolver
- CURLINFO_TLS_SSL_PTR.3: improve the example
- openssl: allow TLS 1.3 by default
- openssl: make the requested TLS version the *minimum* wanted
- openssl: Remove some dead code
- telnet: fix clang warnings
- DEPRECATE: new doc describing planned item removals
- example/crawler.c: simple crawler based on libxml2
- libssh: goto DISCONNECT state on error, not SESSION_FREE
- CMake: Remove unused functions
- darwinssl: allow High Sierra users to build the code using GCC
- scripts: include _curl as part of CLEANFILES

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.60.0-0
- Add CURLOPT_HAPROXYPROTOCOL, support for the HAProxy PROXY protocol
- Add --haproxy-protocol for the command line tool
- Add CURLOPT_DNS_SHUFFLE_ADDRESSES, shuffle returned IP addresses
- FTP: shutdown response buffer overflow CVE-2018-1000300
- RTSP: bad headers buffer over-read CVE-2018-1000301
- FTP: fix typo in recursive callback detection for seeking
- test1208: marked flaky
- HTTP: make header-less responses still count correct body size
- user-agent.d:: mention --proxy-header as well
- http2: fixes typo
- cleanup: misc typos in strings and comments
- rate-limit: use three second window to better handle high speeds
- examples/hiperfifo.c: improved
- pause: when changing pause state, update socket state
- multi: improved pending transfers handling => improved performance
- curl_version_info.3: fix ssl_version description
- add_handle/easy_perform: clear errorbuffer on start if set
- darwinssl: fix iOS build
- cmake: add support for brotli
- parsedate: support UT timezone
- vauth/ntlm.h: fix the #ifdef header guard
- lib/curl_path.h: added #ifdef header guard
- vauth/cleartext: fix integer overflow check
- CURLINFO_COOKIELIST.3: made the example not leak memory
- cookie.d: mention that "-" as filename means stdin
- CURLINFO_SSL_VERIFYRESULT.3: fixed the example
- http2: read pending frames (including GOAWAY) in connection-check
- timeval: remove compilation warning by casting
- cmake: avoid warn-as-error during config checks
- travis-ci: enable -Werror for CMake builds
- openldap: fix for NULL return from ldap_get_attribute_ber()
- threaded resolver: track resolver time and set suitable timeout values
- cmake: Add advapi32 as explicit link library for win32
- docs: fix CURLINFO_*_T examples use of CURL_FORMAT_CURL_OFF_T
- test1148: set a fixed locale for the test
- cookies: when reading from a file, only remove_expired once
- cookie: store cookies per top-level-domain-specific hash table
- openssl: fix build with LibreSSL 2.7
- tls: fix mbedTLS 2.7.0 build + handle sha256 failures
- openssl: RESTORED verify locations when verifypeer==0
- file: restore old behavior for file:////foo/bar URLs
- FTP: allow PASV on IPv6 connections when a proxy is being used
- build-openssl.bat: allow custom paths for VS and perl
- winbuild: make the clean target work without build-type
- build-openssl.bat: Refer to VS2017 as VC14.1 instead of VC15
- curl: retry on FTP 4xx, ignore other protocols
- configure: detect (and use) sa_family_t
- examples/sftpuploadresume: Fix Windows large file seek
- build: cleanup to fix clang warnings/errors
- winbuild: updated the documentation
- lib: silence null-dereference warnings
- travis: bump to clang 6 and gcc 7
- travis: build libpsl and make builds use it
- proxy: show getenv proxy use in verbose output
- duphandle: make sure CURLOPT_RESOLVE is duplicated
- all: Refactor malloc+memset to use calloc
- checksrc: Fix typo
- system.h: Add sparcv8plus to oracle/sunpro 32-bit detection
- vauth: Fix typo
- ssh: show libSSH2 error code when closing fails
- test1148: tolerate progress updates better
- urldata: make service names unconditional
- configure: keep LD_LIBRARY_PATH changes local
- ntlm_sspi: fix authentication using Credential Manager
- schannel: add client certificate authentication
- winbuild: Support custom devel paths for each dependency
- schannel: add support for CURLOPT_CAINFO
- http2: handle on_begin_headers() called more than once
- openssl: support OpenSSL 1.1.1 verbose-mode trace messages
- openssl: fix subjectAltName check on non-ASCII platforms
- http2: avoid strstr() on data not zero terminated
- http2: clear the "drain counter" when a stream is closed
- http2: handle GOAWAY properly
- tool_help: clarify --max-time unit of time is seconds
- curl.1: clarify that options and URLs can be mixed
- http2: convert an assert to run-time check
- curl_global_sslset: always provide available backends
- ftplistparser: keep state between invokes
- Curl_memchr: zero length input can't match
- examples/sftpuploadresume: typecast fseek argument to long
- examples/http2-upload: expand buffer to avoid silly warning
- ctype: restore character classification for non-ASCII platforms
- mime: avoid NULL pointer dereference risk
- cookies: ensure that we have cookies before writing jar
- os400.c: fix checksrc warnings
- configure: provide --with-wolfssl as an alias for --with-cyassl
- cyassl: adapt to libraries without TLS 1.0 support built-in
- http2: get rid of another strstr
- checksrc: force indentation of lines after an else
- cookies: remove unused macro
- CURLINFO_PROTOCOL.3: mention the existing defined names
- tests: provide 'manual' as a feature to optionally require
- travis: enable libssh2 on both macos and Linux
- CURLOPT_URL.3: added ENCODING section
- wolfssl: Fix non-blocking connect
- vtls: don't define MD5_DIGEST_LENGTH for wolfssl
- docs: remove extraneous commas in man pages
- URL: fix ASCII dependency in strcpy_url and strlen_url
- ssh-libssh.c: fix left shift compiler warning
- configure: only check for CA bundle for file-using SSL backends
- travis: add an mbedtls build
- http: don't set the "rewind" flag when not uploading anything
- configure: put CURLDEBUG and DEBUGBUILD in lib/curl_config.h
- transfer: don't unset writesockfd on setup of multiplexed conns
- vtls: use unified "supports" bitfield member in backends
- URLs: fix one more http url
- travis: add a build using WolfSSL
- openssl: change FILE ops to BIO ops
- travis: add build using NSS
- smb: reject negative file sizes
- cookies: accept parameter names as cookie name
- http2: getsock fix for uploads
- all over: fixed format specifiers
- http2: use the correct function pointer typedef

* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 7.59.0-0
- curl: add --proxy-pinnedpubkey
- added: CURLOPT_TIMEVALUE_LARGE and CURLINFO_FILETIME_T
- CURLOPT_RESOLVE: Add support for multiple IP addresses per entry
- Add option CURLOPT_HAPPY_EYEBALLS_TIMEOUT_MS
- Add new tool option --happy-eyeballs-timeout-ms
- Add CURLOPT_RESOLVER_START_FUNCTION and CURLOPT_RESOLVER_START_DATA
- openldap: check ldap_get_attribute_ber() results for NULL before using
- FTP: reject path components with control codes
- readwrite: make sure excess reads don't go beyond buffer end
- lib555: drop text conversion and encode data as ascii codes
- lib517: make variable static to avoid compiler warning
- lib544: sync ascii code data with textual data
- GSKit: restore pinnedpubkey functionality
- darwinssl: Don't import client certificates into Keychain on macOS
- parsedate: fix date parsing for systems with 32 bit long
- openssl: fix pinned public key build error in FIPS mode
- SChannel/WinSSL: Implement public key pinning
- cookies: remove verbose "cookie size:" output
- progress-bar: don't use stderr explicitly, use bar->out
- Fixes for MSDOS
- build: open VC15 projects with VS 2017
- curl_ctype: private is*() type macros and functions
- configure: set PATH_SEPARATOR to colon for PATH w/o separator
- winbuild: make linker generate proper PDB
- curl_easy_reset: clear digest auth state
- curl/curl.h: fix comment typo for CURLOPT_DNS_LOCAL_IP6
- range: commonize FTP and FILE range handling
- progress-bar docs: update to match implementation
- fnmatch: do not match the empty string with a character set
- fnmatch: accept an alphanum to be followed by a non-alphanum in char set
- build: fix termios issue on android cross-compile
- getdate: return -1 for out of range
- formdata: use the mime-content type function
- time-cond: fix reading the file modification time on Windows
- build-openssl.bat: Extend VC15 support to include Enterprise and Professional
- build-wolfssl.bat: Extend VC15 support to include Enterprise and Professional
- openssl: Don't add verify locations when verifypeer==0
- fnmatch: optimize processing of consecutive *s and ?s pattern characters
- schannel: fix compiler warnings
- content_encoding: Add "none" alias to "identity"
- get_posix_time: only check for overflows if they can happen
- http_chunks: don't write chunks twice with CURLOPT_HTTP_TRANSFER_DECODING
- README: language fix
- sha256: build with OpenSSL < 0.9.8
- smtp: fix processing of initial dot in data
- --tlsauthtype: works only if libcurl is built with TLS-SRP support
- tests: new tests for http raw mode
- libcurl-security.3: man page discussion security concerns when using libcurl
- curl_gssapi: make sure this file too uses our *printf()
- BINDINGS: fix curb link (and remove ruby-curl-multi)
- nss: use PK11_CreateManagedGenericObject() if available
- travis: add build with iconv enabled
- ssh: add two missing state names
- CURLOPT_HEADERFUNCTION.3: mention folded headers
- http: fix the max header length detection logic
- header callback: don't chop headers into smaller pieces
- CURLOPT_HEADER.3: clarify problems with different data sizes
- curl --version: show PSL if the run-time lib has it enabled
- examples/sftpuploadresume: resume upload via CURLOPT_APPEND
- Return error if called recursively from within callbacks
- sasl: prefer PLAIN mechanism over LOGIN
- winbuild: Use CALL to run batch scripts
- curl_share_setopt.3: connection cache is shared within multi handles
- winbuild: Use macros for the names of some build utilities
- projects/README: remove reference to dead IDN link/package
- lib655: silence compiler warning
- configure: Fix version check for OpenSSL 1.1.1
- docs/MANUAL: formfind.pl is not accessible on the site anymore
- unit1309: fix warning on Windows x64
- unit1307: proper cleanup on OOM to fix torture tests
- curl_ctype: fix macro redefinition warnings
- build: get CFLAGS (including -werror) used for examples and tests
- NO_PROXY: fix for IPv6 numericals in the URL
- krb5: use nondeprecated functions
- winbuild: prefer documented zlib library names
- http2: mark the connection for close on GOAWAY
- limit-rate: kick in even before "limit" data has been received
- HTTP: allow "header;" to replace an internal header with a blank one
- http2: verbose output new MAX_CONCURRENT_STREAMS values
- SECURITY: distros' max embargo time is 14 days
- curl tool: accept --compressed also if Brotli is enabled and zlib is not
- WolfSSL: adding TLSv1.3
- checksrc.pl: add -i and -m options
- CURLOPT_COOKIEFILE.3: "-" as file name means stdin

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 7.58.0-0
- new libssh-powered SSH SCP/SFTP back-end
- curl-config: add --ssl-backends
- http2: fix incorrect trailer buffer size
- http: prevent custom Authorization headers in redirects
- travis: add boringssl build
- examples/xmlstream.c: don't switch off CURL_GLOBAL_SSL
- SSL: Avoid magic allocation of SSL backend specific data
- lib: don't export all symbols, just everything curl_*
- libssh2: send the correct CURLE error code on scp file not found
- libssh2: return CURLE_UPLOAD_FAILED on failure to upload
- openssl: enable pkcs12 in boringssl builds
- libssh2: remove dead code from SSH_SFTP_QUOTE
- sasl_getmesssage: make sure we have a long enough string to pass
- conncache: fix several lock issues
- threaded-shared-conn.c: new example
- conncache: only allow multiplexing within same multi handle
- configure: check for netinet/in6.h
- URL: tolerate backslash after drive letter for FILE:
- openldap: add commented out debug possibilities
- include: get netinet/in.h before linux/tcp.h
- CONNECT: keep close connection flag in http_connect_state struct
- BINDINGS: another PostgreSQL client
- curl: limit -# update frequency for unknown total size
- configure: add AX_CODE_COVERAGE only if using gcc
- curl.h: remove incorrect comment about ERRORBUFFER
- openssl: improve data-pending check for https proxy
- curl: remove __EMX__ #ifdefs
- CURLOPT_PRIVATE.3: fix grammar
- sftp: allow quoted commands to use relative paths
- CURLOPT_DNS_CACHE_TIMEOUT.3: see also CURLOPT_RESOLVE
- RESOLVE: output verbose text when trying to set a duplicate name
- openssl: Disable file buffering for Win32 SSLKEYLOGFILE
- multi_done: prune DNS cache
- tests: update .gitignore for libtests
- tests: mark data files as non-executable in git
- CURLOPT_DNS_LOCAL_IP4.3: fixed the "SEE ALSO" to not self-reference
- curl.1: documented two missing valid exit codes
- curl.1: mention http:// and https:// as valid proxy prefixes
- vtls: replaced getenv() with curl_getenv()
- setopt: less *or equal* than INT_MAX/1000 should be fine
- examples/smtp-mail.c: use separate defines for options and mail
- curl: support >256 bytes warning messsages
- conncache: fix a return code
- krb5: fix a potential access of uninitialized memory
- rand: add a clang-analyzer work-around
- CURLOPT_READFUNCTION.3: refer to argument with correct name
- brotli: allow compiling with version 0.6.0
- content_encoding: rework zlib_inflate
- curl_easy_reset: release mime-related data
- examples/rtsp: fix error handling macros
- build-openssl.bat: Added support for VC15
- build-wolfssl.bat: Added support for VC15
- build: Added Visual Studio 2017 project files
- winbuild: Added support for VC15
- curl: Support size modifiers for --max-filesize
- examples/cacertinmem: ignore cert-already-exists error
- brotli: data at the end of content can be lost
- curl_version_info.3: call the argument 'age'
- openssl: fix memory leak of SSLKEYLOGFILE filename
- build: remove HAVE_LIMITS_H check
- --mail-rcpt: fix short-text description
- scripts: allow all perl scripts to be run directly
- progress: calculate transfer speed on milliseconds if possible
- system.h: check __LONG_MAX__ for defining curl_off_t
- easy: fix connection ownership in curl_easy_pause
- setopt: reintroduce non-static Curl_vsetopt() for OS400 support
- setopt: fix SSLVERSION to allow CURL_SSLVERSION_MAX_ values
- configure.ac: append extra linker flags instead of prepending them
- HTTP: bail out on negative Content-Length: values
- docs: comment about CURLE_READ_ERROR returned by curl_mime_filedata
- mime: clone mime tree upon easy handle duplication
- openssl: enable SSLKEYLOGFILE support by default
- smtp/pop3/imap_get_message: decrease the data length too...
- CURLOPT_TCP_NODELAY.3: fix typo
- SMB: fix numeric constant suffix and variable types
- ftp-wildcard: fix matching an empty string with "*[^a]"
- curl_fnmatch: only allow 5 '*' sections in a single pattern
- openssl: fix potential memory leak in SSLKEYLOGFILE logic
- SSH: Fix state machine for ssh-agent authentication
- examples/url2file.c: add missing curl_global_cleanup() call
- http2: don't close connection when single transfer is stopped
- libcurl-env.3: first version
- curl: progress bar refresh, get width using ioctl()
- CONNECT_TO: fail attempt to set an IPv6 numerical without IPv6 support

* Wed Nov 29 2017 Anton Novojilov <andy@essentialkaos.com> - 7.57.0-0
- auth: add support for RFC7616 - HTTP Digest access authentication
- share: add support for sharing the connection cache
- HTTP: implement Brotli content encoding
- CVE-2017-8816: NTLM buffer overflow via integer overflow
- CVE-2017-8817: FTP wildcard out of bounds read
- CVE-2017-8818: SSL out of buffer access
- curl_mime_filedata.3: fix typos
- libtest: Add required test libraries for lib1552 and lib1553
- fix time diffs for systems using unsigned time_t
- ftplistparser: memory leak fix: free temporary memory always
- multi: allow table handle sizes to be overridden
- wildcards: don't use with non-supported protocols
- curl_fnmatch: return error on illegal wildcard pattern
- transfer: Fix chunked-encoding upload too early exit
- curl_setup: Improve detection of CURL_WINDOWS_APP
- resolvers: only include anything if needed
- setopt: fix CURLOPT_SSH_AUTH_TYPES option read
- appveyor: add a win32 build
- Curl_timeleft: change return type to timediff_t
- cmake: Export libcurl and curl targets to use by other cmake projects
- curl: in -F option arg, comma is a delimiter for files only
- curl: improved ";type=" handling in -F option arguments
- timeval: use mach_absolute_time() on MacOS
- curlx: the timeval functions are no longer provided as curlx_*
- mkhelp.pl: do not generate comment with current date
- memdebug: use send/recv signature for curl_dosend/curl_dorecv
- cookie: avoid NULL dereference
- url: fix CURLOPT_POSTFIELDSIZE arg value check to allow -1
- include: remove conncache.h inclusion from where its not needed
- CURLOPT_MAXREDIRS: allow -1 as a value
- tests: Fixed torture tests on tests 556 and 650
- http2: Fixed OOM handling in upgrade request
- url: fix CURLOPT_DNS_CACHE_TIMEOUT arg value check to allow -1
- CURLOPT_INFILESIZE: accept -1
- curl: pass through [] in URLs instead of calling globbing error
- curl: speed up handling of many URLs
- ntlm: avoid malloc(0) for zero length passwords
- url: remove faulty arg value check from CURLOPT_SSH_AUTH_TYPES
- HTTP: support multiple Content-Encodings
- travis: add a job with brotli enabled
- url: remove unncessary NULL-check
- fnmatch: remove dead code
- connect: store IPv6 connection status after valid connection
- imap: deal with commands case insensitively
- --interface: add support for Linux VRF
- content_encoding: fix inflate_stream for no bytes available
- cmake: Correctly include curl.rc in Windows builds
- cmake: Add missing setmode check
- connect.c: remove executable bit on file
- SMB: fix uninitialized local variable
- zlib/brotli: only include header files in modules needing them
- URL: return error on malformed URLs with junk after IPv6 bracket
- openssl: fix too broad use of HAVE_OPAQUE_EVP_PKEY
- macOS: Fix missing connectx function with Xcode version older than 9.0
- --resolve: allow IP address within [] brackets
- examples/curlx: Fix code style
- ntlm: remove unnecessary NULL-check to please scan-build
- Curl_llist_remove: fix potential NULL pointer deref
- mime: fix "Value stored to 'sz' is never read" scan-build error
- openssl: fix "Value stored to 'rc' is never read" scan-build error
- http2: fix "Value stored to 'hdbuf' is never read" scan-build error
- http2: fix "Value stored to 'end' is never read" scan-build error
- Curl_open: fix OOM return error correctly
- url: reject ASCII control characters and space in host names
- examples/rtsp: clear RANGE again after use
- connect: improve the bind error message
- make: fix "make distclean"
- connect: add support for new TCP Fast Open API on Linux
- metalink: fix memory-leak and NULL pointer dereference
- URL: update "file:" URL handling
- ssh: remove check for a NULL pointer
- global_init: ignore CURL_GLOBAL_SSL's absense

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.1-0
- imap: if a FETCH response has no size, don't call write callback
- ftp: UBsan fixup 'pointer index expression overflowed
- failf: skip the sprintf() if there are no consumers
- fuzzer: move to using external curl-fuzzer
- lib/Makefile.m32: allow customizing dll suffixes
- docs: fix typo in curl_mime_data_cb man page
- darwinssl: add support for TLSv1.3
- build: fix --disable-crypto-auth
- lib/config-win32.h: let SMB/SMBS be enabled with OpenSSL/NSS
- openssl: fix build without HAVE_OPAQUE_EVP_PKEY
- strtoofft: Remove extraneous null check
- multi_cleanup: call DONE on handles that never got that
- tests: added flaky keyword to tests 587 and 644
- pingpong: return error when trying to send without connection
- remove_handle: call multi_done() first, then clear dns cache pointer
- mime: be tolerant about setting the same header list twice in a part
- mime: improve unbinding top multipart from easy handle
- mime: avoid resetting a part's encoder when part's contents change
- mime: refuse to add subparts to one of their own descendants
- RTSP: avoid integer overflow on funny RTSP responses
- curl: don't pass semicolons when parsing Content-Disposition
- openssl: enable PKCS12 support for !BoringSSL
- FAQ: s/CURLOPT_PROGRESSFUNCTION/CURLOPT_XFERINFOFUNCTION
- CURLOPT_NOPROGRESS.3: also refer to xferinfofunction
- CURLOPT_XFERINFODATA.3: fix duplicate see also
- test298: verify --ftp-method nowcwd with URL encoded path
- FTP: URL decode path for dir listing in nocwd mode
- smtp_done: fix memory leak on send failure
- ftpserver: support case insensitive commands
- test950; verify SMTP with custom request
- openssl: don't use old BORINGSSL_YYYYMM macros
- setopt: update current connection SSL verify params
- winbuild/BUILD.WINDOWS.txt: mention WITH_NGHTTP2
- curl: reimplement stdin buffering in -F option
- mime: keep "text/plain" content type if user-specified
- mime: fix the content reader to handle >16K data properly
- configure: remove the C++ compiler check
- memdebug: trace send, recv and socket
- runtests: use valgrind for torture as well
- ldap: silence clang warning
- makefile.m32: allow to override gcc, ar and ranlib
- setopt: avoid integer overflows when setting millsecond values
- setopt: range check most long options
- ftp: reject illegal IP/port in PASV 227 response
- mime: do not reuse previously computed multipart size
- vtls: change struct Curl_ssl `close' field name to `close_one'
- os400: add missing symbols in config file
- mime: limit bas64-encoded lines length to 76 characters
- mk-ca-bundle: Remove URL for aurora
- mk-ca-bundle: Fix URL for NSS

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.0-0
- curl: enable compression for SCP/SFTP with --compressed-ssh
- libcurl: enable compression for SCP/SFTP with CURLOPT_SSH_COMPRESSION
- vtls: added dynamic changing SSL backend with curl_global_sslset()
- new MIME API, curl_mime_init() and friends
- openssl: initial SSLKEYLOGFILE implementation
- FTP: zero terminate the entry path even on bad input
- examples/ftpuploadresume.c: use portable code
- runtests: match keywords case insensitively
- travis: build the examples too
- strtoofft: reduce integer overflow risks globally
- zsh.pl: produce a working completion script again
- cmake: remove dead code for CURL_DISABLE_RTMP
- progress: Track total times following redirects
- configure: fix --disable-threaded-resolver
- cmake: remove dead code for DISABLED_THREADSAFE
- configure: fix clang version detection
- darwinssi: fix error: variable length array used
- travis: add metalink to some osx builds
- configure: check for __builtin_available() availability
- http_proxy: fix build error for CURL_DOES_CONVERSIONS
- examples/ftpuploadresume: checksrc compliance
- ftp: fix CWD when doing multicwd then nocwd on same connection
- system.h: remove all CURL_SIZEOF_* defines
- http: Don't wait on CONNECT when there is no proxy
- system.h: check for __ppc__ as well
- http2_recv: return error better on fatal h2 errors
- scripts/contri*sh: use "git log --use-mailmap"
- tftp: fix memory leak on too long filename
- system.h: fix build for hppa
- cmake: enable picky compiler options with clang and gcc
- makefile.m32: add support for libidn2
- curl: turn off MinGW CRT's globbing
- request-target.d: mention added in 7.55.0
- curl: shorten and clean up CA cert verification error message
- imap: support PREAUTH
- CURLOPT_USERPWD.3: see also CURLOPT_PROXYUSERPWD
- examples/threaded-ssl: mention that this is for openssl before 1.1
- winbuild: fix embedded manifest option
- tests: Make sure libtests & unittests call curl_global_cleanup()
- system.h: include sys/poll.h for AIX
- darwinssl: handle long strings in TLS certs
- strtooff: fix build for systems with long long but no strtoll
- asyn-thread: Improved cleanup after OOM situations
- HELP-US.md: "How to get started helping out in the curl project"
- curl.h: CURLSSLBACKEND_WOLFSSL used wrong value
- unit1301: fix error message on first test
- ossfuzz: moving towards the ideal integration
- http: fix a memory leakage in checkrtspprefix()
- examples/post-callback: stop returning one byte at a time
- schannel: return CURLE_SSL_CACERT on failed verification
- MAIL-ETIQUETTE: added "1.9 Your emails are public"
- http-proxy: treat all 2xx as CONNECT success
- openssl: use OpenSSL's default ciphers by default
- runtests.pl: support attribute "nonewline" in part verify/upload
- configure: remove --enable-soname-bump and SONAME_BUMP
- travis: add c-ares enabled builds linux + osx
- vtls: fix WolfSSL 3.12 build problems
- http-proxy: when not doing CONNECT, that phase is done immediately
- configure: fix curl_off_t check's include order
- configure: use -Wno-varargs on clang 3.9[.X] debug builds
- rtsp: do not call fwrite() with NULL pointer FILE *
- mbedtls: enable CA path processing
- travis: add build without HTTP/SMTP/IMAP
- checksrc: verify more code style rules
- HTTP proxy: on connection re-use, still use the new remote port
- tests: add initial gssapi test using stub implementation
- rtsp: Segfault when using WRITEDATA
- docs: clarify the CURLOPT_INTERLEAVE* options behavior
- non-ascii: use iconv() with 'char **' argument
- server/getpart: provide dummy function to build conversion enabled
- conversions: fix several compiler warnings
- openssl: add missing includes
- schannel: Support partial send for when data is too large
- socks: fix incorrect port number in SOCKS4 error message
- curl: fix integer overflow in timeout options
- travis: on mac, don't install openssl or libidn
- cookies: reject oversized cookies instead of truncating
- cookies: use lock when using CURLINFO_COOKIELIST
- curl: check fseek() return code and bail on error
- examples/post-callback: use long for CURLOPT_POSTFIELDSIZE
- openssl: only verify RSA private key if supported
- tests: make the imap server not verify user+password
- imap: quote atoms properly when escaping characters
- tests: fix a compiler warning in test 643
- file_range: avoid integer overflow when figuring out byte range
- curl.h: include on cygwin too
- reuse_conn: don't copy flags that are known to be equal
- http: fix adding custom empty headers to repeated requests
- docs: clarify the use of environment variables for proxy
- docs: link CURLOPT_CONNECTTIMEOUT and CURLOPT_CONNECTTIMEOUT_MS
- connect: fix race condition with happy eyeballs timeout
- cookie: fix memory leak if path was set twice in header
- vtls: compare and clone ssl configs properly
- proxy: read the "no_proxy" variable only if necessary

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.1-0
- build: fix 'make install' with configure, install docs/libcurl/* too
- make install: add 8 missing man pages to the installation
- curl: do bounds check using a double comparison
- dist: Add dictserver.py/negtelnetserver.py to release
- digest_sspi: Don't reuse context if the user/passwd has changed
- gitignore: ignore top-level .vs folder
- build: check out *.sln files with Windows line endings
- travis: verify "make install"
- dist: fix the cmake build by shipping cmake_uninstall.cmake.in too
- metalink: fix error: ‘*’ in boolean context, suggest ‘&&’ instead
- configure: use the threaded resolver backend by default if possible
- mkhelp.pl: allow executing this script directly
- maketgz: remove old *.dist files before making the tarball
- openssl: remove CONST_ASN1_BIT_STRING
- openssl: fix "error: this statement may fall through"
- proxy: fix memory leak in case of invalid proxy server name
- curl/system.h: support more architectures (OpenRISC, ARC)
- docs: fix typos
- curl/system.h: add Oracle Solaris Studio
- CURLINFO_TOTAL_TIME: could wrongly return 4200 seconds
- docs: --connect-to clarified
- cmake: allow user to override CMAKE_DEBUG_POSTFIX
- travis: test cmake build on tarball too
- redirect: make it handle absolute redirects to IDN names
- curl/system.h: fix for gcc on PowerPC
- curl --interface: fixed for IPV6 unique local addresses
- cmake: threads detection improvements

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.0-0
- curl: allow --header and --proxy-header read from file
- getinfo: provide sizes as curl_off_t
- curl: prevent binary output spewed to terminal
- curl: added --request-target
- libcurl: added CURLOPT_REQUEST_TARGET
- curl: added --socks5-{basic,gssapi}: control socks5 auth
- libcurl: added CURLOPT_SOCKS5_AUTH
- glob: do not parse after a strtoul() overflow range (CVE-2017-1000101)
- tftp: reject file name lengths that don't fit (CVE-2017-1000100)
- file: output the correct buffer to the user (CVE-2017-1000099)
- includes: remove curl/curlbuild.h and curl/curlrules.h
- dist: make the hugehelp.c not get regenerated unnecessarily
- timers: store internal time stamps as time_t instead of doubles
- progress: let "current speed" be UL + DL speeds combined
- http-proxy: do the HTTP CONNECT process entirely non-blocking
- lib/curl_setup.h: remove CURL_WANTS_CA_BUNDLE_ENV
- fuzz: bring oss-fuzz initial code converted to C89
- configure: disable nghttp2 too if HTTP has been disabled
- mk-ca-bundle.pl: Check curl's exit code after certdata download
- test1148: verify the -# progressbar
- tests: stabilize test 2032 and 2033
- HTTPS-Proxy: don't offer h2 for https proxy connections
- http-proxy: only attempt FTP over HTTP proxy
- curl-compilers.m4: enable vla warning for clang
- curl-compilers.m4: enable double-promotion warning
- curl-compilers.m4: enable missing-variable-declarations clang warning
- curl-compilers.m4: enable comma clang warning
- Makefile.m32: enable -W for MinGW32 build
- CURLOPT_PREQUOTE: not supported for SFTP
- http2: fix OOM crash
- PIPELINING_SERVER_BL: cleanup the internal list use
- mkhelp.pl: fix script name in usage text
- lib1521: add curl_easy_getinfo calls to the test set
- travis: do the distcheck test build out-of-tree as well
- if2ip: fix compiler warning in ISO C90 mode
- lib: fix the djgpp build
- typecheck-gcc: add support for CURLINFO_OFF_T
- travis: enable typecheck-gcc warnings
- maketgz: switch to xz instead of lzma
- CURLINFO_REDIRECT_URL.3: mention the CURLOPT_MAXREDIRS case
- curl-compilers.m4: fix unknown-warning-option on Apple clang
- winbuild: fix boringssl build
- curl/system.h: add check for XTENSA for 32bit gcc
- test1537: fixed memory leak on OOM
- test1521: fix compiler warnings
- curl: fix memory leak on test 1147 OOM
- libtest/make: generate lib1521.c dynamically at build-time
- curl_strequal.3: fix typo in SYNOPSIS
- progress: prevent resetting t_starttransfer
- openssl: improve fallback seed of PRNG with a time based hash
- http2: improved PING frame handling
- test1450: add simple testing for DICT
- make: build the docs subdir only from within src
- cmake: Added compatibility options for older Windows versions
- gtls: fix build when sizeof(long) < sizeof(void *)
- url: make the original string get used on subsequent transfers
- timeval.c: Use long long constant type for timeval assignment
- tool_sleep: typecast to avoid macos compiler warning
- travis.yml: use --enable-werror on debug builds
- test1451: add SMB support to the testbed
- configure: remove checks for 5 functions never used
- configure: try ldap/lber in reversed order first
- smb: fix build for djgpp/MSDOS
- travis: install nghttp2 on linux builds
- smb: add support for CURLOPT_FILETIME
- cmake: fix send/recv argument scanner for windows
- inet_pton: fix include on windows to get prototype
- select.h: avoid macro redefinition harder
- cmake: if inet_pton is used, bump _WIN32_WINNT
- asyn-thread.c: fix unused variable warnings on macOS
- runtests: support "threaded-resolver" as a feature
- test506: skip if threaded-resolver
- cmake: remove spurious "-l" from linker flags
- cmake: add CURL_WERROR for enabling "warning as errors"
- memdebug: don't setbuf() if the file open failed
- curl_easy_escape.3: mention the (lack of) encoding
- test1452: add telnet negotiation
- CURLOPT_POSTFIELDS.3: explain the 100-continue magic better
- cmake: offer CMAKE_DEBUG_POSTFIX when building with MSVC
- tests/valgrind.supp: supress OpenSSL false positive seen on travis
- curl_setup_once: Remove ERRNO/SET_ERRNO macros
- curl-compilers.m4: disable warning spam with Cygwin's clang
- ldap: fix MinGW compiler warning
- make: fix docs build on OpenBSD
- curl_setup: always define WIN32_LEAN_AND_MEAN on Windows
- system.h: include winsock2.h before windows.h
- winbuild: build with warning level 4
- rtspd: fix MSVC level 4 warning
- sockfilt: suppress conversion warning with explicit cast
- libtest: fix MSVC warning C4706
- darwinssl: fix pinnedpubkey build error
- tests/server/resolve.c: fix deprecation warning
- nss: fix a possible use-after-free in SelectClientCert()
- checksrc: escape open brace in regex
- multi: mention integer overflow risk if using > 500 million sockets
- darwinssl: fix --tlsv1.2 regression
- timeval: struct curltime is a struct timeval replacement
- curl_rtmp: fix a compiler warning
- include.d: clarify that it concerns the response headers
- cmake: support make uninstall
- include.d: clarify --include is only for response headers
- libcurl: Stop using error codes defined under CURL_NO_OLDIES
- http: fix response code parser to avoid integer overflow
- configure: fix the check for IdnToUnicode
- multi: fix request timer management
- curl_threads: fix MSVC compiler warning
- travis: build on osx with openssl
- travis: build on osx with libressl
- CURLOPT_NETRC.3: mention the file name on windows
- cmake: set MSVC warning level to 4
- netrc: skip lines starting with '#'
- darwinssl: fix curlssl_sha256sum() compiler warnings on first argument
- BUILD.WINDOWS: mention buildconf.bat for builds off git
- darwinssl: silence compiler warnings
- travis: build on osx with darwinssl
- FTP: skip unnecessary CWD when in nocwd mode
- gssapi: fix memory leak of output token in multi round context
- getparameter: avoid returning uninitialized 'usedarg'
- curl (debug build) easy_events: make event data static
- curl: detect and bail out early on parameter integer overflows
- configure: fix recv/send/select detection on Android

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.1-0
- curl: show the libcurl release date in --version output
- CVE-2017-9502: default protocol drive letter buffer overflow
- openssl: fix memory leak in servercert
- tests: remove the html and PDF versions from the tarball
- mbedtls: enable NTLM (& SMB) even if MD4 support is unavailable
- typecheck-gcc: handle function pointers properly
- llist: no longer uses malloc
- gnutls: removed some code when --disable-verbose is configured
- lib: fix maybe-uninitialized warnings
- multi: clarify condition in curl_multi_wait
- schannel: Don't treat encrypted partial record as pending data
- configure: fix the -ldl check for openssl, add -lpthread check
- configure: accept -Og and -Ofast GCC flags
- Makefile: avoid use of GNU-specific form of $<
- if2ip: fix -Wcast-align warning
- configure: stop prepending to LDFLAGS, CPPFLAGS
- curl: set a 100K buffer size by default
- typecheck-gcc: fix _curl_is_slist_info
- nss: do not leak PKCS #11 slot while loading a key
- nss: load libnssckbi.so if no other trust is specified
- examples: ftpuploadfrommem.c
- url: declare get_protocol_family() static
- examples/cookie_interface.c: changed to example.com
- test1443: test --remote-time
- curl: use utimes instead of obsolescent utime when available
- url: fixed a memory leak on OOM while setting CURLOPT_BUFFERSIZE
- curl_rtmp: fix missing-variable-declarations warnings
- tests: fixed OOM handling of unit tests to abort test
- curl_setup: Ensure no more than one IDN lib is enabled
- tool: Fix missing prototype warnings for CURL_DOES_CONVERSIONS
- CURLOPT_BUFFERSIZE: 1024 bytes is now the minimum size
- curl: non-boolean command line args reject --no- prefixes
- telnet: Write full buffer instead of byte-by-byte
- typecheck-gcc: add missing string options
- typecheck-gcc: add support for CURLINFO_SOCKET
- opt man pages: they all have examples now
- curl_setup_once: use SEND_QUAL_ARG2 for swrite
- test557: set a known good numeric locale
- schannel: return a more specific error code for SEC_E_UNTRUSTED_ROOT
- tests/server: make string literals const
- runtests: use -R for random order
- unit1305: fix compiler warning
- curl_slist_append.3: clarify a NULL input creates a new list
- tests/server: run checksrc by default in debug-builds
- tests: fix -Wcast-qual warnings
- runtests.pl: simplify the datacheck read section
- curl: remove --environment and tool_writeenv.c
- buildconf: fix hang on IRIX
- tftp: silence bad-function-cast warning
- asyn-thread: fix unused macro warnings
- tool_parsecfg: fix -Wcast-qual warning
- sendrecv: fix MinGW-w64 warning
- test537: use correct variable type
- rand: treat fake entropy the same regardless of endianness
- curl: generate the --help output
- tests: removed redundant --trace-ascii arguments
- multi: assign IDs to all timers and make each timer singleton
- multi: use a fixed array of timers instead of malloc
- mbedtls: Support server renegotiation request
- pipeline: fix mistakenly trying to pipeline POSTs
- lib510: don't write past the end of the buffer if it's too small
- CURLOPT_HTTPPROXYTUNNEL.3: clarify, add example
- SecureTransport/DarwinSSL: Implement public key pinning
- curl.1: clarify --config
- curl_sasl: fix build error with CURL_DISABLE_CRYPTO_AUTH + USE_NTLM
- darwinssl: Fix exception when processing a client-side certificate
- curl.1: mention --oauth2-bearer's argument
- mkhelp.pl: do not add current time into curl binary
- asiohiper.cpp / evhiperfifo.c: deal with negative timerfunction input
- ssh: fix memory leak in disconnect due to timeout
- tests: stabilize test 1034
- cmake: auto detection of CURL_CA_BUNDLE/CURL_CA_PATH
- assert: avoid, use DEBUGASSERT instead
- LDAP: using ldap_bind_s on Windows with methods
- redirect: store the "would redirect to" URL when max redirs is reached
- winbuild: fix the nghttp2 build
- examples: fix -Wimplicit-fallthrough warnings
- time: fix type conversions and compiler warnings
- mbedtls: fix variable shadow warning
- test557: fix ubsan runtime error due to int left shift
- transfer: init the infilesize from the postfields
- docs: clarify NO_PROXY further
- build-wolfssl: Sync config with wolfSSL 3.11
- curl-compilers.m4: enable -Wshift-sign-overflow for clang
- example/externalsocket.c: make it use CLOSESOCKETFUNCTION too
- lib574.c: use correct callback proto
- lib583: fix compiler warning
- curl-compilers.m4: fix compiler_num for clang
- typecheck-gcc.h: separate getinfo slist checks from other pointers
- typecheck-gcc.h: check CURLINFO_TLS_SSL_PTR and CURLINFO_TLS_SESSION
- typecheck-gcc.h: check CURLINFO_CERTINFO
- build: provide easy code coverage measuring
- test1537: dedicated tests of the URL (un)escape API calls
- curl_endian: remove unused functions
- test1538: verify the libcurl strerror API calls
- MD(4|5): silence cast-align clang warning
- dedotdot: fixed output for ".." and "." only input
- cyassl: define build macros before including ssl.h
- updatemanpages.pl: error out on too old git version
- curl_sasl: fix unused-variable warning
- x509asn1: fix implicit-fallthrough warning with GCC 7
- libtest: fix implicit-fallthrough warnings with GCC 7
- BINDINGS: add Ring binding
- curl_ntlm_core: pass unsigned char to toupper
- test1262: verify ftp download with -z for "if older than this"
- test1521: test all curl_easy_setopt options
- typecheck-gcc: allow CURLOPT_STDERR to be NULL too
- metalink: remove unused printf() argument
- file: make speedcheck use current time for checks
- configure: fix link with librtmp when specifying path
- examples/multi-uv.c: fix deprecated symbol
- cmake: Fix inconsistency regarding mbed TLS include directory
- setopt: check CURLOPT_ADDRESS_SCOPE option range
- gitignore: ignore all vim swap files
- urlglob: fix division by zero
- libressl: OCSP and intermediate certs workaround no longer needed

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.0-0
- Add CURL_SSLVERSION_MAX_* constants to CURLOPT_SSLVERSION
- Add --max-tls
- Add CURLOPT_SUPPRESS_CONNECT_HEADERS
- Add --suppress-connect-headers
- CVE-2017-7468: switch off SSL session id when client cert is used
- cmake: Replace invalid UTF-8 byte sequence
- tests: use consistent environment variables for setting charset
- proxy: fixed a memory leak on OOM
- ftp: removed an erroneous free in an OOM path
- docs: de-duplicate file lists in the Makefiles
- ftp: fixed a NULL pointer dereference on OOM
- gopher: fixed detection of an error condition from Curl_urldecode
- url: fix unix-socket support for proxy-disabled builds
- test1139: allow for the possibility that the man page is not rebuilt
- cyassl: get library version string at runtime
- digest_sspi: fix compilation warning
- tests: enable HTTP/2 tests to run with non-default port numbers
- warnless: suppress compiler warning
- darwinssl: Warn that disabling host verify also disables SNI
- configure: fix for --enable-pthreads
- checksrc.bat: Ignore curl_config.h.in, curl_config.h
- no-keepalive.d: fix typo
- configure: fix --with-zlib when a path is specified
- build: fix gcc7 implicit fallthrough warnings
- fix potential use of uninitialized variables
- CURLOPT_SSL_CTX_FUNCTION.3: Fix EXAMPLE formatting errors
- CMake: Reorganize SSL support, separate WinSSL and SSPI
- CMake: Add DarwinSSL support
- CMake: Add mbedTLS support
- ares: return error at once if timed out before name resolve starts
- BINDINGS: added C++, perl, go and Scilab bindings
- URL: return error on malformed URLs with junk after port number
- KNOWN_BUGS: Add DarwinSSL won't import PKCS#12 without a password
- http2: Fix assertion error on redirect with CL=0
- updatemanpages.pl: Update man pages to use current date and versions
- --insecure: clarify that this option is for server connections
- mkhelp: simplified the gzip code
- build: fixed making man page in out-of-tree tarball builds
- tests: disabled 1903 due to flakiness
- openssl: add two /* FALLTHROUGH */ to satisfy coverity
- cmdline-opts: fixed a few typos
- authneg: clear auth.multi flag at http_done
- curl_easy_reset: Also reset the authentication state
- proxy: skip SSL initialization for closed connections
- http_proxy: ignore TE and CL in CONNECT 2xx responses
- tool_writeout: fixed a buffer read overrun on --write-out
- make: regenerate docs/curl.1 by running make in docs
- winbuild: add basic support for OpenSSL 1.1.x
- build: removed redundant DEPENDENCIES from makefiles
- CURLINFO_LOCAL_PORT.3: added example
- curl: show HTTPS-Proxy options on CURLE_SSL_CACERT
- tests: strip more options from non-HTTP --libcurl tests
- tests: fixed the documented test server port numbers
- runtests.pl: fixed display of the Gopher IPv6 port number
- multi: fix streamclose() crash in debug mode
- cmake: build manual pages
- cmake: add support for building HTML and PDF docs
- mbedtls: add support for CURLOPT_SSL_CTX_FUNCTION
- make: introduce 'test-nonflaky' target
- CURLINFO_PRIMARY_IP.3: add example
- tests/README: mention nroff for --manual tests
- mkhelp: disable compression if the perl gzip module is unavailable
- openssl: fall back on SSL_ERROR_* string when no error detail
- asiohiper: make sure socket is open in event_cb
- tests/README: make "Run" section foolproof
- curl: check for end of input in writeout backslash handling
- .gitattributes: turn off CRLF for *.am
- multi: fix MinGW-w64 compiler warnings
- schannel: fix variable shadowing warning
- openssl: exclude DSA code when OPENSSL_NO_DSA is defined
- http: Fix proxy connection reuse with basic-auth
- pause: handle mixed types of data when paused
- http: do not treat FTPS over CONNECT as HTTPS
- conncache: make hashkey avoid malloc
- make: use the variable MAKE for recursive calls
- curl: fix callback argument inconsistency
- NTLM: check for features with #ifdef instead of #if
- cmake: add several missing files to the dist
- select: use correct SIZEOF_ constant
- connect: fix unreferenced parameter warning
- schannel: fix unused variable warning
- gcc7: fix ‘*’ in boolean context
- http2: silence unused parameter warnings
- ssh: fix narrowing conversion warning
- telnet: (win32) fix read callback return variable
- docs: Explain --fail-early does not imply --fail
- docs: added examples for CURLINFO_FILETIME.3 and CURLOPT_FILETIME.3
- tests/server/util: remove in6addr_any for recent MinGW
- multi: make curl_multi_wait avoid malloc in the typical case
- include: curl/system.h is a run-time version of curlbuild.h
- easy: silence compiler warning
- llist: replace Curl_llist_alloc with Curl_llist_init
- hash: move key into hash struct to reduce mallocs
- url: don't free postponed data on connection reuse
- curl_sasl: declare mechtable static
- curl: fix Windows Unicode build
- multi: fix queueing of pending easy handles
- tool_operate: fix MinGW compiler warning
- low_speed_limit: improved function for longer time periods
- gtls: fix compiler warning
- sspi: print out InitializeSecurityContext() error message
- schannel: fix compiler warnings
- vtls: fix unreferenced variable warnings
- INSTALL.md: fix secure transport configure arguments
- CURLINFO_SCHEME.3: fix variable type
- libcurl-thread.3: also mention threaded-resolver
- nss: load CA certificates even with --insecure
- openssl: fix this statement may fall through
- poll: prefer over
- polarssl: unbreak build with versions < 1.3.8
- Curl_expire_latest: ignore already expired timers
- configure: turn implicit function declarations into errors
- mbedtls: fix memory leak in error path
- http2: fix handle leak in error path
- .gitattributes: force shell scripts to LF
- configure.ac: ignore CR after version numbers
- extern-scan.pl: strip trailing CR
- openssl: make SSL_ERROR_to_str more future-proof
- openssl: fix thread-safety bugs in error-handling
- openssl: don't try to print nonexistant peer private keys
- nss: fix MinGW compiler warnings

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.1-0
- cyassl: fix typo
- url: Improve CURLOPT_PROXY_CAPATH error handling
- urldata: include curl_sspi.h when Windows SSPI is enabled
- formdata: check for EOF when reading from stdin
- tests: Set CHARSET & LANG to UTF-8 in 1035, 2046 and 2047
- url: Default the proxy CA bundle location to CURL_CA_BUNDLE
- rand: added missing #ifdef HAVE_FCNTL_H around fcntl.h header

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.0-0
- unix_socket: added --abstract-unix-socket and CURLOPT_ABSTRACT_UNIX_SOCKET
- CURLOPT_BUFFERSIZE: support enlarging receive buffer
- CVE-2017-2629: make SSL_VERIFYSTATUS work again
- gnutls-random: check return code for failed random
- openssl-random: check return code when asking for random
- http: remove "Curl_http_done: called premature" message
- cyassl: use time_t instead of long for timeout
- build-wolfssl: Sync config with wolfSSL 3.10
- ftp-gss: check for init before use
- configure: accept --with-libidn2 instead
- ftp: failure to resolve proxy should return that error code
- curl.1: add three more exit codes
- docs/ciphers: link to our own new page about ciphers
- vtls: s/SSLEAY/OPENSSL - fixes multi_socket timeouts with openssl
- darwinssl: fix iOS build
- darwinssl: fix CFArrayRef leak
- cmake: use crypt32.lib when building with OpenSSL on windows
- curl_formadd.3: CURLFORM_CONTENTSLENGTH not needed when chunked
- digest_sspi: copy terminating NUL as well
- curl: fix --remote-time incorrect times on Windows
- curl.1: several updates and corrections
- content_encoding: change return code on a failure
- curl.h: CURLE_FUNCTION_NOT_FOUND is no longer in use
- docs: TCP_KEEPALIVE start and interval default to 60
- darwinssl: --insecure overrides --cacert if both settings are in use
- TheArtOfHttpScripting: grammar
- CIPHERS.md: document GSKit ciphers
- wolfssl: support setting cipher list
- wolfssl: display negotiated SSL version and cipher
- lib506: fix build for Open Watcom
- asiohiper: improved socket handling
- examples: make the C++ examples follow our code style too
- tests/sws: retry send() on EWOULDBLOCK
- cmake: Fix passing _WINSOCKAPI_ macro to compiler
- smtp: Fix STARTTLS denied error message
- imap/pop3: don't print response character in STARTTLS denied messages
- rand: make it work without TLS backing
- url: fix parsing for when 'file' is the default protocol
- url: allow file://X:/path URLs on windows again
- gnutls: check for alpn and ocsp in configure
- IDN: Use TR46 'non-transitional' for toASCII translations
- url: Fix NO_PROXY env var to work properly with --proxy option
- CURLOPT_PREQUOTE.3: takes a struct curl_slist*, not a char*
- docs: Add note about libcurl copying strings to CURLOPT_* manpages
- curl: reset the easy handle at --next
- --next docs: --trace and --trace-ascii are also global
- --write-out docs: 'time_total' is not always shown with ms precision
- http: print correct HTTP string in verbose output when using HTTP/2
- docs: improved language in README.md HISTORY.md CONTRIBUTE.md
- http2: disable server push if not requested
- nss: use the correct lock in nss_find_slot_by_name()
- usercertinmem.c: improve the short description
- CURLOPT_CONNECT_TO: Fix compile warnings
- docs: non-blocking SSL handshake is now supported with NSS
- *.rc: escape non-ASCII/non-UTF-8 character for clarity
- mbedTLS: fix multi interface non-blocking handshake
- PolarSSL: fix multi interface non-blocking handshake
- VC: remove the makefile.vc6 build infra
- telnet: fix windows compiler warnings
- cookies: do not assume a valid domain has a dot
- polarssl: fix hangs
- gnutls: disable TLS session tickets
- mbedtls: disable TLS session tickets
- mbedtls: implement CTR-DRBG and HAVEGE random generators
- openssl: Don't use certificate after transferring ownership
- cmake: Support curl --xattr when built with cmake
- OS400: Fix symbols
- docs: Add more HTTPS proxy documentation
- docs: use more HTTPS links
- cmdline-opts: Fixed build and test in out of source tree builds
- CHANGES.0: removed
- schannel: Remove incorrect SNI disabled message
- darwinssl: Avoid parsing certificates when not in verbose mode
- test552: Fix typos
- telnet: Fix typos
- transfer: only retry nobody-requests for HTTP
- http2: reset push header counter fixes crash
- nss: make FTPS work with --proxytunnel
- test1139: Added the --manual keyword since the manual is required
- polarssl, mbedtls: Fix detection of pending data
- http_proxy: Fix tiny memory leak upon edge case connecting to proxy
- URL: only accept ";options" in SMTP/POP3/IMAP URL schemes
- curl.1: ftp.sunet.se is no longer an FTP mirror
- tool_operate: Show HTTPS-Proxy options on CURLE_SSL_CACERT
- http2: fix memory-leak when denying push streams
- configure: Allow disabling pthreads, fall back on Win32 threads
- curl: fix typo in time condition warning message
- axtls: adapt to API changes
- tool_urlglob: Allow a glob range with the same start and stop
- winbuild: add note on auto-detection of MACHINE in Makefile.vc
- http: fix missing 'Content-Length: 0' while negotiating auth
- proxy: fix hostname resolution and IDN conversion
- docs: fix timeout handling in multi-uv example
- digest_sspi: Fix nonce-count generation in HTTP digest
- sftp: improved checks for create dir failures
- smb: use getpid replacement for windows UWP builds
- digest_sspi: Handle 'stale=TRUE' directive in HTTP digest

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.1-0
- CVE-2016-9594: unititialized random
- lib557: fix checksrc warnings
- lib: fix MSVC compiler warnings
- lib557.c: use a shorter MAXIMIZE representation
- tests: run checksrc on debug builds

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.0-0
- nss: map CURL_SSLVERSION_DEFAULT to NSS default
- vtls: support TLS 1.3 via CURL_SSLVERSION_TLSv1_3
- curl: introduce the --tlsv1.3 option to force TLS 1.3
- curl: Add --retry-connrefused
- proxy: Support HTTPS proxy and SOCKS+HTTP(s)
- add CURLINFO_SCHEME, CURLINFO_PROTOCOL, and {scheme}
- curl: add --fail-early
- CVE-2016-9586: printf floating point buffer overflow
- CVE-2016-9952: Win CE schannel cert wildcard matches too much
- CVE-2016-9953: Win CE schannel cert name out of buffer read
- msvc: removed a straggling reference to strequal.c
- winbuild: remove strcase.obj from curl build
- examples: bugfixed multi-uv.c
- configure: verify that compiler groks -Werror=partial-availability
- mbedtls: fix build with mbedtls versions < 2.4.0
- dist: add unit test CMakeLists.txt to the tarball
- curl -w: added more decimal digits to timing counters
- easy: Initialize info variables on easy init and duphandle
- cmake: disable poll for macOS
- http2: Don't send header fields prohibited by HTTP/2 spec
- ssh: check md5 fingerprints case insensitively (regression)
- openssl: initial TLS 1.3 adaptions
- curl_formadd.3: *_FILECONTENT and *_FILE need the file to be kept
- printf: fix ".*f" handling
- examples/fileupload.c: fclose the file as well
- SPNEGO: Fix memory leak when authentication fails
- realloc: use Curl_saferealloc to avoid common mistakes
- openssl: make sure to fail in the unlikely event that PRNG seeding fails
- URL-parser: for file://[host]/ URLs, the [host] must be localhost
- timeval: prefer time_t to hold seconds instead of long
- Curl_rand: fixed and moved to rand.c
- glob: fix [a-c] globbing regression
- darwinssl: fix SSL client certificate not found on MacOS Sierra
- curl.1: Clarify --dump-header only writes received headers
- http2: Fix address sanitizer memcpy warning
- http2: Use huge HTTP/2 windows
- connects: Don't mix unix domain sockets with regular ones
- url: Fix conn reuse for local ports and interfaces
- x509: Limit ASN.1 structure sizes to 256K
- checksrc: add more checks
- winbuild: add config option ENABLE_NGHTTP2
- http2: check nghttp2_session_set_local_window_size exists
- http2: Fix crashes when parent stream gets aborted
- CURLOPT_CONNECT_TO: Skip non-matching "connect-to" entries
- URL parser: reject non-numerical port numbers
- CONNECT: reject TE or CL in 2xx responses
- CONNECT: read responses one byte at a time
- curl: support zero-length argument strings in config files
- openssl: don't use OpenSSL's ERR_PACK
- curl.1: generated with the new man page system
- curl_easy_recv: Improve documentation and example program
- Curl_getconnectinfo: avoid checking if the connection is closed
- CIPHERS.md: attempt to document TLS cipher names

* Sat Nov 05 2016 Anton Novojilov <andy@essentialkaos.com> - 7.51.0-0
- nss: additional cipher suites are now accepted by CURLOPT_SSL_CIPHER_LIST
- New option: CURLOPT_KEEP_SENDING_ON_ERROR
- CVE-2016-8615: cookie injection for other servers
- CVE-2016-8616: case insensitive password comparison
- CVE-2016-8617: OOB write via unchecked multiplication
- CVE-2016-8618: double-free in curl_maprintf
- CVE-2016-8619: double-free in krb5 code
- CVE-2016-8620: glob parser write/read out of bounds
- CVE-2016-8621: curl_getdate read out of bounds
- CVE-2016-8622: URL unescape heap overflow via integer truncation
- CVE-2016-8623: Use-after-free via shared cookies
- CVE-2016-8624: invalid URL parsing with '#'
- CVE-2016-8625: IDNA 2003 makes curl use wrong host
- openssl: fix per-thread memory leak using 1.0.1 or 1.0.2
- http: accept "Transfer-Encoding: chunked" for HTTP/2 as well
- LICENSE-MIXING.md: update with mbedTLS dual licensing
- examples/imap-append: Set size of data to be uploaded
- test2048: fix url
- darwinssl: disable RC4 cipher-suite support
- CURLOPT_PINNEDPUBLICKEY.3: fix the AVAILABILITY formatting
- openssl: don’t call CRYTPO_cleanup_all_ex_data
- libressl: fix version output
- easy: Reset all statistical session info in curl_easy_reset
- curl_global_cleanup.3: don't unload the lib with sub threads running
- dist: add CurlSymbolHiding.cmake to the tarball
- docs: Remove that --proto is just used for initial retrieval
- configure: Fixed builds with libssh2 in a custom location
- curl.1: --trace supports %% for sending to stderr!
- cookies: same domain handling changed to match browser behavior
- formpost: trying to attach a directory no longer crashes
- CURLOPT_DEBUGFUNCTION.3: fixed unused argument warning
- formpost: avoid silent snprintf() truncation
- ftp: fix Curl_ftpsendf
- mprintf: return error on too many arguments
- smb: properly check incoming packet boundaries
- GIT-INFO: remove the Mac 10.1-specific details
- resolve: add error message when resolving using SIGALRM
- cmake: add nghttp2 support
- dist: remove PDF and HTML converted docs from the releases
- configure: disable poll() in macOS builds
- vtls: only re-use session-ids using the same scheme
- pipelining: skip to-be-closed connections when pipelining
- win: fix Universal Windows Platform build
- curl: do not set CURLOPT_SSLENGINE to DEFAULT automatically
- maketgz: make it support "only" generating version info
- Curl_socket_check: add extra check to avoid integer overflow
- gopher: properly return error for poll failures
- curl: set INTERLEAVEDATA too
- polarssl: clear thread array at init
- polarssl: fix unaligned SSL session-id lock
- polarssl: reduce #ifdef madness with a macro
- curl_multi_add_handle: set timeouts in closure handles
- configure: set min version flags for builds on mac
- INSTALL: converted to markdown => INSTALL.md
- curl_multi_remove_handle: fix a double-free
- multi: fix inifinte loop in curl_multi_cleanup()
- nss: fix tight loop in non-blocking TLS handhsake over proxy
- mk-ca-bundle: Change URL retrieval to HTTPS-only by default
- mbedtls: stop using deprecated include file
- docs: fix req->data in multi-uv example
- configure: Fix test syntax for monotonic clock_gettime
- CURLMOPT_MAX_PIPELINE_LENGTH.3: Clarify it's not for HTTP/2

* Tue Nov 01 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.3-0
- CVE-2016-7167: escape and unescape integer overflows
- mk-ca-bundle.pl: use SHA256 instead of SHA1
- checksrc: detect strtok() use
- errors: new alias CURLE_WEIRD_SERVER_REPLY
- http2: support > 64bit sized uploads
- openssl: fix bad memory free (regression)
- CMake: hide private library symbols
- http: refuse to pass on response body when NO_NODY is set
- cmake: fix curl-config --static-libs
- mbedtls: switch off NTLM in build if md4 isn't available
- curl: --create-dirs on windows groks both forward and backward slashes

* Thu Sep 08 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.2-0
- mbedtls: Added support for NTLM
- SSH: fixed SFTP/SCP transfer problems
- multi: make Curl_expire() work with 0 ms timeouts
- mk-ca-bundle.pl: -m keeps ca cert meta data in output
- TFTP: Fix upload problem with piped input
- CURLOPT_TCP_NODELAY: now enabled by default
- mbedtls: set verbose TLS debug when MBEDTLS_DEBUG is defined
- http2: always wait for readable socket
- cmake: Enable win32 large file support by default
- cmake: Enable win32 threaded resolver by default
- winbuild: Avoid setting redundant CFLAGS to compile commands
- curl.h: make CURL_NO_OLDIES define CURL_STRICTER
- docs: make more markdown files use .md extension
- docs: CONTRIBUTE and LICENSE-MIXING were converted to markdown
- winbuild: Allow changing C compiler via environment variable CC
- rtsp: accept any RTSP session id
- HTTP: retry failed HEAD requests on reused connections too
- configure: add zlib search with pkg-config
- openssl: accept subjectAltName iPAddress if no dNSName match
- MANUAL: Remove invalid link to LDAP documentation
- socks: improved connection procedure
- proxy: reject attempts to use unsupported proxy schemes
- proxy: bring back use of "Proxy-Connection:"
- curl: allow "pkcs11:" prefix for client certificates
- spnego_sspi: fix memory leak in case *outlen is zero
- SOCKS: improve verbose output of SOCKS5 connection sequence
- SOCKS: display the hostname returned by the SOCKS5 proxy server
- http/sasl: Query authentication mechanism supported by SSPI before using
- sasl: Don't use GSSAPI authentication when domain name not specified
- win: Basic support for Universal Windows Platform apps
- nss: fix incorrect use of a previously loaded certificate from file
- nss: work around race condition in PK11_FindSlotByName()
- ftp: fix wrong poll on the secondary socket
- openssl: build warning-free with 1.1.0 (again)
- HTTP: stop parsing headers when switching to unknown protocols
- test219: Add http as a required feature
- TLS: random file/egd doesn't have to match for conn reuse
- schannel: Disable ALPN for Wine since it is causing problems
- http2: make sure stream errors don't needlessly close the connection
- http2: return CURLE_HTTP2_STREAM for unexpected stream close
- darwinssl: --cainfo is intended for backward compatibility only
- speed caps: not based on average speeds anymore
- configure: make the cpp -P detection not clobber CPPFLAGS
- http2: use named define instead of magic constant in read callback
- http2: skip the content-length parsing, detect unknown size
- http2: return EOF when done uploading without known size
- darwinssl: test for errSecSuccess in PKCS12 import rather than noErr
- openssl: fix CURLINFO_SSL_VERIFYRESULT

* Thu Aug 04 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 7.50.1-0
- Initial build
