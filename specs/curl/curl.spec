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
Version:              7.60.0
Release:              0%{?dist}
License:              MIT
Group:                Applications/Internet
URL:                  http://curl.haxx.se

Source0:              http://curl.haxx.se/download/%{name}-%{version}.tar.bz2

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

################################################################################

%changelog
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
