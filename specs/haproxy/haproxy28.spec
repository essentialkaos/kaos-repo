################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  2.8
%define comp_ver   28

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.7
%define pcre_ver      10.44
%define openssl_ver   3.1.7
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.8.11
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

BuildRequires:  make gcc-c++ zlib-devel systemd-devel perl perl-IPC-Cmd

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy30

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

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static OpenSSL build
pushd openssl-%{openssl_ver}
  mkdir build
  # perfecto:ignore
  ./config --prefix=$(pwd)/build no-shared no-threads
  %{__make} %{?_smp_mflags}
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
* Sat Nov 02 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.11-0
- BUG/MINOR: quic: fix computed length of emitted STREAM frames
- BUG/MINOR: proxy: fix server_id_hdr_name leak on deinit()
- BUG/MINOR: proxy: fix log_tag leak on deinit()
- BUG/MINOR: proxy: fix check_{command,path} leak on deinit()
- BUG/MINOR: proxy: fix dyncookie_key leak on deinit()
- BUG/MINOR: proxy: fix source interface and usesrc leaks on deinit()
- BUG/MINOR: proxy: fix header_unique_id leak on deinit()
- DOC/MINOR: management: add missed -dR and -dv options
- DOC: management: rename show stats domain cli "dns" to "resolvers"
- DOC: configuration: fix alphabetical order of bind options
- SCRIPTS: git-show-backports: do not truncate git-show output
- DOC: api/event_hdl: small updates, fix an example and add some precisions
- BUG/MINOR: h3: fix crash on STOP_SENDING receive after GOAWAY emission
- BUG/MINOR: mux-quic: fix crash on qcs SD alloc failure
- BUG/MINOR: quic: fix BUG_ON() on Tx pkt alloc failure
- BUG/MINOR: hlua: report proper context upon error in hlua_cli_io_handler_fct()
- MINOR: activity: make the memory profiling hash size configurable at build
  time
- BUG/MEDIUM: h3: ensure the ":method" pseudo header is totally valid
- BUG/MEDIUM: h3: ensure the ":scheme" pseudo header is totally valid
- BUG/MEDIUM: quic: fix race-condition in quic_get_cid_tid()
- BUG/MINOR: quic: fix race condition in qc_check_dcid()
- BUG/MINOR: quic: fix race-condition on trace for CID retrieval
- BUG/MEDIUM: quic: fix possible exit from qc_check_dcid() without unlocking
- DOC: configuration: more details about the master-worker mode
- MEDIUM: ssl: initialize the SSL stack explicitely
- BUG/MINOR: jwt: don't try to load files with HMAC algorithm
- DOC: configuration: update maxconn description
- BUG/MINOR: jwt: fix variable initialisation
- BUG/MINOR: h1: Fail to parse empty transfer coding names
- BUG/MINOR: h1: Reject empty coding name as last transfer-encoding value
- BUG/MEDIUM: h1: Reject empty Transfer-encoding header
- BUG/MEDIUM: spoe: Be sure to create a SPOE applet if none on the current
  thread
