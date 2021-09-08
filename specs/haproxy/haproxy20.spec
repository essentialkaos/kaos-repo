################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __sysctl          %{_bindir}/systemctl

%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __userdel         %{_sbindir}/userdel
%define __getent          %{_bindir}/getent

################################################################################

%define orig_name         haproxy
%define major_ver         20

%define hp_user           %{orig_name}
%define hp_user_id        188
%define hp_group          %{orig_name}
%define hp_group_id       188
%define hp_homedir        %{_localstatedir}/lib/%{orig_name}
%define hp_confdir        %{_sysconfdir}/%{orig_name}
%define hp_datadir        %{_datadir}/%{orig_name}

%define lua_ver           5.4.3
%define pcre_ver          8.45
%define openssl_ver       1.1.1k
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              %{orig_name}%{major_ver}
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.0.25
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.0/src/%{orig_name}-%{version}.tar.gz
Source1:           %{orig_name}.init
Source2:           %{orig_name}.cfg
Source3:           %{orig_name}.logrotate
Source4:           %{orig_name}.sysconfig
Source5:           %{orig_name}.service

Source10:          https://www.lua.org/ftp/lua-%{lua_ver}.tar.gz
Source11:          https://ftp.pcre.org/pub/pcre/pcre-%{pcre_ver}.tar.gz
Source12:          https://www.openssl.org/source/openssl-%{openssl_ver}.tar.gz
Source13:          https://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{ncurses_ver}.tar.gz
Source14:          https://ftp.gnu.org/gnu/readline/readline-%{readline_ver}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make zlib-devel
BuildRequires:     devtoolset-7-gcc-c++ devtoolset-7-binutils

Requires:          setup >= 2.8.14-14 kaosv >= 2.16

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Provides:          %{name} = %{version}-%{release}

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

# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-7/root/usr/bin:$PATH"

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static OpenSSL build
pushd openssl-%{openssl_ver}
  mkdir build
  ./config --prefix=$(pwd)/build no-shared no-threads
  %{__make} -j1
  %{__make} -j1 install_sw
popd

# Static NCurses build
pushd ncurses-%{ncurses_ver}
  mkdir build
  ./configure --prefix=$(pwd)/build --enable-shared=no
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

# Static readline build
pushd readline-%{readline_ver}
  mkdir build
  ./configure --prefix=$(pwd)/build --enable-static=true
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

# Static Lua build
pushd lua-%{lua_ver}
  mkdir build
  %{__make} %{?_smp_mflags} MYCFLAGS="-I$BUILDDIR/readline-%{readline_ver}/build/include" \
                            MYLDFLAGS="-L$BUILDDIR/readline-%{readline_ver}/build/lib -L$BUILDDIR/ncurses-%{ncurses_ver}/build/lib -lreadline -lncurses" \
                            linux
  %{__make} %{?_smp_mflags} INSTALL_TOP=$(pwd)/build install
popd

# Static PCRE build
pushd pcre-%{pcre_ver}
  mkdir build
  ./configure --prefix=$(pwd)/build \
              --enable-shared=no \
              --enable-utf8 \
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
                          SSL_LIB=openssl-%{openssl_ver}/build/lib \
                          USE_PCRE_JIT=1 \
                          USE_STATIC_PCRE=1 \
                          PCRE_INC=pcre-%{pcre_ver}/build/include \
                          PCRE_LIB=pcre-%{pcre_ver}/build/lib \
                          USE_LUA=1 \
                          LUA_INC=lua-%{lua_ver}/build/include \
                          LUA_LIB=lua-%{lua_ver}/build/lib \
                          USE_ZLIB=1 \
                          ADDLIB="-ldl -lrt -lpthread" \
                          ${use_regparm}

pushd contrib/halog
  %{__make} halog
