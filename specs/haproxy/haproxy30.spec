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
%define pcre_ver      10.45
%define openssl_ver   3.3.4
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        3.0.11
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

BuildRequires:  make gcc-c++ systemd-devel perl perl-IPC-Cmd

%if 0%{?rhel} == 10
BuildRequires:  zlib-ng-compat-devel
%else
BuildRequires:  zlib-devel
%endif

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy28 haproxy32

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
                          ADDLIB="-ldl -lrt -lpthread"

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
* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.11-0
- BUG/MEDIUM: mux-fcgi: Try to fully fill demux buffer on receive if not empty
- BUG/MINOR: cli: Issue an error when too many args are passed for a command
- BUG/MAJOR: listeners: transfer connection accounting when switching listeners
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
- BUG/MEDIUM: peers: hold the refcnt until updating ts->seen
- BUG/MINOR: cli: fix too many args detection for commands
- BUG/MINOR: ssl/ckch: always free() the previous entry during parsing
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
- BUG/MEDIUM: stconn: Disable 0-copy forwarding for filters altering the
  payload
- BUG/MINOR: mux-h2: Reset streams with NO_ERROR code if full response was
  already sent
- BUILD: makefile: enable backtrace by default on musl
- BUG/MEDIUM: server: fix crash after duplicate GUID insertion
- BUG/MEDIUM: server: fix potential null-deref after previous fix
- BUG/MAJOR: cache: Crash because of wrong cache entry deleted
- DOC: configuration: fix the example in crt-store
- BUG/MINOR: h3: Set HTX flags corresponding to the scheme found in the request
- BUG/MEDIUM: hlua: Properly detect shudowns for TCP applets based on the new
  API
- BUG/MEDIUM: hlua: Fix getline() for TCP applets to work with applet's buffers
- REGTESTS: Make the script testing conditional set-var compatible with Vtest2
- REGTESTS: Explicitly allow failing shell commands in some scripts
- CI: vtest: Rely on VTest2 to run regression tests
- CI: vtest: Fix the build script to properly work on MaOS
- BUG/MINOR: limits: compute_ideal_maxconn: don't cap remain if fd_hard_limit=0
- BUG/MEDIUM: httpclient: Throw an error if an lua httpclient instance is
  reused
- DOC: hlua: Add a note to warn user about httpclient object reuse
- DOC: hlua: fix a few typos in HTTPMessage.set_body_len() documentation

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.10-0
- MINOR: log: support "raw" logformat node typecast
- BUG/MINOR: peers: fix expire learned from a peer not converted from ms to
  ticks
- BUG/MEDIUM: peers: prevent learning expiration too far in futur from unsync
  node
- BUG/MEDIUM: mux-quic: fix crash on RS/SS emission if already close local
- BUG/MINOR: mux-quic: remove extra BUG_ON() in _qcc_send_stream()
- BUG/MINOR: log: fix gcc warn about truncating NUL terminator while init char
  arrays
- DOC: config: fix two missing "content" in "tcp-request" examples
- BUILD: compiler: undefine the CONCAT() macro if already defined
- BUG/MINOR: rhttp: fix incorrect dst/dst_port values
- BUG/MINOR: backend: do not overwrite srv dst address on reuse
- BUG/MEDIUM: backend: fix reuse with set-dst/set-dst-port
- BUG/MEDIUM: stream: Fix a possible freeze during a forced shut on a stream
- TESTS: Fix build for filltab25.c
- MINOR: task: add thread safe notification_new and notification_wake variants
- BUG/MINOR: hlua_fcn: fix potential UAF with Queue:pop_wait()
- CLEANUP: log: adjust _lf_cbor_encode_byte() comment
- BUG/MINOR: log: fix CBOR encoding with LOG_VARTEXT_START() + lf_encode_chunk
  ()
- BUG/MEDIUM: sample: fix risk of overflow when replacing multiple regex
  back-refs
- BUG/MINOR: backend: do not use the source port when hashing clientip
- BUG/MINOR: hlua: fix invalid errmsg use in hlua_init()
- DOC: config: add the missing "profiling.memory" to the global kw index
- BUG/MINOR: http-ana: Properly detect client abort when forwarding the
  response