- BUG/MEDIUM: bwlim: Be sure to never set the analyze expiration date in past
- BUG/MINOR: session: Eval L4/L5 rules defined in the default section
- BUG/MEDIUM: debug/cli: fix "show threads" crashing with low thread counts
- BUG/MEDIUM: ssl_sock: fix deadlock in ssl_sock_load_ocsp() on error path
- DOC: configuration: issuers-chain-path not compatible with OCSP
- DOC: config: improve the http-keep-alive section
- BUG/MINOR: stick-table: fix crash for src_inc_gpc() without stkcounter
- BUG/MINOR: server: Don't warn fallback IP is used during init-addr resolution
- BUG/MINOR: cli: Atomically inc the global request counter between CLI commands
- BUG/MINOR: quic: Lack of precision when computing K (cubic only cc)
- BUG/MEDIUM: jwt: Clear SSL error queue on error when checking the signature
- MINOR: queue: add a function to check for TOCTOU after queueing
- BUG/MEDIUM: queue: deal with a rare TOCTOU in assign_server_and_queue()
- MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD (take #2)
- BUG/MEDIUM: init: fix fd_hard_limit default in compute_ideal_maxconn
- BUG/MEDIUM: stream: Prevent mux upgrades if client connection is no longer
  ready
- BUG/MEDIUM: cli: Always release back endpoint between two commands on the mcli
- BUG/MEDIUM: mux-h1: Properly handle empty message when an error is triggered
- BUG/MEDIUM: stconn: Report error on SC on send if a previous SE error was set
- BUG/MEDIUM: quic: prevent conn freeze on 0RTT undeciphered content
- BUG/MEDIUM: http-ana: Report error on write error waiting for the response
- BUG/MEDIUM: h2: Only report early HTX EOM for tunneled streams
- BUG/MEDIUM: mux-h2: Propagate term flags to SE on error in h2s_wake_one_stream
- BUG/MINOR: fcgi-app: handle a possible strdup() failure
- BUG/MINOR: trace/quic: enable conn/session pointer recovery from quic_conn
- BUG/MINOR: trace/quic: permit to lock on frontend/connect/session etc
- BUG/MEDIUM: trace: fix null deref in lockon mechanism since TRACE_ENABLED()
- BUG/MINOR: trace: automatically start in waiting mode with "start <evt>"
- BUG/MINOR: trace/quic: make "qconn" selectable as a lockon criterion
- BUG/MINOR: quic/trace: make quic_conn_enc_level_init() emit NEW not CLOSE
- BUG/MINOR: proto_tcp: delete fd from fdtab if listen() fails
- BUG/MINOR: proto_tcp: keep error msg if listen() fails
- MINOR: channel: implement ci_insert() function
- BUG/MEDIUM: mworker/cli: fix pipelined modes on master CLI
- REGTESTS: mcli: test the pipelined commands on master CLI
- BUG/MINOR: mux-quic: do not send too big MAX_STREAMS ID
- BUG/MINOR: proto_uxst: delete fd from fdtab if listen() fails
- BUG/MINOR: h3: properly reject too long header responses
- DOC: config: correct the table for option tcplog
- BUG/MEDIUM: clock: also update the date offset on time jumps
- BUG/MEDIUM: mux-pt/mux-h1: Release the pipe on connection error on sending
  path
- BUG/MINOR: stconn: Request to send something to be woken up when the pipe is
  full
- BUG/MINOR: pattern: pat_ref_set: fix UAF reported by coverity
- BUG/MINOR: pattern: pat_ref_set: return 0 if err was found
- BUG/MINOR: pattern: do not leave a leading comma on "set" error messages
- DOC: configuration: place the HAPROXY_HTTP_LOG_FMT example on the correct line
- REGTESTS: fix random failures with wrong_ip_port_logging.vtc under load
- BUG/MEDIUM: clock: detect and cover jumps during execution
- BUG/MINOR: pattern: prevent const sample from being tampered in
  pat_match_beg()
- BUG/MEDIUM: pattern: prevent UAF on reused pattern expr
- BUG/MAJOR: mux-h1: Wake SC to perform 0-copy forwarding in CLOSING state
- BUG/MINOR: polling: fix time reporting when using busy polling
- BUG/MINOR: clock: make time jump corrections a bit more accurate
- BUG/MINOR: clock: validate that now_offset still applies to the current date
- BUG/MEDIUM: queue: implement a flag to check for the dequeuing
- BUG/MEDIUM: cache/stats: Wait to have the request before sending the response
- BUG/MEDIUM: promex: Wait to have the request before sending the response
- BUG/MINOR: cfgparse-listen: fix option httpslog override warning message

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.10-0
- BUG/MINOR: cli: Report an error to user if command or payload is too big
- BUG/MINOR: listener: always assign distinct IDs to shards
- BUG/MINOR: log: fix lf_text_len() truncate inconsistency
- BUG/MINOR: tools/log: invalid encode_{chunk,string} usage
- BUG/MINOR: log: invalid snprintf() usage in sess_build_logline()
- CLEANUP: log: lf_text_len() returns a pointer not an integer
- BUG/MEDIUM: http-ana: Deliver 502 on keep-alive for fressh server connection
- BUG/MINOR: http-ana: Fix TX_L7_RETRY and TX_D_L7_RETRY values
- BUG/MINOR: debug: make sure DEBUG_STRICT=0 does work as documented
- BUG/MEDIUM: peers/trace: fix crash when listing event types
- CI: revert kernel addr randomization introduced in 3a0fc864
- MINOR: net_helper: Add support for floats/doubles.
- BUG/MEDIUM: grpc: Fix several unaligned 32/64 bits accesses
- BUG/MEDIUM: stconn: Don't forward channel data if input data must be filtered
- BUG/MEDIUM: evports: do not clear returned events list on signal
- BUG/MEDIUM: applet: Fix applet API to put input data in a buffer
- BUG/MEDIUM: spoe: Always retry when an applet fails to send a frame
- BUG/MEDIUM: peers: Fix exit condition when max-updates-at-once is reached
- BUG/MINOR: server: fix slowstart behavior
- BUG/MEDIUM: cache: Vary not working properly on anything other than
  accept-encoding
- BUG/MINOR: stconn: Fix sc_mux_strm() return value
- BUG/MINOR: sock: handle a weird condition with connect()
- BUG/MINOR: fd: my_closefrom() on Linux could skip contiguous series of sockets
- BUG/MINOR: backend: use cum_sess counters instead of cum_conn
- BUG/MINOR: h1: fix detection of upper bytes in the URI
- BUG/MINOR: mworker: reintroduce way to disable seamless reload with
  -x /dev/null
- BUILD: clock: improve check for pthread_getcpuclockid()
- BUG/MINOR: haproxy: only tid 0 must not sleep if got signal
- DOC: lua: fix filters.txt file location
- MINOR: log: add dup_logsrv() helper function
- BUG/MINOR: log: keep the ref in dup_logger()
- BUG/MINOR: log: smp_rgs array issues with inherited global log directives
- BUG/MINOR: mux-quic: fix error code on shutdown for non HTTP/3
- BUG/MINOR: qpack: fix error code reported on QPACK decoding failure
- BUG/MEDIUM: htx: mark htx_sl as packed since it may be realigned
- BUG/MEDIUM: stick-tables: properly mark stktable_data as packed
- BUG/MINOR: h1: Check authority for non-CONNECT methods only if a scheme
  is found
- BUG/MEDIUM: h1: Reject CONNECT request if the target has a scheme
- BUILD: stick-tables: better mark the stktable_data as 32-bit aligned
- BUG/MEDIUM: fd: prevent memory waste in fdtab array
- BUG/MINOR: htpp-ana/stats: Specify that HTX redirect messages have
  a C-L header
- BUG/MINOR: stats: Don't state the 303 redirect response is chunked
- CLEANUP: ssl/cli: remove unused code in dump_crtlist_conf
- DOC: configuration: update the crt-list documentation
- BUG/MINOR: connection: parse PROXY TLV for LOCAL mode
- BUG/MAJOR: quic: Crash with TLS_AES_128_CCM_SHA256 (libressl only)
- BUG/MEDIUM: quic_tls: prevent LibreSSL < 4.0 from negotiating
  CHACHA20_POLY1305
- BUG/MEDIUM: mux-quic: Create sedesc in same time of the QUIC stream
- BUILD: quic: fix unused variable warning when threads are disabled
- MEDIUM: config: prevent communication with privileged ports
- BUG/MINOR: quic: adjust restriction for stateless reset emission
- BUG/MINOR: http-htx: Support default path during scheme based normalization
- BUG/MINOR: server: Don't reset resolver options on a new default-server line
- DOC: quic: specify that connection migration is not supported
- DOC: config: fix incorrect section reference about custom log format
- REGTESTS: acl_cli_spaces: avoid a warning caused by undefined logs
- CI: scripts: fix build of vtest regarding option -C
- BUILD: fd: errno is also needed without poll()
- CLEANUP: ssl/ocsp: readable ifdef in ssl_sock_load_ocsp
- BUG/MINOR: ssl/ocsp: init callback func ptr as NULL
- BUG/MINOR: activity: fix Delta_calls and Delta_bytes count
- BUG/MINOR: cfgparse: remove the correct option on httpcheck send-state warning
- BUG/MINOR: tcpcheck: report correct error in tcp-check rule parser
- BUG/MINOR: tools: fix possible null-deref in env_expand() on out-of-memory
- BUG/MINOR: hlua: use CertCache.set() from various hlua contexts
- BUG/MINOR: quic: prevent crash on qc_kill_conn()
- CLEANUP: hlua: use hlua_pusherror() where relevant
- BUG/MINOR: hlua: don't use lua_pushfstring() when we don't expect LJMP
- BUG/MINOR: hlua: fix unsafe hlua_pusherror() usage
- BUG/MINOR: hlua: prevent LJMP in hlua_traceback()
- BUG/MINOR: hlua: fix leak in hlua_ckch_set() error path
- CLEANUP: hlua: simplify ambiguous lua_insert() usage in hlua_ctx_resume()
- BUG/MEDIUM: ssl: wrong priority whem limiting ECDSA ciphers in ECDSA+RSA
  configuration
- BUG/MEDIUM: server: fix dynamic servers initial settings
- BUG/MEDIUM: quic: fix connection freeze on post handshake
- MINOR: session: rename private conns elements
- BUG/MAJOR: server: do not delete srv referenced by session
- BUG/MEDIUM: http_ana: ignore NTLM for reuse aggressive/always and no H1
- BUG/MAJOR: connection: fix server used_conns with H2 + reuse safe
- BUG/MEDIUM: quic: don't blindly rely on unaligned accesses

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.9-0
- BUILD: proxy: Replace free_logformat_list() to manually release log-format

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.8-0
- MINOR: mux-h2: add a counter of "glitches" on a connection
- BUG/MINOR: mux-h2: count rejected DATA frames against the connection's flow
  control
- MINOR: mux-h2: count excess of CONTINUATION frames as a glitch
- MINOR: mux-h2: count late reduction of INITIAL_WINDOW_SIZE as a glitch
- MINOR: mux-h2: always use h2c_report_glitch()
- MEDIUM: mux-h2: allow to set the glitches threshold to kill a connection
- MINOR: connection: add a new mux_ctl to report number of connection glitches
- MINOR: mux-h2: implement MUX_CTL_GET_GLITCHES
- MINOR: connection: add sample fetches to report per-connection glitches
- BUG/MAJOR: promex: fix crash on deleted server
- BUG/MINOR: quic: reject unknown frame type
- BUG/MINOR: quic: reject HANDSHAKE_DONE as server
- BUG/MINOR: qpack: reject invalid increment count decoding
- BUG/MINOR: qpack: reject invalid dynamic table capacity
- DOC: quic: Missing tuning setting in "Global parameters"
- BUG/MEDIUM: applet: Immediately free appctx on early error
- BUG/MEDIUM: hlua: Be able to garbage collect uninitialized lua sockets
- BUG/MEDIUM: hlua: Don't loop if a lua socket does not consume received data
- BUG/MEDIUM: quic: fix transient send error with listener socket
- DOC: quic: fix recommandation for bind on multiple address
- MINOR: quic: warn on bind on multiple addresses if no IP_PKTINFO support
- BUG/MINOR: ist: allocate nul byte on istdup
- BUG/MINOR: stats: drop srv refcount on early release
- BUG/MAJOR: server: fix stream crash due to deleted server
- BUG/MINOR: quic: fix output of show quic
- BUG/MINOR: ist: only store NUL byte on succeeded alloc
- BUG/MINOR: ssl/cli: duplicate cleaning code in cli_parse_del_crtlist
- LICENSE: event_hdl: fix GPL license version
- LICENSE: http_ext: fix GPL license version
- DOC: configuration: clarify ciphersuites usage
- BUG/MINOR: config/quic: Alert about PROXY protocol use on a QUIC listener
- BUG/MINOR: hlua: Fix log level to the right value when set via
  TXN:set_loglevel
- MINOR: hlua: Be able to disable logging from lua
- BUG/MINOR: tools: seed the statistical PRNG slightly better
- BUG/MINOR: hlua: fix unsafe lua_tostring() usage with empty stack
- BUG/MINOR: hlua: don't use lua_tostring() from unprotected contexts
- BUG/MINOR: hlua: fix possible crash in hlua_filter_new() under load
- BUG/MINOR: hlua: improper lock usage in hlua_filter_callback()
- BUG/MINOR: hlua: improper lock usage in hlua_filter_new()
- BUG/MEDIUM: hlua: improper lock usage with SET_SAFE_LJMP()
- BUG/MAJOR: hlua: improper lock usage with hlua_ctx_resume()
- BUG/MINOR: hlua: don't call ha_alert() in hlua_event_subscribe()
- BUG/MINOR: sink: fix a race condition in the TCP log forwarding code
- CI: skip scheduled builds on forks
- BUG/MINOR: ssl/cli: typo in new ssl crl-file CLI description
- BUG/MINOR: cfgparse: report proper location for log-format-sd errors
- BUILD: solaris: fix compilation errors
- DOC: configuration: clarify ciphersuites usage (V2)
- BUG/MINOR: ssl: fix possible ctx memory leak in sample_conv_aes_gcm()
- BUG/MINOR: hlua: segfault when loading the same filter from different contexts
- BUG/MINOR: hlua: missing lock in hlua_filter_new()
- BUG/MINOR: hlua: fix missing lock in hlua_filter_delete()
- DEBUG: lua: precisely identify if stream is stuck inside lua or not
- MINOR: hlua: use accessors for stream hlua ctx
- BUG/MEDIUM: hlua: streams don't support mixing lua-load with
  lua-load-per-thread (2nd try)
- BUG/MINOR: listener: Wake proxy's mngmt task up if necessary on session
  release
- BUG/MINOR: listener: Don't schedule frontend without task in
  listener_release()
- BUG/MEDIUM: spoe: Don't rely on stream's expiration to detect processing
  timeout
- BUG/MINOR: spoe: Be sure to be able to quickly close IDLE applets on soft-stop
- CI: temporarily adjust kernel entropy to work with ASAN/clang
- BUG/MEDIUM: spoe: Return an invalid frame on recv if size is too small
- BUG/MINOR: session: ensure conn owner is set after insert into session
- BUG/MEDIUM: ssl: Fix crash in ocsp-update log function
- BUG/MINOR: mux-quic: close all QCS before freeing QCC tasklet
- BUG/MEDIUM: mux-fcgi: Properly handle EOM flag on end-of-trailers HTX block
- OPTIM: http_ext: avoid useless copy in http_7239_extract_{ipv4,ipv6}
- BUG/MINOR: server: 'source' interface ignored from 'default-server' directive
- BUG/MINOR: ssl: Wrong ocsp-update "incompatibility" error message
- BUG/MINOR: ssl: Detect more 'ocsp-update' incompatibilities
- BUG/MINOR: server: fix persistence cookie for dynamic servers
- MINOR: server: allow cookie for dynamic servers
- MINOR: cli: Remove useless loop on commands to find unescaped semi-colon
- BUG/MEDIUM: cli: Warn if pipelined commands are delimited by a \n
- BUG/MINOR: server: ignore 'enabled' for dynamic servers
- BUG/MINOR: backend: properly handle redispatch 0
- BUG/MINOR: proxy: fix logformat expression leak in use_backend rules

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.7-0
- BUG/MAJOR: ssl/ocsp: crash with ocsp when old process exit or using ocsp CLI

* Thu Mar 21 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.6-0
- DOC: configuration: typo req.ssl_hello_type
- BUG/MINOR: mworker/cli: fix set severity-output support
- BUG/MEDIUM: quic: Possible buffer overflow when building TLS records
- BUG/MEDIUM: quic: QUIC CID removed from tree without locking
- BUG/MEDIUM: mux-h2: Report too large HEADERS frame only when rxbuf is empty
- BUG/MINOR: resolvers: default resolvers fails when network not configured
- DOC: config: Update documentation about local haproxy response
- MINOR: stats: store the parent proxy in stats ctx (http)
- BUG/MEDIUM: stats: unhandled switching rules with TCP frontend
- BUG/MINOR: mux-quic: always report error to SC on RESET_STREAM emission
- BUG/MINOR: quic: Wrong keylog callback setting.
- BUG/MINOR: quic: Missing call to TLS message callbacks
- MINOR: h3: check connection error during sending
- BUG/MINOR: h3: close connection on header list too big
- BUG/MINOR: h3: properly handle alloc failure on finalize
- BUG/MINOR: h3: close connection on sending alloc errors
- CLEANUP: quic: Remaining useless code into server part
- BUG/MEDIUM: h3: fix incorrect snd_buf return value
- BUG/MEDIUM: stconn: Forward shutdown on write timeout only if it is
  forwardable
- BUG/MEDIUM: spoe: Never create new spoe applet if there is no server up
- MINOR: mux-h2: support limiting the total number of H2 streams per connection
- DOC: configuration: corrected description of keyword
  tune.ssl.ocsp-update.mindelay
- BUG/MINOR: mux-quic: do not prevent non-STREAM sending on flow control
- BUG/MINOR: mux-h2: also count streams for refused ones
- BUG/MEDIUM: quic: keylog callback not called (USE_OPENSSL_COMPAT)
- MINOR: compiler: add a new DO_NOT_FOLD() macro to prevent code folding
- MINOR: debug: make sure calls to ha_crash_now() are never merged
- MINOR: debug: make ABORT_NOW() store the caller's line number when using abort
- MINOR: debug: make BUG_ON() catch build errors even without DEBUG_STRICT
- MINOR: mux-h2/traces: also suggest invalid header upon parsing error
- MINOR: mux-h2/traces: explicitly show the error/refused stream states
- MINOR: mux-h2/traces: clarify the "rejected H2 request" event
- BUG/MEDIUM: mux-h2: refine connection vs stream error on headers
- MINOR: mux-h2/traces: add a missing trace on connection WU with negative inc
- REGTESTS: add a test to ensure map-ordering is preserved
- BUG/MEDIUM: cli: some err/warn msg dumps add LR into CSV output on stat's CLI
- BUG/MINOR: vars/cli: fix missing LF after "get var" output
- BUG/MEDIUM: cli: fix once for all the problem of missing trailing LFs
- BUG/MINOR: jwt: fix jwt_verify crash on 32-bit archs
- BUG/MEDIUM: pool: fix rare risk of deadlock in pool_flush()
- BUG/MEDIUM: stconn: Allow expiration update when READ/WRITE event is pending
- BUG/MEDIUM: stconn: Don't check pending shutdown to wake an applet up
- BUG/MINOR: h1: Don't support LF only at the end of chunks
- BUG/MEDIUM: h1: Don't support LF only to mark the end of a chunk size
- BUG/MINOR: h1-htx: properly initialize the err_pos field
- BUG/MEDIUM: h1: always reject the NUL character in header values
- BUG/MAJOR: ssl_sock: Always clear retry flags in read/write functions
- BUG/MINOR: ssl: Fix error message after ssl_sock_load_ocsp call
- BUG/MINOR: ssl: Duplicate ocsp update mode when dup'ing ckch
- BUG/MINOR: ssl: Clear the ckch instance when deleting a crt-list line
- MINOR: ssl: Use OCSP_CERTID instead of ckch_store in ckch_store_build_certid
- BUG/MEDIUM: ocsp: Separate refcount per instance and per store
- BUG/MINOR: ssl: Destroy ckch instances before the store during deinit
- BUG/MINOR: ssl: Reenable ocsp auto-update after an "add ssl crt-list"
- REGTESTS: ssl: Fix empty line in cli command input
- REGTESTS: ssl: Add OCSP related tests
- BUG/MEDIUM: ssl: Fix crash when calling "update ssl ocsp-response" when an
  update is ongoing
- BUG/MINOR: h3: fix checking on NULL Tx buffer
- BUG/MEDIUM: mux-quic: report early error on stream
- CLEANUP: quic: Remove unused CUBIC_BETA_SCALE_FACTOR_SHIFT macro.
- MINOR: quic: Stop hardcoding a scale shifting value
  (CUBIC_BETA_SCALE_FACTOR_SHIFT)
- MINOR: quic: extract qc_stream_buf free in a dedicated function
- BUG/MEDIUM: quic: remove unsent data from qc_stream_desc buf
- MINOR: h3: add traces for stream sending function
- BUG/MEDIUM: h3: do not crash on invalid response status code
- BUG/MEDIUM: qpack: allow 6xx..9xx status codes
- BUG/MEDIUM: quic: fix crash on invalid qc_stream_buf_free() BUG_ON
- BUG/MINOR: quic: Wrong ack ranges handling when reaching the limit.
- CLEANUP: quic: Code clarifications for QUIC CUBIC (RFC 9438)
- BUG/MINOR: quic: fix possible integer wrap around in cubic window calculation
- MINOR: quic: Stop using 1024th of a second.
- BUG/MEDIUM: quic: Wrong K CUBIC calculation.
- MINOR: quic: Update K CUBIC calculation (RFC 9438)
- MINOR: quic: Dynamic packet reordering threshold
- MINOR: quic: Add a counter for reordered packets
- MINOR: errors: ha_alert() and ha_warning() uses warn_exec_path()
- BUG/MINOR: diag: always show the version before dumping a diag warning
- BUG/MINOR: diag: run the final diags before quitting when using -c
- MINOR: ext-check: add an option to preserve environment variables
- BUG/MINOR: ext-check: cannot use without preserve-env
- BUILD: address a few remaining calloc(size, n) cases
- DOC: configuration: clarify http-request wait-for-body
- DOC: httpclient: add dedicated httpclient section
- DOC: install: recommend pcre2
- DOC: internal: update missing data types in peers-v2.0.txt
- CI: Update to actions/cache@v4
- DEV: makefile: add a new "range" target to iteratively build all commits
- DEV: makefile: fix POSIX compatibility for "range" target

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.8.5-0
- BUG/MAJOR: quic: complete thread migration before tcp-rules
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
- BUG/MINOR: quic: Possible RX packet memory leak under heavy load
- BUG/MINOR: server: do not leak default-server in defaults sections
- DOC: 51d: updated 51Degrees repo URL for v3.2.10
- DOC: config: fix timeout check inheritance restrictions
- REGTESTS: connection: disable http_reuse_be_transparent.vtc if !TPROXY
- DOC: lua: add sticktable class reference from Proxy.stktable
- DOC: lua: fix Proxy.get_mode() output
- BUG/MINOR: quic: fix CONNECTION_CLOSE_APP encoding
- BUG/MINOR: compression: possible NULL dereferences in
  comp_prepare_compress_request()
- BUG/MEDIUM: master/cli: Properly pin the master CLI on thread 1 / group 1
- BUG/MINOR: h3: fix TRAILERS encoding
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
- BUG/MEDIUM: peers: fix partial message decoding
- BUG/MINOR: cache: Remove incomplete entries from the cache when stream
  is closed
- BUG/MEDIUM: quic: Possible crash during retransmissions and heavy load
- BUG/MINOR: quic: Possible leak of TX packets under heavy load
- BUG/MINOR: quic: Missing QUIC connection path member initialization
- BUG/MINOR: quic: Packet number spaces too lately initialized
- BUG/MINOR: ssl: Double free of OCSP Certificate ID
- MINOR: ssl/cli: Add ha_(warning|alert) msgs to CLI ckch callback
- BUG/MINOR: ssl: Wrong OCSP CID after modifying an SSL certficate
- BUG/MINOR: lua: Wrong OCSP CID after modifying an SSL certficate (LUA)
- BUG/MEDIUM: proxy: always initialize the default settings after init

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.4-0
- BUILD: bug: make BUG_ON() void to avoid a rare warning
- BUG/MINOR: quic: Leak of frames to send.
- BUG/MINOR: quic: Wrong cluster secret initialization
- MINOR: quic: QUIC openssl wrapper implementation
- MINOR: quic: Include QUIC opensssl wrapper header from TLS stacks
  compatibility header
- MINOR: quic: Do not enable O-RTT with USE_QUIC_OPENSSL_COMPAT
- MINOR: quic: Set the QUIC connection as extra data before calling
  SSL_set_quic_method()
- MINOR: quic: Do not enable 0RTT with SSL_set_quic_early_data_enabled()
- MINOR: quic: Add a compilation option for the QUIC OpenSSL wrapper
- MINOR: quic: Export some KDF functions (QUIC-TLS)
- MINOR: quic: Initialize TLS contexts for QUIC openssl wrapper
- MINOR: quic: Call the keylog callback for QUIC openssl wrapper from
  SSL_CTX_keylog()
- MINOR: quic: Add a quic_openssl_compat struct to quic_conn struct
- MINOR: quic: SSL context initialization with QUIC OpenSSL wrapper.
- MINOR: quic: Add "limited-quic" new tuning setting
- DOC: quic: Add "limited-quic" new tuning setting
- BUG/MINOR: quic+openssl_compat: Non initialized TLS encryption levels
- MINOR: quic: Warning for OpenSSL wrapper QUIC bindings without "limited-quic"
- MINOR: quic+openssl_compat: Do not start without "limited-quic"
- MINOR: quic+openssl_compat: Emit an alert for "allow-0rtt" option
- BUILD: Makefile: add USE_QUIC_OPENSSL_COMPAT to make help
- BUG/MINOR: quic: allow-0rtt warning must only be emitted with quic bind
- BUG/MINOR: quic: ssl_quic_initial_ctx() uses error count not error code
- BUILD: quic: fix build on centos 8 and USE_QUIC_OPENSSL_COMPAT
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
- BUG/MEDIUM: master/cli: Pin the master CLI on the first thread of the group 1
- BUG/MINOR: freq_ctr: fix possible negative rate with the scaled API
- BUG/MAJOR: mux-h2: Report a protocol error for any DATA frame before headers
- BUG/MINOR: server: add missing free for server->rdr_pfx
- MINOR: pattern: fix pat_{parse,match}_ip() function comments
- BUG/MEDIUM: server/cli: don't delete a dynamic server that has streams
- BUG/MINOR: mux-quic: remove full demux flag on ncbuf release
- BUG/MEDIUM: actions: always apply a longest match on prefix lookup
- BUG/MEDIUM: quic_conn: let the scheduler kill the task when needed
- BUG/MEDIUM: http-ana: Try to handle response before handling server abort
- MINOR: hlua: Set context's appctx when the lua socket is created
- MINOR: hlua: Don't preform operations on a not connected socket
- MINOR: hlua: Save the lua socket's timeout in its context
- MINOR: hlua: Save the lua socket's server in its context
- MINOR: hlua: Test the hlua struct first when the lua socket is connecting
- BUG/MEDIUM: hlua: Initialize appctx used by a lua socket on connect only
- BUG/MINOR: mux-h1: Handle read0 in rcv_pipe() only when data receipt was tried
- BUG/MINOR: mux-h1: Ignore C-L when sending H1 messages if T-E is also set
- BUG/MEDIUM: h1: Ignore C-L value in the H1 parser if T-E is also set
- BUG/MINOR: hq-interop: simplify parser requirement
- BUG/MEDIUM: stconn: Fix comparison sign in sc_need_room()
- BUG/MINOR: quic: Avoid crashing with unsupported cryptographic algos
- BUG/MINOR: quic: reject packet with no frame
- BUG/MEDIUM: mux-quic: fix RESET_STREAM on send-only stream
- BUG/MINOR: mux-quic: support initial 0 max-stream-data
- BUG/MINOR: h3: strengthen host/authority header parsing
- BUG/MINOR: mux-quic: fix free on qcs-new fail alloc
- BUG/MEDIUM: quic-conn: free unsent frames on retransmit to prevent crash
- BUG/MINOR: mux-h1: Send a 400-bad-request on shutdown before the first request
- BUG/MINOR: mux-h2: make up other blocked streams upon removal from list
- BUG/MEDIUM: mux-h2: Don't report an error on shutr if a shutw is pending
- BUG/MINOR: mux-h2: fix http-request and http-keep-alive timeouts again
- BUG/MINOR: trace: fix trace parser error reporting
- BUG/MEDIUM: peers: Be sure to always refresh recconnect timer in sync task
- BUG/MEDIUM: peers: Fix synchro for huge number of tables
- BUG/MINOR: mux-h2: commit the current stream ID even on reject
- BUG/MINOR: mux-h2: update tracked counters with req cnt/req err
- DOC: internal: filters: fix reference to entities.pdf
- BUG/MINOR: ssl: load correctly @system-ca when ca-base is define
- MINOR: lua: Add flags to configure logging behaviour
- DEBUG: mux-h2/flags: fix list of h2c flags used by the flags decoder
- MINOR: connection: add conn_pr_mode_to_proto_mode() helper func
- BUG/MEDIUM: server: "proto" not working for dynamic servers
- BUG/MINOR: quic: do not consider idle timeout on CLOSING state
- BUG/MINOR: ssl: use a thread-safe sslconns increment
- MINOR: frontend: implement a dedicated actconn increment function
- MEDIUM: quic: count quic_conn instance for maxconn
- MEDIUM: quic: count quic_conn for global sslconns
- BUG/MINOR: ssl: suboptimal certificate selection with TLSv1.3 and dual
  ECDSA/RSA
- BUG/MINOR: mux-quic: fix early close if unset client timeout
- BUG/MEDIUM: ssl: segfault when cipher is NULL
- BUG/MINOR: tcpcheck: Report hexstring instead of binary one on check failure
- BUG/MINOR: stktable: missing free in parse_stick_table()
- BUG/MINOR: cfgparse/stktable: fix error message on stktable_init() failure
- BUG/MEDIUM: pattern: don't trim pools under lock in pat_ref_purge_range()
- BUG/MEDIUM: stconn: Don't report rcv/snd expiration date if SC cannot epxire
- BUG/MEDIUM: Don't apply a max value on room_needed in sc_need_room()
- BUG/MINOR: stconn: Sanitize report for read activity
- CLEANUP: htx: Properly indent htx_reserve_max_data() function
- BUG/MEDIUM: quic: fix actconn on quic_conn alloc failure
- BUG/MEDIUM: quic: fix sslconns on quic_conn alloc failure
- BUG/MINOR: stick-table/cli: Check for invalid ipv4 key
- BUG/MINOR: mux-h1: Properly handle http-request and http-keep-alive timeouts
- BUG/MEDIUM: freq-ctr: Don't report overshoot for long inactivity period
- BUG/MEDIUM: pool: fix releasable pool calculation when overloaded
- BUG/MINOR: quic: idle timer task requeued in the past
- BUG/MEDIUM: quic: Avoid trying to send ACK frames from an empty ack ranges
  tree
- BUG/MEDIUM: quic: Possible crashes when sending too short Initial packets
- BUG/MEDIUM: quic: Avoid some crashes upon TX packet allocation failures
- BUG/MEDIUM: stconn: Don't update stream expiration date if already expired
- DOC: management: -q is quiet all the time
- BUG/MINOR: quic: fix retry token check inconsistency
- DOC: config: use the word 'backend' instead of 'proxy' in 'track' description
- BUG/MEDIUM: applet: Remove appctx from buffer wait list on release
- BUG/MINOR: sink: don't learn srv port from srv addr
- DOC: quic: Wrong syntax for "quic-cc-algo" keyword.
- BUG/MEDIUM: connection: report connection errors even when no mux is installed
- BUG/MINOR: stconn: Handle abortonclose if backend connection was already
  set up
- MINOR: connection: Add a CTL flag to notify mux it should wait for reads again
- MEDIUM: mux-h1: Handle MUX_SUBS_RECV flag in h1_ctl() and susbscribe for reads
- BUG/MEDIUM: stream: Properly handle abortonclose when set on backend only
- REGTESTS: http: Improve script testing abortonclose option
- BUG/MEDIUM: stconn: Report a send activity everytime data were sent
- BUG/MEDIUM: applet: Report a send activity everytime data were sent
- BUG/MEDIUM: mworker: set the master variable earlier
- BUG/MEDIUM: stream: Don't call mux .ctl() callback if not implemented
- BUG/MEDIUM: stconn: Update fsb date on partial sends
- MINOR: htx: Use a macro for overhead induced by HTX
- MINOR: channel: Add functions to get info on buffers and deal with HTX streams
- BUG/MINOR: stconn: Fix streamer detection for HTX streams
- BUG/MINOR: stconn: Use HTX-aware channel's functions to get info on buffer
- BUG/MINOR: stconn/applet: Report send activity only if there was output data
- BUG/MINOR: stconn: Report read activity on non-indep streams for partial sends

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
