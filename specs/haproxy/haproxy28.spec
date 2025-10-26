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

%define lua_ver       5.4.8
%define pcre_ver      10.47
%define openssl_ver   3.2.6
%define ncurses_ver   6.5
%define readline_ver  8.3

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.8.16
Release:        0%{?dist}
License:        GPLv2+
URL:            https://www.haproxy.org
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

BuildRequires:  make gcc-c++ systemd-devel perl perl-IPC-Cmd

%if 0%{?rhel} == 10
BuildRequires:  zlib-ng-compat-devel
%else
BuildRequires:  zlib-devel
%endif

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy30 haproxy32

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
  ./config --prefix=$(pwd)/build no-shared no-threads no-tests
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
* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 2.8.16-0
- BUG/MINOR: cli: Issue an error when too many args are passed for a command
- BUG/MAJOR: listeners: transfer connection accounting when switching
  listeners
- MINOR: applet: add appctx_schedule() macro
- BUG/MINOR: dns: add tempo between 2 connection attempts for dns servers
- CLEANUP: dns: remove unused dns_stream_server struct member
- BUG/MINOR: dns: prevent ds accumulation within dss
- BUG/MINOR: mux-h1: Don't pretend connection was released for TCP>H1>H2
  upgrade
- BUG/MINOR: mux-h1: Fix trace message in h1_detroy() to not relay on
  connection
- BUG/MINOR: proxy: only use proxy_inc_fe_cum_sess_ver_ctr() with frontends
- MINOR: quic: extend return value during TP parsing
- BUG/MINOR: quic: use proper error code on missing CID in TPs
- BUG/MINOR: quic: use proper error code on invalid server TP
- BUG/MINOR: quic: reject retry_source_cid TP on server side
- BUG/MINOR: quic: use proper error code on invalid received TP value
- BUG/MINOR: quic: fix TP reject on invalid max-ack-delay
- BUG/MINOR: quic: reject invalid max_udp_payload size
- BUG/MINOR: cli: fix too many args detection for commands
- BUG/MINOR: threads: fix soft-stop without multithreading support
- BUG/MINOR: hlua: Fix Channel:data() and Channel:line() to respect
  documentation
- BUG/MINOR: sink: detect and warn when using "send-proxy" options with ring
  servers
- DOC: ring: refer to newer RFC5424
- DOC: config: restore default values for resolvers hold directive
- DOC: config: recommend disabling libc-based resolution with resolvers
- BUG/MINOR: h3: don't insert more than one Host header
- CLEANUP: quic: Useless BIO_METHOD initialization
- MINOR: quic: Add useful error traces about qc_ssl_sess_init() failures
- MEDIUM: hlua: Add function to change the body length of an HTTP Message
- BUG/MINOR: mux-h2: Reset streams with NO_ERROR code if full response was
  already sent
- BUILD: makefile: enable backtrace by default on musl
- BUG/MINOR: h3: Set HTX flags corresponding to the scheme found in the
  request
- REGTESTS: Make the script testing conditional set-var compatible with
  Vtest2
- CI: vtest: Rely on VTest2 to run regression tests
- REGTESTS: Explicitly allow failing shell commands in some scripts
- BUG/MINOR: limits: compute_ideal_maxconn: don't cap remain if
  fd_hard_limit=0
- BUG/MINOR: init: relax LSTCHK_NETADM checks for non root
- MINOR: compiler: add __nonstring macro
- BUG/MEDIUM: httpclient: Throw an error if an lua httpclient instance is
  reused
- DOC: hlua: Add a note to warn user about httpclient object reuse
- DOC: hlua: fix a few typos in HTTPMessage.set_body_len() documentation
- BUG/MINOR: mux-quic: do not decode if conn in error
- BUG/MEDIUM: check: Requeue healthchecks on I/O events to handle check
  timeout
- BUG/MEDIUM: fd: Use the provided tgid in fd_insert() to get tgroup_info
- BUG/MINOR: config/server: reject QUIC addresses
- BUG/MEDIUM: check: Set SOCKERR by default when a connection error is
  reported