- BUG/MEDIUM: http-ana: Report 502 from req analyzer only during rsp forwarding
- BUG/MINOR: sink: add tempo between 2 connection attempts for sft servers (2)
- BUG/MEDIUM: h3: trim whitespaces when parsing headers value
- BUG/MEDIUM: h3: trim whitespaces in header value prior to QPACK encoding
- BUG/MINOR: h3: filter upgrade connection header
- BUG/MINOR: h3: reject invalid :path in request
- BUG/MINOR: h3: reject request URI with invalid characters
- BUG/MEDIUM: hlua: fix hlua_applet_{http,tcp}_fct() yield regression
  (lost data)
- BUG/MINOR: quic: do not crash on CRYPTO ncbuf alloc failure
- DEBUG: stream: Add debug counters to track some client/server aborts
- BUG/MINOR: stktable: invalid use of stkctr_set_entry() with mixed table types
- BUG/MEDIUM: mux-fcgi: Properly handle read0 on partial records
- DEBUG: fd: add a counter of takeovers of an FD since it was last opened
- MINOR: fd: add a generation number to file descriptors
- MINOR: epoll: permit to mask certain specific events
- DEBUG: epoll: store and compare the FD's generation count with reported event
- MEDIUM: epoll: skip reports of stale file descriptors
- IMPORT: plock: give higher precedence to W than S
- IMPORT: plock: lower the slope of the exponential back-off
- IMPORT: plock: use cpu_relax() for a shorter time in EBO
- BUG/MINOR debug: fix !USE_THREAD_DUMP in ha_thread_dump_fill()
- BUG/MINOR: mux-h2: prevent past scheduling with idle connections
- BUG/MINOR: rhttp: fix reconnect if timeout connect unset
- BUG/MINOR: rhttp: ensure GOAWAY can be emitted after reversal
- MINOR: tools: also protect the library name resolution against concurrent
  accesses

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.9-0
- BUG/MEDIUM: ssl: chosing correct certificate using RSA-PSS with TLSv1.3
- BUG/MEDIUM: mux-quic: do not attach on already closed stream
- MINOR: mux-quic: change return value of qcs_attach_sc()
- BUG/MINOR: mux-quic: handle closure of uni-stream
- BUG/MINOR: spoe: Check the shared waiting queue to shut applets during
  stopping
- BUG/MINOR: spoe: Allow applet creation when closing the last one during
  stopping
- BUG/MEDIUM: spoe: Don't wakeup idle applets in loop during stopping
- BUG/MEDIUM: fd: mark FD transferred to another process as FD_CLONED
- REGTESTS: Fix truncated.vtc to send 0-CRLF
- BUG/MEDIUM: htx: wrong count computation in htx_xfer_blks()
- DOC: htx: clarify <mark> parameter for htx_xfer_blks()
- DOC: option redispatch should mention persist options
- BUG/MEDIUM: server: properly initialize PROXY v2 TLVs
- TESTS: ist: fix wrong array size
- CI: github: fix h2spec.config proxy names
- BUG/MINOR: stream: fix age calculation in "show sess" output
- BUG/MINOR: cfgparse-tcp: relax namespace bind check
- MINOR: startup: adjust alert messages, when capabilities are missed
- BUG/MEDIUM: thread: use pthread_self() not ha_pthread[tid] in set_affinity
- DOC: management: rename some last occurences from domain "dns" to "resolvers"
- BUG/MINOR: server: fix the "server-template" prefix memory leak
- BUILD: ssl: allow to build without the renegotiation API of WolfSSL
- BUILD: ssl: more cleaner approach to WolfSSL without renegotiation
- BUG/MEDIUM: debug: close a possible race between thread dump and panic()
- BUG/MINOR: quic: reserve length field for long header encoding
- BUG/MINOR: quic: fix CRYPTO payload size calcul for encoding
- BUG/MINOR: ssl/cli: "show ssl crt-list" lacks client-sigals
- BUG/MINOR: ssl/cli: "show ssl crt-list" lacks sigals
- BUG/MINOR: cli: Wait for the last ACK when FDs are xferred from the old worker
- BUG/MEDIUM: filters: Handle filters registered on data with no payload
  callback
- BUG/MINOR: fcgi: Don't set the status to 302 if it is already set
- BUG/MINOR: quic: prevent crash on conn access after MUX init failure
- BUG/MINOR: mux-quic: prevent crash after MUX init failure
- BUG/MINOR: mux-h2: Properly handle full or truncated HTX messages on shut
- BUG/MINOR: tcp-rules: Don't forward close during tcp-response content rules
  eval
