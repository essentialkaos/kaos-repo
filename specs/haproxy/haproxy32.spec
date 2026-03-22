################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  3.2
%define comp_ver   32

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.8
%define pcre_ver      10.47
%define openssl_ver   3.5.5
%define ncurses_ver   6.6
%define readline_ver  8.3

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        3.2.15
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

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy28 haproxy30

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
  ln -sf libncursesw.a build/lib/libncurses.a
  ln -sf libncursesw.a build/lib/libtinfo.a
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
%doc CHANGELOG LICENSE doc/* examples/*.cfg
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
* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.15-0
- BUG/MINOR: mworker: don't set the PROC_O_LEAVING flag on master process
- BUG/MINOR: tcpcheck: Fix typo in error error message for `http-check
  expect`
- BUG/MINOR: jws: fix memory leak in jws_b64_signature
- DOC: configuration: http-check expect example typo
- DOC/CLEANUP: config: update mentions of the old "Global parameters" section
- BUG/MINOR: mworker: always stop the receiving listener
- BUG/MINOR: memprof: avoid a small memory leak in "show profiling"
- MINOR: tools: extend the pointer hashing code to ease manipulations
- MINOR: memprof: attempt different retry slots for different hashes on
  collision
- BUG/MINOR: mworker: only match worker processes when looking for unspawned
  proc
- BUG/MINOR: mworker: fix typo &= instead of & in proc list serialization
- BUG/MINOR: mworker: set a timeout on the worker socketpair read at startup
- BUG/MINOR: mworker: avoid passing NULL version in proc list serialization
- BUG/MINOR: sockpair: set FD_CLOEXEC on fd received via SCM_RIGHTS
- BUG/MINOR: spoe: Properly switch SPOE filter to WAITING_ACK state
- BUG/MEDIUM: spoe: Properly abort processing on client abort
- BUG/MINOR: h2/h3: Only test number of trailers inserted in HTX message
- MINOR: htx: Add function to truncate all blocks after a specific block
- BUG/MINOR: h2/h3: Never insert partial headers/trailers in an HTX message
- BUG/MINOR: http-ana: Swap L7 buffer with request buffer by hand
- BUG/MINOR: proxy: do not forget to validate quic-initial rules
- BUG/MINOR: stream: Fix crash in stream dump if the current rule has no
  keyword
- BUG/MINOR: mjson: make mystrtod() length-aware to prevent out-of-bounds
  reads
- BUG/MINOR: spoe: Fix condition to abort processing on client abort
- BUILD: spoe: Remove unsused variable
- DEV: gdb: add a utility to find the post-mortem address from a core
- MINOR: tools: add a function to create a tar file header
- MINOR: tools: add a function to load a file into a tar archive
- MINOR: config: support explicit "on" and "off" for "set-dumpable"
- MINOR: debug: read all libs in memory when set-dumpable=libs
- DEV: gdb: add a new utility to extract libs from a core dump:
  libs-from-core
- MINOR: debug: copy debug symbols from /usr/lib/debug when present
- MINOR: debug: opportunistically load libthread_db.so.1 with
  set-dumpable=libs
- BUG/MINOR: mworker: don't try to access an initializing process
- BUG/MEDIUM: peers: enforce check on incoming table key type
- BUG/MINOR: mux-h2: properly ignore R bit in GOAWAY stream ID
- BUG/MINOR: mux-h2: properly ignore R bit in WINDOW_UPDATE increments
- BUG/MAJOR: h3: check body size with content-length on empty FIN
- BUG/MEDIUM: h3: reject unaligned frames except DATA
- MINOR: mworker/cli: extract worker "show proc" row printer
- BUG/MINOR: mworker/cli: fix show proc pagination losing entries on resume
- CI: github: treat vX.Y.Z release tags as stable like haproxy-* branches

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.14-0
- MINOR: mux-h2: also count glitches on invalid trailers
- MINOR: mux-h2: add a new setting, "tune.h2.log-errors" to tweak error
  logging
- BUG/MEDIUM: mux-h2: make sure to always report pending errors to the stream
- BUG/MINOR: promex: fix server iteration when last server is deleted
- BUG/MEDIUM: stream: Handle TASK_WOKEN_RES as a stream event
- BUG/MEDIUM: hpack: correctly deal with too large decoded numbers
- BUG/MAJOR: qpack: unchecked length passed to huffman decoder
- BUG/MINOR: qpack: fix 1-byte OOB read in qpack_decode_fs_pfx()
- BUG/MEDIUM: qpack: correctly deal with too large decoded numbers
- BUG/MINOR: h1-htx: Be sure that H1 response version starts by "HTTP/"
- DEBUG: stream: Display the currently running rule in stream dump
- MINOR: filters: Set last_entity when a filter fails on stream_start
  callback
- BUG/MAJOR: fcgi: Fix param decoding by properly checking its size
- BUG/MAJOR: resolvers: Properly lowered the names found in DNS response
- BUG/MEDIUM: mux-fcgi: Use a safe loop to resume each stream eligible for
  sending
- BUG/MINOR: ssl-sample: Fix sample_conv_sha2() by checking EVP_Digest*
  failures
- BUG/MINOR: backend: Don't get proto to use for webscoket if there is no
  server
- SCRIPTS: git-show-backports: hide the common ancestor warning in quiet mode
- SCRIPTS: git-show-backports: add a restart-from-last option

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.13-0
- DOC: internals: addd mworker V3 internals
- DOC: proxy-proto: underline the packed attribute for struct pp2_tlv_ssl
- BUG/MINOR: deviceatlas: add missing return on error in config parsers
- BUG/MINOR: deviceatlas: add NULL checks on strdup() results in config
  parsers
- BUG/MEDIUM: deviceatlas: fix resource leaks on init error paths
- BUG/MINOR: deviceatlas: fix off-by-one in da_haproxy_conv()
- BUG/MINOR: deviceatlas: fix cookie vlen using wrong length after extraction
- BUG/MINOR: deviceatlas: fix double-checked locking race in checkinst
- BUG/MINOR: deviceatlas: fix resource leak on hot-reload compile failure
- BUG/MINOR: deviceatlas: fix deinit to only finalize when initialized
- BUG/MINOR: deviceatlas: set cache_size on hot-reloaded atlas instance
- BUG/MINOR: ssl: lack crtlist_dup_ssl_conf() declaration
- BUG/MINOR: ssl: double-free on error path w/ ssl-f-use parser
- BUG/MINOR: ssl: fix leak in ssl-f-use parser upon error
- BUG/MINOR: ssl: clarify ssl-f-use errors in post-section parsing
- BUG/MINOR: ssl: error with ssl-f-use when no "crt"
- BUG/MAJOR: Revert "MEDIUM: mux-quic: add BUG_ON if sending on locally closed
  QCS"
- BUG/MEDIUM: h3: reject frontend CONNECT as currently not implemented
- BUG/MEDIUM: mux-h2/quic: Stop sending via fast-forward if stream is closed
- BUG/MEDIUM: mux-h1: Stop sending vi fast-forward for unexpected states
- BUG/MEDIUM: applet: Fix test on shut flags for legacy applets (v2)
- DEV: term-events: Fix hanshake events decoding
- BUG/MINOR: flt-trace: Properly compute length of the first DATA block
- CLEANUP: compression: Remove unused static buffers
- BUG/MINOR: http-ana: Stop to wait for body on client error/abort
- MINOR: stconn: Add missing SC_FL_NO_FASTFWD flag in sc_show_flags
- CI: vtest: move the vtest2 URL to vinyl-cache.org
- CI: github: disable windows.yml by default on unofficials repo
- CLEANUP: mux-h1: Remove unneeded null check

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.12-0
- MINOR: rawsock: introduce CO_RFL_TRY_HARDER to detect closures on complete
  reads
- MEDIUM: ssl: don't always process pending handshakes on closed connections
- BUG/MAJOR: applet: Don't call I/O handler if the applet was shut
- BUG/MEDIUM: applet: Fix test on shut flags for legacy applets
- DOC: internals: cleanup few typos in master-worker documentation
- BUG/MEDIUM: threads: Atomically set TH_FL_SLEEPING and clr FL_NOTIFIED
- CLEANUP: haproxy: fix bad line wrapping in run_poll_loop()
- BUG/MINOR: cpu-topo: count cores not cpus to distinguish core types
- BUG/MEDIUM: lb-chash: always properly initialize lb_nodes with dynamic
  servers
- DOC: config: mention the limitation on server id range for consistent hash
- BUG/MINOR: config: Fix setting of alt_proto
- BUG/MINOR: startup: fix allocation error message of progname string
- BUG/MINOR: startup: handle a possible strdup() failure
- BUG/MAJOR: quic: reject invalid token
- BUG/MAJOR: quic: fix parsing frame type

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.11-0
- BUG/MEDIUM: http-ana: Properly detect client abort when forwarding response
  (v2)
- BUG/MEDIUM: stconn: Don't report abort from SC if read0 was already
  received
- BUG/MINOR: sock-inet: ignore conntrack for transparent sockets on Linux
- MINOR: ssl: Add a function to hash SNIs
- MINOR: ssl: Store hash of the SNI for cached TLS sessions
- MINOR: ssl: Compare hashes instead of SNIs when a session is cached
- MINOR: connection/ssl: Store the SNI hash value in the connection itself
- MEDIUM: tcpcheck/backend: Get the connection SNI before initializing SSL
  ctx
- BUG/MEDIUM: ssl: Don't reuse TLS session if the connection's SNI differs
- MEDIUM: ssl/server: No longer store the SNI of cached TLS sessions
- MINOR: connections: Add a new CO_FL_SSL_NO_CACHED_INFO flag
- BUG/MEDIUM: ssl: Don't resume session for check connections
- BUG/MINOR: backend: fix the conn_retries check for TFO
- BUG/MINOR: backend: inspect request not response buffer to check for TFO
- DOC: config: fix the length attribute name for stick tables of type binary /
  string
- BUG/MEDIUM: mworker: can't use signals after a failed reload
- BUILD: ssl: strchr definition changed in C23
- BUILD: tools: memchr definition changed in C23
- BUG/MINOR: cfgparse: wrong section name upon error
- BUILD: sockpair: fix build issue on macOS related to variable-length arrays
- BUG/MINOR: cli/stick-tables: argument to "show table" is optional
- REGTESTS: ssl: Fix reg-tests curve check
- MINOR: cfgparse: remove duplicate "force-persist" in common kw list
- BUG/MINOR: hlua_fcn: fix broken yield for Patref:add_bulk()
- BUG/MINOR: hlua_fcn: ensure Patref:add_bulk() is given a table object before
  using it
- BUG/MEDIUM: quic: fix ACK ECN frame parsing
- BUG/MINOR: http_act: fix deinit performed on uninitialized lf_expr in
  release_http_map()
- BUG/MINOR: proxy: free persist_rules
- BUG/MINOR: cfgparse: fix "default" prefix parsing
- BUG/MEDIUM: promex: server iteration may rely on stale server
- BUG/MEDIUM: log: parsing log-forward options may result in segfault
- BUG/MEDIUM: ssl: fix error path on generate-certificates
- BUG/MEDIUM: ssl: fix generate-certificates option when SNI greater than
  64bytes
- BUG/MEDIUM: mux-quic: prevent BUG_ON() on aborted uni stream close
- REGTESTS: ssl: fix generate-certificates w/ LibreSSL
- BUG/MINOR: proxy: fix deinit crash on defaults with duplicate name
- BUG/MEDIUM: hlua: fix invalid lua_pcall() usage in hlua_traceback()
- BUG/MINOR: hlua: consume error object if ignored after a failing lua_pcall
  ()
- BUG/MINOR: promex: Detach promex from the server on error dump its metrics
  dump
- BUG/MEDIUM: mux-h1: Skip UNUSED htx block when formating the start line
- MINOR: ssl: allow to disable certificate compression
- BUG/MINOR: ssl: fix error message of tune.ssl.certificate-compression
- CLEANUP: mworker/cli: remove useless variable
- BUG/MINOR: mworker/cli: 'show proc' is limited by buffer size
- BUG/MINOR: mworker/cli: fix show proc pagination using reload counter
- BUG/MEDIUM: mux-h2: synchronize all conditions to create a new backend
  stream
- MINOR: hlua: Add support for lua 5.5
- DOC: reg-tests: update VTest upstream link in the starting guide
- BUG/MINOR: config: check capture pool creations for failures
- BUG/MEDIUM: debug: only dump Lua state when panicking

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.10-0
- BUG/MEDIUM: mworker/listener: ambiguous use of RX_F_INHERITED with shards
- BUG/MEDIUM: h1-htx: Don't set HTX_FL_EOM flag on 1xx informational messages
- BUG/MINOR: http-ana: Reset analyse_exp date after 'wait-for-body' action
- BUG/MEDIUM: applet: Fix conditions to detect spinning loop with the new API
- BUG/MEDIUM: cli: State the cli have no more data to deliver if it yields
- BUG/MINOR: acme: handle multiple auth with the same name
- BUG/MINOR: acme: prevent creating map entries with dns-01
- BUG/MINOR: acme: better challenge_ready processing
- BUG/MINOR: acme: warning â€˜ctxâ€™ may be used uninitialized
- BUG/MINOR: acme: fix ha_alert() call
- BUG/MINOR: jwt: Missing "case" in switch statement
- BUG/MEDIUM: connection: fix "bc_settings_streams_limit" typo
- DOC: config: mention clearer that the cache's total-max-size is mandatory
- DOC: config: reorder the cache section's keywords
- BUG/MINOR: quic/ssl: crash in ClientHello callback ssl traces
- MINOR: quic: Add useful debugging traces in qc_idle_timer_do_rearm()
- BUG/MINOR: ssl: Don't allow to set NULL sni
- BUG/MEDIUM: http-ana: Don't close server connection on read0 in TUNNEL mode
- DOC: config: Fix description of the spop mode
- DOC: config: Improve spop mode documentation
- MINOR: h2/trace: emit a trace of the received RST_STREAM type
- MINOR: hlua: emit a log instead of an alert for aborted actions due to
  unavailable yield
- BUG/MEDIUM: quic: support some ciphersuites and curves related options
- BUG/MINOR: cfgparse-listen: update err_code for fatal error on proxy
  directive
- MEDIUM: h1: Immediately try to read data for frontend
- MEDIUM: mux-h2: do not needlessly refrain from sending data early
- MINOR: mux-h2: extract the code to send preface+settings into its own
  function
- BUG/MINOR: mux-h2: send the preface along with the first request if needed
- MINOR: cfgdiag: adjust diag on servers
- BUG/MINOR: check: only try connection reuse for http-check rulesets
- MINOR: quic: adjust CID conn tree alloc in qc_new_conn()
- MINOR: quic: split CID alloc/generation function
- BUG/MEDIUM: quic: handle collision on CID generation
- BUG/MEDIUM: quic: Don't try to use hystart if not implemented

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.9-0
- MINOR: ssl/sample: expose ssl_*c_curve for AWS-LC
- Revert "BUG/MEDIUM: connections: permit to permanently remove an idle conn"
- BUG/MEDIUM: connection: do not reinsert a purgeable conn in idle list
- BUG/MEDIUM: connection/ssl: also fix the ssl_sock_io_cb() regarding idle
  list
- BUG/MINOR: config: Limit "tune.maxpollevents" parameter to 1000000
- BUG/MEDIUM: stick-tables: Make sure updates are seen as local
- BUG/MINOR: quic: close connection on CID alloc failure
- BUG/MINOR: acme: more explicit error when BIO_new_file()
- BUG/MEDIUM: acme: move from mt_list to a rwlock + ebmbtree
- BUG/MINOR: acme: can't override the default resolver
- BUG/MINOR: check: fix reuse-pool if MUX inherited from server
- DOC: configuration: add missing ssllib_name_startswith()
- DOC: configuration: add missing openssl_version predicates
- BUG/MEDIUM: stick-tables: Always return the good stksess from
  stktable_set_entry
- BUG/MINOR: stick-tables: Fix return value for __stksess_kill()
- MINOR: h1: h1_release() should return if it destroyed the connection
- BUG/MEDIUM: h1: prevent a crash on HTTP/2 upgrade
- BUG/MINOR: quic-be: backend SSL session reuse fix (OpenSSL 3.5)
- BUG/MEDIUM: mworker: signals inconsistencies during startup and reload
- BUG/MINOR: mworker: wrong signals during startup
- BUG/MINOR: ssl: remove dead code in ssl_sock_from_buf()
- BUG/MINOR: acme: alert when the map doesn't exist at startup
- DOC: acme: add details about the DNS-01 support
- DOC: acme: explain how to dump the certificates
- DOC: acme: configuring acme needs a crt file
- BUG/MEDIUM: queues: Don't forget to unlock the queue before exiting
- MINOR: muxes: Support an optional ALPN string when defining mux protocols
- MINOR: config: Do proto detection for listeners before checks about ALPN
- BUG/MEDIUM: config: Use the mux protocol ALPN by default for listeners if
  forced
- BUG/MEDIUM: proxy: do not align proxy_per_tgroup beyond allocator's
  capabilities
- ADMIN: haproxy-dump-certs: implement a certificate dumper
- ADMIN: dump-certs: don't update the file if it's up to date
- ADMIN: dump-certs: create files in a tmpdir
- ADMIN: dump-certs: fix lack of / in -p
- ADMIN: dump-certs: use same error format as haproxy
- ADMIN: dump-certs: let dry-run compare certificates
- DOC: http: document 413 response code

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.8-0
- BUG/MEDIUM: mt_lists: Avoid el->prev = el->next = el
- BUG/MEDIUM: applet: Improve again spinning loops detection with the new API
- BUG/MINOR: stick-tables: properly index string-type keys
- BUG/MEDIUM: mt_list: Use atomic operations to prevent compiler optims
- MINOR: applet: do not put SE_FL_WANT_ROOM on rcv_buf() if the channel is
  empty
- MINOR: cli: create cli_raw_rcv_buf() from the generic applet_raw_rcv_buf()
- BUG/MEDIUM: cli: do not return ACKs one char at a time
- MINOR: backend: srv_queue helper
- MINOR: backend: srv_is_up converter
- BUG/MEDIUM: ssl: Crash because of dangling ckch_store reference in a ckch
  instance
- DOC: config: slightly clarify the ssl_fc_has_early() behavior
- MINOR: ssl-sample: add ssl_fc_early_rcvd() to detect use of early data
- MINOR: http: fix 405,431,501 default errorfile
- BUG/MINOR: init: Do not close previously created fd in stdio_quiet
- BUG/MINOR: resolvers: Apply dns-accept-family setting on additional records
- BUG/MINOR: ssl: returns when SSL_CTX_new failed during init
- BUG/MINOR: resolvers: ensure fair round robin iteration
- OPTIM: backend: skip conn reuse for incompatible proxies
- SCRIPTS: build-ssl: fix rpath in AWS-LC install for openssl and bssl bin
- BUG/MEDIUM: mux-h1: fix 414 / 431 status code reporting
- BUG/MEDIUM: mux-h2: make sure not to move a dead connection to idle
- BUG/MEDIUM: connections: permit to permanently remove an idle conn
- BUG/MEDIUM: server: close a race around ready_srv when deleting a server
- BUG/MINOR: acme: wrong dns-01 challenge in the log

* Sat Mar 21 2026 Anton Novojilov <andy@essentialkaos.com> - 3.2.7-0
- BUG/MINOR: acme: avoid overflow when diff > notAfter
- BUG/MINOr: hlua: Fix receive from HTTP applet by properly accounting data
- BUG/MEDIUM: ssl: take care of second client hello
- BUG/MINOR: ssl: always clear the remains of the first hello for the second
  one
- BUG/MINOR: ssl: leak in ssl-f-use
- BUG/MINOR: ssl: leak crtlist_name in ssl-f-use
- BUILD: makefile: disable tail calls optimizations with memory profiling
- BUG/MEDIUM: apppet: Improve spinning loop detection with the new API
- BUG/MINOR: sink: retry attempt for sft server may never occur
- MINOR: debug: add distro name and version in postmortem
- BUG/MINOR: ssl: Free global_ssl structure contents during deinit
- BUG/MINOR: ssl: Free key_base from global_ssl structure during deinit
- BUG/MINOR: ssl: Potential NULL deref in trace macro
- TESTS: quic: useless param for b_quic_dec_int()
- BUG/MEDIUM: pools: fix crash on filtered "show pools" output
- BUG/MINOR: pools: don't report "limited to the first X entries" by default
- BUG/MAJOR: lb-chash: fix key calculation when using default hash-key id
- BUILD: ssl: can't build when using -DLISTEN_DEFAULT_CIPHERS
- BUG/MINOR: quic: too short PADDING frame for too short packets
- MINOR: quic: restore QUIC_HP_SAMPLE_LEN constant
- BUG/MEDIUM: stick-tables: Don't forget to dec count on failure.
- BUG/MINOR: quic: check applet_putchk() for 'show quic' first line
- DOC: clarify the experimental status for certain features
- BUG/MEDIUM: threads/config: drop absent threads from thread groups
- BUG/MEDIUM: mt_list: Make sure not to unlock the element twice
- BUG/MEDIUM: cli: also free the trash chunk on the error path
- BUG/MINOR: quic: SSL counters not handled
- BUG/MAJOR: quic: uninitialized quic_conn_closed struct members
- BUG/MEDIUM: h3: properly encode response after interim one in same buf
- MINOR: ncbuf: extract common types
- MINOR: ncbmbuf: define new ncbmbuf type
- MINOR: ncbmbuf: implement add
- MINOR: ncbmbuf: implement iterator bitmap utilities functions
- MINOR: ncbmbuf: implement ncbmb_data()
- MINOR: ncbmbuf: implement advance operation
- MINOR: ncbmbuf: add tests as standalone mode
- BUG/MAJOR: quic: use ncbmbuf for CRYPTO handling
- BUG/MEDIUM: build: limit excessive and counter-productive gcc-15
  vectorization
- MINOR: acme: acme-vars allow to pass data to the dpapi sink
- MINOR: acme: check acme-vars allocation during escaping
- CLEANUP: acme: acme_will_expire() uses acme_schedule_date()
- MINOR: acme: provider-name for dpapi sink
- BUILD: acme: fix false positive null pointer dereference
- MINOR: acme: implement "reuse-key" option
- MEDIUM: acme: don't insert acme account key in ckchs_tree
- BUG/MINOR: acme: memory leak from the config parser
- MINOR: acme: add the dns-01-record field to the sink
- MINOR: acme: display the complete challenge_ready command in the logs

* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.6-0
- MINOR: stick-tables: limit the number of visited nodes during expiration
- OPTIM: stick-tables: exit expiry faster when the update lock is held
- MINOR: server: Parse sni and pool-conn-name expressions in a dedicated
  function
- BUG/MEDIUM: server: Use sni as pool connection name for SSL server only
- BUG/MINOR: server: Update healthcheck when server settings are changed via
  CLI
- BUG/MINOR: tcpcheck: Don't use sni as pool-conn-name for non-SSL
  connections
- MINOR: debug: report the process id in warnings and panics
- DEBUG: stream: count the number of passes in the connect loop
- MINOR: debug: report the number of loops and ctxsw for each thread
- MINOR: debug: report the time since last wakeup and call
- DEBUG: peers: export functions that use locks
- MINOR: stick-table: permit stksess_new() to temporarily allocate more
  entries
- MEDIUM: stick-tables: relax stktable_trash_oldest() to only purge what is
  needed
- MEDIUM: stick-tables: give up on lock contention in process_table_expire()
- MEDIUM: stick-tables: don't wait indefinitely in stktable_add_pend_updates
  ()
- MEDIUM: peers: don't even try to process updates under contention
- MEDIUM: stick-table: move process_table_expire() to a single thread
- MEDIUM: peers: move process_peer_sync() to a single thread
- MINOR: activity: indicate the number of calls on "show tasks"
- MINOR: tools: don't emit "+0" for symbol names which exactly match known
  ones
- BUG/MEDIUM: resolvers: Properly cache do-resolv resolution
- BUG/MINOR: resolvers: Restore round-robin selection on records in DNS
  answers
- BUG/MEDIUM: resolvers: Test for empty tree when getting a record from DNS
  answer
- BUG/MEDIUM: resolvers: Make resolution owns its hostname_dn value
- BUG/MEDIUM: resolvers: Accept to create resolution without hostname
- BUG/MEDIUM: resolvers: Wake resolver task up whne unlinking a stream
  requester
- OPTIM: sink: reduce contention on sink_announce_dropped()
- MEDIUM: dns: bind the nameserver sockets to the initiating thread
- MEDIUM: resolvers: make the process_resolvers() task single-threaded
- BUG/MINOR: acme/cli: wrong description for "acme challenge_ready"
- BUG/MEDIUM: stick-tables: Don't let table_process_entry() handle refcnt
- BUG/MINOR: pools: Fix the dump of pools info to deal with buffers
  limitations
- BUILD: halog: misleading indentation in halog.c
- CI: github: build halog on the vtest job
- BUG/MINOR: acme: don't unlink from acme_ctx_destroy()
- BUG/MEDIUM: acme: cfg_postsection_acme() don't init correctly acme sections
- BUG/MEDIUM: acme: free() of i2d_X509_REQ() with AWS-LC
- MINOR: sched: let's permit to share the local ctx between threads
- MINOR: sched: pass the thread number to is_sched_alive()
- BUG/MEDIUM: wdt: improve stuck task detection accuracy
- MINOR: ssl: add the ssl_bc_sni sample fetch function to retrieve backend
  SNI
- BUG/MINOR: compression: Test payload size only if content-length is
  specified
- BUG/MINOR: pattern: Properly flag virtual maps as using samples
- BUG/MINOR: acme: possible overflow on scheduling computation
- BUG/MINOR: acme: possible overflow in acme_will_expire()
- BUG/MINOR: pattern: Fix pattern lookup for map with opt@ prefix
- BUG/MEDIUM: ssl: ca-file directory mode must read every certificates of a
  file
- MINOR: mt_list: Implement MT_LIST_POP_LOCKED()
- BUG/MEDIUM: stick-tables: Make sure not to free a pending entry
- MEDIUM: servers: Schedule the server requeue target on creation
- MEDIUM: fwlc: Make it so fwlc_srv_reposition works with unqueued srv
- BUG/MEDIUM: fwlc: Handle memory allocation failures.
- DOC: config: clarify some known limitations of the json_query() converter
- BUG/CRITICAL: mjson: fix possible DoS when parsing numbers
- BUG/MINOR: h2: forbid 'Z' as well in header field names checks
- BUG/MINOR: h3: forbid 'Z' as well in header field names checks
- BUG/MEDIUM: resolvers: break an infinite loop in
  resolv_get_ip_from_response()

* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.5-0
- BUG/MEDIUM: stconn: Fix conditions to know an applet can get data from
  stream
- BUG/MEDIUM: Remove sync sends from streams to applets
- MINOR: quic: implement qc_ssl_do_hanshake()
- BUG/MEDIUM: quic: listener connection stuck during handshakes (OpenSSL 3.5)
- BUG/MINOR: mux-h1: fix wrong lock label
- MEDIUM: dns: don't call connect to dest socket for AF_INET*
- BUG/MINOR: spoe: Properly detect and skip empty NOTIFY frames
- BUG/MEDIUM: cli: Report inbuf is no longer full when a line is consumed
- BUG/MEDIUM: mworker: more verbose error upon loading failure
- BUG/MEDIUM: mux-h2: fix crash on idle-ping due to unwanted ABORT_NOW
- BUG/MEDIUM: ssl: apply ssl-f-use on every "ssl" bind
- MINOR: dns: dns_connect_nameserver: fix fd leak at error path
- BUG/MEDIUM: quic: reset padding when building GSO datagrams
- BUG/MINOR: quic: do not emit probe data if CONNECTION_CLOSE requested
- BUG/MAJOR: quic: fix INITIAL padding with probing packet only
- BUG/MINOR: quic: don't coalesce probing and ACK packet of same type
- MINOR: quic: centralize padding for HP sampling on packet building
- MINOR: http_ana: fix typo in http_res_get_intercept_rule
- BUG/MEDIUM: mux-spop: Reject connection attempts from a non-spop frontend
- BUG/MEDIUM: http_ana: handle yield for "stats http-request" evaluation
- BUG/MEDIUM: spoe: Improve error detection in SPOE applet on client abort
- MINOR: sample: Add le2dec (little endian to decimal) sample fetch
- MINOR: sample: Add base2 converter
- BUG/MINOR: quic: reorder fragmented RX CRYPTO frames by their offsets
- MINOR: ssl: diagnostic warning when both 'default-crt' and 'strict-sni' are
  used
- DOC: configuration: clarify 'default-crt' and implicit default certificates
- MINOR: quic: remove ->offset qf_crypto struct field
- BUG/MINOR: mux-quic: trace with non initialized qcc
- BUG/MINOR: acl: set arg_list->kw to aclkw->kw string literal if aclkw is
  found
- BUG/MEDIUM: mworker: fix startup and reload on macOS
- BUG/MINOR: connection: rearrange union list members
- BUG/MINOR: connection: remove extra session_unown_conn() on reverse
- BUG/MINOR: server: decrement session idle_conns on del server
- BUILD: mworker: fix ignoring return value of â€˜readâ€™
- DOC: unreliable sockpair@ on macOS
- DOC: configuration: confuse "strict-mode" with "zero-warning"
- MINOR: doc: add missing statistics column
- MINOR: doc: add missing statistics column
- CLEANUP: quic: remove a useless CRYPTO frame variable assignment
- BUG/MEDIUM: quic: CRYPTO frame freeing without eb_delete()
- BUG/MAJOR: mux-quic: fix crash on reload during emission
- REG-TESTS: map_redirect: Don't use hdr_dom in ACLs with "-m end" matching
  method
- BUG/MEDIUM: server: Duplicate healthcheck's alpn inherited from default
  server
- BUG/MINOR: halog: Add OOM checks for calloc() in filter_count_srv_status
  () and filter_count_url()
- BUG/MINOR: log: Add OOM checks for calloc() and malloc() in logformat parser
  and dup_logger()
- BUG/MINOR: acl: Add OOM check for calloc() in smp_fetch_acl_parse()
- BUG/MINOR: cfgparse: Add OOM check for calloc() in cfg_parse_listen()
- BUG/MINOR: compression: Add OOM check for calloc() in
  parse_compression_options()
- BUG/MINOR: tools: Add OOM check for malloc() in indent_msg()
- BUG/MINOR: quic: ignore AGAIN ncbuf err when parsing CRYPTO frames
- BUG/MINOR: quic: fix room check if padding requested
- BUG/MINOR: quic: fix padding issue on INITIAL retransmit
- BUG/MINOR: haproxy: be sure not to quit too early on soft stop
- BUILD: acl: silence a possible null deref warning in parse_acl_expr()
- MINOR: quic: Add more information about RX packets
- BUG/MEDIUM: stick-tables: don't leave the expire loop with elements deleted
- BUG/MINOR: stick-tables: never leave used entries without expiration
- BUG/MEDIUM: peers: don't fail twice to grab the update lock
- BUG/MINOR: check: ensure check-reuse is compatible with SSL
- BUG/MINOR: check: fix dst address when reusing a connection
- REGTESTS: explicitly use "balance roundrobin" where RR is needed
- BUG/MEDIUM: conn: fix UAF on connection after reversal on edge
- BUG/MINOR: connection: streamline conn detach from lists
- BUG/MINOR: log: fix potential memory leak upon error in
  add_to_logformat_list()
- BUILD: trace: silence a bogus build warning at -Og
- BUG/MINOR: cpu_topo: work around a small bug in musl's CPU_ISSET()
- CLEANUP: quic: fix typo in quic_tx trace
- BUG/MEDIUM: mux-h2: Reset MUX blocking flags when a send error is caught
- BUG/MEDIUM: mux-h2; Don't block reveives in H2_CS_ERROR and H2_CS_ERROR2
  states
- BUG/MEDIUM: mux-h2: Restart reading when mbuf ring is no longer full
- BUG/MINOR: mux-h2: Remove H2_CF_DEM_DFULL flags when the demux buffer is
  reset
- BUG/MEDIUM: mux-h2: Report RST/error to app-layer stream during 0-copy
  fwding
- BUG/MEDIUM: mux-h2: Reinforce conditions to report an error to app-layer
  stream
- OPTIM: check: do not delay MUX for ALPN if SSL not active
- BUG/MEDIUM: checks: fix ALPN inheritance from server
- BUG/MEDIUM: h1: Allow reception if we have early data
- BUG/MEDIUM: ssl: create the mux immediately on early data
- BUG/MINOR: activity: fix reporting of task latency
- BUG/MEDIUM: stick-tables: don't loop on non-expirable entries
- BUG/MINOR: stick-table: make sure never to miss a process_table_expire
  update
- BUG/MAJOR: stream: Remove READ/WRITE events on channels after analysers
  eval
- BUG/MAJOR: stream: Force channel analysis on successful synchronous send
- BUG/MINOR: acme: null pointer dereference upon allocation failure
- BUG/MEDIUM: jws: return size_t in JWS functions
- BUG/MINOR: ssl: Potential NULL deref in trace macro
- BUG/MINOR: ssl: Fix potential NULL deref in trace callback
- BUG/MINOR: ocsp: prototype inconsistency
- BUG/MEDIUM: http_ana: fix potential NULL deref in http_process_req_common()
- BUG/MINOR: ocsp: Crash when updating CA during ocsp updates
- BUG/MINOR: resolvers: always normalize FQDN from response
- BUG/MEDIUM: ring: invert the length check to avoid an int overflow
- DEBUG: stick-tables: export stktable_add_pend_updates() for better
  reporting
- BUG/MEDIUM: pattern: fix possible infinite loops on deletion (try 2)

* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- DOC: deviceatlas build clarifications
- BUG/MEDIUM: ssl/clienthello: ECDSA with ssl-max-ver TLSv1.2 and no ECDSA
  ciphers
- BUG/MEDIUM: acme: use POST-as-GET instead of GET for resources
- MINOR: acme: remove acme_req_auth() and use acme_post_as_get() instead
- BUG/MINOR: acme: allow "processing" in challenge requests
- CLEANUP: acme: fix wrong spelling of "resources"
- MINOR: acme: add ACME to the haproxy -vv feature list
- MINOR: acme: implement traces
- BUG/MINOR: hlua: Skip headers when a receive is performed on an HTTP applet
- BUG/MEDIUM: hlua: Report to SC when data were consumed on a lua socket
- BUG/MEDIUM: hlua: Report to SC when output data are blocked on a lua socket
- BUG/MEDIUM: dns: Reset reconnect tempo when connection is finally
  established
- BUG/MEDIUM: logs: fix sess_build_logline_orig() recursion with options
- BUG/MINOR: hlua: take default-path into account with lua-load-per-thread
- BUG/MEDIUM: mux-quic: ensure Early-data header is set
- CLEANUP: ssl: Rename ssl_trace-t.h to ssl_trace.h
- BUILD: acme: avoid declaring TRACE_SOURCE in acme-t.h
- BUG/MEDIUM: hlua_fcn: ensure systematic watcher cleanup for server list
  iterator
- MINOR: acme: emit a log for DNS-01 challenge response
- MINOR: acme: emit the DNS-01 challenge details on the dpapi sink
- MEDIUM: acme: allow to wait and restart the task for DNS-01
- MINOR: acme: update the log for DNS-01
- BUG/MINOR: acme: possible integer underflow in acme_txt_record()
- MEDIUM: acme: use lowercase for challenge names in configuration
- DOC: management: clarify usage of -V with -c
- MEDIUM: ssl/cli: relax crt insertion in crt-list of type directory
- BUG/MINOR: listener: really assign distinct IDs to shards
- MINOR: quic: Prevent QUIC build with OpenSSL 3.5 new QUIC API version <
  3.5.1
- BUG/MEDIUM: quic: Crash after QUIC server callbacks restoration
  (OpenSSL 3.5)
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
- MINOR: h1-htx: Add function to format an HTX message in its H1
  representation
- BUG/MINOR: mux-h1: Use configured error files if possible for early H1
  errors
- BUG/MINOR: h1-htx: Don't forget to init flags in h1_format_htx_msg function
- BUG/MEDIUM: h3: do not overwrite interim with final response
- BUG/MINOR: h3: properly realloc buffer after interim response encoding
- BUG/MINOR: h3: ensure that invalid status code are not encoded (FE side)
- MINOR: qmux: change API for snd_buf FIN transmission
- BUG/MEDIUM: h3: handle interim response properly on FE side
- BUG/MINOR: quic: Wrong source address use on FreeBSD
- MINOR: h3: remove unused outbuf in h3_resp_headers_send()
- BUG/MINOR: applet: Don't trigger BUG_ON if the tid is not on appctx init
- BUG/MINOR: halog: exit with error when some output filters are set
  simultaneosly
- BUG/MEDIUM: threads: Disable the workaround to load libgcc_s on macOS
- BUG/MINOR: logs: fix log-steps extra log origins selection
- BUG/MINOR: hq-interop: fix FIN transmission
- BUG/MINOR mux-quic: apply correctly timeout on output pending data
- BUG/MINOR: mux-quic: ensure close-spread-time is properly applied
- CLEANUP: http-client: Remove useless indentation when sending request body
- DOC: list missing global QUIC settings
- BUILD: compat: provide relaxed versions of the MIN/MAX macros
- BUILD: compat: always set _POSIX_VERSION to ease comparisons
- BUG/MINOR: stick-table: cap sticky counter idx with tune.nb_stk_ctr instead
  of MAX_SESS_STKCTR
- MINOR: sock: update broken accept4 detection for older hardwares.
- BUG/MEDIUM: ssl: Fix 0rtt to the server
- BUG/MEDIUM: ssl: fix build with AWS-LC
- BUG/MINOR: init: Initialize random seed earlier in the init process
- DOC: management: fix typo in commit f4f93c56
- DOC: config: recommend single quoting passwords
- BUG/MEDIUM: mux-quic: adjust wakeup behavior
- BUG/MEDIUM: http-client: Test HTX_FL_EOM flag before commiting the HTX
  buffer

* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- CI: enable USE_QUIC=1 for OpenSSL versions >= 3.5.0
- CI: github: add an OpenSSL 3.5.0 job
- CI: github: update the stable CI to ubuntu-24.04
- BUILD: quic: QUIC build against OpenSSL 3.5 broken
- BUG/MEDIUM: quic: SSL/TCP handshake failures with OpenSSL 3.5
- CI: github: update to OpenSSL 3.5.1
- BUG/MINOR: quic: Missing TLS 1.3 QUIC cipher suites and groups inits
  (OpenSSL 3.5 QUIC API)
- BUG/MINOR: ssl/ocsp: fix definition discrepancies with ocsp_update_init()
- BUG/MINOR: ssl: crash in ssl_sock_io_cb() with SSL traces and idle
  connections
- BUG/MINOR: http-act: Fix parsing of the expression argument for pause action
- BUILD/MEDIUM: deviceatlas: fix when installed in custom locations.

* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- BUG/MINOR: config/server: reject QUIC addresses
- BUG/MINOR: http-ana: Properly handle keep-query redirect option if no QS
- BUG/MINOR: quic: Fix OSSL_FUNC_SSL_QUIC_TLS_got_transport_params_fn
  callback (OpenSSL3.5)
- BUG/MEDIUM: cli: Don't consume data if outbuf is full or not available
- MINOR: cli: handle EOS/ERROR first
- BUG/MEDIUM: check: Set SOCKERR by default when a connection error is
  reported
- DOC: config: prefer-last-server: add notes for non-deterministic algorithms
- BUG/MINOR: mux-quic/h3: properly handle too low peer fctl initial stream
- BUG/MAJOR: fwlc: Count an avoided server as unusable.
- MINOR: fwlc: Factorize code.
- BUG/MINOR: tools: only reset argument start upon new argument
- BUG/MINOR: stream: Avoid recursive evaluation for unique-id based on itself
- BUG/MINOR: log: Be able to use %%ID alias at anytime of the stream's
  evaluation
- DOC: configuration: add details on prefer-client-ciphers
- BUG/MINOR: quic: wrong QUIC_FT_CONNECTION_CLOSE(0x1c) frame encoding
- MINOR: quic: Useless TX buffer size reduction in closing state
- DOC: config: crt-list clarify default cert + cert-bundle
- SCRIPTS: drop the HTML generation from announce-release
- BUG/MINOR: tools: use my_unsetenv instead of unsetenv
- MINOR: ssl: check TLS1.3 ciphersuites again in clienthello with recent
  AWS-LC
- BUG/MEDIUM: hlua: Forbid any L6/L7 sample fetche functions from lua
  services
- BUG/MEDIUM: mux-h2: Properly handle connection error during preface sending
- BUG/MINOR: jwt: Copy input and parameters in dedicated buffers in jwt_verify
  converter
- DOC: Fix 'jwt_verify' converter doc
- BUG/MINOR: httpclient: wrongly named httpproxy flag
- BUILD: dev/phash: remove the accidentally committed a.out file

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- BUILD: tools: properly define ha_dump_backtrace() to avoid a build warning
- DOC: config: Fix a typo in 2.7 (Name format for maps and ACLs)
- BUG/MAJOR: leastconn: Protect tree_elt with the lbprm lock
- BUG/MEDIUM: check: Requeue healthchecks on I/O events to handle check timeout
- BUG/MINOR: mux-spop: Fix null-pointer deref on SPOP stream allocation failure
- BUG/MEDIUM: cli: Properly parse empty lines and avoid crashed
- BUG/MINOR: config: emit warning for empty args only in discovery mode
- BUG/MINOR: config: fix arg number reported on empty arg warning
- BUG/MINOR: quic: Missing SSL session object freeing
- BUG/MEDIUM: fd: Use the provided tgid in fd_insert() to get tgroup_info
- BUG/MINIR: h1: Fix doc of 'accept-unsafe-...-request' about URI parsing

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- Initial build for kaos repository