- BUG/MEDIUM: ssl/clienthello: ECDSA with ssl-max-ver TLSv1.2 and no ECDSA
  ciphers
- MINOR: http: add a function to validate characters of :authority
- BUG/MEDIUM: h2/h3: reject some forbidden chars in :authority before
  reassembly
- BUG/MEDIUM: h1/h2/h3: reject forbidden chars in the Host header field
- DOC: config: prefer-last-server: add notes for non-deterministic algorithms
- BUG/MINOR: stream: Avoid recursive evaluation for unique-id based on itself
- BUG/MINOR: log: Be able to use %%ID alias at anytime of the stream's
  evaluation
- DOC: configuration: add details on prefer-client-ciphers
- BUG/MINOR: quic: wrong QUIC_FT_CONNECTION_CLOSE(0x1c) frame encoding
- SCRIPTS: drop the HTML generation from announce-release
- BUG/MEDIUM: hlua: Forbid any L6/L7 sample fetche functions from lua
  services
- BUG/MEDIUM: mux-h2: Properly handle connection error during preface sending
- BUG/MINOR: jwt: Copy input and parameters in dedicated buffers in jwt_verify
  converter
- DOC: Fix 'jwt_verify' converter doc
- BUG/MINOR: hlua: Skip headers when a receive is performed on an HTTP applet
- BUG/MEDIUM: hlua: Report to SC when data were consumed on a lua socket
- BUG/MEDIUM: hlua: Report to SC when output data are blocked on a lua socket
- BUG/MEDIUM: dns: Reset reconnect tempo when connection is finally
  established
- BUG/MINOR: hlua: take default-path into account with lua-load-per-thread
- DOC: management: clarify usage of -V with -c
- BUG/MINOR: listener: really assign distinct IDs to shards
- BUG/MEDIUM: http-client: Don't wake http-client applet if nothing was
  xferred
- BUG/MEDIUM: http-client: Properly inc input data when HTX blocks are
  xferred
- BUG/MEDIUM: http-client: Ask for more room when request data cannot be
  xferred
- BUG/MINOR: http-client: Ignore 1XX interim responses in non-HTX mode
- BUG/MINOR: http-client: Reject any 101-switching-protocols response
- BUG/MEDIUM: http-client: Drain the request if an early response is received
- BUG/MEDIUM: http-client: Notify applet has more data to deliver until the
  EOM
- BUG/MINOR: applet: Don't trigger BUG_ON if the tid is not on appctx init
- BUG/MINOR: halog: exit with error when some output filters are set
  simultaneosly
- BUG/MEDIUM: threads: Disable the workaround to load libgcc_s on macOS
- DOC: list missing global QUIC settings
- BUILD: compat: always set _POSIX_VERSION to ease comparisons
- BUG/MINOR: stick-table: cap sticky counter idx with tune.nb_stk_ctr instead
  of MAX_SESS_STKCTR
- BUG/MEDIUM: ssl: Fix 0rtt to the server
- BUG/MEDIUM: ssl: fix build with AWS-LC
- BUG/MINOR: init: Initialize random seed earlier in the init process
- DOC: management: fix typo in commit f4f93c56
- DOC: config: recommend single quoting passwords
- BUG/MEDIUM: http-client: Test HTX_FL_EOM flag before commiting the HTX
  buffer
- BUG/MINOR: mux-h1: fix wrong lock label
- BUG/MINOR: quic: do not emit probe data if CONNECTION_CLOSE requested
- BUG/MINOR: acl: set arg_list->kw to aclkw->kw string literal if aclkw is
  found
- DOC: unreliable sockpair@ on macOS
- DOC: configuration: confuse "strict-mode" with "zero-warning"
- MINOR: doc: add missing statistics column
- MINOR: doc: add missing statistics column
- BUG/MEDIUM: server: Duplicate healthcheck's alpn inherited from default
  server
