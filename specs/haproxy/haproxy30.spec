################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  3.0
%define comp_ver   30

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.7
%define pcre_ver      10.44
%define openssl_ver   3.2.3
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        3.0.5
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

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy28

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
* Sat Nov 02 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- BUG/MEDIUM: server/addr: fix tune.events.max-events-at-once event miss and
  leak
- BUG/MEDIUM: stconn: Report error on SC on send if a previous SE error was set
- BUG/MEDIUM: mux-pt/mux-h1: Release the pipe on connection error on sending
  path
- BUILD: mux-pt: Use the right name for the sedesc variable
- BUG/MINOR: stconn: bs.id and fs.id had their dependencies incorrect
- BUG/MEDIUM: ssl: reactivate 0-RTT for AWS-LC
- BUG/MEDIUM: ssl: 0-RTT initialized at the wrong place for AWS-LC
- BUG/MEDIUM: quic: prevent conn freeze on 0RTT undeciphered content
- BUG/MEDIUM: http-ana: Report error on write error waiting for the response
- BUG/MEDIUM: h2: Only report early HTX EOM for tunneled streams
- BUG/MEDIUM: mux-h2: Propagate term flags to SE on error in h2s_wake_one_stream
- BUG/MEDIUM: peer: Notify the applet won't consume data when it waits for sync
- BUG/MINOR: fcgi-app: handle a possible strdup() failure
- DOC: configuration: fix alphabetical ordering of {bs,fs}.aborted
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
- BUG/MINOR: pattern: pat_ref_set: fix UAF reported by coverity
- BUG/MINOR: pattern: pat_ref_set: return 0 if err was found
- DOC: config: correct the table for option tcplog
- BUG/MINOR: cfgparse-global: remove tune.fast-forward from common_kw_list
- BUILD: quic: 32bits build broken by wrong integer conversions for printf()
- BUG/MEDIUM: clock: also update the date offset on time jumps
- MINOR: tools: Implement ipaddrcpy().
- MINOR: quic: Implement quic_tls_derive_token_secret().
- MEDIUM: ssl/quic: implement quic crypto with EVP_AEAD
- MINOR: quic: Token for future connections implementation.
- BUG/MINOR: quic: Missing incrementation in NEW_TOKEN frame builder
- MINOR: quic: Modify NEW_TOKEN frame structure (qf_new_token struct)
- MINOR: quic: Implement qc_ssl_eary_data_accepted().
- MINOR: quic: Add trace for QUIC_EV_CONN_IO_CB event.
- BUG/MEDIUM: quic: always validate sender address on 0-RTT
- BUG/MINOR: quic: Crash from trace dumping SSL eary data status (AWS-LC)
- BUG/MINOR: quic: Too short datagram during packet building failures
  (aws-lc only)
- DOC: configuration: place the HAPROXY_HTTP_LOG_FMT example on the correct line
- REGTESTS: fix random failures with wrong_ip_port_logging.vtc under load
- BUG/MEDIUM: clock: detect and cover jumps during execution
- BUG/MINOR: pattern: prevent const sample from being tampered in
  pat_match_beg()
- BUG/MEDIUM: pattern: prevent UAF on reused pattern expr
- BUG/MAJOR: mux-h1: Wake SC to perform 0-copy forwarding in CLOSING state
- BUG/MINOR: h1-htx: Don't flag response as bodyless when a tunnel is
 established
- BUG/MINOR: pattern: do not leave a leading comma on "set" error messages
- MEDIUM: h1: Accept invalid T-E values with accept-invalid-http-response option
- BUG/MINOR: polling: fix time reporting when using busy polling
- BUG/MINOR: clock: make time jump corrections a bit more accurate
- BUG/MINOR: clock: validate that now_offset still applies to the current date
- BUG/MEDIUM: queue: implement a flag to check for the dequeuing
- BUG/MINOR: peers: local entries updates may not be advertised after resync
- DOC: config: Explicitly list relaxing rules for accept-invalid-http-* options
- BUG/MEDIUM: sc_strm/applet: Wake applet after a successfull synchronous send
- BUG/MEDIUM: cache/stats: Wait to have the request before sending the response
- BUG/MEDIUM: promex: Wait to have the request before sending the response
- BUG/MINOR: cfgparse-listen: fix option httpslog override warning message
- MINOR: quic: convert qc_stream_desc release field to flags
- MINOR: quic: implement function to check if STREAM is fully acked
- BUG/MEDIUM: quic: handle retransmit for standalone FIN STREAM
- BUG/MINOR: quic: prevent freeze after early QCS closure

