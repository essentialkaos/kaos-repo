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

%define lua_ver       5.4.7
%define pcre_ver      10.45
%define openssl_ver   3.0.16
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.6.22
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

Conflicts:      haproxy haproxy22 haproxy24 haproxy28 haproxy30

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
* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 2.6.22-0
- BUG/MEDIUM: ssl: chosing correct certificate using RSA-PSS with TLSv1.3
- BUG/MINOR: ssl_sock: fix xprt_set_used() to properly clear the TASK_F_USR1
  bit
- BUG/MINOR: h1: do not forward h2c upgrade header token
- BUG/MINOR: h2: reject extended connect for h2c protocol
- MINOR: mux-h1: Set EOI on SE during demux when both side are in DONE state
- BUG/MEDIUM: mux-h1/mux-h2: Reject upgrades with payload on H2 side only
- REGTESTS: h1/h2: Update script testing H1/H2 protocol upgrades
- REGTESTS: shorten a bit the delay for the h1/h2 upgrade test
- BUG/MINOR: http-ana: Disable fast-fwd for unfinished req waiting for upgrade
- BUG/MINOR: spoe: Check the shared waiting queue to shut applets during
  stopping
- BUG/MINOR: spoe: Allow applet creation when closing the last one during
  stopping
- BUG/MEDIUM: spoe: Don't wakeup idle applets in loop during stopping
- BUG/MEDIUM: clock: make sure now_ms cannot be TICK_ETERNITY
- BUG/MEDIUM: fd: mark FD transferred to another process as FD_CLONED
- REGTESTS: Fix truncated.vtc to send 0-CRLF
- BUG/MEDIUM: htx: wrong count computation in htx_xfer_blks()
- DOC: htx: clarify <mark> parameter for htx_xfer_blks()
- DOC: option redispatch should mention persist options
- TESTS: ist: fix wrong array size
- BUG/MEDIUM: thread: use pthread_self() not ha_pthread[tid] in set_affinity
- DOC: management: rename some last occurences from domain "dns" to "resolvers"
- BUG/MINOR: server: fix the "server-template" prefix memory leak
- BUG/MINOR: quic: reserve length field for long header encoding
- BUG/MINOR: quic: fix CRYPTO payload size calcul for encoding
- BUG/MINOR: cli: Wait for the last ACK when FDs are xferred from the old
  worker
- BUG/MEDIUM: filters: Handle filters registered on data with no payload
  callback
- BUG/MINOR: fcgi: Don't set the status to 302 if it is already set
- BUG/MINOR: quic: prevent crash on conn access after MUX init failure
- BUG/MINOR: tcp-rules: Don't forward close during tcp-response content rules
  eval
- BUG/MINOR: cli: Fix memory leak on error for _getsocks command
- BUG/MINOR: cli: Fix a possible infinite loop in _getsocks()
- BUG/MINOR: config/userlist: Support one 'users' option for 'group' directive
- BUG/MINOR: auth: Fix a leak on error path when parsing user's groups
- BUG/MINOR: flt-trace: Support only one name option
- BUG/MINOR: stats-json: Define JSON_INT_MAX as a signed integer
- BUG/MINOR: cfgparse: fix NULL ptr dereference in cfg_parse_peers
- BUG/MINOR: sink: add tempo between 2 connection attempts for sft servers
- BUG/MINOR: h2: always trim leading and trailing LWS in header values
- CLEANUP: h3: fix documentation of h3_rcv_buf()
- BUG/MINOR: server: check for either proxy-protocol v1 or v2 to send hedaer
- BUG/MEIDUM: startup: return to initial cwd only after check_config_validity()
- BUG/MINOR: cfgparse/peers: fix inconsistent check for missing peer server
- BUG/MINOR: cfgparse/peers: properly handle ignored local peer case
- BUG/MINOR: server: dont return immediately from parse_server() when skipping
  checks
- MINOR: cfgparse/peers: provide more info when ignoring invalid "peer"
  or "server" lines
