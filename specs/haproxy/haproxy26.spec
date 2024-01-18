################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  2.6
%define comp_ver   26

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   3.0.12
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.6.16
Release:        0%{?dist}
License:        GPLv2+
URL:            https://haproxy.1wt.eu
Group:          System Environment/Daemons

Source0:        https://www.haproxy.org/download/%{major_ver}/src/%{orig_name}-%{version}.tar.gz
Source1:        %{orig_name}.cfg
Source2:        %{orig_name}.logrotate

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

Conflicts:      haproxy haproxy22 haproxy24 haproxy28

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

%setup -qn %{orig_name}-%{version}

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

sed "s#@SBINDIR@#%{_sbindir}#g" admin/systemd/%{orig_name}.service.in > \
                                admin/systemd/%{orig_name}.service

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -pDm 0644 %{SOURCE1} %{buildroot}%{hp_confdir}/%{orig_name}.cfg
install -pDm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{orig_name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 admin/systemd/%{orig_name}.service %{buildroot}%{_unitdir}/

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
  systemctl enable %{orig_name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  systemctl --no-reload disable %{orig_name}.service &>/dev/null || :
  systemctl stop %{orig_name}.service &>/dev/null || :
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
%config(noreplace) %{hp_confdir}/%{orig_name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{orig_name}
%{hp_datadir}/*
%{_unitdir}/%{orig_name}.service
%{_sbindir}/%{orig_name}
%{_bindir}/halog
%{_mandir}/man1/%{orig_name}.1.gz

################################################################################

%changelog
* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.6.16-0
- CI: get rid of travis-ci wrapper for Coverity scan
- BUG/MINOR: hlua: fix invalid use of lua_pop on error paths
- BUG/MINOR: stktable: allow sc-set-gpt(0) from tcp-request connection
- DOC: typo: fix sc-set-gpt references
- SCRIPTS: git-show-backports: automatic ref and base detection with -m
- BUILD: Makefile: add the USE_QUIC option to make help
- MINOR: atomic: make sure to always relax after a failed CAS
- BUG/MINOR: hlua_fcn: potentially unsafe stktable_data_ptr usage
- DOC: lua: fix core.register_action typo
- BUG/MINOR: ssl_sock: fix possible memory leak on OOM
- BUG/MINOR: ssl/cli: can't find ".crt" files when replacing a certificate
- BUG/MEDIUM: stconn: Wake applets on sending path if there is a pending
  shutdown
- BUG/MEDIUM: stconn: Don't block sends if there is a pending shutdown
- BUG/MINOR: quic: Possible skipped RTT sampling
- BUG/MAJOR: quic: Really ignore malformed ACK frames.
- BUG/MEDIUM: h1-htx: Ensure chunked parsing with full output buffer
- DOC: configuration: update examples for req.ver
- BUG/MINOR: quic: Wrong RTT adjusments
- BUG/MEDIUM: stconn/stream: Forward shutdown on write timeout
- BUG/MINOR: hlua/action: incorrect message on E_YIELD error
- CI: Update to actions/checkout@v4
- BUG/MINOR: quic: Wrong RTT computation (srtt and rrt_var)
- BUG/MINOR: quic: Leak of frames to send.
- BUG/MINOR: quic: Wrong cluster secret initialization
- MINOR: hlua: add hlua_stream_ctx_prepare helper function
- BUG/MEDIUM: hlua: streams don't support mixing lua-load with
  lua-load-per-thread
- Revert "BUG/MEDIUM: quic: missing check of dcid for init pkt including
  a token"
- CI: musl: highlight section if there are coredumps
- CI: musl: drop shopt in workflow invocation
- BUG/MEDIUM: hlua: don't pass stale nargs argument to lua_resume()
- BUG/MINOR: hlua/init: coroutine may not resume itself
- BUG/MEDIUM: mux-fcgi: Don't swap trash and dbuf when handling STDERR records
- BUG/MINOR: promex: fix backend_agg_check_status
- BUG/MINOR: freq_ctr: fix possible negative rate with the scaled API
- BUG/MAJOR: mux-h2: Report a protocol error for any DATA frame before headers
- BUG/MINOR: server: add missing free for server->rdr_pfx
- MINOR: pattern: fix pat_{parse,match}_ip() function comments
- BUG/MEDIUM: server/cli: don't delete a dynamic server that has streams
- BUILD: bug: make BUG_ON() void to avoid a rare warning
- BUG/MEDIUM: actions: always apply a longest match on prefix lookup
- BUG/MEDIUM: quic_conn: let the scheduler kill the task when needed
- MINOR: hlua: Set context's appctx when the lua socket is created
- MINOR: hlua: Don't preform operations on a not connected socket
- MINOR: hlua: Save the lua socket's timeout in its context
- MINOR: hlua: Save the lua socket's server in its context
- MINOR: hlua: Test the hlua struct first when the lua socket is connecting
- BUG/MEDIUM: hlua: Initialize appctx used by a lua socket on connect only
- BUG/MINOR: mux-h1: Ignore C-L when sending H1 messages if T-E is also set
- BUG/MEDIUM: h1: Ignore C-L value in the H1 parser if T-E is also set
- BUG/MINOR: hq-interop: simplify parser requirement
- BUG/MINOR: quic: Avoid crashing with unsupported cryptographic algos
- BUG/MINOR: quic: reject packet with no frame
- BUG/MINOR: mux-quic: support initial 0 max-stream-data
- BUG/MINOR: h3: strengthen host/authority header parsing
- BUG/MINOR: mux-quic: fix free on qcs-new fail alloc
- BUG/MINOR: mux-h2: make up other blocked streams upon removal from list
- BUG/MEDIUM: mux-h2: Don't report an error on shutr if a shutw is pending
- BUG/MINOR: mux-h2: fix http-request and http-keep-alive timeouts again
- BUG/MEDIUM: peers: Be sure to always refresh recconnect timer in sync task
- BUG/MEDIUM: peers: Fix synchro for huge number of tables
- BUG/MINOR: mux-h2: commit the current stream ID even on reject
- BUG/MINOR: mux-h2: update tracked counters with req cnt/req err
- DOC: internal: filters: fix reference to entities.pdf
- BUG/MINOR: ssl: load correctly @system-ca when ca-base is define
- MINOR: connection: add conn_pr_mode_to_proto_mode() helper func
- BUG/MEDIUM: server: "proto" not working for dynamic servers
- BUG/MINOR: ssl: suboptimal certificate selection with TLSv1.3 and dual
  ECDSA/RSA
- BUG/MEDIUM: ssl: segfault when cipher is NULL
- BUG/MINOR: tcpcheck: Report hexstring instead of binary one on check failure
- BUG/MINOR: stktable: missing free in parse_stick_table()
- BUG/MINOR: cfgparse/stktable: fix error message on stktable_init() failure
- CLEANUP: htx: Properly indent htx_reserve_max_data() function
- BUG/MINOR: stick-table/cli: Check for invalid ipv4 key
- BUG/MINOR: mux-h1: Properly handle http-request and http-keep-alive timeouts
- BUG/MEDIUM: pool: fix releasable pool calculation when overloaded
- DOC: management: -q is quiet all the time
- DOC: config: use the word 'backend' instead of 'proxy' in 'track' description
- BUG/MEDIUM: applet: Remove appctx from buffer wait list on release
- DOC: quic: Wrong syntax for "quic-cc-algo" keyword.
- BUG/MINOR: stconn: Handle abortonclose if backend connection was already
  set up
- MINOR: connection: Add a CTL flag to notify mux it should wait for reads again
- MEDIUM: mux-h1: Handle MUX_SUBS_RECV flag in h1_ctl() and susbscribe for reads
- BUG/MEDIUM: stream: Properly handle abortonclose when set on backend only
- REGTESTS: http: Improve script testing abortonclose option
- BUG/MINOR: http-client: Don't forget to commit changes on HTX message
- BUG/MEDIUM: stream: Don't call mux .ctl() callback if not implemented
- MINOR: htx: Use a macro for overhead induced by HTX
- MINOR: channel: Add functions to get info on buffers and deal with HTX streams
- BUG/MINOR: stconn: Fix streamer detection for HTX streams
- BUG/MINOR: stconn: Use HTX-aware channel's functions to get info on buffer
- BUG/MINOR: quic: do not consider idle timeout on CLOSING state
- BUG/MINOR: mux-quic: fix early close if unset client timeout
- BUG/MINOR: ssl: use a thread-safe sslconns increment
- MINOR: frontend: implement a dedicated actconn increment function
- BUG/MINOR: quic: idle timer task requeued in the past
- BUG/MEDIUM: quic: Avoid trying to send ACK frames from an empty ack ranges
  tree
- BUG/MEDIUM: quic: Possible crashes when sending too short Initial packets
- BUG/MINOR: sink: don't learn srv port from srv addr
- MEDIUM: quic: count quic_conn instance for maxconn
- MEDIUM: quic: count quic_conn for global sslconns
- BUG/MEDIUM: quic: fix actconn on quic_conn alloc failure
- BUG/MEDIUM: quic: fix sslconns on quic_conn alloc failure
- BUG/MEDIUM: mux-h2: fail earlier on malloc in takeover()
- BUG/MEDIUM: mux-h1: fail earlier on malloc in takeover()
- BUG/MEDIUM: mux-fcgi: fail earlier on malloc in takeover()
- BUG/MINOR: stream/cli: report correct stream age in "show sess"
- MINOR: stktable: add stktable_deinit function
- BUG/MINOR: proxy/stktable: missing frees on proxy cleanup
- REGTESTS: http: add a test to validate chunked responses delivery
- BUG/MINOR: startup: set GTUNE_SOCKET_TRANSFER correctly
- BUG/MINOR: sock: mark abns sockets as non-suspendable and always unbind them
- BUG/MEDIUM: quic: Possible crash for connections to be killed
- BUG/MINOR: server: do not leak default-server in defaults sections
- DOC: 51d: updated 51Degrees repo URL for v3.2.10
- DOC: config: fix timeout check inheritance restrictions
- REGTESTS: connection: disable http_reuse_be_transparent.vtc if !TPROXY
- DOC: lua: add sticktable class reference from Proxy.stktable
- DOC: lua: fix Proxy.get_mode() output
- BUG/MINOR: quic: fix CONNECTION_CLOSE_APP encoding
- BUG/MINOR: h3: always reject PUSH_PROMISE
- DOC: config: fix missing characters in set-spoe-group action
- BUG/MINOR: quic_tp: fix preferred_address decoding
- BUG/MINOR: config: Stopped parsing upon unmatched environment variables
- BUG/MINOR: cfgparse-listen: fix warning being reported as an alert
- DOC: config: specify supported sections for "max-session-srv-conns"
- DOC: config: add matrix entry for "max-session-srv-conns"
- DOC: config: fix monitor-fail typo
- REGTESTS: sample: Test the behavior of consecutive delimiters for the field
  converter
- BUG/MINOR: sample: Make the `word` converter compatible with `-m found`
- DOC: Clarify the differences between field() and word()
- BUG/MINOR: cache: Remove incomplete entries from the cache when stream
  is closed
- BUG/MEDIUM: pattern: don't trim pools under lock in pat_ref_purge_range()
- BUG/MINOR: quic: Possible memory leak from TX packets
- BUG/MEDIUM: quic: Avoid some crashes upon TX packet allocation failures
- BUG/MINOR: quic: Possible leak of TX packets under heavy load

* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 2.6.15-0
- BUG/MINOR: quic: Wrong encryption level flags checking
- BUG/MINOR: server: inherit from netns in srv_settings_cpy()
- BUG/MINOR: namespace: missing free in netns_sig_stop()
- BUG/MINOR: quic: Missing initialization (packet number space probing)
- BUG/MEDIUM: mworker: increase maxsock with each new worker
- BUG/MINOR: quic: ticks comparison without ticks API use
- DOC: Add tune.h2.max-frame-size option to table of contents
- REGTESTS: h1_host_normalization : Add a barrier to not mix up log messages
- BUG/MINOR: mworker: leak of a socketpair during startup failure
- BUG/MEDIUM: mux-h2: make sure control frames do not refresh the idle timeout
- BUG/MINOR: mux-h2: refresh the idle_timer when the mux is empty
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
- BUG/MINOR: tcp_sample: bc_{dst,src} return IP not INT
- BUG/MINOR: cache: A 'max-age=0' cache-control directive can be overriden
  by a s-maxage
- BUG/MEDIUM: sink: invalid server list in sink_new_from_logsrv()
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
- BUG/MINOR: sink/log: properly deinit srv in sink_new_from_logsrv()
- BUG/MINOR: config: Remove final '\n' in error messages
- BUG/MEDIUM: quic: token IV was not computed using a strong secret
- BUG/MINOR: quic: retry token remove one useless intermediate expand
- BUG/MEDIUM: quic: missing check of dcid for init pkt including a token
- BUG/MEDIUM: quic: timestamp shared in token was using internal time clock
- BUG/MINOR: hlua: hlua_yieldk ctx argument should support pointers
- DOC: config: Fix fc_src description to state the source address is returned
- BUG/MINOR: sample: Fix wrong overflow detection in add/sub conveters
- BUG/MINOR: http: Return the right reason for 302
- CI: explicitely highlight VTest result section if there's something
- BUILD: quic: fix warning during compilation using gcc-6.5
- BUG/MINOR: hlua: add check for lua_newstate
- BUG/MINOR: h1-htx: Return the right reason for 302 FCGI responses
- BUG/MINOR: quic: Missing parentheses around PTO probe variable.
- BUG/MEDIUM: listener: Acquire proxy's lock in relax_listener() if necessary
- MINOR: quic: Make ->set_encryption_secrets() be callable two times
- MINOR: quic: Useless call to SSL_CTX_set_quic_method()
- BUG/MEDIUM: h3: Properly report a C-L header was found to the HTX start-line
- DOC: configuration: describe Td in Timing events
- BUG/MINOR: chunk: fix chunk_appendf() to not write a zero if buffer is full
- BUG/MEDIUM: h3: Be sure to handle fin bit on the last DATA frame
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

* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.6.14-0
- BUG/MINOR: fd: always remove late updates when freeing fd_updt[]
- MINOR: ssl: ssl_sock_load_cert_chain() display error strings
- CI: switch to Fastly CDN to download LibreSSL
- BUILD: ssl: switch LibreSSL to Fastly CDN
- BUG/MEDIUM: spoe: Don't start new applet if there are enough idle ones
- BUG/MINOR: resolvers: Use sc_need_room() to wait more room when dumping stats
- MINOR: quic: use real sending rate measurement
- DEV: haring: automatically disable DEBUG_STRICT
- DEV: haring: update readme to suggest using the same build options for haring
- BUG/MINOR: mux-quic: prevent quic_conn error code to be overwritten
- BUG/MINOR: debug: do not emit empty lines in thread dumps
- BUG/MINOR: quic: Wrong key update cipher context initialization for encryption
- BUILD: ssl: buggy -Werror=dangling-pointer since gcc 13.0
- DOC: configuration: add info about ssl-engine for 2.6
- BUG/MINOR: quic: Possible crash when dumping version information
- BUILD: mjson: Fix warning about unused variables
- MINOR: spoe: Don't stop disabled proxies
- BUG/MEDIUM: filters: Don't deinit filters for disabled proxies during startup
- MINOR: http-rules: Add missing actions in http-after-response ruleset
- BUG/MINOR: quic: Buggy acknowlegments of acknowlegments function
- BUG/MEDIUM: mux-fcgi: Don't request more room if mux is waiting for more data
- BUG/MINOR: proxy: missing free in free_proxy for redirect rules
- MINOR: proxy: add http_free_redirect_rule() function
- BUG/MINOR: http_rules: fix errors paths in http_parse_redirect_rule()
- BUG/MINOR: errors: handle malloc failure in usermsgs_put()
- BUG/MINOR: log: fix memory error handling in parse_logsrv()
- MINOR: htx: add function to set EOM reliably
- MINOR: checks: make sure spread-checks is used also at boot time
- MINOR: clock: measure the total boot time
- BUG/MINOR: checks: postpone the startup of health checks by the boot time
- BUG/MINOR: clock: fix the boot time measurement method for 2.6 and older
- BUG/MINOR: tcp-rules: Don't shortened the inspect-delay when EOI is set
- REGTESTS: log: Reduce response inspect-delay for last_rule.vtc
- DOC: config: Clarify conditions to shorten the inspect-delay for TCP rules
- REGTESTS: log: Reduce again response inspect-delay for last_rule.vtc
- DOC: add size format section to manual
- DOC/MINOR: config: Fix typo in description for `ssl_bc` in configuration.txt
- BUG/MINOR: hlua: unsafe hlua_lua2smp() usage
- SCRIPTS: publish-release: update the umask to keep group write access
- BUG/MINOR: mux-quic: properly handle buf alloc failure
- BUG/MINOR: mux-quic: handle properly recv ncbuf alloc failure
- BUG/MINOR: quic: do not alloc buf count on alloc failure
- BUG/MINOR: mux-quic: differentiate failure on qc_stream_desc alloc
- BUG/MINOR: mux-quic: handle properly Tx buf exhaustion
- MINOR: mux-quic: uninline qc_attach_sc()
- BUG/MEDIUM: mux-quic: fix EOI for request without payload
- BUG/MINOR: quic: Wrong token length check (quic_generate_retry_token())
- BUG/MINOR: quic: Missing Retry token length on receipt
- DOC: config: Fix bind/server/peer documentation in the peers section
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- BUG/MINOR: quic: Possible crash when SSL session init fails
- DOC: config: fix jwt_verify() example using var()
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