- BUG/MINOR: cli: Don't set SE flags from the cli applet
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
- BUG/MEDIUM: stream: never allocate connection addresses from signal handler
- MINOR: freq_ctr: provide non-blocking read functions
- BUG/MEDIUM: stream: use non-blocking freq_ctr calls from the stream dumper
- BUG/MINOR: h2: always trim leading and trailing LWS in header values
- BUG/MINOR: h3: do not report transfer as aborted on preemptive response
- CLEANUP: h3: fix documentation of h3_rcv_buf()
- BUG/MINOR: server: check for either proxy-protocol v1 or v2 to send hedaer
- CLEANUP: log: removing "log-balance" references
- BUG/MINOR: log: set proper smp size for balance log-hash
- BUG/MEIDUM: startup: return to initial cwd only after check_config_validity()
- BUG/MINOR: cfgparse/peers: fix inconsistent check for missing peer server
- BUG/MINOR: cfgparse/peers: properly handle ignored local peer case
- BUG/MINOR: server: dont return immediately from parse_server() when skipping
  checks
- MINOR: cfgparse/peers: provide more info when ignoring invalid "peer" or
  "server" lines
- BUG/MINOR: stats: fix capabilities and hide settings for some generic metrics
- BUG/MINOR: namespace: handle a possible strdup() failure
- BUG/MINOR: ssl_crtlist: handle a possible strdup() failure
- BUG/MINOR: http-check: Don't pretend a C-L heeader is set before adding it
- BUG/MEDIUM: hlua/cli: fix cli applet UAF in hlua_applet_wakeup()
- BUG/MEDIUM: stream: don't use localtime in dumps from a signal handler
- MINOR: compiler: add a simple macro to concatenate resolved strings
- MINOR: compiler: add a new __decl_thread_var() macro to declare local
  variables
- MINOR: tools: resolve main() only once in resolve_sym_name()
- MINOR: tools: use only opportunistic symbols resolution
- BUILD: tools: silence a build warning when USE_THREAD=0
- MINOR: tinfo: split the signal handler report flags into 3
- MINOR: cli: export cli_io_handler() to ease symbol resolution
- MINOR: tools: improve symbol resolution without dl_addr
- MINOR: tools: ease the declaration of known symbols in resolve_sym_name()
- MINOR: tools: teach resolve_sym_name() a few more common symbols
- BUILD: tools: avoid a build warning on gcc-4.8 in resolve_sym_name()

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.8-0


* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.7-0
- BUG/MEDIUM: pattern: prevent uninitialized reads in pat_match_{str,beg}
- MINOR: quic: notify connection layer on handshake completion
- BUG/MINOR: stream: unblock stream on wait-for-handshake completion
- BUG/MEDIUM: quic: support wait-for-handshake
- MINOR: quic: simplify qc_parse_pkt_frms() return path
- MINOR: quic: use dynamically allocated frame on parsing
- MINOR: quic: extend return value of CRYPTO parsing
- BUG/MINOR: quic: repeat packet parsing to deal with fragmented CRYPTO
- CLEANUP: guid: remove global tree export
- BUG/MINOR: guid/server: ensure thread-safety on GUID insert/delete
- BUG/MEDIUM: quic: prevent crash due to CRYPTO parsing error
- BUG/MINOR: cli: don't show sockpairs in HAPROXY_CLI and HAPROXY_MASTER_CLI
- BUG/MEDIUM: resolvers: Insert a non-executed resulution in front of the wait
  list
- BUG/MEDIUM: mux-h2: Don't send RST_STREAM frame for streams with no ID
- BUG/MINOR: Don't report early srv aborts on request forwarding in DONE state
- BUG/MEDIUM: checks: make sure to always apply offsets to now_ms in expiration
- BUG/MEDIUM: mailers: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: mux_quic: make sure to always apply offsets to now_ms in expiration
- BUG/MINOR: peers: make sure to always apply offsets to now_ms in expiration
- DOC: config: A a space before ':' for {bs,fs}.aborted and {bs,fs}.rst_code
- DOC: config: Fix a typo in "1.3.1. The Request line"
- BUG/MINOR: http_ana: Report -1 for %%Tr for invalid response only
- DOC: config: Slightly improve the %%Tr documentation
- DOC: config: Move wait_end in section about internal samples
- DOC: config: Move fs.* and bs.* in section about L5 samples
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
- DOC: config: Improve documentation of tune.http.maxhdr directive
- BUG/MEDIUM: debug: don't set the STUCK flag from debug_handler()
- BUG/MEDIUM: wdt: fix the stuck detection for warnings
- BUG/MINOR: activity/memprofile: reinitialize the free calls on DSO summary
- MINOR: activity/memprofile: offer a function to unregister stale info
- BUG/MEDIUM: pools/memprofile: always clean stale pool info on pool_destroy()
- BUG/MAJOR: mux-h1: Properly handle wrapping on obuf when dumping the
  first-line