- BUG/MINOR: namespace: handle a possible strdup() failure
- BUG/MEDIUM: hlua/cli: fix cli applet UAF in hlua_applet_wakeup()
- MINOR: cli: export cli_io_handler() to ease symbol resolution
- BUG/MINOR: peers: fix expire learned from a peer not converted from ms to
  ticks
- BUG/MEDIUM: peers: prevent learning expiration too far in futur from unsync
  node
- BUG/MINOR: log: fix gcc warn about truncating NUL terminator while init char
  arrays
- DOC: config: fix two missing "content" in "tcp-request" examples
- BUG/MINOR: backend: do not overwrite srv dst address on reuse
- BUG/MEDIUM: backend: fix reuse with set-dst/set-dst-port
- TESTS: Fix build for filltab25.c
- BUG/MEDIUM: sample: fix risk of overflow when replacing multiple regex
  back-refs
- BUG/MINOR: backend: do not use the source port when hashing clientip
- BUG/MINOR: hlua: fix invalid errmsg use in hlua_init()
- DOC: config: add the missing "profiling.memory" to the global kw index
- BUG/MINOR: sink: add tempo between 2 connection attempts for sft servers (2)
- MINOR: h3: check return values of htx_add_* on headers parsing
- BUG/MEDIUM: h3: trim whitespaces when parsing headers value
- BUG/MEDIUM: h3: trim whitespaces in header value prior to QPACK encoding
- BUG/MINOR: h3: filter upgrade connection header
- BUG/MINOR: h3: reject invalid :path in request
- BUG/MINOR: h3: reject request URI with invalid characters
- BUG/MINOR: quic: do not crash on CRYPTO ncbuf alloc failure
- BUG/MINOR: mux-h2: prevent past scheduling with idle connections
- BUG/MINOR: mux-quic: fix BUG_ON() crash on init failure after app-ops

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.6.21-0
- MEDIUM: h1: Accept invalid T-E values with accept-invalid-http-response option
- BUG/MEDIUM: mux-pt: Never fully close the connection on shutdown
- MINOR: task: define two new one-shot events for use with WOKEN_OTHER or MSG
- BUG/MEDIUM: stream: make stream_shutdown() async-safe
- BUG/MEDIUM: queue: always dequeue the backend when redistributing the last
  server
- BUG/MEDIUM: queue: make sure never to queue when there's no more served conns
- BUG/MINOR: cli: don't show sockpairs in HAPROXY_CLI and HAPROXY_MASTER_CLI
- BUG/MEDIUM: resolvers: Insert a non-executed resulution in front of the wait
  list
- BUG/MEDIUM: mux-h2: Don't send RST_STREAM frame for streams with no ID
- BUG/MEDIUM: checks: make sure to always apply offsets to now_ms in expiration
- BUG/MEDIUM: mailers: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: peers: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: http_ana: Report -1 for %%Tr for invalid response only
- DOC: config: Slightly improve the %%Tr documentation
- DOC: lua: fix yield-dependent methods expected contexts
- DOC: configuration: explain quotes and spaces in conditional blocks
- BUG/MINOR: http-ana: Adjust the server status before the L7 retries
- BUG/MEDIUM: mux-h2: Increase max number of headers when encoding HEADERS
  frames
- BUG/MEDIUM: mux-h2: Check the number of headers in HEADERS frame after
  decoding
- BUG/MEDIUM: h3: Properly limit the number of headers received
- BUG/MEDIUM: h3: Increase max number of headers when sending headers
- BUG/MAJOR: quic: fix wrong packet building due to already acked frames
- BUG/MEDIUM: http-ana: Don't release too early the L7 buffer
- BUG/MEDIUM: sock: Remove FD_POLL_HUP during connect() if FD_POLL_ERR is
  not set
