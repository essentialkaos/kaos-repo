################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  2.4
%define comp_ver   24

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   1.1.1v
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.4.24
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

Conflicts:      haproxy haproxy22 haproxy26 haproxy28

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
                          SSL_LIB=openssl-%{openssl_ver}/build/lib \
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
* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 2.4.24-0
- MINOR: proto_uxst: add resume method
- CLEANUP: listener: function comment typo in stop_listener()
- BUG/MINOR: listener: null pointer dereference suspected by coverity
- MINOR: listener/api: add lli hint to listener functions
- MINOR: listener: add relax_listener() function
- MINOR: listener: workaround for closing a tiny race between resume_listener()
  and stopping
- MINOR: listener: make sure we don't pause/resume bypassed listeners
- BUG/MEDIUM: listener: fix pause_listener() suspend return value handling
- BUG/MINOR: listener: fix resume_listener() resume return value handling
- BUG/MEDIUM: resume from LI_ASSIGNED in default_resume_listener()
- MINOR: listener: pause_listener() becomes suspend_listener()
- BUG/MEDIUM: listener/proxy: fix listeners notify for proxy resume
- MEDIUM: proto_ux: properly suspend named UNIX listeners
- MINOR: proto_ux: ability to dump ABNS names in error messages
- MINOR: lua: Add a function to get a reference on a table in the stack
- CLEANUP: Remove unused function hlua_get_top_error_string
- MINOR: hlua: add simple hlua reference handling API
- BUG/MINOR: hlua: fix reference leak in core.register_task()
- BUG/MINOR: hlua: fix reference leak in hlua_post_init_state()
- MINOR: hlua: simplify lua locking
- BUG/MEDIUM: hlua: prevent deadlocks with main lua lock
- BUG/MINOR: server: inherit from netns in srv_settings_cpy()
- BUG/MINOR: namespace: missing free in netns_sig_stop()
- BUG/MEDIUM: mworker: increase maxsock with each new worker
- DOC: Add tune.h2.max-frame-size option to table of contents
- BUILD: debug: avoid a build warning related to epoll_wait() in debug code
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
- BUG/MINOR: hlua: hlua_yieldk ctx argument should support pointers
- BUG/MINOR: sample: Fix wrong overflow detection in add/sub conveters
- BUG/MINOR: http: Return the right reason for 302
- CI: explicitely highlight VTest result section if there's something
- BUG/MINOR: hlua: add check for lua_newstate
- BUG/MINOR: h1-htx: Return the right reason for 302 FCGI responses
- BUG/MEDIUM: listener: Acquire proxy's lock in relax_listener() if necessary
- DOC: configuration: describe Td in Timing events
- BUG/MINOR: chunk: fix chunk_appendf() to not write a zero if buffer is full
- BUG/MAJOR: http-ana: Get a fresh trash buffer for each header value
  replacement
- BUG/MAJOR: http: reject any empty content-length header value
- MINOR: ist: add new function ist_find_range() to find a character range
- MINOR: http: add new function http_path_has_forbidden_char()
- MINOR: h2: pass accept-invalid-http-request down the request parser
- REGTESTS: http-rules: add accept-invalid-http-request for normalize-uri tests
- BUG/MINOR: h1: do not accept '#' as part of the URI component
- BUG/MINOR: h2: reject more chars from the :path pseudo header
- REGTESTS: http-rules: verify that we block '#' by default for normalize-uri
- DOC: clarify the handling of URL fragments in requests
- BUG/MINOR: http: skip leading zeroes in content-length values

* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.4.23-0
- DEV: hpack: fix `trash` build regression
- BUG/MINOR: ssl: ssl-(min|max)-ver parameter not duplicated for bundles in
  crt-list
- BUG/MINOR: mworker: stop doing strtok directly from the env
- BUG/MEDIUM: mworker: don't register mworker_accept_wrapper() when master FD
  is wrong