- BUG/MAJOR: quic: fix wrong packet building due to already acked frames
- DEV: lags/show-sess-to-flags: Properly handle fd state on server side
- BUG/MEDIUM: http-ana: Don't release too early the L7 buffer
- BUG/MEDIUM: sock: Remove FD_POLL_HUP during connect() if FD_POLL_ERR is not
  set
- MINOR: mux-quic: Don't send an emtpy H3 DATA frame during zero-copy forwarding
- BUG/MINOR: log: fix lf_text() behavior with empty string
- BUG/MEDIUM: event_hdl: fix uninitialized value in async mode when no data is
  provided
- BUG/MEDIUM: http-ana: Reset request flag about data sent to perform a L7 retry
- BUG/MINOR: h1-htx: Use default reason if not set when formatting the response
- BUG/MINOR: signal: register default handler for SIGINT in signal_init()
- BUG/MINOR: quic: remove startup alert if conn socket-owner unsupported
- MINOR: mux-h2/traces: add a missing trace on negative initial window size
- CLEANUP: mux-h2/traces: reword certain ambiguous traces
- BUG/MINOR: server-state: Fix expiration date of srvrq_check tasks

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 3.0.6-0
- MINOR: connection: No longer include stconn type header in connection-t.h
- BUG/MINOR: h1: do not forward h2c upgrade header token
- BUG/MINOR: h2: reject extended connect for h2c protocol
- MINOR: mux-h1: Set EOI on SE during demux when both side are in DONE state
- BUG/MEDIUM: mux-h1/mux-h2: Reject upgrades with payload on H2 side only
- REGTESTS: h1/h2: Update script testing H1/H2 protocol upgrades
- REGTESTS: shorten a bit the delay for the h1/h2 upgrade test
- BUG/MINOR: mux-quic: report glitches to session
- BUG/MEDIUM: cli: Be sure to catch immediate client abort
- BUG/MEDIUM: cli: Deadlock when setting frontend maxconn
- BUG/MINOR: server: make sure the HMAINT state is part of MAINT
- BUG/MINOR: cfgparse-global: fix allowed args number for setenv
- BUILD: tools: only include execinfo.h for the real backtrace() function
- MINOR: tools: do not attempt to use backtrace() on linux without glibc
- MINOR: task: define two new one-shot events for use with WOKEN_OTHER or MSG
- BUG/MEDIUM: stream: make stream_shutdown() async-safe
- BUG/MINOR: queue: make sure that maintenance redispatches server queue
- MINOR: server: make srv_shutdown_sessions() call pendconn_redistribute()
- BUG/MEDIUM: queue: always dequeue the backend when redistributing the last
  server
- BUG/MINOR: mux-h1: Fix condition to set EOI on SE during zero-copy forwarding
- BUG/MINOR: http-ana: Disable fast-fwd for unfinished req waiting for upgrade
- MINOR: debug: make mark_tainted() return the previous value
- MINOR: chunk: drop the global thread_dump_buffer
- MINOR: debug: split ha_thread_dump() in two parts
- MINOR: debug: slightly change the thread_dump_pointer signification
- MINOR: debug: make ha_thread_dump_done() take the pointer to be used
- MINOR: debug: replace ha_thread_dump() with its two components
- MEDIUM: debug: on panic, make the target thread automatically allocate its buf
- BUG/MEDIUM: server: server stuck in maintenance after FQDN change
- BUG/MEDIUM: hlua: make hlua_ctx_renew() safe
- BUG/MEDIUM: hlua: properly handle sample func errors in
  hlua_run_sample_{fetch,conv}()