- BUG/MEDIUM: http-ana: Reset request flag about data sent to perform a L7 retry
- BUG/MINOR: h1-htx: Use default reason if not set when formatting the response
- BUG/MINOR: signal: register default handler for SIGINT in signal_init()
- BUG/MINOR: server-state: Fix expiration date of srvrq_check tasks
- BUG/MEDIUM: mux-h1: Fix how timeouts are applied on H1 connections
- BUG/MEDIUM: pattern: prevent uninitialized reads in pat_match_{str,beg}
- MINOR: quic: notify connection layer on handshake completion
- BUG/MINOR: stream: unblock stream on wait-for-handshake completion
- BUG/MEDIUM: stconn: Don't forward shut for SC in connecting state
- BUG/MEDIUM: queues: Make sure we call process_srv_queue() when leaving
- BUG/MEDIUM: queues: Do not use pendconn_grab_from_px().
- BUG/MEDIUM: queue: Make process_srv_queue return the number of streams
- MINOR: config: Alert about extra arguments for errorfile and errorloc
- BUG/MINOR: stktable: fix big-endian compatiblity in smp_to_stkey()
- BUG/MINOR: quic: reject NEW_TOKEN frames from clients
- BUG/MEDIUM: stktable: fix missing lock on some table converters
- BUG/MAJOR: quic: reject too large CRYPTO frames
- BUG/MINOR: quic: ensure a detached coalesced packet can't access its
  neighbours
- MINOR: quic: Add a BUG_ON() on quic_tx_packet refcount
- BUILD: quic: Move an ASSUME_NONNULL() for variable which is not null
- BUG/MINOR: quic: do not increase congestion window if app limited
- BUG/MINOR: ssl: put ssl_sock_load_ca under SSL_NO_GENERATE_CERTIFICATES
- BUG/MINOR: stream: Properly handle "on-marked-up shutdown-backup-sessions"

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.6.20-0
- BUG/MEDIUM: cli: Deadlock when setting frontend maxconn
- BUG/MINOR: cfgparse-global: fix allowed args number for setenv
- BUG/MEDIUM: server: server stuck in maintenance after FQDN change
- BUG/MEDIUM: hlua: make hlua_ctx_renew() safe
- BUG/MEDIUM: hlua: properly handle sample func errors in
  hlua_run_sample_{fetch,conv}()
- BUG/MINOR: http-ana: Don't report a server abort if response payload is
  invalid
- BUG/MINOR: mworker: fix mworker-max-reloads parser
- BUG/MEDIUM: connection/http-reuse: fix address collision on unhandled address
  families
- BUG/MINOR: server: fix dynamic server leak with check on failed init
- BUG/MEDIUM: server: fix race on servers_list during server deletion
- BUG/MINOR: ssl/cli: 'set ssl cert' does not check the transaction name
  correctly
- BUG/MINOR: http-ana: Report internal error if an action yields on a final eval
- MINOR: stream: Save last evaluated rule on invalid yield
- CLEANUP: connection: properly name the CO_ER_SSL_FATAL enum entry

* Fri Nov 01 2024 Anton Novojilov <andy@essentialkaos.com> - 2.6.19-0
- BUG/MEDIUM: cli: fix cli_output_msg() regression
- BUG/MINOR: quic: fix computed length of emitted STREAM frames
- DOC/MINOR: management: add missed -dR and -dv options
- DOC: management: rename show stats domain cli "dns" to "resolvers"
- DOC: configuration: fix alphabetical order of bind options
- SCRIPTS: git-show-backports: do not truncate git-show output
- BUG/MINOR: mux-quic: fix crash on qcs SD alloc failure
- BUG/MINOR: quic: fix BUG_ON() on Tx pkt alloc failure
- BUG/MINOR: hlua: report proper context upon error in hlua_cli_io_handler_fct()
- BUG/MEDIUM: h3: ensure the ":method" pseudo header is totally valid
- BUG/MEDIUM: h3: ensure the ":scheme" pseudo header is totally valid
- DOC: configuration: more details about the master-worker mode
- MEDIUM: ssl: initialize the SSL stack explicitely
- MINOR: mux-h2/traces: explicitly show the error/refused stream states
- REGTESTS: add a test to ensure map-ordering is preserved
- MINOR: quic: Add packet loss and maximum cc window to "show quic"
- MINOR: quic: Add a counter for reordered packets
- BUG/MINOR: quic: Lack of precision when computing K (cubic only cc)
- BUG/MINOR: jwt: don't try to load files with HMAC algorithm
- BUG/MINOR: jwt: fix variable initialisation
- BUG/MEDIUM: jwt: Clear SSL error queue on error when checking the signature
- BUG/MINOR: h1: Fail to parse empty transfer coding names
- BUG/MINOR: h1: Reject empty coding name as last transfer-encoding value
- BUG/MEDIUM: h1: Reject empty Transfer-encoding header
- BUG/MEDIUM: spoe: Be sure to create a SPOE applet if none on the current
  thread