popd

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -pDm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{orig_name}
install -pDm 0644 %{SOURCE2} %{buildroot}%{hp_confdir}/%{orig_name}.cfg
install -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{orig_name}
install -pDm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{orig_name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/

install -pm 0755 ./contrib/halog/halog %{buildroot}%{_bindir}/halog
install -pm 0644 ./examples/errorfiles/* %{buildroot}%{hp_datadir}

for file in $(find . -type f -name '*.txt') ; do
  iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
  touch -r $file $file.new && \
  mv $file.new $file
done

%clean
rm -rf %{buildroot}

%pre
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{hp_group} >/dev/null || %{__groupadd} -g %{hp_group_id} -r %{hp_group} 2>/dev/null
  %{__getent} passwd %{hp_user} >/dev/null || %{__useradd} -r -u %{hp_user_id} -g %{hp_group} -d %{hp_homedir} -s /sbin/nologin %{hp_user} 2>/dev/null
fi

%post
if [[ $1 -eq 1 ]] ; then
  %{__sysctl} enable %{orig_name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  %{__sysctl} --no-reload disable %{orig_name}.service &>/dev/null || :
  %{__sysctl} stop %{orig_name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGELOG LICENSE README doc/* examples/*.cfg
%dir %{hp_datadir}
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{orig_name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{orig_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{orig_name}
%{hp_datadir}/*
%{_initrddir}/%{orig_name}
%{_unitdir}/%{orig_name}.service
%{_sbindir}/%{orig_name}
%{_bindir}/halog
%{_mandir}/man1/%{orig_name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Wed Sep 08 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.25-0
- BUG/MEDIUM: sock: really fix detection of early connection failures in for 2.3
- REGTESTS: abortonclose: after retries, 503 is expected, not close
- BUG/MEDIUM: base64: check output boundaries within base64{dec,urldec}
- MINOR: compiler: implement an ONLY_ONCE() macro
- BUG/MINOR: lua: use strlcpy2() not strncpy() to copy sample keywords
- BUG/MINOR: ebtree: remove dependency on incorrect macro for bits per long
- BUG/MINOR threads: Use get_(local|gm)time instead of (local|gm)time
- BUG/MINOR: tools: Fix loop condition in dump_text()
- CLEANUP: Add missing include guard to signal.h
- DOC: configuration: remove wrong tcp-request examples in tcp-response
- BUG/MINOR: config: reject configs using HTTP with bufsize >= 256 MB
- CLEANUP: htx: remove comments about "must be < 256 MB"
- BUG/MAJOR: htx: fix missing header name length check in htx_add_header/trailer
- Revert "BUG/MINOR: stream-int: Don't block reads in si_update_rx() if chn
  may receive"
- MINOR: action: Use a generic function to check validity of an action rule list
- REGTESTS: mark http_abortonclose as broken

* Wed Aug 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.24-0
- BUG/MEDIUM: tcp-check: Do not dereference inexisting connection
- BUILD: add detection of missing important CFLAGS
- BUG/MEDIUM: mworker: do not register an exit handler if exit is expected
- BUG/MINOR: mworker: do not export HAPROXY_MWORKER_REEXEC across programs
- BUG/MINOR: systemd: must check the configuration using -Ws
- BUG/MINOR: mux-h2: Obey dontlognull option during the preface
- BUG/MEDIUM: mux-h2: Handle remaining read0 cases on partial frames
- BUG/MINOR: connection: Add missing error labels to conn_err_code_str
- BUG/MINOR: server: update last_change on maint->ready transitions too
- MINOR: spoe: Add a pointer on the filter config in the spoe_agent structure
- BUG/MEDIUM: spoe: Create a SPOE applet if necessary when the last one
  is released
- BUG/MEDIUM: spoe: Fix policy to close applets when SPOE connections are queued
- DOC: Improve the lua documentation
- DOC: config: Fix 'http-response send-spoe-group' documentation
- MINOR: mux-h1/proxy: Add a proxy option to disable clear h2 upgrade
- DOC/MINOR: fix typo in management document
- BUG/MAJOR: h2: enforce stricter syntax checks on the :method pseudo-header
- REGTESTS: add a test to prevent h2 desync attacks

* Wed Aug 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.23-0
- DOC: Explicitly state only IPv4 are supported by forwardfor/originalto options
- BUG/MINOR: tools: fix parsing "us" unit for timers
- DOC: clarify that compression works for HTTP/2
- BUG/MEDIUM: sample: Fix adjusting size in field converter
- BUG/MEDIUM: threads: Ignore current thread to end its harmless period
- BUG/MINOR: http-fetch: Make method smp safe if headers were already forwarded
- BUG/MINOR: http_htx: Remove BUG_ON() from http_get_stline() function
- BUG/MINOR: logs: Report the true number of retries if there was no connection
- BUG/MINOR: mux-h1: Release idle server H1 connection if data are received
- BUG/MINOR: server: free srv.lb_nodes in free_server
- BUG/MAJOR: mux-h2: Properly detect too large frames when decoding headers
- BUG/MEDIUM: mux-h2: Fix dfl calculation when merging CONTINUATION frames
- BUG/MEDIUM: config: fix cpu-map notation with both process and threads
- BUG/MINOR: mworker/init: don't reset nb_oldpids in non-mworker cases
- BUG/MINOR: mworker: don't use oldpids[] anymore for reload
- BUG/MEDIUM: mux-h2: Properly handle shutdowns when received with data
- BUG/MINOR: peers: remove useless table check if initial resync is finished
- BUG/MEDIUM: peers: re-work connection to new process during reload.
- BUG/MEDIUM: peers: re-work refcnt on table to protect against flush
- BUG/MINOR: htx: Preserve HTX flags when draining data from an HTX message
- BUG/MINOR: applet: Notify the other side if data were consumed by an applet
- BUG/MEDIUM: peers: initialize resync timer to get an initial full resync
- BUG/MEDIUM: peers: register last acked value as origin receiving a resync req
- BUG/MEDIUM: peers: stop considering ack messages teaching a full resync
- BUG/MEDIUM: peers: reset starting point if peers appears longly disconnected
- BUG/MEDIUM: peers: reset commitupdate value in new conns
- BUG/MEDIUM: peers: re-work updates lookup during the sync on the fly
- BUG/MEDIUM: peers: reset tables stage flags stages on new conns
- MINOR: peers: add informative flags about resync process for debugging
- MINOR: hlua: Add error message relative to the Channel manipulation and
  HTTP mode
- BUG/MINOR: hlua: Don't rely on top of the stack when using Lua buffers
- BUG/MEDIUM: cli: prevent memory leak on write errors
- BUG/MINOR: stream: Decrement server current session counter on L7 retry
- BUG/MINOR: stream: properly clear the previous error mask on L7 retries
- BUG/MINOR: stream: Reset stream final state and si error type on L7 retry
- BUG/MINOR: http_fetch: fix possible uninit sockaddr in fetch_url_ip/port
- MINOR: channel: Rely on HTX version if appropriate in channel_may_recv()
- BUG/MINOR: stream-int: Don't block reads in si_update_rx() if chn may receive
- MEDIUM: mux-h1: Don't block reads when waiting for the other side
- REGTESTS: Add script to test abortonclose option
- BUG/MEDIUM: ebtree: Invalid read when looking for dup entry
- BUG/MAJOR: server: prevent deadlock when using 'set maxconn server'
- BUG/MEDIUM: filters: Exec pre/post analysers only one time per filter
- BUG/MINOR: http-comp: Preserve HTTP_MSGF_COMPRESSIONG flag on the response
- BUG/MINOR: http-ana: Handle L7 retries on refused early data before K/A aborts
- BUG/MINOR: server: Missing calloc return value check in srv_parse_source
- BUG/MINOR: peers: Missing calloc return value check in peers_register_table
- BUG/MINOR: ssl: Missing calloc return value check in ssl_init_single_engine
- BUG/MINOR: http: Missing calloc return value check in parse_http_req_capture
- BUG/MINOR: proxy: Missing calloc return value check in proxy_parse_declare
- BUG/MINOR: proxy: Missing calloc return value check in proxy_defproxy_cpy
- BUG/MINOR: http: Missing calloc return value check while parsing
  tcp-request/tcp-response
- BUG/MINOR: http: Missing calloc return value check while parsing
  tcp-request rule
- BUG/MINOR: compression: Missing calloc return value check in
  comp_append_type/algo
- BUG/MINOR: worker: Missing calloc return value check in
  mworker_env_to_proc_list
- BUG/MINOR: http: Missing calloc return value check while parsing redirect rule
- BUG/MINOR: http: Missing calloc return value check in make_arg_list
- BUG/MINOR: proxy: Missing calloc return value check in chash_init_server_tree
- BUG/MINOR: ssl: OCSP stapling does not work if expire too far in the future
- BUG/MEDIUM: compression: Add a flag to know the filter is still
  processing data
- BUG/MEDIUM: dns: reset file descriptor if send returns an error
- BUG/MAJOR: htx: Fix htx_defrag() when an HTX block is expanded
- DOC: lua: Add a warning about buffers modification in HTTP
- BUG/MINOR: stick-table: insert srv in used_name tree even with fixed id
- BUG/MEDIUM: shctx: use at least thread-based locking on USE_PRIVATE_CACHE
- BUG/MINOR: ssl: use atomic ops to update global shctx stats
- BUG/MINOR: mworker: fix typo in chroot error message
- BUG/MAJOR: queue: set SF_ASSIGNED when setting strm->target on dequeue
- MINOR: mux-h2: obey http-ignore-probes during the preface
- BUG/MEDIUM: dns: send messages on closed/reused fd if fd was detected broken
- BUG/MEDIUM: spoe: Register pre/post analyzers in start_analyze
  callback function
- BUG/MAJOR: server: fix deadlock when changing maxconn via agent-check
- MINOR: tcp-act: Add set-src/set-src-port for "tcp-request content" rules
- DOC: config: Add missing actions in "tcp-request session" documentation
- BUG/MINOR: resolvers: answser item list was randomly purged or errors
- BUG/MEDIUM: server/cli: Fix ABBA deadlock when fqdn is set from the CLI
- BUG/MINOR: server/cli: Fix locking in function processing "set server" command
- BUG/MEDIUM: sock: make sure to never miss early connection failures
- BUG/MINOR: cli: fix server name output in "show fd"
- BUG/MINOR: stick-table: fix several printf sign errors dumping tables
- DOC: stick-table: add missing documentation about gpt0 stored type
- DOC: peers: fix the protocol tag name in the doc
- DOC: config: use CREATE USER for mysql-check
- BUG/MINOR: resolvers: Reset server IP when no ip is found in the response
- MINOR: resolvers: Reset server IP on error in resolv_get_ip_from_response()
- BUG/MINOR: peers: fix data_type bit computation more than 32 data_types
- Revert "MINOR: tcp-act: Add set-src/set-src-port for "tcp-request
  content" rules"
- MINOR: pools/debug: slightly relax DEBUG_DONT_SHARE_POOLS
- BUG/MINOR: pools: fix a possible memory leak in the lockless pool_flush()
- MINOR: pools: do not maintain the lock during pool_flush()
- BUG/MEDIUM: pools: Always update free_list in pool_gc().
- MEDIUM: memory: make pool_gc() run under thread isolation
- MEDIUM: pools: use a single pool_gc() function for locked and lockless
- BUG/MAJOR: pools: fix possible race with free() in the lockless variant
- CLEANUP: pools: remove now unused seq and pool_free_list
- BUG/MINOR: server-state: load SRV resolution only if params match the config
- BUG/MINOR: server: Forbid to set fqdn on the CLI if SRV resolution is enabled

* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.22-0
- MINOR: time: also provide a global, monotonic global_now_ms timer
- BUG/MEDIUM: freq_ctr/threads: use the global_now_ms variable
- MINOR/BUG: mworker/cli: do not use the unix_bind prefix for the master
  CLI socket
- MINOR: lua: Slightly improve function dumping the lua traceback
- BUG/MEDIUM: debug/lua: Use internal hlua function to dump the lua traceback
- BUG/MEDIUM: lua: Always init the lua stack before referencing the context
- BUG/MEDIUM: time: make sure to always initialize the global tick
- BUG/MEDIUM: thread: Fix a deadlock if an isolated thread is marked as harmless
- MINOR: tools: make url2ipv4 return the exact number of bytes parsed
- BUG/MINOR: http_fetch: make hdr_ip() reject trailing characters
- BUG/MEDIUM: mux-h1: make h1_shutw_conn() idempotent
- BUG/MINOR: stats: Apply proper styles in HTML status page.
- BUG/MINOR: tcp: fix silent-drop workaround for IPv6
- BUILD: tcp: use IPPROTO_IPV6 instead of SOL_IPV6 on FreeBSD/MacOS
- BUG/MINOR: http_fetch: make hdr_ip() resistant to empty fields
- BUG/MAJOR: dns: fix null pointer dereference in snr_update_srv_status
- BUG/MAJOR: dns: disabled servers through SRV records never recover
- BUG/MINOR: resolvers: Unlink DNS resolution to set RMAINT on SRV resolution
- MINOR: resolvers: Use a function to remove answers attached to a resolution
- MINOR: resolvers: Purge answer items when a SRV resolution triggers an error
- MINOR: resolvers: Add function to change the srv status based on
  SRV resolution
- MINOR: resolvers: Directly call srvrq_update_srv_state() when possible
- BUG/MEDIUM: resolvers: Don't release resolution from a requester callbacks

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.21-0
- BUG/MINOR: sample: check alloc_trash_chunk return value in concat()
- BUG/MINOR: sample: Memory leak of sample_expr structure in case of error
- BUG/MINOR: init: Use a dynamic buffer to set HAPROXY_CFGFILES env variable
- BUG/MINOR: peers: Wrong "new_conn" value for "show peers" CLI command.
- BUG/MINOR: mworker: define _GNU_SOURCE for strsignal()
- BUG/MEDIUM: mux-h2: fix read0 handling on partial frames
- BUILD/MINOR: lua: define _GNU_SOURCE for LLONG_MAX
- BUG/MEDIUM: stats: add missing INF_BUILD_INFO definition
- BUG/MEDIUM: filters/htx: Fix data forwarding when payload length is unknown
- BUG/MINOR: config: fix leak on proxy.conn_src.bind_hdr_name
- DOC: management: fix "show resolvers" alphabetical ordering
- BUG/MINOR: stick-table: Always call smp_fetch_src() with a valid arg list
- BUG/MEDIUM: ssl: check a connection's status before computing a handshake
- BUG/MINOR: xxhash: make sure armv6 uses memcpy()
- BUILD: Makefile: move REGTESTST_TYPE default setting
- BUG/MEDIUM: mux-h2: handle remaining read0 cases
- BUG/MEDIUM: mux-h2: do not quit the demux loop before setting END_REACHED
- BUG/MEDIUM: mux-h2: Be sure to enter in demux loop even if dbuf is empty
- BUG/MEDIUM: mux-h1: Always set CS_FL_EOI for response in MSG_DONE state
- BUG/MINOR: server: re-align state file fields number
- BUG/MINOR: tools: Fix a memory leak on error path in parse_dotted_uints()
- BUG/MINOR: backend: hold correctly lock when killing idle conn
- BUG/MINOR: server: Fix server-state-file-name directive
- CLEANUP: deinit: release global and per-proxy server-state variables on deinit
- BUG/MEDIUM: config: don't pick unset values from last defaults section
- BUG/MINOR: cfgparse: do not mention "addr:port" as supported on proxy lines
- BUG/MINOR: server: Don't call fopen() with server-state filepath set to NULL
- CLEANUP: channel: fix comment in ci_putblk.
- BUG/MINOR: server: Remove RMAINT from admin state when loading server state
- BUG/MINOR: session: atomically increment the tracked sessions counter
- BUG/MINOR: checks: properly handle wrapping time in __health_adjust()
- BUG/MINOR: sample: Always consider zero size string samples as unsafe
- BUG/MINOR: server: Init params before parsing a new server-state line
- BUG/MINOR: server: Be sure to cut the last parsed field of a server-state line
- BUG/MEDIUM: mux-h1: Fix handling of responses to CONNECT other than 200-ok
- BUG/MINOR: sample: secure convs that accept base64 string and var name as args
- BUG/MEDIUM: vars: make functions vars_get_by_{name,desc} thread-safe
- BUG/MEDIUM: proxy: use thread-safe stream killing on hard-stop
- BUG/MEDIUM: cli/shutdown sessions: make it thread-safe
- BUG/MINOR: proxy: wake up all threads when sending the hard-stop signal
- BUG/MINOR: resolvers: new callback to properly handle SRV record errors
- BUG/MEDIUM: resolvers: Reset server address and port for obselete SRV records
- BUG/MEDIUM: resolvers: Reset address for unresolved servers
- BUG/MINOR: mux-h1: Immediately report H1C errors from h1_snd_buf()
- BUG/MINOR: http-ana: Only consider dst address to process originalto option
- BUG/MINOR: tcp-act: Don't forget to set the original port
  for IPv4 set-dst rule
- BUG/MINOR: connection: Use the client's dst family for adressless servers
- BUG/MEDIUM: spoe: Kill applets if there are pending connections
  and nbthread > 1
- DOC: spoe: Add a note about fragmentation support in HAProxy
- BUG/MINOR: http-ana: Don't increment HTTP error counter on read error/timeout
- BUG/MEDIUM: dns: Consider the fact that dns answers are case-insensitive
- BUG/MINOR: hlua: Don't strip last non-LWS char in hlua_pushstrippedstring()
- BUG/MINOR: ssl: don't truncate the file descriptor to 16 bits in debug mode
- BUG/MEDIUM: session: NULL dereference possible when accessing the listener
- BUG/MEDIUM: filters: Set CF_FL_ANALYZE on channels when filters are attached
- BUG/MINOR: proxy/session: Be sure to have a listener to increment its counters
- BUG/MINOR: session: Add some forgotten tests on session's listener
- CLEANUP: tcp-rules: add missing actions in the tcp-request error message
- BUG/MINOR: resolvers: Consider server to have no IP on DNS resolution error
- BUG/MINOR: resolvers: Reset server address on DNS error only on status change
- BUG/MINOR: resolvers: Add missing case-insensitive comparisons
  of DNS hostnames
- MINOR: time: export the global_now variable
- BUG/MINOR: freq_ctr/threads: make use of the last updated global time

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.20-0
- BUG/MINOR: pattern: a sample marked as const could be written
- BUG/MINOR: lua: set buffer size during map lookups
- BUG/MINOR: peers: Do not ignore a protocol error for dictionary entries.
- BUG/MINOR: peers: Missing TX cache entries reset.
- BUG/MEDIUM: peers: fix decoding of multi-byte length in stick-table messages
- BUG/MINOR: http-fetch: Extract cookie value even when no cookie name
- BUG/MINOR: http-fetch: Fix calls w/o parentheses of the cookie sample fetches
- BUG/MAJOR: spoe: Be sure to remove all references on a released spoe applet
- MINOR: spoe: Don't close connection in sync mode on processing timeout
- MINOR: cfgparse: tighten the scope of newnameserver variable, free it
  on error.
- BUILD: http-htx: fix build warning regarding long type in printf
- BUG/MEDIUM: filters: Forward all filtered data at the end of http filtering
- BUG/MINOR: http-ana: Don't wait for the body of CONNECT requests
- BUG/MAJOR: filters: Always keep all offsets up to date during data filtering
- BUG/MAJOR: peers: fix partial message decoding
- DOC: config: Move req.hdrs and req.hdrs_bin in L7 samples fetches section
- MINOR: plock: use an ARMv8 instruction barrier for the pause instruction
- BUG/MINOR: lua: lua-load doesn't check its parameters
- BUG/MINOR: lua: Post init register function are not executed beyond
  the first one
- BUG/MINOR: lua: Some lua init operation are processed unsafe
- MINOR: actions: Export actions lookup functions
- MINOR: actions: add a function returning a service pointer from its name
- MINOR: cli: add a function to look up a CLI service description
- BUG/MINOR: lua: warn when registering action, conv, sf, cli or applet
  multiple times
- DOC/MINOR: Fix formatting in Management Guide
- BUG/MAJOR: spoa/python: Fixing return None
- DOC: spoa/python: Fixing typo in IP related error messages
- DOC: spoa/python: Rephrasing memory related error messages
- DOC: spoa/python: Fixing typos in comments
- BUG/MINOR: spoa/python: Cleanup references for failed Module Addobject
  operations
- BUG/MINOR: spoa/python: Cleanup ipaddress objects if initialization fails
- BUG/MEDIUM: spoa/python: Fixing PyObject_Call positional arguments
- BUG/MEDIUM: spoa/python: Fixing references to None
- DOC: email change of the DeviceAtlas maintainer
- BUG/MINOR: tools: make parse_time_err() more strict on the timer validity
- BUG/MINOR: tools: Reject size format not starting by a digit
- BUG/MEDIUM: lb-leastconn: Reposition a server using the right eweight
- CLEANUP: lua: Remove declaration of an inexistant function
- CLEANUP: contrib/prometheus-exporter: typo fixes for ssl reuse metric
- REGTESTS: make use of HAPROXY_ARGS and pass -dM by default
- BUILD: Makefile: have "make clean" destroy .o/.a/.s in contrib subdirs as well
- BUG/MINOR: mux-h1: Don't set CS_FL_EOI too early for protocol upgrade requests
- BUG/MEDIUM: http-ana: Never for sending data in TUNNEL mode
- CONTRIB: halog: fix build issue caused by %%L printf format
- CONTRIB: halog: mark the has_zero* functions unused
- CONTRIB: halog: fix signed/unsigned build warnings on counts and timestamps
- BUILD: plock: remove dead code that causes a warning in gcc 11
- BUILD: hpack: hpack-tbl-t.h uses VAR_ARRAY but does not include compiler.h
- MINOR: atomic: don't use ; to separate instruction on aarch64.
- BUG/MINOR: cfgparse: Fail if the strdup() for `rule->be.name` for
  `use_backend` fails
- SCRIPTS: improve announce-release to support different tag and versions
- SCRIPTS: make announce release support preparing announces before tag exists
- BUG/MINOR: srv: do not init address if backend is disabled
- BUILD: Makefile: exclude broken tests by default
- MINOR: contrib/prometheus-exporter: export build_info
- DOC: fix some spelling issues over multiple files
- SCRIPTS: announce-release: fix typo in help message
- DOC: Add maintainers for the Prometheus exporter
- BUG/MINOR: sample: fix concat() converter's corruption with non-string
  variables

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.19-0
- DOC: ssl: crt-list negative filters are only a hint
- BUILD: makefile: Fix building with closefrom() support enabled
- BUG/MINOR: Fix several leaks of 'log_tag' in init().
- BUG/MEDIUM: queue: make pendconn_cond_unlink() really thread-safe
- MINOR: counters: fix a typo in comment
- BUG/MINOR: stats: fix validity of the json schema
- MINOR: hlua: Display debug messages on stderr only in debug mode
- BUG/MINOR: peers: Inconsistency when dumping peer status codes.
- BUG/MINOR: mux-h1: Always set the session on frontend h1 stream
- BUG/MEDIUM: mux-h2: Don't handle pending read0 too early on streams
- BUG/MINOR: http-htx: Expect no body for 204/304 internal HTTP responses
- BUG/MEDIUM: h1: Always try to receive more in h1_rcv_buf().
- BUG/MINOR: init: only keep rlim_fd_cur if max is unlimited
- BUG/MINOR: mux-h2: do not stop outgoing connections on stopping
- MINOR: fd: report an error message when failing initial allocations
- BUG/MEDIUM: task: bound the number of tasks picked from the wait queue at once
- BUG/MEDIUM: spoe: Unset variable instead of set it if no data provided
- BUG/MEDIUM: mux-h1: Get the session from the H1S when capturing bad messages
- BUG/MEDIUM: lb: Always lock the server when calling server_{take,drop}_conn
- BUG/MINOR: peers: Possible unexpected peer seesion reset after collisions.
- BUG/MINOR: queue: properly report redistributed connections
- BUG/MEDIUM: server: support changing the slowstart value from state-file
- BUG/MINOR: http-ana: Don't send payload for internal responses to HEAD
  requests
- BUG/MAJOR: mux-h2: Don't try to send data if we know it is no longer possible
- BUG/MINOR: extcheck: add missing checks on extchk_setenv()
- BUG/MINOR: log: fix memory leak on logsrv parse error
- BUG/MINOR: server: fix srv downtime calcul on starting
- BUG/MINOR: server: fix down_time report for stats
- BUG/MINOR: lua: initialize sample before using it
- BUG/MINOR: cache: Inverted variables in http_calc_maxage function
- BUG/MEDIUM: filters: Don't try to init filters for disabled proxies
- BUG/MINOR: server: Set server without addr but with dns in RMAINT on startup
- MINOR: server: Copy configuration file and line for server templates
- BUG/MEDIUM: mux-pt: Release the tasklet during an HTTP upgrade
- BUG/MINOR: filters: Skip disabled proxies during startup only
- BUG/MEDIUM: stick-table: limit the time spent purging old entries
- MINOR: http-htx: Add understandable errors for the errorfiles parsing
- BUG/MINOR: http-htx: Just warn if payload of an errorfile doesn't match
  the C-L

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.18-0
- SCRIPTS: git-show-backports: make -m most only show the left branch
- SCRIPTS: git-show-backports: emit the shell command to backport a commit
- BUG/MEDIUM: mux-h2: Don't fail if nothing is parsed for a legacy chunk
  response
- BUG/MEDIUM: mux-h1: Refresh H1 connection timeout after a synchronous send
- BUG/MEDIUM: map/lua: Return an error if a map is loaded during runtime
- BUG/MINOR: lua: Check argument type to convert it to IPv4/IPv6 arg validation
- BUG/MINOR: lua: Check argument type to convert it to IP mask in arg validation
- BUG/MINOR: snapshots: leak of snapshots on deinit()
- BUG/MINOR: stats: use strncmp() instead of memcmp() on health states
- BUG/MEDIUM: htx: smp_prefetch_htx() must always validate the direction
- BUG/MINOR: reload: do not fail when no socket is sent
- DOC: cache: Use '<name>' instead of '<id>' in error message
- BUG/MAJOR: contrib/spoa-server: Fix unhandled python call leading to memory
  leak
- BUG/MINOR: contrib/spoa-server: Ensure ip address references are freed
- BUG/MINOR: contrib/spoa-server: Do not free reference to NULL
- BUG/MINOR: contrib/spoa-server: Updating references to free in case of failure
- BUG/MEDIUM: contrib/spoa-server: Fix ipv4_address used instead of ipv6_address
- BUG/MINOR: startup: haproxy -s cause 100%% cpu
- BUG/MEDIUM: doc: Fix replace-path action description
- BUG/MEDIUM: ssl: check OCSP calloc in ssl_sock_load_ocsp()
- BUG/MINOR: threads: work around a libgcc_s issue with chrooting
- BUILD: thread: limit the libgcc_s workaround to glibc only
- MINOR: Commit .gitattributes
- CLEANUP: Update .gitignore
- BUG/MINOR: auth: report valid crypto(3) support depending on build options
- BUG/MEDIUM: mux-h1: always apply the timeout on half-closed connections
- BUILD: threads: better workaround for late loading of libgcc_s
- BUG/MEDIUM: pattern: Renew the pattern expression revision when it is pruned
- BUG/MEDIUM: http-ana: Don't wait to send 1xx responses received from servers
- BUG/MEDIUM: ssl: does not look for all SNIs before chosing a certificate
- BUG/MINOR: ssl: verifyhost is case sensitive
- BUG/MINOR: server: report correct error message for invalid port on "socks4"
- BUG/MINOR: http-fetch: Don't set the sample type during the htx prefetch
- BUG/MEDIUM: h2: report frame bits only for handled types
- BUG/MINOR: Fix memory leaks cfg_parse_peers
- BUG/MINOR: config: Fix memory leak on config parse listen
- BUG/MEDIUM: listeners: do not pause foreign listeners
- DOC: spoa-server: fix false friends `actually`
- DOC: agent-check: fix typo in "fail" word expected reply
- REGTESTS: add a few load balancing tests
- REGTEST: fix host part in balance-uri-path-only.vtc
- REGTEST: make abns_socket.vtc require 1.8
- REGTEST: make map_regm_with_backref require 1.7

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.17-0
- BUILD: ebtree: fix build on libmusl after recent introduction of eb_memcmp()
- REGEST: Add reg tests about error files
- BUG/MINOR: threads: Don't forget to init each thread toremove_lock.
- MINOR: pools: increase MAX_BASE_POOLS to 64
- BUILD: thread: add parenthesis around values of locking macros
- BUG/MINOR: cfgparse: don't increment linenum on incomplete lines
- BUG/MEDIUM: resolve: fix init resolving for ring and peers section.
- BUG/MEDIUM: mux-h2: Emit an error if the response chunk formatting
  is incomplete
- BUG/MAJOR: dns: Make the do-resolve action thread-safe
- BUG/MEDIUM: dns: Release answer items when a DNS resolution is freed
- BUG/MEDIUM: mux-h1: Wakeup the H1C in h1_rcv_buf() if more data are expected
- BUG/MEDIUM: mux-h1: Disable the splicing when nothing is received
- BUG/MINOR: debug: Don't dump the lua stack if it is not initialized
- MEDIUM: lua: Add support for the Lua 5.4
- BUG/MEDIUM: dns: Don't yield in do-resolve action on a final evaluation
- BUG/MINOR: tcp-rules: Set the inspect-delay when a tcp-response action yields
- MINOR: connection: Preinstall the mux for non-ssl connect
- MINOR: stream-int: Be sure to have a mux to do sends and receives
- SCRIPTS: announce-release: add the link to the wiki in the announce messages

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.16-0
- MINOR: http: Add 410 to http-request deny
- MINOR: http: Add 404 to http-request deny
- BUG/MINOR: tcp-rules: tcp-response must check the buffer's fullness
- BUG/MEDIUM: ebtree: use a byte-per-byte memcmp() to compare memory blocks
- BUG/MINOR: spoe: add missing key length check before checking key names
- BUG/MINOR: cli: allow space escaping on the CLI
- BUG/MINOR: mworker/cli: fix the escaping in the master CLI
- BUG/MINOR: mworker/cli: fix semicolon escaping in master CLI
- REGTEST: http-rules: test spaces in ACLs
- REGTEST: http-rules: test spaces in ACLs with master CLI
- MEDIUM: map: make the "clear map" operation yield
- BUG/MINOR: systemd: Wait for network to be online
- REGTEST: Add a simple script to tests errorfile directives in proxy sections
- BUG/MINOR: spoe: correction of setting bits for analyzer
- BUG/MINOR: http_ana: clarify connection pointer check on L7 retry
- MINOR: spoe: Don't systematically create new applets if processing rate is low
- REGTEST: ssl: tests the ssl_f_* sample fetches
- REGTEST: ssl: add some ssl_c_* sample fetches test
- BUG/MEDIUM: fetch: Fix hdr_ip misparsing IPv4 addresses due to missing NUL
- MINOR: cli: make "show sess" stop at the last known session
- DOC: ssl: add "allow-0rtt" and "ciphersuites" in crt-list
- BUG/MEDIUM: pattern: Add a trailing \0 to match strings only if possible
- BUG/MINOR: proxy: fix dump_server_state()'s misuse of the trash
- BUG/MINOR: proxy: always initialize the trash in show servers state
- DOC: configuration: add missing index entries for
  tune.pool-{low,high}-fd-ratio
- DOC: configuration: fix alphabetical ordering for
  tune.pool-{high,low}-fd-ratio
- BUG/MINOR: http_act: don't check capture id in backend (2)
- BUG/MINOR: mux-h1: Fix the splicing in TUNNEL mode
- BUG/MINOR: mux-h1: Don't read data from a pipe if the mux is unable to receive
- BUG/MINOR: mux-h1: Disable splicing only if input data was processed
- BUG/MEDIUM: mux-h1: Disable splicing for the conn-stream if read0 is received
- BUG/MEDIUM: mux-h1: Subscribe rather than waking up in h1_rcv_buf()
- MINOR: connection: move the CO_FL_WAIT_ROOM cleanup to the reader only
- BUG/MEDIUM: connection: Continue to recv data to a pipe when the FD
  is not ready
- BUG/MINOR: backend: Remove CO_FL_SESS_IDLE if a client remains on
  the last server
- MINOR: http: Add support for http 413 status
- BUG/MAJOR: stream: Mark the server address as unset on new outgoing connection
- BUG/MEDIUM: stream-int: Disable connection retries on plain HTTP proxy mode
- DOC: configuration: remove obsolete mentions of H2 being converted to HTTP/1.x
- BUG/MINOR: sample: Free str.area in smp_check_const_bool
- BUG/MINOR: sample: Free str.area in smp_check_const_meth
- CONTRIB: da: fix memory leak in dummy function da_atlas_open()
- BUG/MEDIUM: mux-h1: Continue to process request when switching in tunnel mode
- BUG/MEDIUM: log: issue mixing sampled to not sampled log servers.
- BUG/MEDIUM: channel: Be aware of SHUTW_NOW flag when output data are peeked

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.15-0
- BUG/MINOR: protocol_buffer: Wrong maximum shifting.
- BUG/MINOR: peers: Incomplete peers sections should be validated.
- DOC: hashing: update link to hashing functions
- DOC: Improve documentation on http-request set-src
- BUG/MINOR: ssl: default settings for ssl server options are not used
- BUG/MEDIUM: http-ana: Handle NTLM messages correctly.
- BUG/MINOR: tools: fix the i386 version of the div64_32 function
- BUG/MINOR: http: make url_decode() optionally convert '+' to SP
- DOC: option logasap does not depend on mode
- BUG/MINOR: check: Update server address and port to execute an external check
- MINOR: checks: Add a way to send custom headers and payload during http chekcs
- BUG/MINOR: checks: Respect the no-check-ssl option
- BUG/MINOR: checks: chained expect will not properly wait for enough data
- BUG/MINOR: obj_type: Handle stream object in obj_base_ptr() function
- BUG/MEDIUM: capture: capture-req/capture-res converters crash without a stream
- BUG/MEDIUM: capture: capture.{req,res}.* crash without a stream
- BUG/MEDIUM: http: the "http_first_req" sample fetch could crash without
  a steeam
- BUG/MEDIUM: http: the "unique-id" sample fetch could crash without a steeam
- BUG/MEDIUM: sample: make the CPU and latency sample fetches check for a stream
- BUG/MEDIUM: listener: mark the thread as not stuck inside the loop
- MINOR: threads: export the POSIX thread ID in panic dumps
- BUG/MINOR: debug: properly use long long instead of long for the thread ID
- BUG/MEDIUM: shctx: really check the lock's value while waiting
- BUG/MEDIUM: shctx: bound the number of loops that can happen around the lock
- MINOR: stream: report the list of active filters on stream crashes
- REGTEST: ssl: test the client certificate authentication
- BUG/MEDIUM: backend: don't access a non-existing mux from a previous
  connection
- Revert "BUG/MINOR: connection: make sure to correctly tag local
  PROXY connections"
- BUG/MEDIUM: server/checks: Init server check during config validity check
- BUG/MINOR: checks/server: use_ssl member must be signed
- BUG/MEDIUM: checks: Always initialize checks before starting them
- BUG/MINOR: checks: Compute the right HTTP request length for HTTP
  health checks
- BUG/MINOR: checks: Remove a warning about http health checks
- BUG/MEDIUM: streams: Remove SF_ADDR_SET if we're retrying due to L7 retry.
- BUG/MEDIUM: stream: Only allow L7 retries when using HTTP.
- BUG/MAJOR: stream-int: always detach a faulty endpoint on connect failure
- BUG/MEDIUM: connections: force connections cleanup on server changes
- BUG/MEDIUM: ssl: fix the id length check within smp_fetch_ssl_fc_session_id()
- CLEANUP: connections: align function declaration
- BUG/MINOR: sample: Set the correct type when a binary is converted to a string
- BUG/MINOR: threads: fix multiple use of argument inside HA_ATOMIC_CAS()
- BUG/MINOR: threads: fix multiple use of argument inside
  HA_ATOMIC_UPDATE_{MIN,MAX}()
- BUG/MEDIUM: lua: Fix dumping of stick table entries for STD_T_DICT
- BUG/MINOR: config: Make use_backend and use-server post-parsing less obscur
- BUG/MINOR: http-ana: fix NTLM response parsing again
- BUG/MEDIUM: http_ana: make the detection of NTLM variants safer
- BUG/MINOR: cfgparse: Abort parsing the current line if an invalid \x sequence
  is encountered
- BUG/MINOR: pools: use %%u not %%d to report pool stats in "show pools"
- BUG/MINOR: pollers: remove uneeded free in global init
- BUG/MINOR: soft-stop: always wake up waiting threads on stopping
- BUILD: select: only declare existing local labels to appease clang
- BUG/MINOR: cache: Don't needlessly test "cache" keyword in parse_cache_flt()
- BUG/MINOR: checks: Respect check-ssl param when a port or an addr is specified
- BUG/MINOR: server: Fix server_finalize_init() to avoid unused variable
- BUG/MINOR: lua: Add missing string length for lua sticktable lookup
- BUG/MINOR: nameservers: fix error handling in parsing of resolv.conf
- Revert "BUG/MEDIUM: connections: force connections cleanup on server changes"
- SCRIPTS: publish-release: pass -n to gzip to remove timestamp
- BUG/MINOR: peers: fix internal/network key type mapping.
- BUG/MEDIUM: lua: Reset analyse expiration timeout before executing
  a lua action
- BUG/MEDIUM: hlua: Lock pattern references to perform set/add/del operations
- BUG/MEDIUM: contrib/prometheus-exporter: Properly set flags to dump metrics
- BUG/MINOR: logs: prevent double line returns in some events.
- BUG/MEDIUM: logs: fix trailing zeros on log message.
- BUG/MINOR: proto-http: Fix detection of NTLM for the legacy HTTP version
- BUILD: makefile: adjust the sed expression of "make help" for solaris
- BUG/MEDIUM: mworker: fix the copy of options in copy_argv()
- BUG/MINOR: init: -x can have a parameter starting with a dash
- BUG/MINOR: init: -S can have a parameter starting with a dash
- BUG/MEDIUM: mworker: fix the reload with an -- option
- BUG/MINOR: mworker: fix a memleak when execvp() failed
- BUG/MEDIUM: log: don't hold the log lock during writev() on a file descriptor
- BUG/MEDIUM: pattern: fix thread safety of pattern matching
- REGTESTS: Add missing OPENSSL to REQUIRE_OPTIONS for lua/txn_get_priv
- REGTESTS: Add missing OPENSSL to REQUIRE_OPTIONS for
  compression/lua_validation
- BUG/MINOR: ssl: fix ssl-{min,max}-ver with openssl < 1.1.0
- REGTESTS: checks: Fix tls_health_checks when IPv6 addresses are used

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.14-0
- BUG/MINOR: namespace: avoid closing fd when socket failed in my_socketat
- BUG/MEDIUM: muxes: Use the right argument when calling the destroy method.
- SCRIPTS: announce-release: use mutt -H instead of -i to include the draft
- MINOR: http-htx: Add a function to retrieve the headers size of an HTX message
- MINOR: filters: Forward data only if the last filter forwards something
- BUG/MINOR: filters: Count HTTP headers as filtered data but don't forward them
- BUG/MINOR: http-ana: Matching on monitor-uri should be case-sensitive
- BUG/MAJOR: http-ana: Always abort the request when a tarpit is triggered
- MINOR: ist: add an iststop() function
- BUG/MINOR: http: http-request replace-path duplicates the query string
- BUG/MEDIUM: shctx: make sure to keep all blocks aligned
- MINOR: compiler: move CPU capabilities definition from config.h and complete
  them
- BUG/MEDIUM: ebtree: don't set attribute packed without unaligned access
  support
- BUILD: fix recent build failure on unaligned archs
- CLEANUP: cfgparse: Fix type of second calloc() parameter
- BUG/MINOR: sample: fix the json converter's endian-sensitivity
- BUG/MEDIUM: ssl: fix several bad pointer aliases in a few sample fetch
  functions
- BUG/MINOR: connection: make sure to correctly tag local PROXY connections
- MINOR: compiler: add new alignment macros
- BUILD: ebtree: improve architecture-specific alignment
- BUG/MINOR: sample: Make sure to return stable IDs in the unique-id fetch
- BUG/MINOR: dns: ignore trailing dot
- MINOR: contrib/prometheus-exporter: Add heathcheck status/code in server
  metrics
- MINOR: contrib/prometheus-exporter: Add the last heathcheck duration metric
- BUG/MEDIUM: random: initialize the random pool a bit better
- MINOR: tools: add 64-bit rotate operators
- BUG/MEDIUM: random: implement a thread-safe and process-safe PRNG
- MINOR: backend: use a single call to ha_random32() for the random LB algo
- BUG/MINOR: checks/threads: use ha_random() and not rand()
- BUG/MAJOR: list: fix invalid element address calculation
- MINOR: debug: report the task handler's pointer relative to main
- BUG/MEDIUM: debug: make the debug_handler check for the thread
  in threads_to_dump
- MINOR: haproxy: export main to ease access from debugger
- BUG/MINOR: wdt: do not return an error when the watchdog couldn't be enabled
- DOC: fix incorrect indentation of http_auth_*
- OPTIM: startup: fast unique_id allocation for acl.
- BUG/MINOR: pattern: Do not pass len = 0 to calloc()
- DOC: configuration.txt: fix various typos
- DOC: assorted typo fixes in the documentation and Makefile
- BUG/MINOR: init: make the automatic maxconn consider the max of
  soft/hard limits
- BUG/MAJOR: proxy_protocol: Properly validate TLV lengths
- REGTEST: make the PROXY TLV validation depend on version 2.2
- MINOR: htx: Add a function to return a block at a specific offset
- BUG/MEDIUM: cache/filters: Fix loop on HTX blocks caching the response payload
- BUG/MEDIUM: compression/filters: Fix loop on HTX blocks compressing
  the payload
- BUG/MINOR: http-ana: Reset request analysers on a response side error
- BUG/MINOR: lua: Ignore the reserve to know if a channel is full or not
- BUG/MINOR: http-rules: Preserve FLT_END analyzers on reject action
- BUG/MINOR: http-rules: Fix a typo in the reject action function
- BUG/MINOR: rules: Preserve FLT_END analyzers on silent-drop action
- BUG/MINOR: rules: Increment be_counters if backend is assigned for
  a silent-drop
- DOC: fix typo about no-tls-tickets
- DOC: improve description of no-tls-tickets
- DOC: ssl: clarify security implications of TLS tickets
- BUILD: wdt: only test for SI_TKILL when compiled with thread support
- BUG/MEDIUM: random: align the state on 2*64 bits for ARM64
- BUG/MINOR: haproxy: always initialize sleeping_thread_mask
- BUG/MINOR: listener/mq: do not dispatch connections to remote threads when
  stopping
- BUG/MINOR: haproxy/threads: try to make all threads leave together
- DOC: proxy_protocol: Reserve TLV type 0x05 as PP2_TYPE_UNIQUE_ID
- BUILD: on ARM, must be linked to libatomic.
- BUILD: makefile: fix regex syntax in ARM platform detection
- BUILD: makefile: fix expression again to detect ARM platform
- BUG/MEDIUM: peers: resync ended with RESYNC_PARTIAL in wrong cases.
- DOC: assorted typo fixes in the documentation
- MINOR: wdt: Move the definitions of WDTSIG and DEBUGSIG into types/signal.h.
- BUG/MEDIUM: wdt: Don't ignore WDTSIG and DEBUGSIG in __signal_process_queue().
- MINOR: memory: Change the flush_lock to a spinlock, and don't get it in alloc.
- BUG/MINOR: connections: Make sure we free the connection on failure.
- REGTESTS: use "command -v" instead of "which"
- REGTEST: increase timeouts on the seamless-reload test
- BUG/MINOR: haproxy/threads: close a possible race in soft-stop detection
- BUG/MINOR: peers: init bind_proc to 1 if it wasn't initialized
- BUG/MINOR: peers: avoid an infinite loop with peers_fe is NULL
- BUG/MINOR: peers: Use after free of "peers" section.
- MINOR: listener: add so_name sample fetch
- BUILD: ssl: only pass unsigned chars to isspace()
- BUG/MINOR: stats: Fix color of draining servers on stats page
- DOC: internals: Fix spelling errors in filters.txt
- MINOR: http-rules: Add a flag on redirect rules to know the rule direction
- BUG/MINOR: http_ana: make sure redirect flags don't have overlapping bits
- MINOR: http-rules: Handle the rule direction when a redirect is evaluated
- BUG/MINOR: filters: Use filter offset to decude the amount of forwarded data
- BUG/MINOR: filters: Forward everything if no data filters are called
- BUG/MINOR: http-ana: Reset request analysers on error when waiting
  for response
- BUG/CRITICAL: hpack: never index a header into the headroom after wrapping

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.0.13-0
- BUG/MINOR: checks: refine which errno values are really errors.
- BUG/MEDIUM: checks: Only attempt to do handshakes if the connection is ready.
- BUG/MEDIUM: connections: Hold the lock when wanting to kill a connection.
- MINOR: config: disable busy polling on old processes
- MINOR: ssl: Remove unused variable "need_out".
- BUG/MINOR: h1: Report the right error position when a header value is invalid
- BUG/MINOR: proxy: Fix input data copy when an error is captured
- BUG/MEDIUM: http-ana: Truncate the response when a redirect rule is applied
- BUG/MINOR: channel: inject output data at the end of output
- BUG/MEDIUM: session: do not report a failure when rejecting a session
- BUG/MINOR: stream-int: Don't trigger L7 retry if max retries is already
  reached
- BUG/MINOR: mux-h2: use a safe list_for_each_entry in h2_send()
- BUG/MEDIUM: mux-h2: fix missing test on sending_list in previous patch
- BUG/MEDIUM: mux-h2: don't stop sending when crossing a buffer boundary
- BUG/MINOR: cli/mworker: can't start haproxy with 2 programs
- REGTEST: mcli/mcli_start_progs: start 2 programs
- BUG/MEDIUM: mworker: remain in mworker mode during reload
- BUG/MEDIUM: mux_h1: Don't call h1_send if we subscribed().
- BUG/MAJOR: hashes: fix the signedness of the hash inputs
- REGTEST: add sample_fetches/hashes.vtc to validate hashes
- BUG/MEDIUM: cli: _getsocks must send the peers sockets
- BUG/MINOR: stream: don't mistake match rules for store-request rules
- BUG/MEDIUM: connection: add a mux flag to indicate splice usability
- BUG/MINOR: pattern: handle errors from fgets when trying to load patterns
- BUG/MINOR: cache: Fix leak of cache name in error path
- BUG/MINOR: dns: Make dns_query_id_seed unsigned
- BUG/MINOR: 51d: Fix bug when HTX is enabled
- BUILD: pattern: include errno.h
- BUG/MINOR: http-ana/filters: Wait end of the http_end callback for all filters
- BUG/MINOR: http-rules: Remove buggy deinit functions for HTTP rules
- BUG/MINOR: stick-table: Use MAX_SESS_STKCTR as the max track ID during parsing
- BUG/MINOR: tcp-rules: Fix memory releases on error path during action parsing
- MINOR: proxy/http-ana: Add support of extra attributes for the cookie
  directive
- BUG/MINOR: http_act: don't check capture id in backend
- BUG/MEDIUM: 0rtt: Only consider the SSL handshake.
- BUG/MINOR: stktable: report the current proxy name in error messages
- BUG/MEDIUM: mux-h2: make sure we don't emit TE headers with anything but
  "trailers"
- BUILD: cfgparse: silence a bogus gcc warning on 32-bit machines
- BUG/MINOR: dns: allow srv record weight set to 0
- BUG/MEDIUM: ssl: Don't forget to free ctx->ssl on failure.
- BUG/MINOR: tcpchecks: fix the connect() flags regarding delayed ack
- BUG/MEDIUM: pipe: fix a use-after-free in case of pipe creation error
- BUG/MINOR: connection: fix ip6 dst_port copy in make_proxy_line_v2
- BUG/MEDIUM: connections: Don't forget to unlock when killing a connection.
- BUG/MEDIUM: memory_pool: Update the seq number in pool_flush().
- MINOR: memory: Only init the pool spinlock once.
- BUG/MEDIUM: memory: Add a rwlock before freeing memory.
- BUG/MAJOR: memory: Don't forget to unlock the rwlock if the pool is empty.
- BUG/MINOR: ssl: we may only ignore the first 64 errors
- CONTRIB: debug: add missing flags SF_HTX and SF_MUX
- CONTRIB: debug: add the possibility to decode the value as certain types only
- CONTRIB: debug: support reporting multiple values at once
- MINOR: acl: Warn when an ACL is named 'or'
- CONTRIB: debug: also support reading values from stdin
- SCRIPTS: announce-release: place the send command in the mail's header
- SCRIPTS: announce-release: allow the user to force to overwrite old files
- MINOR: build: add linux-glibc-legacy build TARGET
- BUG/MINOR: unix: better catch situations where the unix socket path length is
  close to the limit
- MINOR: http: add a new "replace-path" action
- BUG/MINOR: ssl: Possible memleak when allowing the 0RTT data buffer.
- BUG/MINOR: dns: allow 63 char in hostname
- BUG/MEDIUM: listener: only consider running threads when resuming listeners
- BUG/MINOR: listener: enforce all_threads_mask on bind_thread on init
- BUG/MINOR: tcp: avoid closing fd when socket failed in tcp_bind_listener
- DOC: word converter ignores delimiters at the start or end of input string
- BUG/MINOR: tcp: don't try to set defaultmss when value is negative
- SCRIPTS: make announce-release executable again

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.12-0
- DOC: Improve documentation of http-re(quest|sponse) replace-(header|value|uri)
- DOC: clarify the fact that replace-uri works on a full URI
- BUG/MINOR: sample: fix the closing bracket and LF in the debug converter
- BUG/MINOR: sample: always check converters' arguments
- BUG/MEDIUM: ssl: Don't set the max early data we can receive too early.
- MINOR: task: only check TASK_WOKEN_ANY to decide to requeue a task
- BUG/MAJOR: task: add a new TASK_SHARED_WQ flag to fix foreing requeuing
- BUG/MEDIUM: ssl: Revamp the way early data are handled.
- MINOR: fd/threads: make _GET_NEXT()/_GET_PREV() use the volatile attribute
- BUG/MEDIUM: fd/threads: fix a concurrency issue between add and rm on
  the same fd
- BUG/MINOR: ssl: openssl-compat: Fix getm_ defines
- BUG/MEDIUM: stream: Be sure to never assign a TCP backend to an HTX stream
- BUILD: ssl: improve SSL_CTX_set_ecdh_auto compatibility

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.11-0
- BUG/MINOR: stream: init variables when the list is empty
- BUG/MINOR: contrib/prometheus-exporter: Use HTX errors and not legacy ones
- BUG/MINOR: contrib/prometheus-exporter: decode parameter and value only
- BUG/MINOR: http-htx: Don't make http_find_header() fail if the value is empty
- DOC: Clarify behavior of server maxconn in HTTP mode
- DOC: clarify matching strings on binary fetches
- DOC: move the "group" keyword at the right place
- BUG/MEDIUM: stream-int: don't subscribed for recv when we're trying to
  flush data
- BUG/MINOR: stream-int: avoid calling rcv_buf() when splicing is still possible
- BUG/MEDIUM: listener/thread: fix a race when pausing a listener
- BUG/MINOR: ssl: certificate choice can be unexpected with openssl >= 1.1.1
- BUG/MEDIUM: mux-h1: Never reuse H1 connection if a shutw is pending
- BUG/MINOR: mux-h1: Don't rely on CO_FL_SOCK_RD_SH to set H1C_F_CS_SHUTDOWN
- BUG/MINOR: mux-h1: Fix conditions to know whether or not we may receive data
- BUG/MEDIUM: tasks: Make sure we switch wait queues in task_set_affinity().
- BUG/MEDIUM: checks: Make sure we set the task affinity just before connecting.
- BUG/MINOR: mux-h1: Be sure to set CS_FL_WANT_ROOM when EOM can't be added
- BUG/MINOR: proxy: make soft_stop() also close FDs in LI_PAUSED state
- BUG/MINOR: listener/threads: always use atomic ops to clear the FD events
- BUG/MINOR: listener: also clear the error flag on a paused listener
- BUG/MEDIUM: listener/threads: fix a remaining race in the listener's accept()
- DOC: document the listener state transitions
- BUG/MAJOR: dns: add minimalist error processing on the Rx path
- BUG/MEDIUM: proto_udp/threads: recv() and send() must not be exclusive.
- BUG/MEDIUM: kqueue: Make sure we report read events even when no data.
- DOC: listeners: add a few missing transitions
- BUG/MINOR: tasks: only requeue a task if it was already in the queue
- DOC: proxies: HAProxy only supports 3 connection modes
- BUILD/MINOR: ssl: shut up a build warning about format truncation
- BUILD/MINOR: tools: shut up the format truncation warning in get_gmt_offset()
- BUILD: do not disable -Wformat-truncation anymore
- DOC: remove references to the outdated architecture.txt
- BUG/MINOR: log: fix minor resource leaks on logformat error path
- BUG/MINOR: mworker: properly pass SIGTTOU/SIGTTIN to workers
- BUG/MINOR: listener: do not immediately resume on transient error
- BUG/MINOR: server: make "agent-addr" work on default-server line
- BUG/MINOR: listener: fix off-by-one in state name check
- BUILD/MINOR: unix sockets: silence an absurd gcc warning about strncpy()

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.10-0
- BUG/MINOR: init: fix set-dumpable when using uid/gid
- MINOR: peers: Alway show the table info for disconnected peers.
- MINOR: peers: Add TX/RX heartbeat counters.
- MINOR: peers: Add debugging information to "show peers".
- BUG/MINOR: peers: Wrong null "server_name" data field handling.
- BUG/MINOR: ssl: fix crt-list neg filter for openssl < 1.1.1
- BUG/MEDIUM: mworker: don't fill the -sf argument with -1 during the reexec
- BUG/MINOR: peers: "peer alive" flag not reset when deconnecting.
- BUILD/MINOR: ssl: fix compiler warning about useless statement
- BUG/MEDIUM: stream-int: Don't loose events on the CS when an EOS is reported
- BUILD: debug: Avoid warnings in dev mode with -02 because of some BUG_ON tests
- BUG/MINOR: mux-h1: Fix tunnel mode detection on the response path
- BUG/MINOR: http-ana: Properly catch aborts during the payload forwarding
- MINOR: freq_ctr: Make the sliding window sums thread-safe
- MINOR: stream: Remove the lock on the proxy to update time stats
- MINOR: counters: Add fields to store the max observed for {q,c,d,t}_time
- MINOR: contrib/prometheus-exporter: Report metrics about max times for
  sessions
- BUG/MINOR: contrib/prometheus-exporter: Rename some metrics
- MINOR: contrib/prometheus-exporter: report the number of idle conns
  per server
- MINOR: contrib/prometheus-exporter: filter exported metrics by scope
- MINOR: contrib/prometheus-exporter: Add a param to ignore servers
  in maintenance
- BUG/MINOR: stream-int: Fix si_cs_recv() return value
- MINOR: stats: Report max times in addition of the averages for sessions
- REGTEST: vtest can now enable mcli with its own flag
- MEDIUM: mux-h1: Add the support of headers adjustment for bogus HTTP/1 apps
- BUG/MINOR: mux-h1: Fix a UAF in cfg_h1_headers_case_adjust_postparser()
- BUG/MINOR: mux-h1: Adjust header case when chunked encoding is add to
  a message
- DOC: Add missing stats fields in the management manual
- DOC: Add documentation about the use-service action
- BUG/MINOR: cli: fix out of bounds in -S parser
- BUG/MINOR: ssl: fix curve setup with LibreSSL
- MINOR: ist: add ist_find_ctl()
- BUG/MAJOR: h2: reject header values containing invalid chars
- BUG/MAJOR: h2: make header field name filtering stronger
- BUG/MAJOR: mux-h2: don't try to decode a response HEADERS frame in idle state
- SCRIPTS: create-release: show the correct origin name in suggested commands
- SCRIPTS: git-show-backports: add "-s" to proposed cherry-pick commands

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.9-0
- MINOR: config: warn on presence of "\n" in header values/replacements
- BUG/MINOR: mux-h2: do not emit logs on backend connections
- MINOR: tcp: avoid confusion in time parsing init
- BUG/MINOR: cli: don't call the kw->io_release if kw->parse failed
- BUG/MINOR: mux-h2: Don't pretend mux buffers aren't full anymore if nothing
  sent
- BUG/MAJOR: stream-int: Don't receive data from mux until SI_ST_EST is reached
- BUG/MINOR: spoe: fix off-by-one length in UUID format string
- MINOR: mux: Add a new method to get informations about a mux.
- BUG/MEDIUM: stream_interface: Only use SI_ST_RDY when the mux is ready.
- BUG/MEDIUM: servers: Only set SF_SRV_REUSED if the connection if fully ready.
- BUG/MINOR: config: Update cookie domain warn to RFC6265
- BUG/MEDIUM: mux-h2: report no available stream on a connection having errors
- BUG/MEDIUM: mux-h2: immediately remove a failed connection from the idle list
- BUG/MEDIUM: mux-h2: immediately report connection errors on streams
- BUG/MEDIUM: mux-h1: Disable splicing for chunked messages
- BUG/MEDIUM: stream: Be sure to support splicing at the mux level to enable it
- MINOR: doc: http-reuse connection pool fix
- BUG/MEDIUM: stream: Be sure to release allocated captures for TCP streams
- BUG/MINOR: action: do-resolve now use cached response
- BUG: dns: timeout resolve not applied for valid resolutions
- DOC: management: document reuse and connect counters in the CSV format
- DOC: management: document cache_hits and cache_lookups in the CSV format
- DOC: management: fix typo on "cache_lookups" stats output
- BUG/MINOR: queue/threads: make the queue unlinking atomic
- BUG/MEDIUM: listeners: always pause a listener on out-of-resource condition
- BUG/MEDIUM: Make sure we leave the session list in session_free().
- CLEANUP: session: slightly simplify idle connection cleanup logic
- MINOR: memory: also poison the area on freeing
- BUILD: contrib/da: remove an "unused" warning
- BUG/MINOR: log: limit the size of the startup-logs
- BUG/MEDIUM: filters: Don't call TCP callbacks for HTX streams
- BUG/MINOR: mux-h1: Don't set CS_FL_EOS on a read0 when receiving data to pipe

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.8-0
- BUG/MINOR: stats: Add a missing break in a switch statement
- BUG/MINOR: lua: Properly initialize the buffer's fields for string samples
  in hlua_lua2(smp|arg)
- BUG/MEDIUM: lua: Store stick tables into the sample's `t` field
- BUG/MINOR: action: do-resolve does not yield on requests with body
- MINOR: mux-h2: add a per-connection list of blocked streams
- BUILD: ebtree: make eb_is_empty() and eb_is_dup() take a const
- BUG/MEDIUM: mux-h2: do not enforce timeout on long connections
- BUG/MINOR: peers: crash on reload without local peer.
- BUG/MEDIUM: cache: make sure not to cache requests with absolute-uri
- DOC: clarify some points around http-send-name-header's behavior
- DOC: fix typo in Prometheus exporter doc
- MINOR: stats: mention in the help message support for "json" and "typed"
- BUG/MEDIUM: applet: always check a fast running applet's activity before
  killing
- BUG/MINOR: ssl: abort on sni allocation failure
- BUG/MINOR: ssl: free the sni_keytype nodes
- BUG/MINOR: ssl: abort on sni_keytypes allocation failure
- BUILD: ssl: wrong #ifdef for SSL engines code
- BUG/MEDIUM: htx: Catch chunk_memcat() failures when HTX data are formatted to
  h1
- BUG/MINOR: chunk: Fix tests on the chunk size in functions copying data
- BUG/MINOR: mux-h1: Mark the output buffer as full when the xfer is interrupted
- BUG/MINOR: mux-h1: Capture ignored parsing errors
- BUG/MINOR: WURFL: fix send_log() function arguments
- MINOR: version: make the version strings variables, not constants
- BUG/MINOR: http-htx: Properly set htx flags on error files to support
  keep-alive
- BUG/MINOR: mworker/ssl: close openssl FDs unconditionally
- BUG/MINOR: tcp: Don't alter counters returned by tcp info fetchers
- BUG/MEDIUM: mux_pt: Make sure we don't have a conn_stream before freeing.
- BUG/MAJOR: idle conns: schedule the cleanup task on the correct threads
- BUG/MEDIUM: mux_pt: Don't destroy the connection if we have a stream attached.
- BUG/MEDIUM: mux_pt: Only call the wake emthod if nobody subscribed to receive.
- REGTEST: mcli/mcli_show_info: launch a 'show info' on the master CLI
- CLEANUP: ssl: make ssl_sock_load_cert*() return real error codes
- CLEANUP: ssl: make ssl_sock_put_ckch_into_ctx handle errcode/warn
- CLEANUP: ssl: make ssl_sock_load_dh_params handle errcode/warn
- CLEANUP: bind: handle warning label on bind keywords parsing.
- BUG/MEDIUM: ssl: 'tune.ssl.default-dh-param' value ignored with
  openssl > 1.1.1
- BUG/MINOR: mworker/cli: reload fail with inherited FD
- BUG/MINOR: ssl: Fix fd leak on error path when a TLS ticket keys file
  is parsed
- BUG/MINOR: stick-table: Never exceed (MAX_SESS_STKCTR-1) when fetching
  a stkctr
- BUG/MINOR: cache: alloc shctx after check config
- BUG/MINOR: sample: Make the `field` converter compatible with `-m found`
- BUG/MINOR: mux-h2: also make sure blocked legacy connections may expire
- BUG/MEDIUM: http: unbreak redirects in legacy mode
- BUG/MINOR: ssl: fix memcpy overlap without consequences.
- BUG/MINOR: stick-table: fix an incorrect 32 to 64 bit key conversion
- BUG/MEDIUM: pattern: make the pattern LRU cache thread-local and lockless

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.7-0
- BUG/MEDIUM: stick-table: Properly handle "show table" with a data type
  argument
- BUG/MINOR: mux-h2: Be sure to have a connection to unsubcribe
- BUG/MAJOR: mux-h2: Handle HEADERS frames received after a RST_STREAM frame
- BUG/MEDIUM: check/threads: make external checks run exclusively on thread 1
- BUG/MINOR: stream-int: Process connection/CS errors first in si_cs_send()
- BUG/MEDIUM: stream-int: Process connection/CS errors during synchronous sends
- BUG/MEDIUM: checks: make sure the connection is ready before trying to recv
- BUG/MINOR: mux-h2: do not wake up blocked streams before the mux is ready
- BUG/MEDIUM: namespace: close open namespaces during soft shutdown
- BUG/MEDIUM: mux-h2: don't reject valid frames on closed streams
- BUG/MINOR: mux-h2: Use the dummy error when decoding headers for a closed
  stream
- BUG/MAJOR: mux_h2: Don't consume more payload than received for skipped frames
- BUG/MINOR: mux-h1: Do h2 upgrade only on the first request
- BUG/MEDIUM: spoe: Use a different engine-id per process
- MINOR: spoe: Improve generation of the engine-id
- MINOR: spoe: Support the async mode with several threads
- MINOR: stats: Add the support of float fields in stats
- BUG/MINOR: contrib/prometheus-exporter: Return the time averages in seconds
- DOC: Fix documentation about the cli command to get resolver stats
- BUG/MEDIUM: namespace: fix fd leak in master-worker mode

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.6-0
- MINOR: debug: indicate the applet name when the task is task_run_applet()
- MINOR: tools: add append_prefixed_str()
- MINOR: lua: export applet and task handlers
- MEDIUM: debug: make the thread dump code show Lua backtraces
- BUG/MEDIUM: mux-h1: do not truncate trailing 0CRLF on buffer boundary
- BUG/MEDIUM: mux-h1: do not report errors on transfers ending on buffer full
- DOC: fixed typo in management.txt
- BUG/MINOR: mworker: disable SIGPROF on re-exec
- BUG/MEDIUM: listener/threads: fix an AB/BA locking issue in delete_listener()
- BUG/MEDIUM: url32 does not take the path part into account in the returned
  hash.
- BUG/MEDIUM: proto-http: Always start the parsing if there is no outgoing data
- BUG/MEDIUM: peers: local peer socket not bound.
- BUG/MINOR: http-ana: Reset response flags when 1xx messages are handled
- BUG/MINOR: h1: Properly reset h1m when parsing is restarted
- BUG/MINOR: mux-h1: Fix size evaluation of HTX messages after headers parsing
- BUG/MINOR: mux-h1: Don't stop anymore input processing when the max is reached
- BUG/MINOR: mux-h1: Be sure to update the count before adding EOM after
  trailers
- BUG/MEDIUM: cache: Properly copy headers splitted on several shctx blocks
- BUG/MEDIUM: cache: Don't cache objects if the size of headers is too big
- BUG/MINOR: checks: stop polling for write when we have nothing left to send
- BUG/MINOR: checks: start sending the request right after connect()
- BUG/MINOR: checks: make __event_chk_srv_r() report success before closing
- BUG/MINOR: checks: do not uselessly poll for reads before the connection is up
- MINOR: contrib/prometheus-exporter: Report DRAIN/MAINT/NOLB status for servers
- BUG/MINOR: lb/leastconn: ignore the server weights for empty servers
- BUG/MAJOR: ssl: ssl_sock was not fully initialized.
- BUG/MEDIUM: connection: don't keep more idle connections than ever needed
- MINOR: stats: report the number of idle connections for each server
- BUG/MINOR: listener: Fix a possible null pointer dereference
- BUG/MINOR: ssl: always check for ssl connection before getting its XPRT
  context
- BUG/MEDIUM: http: also reject messages where "chunked" is missing from
  transfer-enoding
- BUG/MINOR: filters: Properly set the HTTP status code on analysis error
- BUG/MINOR: acl: Fix memory leaks when an ACL expression is parsed
- BUG/MINOR: backend: Fix a possible null pointer dereference
- BUG/MINOR: Missing stat_field_names (since f21d17bb)
- MINOR: sample: Add UUID-fetch

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.5-0
- BUG/MEDIUM: stick-table: Wrong stick-table backends parsing.
- BUG/MINOR: ssl: fix 0-RTT for BoringSSL
- MINOR: ssl: ssl_fc_has_early should work for BoringSSL
- BUG/MINOR: buffers/threads: always clear a buffer's head before releasing it
- BUG/MEDIUM: proxy: Don't forget the SF_HTX flag when upgrading TCP=>H1+HTX.
- BUG/MEDIUM: proxy: Don't use cs_destroy() when freeing the conn_stream.
- BUG/MINOR: lua: fix setting netfilter mark
- BUG/MINOR: Fix prometheus '# TYPE' and '# HELP' headers
- BUG/MEDIUM: mux_h1: Don't bother subscribing in recv if we're not connected.
- BUG/MEDIUM: lua: Fix test on the direction to set the channel exp timeout
- BUG/MINOR: stats: Wait the body before processing POST requests
- MINOR: fd: make sure to mark the thread as not stuck in fd_update_events()
- BUG/MEDIUM: mux_pt: Don't call unsubscribe if we did not subscribe.

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.4-0
- BUG/MEDIUM: protocols: add a global lock for the init/deinit stuff
- BUG/MINOR: proxy: always lock stop_proxy()
- BUILD: threads: add the definition of PROTO_LOCK
- BUG/MEDIUM: lb-chash: Fix the realloc() when the number of nodes is increased
- BUG/MEDIUM: streams: Don't switch the SI to SI_ST_DIS if we have data to send.
- BUG/MINOR: log: make sure writev() is not interrupted on a file output
- DOC: improve the wording in CONTRIBUTING about how to document a bug fix
- BUG/MINOR: hlua/htx: Reset channels analyzers when txn:done() is called
- BUG/MEDIUM: hlua: Check the calling direction in lua functions of the HTTP
  class
- MINOR: hlua: Don't set request analyzers on response channel for lua actions
- MINOR: hlua: Add a flag on the lua txn to know in which context it can be used
- BUG/MINOR: hlua: Only execute functions of HTTP class if the txn is HTTP ready
- BUG/MINOR: htx: Fix free space addresses calculation during a block expansion
- BUG/MAJOR: queue/threads: avoid an AB/BA locking issue in process_srv_queue()
- BUG/MINOR: debug: fix a small race in the thread dumping code
- MINOR: wdt: also consider that waiting in the thread dumper is normal
- BUG/MEDIUM: lb-chash: Ensure the tree integrity when server weight is
  increased
- BUG/MAJOR: http/sample: use a static buffer for raw -> htx conversion
- BUG/MINOR: stream-int: also update analysers timeouts on activity
- BUG/MEDIUM: mux-h2: unbreak receipt of large DATA frames
- BUG/MEDIUM: mux-h2: split the stream's and connection's window sizes
- BUG/MEDIUM: proxy: Make sure to destroy the stream on upgrade from TCP to H2
- BUG/MEDIUM: fd: Always reset the polled_mask bits in fd_dodelete().
- BUG/MINOR: mux-h2: don't refrain from sending an RST_STREAM after another one
- BUG/MINOR: mux-h2: use CANCEL, not STREAM_CLOSED in h2c_frt_handle_data()
- BUG/MINOR: mux-h2: do not send REFUSED_STREAM on aborted uploads
- BUG/MEDIUM: mux-h2: do not recheck a frame type after a state transition
- BUG/MINOR: mux-h2: always send stream window update before connection's
- BUG/MINOR: mux-h2: always reset rcvd_s when switching to a new frame
- BUG/MEDIUM: checks: make sure to close nicely when we're the last to speak

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- BUG/MINOR: dns: remove irrelevant dependency on a client connection
- BUG/MEDIUM: checks: Don't attempt to receive data if we already subscribed.
- BUG/MEDIUM: http/htx: unbreak option http_proxy
- BUG/MINOR: backend: do not try to install a mux when the connection failed
- BUG/MINOR: http_fetch: Fix http_auth/http_auth_group when called from TCP
  rules
- BUG/MINOR: http_htx: Initialize HTX error messages for TCP proxies
- BUG/MINOR: cache/htx: Make maxage calculation HTX aware
- BUG/MINOR: hlua: Make the function txn:done() HTX aware
- DOC: htx: Update comments in HTX files
- BUG/MINOR: debug: Remove flags CO_FL_SOCK_WR_ENA/CO_FL_SOCK_RD_ENA
- BUG/MINOR: session: Emit an HTTP error if accept fails only for H1 connection
- BUG/MINOR: session: Send a default HTTP error if accept fails for a H1 socket
- BUG/MINOR: checks: do not exit tcp-checks from the middle of the loop
- BUG/MEDIUM: mux-h1: Trim excess server data at the end of a transaction
- BUG/MINOR: mux-h1: Close server connection if input data remains in
  h1_detach()
- BUG/MEDIUM: tcp-checks: do not dereference inexisting conn_stream
- BUG/MINOR: http_ana: Be sure to have an allocated buffer to generate an error
- BUG/MINOR: http_htx: Support empty errorfiles
- BUG/CRITICAL: http_ana: Fix parsing of malformed cookies which start by a
  delimiter

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- BUG/MINOR: mworker/cli: don't output a \n before the response
- BUG/MEDIUM: ssl: Don't attempt to set alpn if we're not using SSL.
- BUG/MEDIUM: mux-h1: Always release H1C if a shutdown for writes was reported
- BUG/MEDIUM: checks: unblock signals in external checks
- BUG/MINOR: mux-h1: Skip trailers for non-chunked outgoing messages
- BUG/MINOR: mux-h1: Don't return the empty chunk on HEAD responses
- BUG/MEDIUM: connections: Always call shutdown, with no linger.
- BUG/MEDIUM: checks: Make sure the tasklet won't run if the connection is
  closed.
- BUG/MINOR: contrib/prometheus-exporter: Don't use channel_htx_recv_max()
- BUG/MINOR: hlua: Don't use channel_htx_recv_max()
- BUG/MEDIUM: channel/htx: Use the total HTX size in channel_htx_recv_limit()
- BUG/MINOR: hlua/htx: Respect the reserve when HTX data are sent
- BUG/MINOR: contrib/prometheus-exporter: Respect the reserve when data are sent
- BUG/MEDIUM: connections: Make sure we're unsubscribe before upgrading the mux.
- BUG/MEDIUM: servers: Authorize tfo in default-server.
- BUG/MEDIUM: sessions: Don't keep an extra idle connection in sessions.
- MINOR: server: Add "no-tfo" option.
- BUG/MINOR: contrib/prometheus-exporter: Don't try to add empty data blocks
- MINOR: action: Add the return code ACT_RET_DONE for actions
- BUG/MEDIUM: http/applet: Finish request processing when a service is
  registered
- BUG/MEDIUM: lb_fas: Don't test the server's lb_tree from outside the lock
- BUG/MEDIUM: mux-h1: Handle TUNNEL state when outgoing messages are formatted
- BUG/MINOR: mux-h1: Don't process input or ouput if an error occurred
- MINOR: stream-int: Factorize processing done after sending data in
  si_cs_send()
- BUG/MEDIUM: stream-int: Don't rely on CF_WRITE_PARTIAL to unblock opposite si
- BUG/MEDIUM: servers: Don't forget to set srv_cs to NULL if we can't reuse it.
- BUG/MINOR: ssl: revert empty handshake detection in OpenSSL <= 1.0.2
- BUG/MEDIUM: fd/threads: fix excessive CPU usage on multi-thread accept
- BUG/MINOR: server: Be really able to keep "pool-max-conn" idle connections
- BUG/MEDIUM: checks: Don't attempt to read if we destroyed the connection.
- BUG/MEDIUM: da: cast the chunk to string.
- DOC: Fix typos and grammer in configuration.txt
- BUG/MEDIUM: servers: Fix a race condition with idle connections.
- MINOR: task: introduce work lists
- BUG/MAJOR: listener: fix thread safety in resume_listener()
- BUG/MEDIUM: mux-h1: Don't release h1 connection if there is still data to send
- BUG/MINOR: mux-h1: Correctly report Ti timer when HTX and keepalives are used
- BUG/MEDIUM: streams: Don't give up if we couldn't send the request.
- BUG/MEDIUM: streams: Don't redispatch with L7 retries if redispatch isn't set.
- BUG/MINOR: mux-pt: do not pretend there's more data after a read0
- BUG/MEDIUM: tcp-check: unbreak multiple connect rules again
- BUG/MEDIUM: threads: cpu-map designating a single thread/process are ignored

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- BUG/MEDIUM: h2/htx: Update data length of the HTX when the cookie list is
  built
- BUG/MINOR: lua/htx: Make txn.req_req_* and txn.res_rep_* HTX aware
- BUG/MINOR: mux-h1: Add the header connection in lower case in outgoing
  messages
- BUG/MEDIUM: compression: Set Vary: Accept-Encoding for compressed responses
- MINOR: htx: Add the function htx_change_blk_value_len()
- BUG/MEDIUM: htx: Fully update HTX message when the block value is changed
- BUG/MEDIUM: mux-h2: Reset padlen when several frames are demux
- BUG/MEDIUM: mux-h2: Remove the padding length when a DATA frame size is
  checked
- BUG/MEDIUM: lb_fwlc: Don't test the server's lb_tree from outside the lock
- BUG/MAJOR: sample: Wrong stick-table name parsing in "if/unless" ACL
  condition.
- BUG/MINOR: mworker-prog: Fix segmentation fault during cfgparse
- BUG/MEDIUM: mworker: don't call the thread and fdtab deinit
- BUG/MEDIUM: mworker/cli: command pipelining doesn't work anymore
- BUILD: mworker: silence two printf format warnings around getpid()
- BUILD: makefile: use :space: instead of digits to count commits
- BUILD: makefile: do not rely on shell substitutions to determine git version
- BUG/MINOR: spoe: Fix memory leak if failing to allocate memory
- BUG/MEDIUM: stream_interface: Don't add SI_FL_ERR the state is < SI_ST_CON.
- BUG/MEDIUM: connections: Always add the xprt handshake if needed.
- BUG/MEDIUM: ssl: Don't do anything in ssl_subscribe if we have no ctx.
- BUG/MINOR: htx: Save hdrs_bytes when the HTX start-line is replaced
- BUG/MAJOR: mux-h1: Don't crush trash chunk area when outgoing message is
  formatted
- BUG/MINOR: memory: Set objects size for pools in the per-thread cache
- BUG/MINOR: log: Detect missing sampling ranges in config
- BUG/MEDIUM: proto_htx: Don't add EOM on 1xx informational messages
- BUG/MEDIUM: mux-h1: Use buf_room_for_htx_data() to detect too large messages
- BUG/MINOR: mux-h1: Make format errors during output formatting fatal

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Initial build for kaos repository