* Sat Nov 02 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.4-0
- MINOR: proto: extend connection thread rebind API
- BUILD: listener: silence a build warning about unused value without threads
- BUG/MEDIUM: quic: prevent crash on accept queue full
- CLEANUP: proto: rename TID affinity callbacks
- CLEANUP: quic: rename TID affinity elements
- BUG/MINOR: session: Eval L4/L5 rules defined in the default section
- BUG/MEDIUM: debug/cli: fix "show threads" crashing with low thread counts
- DOC: install: don't reference removed CPU arg
- BUG/MEDIUM: ssl_sock: fix deadlock in ssl_sock_load_ocsp() on error path
- BUG/MAJOR: mux-h2: force a hard error upon short read with pending error
- DOC: configuration: issuers-chain-path not compatible with OCSP
- DOC: config: improve the http-keep-alive section
- BUG/MINOR: stick-table: fix crash for src_inc_gpc() without stkcounter
- BUG/MINOR: server: Don't warn fallback IP is used during init-addr resolution
- BUG/MINOR: cli: Atomically inc the global request counter between CLI commands
- BUG/MINOR: quic: Non optimal first datagram.
- MEDIUM: sink: don't set NOLINGER flag on the outgoing stream interface
- BUG/MINOR: quic: Lack of precision when computing K (cubic only cc)
- BUG/MEDIUM: jwt: Clear SSL error queue on error when checking the signature
- MINOR: quic: Dump TX in flight bytes vs window values ratio.
- MINOR: quic: Add information to "show quic" for CUBIC cc.
- MEDIUM: h1: allow to preserve keep-alive on T-E + C-L
- MINOR: queue: add a function to check for TOCTOU after queueing
- BUG/MEDIUM: queue: deal with a rare TOCTOU in assign_server_and_queue()
- MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD (take #2)
- BUG/MEDIUM: init: fix fd_hard_limit default in compute_ideal_maxconn
- Revert "MEDIUM: sink: don't set NOLINGER flag on the outgoing stream
  interface"
- MEDIUM: log: relax some checks and emit diag warnings instead in
  lf_expr_postcheck()
- DOC: quic: fix default minimal value for max window size
- MINOR: proxy: Add support of 429-Too-Many-Requests in retry-on status
- BUG/MEDIUM: mux-h2: Set ES flag when necessary on 0-copy data forwarding
- BUG/MEDIUM: stream: Prevent mux upgrades if client connection is no longer
  ready
- BUG/MINIR: proxy: Match on 429 status when trying to perform a L7 retry
- BUG/MEDIUM: mux-pt: Never fully close the connection on shutdown
- BUG/MEDIUM: cli: Always release back endpoint between two commands on the mcli
- BUG/MINOR: quic: unexploited retransmission cases for Initial pktns.
- BUG/MEDIUM: mux-h1: Properly handle empty message when an error is triggered
- MINOR: mux-h2: try to clear DEM_MROOM and MUX_MFULL at more places
- BUG/MAJOR: mux-h2: always clear MUX_MFULL and DEM_MROOM when clearing the mbuf
- BUG/MINOR: quic: Too shord datagram during O-RTT handshakes (aws-lc only)
- BUG/MINOR: Crash on O-RTT RX packet after dropping Initial pktns
- BUG/MEDIUM: mux-pt: Fix condition to perform a shutdown for writes in
  mux_pt_shut()

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- BUG/MINOR: log: fix broken '+bin' logformat node option
- DEBUG: hlua: distinguish burst timeout errors from exec timeout errors
- REGTESTS: ssl: fix some regtests 'feature cmd' start condition
- BUG/MEDIUM: proxy: fix email-alert invalid free
- DOC: configuration: fix alphabetical order of bind options
- DOC: management: document ptr lookup for table commands
- BUG/MAJOR: quic: fix padding with short packets
- SCRIPTS: git-show-backports: do not truncate git-show output
- DOC: api/event_hdl: small updates, fix an example and add some precisions
- BUG/MINOR: h3: fix crash on STOP_SENDING receive after GOAWAY emission
- BUG/MINOR: mux-quic: fix crash on qcs SD alloc failure
- BUG/MINOR: h3: fix BUG_ON() crash on control stream alloc failure
- BUG/MINOR: quic: fix BUG_ON() on Tx pkt alloc failure
- DEV: flags/show-fd-to-flags: adapt to recent versions
- BUG/MINOR: hlua: report proper context upon error in hlua_cli_io_handler_fct()
- BUG/MEDIUM: stick-table: Decrement the ref count inside lock to kill a session
- DOC: configuration: add details about crt-store in bind "crt" keyword
- BUG/MINOR: server: fix first server template name lookup UAF
- MINOR: activity: make the memory profiling hash size configurable at build
  time
- BUG/MEDIUM: server/dns: prevent DOWN/UP flap upon resolution timeout or error
- BUG/MEDIUM: h3: ensure the ":method" pseudo header is totally valid
- BUG/MEDIUM: h3: ensure the ":scheme" pseudo header is totally valid
- BUG/MEDIUM: quic: fix race-condition in quic_get_cid_tid()
- BUG/MINOR: quic: fix race condition in qc_check_dcid()
- BUG/MINOR: quic: fix race-condition on trace for CID retrieval
- BUG/MEDIUM: quic: fix possible exit from qc_check_dcid() without unlocking
- BUG/MINOR: promex: Remove Help prefix repeated twice for each metric
- BUG/MEDIUM: hlua/cli: Fix lua CLI commands to work with applet's buffers
- DOC: configuration: more details about the master-worker mode
- BUG/MEDIUM: server: fix race on server_atomic_sync()
- BUG/MINOR: jwt: don't try to load files with HMAC algorithm
- MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD
- DOC: configuration: update maxconn description
- BUG/MEDIUM: peers: Fix crash when syncing learn state of a peer without appctx
- Revert "MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD"
- BUG/MINOR: jwt: fix variable initialisation
- BUG/MINOR: h1: Fail to parse empty transfer coding names
- BUG/MINOR: h1: Reject empty coding name as last transfer-encoding value
- BUG/MEDIUM: h1: Reject empty Transfer-encoding header
- BUG/MEDIUM: spoe: Be sure to create a SPOE applet if none on the current
  thread
- DEV: flags/quic: decode quic_conn flags
- BUG/MEDIUM: bwlim: Be sure to never set the analyze expiration date in past

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- MINOR: log: fix "http-send-name-header" ignore warning message
- BUG/MINOR: proxy: fix server_id_hdr_name leak on deinit()
- BUG/MINOR: proxy: fix log_tag leak on deinit()
- BUG/MINOR: proxy: fix email-alert leak on deinit()
- BUG/MINOR: proxy: fix check_{command,path} leak on deinit()
- BUG/MINOR: proxy: fix dyncookie_key leak on deinit()
- BUG/MINOR: proxy: fix source interface and usesrc leaks on deinit()
- BUG/MINOR: proxy: fix header_unique_id leak on deinit()
- BUG/MEDIUM: log: fix lf_expr_postcheck() behavior with default section
- DOC: config: move "hash-key" from proxy to server options
- DOC: config: add missing section hint for "guid" proxy keyword
- DOC: config: add missing context hint for new server and proxy keywords
- BUG/MINOR: promex: Skip resolvers metrics when there is no resolver section
- MINOR: proxy: add proxy_free_common() helper function
- BUG/MEDIUM: proxy: fix UAF with {tcp,http}checks logformat expressions
- CLEANUP: log/proxy: fix comment in proxy_free_common()
- BUG/MAJOR: mux-h1: Prevent any UAF on H1 connection after draining a request
- BUG/MINOR: quic: fix padding of INITIAL packets
- DOC/MINOR: management: add missed -dR and -dv options
- DOC/MINOR: management: add -dZ option
- DOC: management: rename show stats domain cli "dns" to "resolvers"

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- BUG/MINOR: cfgparse: remove the correct option on httpcheck send-state warning
- BUG/MINOR: tcpcheck: report correct error in tcp-check rule parser
- BUG/MINOR: tools: fix possible null-deref in env_expand() on out-of-memory
- DOC: configuration: add an example for keywords from crt-store
- BUG/MINOR: hlua: use CertCache.set() from various hlua contexts
- BUG/MEDIUM: h1-htx: Don't state interim responses are bodyless
- MEDIUM: stconn: Be able to unblock zero-copy data forwarding from done_fastfwd
- BUG/MEDIUM: mux-quic: Unblock zero-copy forwarding if the txbuf can be
  released
- BUG/MINOR: quic: prevent crash on qc_kill_conn()
- CLEANUP: hlua: use hlua_pusherror() where relevant
- BUG/MINOR: hlua: don't use lua_pushfstring() when we don't expect LJMP
- BUG/MINOR: hlua: fix unsafe hlua_pusherror() usage
- BUG/MINOR: hlua: prevent LJMP in hlua_traceback()
- BUG/MINOR: hlua: fix leak in hlua_ckch_set() error path
- CLEANUP: hlua: simplify ambiguous lua_insert() usage in hlua_ctx_resume()
- BUG/MEDIUM: mux-quic: Don't unblock zero-copy fwding if blocked during nego
- BUG/MEDIUM: ssl: wrong priority whem limiting ECDSA ciphers in ECDSA+RSA
  configuration
- BUG/MEDIUM: ssl: bad auth selection with TLS1.2 and WolfSSL
- BUG/MINOR: quic: fix computed length of emitted STREAM frames
- BUG/MINOR: quic: ensure Tx buf is always purged
- BUG/MEDIUM: stconn/mux-h1: Fix suspect change causing timeouts
- BUG/MAJOR: mux-h1:  Properly copy chunked input data during zero-copy nego
- BUG/MINOR: mux-h1: Use the right variable to set NEGO_FF_FL_EXACT_SIZE flag

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- Initial build for kaos repository