- BUG/MINOR: quic: fix room check if padding requested
- BUG/MINOR: haproxy: be sure not to quit too early on soft stop
- BUILD: acl: silence a possible null deref warning in parse_acl_expr()
- OPTIM: check: do not delay MUX for ALPN if SSL not active
- BUG/MEDIUM: checks: fix ALPN inheritance from server
- BUG/MEDIUM: h1: Allow reception if we have early data
- BUG/MEDIUM: ssl: create the mux immediately on early data
- BUG/MINOR: activity: fix reporting of task latency
- BUG/MINOR: ocsp: Crash when updating CA during ocsp updates
- BUG/MINOR: resolvers: always normalize FQDN from response
- BUG/MINOR: server: Update healthcheck when server settings are changed via
  CLI
- BUG/MEDIUM: ssl: ca-file directory mode must read every certificates of a
  file
- BUG/MINOR: h3: Fix errors introduced because of failed backport
- Revert "BUG/MINOR: config/server: reject QUIC addresses"
- DOC: config: clarify some known limitations of the json_query() converter
- BUG/CRITICAL: mjson: fix possible DoS when parsing numbers
- BUG/MINOR: h2: forbid 'Z' as well in header field names checks
- BUG/MINOR: h3: forbid 'Z' as well in header field names checks
- Revert "BUILD: makefile: enable backtrace by default on musl"

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 2.8.15-0
- BUG/MEDIUM: ssl: chosing correct certificate using RSA-PSS with TLSv1.3
- BUG/MEDIUM: clock: make sure now_ms cannot be TICK_ETERNITY
- BUG/MINOR: spoe: Check the shared waiting queue to shut applets during
  stopping
- BUG/MINOR: spoe: Allow applet creation when closing the last one during
  stopping
- BUG/MEDIUM: spoe: Don't wakeup idle applets in loop during stopping
- BUG/MEDIUM: mux-quic: do not attach on already closed stream
- MINOR: mux-quic: change return value of qcs_attach_sc()
- BUG/MINOR: mux-quic: handle closure of uni-stream
- DOC: config: reorder "tune.lua.*" keywords by alphabetical order
- DOC: config: add "tune.lua.burst-timeout" to the list of global parameters
- BUG/MEDIUM: fd: mark FD transferred to another process as FD_CLONED
- REGTESTS: Fix truncated.vtc to send 0-CRLF
- BUG/MEDIUM: htx: wrong count computation in htx_xfer_blks()
- DOC: htx: clarify <mark> parameter for htx_xfer_blks()
- DOC: option redispatch should mention persist options
- TESTS: ist: fix wrong array size
- BUG/MEDIUM: thread: use pthread_self() not ha_pthread[tid] in set_affinity
- DOC: management: rename some last occurences from domain "dns" to "resolvers"
- BUG/MINOR: server: fix the "server-template" prefix memory leak
- BUG/MEDIUM: debug: close a possible race between thread dump and panic()
- BUG/MINOR: quic: reserve length field for long header encoding
- BUG/MINOR: quic: fix CRYPTO payload size calcul for encoding
- BUG/MINOR: ssl/cli: "show ssl crt-list" lacks client-sigals
- BUG/MINOR: ssl/cli: "show ssl crt-list" lacks sigals
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
- MINOR: clock: always use atomic ops for global_now_ms
- BUG/MINOR: mux-h1: always make sure h1s->sd exists in h1_dump_h1s_info()
- MINOR: tinfo: add a new thread flag to indicate a call from a sig handler
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
- MINOR: compiler: add a simple macro to concatenate resolved strings
- BUILD: compiler: undefine the CONCAT() macro if already defined
- MINOR: compiler: add a new __decl_thread_var() macro to declare local
  variables
- MINOR: tools: resolve main() only once in resolve_sym_name()
- MINOR: tools: use only opportunistic symbols resolution
- BUILD: tools: silence a build warning when USE_THREAD=0
- MINOR: cli: export cli_io_handler() to ease symbol resolution
- MINOR: tools: improve symbol resolution without dl_addr
- MINOR: tools: ease the declaration of known symbols in resolve_sym_name()
- MINOR: tools: teach resolve_sym_name() a few more common symbols
- BUILD: tools: avoid a build warning on gcc-4.8 in resolve_sym_name()
- BUG/MINOR: peers: fix expire learned from a peer not converted from ms to
  ticks
