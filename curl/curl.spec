###############################################################################

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

###############################################################################

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

%if 0%{?fedora} > 21 || 0%{?rhel} > 6
%define have_multilib_rpm_config 1
%else
%define have_multilib_rpm_config 0
%endif

###############################################################################

Summary:              Utility for getting files from remote servers
Name:                 curl
Version:              7.54.0
Release:              0%{?dist}
License:              MIT
Group:                Applications/Internet
URL:                  http://curl.haxx.se

Source0:              http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Source100:            curlbuild.h

Patch101:             0101-%{name}-7.41.1-multilib.patch
Patch102:             0102-%{name}-7.48.0-debug.patch
Patch108:             0108-%{name}-7.40.0-threaded-dns-multi.patch
Patch302:             0302-%{name}-7.47.1-pkgconfig.patch

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

%if %{have_multilib_rpm_config}
BuildRequires:        multilib-rpm-config
%endif

Requires:             libcurl%{?_isa} = %{version}-%{release}
%if ! %{use_nss}
Requires:             %{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%endif

###############################################################################

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks.

###############################################################################

# Require at least the version of libssh2/c-ares that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%define libssh2_version   %(pkg-config --modversion libssh2 2>/dev/null || echo 0)
%define cares_version     %(pkg-config --modversion libcares 2>/dev/null || echo 0)

###############################################################################

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

###############################################################################

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

###############################################################################

%prep
%setup -qn curl-%{version}

%patch101 -p1
%patch102 -p1

%if 0%{?use_threads_posix} && 0%{?fedora} < 14 && 0%{?rhel} < 7
%patch108
%endif

%patch302

%build
%if ! 0%{?use_nss}
export CPPFLAGS="$(pkg-config --cflags openssl)"
%endif

[ -x /usr/kerberos/bin/krb5-config ] && KRB5_PREFIX="=/usr/kerberos"

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
make %{_smp_mflags} V=1

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install

install -dm 0755 %{buildroot}%{_datadir}/aclocal

install -pm 0644 docs/libcurl/libcurl.m4 %{buildroot}%{_datadir}/aclocal

%if %{have_multilib_rpm_config}
  %multilib_fix_c_header --file %{_includedir}/%{name}/curlbuild.h
%else
  %if %{__isa_bits} == 64
    mv %{buildroot}%{_includedir}/%{name}/curlbuild{,-64}.h
  %else
    mv %{buildroot}%{_includedir}/%{name}/curlbuild{,-32}.h
  %endif
  
  install -pm 644 %{SOURCE100} %{buildroot}%{_includedir}/%{name}
%endif

%clean
rm -rf %{buildroot}

%post -n libcurl
/sbin/ldconfig

%postun -n libcurl
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES README*
%doc docs/BUGS docs/FAQ docs/FEATURES docs/SECURITY.md docs/TODO docs/HTTP2.md
%doc docs/SSL-PROBLEMS.md docs/THANKS docs/KNOWN_BUGS docs/FEATURES
%doc docs/MANUAL docs/RESOURCES docs/TheArtOfHttpScripting
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

###############################################################################

%changelog
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
- curl.1: --trace supports % for sending to stderr!
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