- BUG/MINOR: stick-table: fix crash for src_inc_gpc() without stkcounter
- BUG/MINOR: server: Don't warn fallback IP is used during init-addr resolution
- BUG/MINOR: cli: Atomically inc the global request counter between CLI commands
- MINOR: queue: add a function to check for TOCTOU after queueing
- BUG/MEDIUM: queue: deal with a rare TOCTOU in assign_server_and_queue()
- MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD (take #2)
- BUG/MEDIUM: init: fix fd_hard_limit default in compute_ideal_maxconn
- DOC: configuration: update maxconn description
- DOC: configuration: issuers-chain-path not compatible with OCSP
- DOC: config: improve the http-keep-alive section
- BUG/MEDIUM: stream: Prevent mux upgrades if client connection is no longer
  ready
- BUG/MEDIUM: cli: Always release back endpoint between two commands on the mcli
- BUG/MEDIUM: quic: prevent conn freeze on 0RTT undeciphered content
- BUG/MEDIUM: h2: Only report early HTX EOM for tunneled streams
- BUG/MINOR: fcgi-app: handle a possible strdup() failure
- BUG/MINOR: trace/quic: enable conn/session pointer recovery from quic_conn
- CLEANUP: trace: remove the QUIC-specific ifdefs
- BUG/MINOR: trace/quic: permit to lock on frontend/connect/session etc
- BUG/MINOR: trace: automatically start in waiting mode with "start <evt>"
- BUG/MINOR: trace/quic: make "qconn" selectable as a lockon criterion
- BUG/MINOR: quic/trace: make quic_conn_enc_level_init() emit NEW not CLOSE
- BUG/MINOR: proto_tcp: delete fd from fdtab if listen() fails
- BUG/MINOR: proto_tcp: keep error msg if listen() fails
- REGTESTS: mcli: test the pipelined commands on master CLI
- BUG/MINOR: mux-quic: do not send too big MAX_STREAMS ID
- BUG/MINOR: proto_uxst: delete fd from fdtab if listen() fails
- BUG/MINOR: h3: properly reject too long header responses
- DOC: config: correct the table for option tcplog
- BUG/MINOR: pattern: pat_ref_set: fix UAF reported by coverity
- BUG/MINOR: pattern: pat_ref_set: return 0 if err was found
- BUG/MINOR: pattern: do not leave a leading comma on "set" error messages
- REGTESTS: fix random failures with wrong_ip_port_logging.vtc under load
- BUG/MINOR: pattern: prevent const sample from being tampered in
  pat_match_beg()
- BUG/MEDIUM: pattern: prevent UAF on reused pattern expr
- BUG/MINOR: polling: fix time reporting when using busy polling
- BUG/MEDIUM: queue: implement a flag to check for the dequeuing
- BUG/MEDIUM: cache/stats: Wait to have the request before sending the response
- BUG/MEDIUM: promex: Wait to have the request before sending the response
- BUG/MINOR: cfgparse-listen: fix option httpslog override warning message

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.6.18-0
- BUG/MEDIUM: cli: fix once for all the problem of missing trailing LFs
- BUG/MEDIUM: mux-quic: report early error on stream
- BUG/MEDIUM: quic: remove unsent data from qc_stream_desc buf
- MINOR: ext-check: add an option to preserve environment variables
- BUG/MINOR: ext-check: cannot use without preserve-env
- MINOR: server: allow cookie for dynamic servers
- MINOR: cli: Remove useless loop on commands to find unescaped semi-colon
- BUG/MEDIUM: cli: Warn if pipelined commands are delimited by a \n
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
- BUG/MINOR: connection: parse PROXY TLV for LOCAL mode
- BUG/MAJOR: quic: Crash with TLS_AES_128_CCM_SHA256 (libressl only)
- BUG/MEDIUM: quic_tls: prevent LibreSSL < 4.0 from negotiating
  CHACHA20_POLY1305
- BUG/MEDIUM: mux-quic: Create sedesc in same time of the QUIC stream
- MEDIUM: config: prevent communication with privileged ports
- BUG/MINOR: quic: adjust restriction for stateless reset emission
- BUG/MINOR: http-htx: Support default path during scheme based normalization
- BUG/MINOR: server: Don't reset resolver options on a new default-server line
- DOC: quic: specify that connection migration is not supported
- DOC: config: fix incorrect section reference about custom log format
- REGTESTS: acl_cli_spaces: avoid a warning caused by undefined logs
- CI: scripts: fix build of vtest regarding option -C
- BUILD: fd: errno is also needed without poll()
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
- MINOR: hlua: don't dump empty entries in hlua_traceback()
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
- BUG/MINOR: haproxy: only tid 0 must not sleep if got signal

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.6.17-0
- BUG/MEDIUM: connection: report connection errors even when no mux is installed
- BUG/MEDIUM: mworker: set the master variable earlier
- BUG/MEDIUM: proxy: always initialize the default settings after init
- DOC: configuration: typo req.ssl_hello_type
- BUG/MINOR: mworker/cli: fix set severity-output support
- BUG/MEDIUM: mux-h2: Report too large HEADERS frame only when rxbuf is empty
- BUG/MINOR: resolvers: default resolvers fails when network not configured
- DOC: config: Update documentation about local haproxy response
- MINOR: stats: store the parent proxy in stats ctx (http)
- BUG/MEDIUM: stats: unhandled switching rules with TCP frontend
- MINOR: h3: check connection error during sending
- BUG/MINOR: h3: close connection on header list too big
- BUG/MINOR: h3: properly handle alloc failure on finalize
- BUG/MINOR: h3: close connection on sending alloc errors
- CLEANUP: quic: Remaining useless code into server part
- BUG/MEDIUM: h3: fix incorrect snd_buf return value
- BUG/MEDIUM: stconn: Forward shutdown on write timeout only if it is
  forwardable
- BUG/MEDIUM: spoe: Never create new spoe applet if there is no server up
- BUG/MEDIUM: h3: fix regression which completely prevents any send
- BUG/MINOR: mux-quic: do not prevent non-STREAM sending on flow control
- MINOR: compiler: add a new DO_NOT_FOLD() macro to prevent code folding
- MINOR: debug: make sure calls to ha_crash_now() are never merged
- MINOR: debug: make ABORT_NOW() store the caller's line number when using abort
- MINOR: debug: make BUG_ON() catch build errors even without DEBUG_STRICT
- BUG/MEDIUM: cli: some err/warn msg dumps add LR into CSV output on stat's CLI
- BUG/MINOR: vars/cli: fix missing LF after "get var" output
- BUG/MINOR: jwt: fix jwt_verify crash on 32-bit archs
- BUG/MEDIUM: pool: fix rare risk of deadlock in pool_flush()
- BUG/MINOR: h1-htx: properly initialize the err_pos field
- BUG/MINOR: h1: Don't support LF only at the end of chunks
- BUG/MEDIUM: h1: Don't support LF only to mark the end of a chunk size
- BUG/MEDIUM: h1: always reject the NUL character in header values
- BUG/MAJOR: ssl_sock: Always clear retry flags in read/write functions
- BUG/MINOR: ssl: Clear the ckch instance when deleting a crt-list line
- REGTESTS: ssl: Fix empty line in cli command input
- BUG/MINOR: h3: fix checking on NULL Tx buffer
- CLEANUP: quic: Remove unused CUBIC_BETA_SCALE_FACTOR_SHIFT macro.
- MINOR: quic: Stop hardcoding a scale shifting value
  (CUBIC_BETA_SCALE_FACTOR_SHIFT)
- MINOR: quic: extract qc_stream_buf free in a dedicated function
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
- BUG/MINOR: diag: run the final diags before quitting when using -c
- BUILD: address a few remaining calloc(size, n) cases
- DOC: configuration: clarify http-request wait-for-body
- DOC: httpclient: add dedicated httpclient section
- DOC: install: recommend pcre2
- DOC: internal: update missing data types in peers-v2.0.txt
- CI: Update to actions/cache@v4
- DEV: makefile: add a new "range" target to iteratively build all commits
- DEV: makefile: fix POSIX compatibility for "range" target
- BUG/MAJOR: promex: fix crash on deleted server
- BUG/MINOR: quic: reject unknown frame type
- BUG/MINOR: quic: reject HANDSHAKE_DONE as server
- BUG/MINOR: qpack: reject invalid increment count decoding
- BUG/MINOR: qpack: reject invalid dynamic table capacity
- BUG/MEDIUM: applet: Immediately free appctx on early error
- BUG/MEDIUM: hlua: Be able to garbage collect uninitialized lua sockets
- BUG/MEDIUM: hlua: Don't loop if a lua socket does not consume received data
- MINOR: quic: warn on bind on multiple addresses if no IP_PKTINFO support
- BUG/MINOR: ist: allocate nul byte on istdup
- BUG/MINOR: stats: drop srv refcount on early release
- BUG/MAJOR: server: fix stream crash due to deleted server
- BUG/MINOR: ist: only store NUL byte on succeeded alloc
- BUG/MINOR: ssl/cli: duplicate cleaning code in cli_parse_del_crtlist
- DOC: configuration: clarify ciphersuites usage
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
- BUG/MINOR: ssl/cli: typo in new ssl crl-file CLI description
- BUG/MINOR: cfgparse: report proper location for log-format-sd errors
- DOC: configuration: clarify ciphersuites usage (V2)
- BUG/MINOR: ssl: fix possible ctx memory leak in sample_conv_aes_gcm()
- BUG/MINOR: hlua: segfault when loading the same filter from different contexts
- BUG/MINOR: hlua: missing lock in hlua_filter_new()
- BUG/MINOR: hlua: fix missing lock in hlua_filter_delete()
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
- BUG/MINOR: mux-quic: close all QCS before freeing QCC tasklet
- BUG/MEDIUM: mux-fcgi: Properly handle EOM flag on end-of-trailers HTX block
- BUG/MINOR: server: 'source' interface ignored from 'default-server' directive
- BUG/MINOR: server: ignore 'enabled' for dynamic servers
- BUG/MINOR: backend: properly handle redispatch 0
- DOC: config: Remove httpclient.timeout.connect parameter
- DEBUG: lua: precisely identify if stream is stuck inside lua or not
- MINOR: hlua: use accessors for stream hlua ctx
- BUG/MEDIUM: hlua: streams don't support mixing lua-load with
  lua-load-per-thread (2nd try)
- BUG/MINOR: proxy: fix logformat expression leak in use_backend rules

* Thu Mar 21 2024 Anton Novojilov <andy@essentialkaos.com> - 2.6.16-1
- OpenSSL updated to 3.0.13
- PCRE2 updated to 10.43

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