- MINOR: startup: HAPROXY_STARTUP_VERSION contains the version used to start
- BUG/MINOR: sched: properly report long_rq when tasks remain in the queue
- BUG/MEDIUM: sched: allow a bit more TASK_HEAVY to be processed when needed
- BUG/MINOR: mworker: prevent incorrect values in uptime
- BUG/MINOR: cache: Cache response even if request has "no-cache" directive
- BUG/MINOR: cache: Check cache entry is complete in case of Vary
- BUG/MINOR: ring: do not realign ring contents on resize
- DOC: config: Fix description of options about HTTP connection modes
- DOC: config: Add the missing tune.fail-alloc option from global listing
- DOC: config: Clarify the meaning of 'hold' in the 'resolvers' section
- BUG/MINOR: http-check: Don't set HTX_SL_F_BODYLESS flag with a log-format body
- BUG/MINOR: http-check: Skip C-L header for empty body when it's not mandatory
- BUG/MINOR: http-ana: Do a L7 retry on read error if there is no response
- BUG/MINOR: ssl: Use 'date' instead of 'now' in ocsp stapling callback
- BUG/MINOR: init: properly detect NUMA bindings on large systems
- BUG/MINOR: init: make sure to always limit the total number of threads
- DOC/CLEANUP: fix typos
- BUG/MINOR: mux-h2: make sure the h2c task exists before refreshing it
- BUG/MEDIUM: listener: duplicate inherited FDs if needed
- BUG/MEDIUM: spoe: Don't set the default traget for the SPOE agent frontend
- BUG/MINOR: proto_ux: report correct error when bind_listener fails
- BUG/MINOR: protocol: fix minor memory leak in protocol_bind_all()
- BUG/MINOR: sock_unix: match finalname with tempname in sock_unix_addrcmp()
- BUG/MEDIUM: connection: Clear flags when a conn is removed from an idle list
- BUG/MEDIUM: connection: Preserve flags when a conn is removed from an idle
  list
- BUG/MEDIUM: mux-h2: erase h2c->wait_event.tasklet on error path
- BUG/MEDIUM: mux-h1: Wakeup H1C on shutw if there is no I/O subscription
- BUILD: da: extends CFLAGS to support API v3 from 3.1.7 and onwards.
- MINOR: proxy/pool: prevent unnecessary calls to pool_gc()
- DOC: config: strict-sni allows to start without certificate
- BUG/MEDIUM: channel: Improve reports for shut in co_getblk()
- BUG/MEDIUM: dns: Properly handle error when a response consumed
- MINOR: proxy: check if p is NULL in free_proxy()
- BUG/MINOR: sink: free forward_px on deinit()
- BUG/MINOR: log: free log forward proxies on deinit()
- BUG/MINOR: hlua: enforce proper running context for register_x functions
- CLEANUP: hlua: fix conflicting comment in hlua_ctx_destroy()
- BUG/MEDIUM: resolvers: Force the connect timeout for DNS resolutions
- BUG/MINOR: stick_table: alert when type len has incorrect characters
- CI: bump "actions/checkout" to v3 for cross zoo matrix
- REGTESTS: fix the race conditions in log_uri.vtc
- BUG/MEDIUM: log: Properly handle client aborts in syslog applet
- CLEANUP: backend: Remove useless debug message in assign_server()
- BUG/MINOR: cfgparse: make sure to include openssl-compat
- BUG/MEDIUM: proxy/sktable: prevent watchdog trigger on soft-stop
- BUG/MEDIUM: Update read expiration date on synchronous send
- BUG/MINOR: mux-h2: make sure to produce a log on invalid requests
- MINOR: checks: make sure spread-checks is used also at boot time
- MINOR: clock: measure the total boot time
- BUG/MINOR: checks: postpone the startup of health checks by the boot time
- BUG/MINOR: clock: fix the boot time measurement method for 2.6 and older
- BUG/MINOR: tcp-rules: Don't shortened the inspect-delay when EOI is set
- DOC: config: Clarify conditions to shorten the inspect-delay for TCP rules
- DOC: add size format section to manual
- DOC/MINOR: config: Fix typo in description for `ssl_bc` in configuration.txt
- BUG/MINOR: hlua: unsafe hlua_lua2smp() usage
- SCRIPTS: publish-release: update the umask to keep group write access
- BUG/MINOR: log: fix memory error handling in parse_logsrv()
- BUG/MINOR: proxy: missing free in free_proxy for redirect rules
- MINOR: spoe: Don't stop disabled proxies
- BUILD: mjson: Fix warning about unused variables
- BUG/MINOR: debug: do not emit empty lines in thread dumps
- BUG/MEDIUM: spoe: Don't start new applet if there are enough idle ones
- CI: switch to Fastly CDN to download LibreSSL
- BUILD: ssl: switch LibreSSL to Fastly CDN
- BUG/MINOR: server: incorrect report for tracking servers leaving drain
- MINOR: server: explicitly commit state change in srv_update_status()
- BUG/MINOR: server: don't miss proxy stats update on server state transitions
- BUG/MINOR: server: don't miss server stats update on server state transitions
- BUG/MINOR: server: don't use date when restoring last_change from state file
- CI: cirrus-ci: bump FreeBSD image to 13-1
- BUG/MEDIUM: filters: Don't deinit filters for disabled proxies during startup
- MINOR: proxy: add http_free_redirect_rule() function
- BUG/MINOR: http_rules: fix errors paths in http_parse_redirect_rule()
- DOC: config: Fix bind/server/peer documentation in the peers section
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
