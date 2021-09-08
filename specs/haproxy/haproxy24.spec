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
%define major_ver         24

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

Name:              haproxy%{major_ver}
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.4.4
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.4/src/%{orig_name}-%{version}.tar.gz
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

%{__make} admin/halog/halog

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
* Wed Sep 08 2021 Anton Novojilov <andy@essentialkaos.com> - 2.4.4-0
- BUG/MEDIUM: h2: match absolute-path not path-absolute for :path
- REGTESTS: http_upgrade: fix incorrect expectation on TCP->H1->H2
- REGTESTS: abortonclose: after retries, 503 is expected, not close
- MINOR: hlua: take the global Lua lock inside a global function
- BUG/MINOR: stick-table: fix the sc-set-gpt* parser when using expressions
- BUG/MEDIUM: base64: check output boundaries within base64{dec,urldec}
- BUG/MINOR: base64: base64urldec() ignores padding in output size check
- MINOR: compiler: implement an ONLY_ONCE() macro
- BUG/MINOR: lua: use strlcpy2() not strncpy() to copy sample keywords
- BUG/MINOR: time: fix idle time computation for long sleeps
- MINOR: time: add report_idle() to report process-wide idle time
- BUG/MINOR: ebtree: remove dependency on incorrect macro for bits per long
- BUG/MINOR threads: Use get_(local|gm)time instead of (local|gm)time
- BUG/MINOR: tools: Fix loop condition in dump_text()
- CLEANUP: Add missing include guard to signal.h
- BUG/MINOR: vars: fix set-var/unset-var exclusivity in the keyword parser
- DOC: configuration: remove wrong tcp-request examples in tcp-response
- BUG/MINOR: config: reject configs using HTTP with bufsize >= 256 MB
- CLEANUP: htx: remove comments about "must be < 256 MB"
- BUG/MAJOR: htx: fix missing header name length check in htx_add_header/trailer
- Revert "BUG/MINOR: stream-int: Don't block reads in si_update_rx() if chn
  may receive"

* Wed Aug 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.4.3-0
- BUILD: http_htx: fix ci compilation error with isdigit for Windows
- MINOR: mux_h2: define config to disable h2 websocket support
- BUG/MINOR: ssl: Default-server configuration ignored by server
- BUILD: add detection of missing important CFLAGS
- BUILD: lua: silence a build warning with TCC
- BUG/MEDIUM: mworker: do not register an exit handler if exit is expected
- BUG/MINOR: mworker: do not export HAPROXY_MWORKER_REEXEC across programs
- BUILD/MINOR: memprof fix macOs build.
- BUG/MEDIUM: ssl_sample: fix segfault for srv samples on invalid request
- BUG/MINOR: stats: Add missing agent stats on servers
- BUG/MINOR: check: fix the condition to validate a port-less server
- BUG/MINOR: resolvers: Use a null-terminated string to lookup in servers tree
- BUG/MINOR: systemd: must check the configuration using -Ws
- BUG/MINOR: mux-h1: Obey dontlognull option for empty requests
- BUG/MINOR: mux-h2: Obey dontlognull option during the preface
- BUG/MINOR: mux-h1: Be sure to swap H1C to splice mode when rcv_pipe()
  is called
- BUG/MEDIUM: mux-h2: Handle remaining read0 cases on partial frames
- BUG/MINOR: connection: Add missing error labels to conn_err_code_str
- BUG/MEDIUM: connection: close a rare race between idle conn close and takeover
- BUG/MEDIUM: pollers: clear the sleeping bit after waking up, not before
- BUG/MINOR: select: fix excess number of dead/skip reported
- BUG/MINOR: poll: fix abnormally high skip_fd counter
- BUG/MINOR: pollers: always program an update for migrated FDs
- BUG/MINOR: fd: protect fd state harder against a concurrent takeover
- DOC: internals: document the FD takeover process
- BUILD: opentracing: fixed build when using pkg-config utility
- BUG/MINOR: server: remove srv from px list on CLI 'add server' error
- BUG/MINOR: server: update last_change on maint->ready transitions too
- MINOR: server: unmark deprecated on enable health/agent cli
- ADMIN: dyncookie: implement a simple dynamic cookie calculator
- MINOR: spoe: Add a pointer on the filter config in the spoe_agent structure
- BUG/MEDIUM: spoe: Create a SPOE applet if necessary when the last one
  is released