- BUG/MEDIUM: peers: prevent learning expiration too far in futur from unsync
  node
- BUG/MEDIUM: mux-quic: fix crash on RS/SS emission if already close local
- BUG/MINOR: mux-quic: remove extra BUG_ON() in _qcc_send_stream()
- BUG/MINOR: log: fix gcc warn about truncating NUL terminator while init char
  arrays
- DOC: config: fix two missing "content" in "tcp-request" examples
- BUG/MINOR: backend: do not overwrite srv dst address on reuse
- BUG/MEDIUM: backend: fix reuse with set-dst/set-dst-port
- TESTS: Fix build for filltab25.c
- MINOR: task: add thread safe notification_new and notification_wake variants
- BUG/MINOR: hlua_fcn: fix potential UAF with Queue:pop_wait()
- BUG/MEDIUM: sample: fix risk of overflow when replacing multiple regex
  back-refs
- BUG/MINOR: backend: do not use the source port when hashing clientip
- BUG/MINOR: hlua: fix invalid errmsg use in hlua_init()
- DOC: config: add the missing "profiling.memory" to the global kw index
- BUG/MINOR: http-ana: Properly detect client abort when forwarding the
  response
- BUG/MEDIUM: http-ana: Report 502 from req analyzer only during rsp forwarding
- BUG/MINOR: mux-h2: Properly handle full or truncated HTX messages on shut
- BUG/MINOR: sink: add tempo between 2 connection attempts for sft servers (2)
- BUG/MINOR: backend: fix reuse with set-dst/set-dst-port (2)
- BUG/MEDIUM: backend: do not overwrite srv dst address on reuse (2)
- BUG/MEDIUM: h3: trim whitespaces when parsing headers value
- BUG/MEDIUM: h3: trim whitespaces in header value prior to QPACK encoding
- BUG/MINOR: h3: filter upgrade connection header
- BUG/MINOR: h3: reject invalid :path in request
- BUG/MINOR: h3: reject request URI with invalid characters
- BUG/MEDIUM: hlua: fix hlua_applet_{http,tcp}_fct() yield regression
  (lost data)
- BUG/MINOR: mux-quic: fix BUG_ON() crash on init failure after app-ops
- BUG/MINOR: quic: do not crash on CRYPTO ncbuf alloc failure
- BUG/MINOR debug: fix !USE_THREAD_DUMP in ha_thread_dump_fill()
- BUG/MINOR: mux-h2: prevent past scheduling with idle connections
- MINOR: tools: also protect the library name resolution against concurrent
  accesses

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.8.14-0
- BUG/MEDIUM: stconn: Really report blocked send if sends are blocked by
  an error
- BUG/MEDIUM: mux-h1: Fix how timeouts are applied on H1 connections
- MINOR: debug: make mark_tainted() return the previous value
- DEBUG: add a tainted flag when ha_panic() is called
- MINOR: chunk: drop the global thread_dump_buffer
- MINOR: debug: split ha_thread_dump() in two parts
- MINOR: debug: slightly change the thread_dump_pointer signification
- MINOR: debug: make ha_thread_dump_done() take the pointer to be used
- MINOR: debug: replace ha_thread_dump() with its two components
- MEDIUM: debug: on panic, make the target thread automatically allocate its buf
- BUG/MEDIUM: pattern: prevent uninitialized reads in pat_match_{str,beg}
- MINOR: quic: notify connection layer on handshake completion
- BUG/MINOR: stream: unblock stream on wait-for-handshake completion
- BUG/MEDIUM: quic: support wait-for-handshake
- MINOR: quic: simplify qc_parse_pkt_frms() return path
- MINOR: quic: use dynamically allocated frame on parsing
- MINOR: quic: extend return value of CRYPTO parsing
- BUG/MINOR: quic: repeat packet parsing to deal with fragmented CRYPTO
- BUG/MEDIUM: quic: prevent crash due to CRYPTO parsing error
- BUG/MEDIUM: stconn: Don't forward shut for SC in connecting state
- BUG/MEDIUM: stconn: Only consider I/O timers to update stream's expiration
  date
