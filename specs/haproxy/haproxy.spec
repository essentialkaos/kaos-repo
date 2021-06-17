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

%define hp_user           %{name}
%define hp_user_id        188
%define hp_group          %{name}
%define hp_group_id       188
%define hp_homedir        %{_localstatedir}/lib/%{name}
%define hp_confdir        %{_sysconfdir}/%{name}
%define hp_datadir        %{_datadir}/%{name}

%define lua_ver           5.4.3
%define pcre_ver          8.45
%define openssl_ver       1.1.1k
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.4.1
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.4/src/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.cfg
Source3:           %{name}.logrotate
Source4:           %{name}.sysconfig
Source5:           %{name}.service

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

%setup -q

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

%{__make} admin/halog/halog

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -pDm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pDm 0644 %{SOURCE2} %{buildroot}%{hp_confdir}/%{name}.cfg
install -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/

install -pm 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
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
  %{__sysctl} enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
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
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{hp_datadir}/*
%{_initrddir}/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.4.1-0
- BUG/MEDIUM: ebtree: Invalid read when looking for dup entry
- BUG/MAJOR: server: prevent deadlock when using 'set maxconn server'
- BUILD/MINOR: opentracing: fixed build when using clang
- BUG/MEDIUM: filters: Exec pre/post analysers only one time per filter
- BUG/MINOR: http-comp: Preserve HTTP_MSGF_COMPRESSIONG flag on the response
- Revert "MEDIUM: http-ana: Deal with L7 retries in HTTP analysers"
- BUG/MINOR: http-ana: Send the right error if max retries is reached
  on L7 retry
- BUG/MINOR: http-ana: Handle L7 retries on refused early data before K/A aborts
- MINOR: http-ana: Perform L7 retries because of status codes
  in response analyser
- MINOR: cfgparse: Fail when encountering extra arguments in macro
- DOC: intro: Fix typo in starter guide
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
- BUG/MINOR: compression: Missing calloc return value check
  in comp_append_type/algo
- BUG/MINOR: worker: Missing calloc return value check in
  mworker_env_to_proc_list
- BUG/MINOR: http: Missing calloc return value check while parsing redirect rule
- BUG/MINOR: http: Missing calloc return value check in make_arg_list
- BUG/MINOR: proxy: Missing calloc return value check in chash_init_server_tree
- CLEANUP: http-ana: Remove useless if statement about L7 retries
- BUG/MINOR: vars: Be sure to have a session to get checks variables
- DOC/MINOR: move uuid in the configuration to the right alphabetical order
- BUG/MAJOR: stream-int: Release SI endpoint on server side ASAP on retry
- MINOR: errors: allow empty va_args for diag variadic macro
- DOC: use the req.ssl_sni in examples
- BUILD: make tune.ssl.keylog available again
- BUG/MINOR: ssl: OCSP stapling does not work if expire too far in the future
- Revert "BUG/MINOR: opentracing: initialization after establishing daemon mode"
- BUG/MEDIUM: opentracing: initialization before establishing daemon
  and/or chroot mode
- BUG/MEDIUM: compression: Fix loop skipping unused blocks to get the next block
- BUG/MEDIUM: compression: Properly get the next block to iterate on payload
- BUG/MEDIUM: compression: Add a flag to know the filter is still
  processing data
- BUG/MINOR: pools: fix a possible memory leak in the lockless pool_flush()
- BUG/MINOR: pools: make DEBUG_UAF always write to the to-be-freed location
- MINOR: pools: do not maintain the lock during pool_flush()
- MINOR: pools: call malloc_trim() under thread isolation
- MEDIUM: pools: use a single pool_gc() function for locked and lockless
- BUG/MAJOR: pools: fix possible race with free() in the lockless variant
- CLEANUP: pools: remove now unused seq and pool_free_list
- BUG/MAJOR: htx: Fix htx_defrag() when an HTX block is expanded
- BUG/MINOR: mux-fcgi: Expose SERVER_SOFTWARE parameter by default
- CLEANUP: l7-retries: do not test the buffer before calling b_alloc()
- BUG/MINOR: resolvers: answser item list was randomly purged or errors
- MEDIUM: resolvers: add a ref on server to the used A/AAAA answer item
- MEDIUM: resolvers: add a ref between servers and srv request or used
  SRV record
- BUG/MAJOR: resolvers: segfault using server template without SRV RECORDs
- DOC: lua: Add a warning about buffers modification in HTTP
- BUG/MINOR: stick-table: insert srv in used_name tree even with fixed id
- BUG/MEDIUM: server: extend thread-isolate over much of CLI 'add server'
- BUG/MEDIUM: server: clear dynamic srv on delete from proxy id/name trees
- BUG/MEDIUM: server: do not forget to generate the dynamic servers ids
- BUG/MINOR: server: do not keep an invalid dynamic server in px ids tree
- BUG/MEDIUM: server: do not auto insert a dynamic server in px addr_node
- BUG/MEDIUM: shctx: use at least thread-based locking on USE_PRIVATE_CACHE
- BUG/MINOR: ssl: use atomic ops to update global shctx stats
- BUG/MINOR: mworker: fix typo in chroot error message
- CLEANUP: global: remove unused definition of stopping_task[]
- BUG/MAJOR: queue: set SF_ASSIGNED when setting strm->target on dequeue
- MINOR: backend: only skip LB when there are actual connections
- BUG/MINOR: mux-h1: do not skip the error response on bad requests
- BUG/MINOR: server: explicitly set "none" init-addr for dynamic servers
- MINOR: connection: add helper conn_append_debug_info()
- MINOR: mux-h2/trace: report a few connection-level info during h2_init()
- CLEANUP: mux-h2/traces: better align user messages
- BUG/MINOR: stats: make "show stat typed desc" work again
- MINOR: mux-h2: obey http-ignore-probes during the preface
- BUG/MINOR: mux-h2/traces: bring back the lost "rcvd H2 REQ" trace
- BUG/MINOR: mux-h2/traces: bring back the lost "sent H2 REQ/RES" traces

* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- BUG/MINOR: http_fetch: fix possible uninit sockaddr in fetch_url_ip/port
- CLEANUP: cli/activity: Remove double spacing in set profiling command
- CI: Build VTest with clang
- CI: extend spellchecker whitelist, add "ists" as well
- CLEANUP: assorted typo fixes in the code and comments
- BUG/MINOR: memprof: properly account for differences for realloc()
- MINOR: memprof: also report the method used by each call
- MINOR: memprof: also report the totals and delta alloc-free
- CLEANUP: pattern: remove the unused and dangerous pat_ref_reload()
- BUG/MINOR: http_act: Fix normalizer names in error messages
- MINOR: uri_normalizer: Add `fragment-strip` normalizer
- MINOR: uri_normalizer: Add `fragment-encode` normalizer
- IMPORT: slz: use the generic function for the last bytes of the crc32
- IMPORT: slz: do not produce the crc32_fast table when CRC is natively
  supported
- BUILD/MINOR: opentracing: fixed compilation with filter enabled
- BUILD: makefile: add a few popular ARMv8 CPU targets
- BUG/MEDIUM: stick_table: fix crash when using tcp smp_fetch_src
- REGTESTS: stick-table: add src_conn_rate test
- CLEANUP: stick-table: remove a leftover of an old keyword declaration
- BUG/MINOR: stats: fix lastchk metric that got accidently lost
- EXAMPLES: add a "basic-config-edge" example config
- EXAMPLES: add a trivial config for quick testing
- DOC: management: Correct example reload command in the document
- Revert "CI: Build VTest with clang"
- MINOR: activity/cli: optionally support sorting by address on "show profiling"
- DEBUG: ssl: export ssl_sock_close() to see its symbol resolved in profiling
- BUG/MINOR: lua/vars: prevent get_var() from allocating a new name
- DOC: config: Fix configuration example for mqtt
- BUG/MAJOR: config: properly initialize cpu_map.thread[] up to MAX_THREADS
- BUILD: config: avoid a build warning on numa_detect_topology() without threads
- DOC: update min requirements in INSTALL
- IMPORT: slz: use inttypes.h instead of stdint.h
- BUILD: sample: use strtoll() instead of atoll()
- MINOR: version: mention that it's LTS now.

* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.10-0
- BUILD: backend: fix build breakage in idle conn locking fix
- BUG/MINOR: tcp: fix silent-drop workaround for IPv6
- BUILD: tcp: use IPPROTO_IPV6 instead of SOL_IPV6 on FreeBSD/MacOS
- BUG/MINOR: ssl: Fix update of default certificate
- BUG/MINOR: ssl: Prevent removal of crt-list line if the instance is
  a default one
- BUG/MINOR: http_fetch: make hdr_ip() resistant to empty fields
- BUG/MINOR: ssl: Add missing free on SSL_CTX in ckch_inst_free
- REGTESTS: ssl: "set ssl cert" and multi-certificates bundle
- DOC: Explicitly state only IPv4 are supported by forwardfor/originalto options
- REGTESTS: ssl: mark set_ssl_cert_bundle.vtc as broken
- CONTRIB: halog: fix issue with array of type char
- BUG/MINOR: tools: fix parsing "us" unit for timers
- DOC: clarify that compression works for HTTP/2
- MINOR: No longer rely on deprecated sample fetches for predefined ACLs
- BUG/MEDIUM: sample: Fix adjusting size in field converter
- DOC: ssl: Certificate hot update only works on fronted certificates
- BUG/MEDIUM: threads: Ignore current thread to end its harmless period
- BUG/MINOR: checks: Set missing id to the dummy checks frontend
- MINOR: logs: Add support of checks as session origin to format lf strings
- BUG/MINOR: connection: Fix fc_http_major and bc_http_major for TCP connections
- MINOR: connection: Make bc_http_major compatible with tcp-checks
- BUG/MINOR: ssl-samples: Fix ssl_bc_* samples when called from a health-check
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

* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.9-0
- BUG/MEDIUM: mux-h1: make h1_shutw_conn() idempotent
- MEDIUM: backend: use a trylock to grab a connection on high FD counts as well
- BUG/MINOR: payload: Wait for more data if buffer is empty
  in payload/payload_lv
- BUG/MINOR: stats: Apply proper styles in HTML status page.
- BUG/MEDIUM: time: make sure to always initialize the global tick

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.8-0
- MINOR: time: export the global_now variable
- BUG/MINOR: freq_ctr/threads: make use of the last updated global time
- BUG/MEDIUM: mux-fcgi: Fix locking of idle_conns lock in the FCGI I/O callback
- MINOR: time: also provide a global, monotonic global_now_ms timer
- BUG/MEDIUM: freq_ctr/threads: use the global_now_ms variable
- BUG/MINOR: protocol: add missing support of dgram unix socket.
- MINOR/BUG: mworker/cli: do not use the unix_bind prefix for the master
  CLI socket
- MEDIUM: lua: Use a per-thread counter to track some non-reentrant parts of lua
- BUG/MEDIUM: debug/lua: Don't dump the lua stack if not dumpable
- BUG/MINOR: ssl: Prevent disk access when using "add ssl crt-list"
- BUILD: ssl: guard ecdh functions with SSL_CTX_set_tmp_ecdh macro
- MINOR: lua: Slightly improve function dumping the lua traceback
- BUG/MEDIUM: debug/lua: Use internal hlua function to dump the lua traceback
- BUG/MEDIUM: lua: Always init the lua stack before referencing the context
- MINOR: fd: make fd_clr_running() return the remaining running mask
- MINOR: fd: remove the unneeded running bit from fd_insert()
- BUG/MEDIUM: fd: do not wait on FD removal in fd_delete()
- CLEANUP: fd: remove unused fd_set_running_excl()
- BUG/MEDIUM: fd: Take the fd_mig_lock when closing if no DWCAS is available.
- BUG/MEDIUM: thread: Fix a deadlock if an isolated thread is marked as harmless
- MINOR: tools: make url2ipv4 return the exact number of bytes parsed
- BUG/MINOR: http_fetch: make hdr_ip() reject trailing characters

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.7-0
- BUG/MINOR: backend: fix condition for reuse on mode HTTP
- BUG/MINOR: hlua: Don't strip last non-LWS char in hlua_pushstrippedstring()
- BUG/MINOR: ssl: don't truncate the file descriptor to 16 bits in debug mode
- REORG: atomic: reimplement pl_cpu_relax() from atomic-ops.h
- BUG/MINOR: mt-list: always perform a cpu_relax call on failure
- MINOR: atomic: add armv8.1-a atomics variant for cas-dw
- MINOR: atomic: implement a more efficient arm64 __ha_cas_dw() using pairs
- BUG/MEDIUM: session: NULL dereference possible when accessing the listener
- MINOR: tasks: refine the default run queue depth
- MINOR: listener: refine the default MAX_ACCEPT from 64 to 4
- OPTIM: server: switch the actconn list to an mt-list
- MINOR: server: move actconns to the per-thread structure
- MINOR: lb/api: let callers of take_conn/drop_conn tell if they have the lock
- OPTIM: lb-first: do not take the server lock on take_conn/drop_conn
- OPTIM: lb-leastconn: do not take the server lock on take_conn/drop_conn
- OPTIM: lb-leastconn: do not unlink the server if it did not change
- MINOR: dynbuf: make the buffer wait queue per thread
- MINOR: dynbuf: use regular lists instead of mt_lists for buffer_wait
- MINOR: dynbuf: pass offer_buffers() the number of buffers instead of
  a threshold
- MINOR: stream: add an "epoch" to figure which streams appeared when
- MINOR: cli/streams: make "show sess" dump all streams till the new epoch
- MINOR: streams: use one list per stream instead of a global one
- MEDIUM: streams: do not use the streams lock anymore
- MEDIUM: pools: add CONFIG_HAP_NO_GLOBAL_POOLS and CONFIG_HAP_GLOBAL_POOLS
- MINOR: pools: double the local pool cache size to 1 MB
- MEDIUM: backend: use a trylock when trying to grab an idle connection
- MINOR: task: limit the number of subsequent heavy tasks with flag TASK_HEAVY
- MINOR: ssl: mark the SSL handshake tasklet as heavy
- BUG/MEDIUM: ssl: properly remove the TASK_HEAVY flag at end of handshake
- MINOR: task: add an application specific flag to the state: TASK_F_USR1
- MEDIUM: muxes: mark idle conns tasklets with TASK_F_USR1
- MINOR: xprt: add new xprt_set_idle and xprt_set_used methods
- MEDIUM: ssl: implement xprt_set_used and xprt_set_idle to relax context checks
- MEDIUM: task: remove the tasks_run_queue counter and have one per thread
- MINOR: task: give the scheduler a bit more flexibility in the runqueue size
- OPTIM: task: automatically adjust the default runqueue-depth to the threads
- BUG/MEDIUM: stick-tables: fix ref counter in table entry using multiple
  http tracksc.
- BUILD: atomic/arm64: force the register pairs to use in __ha_cas_dw()
- BUG/MEDIUM: filters: Set CF_FL_ANALYZE on channels when filters are attached
- BUG/MINOR: tcpcheck: Update .health threshold of agent inside an agent-check
- BUG/MINOR: proxy/session: Be sure to have a listener to increment its counters
- BUG/MINOR: session: Add some forgotten tests on session's listener
- BUG/MINOR: tcpcheck: Fix double free on error path when parsing tcp/http-check
- CLEANUP: tcp-rules: add missing actions in the tcp-request error message
- Revert "BUG/MINOR: resolvers: Only renew TTL for SRV records with
  an additional record"
- BUG/MINOR: resolvers: Consider server to have no IP on DNS resolution error
- BUG/MINOR: resolvers: Reset server address on DNS error only on status change
- BUG/MINOR: resolvers: Unlink DNS resolution to set RMAINT on SRV resolution
- BUG/MEDIUM: resolvers: Don't set an address-less server as UP
- BUG/MEDIUM: resolvers: Fix the loop looking for an existing ADD item
- MINOR: resolvers: new function find_srvrq_answer_record()
- BUG/MINOR; resolvers: Ignore DNS resolution for expired SRV item
- BUG/MEDIUM: resolvers: Trigger a DNS resolution if an ADD item is obsolete
- MINOR: resolvers: Use a function to remove answers attached to a resolution
- MINOR: resolvers: Purge answer items when a SRV resolution triggers an error
- MINOR: resolvers: Add function to change the srv status based on
  SRV resolution
- MINOR: resolvers: Directly call srvrq_update_srv_state() when possible
- BUG/MEDIUM: resolvers: Don't release resolution from a requester callbacks
- BUG/MEDIUM: resolvers: Skip DNS resolution at startup if SRV resolution is set
- MINOR: resolvers: Use milliseconds for cached items in resolver responses
- MINOR: resolvers: Don't try to match immediatly renewed ADD items
- BUG/MINOR: resolvers: Add missing case-insensitive comparisons
  of DNS hostnames

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.6-0
- MINOR: check: do not ignore a connection header for http-check send
- BUILD: ssl: fix typo in HAVE_SSL_CTX_ADD_SERVER_CUSTOM_EXT macro
- BUILD: ssl: guard SSL_CTX_add_server_custom_ext with special macro
- BUILD: ssl: guard SSL_CTX_set_msg_callback with
  SSL_CTRL_SET_MSG_CALLBACK macro
- BUG/MINOR: intops: fix mul32hi()'s off-by-one
- BUG/MINOR: http-ana: Don't increment HTTP error counter on internal errors
- BUG/MEDIUM: mux-h1: Always set CS_FL_EOI for response in MSG_DONE state
- BUG/MINOR: server: re-align state file fields number
- BUG/MINOR: tools: Fix a memory leak on error path in parse_dotted_uints()
- BUG/MINOR: backend: hold correctly lock when killing idle conn
- BUG/MINOR: server: Fix server-state-file-name directive
- CLEANUP: deinit: release global and per-proxy server-state variables on deinit
- BUG/MEDIUM: config: don't pick unset values from last defaults section
- BUG/MINOR: stats: revert the change on ST_CONVDONE
- BUG/MINOR: cfgparse: do not mention "addr:port" as supported on proxy lines
- BUG/MINOR: server: Don't call fopen() with server-state filepath set to NULL
- DOC: tune: explain the origin of block size for ssl.cachesize
- CLEANUP: channel: fix comment in ci_putblk.
- BUG/MINOR: server: Remove RMAINT from admin state when loading server state
- BUG/MINOR: session: atomically increment the tracked sessions counter
- BUG/MINOR: checks: properly handle wrapping time in __health_adjust()
- BUG/MEDIUM: checks: don't needlessly take the server lock in health_adjust()
- BUG/MINOR: sample: Always consider zero size string samples as unsafe
- BUILD: ssl: introduce fine guard for OpenSSL specific SCTL functions
- DOC: explain the relation between pool-low-conn and tune.idle-pool.shared
- BUG/MEDIUM: lists: Avoid an infinite loop in MT_LIST_TRY_ADDQ().
- BUG/MEDIUM: spoe: Resolve the sink if a SPOE logs in a ring buffer
- BUG/MINOR: http-rules: Always replace the response status on a return action
- BUG/MINOR: server: Init params before parsing a new server-state line
- BUG/MINOR: server: Be sure to cut the last parsed field of a server-state line
- BUG/MEDIUM: mux-h1: Fix handling of responses to CONNECT other than 200-ok
- BUG/MINOR: ssl/cli: potential null pointer dereference in "set ssl cert"
- MINOR: Configure the `cpp` userdiff driver for *.[ch] in .gitattributes
- BUG/MINOR: sample: secure convs that accept base64 string and var name as args
- BUG/MEDIUM: vars: make functions vars_get_by_{name,desc} thread-safe
- BUG/MEDIUM: proxy: use thread-safe stream killing on hard-stop
- BUG/MEDIUM: cli/shutdown sessions: make it thread-safe
- BUG/MINOR: proxy: wake up all threads when sending the hard-stop signal
- BUG/MINOR: fd: properly wait for !running_mask in fd_set_running_excl()
- BUG/MINOR: resolvers: Fix condition to release received ARs if not assigned
- BUG/MINOR: resolvers: Only renew TTL for SRV records with an additional record
- BUG/MINOR: resolvers: new callback to properly handle SRV record errors
- BUG/MEDIUM: resolvers: Reset server address and port for obselete SRV records
- BUG/MEDIUM: resolvers: Reset address for unresolved servers
- BUG/MINOR: ssl: potential null pointer dereference in ckchs_dup()
- CLEANUP: muxes: Remove useless if condition in show_fd function
- BUG/MINOR: stats: fix compare of no-maint url suffix
- BUG/MINOR: mux-h1: Immediately report H1C errors from h1_snd_buf()
- BUG/MINOR: http-ana: Only consider dst address to process originalto option
- BUG/MINOR: tcp-act: Don't forget to set the original port for
  IPv4 set-dst rule
- BUG/MINOR: connection: Use the client's dst family for adressless servers
- BUG/MEDIUM: spoe: Kill applets if there are pending connections
  and nbthread > 1
- DOC: spoe: Add a note about fragmentation support in HAProxy
- BUG/MINOR: mux-h2: Fix typo in scheme adjustment
- BUG/MINOR: http-ana: Don't increment HTTP error counter on read error/timeout

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.5-0
- BUG/MINOR: init: Use a dynamic buffer to set HAPROXY_CFGFILES env variable
- MINOR: config: Add failifnotcap() to emit an alert on proxy capabilities
- MINOR: server: Forbid server definitions in frontend sections
- BUG/MINOR: threads: Fixes the number of possible cpus report for Mac.
- MINOR: peers: Add traces for peer control messages.
- BUG/MINOR: dns: SRV records ignores duplicated AR records (v2)
- BUILD: peers: fix build warning about unused variable
- BUG/MEDIUM: stats: add missing INF_BUILD_INFO definition
- BUG/MINOR: peers: Possible appctx pointer dereference.
- MINOR: build: discard echoing in help target
- BUG/MINOR: peers: Wrong "new_conn" value for "show peers" CLI command.
- BUG/MINOR: mux_h2: missing space between "st" and ".flg" in the "show fd"
  helper
- BUG/MINOR: mworker: define _GNU_SOURCE for strsignal()
- BUG/MEDIUM: tcpcheck: Don't destroy connection in the wake callback context
- BUG/MEDIUM: mux-h2: fix read0 handling on partial frames
- BUILD/MINOR: lua: define _GNU_SOURCE for LLONG_MAX
- DOC: Improve documentation of the various hdr() fetches
- BUG/MEDIUM: filters/htx: Fix data forwarding when payload length is unknown
- BUG/MINOR: config: fix leak on proxy.conn_src.bind_hdr_name
- BUG/MINOR: ssl: init tmp chunk correctly in ssl_sock_load_sctl_from_file()
- BUG/MEDIUM: session: only retrieve ready idle conn from session
- REORG: backend: simplify conn_backend_get
- BUG/MEDIUM: backend: never reuse a connection for tcp mode
- BUG/MINOR: backend: check available list allocation for reuse
- MINOR: contrib: Make the wireshark peers dissector compile for more distribs.
- CLEANUP: tools: make resolve_sym_name() take a const pointer
- CLEANUP: cli: make "show fd" use a const connection to access other fields
- MINOR: cli: make "show fd" also report the xprt and xprt_ctx
- MINOR: xprt: add a new show_fd() helper to complete some "show fd" dumps.
- MINOR: ssl: provide a "show fd" helper to report important SSL information
- MINOR: xprt/mux: export all *_io_cb functions so that "show fd" resolves them
- MINOR: mux-h2: make the "show fd" helper also decode the h2s subscriber
  when known
- MINOR: mux-h1: make the "show fd" helper also decode the h1s subscriber
  when known
- MINOR: mux-fcgi: make the "show fd" helper also decode the fstrm subscriber
  when known
- MINOR: cli: give the show_fd helpers the ability to report a suspicious entry
- MINOR: cli/show_fd: report some easily detectable suspicious states
- MINOR: ssl/show_fd: report some FDs as suspicious when possible
- MINOR: mux-h2/show_fd: report as suspicious an entry with too many calls
- MINOR: mux-h1/show_fd: report as suspicious an entry with too many calls
- MINOR: h1: Raise the chunk size limit up to (2^52 - 1)
- DOC: management: fix "show resolvers" alphabetical ordering
- BUG/MINOR: stick-table: Always call smp_fetch_src() with a valid arg list
- BUG/MEDIUM: ssl/cli: abort ssl cert is freeing the old store
- BUG/MEDIUM: ssl: check a connection's status before computing a handshake
- BUG/MINOR: mux_h2: fix incorrect stat titles
- BUG/MINOR: xxhash: make sure armv6 uses memcpy()
- BUG/MINOR: ssl: do not try to use early data if not configured
- BUILD: ssl: fix build breakage with last commit
- MINOR: cli/show_fd: report local and report ports when known
- BUILD: Makefile: move REGTESTST_TYPE default setting
- BUG/MEDIUM: mux-h2: handle remaining read0 cases
- BUG/MEDIUM: mux-h2: do not quit the demux loop before setting END_REACHED
- BUG/MINOR: sock: Unclosed fd in case of connection allocation failure
- MINOR: config: Deprecate and ignore tune.chksize global option

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.4-0
- MINOR: reg-tests: add a way to add service dependency
- BUG/MINOR: sample: check alloc_trash_chunk return value in concat()
- BUG/MINOR: reg-tests: fix service dependency script
- MINOR: reg-tests: add base prometheus test
- Revert "BUG/MINOR: dns: SRV records ignores duplicated AR records"
- BUG/MINOR: sample: Memory leak of sample_expr structure in case of error
- BUG/MINOR: check: Don't perform any check on servers defined in a frontend
- BUG/MINOR: init: enforce strict-limits when using master-worker
- MINOR: contrib/prometheus-exporter: avoid connection close header
- MINOR: contrib/prometheus-exporter: use fill_info for process dump

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- MINOR: plock: use an ARMv8 instruction barrier for the pause instruction
- BUG/MEDIUM: lists: Lock the element while we check if it is in a list.
- MINOR: task: remove __tasklet_remove_from_tasklet_list()
- BUG/MEDIUM: task: close a possible data race condition on a tasklet's
  list link
- BUG/MEDIUM: local log format regression.
- BUG/MINOR: mux-h2/stats: make stream/connection proto errors more accurate
- BUG/MINOR: mux-h2/stats: not all GOAWAY frames are errors
- BUG/MINOR: lua: missing "\n" in error message
- BUG/MINOR: lua: lua-load doesn't check its parameters
- BUG/MINOR: lua: Post init register function are not executed beyond
  the first one
- BUG/MINOR: lua: Some lua init operation are processed unsafe
- MINOR: actions: Export actions lookup functions
- MINOR: actions: add a function returning a service pointer from its name
- MINOR: cli: add a function to look up a CLI service description
- BUG/MINOR: lua: warn when registering action, conv, sf, cli or applet
  multiple times
- BUG/MAJOR: ring: tcp forward on ring can break the reader counter.
- BUILD/MINOR: haproxy DragonFlyBSD affinity build update.
- DOC/MINOR: Fix formatting in Management Guide
- BUG/MINOR: listener: use sockaddr_in6 for IPv6
- BUG/MINOR: mux-h1: Handle keep-alive timeout for idle frontend connections
- MINOR: protocol: add a ->set_port() helper to address families
- MINOR: listener: automatically set the port when creating listeners
- MINOR: listener: now use a generic add_listener() function
- MEDIUM: ssl: fatal error with bundle + openssl < 1.1.1
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
- BUG/MINOR: http-check: Use right condition to consider HTX message as full
- BUG/MINOR: tcpcheck: Don't rearm the check timeout on each read
- MINOR: tcpcheck: Only wait for more payload data on HTTP expect rules
- BUG/MINOR: tools: make parse_time_err() more strict on the timer validity
- BUG/MINOR: tools: Reject size format not starting by a digit
- BUG/MEDIUM: lb-leastconn: Reposition a server using the right eweight
- BUG/MEDIUM: ssl/crt-list: bad behavior with "commit ssl cert"
- REGTESTS: make use of HAPROXY_ARGS and pass -dM by default
- BUILD: SSL: fine guard for SSL_CTX_add_server_custom_ext call
- BUILD: Makefile: have "make clean" destroy .o/.a/.s in contrib subdirs as well
- BUG/MINOR: mux-h1: Don't set CS_FL_EOI too early for protocol upgrade requests
- BUG/MEDIUM: http-ana: Never for sending data in TUNNEL mode
- BUG/MEDIUM: mux-h1: Handle h1_process() failures on a pipelined request
- CONTRIB: halog: fix build issue caused by %%L printf format
- CONTRIB: halog: mark the has_zero* functions unused
- CONTRIB: halog: fix signed/unsigned build warnings on counts and timestamps
- CONTRIB: debug: address "poll" utility build on non-linux platforms
- BUILD: plock: remove dead code that causes a warning in gcc 11
- BUILD: ssl: fine guard for SSL_CTX_get0_privatekey call
- BUG/MINOR: dns: SRV records ignores duplicated AR records
- DOC: fix "smp_size" vs "sample_size" in "log" directive arguments
- BUG/MEDIUM: mux_h2: Add missing braces in h2_snd_buf()around trace+wakeup
- BUILD: hpack: hpack-tbl-t.h uses VAR_ARRAY but does not include compiler.h
- MINOR: atomic: don't use ; to separate instruction on aarch64.
- BUG/MINOR: sink: Return an allocation failure in __sink_new if strdup() fails
- BUG/MINOR: cfgparse: Fail if the strdup() for `rule->be.name` for
  `use_backend` fails
- BUG/MINOR: tcpcheck: Report a L7OK if the last evaluated rule is a send rule
- DOC: Improve the message printed when running `make` w/o `TARGET`
- BUG/MINOR: stats: Make stat_l variable used to dump a stat line thread local
- SCRIPTS: improve announce-release to support different tag and versions
- SCRIPTS: make announce release support preparing announces before tag exists
- BUG/MINOR: srv: do not init address if backend is disabled
- BUG/MINOR: srv: do not cleanup idle conns if pool max is null
- MINOR: converter: adding support for url_enc
- BUILD: Makefile: exclude broken tests by default
- CLEANUP: cfgparse: replace "realloc" with "my_realloc2" to fix to memory
  leak on error
- MINOR: contrib/prometheus-exporter: export build_info
- DOC: fix some spelling issues over multiple files
- SCRIPTS: announce-release: fix typo in help message
- DOC: Add maintainers for the Prometheus exporter
- BUG/MINOR: sample: fix concat() converter's corruption with non-string
  variables

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- BUILD: http-htx: fix build warning regarding long type in printf
- CLEANUP: cfgparse: remove duplicate registration for transparent build options
- BUG/MEDIUM: filters: Forward all filtered data at the end of http filtering
- BUG/MINOR: http-ana: Don't wait for the body of CONNECT requests
- DOC: add missing 3.10 in the summary
- BUG/MINOR: ssl: segv on startup when AKID but no keyid
- BUG/MEDIUM: http-ana: Don't eval http-after-response ruleset on empty messages
- BUG/MEDIUM: ssl/crt-list: bundle support broken in crt-list
- BUG/MEDIUM: ssl: error when no certificate are found
- BUG/MINOR: ssl/crt-list: load bundle in crt-list only if activated
- BUG/MEDIUM: ssl/crt-list: fix error when no file found
- BUILD: makefile: enable crypt(3) for OpenBSD
- DOC: clarify how to create a fallback crt
- CLEANUP: connection: do not use conn->owner when the session is known
- BUG/MAJOR: connection: reset conn->owner when detaching from session list
- BUG/MINOR: http_htx: Fix searching headers by substring
- DOC: better describes how to configure a fallback crt
- BUG/MAJOR: filters: Always keep all offsets up to date during data filtering
- MEDIUM: cache: Change caching conditions
- DOC: cache: Add new caching limitation information
- REGTESTS: Add sample_fetches/cook.vtc
- REGTESTS: converter: add url_dec test
- MINOR: http_act: Add -m flag for del-header name matching method
- BUILD: Make DEBUG part of .build_opts
- BUILD: Show the value of DEBUG= in haproxy -vv
- BUG/MEDIUM: http_act: Restore init of log-format list
- BUG/MAJOR: peers: fix partial message decoding
- DOC: better document the config file format and escaping/quoting rules
- DOC: Clarify %%HP description in log-format
- BUG/MINOR: tcpcheck: Don't forget to reset tcp-check flags on new kind of
  check
- MINOR: tcpcheck: Don't handle anymore in-progress send rules in tcpcheck_main
- BUG/MAJOR: tcpcheck: Allocate input and output buffers from the buffer pool
- DOC: config: Move req.hdrs and req.hdrs_bin in L7 samples fetches section
- BUG/MINOR: http-fetch: Fix smp_fetch_body() when called from a health-check

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- BUG/MINOR: ssl: don't report 1024 bits DH param load error when it's higher
- MINOR: http-htx: Add understandable errors for the errorfiles parsing
- DOC: config: Fix a typo on ssl_c_chain_der
- BUG/MEDIUM: ssl/crt-list: correctly insert crt-list line if crt already loaded
- BUG/MINOR: pattern: a sample marked as const could be written
- BUG/MINOR: lua: set buffer size during map lookups
- BUG/MINOR: stats: free dynamically stats fields/lines on shutdown
- BUG/MINOR: peers: Do not ignore a protocol error for dictionary entries.
- BUG/MINOR: peers: Missing TX cache entries reset.
- BUG/MEDIUM: peers: fix decoding of multi-byte length in stick-table messages
- BUG/MINOR: http-fetch: Extract cookie value even when no cookie name
- BUG/MINOR: http-fetch: Fix calls w/o parentheses of the cookie sample fetches
- BUG/MEDIUM: check: reuse srv proto only if using same mode
- MINOR: check: report error on incompatible proto
- MINOR: check: report error on incompatible connect proto
- BUG/MINOR: http-htx: Handle warnings when parsing http-error and http-errors
- BUG/MAJOR: spoe: Be sure to remove all references on a released spoe applet
- MINOR: spoe: Don't close connection in sync mode on processing timeout
- BUG/MINOR: tcpcheck: Don't warn on unused rules if check option is after
- MINOR: init: Fix the prototype for per-thread free callbacks
- MINOR: config/mux-h2: Return ERR_ flags from init_h2() instead of a status
- MINOR: cfgparse: tighten the scope of newnameserver variable, free it on
  error.
- REGTEST: ssl: test wildcard and multi-type + exclusions
- REGTEST: ssl: mark reg-tests/ssl/ssl_crt-list_filters.vtc as broken
- MINOR: peers: Add traces to peer_treat_updatemsg().
- REGTEST: make ssl_client_samples and ssl_server_samples require to 2.2

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Initial build for kaos repository
