################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define hp_user      %{name}
%define hp_group     %{name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{name}
%define hp_confdir   %{_sysconfdir}/%{name}
%define hp_datadir   %{_datadir}/%{name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   3.1.3
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.8.3
Release:        0%{?dist}
License:        GPLv2+
URL:            https://haproxy.1wt.eu
Group:          System Environment/Daemons

Source0:        https://www.haproxy.org/download/2.8/src/%{name}-%{version}.tar.gz
Source1:        %{name}.cfg
Source2:        %{name}.logrotate

Source10:       https://www.lua.org/ftp/lua-%{lua_ver}.tar.gz
Source11:       https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{pcre_ver}/pcre2-%{pcre_ver}.tar.gz
Source12:       https://www.openssl.org/source/openssl-%{openssl_ver}.tar.gz
Source13:       https://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{ncurses_ver}.tar.gz
Source14:       https://ftp.gnu.org/gnu/readline/readline-%{readline_ver}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make zlib-devel systemd-devel perl perl-IPC-Cmd

%if 0%{?rhel} <= 7
BuildRequires:  devtoolset-11-gcc-c++ devtoolset-11-binutils
%else
BuildRequires:  gcc-c++
%endif

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
HAProxy is a free, fast and reliable solution offering high
availability, load balancing, and proxying for TCP and HTTP-based
applications. It is particularly suited for web sites crawling under
very high loads while needing persistence or Layer7 processing.
Supporting tens of thousands of connections is clearly realistic with
modern hardware. Its mode of operation makes integration with existing
architectures very easy and riskless, while still offering the
possibility not to expose fragile web servers to the net.

################################################################################

%prep
%{crc_check}

%setup -q

tar xzvf %{SOURCE10}
tar xzvf %{SOURCE11}
tar xzvf %{SOURCE12}
tar xzvf %{SOURCE13}
tar xzvf %{SOURCE14}

%build

%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from DevToolSet 11
export PATH="/opt/rh/devtoolset-11/root/usr/bin:$PATH"
%endif

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static OpenSSL build
pushd openssl-%{openssl_ver}
  mkdir build
  # perfecto:ignore
  ./config --prefix=$(pwd)/build no-shared no-threads
  %{__make}
  %{__make} install_sw
popd

# Static NCurses build
pushd ncurses-%{ncurses_ver}
  mkdir build
  # perfecto:ignore
  ./configure --prefix=$(pwd)/build --enable-shared=no
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

# Static readline build
pushd readline-%{readline_ver}
  mkdir build
  # perfecto:ignore
  ./configure --prefix=$(pwd)/build --enable-static=true
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

# Static Lua build
pushd lua-%{lua_ver}
  mkdir build
  %{__make} %{?_smp_mflags} \
            MYCFLAGS="-I$BUILDDIR/readline-%{readline_ver}/build/include" \
            MYLDFLAGS="-L$BUILDDIR/readline-%{readline_ver}/build/lib -L$BUILDDIR/ncurses-%{ncurses_ver}/build/lib -lreadline -lncurses" \
            linux
  %{__make} %{?_smp_mflags} INSTALL_TOP=$(pwd)/build install
popd

# Static PCRE build
pushd pcre2-%{pcre_ver}
  mkdir build
  # perfecto:ignore
  ./configure --prefix=$(pwd)/build \
              --enable-shared=no \
              --enable-jit
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

### DEPS BUILD END ###

%ifarch %ix86 x86_64
use_regparm="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" \
                          TARGET="linux-glibc" \
                          USE_OPENSSL=1 \
                          SSL_INC=openssl-%{openssl_ver}/build/include \
                          SSL_LIB=openssl-%{openssl_ver}/build/%{_lib} \
                          USE_PCRE2_JIT=1 \
                          USE_STATIC_PCRE2=1 \
                          PCRE2_INC=pcre2-%{pcre_ver}/build/include \
                          PCRE2_LIB=pcre2-%{pcre_ver}/build/lib \
                          USE_LUA=1 \
                          LUA_INC=lua-%{lua_ver}/build/include \
                          LUA_LIB=lua-%{lua_ver}/build/lib \
                          USE_ZLIB=1 \
                          USE_SYSTEMD=1 \
                          ADDLIB="-ldl -lrt -lpthread" \
                          ${use_regparm}

%{__make} admin/halog/halog

sed "s#@SBINDIR@#%{_sbindir}#g" admin/systemd/%{name}.service.in > \
                                admin/systemd/%{name}.service

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

pushd admin/systemd
  %{__make}
popd

install -pDm 0644 %{SOURCE1} %{buildroot}%{hp_confdir}/%{name}.cfg
install -pDm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 admin/systemd/%{name}.service %{buildroot}%{_unitdir}/

install -pm 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
install -pm 0644 ./examples/errorfiles/* %{buildroot}%{hp_datadir}

%clean
rm -rf %{buildroot}

%pre
if [[ $1 -eq 1 ]] ; then
  getent group %{hp_group} >/dev/null || groupadd -g %{hp_group_id} -r %{hp_group} 2>/dev/null
  getent passwd %{hp_user} >/dev/null || useradd -r -u %{hp_user_id} -g %{hp_group} -d %{hp_homedir} -s /sbin/nologin %{hp_user} 2>/dev/null
fi

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  systemctl --no-reload disable %{name}.service &>/dev/null || :
  systemctl stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  systemctl daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGELOG LICENSE README doc/* examples/*.cfg
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{hp_datadir}/*
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz

################################################################################

%changelog
* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.3-0
- CI: do not use "groupinstall" for Fedora Rawhide builds
- CI: get rid of travis-ci wrapper for Coverity scan
- BUG/MEDIUM: quic: fix tasklet_wakeup loop on connection closing
- BUG/MINOR: hlua: fix invalid use of lua_pop on error paths
- DEV: flags/show-sess-to-flags: properly decode fd.state
- BUG/MINOR: stktable: allow sc-set-gpt(0) from tcp-request connection
- BUG/MINOR: stktable: allow sc-add-gpc from tcp-request connection
- DOC: typo: fix sc-set-gpt references
- SCRIPTS: git-show-backports: automatic ref and base detection with -m
- REGTESTS: Do not use REQUIRE_VERSION for HAProxy 2.5+ (3)
- DOC: jwt: Add explicit list of supported algorithms
- BUILD: Makefile: add the USE_QUIC option to make help
- IMPORT: plock: also support inlining the int code
- MINOR: threads: inline the wait function for pthread_rwlock emulation
- MINOR: atomic: make sure to always relax after a failed CAS
- IMPORT: xxhash: update xxHash to version 0.8.2
- CI: fedora: fix "dnf" invocation syntax
- BUG/MINOR: hlua_fcn: potentially unsafe stktable_data_ptr usage
- DOC: lua: fix core.register_action typo
- BUG/MINOR: ssl_sock: fix possible memory leak on OOM
- BUILD: import: guard plock.h against multiple inclusion
- BUG/MINOR: ssl/cli: can't find ".crt" files when replacing a certificate
- BUG/MINOR: stream: protect stream_dump() against incomplete streams
- DOC: config: mention uid dependency on the tune.quic.socket-owner option
- BUG/MINOR: checks: do not queue/wake a bounced check
- DEBUG: applet: Properly report opposite SC expiration dates in traces
- BUG/MEDIUM: stconn: Update stream expiration date on blocked sends
- BUG/MINOR: stconn: Don't report blocked sends during connection establishment
- BUG/MEDIUM: stconn: Wake applets on sending path if there is a pending
  shutdown
- BUG/MEDIUM: stconn: Don't block sends if there is a pending shutdown
- BUG/MINOR: quic: Possible skipped RTT sampling
- BUG/MAJOR: quic: Really ignore malformed ACK frames.
- BUG/MEDIUM: h1-htx: Ensure chunked parsing with full output buffer
- BUG/MINOR: stream: further protect stream_dump() against incomplete sessions
- DOC: configuration: update examples for req.ver
- MINOR: httpclient: allow to configure the retries
- MINOR: httpclient: allow to configure the timeout.connect
- BUG/MINOR: quic: Wrong RTT adjusments
- BUG/MINOR: quic: Wrong RTT computation (srtt and rrt_var)
- BUG/MEDIUM: applet: Fix API for function to push new data in channels buffer
- BUG/MEDIUM: stconn: Report read activity when a stream is attached to front SC
- BUG/MEDIUM: applet: Report an error if applet request more room on aborted SC
- BUG/MEDIUM: stconn/stream: Forward shutdown on write timeout
- NUG/MEDIUM: stconn: Always update stream's expiration date after I/O
- BUG/MINOR: applet: Always expect data when CLI is waiting for a new command
- BUG/MINOR: ring/cli: Don't expect input data when showing events
- BUG/MINOR: hlua/action: incorrect message on E_YIELD error
- MEDIUM: capabilities: enable support for Linux capabilities
- CI: Update to actions/checkout@v4

* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- DOC: ssl: Fix typo in 'ocsp-update' option
- DOC: ssl: Add ocsp-update troubleshooting clues and emphasize on crt-list
  only aspect
- BUG/MINOR: tcp_sample: bc_{dst,src} return IP not INT
- BUG/MINOR: cache: A 'max-age=0' cache-control directive can be overriden
  by a s-maxage
- BUG/MEDIUM: sink: invalid server list in sink_new_from_logsrv()
- BUG/MINOR: http_ext: unhandled ERR_ABORT in proxy_http_parse_7239()
- BUG/MINOR: sink: missing sft free in sink_deinit()
- BUG/MINOR: ring: size warning incorrectly reported as fatal error
- BUG/MINOR: ring: maxlen warning reported as alert
- BUG/MINOR: log: LF upsets maxlen for UDP targets
- MINOR: sink/api: pass explicit maxlen parameter to sink_write()
- BUG/MEDIUM: log: improper use of logsrv->maxlen for buffer targets
- BUG/MINOR: log: fix missing name error message in cfg_parse_log_forward()
- BUG/MINOR: log: fix multiple error paths in cfg_parse_log_forward()
- BUG/MINOR: log: free errmsg on error in cfg_parse_log_forward()
- BUG/MINOR: sink: invalid sft free in sink_deinit()
- BUG/MINOR: sink: fix errors handling in cfg_post_parse_ring()
- BUG/MINOR: server: set rid default value in new_server()
- MINOR: hlua_fcn/mailers: handle timeout mail from mailers section
- BUG/MINOR: sink/log: properly deinit srv in sink_new_from_logsrv()
- EXAMPLES: maintain haproxy 2.8 retrocompatibility for lua mailers script
- BUG/MINOR: hlua_fcn/queue: use atomic load to fetch queue size
- BUG/MINOR: config: Remove final '\n' in error messages
- BUG/MEDIUM: quic: token IV was not computed using a strong secret
- BUG/MINOR: quic: retry token remove one useless intermediate expand
- BUG/MEDIUM: quic: missing check of dcid for init pkt including a token
- BUG/MEDIUM: quic: timestamp shared in token was using internal time clock
- CLEANUP: quic: remove useless parameter 'key' from quic_packet_encrypt
- BUG/MINOR: hlua: hlua_yieldk ctx argument should support pointers
- BUG/MEDIUM: hlua_fcn/queue: bad pop_wait sequencing
- DOC: config: Fix fc_src description to state the source address is returned
- BUG/MINOR: sample: Fix wrong overflow detection in add/sub conveters
- BUG/MINOR: http: Return the right reason for 302
- CI: add naming convention documentation
- CI: explicitely highlight VTest result section if there's something
- BUILD: quic: fix warning during compilation using gcc-6.5
- BUG/MINOR: hlua: add check for lua_newstate
- BUG/MINOR: h1-htx: Return the right reason for 302 FCGI responses
- MINOR: cpuset: add cpu_map_configured() to know if a cpu-map was found
- BUG/MINOR: config: do not detect NUMA topology when cpu-map is configured
- BUG/MINOR: cpuset: remove the bogus "proc" from the cpu_map struct
- BUG/MINOR: init: set process' affinity even in foreground
- BUG/MINOR: server: Don't warn on server resolution failure with init-addr none
- BUG/MINOR: quic: Missing parentheses around PTO probe variable.
- BUG/MINOR: server-state: Ignore empty files
- BUG/MINOR: server-state: Avoid warning on 'file not found'
- BUG/MEDIUM: listener: Acquire proxy's lock in relax_listener() if necessary
- MINOR: quic: Make ->set_encryption_secrets() be callable two times
- MINOR: quic: Useless call to SSL_CTX_set_quic_method()
- BUG/MINOR: ssl: OCSP callback only registered for first SSL_CTX
- BUG/MEDIUM: h3: Properly report a C-L header was found to the HTX start-line
- DOC: configuration: describe Td in Timing events
- BUG/MINOR: chunk: fix chunk_appendf() to not write a zero if buffer is full
- BUG/MEDIUM: h3: Be sure to handle fin bit on the last DATA frame
- BUG/MEDIUM: bwlim: Reset analyse expiration date when then channel analyse
  ends
- BUG/MEDIUM: quic: consume contig space on requeue datagram
- BUG/MINOR: http-client: Don't forget to commit changes on HTX message
- BUG/MINOR: quic: reappend rxbuf buffer on fake dgram alloc error
- BUILD: quic: fix wrong potential NULL dereference
- BUG/MAJOR: http-ana: Get a fresh trash buffer for each header value
  replacement
- REORG: http: move has_forbidden_char() from h2.c to http.h
- BUG/MAJOR: h3: reject header values containing invalid chars
- BUG/MAJOR: http: reject any empty content-length header value
- MINOR: ist: add new function ist_find_range() to find a character range
- MINOR: http: add new function http_path_has_forbidden_char()
- MINOR: h2: pass accept-invalid-http-request down the request parser
- REGTESTS: http-rules: add accept-invalid-http-request for normalize-uri tests
- BUG/MINOR: h1: do not accept '#' as part of the URI component
- BUG/MINOR: h2: reject more chars from the :path pseudo header
- BUG/MINOR: h3: reject more chars from the :path pseudo header
- REGTESTS: http-rules: verify that we block '#' by default for normalize-uri
- DOC: clarify the handling of URL fragments in requests
- BUG/MINOR: http: skip leading zeroes in content-length values

* Fri Jul 14 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- BUG/MINOR: stats: Fix Lua's `get_stats` function
- BUG/MINOR: stream: do not use client-fin/server-fin with HTX
- BUG/MINOR: quic: Possible crash when SSL session init fails
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- DOC: quic: fix misspelled tune.quic.socket-owner
- DOC: config: fix jwt_verify() example using var()
- DOC: config: fix rfc7239 converter examples (again)
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
- BUG/MINOR: proxy/server: free default-server on deinit
- BUG/MEDIUM: hlua: Use front SC to detect EOI in HTTP applets' receive
  functions
- BUG/MINOR: peers: Improve detection of config errors in peers sections
- REG-TESTS: stickiness: Delay haproxys start to properly resolv variables
- BUG/MINOR: ssl: log message non thread safe in SSL Hanshake failure
- BUG/MINOR: quic: Wrong encryption level flags checking
- BUG/MINOR: quic: Address inversion in "show quic full"
- BUG/MINOR: server: inherit from netns in srv_settings_cpy()
- BUG/MINOR: namespace: missing free in netns_sig_stop()
- BUG/MINOR: quic: Missing initialization (packet number space probing)
- BUG/MINOR: quic: Possible crash in quic_conn_prx_cntrs_update()
- BUG/MINOR: quic: Possible endless loop in quic_lstnr_dghdlr()
- BUG/MEDIUM: mworker: increase maxsock with each new worker
- BUG/MINOR: quic: ticks comparison without ticks API use
- DOC: Add tune.h2.be.* and tune.h2.fe.* options to table of contents
- DOC: Add tune.h2.max-frame-size option to table of contents
- REGTESTS: h1_host_normalization : Add a barrier to not mix up log messages
- DOC: Attempt to fix dconv parsing error for tune.h2.fe.initial-window-size
- BUG/MINOR: http_ext: fix if-none regression in forwardfor option
- BUG/MINOR: mworker: leak of a socketpair during startup failure
- BUG/MINOR: quic: Prevent deadlock with CID tree lock
- BUG/MEDIUM: quic: error checking buffer large enought to receive the retry tag
- BUG/MINOR: config: fix stick table duplicate name check
- BUG/MINOR: quic: Missing random bits in Retry packet header
- BUG/MINOR: quic: Wrong Retry paquet version field endianess
- BUG/MINOR: quic: Wrong endianess for version field in Retry token
- IMPORT: slz: implement a synchronous flush() operation
- MINOR: compression/slz: add support for a pure flush of pending bytes
- BUILD: debug: avoid a build warning related to epoll_wait() in debug code
- MINOR: quic: Move QUIC encryption level structure definition
- MINOR: quic: Move packet number space related functions
- MINOR: quic: Reduce the maximum length of TLS secrets
- CLEANUP: quic: Remove server specific about Initial packet number space

* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- MINOR: compression: Improve the way Vary header is added
- BUILD: makefile: search for SSL_INC/wolfssl before SSL_INC
- MINOR: init: pre-allocate kernel data structures on init
- DOC: install: add details about WolfSSL
- BUG/MINOR: ssl_sock: add check for ha_meth
- BUG/MINOR: thread: add a check for pthread_create
- BUILD: init: print rlim_cur as regular integer
- DOC: install: specify the minimum openssl version recommended
- CLEANUP: mux-quic: remove unneeded fields in qcc
- MINOR: mux-quic: remove nb_streams from qcc
- MINOR: quic: fix stats naming for flow control BLOCKED frames
- BUG/MEDIUM: mux-quic: only set EOI on FIN
- BUG/MEDIUM: threads: fix a tiny race in thread_isolate()
- DOC: config: fix rfc7239 converter examples
- DOC: quic: remove experimental status for QUIC
- CLEANUP: mux-quic: rename functions for mux_ops
- CLEANUP: mux-quic: rename internal functions
- BUG/MINOR: mux-h2: refresh the idle_timer when the mux is empty
- DOC: config: Fix bind/server/peer documentation in the peers section
- BUILD: Makefile: use -pthread not -lpthread when threads are enabled
- CLEANUP: doc: remove 21 totally obsolete docs
- DOC: install: mention the common strict-aliasing warning on older compilers
- DOC: install: clarify a few points on the wolfSSL build method
- MINOR: quic: Add QUIC connection statistical counters values to "show quic"
- EXAMPLES: update the basic-config-edge file for 2.8
- MINOR: quic/cli: clarify the "show quic" help message
- MINOR: version: mention that it's LTS now.