- BUG/MEDIUM: queues: Make sure we call process_srv_queue() when leaving
- BUG/MEDIUM: queues: Do not use pendconn_grab_from_px().
- DOC: config: add example for server "track" keyword
- BUG/MEDIUM: queue: Make process_srv_queue return the number of streams
- MINOR: config: Alert about extra arguments for errorfile and errorloc
- BUG/MINOR: stktable: fix big-endian compatiblity in smp_to_stkey()
- BUG/MINOR: quic: reject NEW_TOKEN frames from clients
- BUG/MEDIUM: stktable: fix missing lock on some table converters
- BUG/MAJOR: quic: reject too large CRYPTO frames
- BUG/MINOR: init: set HAPROXY_STARTUP_VERSION from the variable, not the macro
- BUG/MINOR: quic: ensure a detached coalesced packet can't access its
  neighbours
- MINOR: quic: Add a BUG_ON() on quic_tx_packet refcount
- BUILD: quic: Move an ASSUME_NONNULL() for variable which is not null
- BUG/MEDIUM: mux-h1: Properly close H1C if an error is reported before sending
  data
- BUG/MINOR: quic: do not increase congestion window if app limited
- BUG/MINOR: ssl: put ssl_sock_load_ca under SSL_NO_GENERATE_CERTIFICATES
- BUG/MINOR: stream: Properly handle "on-marked-up shutdown-backup-sessions"

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.8.13-0
- BUG/MINOR: ssl_sock: fix xprt_set_used() to properly clear the TASK_F_USR1 bit
- BUG/MINOR: h1: do not forward h2c upgrade header token
- BUG/MINOR: h2: reject extended connect for h2c protocol
- MINOR: mux-h1: Set EOI on SE during demux when both side are in DONE state
- BUG/MEDIUM: mux-h1/mux-h2: Reject upgrades with payload on H2 side only
- REGTESTS: h1/h2: Update script testing H1/H2 protocol upgrades
- REGTESTS: shorten a bit the delay for the h1/h2 upgrade test
- MINOR: task: define two new one-shot events for use with WOKEN_OTHER or MSG
- BUG/MEDIUM: stream: make stream_shutdown() async-safe
- BUG/MEDIUM: queue: always dequeue the backend when redistributing the last
  server
- BUG/MINOR: http-ana: Disable fast-fwd for unfinished req waiting for upgrade
- BUG/MEDIUM: queue: make sure never to queue when there's no more served conns
- BUG/MINOR: cli: don't show sockpairs in HAPROXY_CLI and HAPROXY_MASTER_CLI
- BUG/MEDIUM: resolvers: Insert a non-executed resulution in front of the wait
  list
- BUG/MEDIUM: mux-h2: Don't send RST_STREAM frame for streams with no ID
- BUG/MINOR: Don't report early srv aborts on request forwarding in DONE state
- BUG/MEDIUM: checks: make sure to always apply offsets to now_ms in expiration
- BUG/MEDIUM: mailers: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: mux_quic: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: peers: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: http_ana: Report -1 for %%Tr for invalid response only
- DOC: config: Slightly improve the %%Tr documentation
- DOC: config: Move wait_end in section about internal samples
- DOC: lua: fix yield-dependent methods expected contexts
- DOC: configuration: explain quotes and spaces in conditional blocks
- DOC: configuration: wrap long line for "strstr()" conditional expression
- BUG/MINOR: http-ana: Adjust the server status before the L7 retries
- BUG/MEDIUM: mux-h2: Increase max number of headers when encoding HEADERS
  frames
- BUG/MEDIUM: mux-h2: Check the number of headers in HEADERS frame after
  decoding