- BUG/MINOR: buffer: fix buffer_dump() formatting
- BUG/MINOR: tcpcheck: Properly detect pending HTTP data in output buffer
- DOC: Improve the lua documentation
- DOC: config: Fix 'http-response send-spoe-group' documentation
- BUG/MEDIUM: spoe: Fix policy to close applets when SPOE connections are queued
- BUG/MEDIUM: cfgcheck: verify existing log-forward listeners during
  config check
- CLEANUP: assorted typo fixes in the code and comments
- DOC/MINOR: fix typo in management document
- MINOR: http: add a new function http_validate_scheme() to validate a scheme
- BUG/MAJOR: h2: verify early that non-http/https schemes match the valid syntax
- BUG/MAJOR: h2: verify that :path starts with a '/' before concatenating it
- BUG/MAJOR: h2: enforce stricter syntax checks on the :method pseudo-header
- BUG/MEDIUM: h2: give :authority precedence over Host
- REGTESTS: add a test to prevent h2 desync attacks

* Thu Jul 08 2021 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- BUG/MINOR: server-state: load SRV resolution only if params match the config
- BUG/MINOR: server: Forbid to set fqdn on the CLI if SRV resolution is enabled
- BUG/MEDIUM: server/cli: Fix ABBA deadlock when fqdn is set from the CLI
- MINOR: resolvers: Clean server in a dedicated function when removing
  a SRV item
- MINOR: resolvers: Remove server from named_servers tree when removing
  a SRV item
- BUG/MEDIUM: resolvers: Add a task on servers to check SRV resolution status
- BUG/MINOR: resolvers: Use resolver's lock in resolv_srvrq_expire_task()
- BUG/MINOR: server/cli: Fix locking in function processing "set server" command
- BUG/MINOR: cache: Correctly handle existing-but-empty 'accept-encoding' header
- BUG/MAJOR: server: fix deadlock when changing maxconn via agent-check
- REGTESTS: fix maxconn update with agent-check
- MINOR: tcp-act: Add set-src/set-src-port for "tcp-request content" rules
- DOC: config: Add missing actions in "tcp-request session" documentation
- CLEANUP: dns: Remove a forgotten debug message
- BUG/MINOR: resolvers: Always attach server on matching record on resolution
- BUG/MINOR: resolvers: Reset server IP when no ip is found in the response
- MINOR: resolvers: Reset server IP on error in resolv_get_ip_from_response()
- BUG/MINOR: checks: return correct error code for srv_parse_agent_check
- BUILD: Makefile: fix linkage for Haiku.
- BUG/MINOR: tcpcheck: Fix numbering of implicit HTTP send/expect rules
- BUG/MINOR: mqtt: Fix parser for string with more than 127 characters
- BUG/MINOR: mqtt: Support empty client ID in CONNECT message
- BUG/MEDIUM: resolvers: Make 1st server of a template take part to
  SRV resolution
- DOC: config: use CREATE USER for mysql-check
- BUG/MINOR: stick-table: fix several printf sign errors dumping tables
- BUG/MINOR: peers: fix data_type bit computation more than 32 data_types
- DOC: stick-table: add missing documentation about gpt0 stored type
- BUG/MEDIUM: sock: make sure to never miss early connection failures
- BUG/MINOR: cli: fix server name output in "show fd"
- Revert "MINOR: tcp-act: Add set-src/set-src-port for "tcp-request
  content" rules"
- MINOR: http: implement http_get_scheme
- MEDIUM: http: implement scheme-based normalization
- MEDIUM: h1-htx: apply scheme-based normalization on h1 requests
- MEDIUM: h2: apply scheme-based normalization on h2 requests
- REGTESTS: add http scheme-based normalization test

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
- Initial build for kaos repository