- BUG/MEDIUM: mux-quic: ensure timeout server is active for short requests
- BUG/MEDIUM: queue: make sure never to queue when there's no more served conns
- BUG/MINOR: httpclient: return NULL when no proxy available during
  httpclient_new()
- BUG/MEDIUM: stconn: Wait iobuf is empty to shut SE down during a check send
- BUG/MINOR: http-ana: Don't report a server abort if response payload is
  invalid
- BUG/MEDIUM: stconn: Check FF data of SC to perform a shutdown in sc_notify()
- BUG/MAJOR: filters/htx: Add a flag to state the payload is altered by a filter
- REGTESTS: Never reuse server connection in http-messaging/truncated.vtc
- BUG/MINOR: quic: avoid leaking post handshake frames
- BUG/MEDIUM: quic: avoid freezing 0RTT connections
- DOC: config: fix rfc7239 forwarded typo in desc
- BUG/MINOR: mworker: fix mworker-max-reloads parser
- BUG/MINOR: mux-quic: do not close STREAM with empty FIN if no data sent
- BUG/MEDIUM: stats-html: Never dump more data than expected during 0-copy FF
- BUG/MEDIUM: mux-h2: Remove H2S from send list if data are sent via 0-copy FF
- BUG/MEDIUM: connection/http-reuse: fix address collision on unhandled address
  families
- MINOR: activity/memprofile: always return "other" bin on NULL return address
- MINOR: activity/memprofile: show per-DSO stats
- BUG/MINOR: server: fix dynamic server leak with check on failed init
- BUG/MEDIUM: stconn: Report blocked send if sends are blocked by an error
- BUG/MINOR: http-ana: Fix wrong client abort reports during responses
  forwarding
- BUG/MINOR: stconn: Don't disable 0-copy FF if EOS was reported on consumer
  side
- BUG/MEDIUM: server: fix race on servers_list during server deletion
- BUILD: debug: silence a build warning with threads disabled
- MINOR: pools: export the pools variable
- MINOR: debug: place a magic pattern at the beginning of post_mortem
- MINOR: debug: place the post_mortem struct in its own section.
- MINOR: debug: store important pointers in post_mortem
- MINOR: cli: remove non-printable characters from 'debug dev fd'
- BUG/MINOR: trace: stop rewriting argv with -dt
- BUG/MINOR: ssl/cli: 'set ssl cert' does not check the transaction name
  correctly
- DOC: config: add missing glitch_{cnt,rate} data types
- DOC: config: add missing glitch_{cnt,rate} sample definitions
- BUG/MEDIUM: mux-h1: Fix how timeouts are applied on H1 connections
- BUG/MINOR: http-ana: Report internal error if an action yields on a final eval
- MINOR: stream: Save last evaluated rule on invalid yield
- BUG/MEDIUM: promex: Fix dump of extra counters
- DOC: config: document connection error 44 (reverse connect failure)
- CLEANUP: connection: properly name the CO_ER_SSL_FATAL enum entry
- BUG/MINOR: quic: fix malformed probing packet building
- MINOR: cli/debug: show dev: add cmdline and version
- MINOR: stream/stats: Expose the current number of streams in stats
- MINOR: stream/stats: Expose the total number of streams ever created in stats
- BUG/MINOR: stats: Fix the name for the total number of streams created
- MINOR: connection: add more connection error codes to cover common errno
- MINOR: rawsock: set connection error codes when returning from
  recv/send/splice
- MINOR: connection: add new sample fetch functions fc_err_name and bc_err_name
- MINOR: debug: print gdb hints when crashing
- MINOR: debug: do not limit backtraces to stuck threads
- MINOR: debug: also add a pointer to struct global to post_mortem
- MINOR: debug: also add fdtab and acitvity to struct post_mortem
- MINOR: debug: remove the redundant process.thread_info array from post_mortem
- MINOR: wdt: move the local timers to a struct
- MINOR: debug: add a function to dump a stuck thread
- DEBUG: wdt: better detect apparently locked up threads and warn about them
- DEBUG: cli: make it possible for "debug dev loop" to trigger warnings
- DEBUG: wdt: make the blocked traffic warning delay configurable
- DEBUG: wdt: add a stats counter "BlockedTrafficWarnings" in show info
- BUILD: debug: also declare strlen() in __ABORT_NOW()
- BUILD: Missing inclusion header for ssize_t type
- MINOR: debug: move the "recover now" warn message after the optional notes

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