- BUG/MEDIUM: h3: Properly limit the number of headers received
- BUG/MEDIUM: h3: Increase max number of headers when sending headers
- BUG/MEDIUM: debug: don't set the STUCK flag from debug_handler()
- MINOR: activity/memprofile: offer a function to unregister stale info
- BUG/MEDIUM: pools/memprofile: always clean stale pool info on pool_destroy()
- MINOR: quic: convert qc_stream_desc release field to flags
- MINOR: quic: implement function to check if STREAM is fully acked
- BUG/MEDIUM: quic: handle retransmit for standalone FIN STREAM
- BUG/MINOR: quic: prevent freeze after early QCS closure
- BUG/MAJOR: quic: fix wrong packet building due to already acked frames
- DEV: lags/show-sess-to-flags: Properly handle fd state on server side
- BUG/MEDIUM: http-ana: Don't release too early the L7 buffer
- BUG/MEDIUM: sock: Remove FD_POLL_HUP during connect() if FD_POLL_ERR is not
  set
- BUG/MEDIUM: event_hdl: fix uninitialized value in async mode when no data is
  provided
- BUG/MEDIUM: http-ana: Reset request flag about data sent to perform a L7 retry
- BUG/MINOR: h1-htx: Use default reason if not set when formatting the response
- BUG/MINOR: signal: register default handler for SIGINT in signal_init()
- BUG/MINOR: quic: remove startup alert if conn socket-owner unsupported
- BUG/MINOR: server-state: Fix expiration date of srvrq_check tasks

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.8.12-0
- BUG/MAJOR: ocsp: Separate refcount per instance and per store
- BUG/MEDIUM: ssl: Fix crash when calling "update ssl ocsp-response" when an
  update is ongoing
- MEDIUM: h1: Accept invalid T-E values with accept-invalid-http-response option
- DOC: config: Explicitly list relaxing rules for accept-invalid-http-* options
- BUG/MEDIUM: mux-pt: Never fully close the connection on shutdown
- BUG/MEDIUM: cli: Deadlock when setting frontend maxconn
- BUG/MINOR: server: make sure the HMAINT state is part of MAINT
- BUG/MINOR: cfgparse-global: fix allowed args number for setenv
- BUG/MEDIUM: server: server stuck in maintenance after FQDN change
- BUG/MEDIUM: hlua: make hlua_ctx_renew() safe
- BUG/MEDIUM: hlua: properly handle sample func errors in
  hlua_run_sample_{fetch,conv}()
- BUG/MEDIUM: mux-quic: ensure timeout server is active for short requests
- BUG/MINOR: httpclient: return NULL when no proxy available during
  httpclient_new()
- BUG/MINOR: http-ana: Don't report a server abort if response payload is
  invalid
- REGTESTS: Never reuse server connection in http-messaging/truncated.vtc
- DOC: config: fix rfc7239 forwarded typo in desc
- BUG/MINOR: mworker: fix mworker-max-reloads parser
- BUG/MEDIUM: connection/http-reuse: fix address collision on unhandled address
  families
- MINOR: activity/memprofile: always return "other" bin on NULL return address
- BUG/MINOR: mux-quic: do not close STREAM with empty FIN if no data sent
- BUG/MINOR: server: fix dynamic server leak with check on failed init
- BUG/MINOR: http-ana: Fix wrong client abort reports during responses
  forwarding
- BUG/MEDIUM: stconn: Report blocked send if sends are blocked by an error
- BUG/MEDIUM: server: fix race on servers_list during server deletion
- MINOR: pools: export the pools variable
- MINOR: cli: remove non-printable characters from 'debug dev fd'
- BUG/MINOR: ssl/cli: 'set ssl cert' does not check the transaction name
  correctly
- BUG/MINOR: http-ana: Report internal error if an action yields on a final eval
- MINOR: stream: Save last evaluated rule on invalid yield
- CLEANUP: connection: properly name the CO_ER_SSL_FATAL enum entry

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
