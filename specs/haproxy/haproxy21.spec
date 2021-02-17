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

%define lua_ver           5.4.2
%define pcre_ver          8.44
%define openssl_ver       1.1.1j
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.1.11
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.1/src/%{name}-%{version}.tar.gz
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
%if 0%{?rhel} <= 6
                          USE_NS= \
%endif
                          ADDLIB="-ldl -lrt -lpthread" \
                          ${use_regparm}

pushd contrib/halog
  %{__make} halog
popd

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

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/
%endif

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
* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.11-0
- MINOR: http-htx: Add understandable errors for the errorfiles parsing
- BUG/MINOR: http-htx: Just warn if payload of an errorfile doesn't match
  the C-L
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
- DOC: Clarify %%HP description in log-format
- DOC: config: Move req.hdrs and req.hdrs_bin in L7 samples fetches section
- MINOR: plock: use an ARMv8 instruction barrier for the pause instruction
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
- CONTRIB: debug: address "poll" utility build on non-linux platforms
- BUILD: plock: remove dead code that causes a warning in gcc 11
- BUG/MEDIUM: mux_h2: Add missing braces in h2_snd_buf()around trace+wakeup
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

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.10-0
- BUG/MEDIUM: ssl: crt-list negative filters don't work
- MINOR: ssl: reach a ckch_store from a sni_ctx
- BUILD: makefile: Fix building with closefrom() support enabled
- BUG/MINOR: Fix several leaks of 'log_tag' in init().
- DOC: tcp-rules: Refresh details about L7 matching for tcp-request content
  rules
- BUG/MEDIUM: queue: make pendconn_cond_unlink() really thread-safe
- MINOR: counters: fix a typo in comment
- BUG/MINOR: stats: fix validity of the json schema
- MINOR: hlua: Display debug messages on stderr only in debug mode
- BUG/MINOR: peers: Inconsistency when dumping peer status codes.
- BUG/MINOR: mux-h1: Always set the session on frontend h1 stream
- BUG/MEDIUM: mux-fcgi: Don't handle pending read0 too early on streams
- BUG/MEDIUM: mux-h2: Don't handle pending read0 too early on streams
- BUG/MINOR: http-htx: Expect no body for 204/304 internal HTTP responses
- BUG/MINOR: init: only keep rlim_fd_cur if max is unlimited
- BUG/MINOR: mux-h2: do not stop outgoing connections on stopping
- MINOR: fd: report an error message when failing initial allocations
- BUG/MEDIUM: task: bound the number of tasks picked from the wait queue at once
- BUG/MEDIUM: spoe: Unset variable instead of set it if no data provided
- BUG/MEDIUM: mux-h1: Get the session from the H1S when capturing bad messages
- BUG/MEDIUM: lb: Always lock the server when calling server_{take,drop}_conn
- BUG/MINOR: peers: Possible unexpected peer seesion reset after collisions.
- BUILD: ssl: make BoringSSL use its own version numbers
- BUG/MINOR: disable dynamic OCSP load with BoringSSL
- BUG/MEDIUM: ssl: OCSP must work with BoringSSL
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
- MINOR: ist: Add a case insensitive istmatch function
- BUG/MINOR: cache: Manage multiple values in cache-control header value
- BUG/MINOR: cache: Inverted variables in http_calc_maxage function
- BUG/MEDIUM: filters: Don't try to init filters for disabled proxies
- BUG/MINOR: proxy/server: Skip per-proxy/server post-check for disabled proxies
- BUG/MINOR: server: Set server without addr but with dns in RMAINT on startup
- MINOR: server: Copy configuration file and line for server templates
- BUG/MEDIUM: mux-pt: Release the tasklet during an HTTP upgrade
- BUG/MINOR: filters: Skip disabled proxies during startup only
- BUG/MEDIUM: stick-table: limit the time spent purging old entries
- CLEANUP: mux-h2: Remove the h1 parser state from the h2 stream

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.9-0
- BUG/MEDIUM: mux-h1: Refresh H1 connection timeout after a synchronous send
- SCRIPTS: git-show-backports: make -m most only show the left branch
- SCRIPTS: git-show-backports: emit the shell command to backport a commit
- BUG/MINOR: ssl: fix memory leak at OCSP loading
- BUG/MEDIUM: ssl: memory leak of ocsp data at SSL_CTX_free()
- BUG/MEDIUM: map/lua: Return an error if a map is loaded during runtime
- MINOR: arg: Add an argument type to keep a reference on opaque data
- BUG/MINOR: converters: Store the sink in an arg pointer for debug() converter
- BUG/MINOR: lua: Duplicate map name to load it when a new Map object is created
- BUG/MINOR: arg: Fix leaks during arguments validation for fetches/converters
- BUG/MINOR: lua: Check argument type to convert it to IPv4/IPv6 arg validation
- BUG/MINOR: lua: Check argument type to convert it to IP mask in arg validation
- MINOR: hlua: Don't needlessly copy lua strings in trash during args validation
- BUG/MINOR: lua: Duplicate lua strings in sample fetches/converters arg array
- MEDIUM: lua: Don't filter exported fetches and converters
- BUG/MINOR: snapshots: leak of snapshots on deinit()
- BUG/MINOR: stats: use strncmp() instead of memcmp() on health states
- BUG/MEDIUM: htx: smp_prefetch_htx() must always validate the direction
- BUG/MINOR: reload: do not fail when no socket is sent
- MINOR: http-htx: Add an option to eval query-string when the path is replaced
- BUG/MINOR: http-rules: Replace path and query-string in "replace-path" action
- DOC: cache: Use '<name>' instead of '<id>' in error message
- BUG/MAJOR: contrib/spoa-server: Fix unhandled python call leading to memory
  leak
- BUG/MINOR: contrib/spoa-server: Ensure ip address references are freed
- BUG/MINOR: contrib/spoa-server: Do not free reference to NULL
- BUG/MINOR: contrib/spoa-server: Updating references to free in case of failure
- BUG/MEDIUM: contrib/spoa-server: Fix ipv4_address used instead of ipv6_address
- BUG/MINOR: startup: haproxy -s cause 100%% cpu
- BUG/MEDIUM: doc: Fix replace-path action description
- Revert "BUG/MINOR: http-rules: Replace path and query-string in "replace-path"
  action"
- BUG/MEDIUM: ssl: check OCSP calloc in ssl_sock_load_ocsp()
- BUG/MINOR: threads: work around a libgcc_s issue with chrooting
- BUILD: thread: limit the libgcc_s workaround to glibc only
- MINOR: Commit .gitattributes
- CLEANUP: Update .gitignore
- BUG/MINOR: auth: report valid crypto(3) support depending on build options
- BUG/MEDIUM: mux-h1: always apply the timeout on half-closed connections
- BUILD: threads: better workaround for late loading of libgcc_s
- BUG/MEDIUM: pattern: Renew the pattern expression revision when it is pruned
- MINOR: arg: Use chunk_destroy() to release string arguments
- BUG/MEDIUM: http-ana: Don't wait to send 1xx responses received from servers
- BUG/MEDIUM: ssl: does not look for all SNIs before chosing a certificate
- BUG/MINOR: ssl: verifyhost is case sensitive
- BUG/MINOR: server: report correct error message for invalid port on "socks4"
- BUG/MINOR: h2/trace: do not display "stream error" after a frame ACK
- BUG/MINOR: http-fetch: Don't set the sample type during the htx prefetch
- BUG/MEDIUM: h2: report frame bits only for handled types
- MINOR: h2/trace: also display the remaining frame length in traces
- BUG/MINOR: Fix memory leaks cfg_parse_peers
- MINOR: backend: make the "whole" option of balance uri take only one bit
- MINOR: backend: add a new "path-only" option to "balance uri"
- REGTESTS: add a few load balancing tests
- DOC: spoa-server: fix false friends `actually`
- BUG/MINOR: config: Fix memory leak on config parse listen
- BUG/MEDIUM: listeners: do not pause foreign listeners
- DOC: agent-check: fix typo in "fail" word expected reply
- REGTEST: fix host part in balance-uri-path-only.vtc
- REGTEST: make abns_socket.vtc require 1.8
- REGTEST: make map_regm_with_backref require 1.7

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.8-0
- BUG/MEDIUM: log: don't hold the log lock during writev() on a file descriptor
- BUG/MEDIUM: pattern: fix thread safety of pattern matching
- BUILD: make dladdr1 depend on glibc version and not __USE_GNU
- REGTESTS: Add missing OPENSSL to REQUIRE_OPTIONS for lua/txn_get_priv
- REGTESTS: Add missing OPENSSL to REQUIRE_OPTIONS for
  compression/lua_validation
- BUG/MINOR: ssl: fix ssl-{min,max}-ver with openssl < 1.1.0
- BUG/MEDIUM: ssl: crt-list must continue parsing on ERR_WARN
- MINOR: http: Add 410 to http-request deny
- MINOR: http: Add 404 to http-request deny
- BUG/MINOR: http: make smp_fetch_body() report that the contents may change
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
- BUILD: haproxy: fix build error when RLIMIT_AS is not set
- BUG/MINOR: http_act: don't check capture id in backend (2)
- BUG/MINOR: mux-h1: Fix the splicing in TUNNEL mode
- BUG/MINOR: mux-h1: Don't read data from a pipe if the mux is unable to receive
- BUG/MINOR: mux-h1: Disable splicing only if input data was processed
- BUG/MEDIUM: mux-h1: Disable splicing for the conn-stream if read0 is received
- MINOR: mux-h1: Improve traces about the splicing
- BUG/MEDIUM: mux-h1: Subscribe rather than waking up in h1_rcv_buf()
- MINOR: connection: move the CO_FL_WAIT_ROOM cleanup to the reader only
- BUG/MEDIUM: connection: Continue to recv data to a pipe when the FD is not
  ready
- BUG/MINOR: backend: Remove CO_FL_SESS_IDLE if a client remains on the last
  server
- MINOR: http: Add support for http 413 status
- DOC: configuration: remove obsolete mentions of H2 being converted to HTTP/1.x
- BUG/MINOR: sample: Free str.area in smp_check_const_bool
- BUG/MINOR: sample: Free str.area in smp_check_const_meth
- BUG/MEDIUM: lists: add missing store barrier on MT_LIST_BEHEAD()
- BUG/MEDIUM: lists: add missing store barrier in MT_LIST_ADD/MT_LIST_ADDQ
- CONTRIB: da: fix memory leak in dummy function da_atlas_open()
- BUG/MEDIUM: mux-h1: Continue to process request when switching in tunnel mode
- BUG/MINOR: mux-fcgi: Handle empty STDERR record
- BUG/MINOR: mux-fcgi: Set conn state to RECORD_P when skipping the record
  padding
- BUG/MINOR: mux-fcgi: Set flags on the right stream field for empty FCGI_STDOUT
- BUG/MEDIUM: log: issue mixing sampled to not sampled log servers.
- BUG/MEDIUM: fcgi-app: fix memory leak in fcgi_flt_http_headers
- BUG/MEDIUM: server: resolve state file handle leak on reload
- BUG/MEDIUM: server: fix possibly uninitialized state file on close
- BUG/MEDIUM: channel: Be aware of SHUTW_NOW flag when output data are peeked
- BUILD: ebtree: fix build on libmusl after recent introduction of eb_memcmp()
- REGEST: Add reg tests about error files
- BUG/MINOR: threads: Don't forget to init each thread toremove_lock.
- MINOR: pools: increase MAX_BASE_POOLS to 64
- BUILD: thread: add parenthesis around values of locking macros
- BUG/MINOR: cfgparse: don't increment linenum on incomplete lines
- BUG/MEDIUM: resolve: fix init resolving for ring and peers section.
- BUG/MAJOR: dns: Make the do-resolve action thread-safe
- BUG/MEDIUM: dns: Release answer items when a DNS resolution is freed
- BUG/MINOR: mux-fcgi: Don't url-decode the QUERY_STRING parameter anymore
- BUG/MEDIUM: mux-h1: Wakeup the H1C in h1_rcv_buf() if more data are expected
- BUG/MEDIUM: mux-h1: Disable the splicing when nothing is received
- BUILD: tools: fix build with static only toolchains
- BUG/MINOR: debug: Don't dump the lua stack if it is not initialized
- MEDIUM: lua: Add support for the Lua 5.4
- BUG/MEDIUM: dns: Don't yield in do-resolve action on a final evaluation
- BUG/MINOR: tcp-rules: Set the inspect-delay when a tcp-response action yields
- MINOR: connection: Preinstall the mux for non-ssl connect
- MINOR: stream-int: Be sure to have a mux to do sends and receives
- SCRIPTS: announce-release: add the link to the wiki in the announce messages
- BUG/MEDIUM: backend: always attach the transport before installing the mux

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.7-0
- BUG/MAJOR: http-htx: Don't forget to copy error messages from defaults
  sections

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.6-0
- Revert "BUG/MEDIUM: connections: force connections cleanup on server changes"
- SCRIPTS: publish-release: pass -n to gzip to remove timestamp
- BUG/MINOR: peers: fix internal/network key type mapping.
- BUG/MEDIUM: lua: Reset analyse expiration timeout before executing
  a lua action
- BUG/MEDIUM: http-htx: Duplicate error messages as raw data instead of string
- BUG/MEDIUM: hlua: Lock pattern references to perform set/add/del operations
- BUG/MEDIUM: contrib/prometheus-exporter: Properly set flags to dump metrics
- BUG/MEDIUM: mworker: fix the copy of options in copy_argv()
- BUG/MINOR: init: -x can have a parameter starting with a dash
- BUG/MINOR: init: -S can have a parameter starting with a dash
- BUG/MEDIUM: mworker: fix the reload with an -- option
- BUG/MINOR: ssl: fix a trash buffer leak in some error cases
- BUG/MINOR: mworker: fix a memleak when execvp() failed

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.5-0
- BUG/MINOR: protocol_buffer: Wrong maximum shifting.
- MINOR: ssl: improve the errors when a crt can't be open
- BUG/MINOR: ssl/cli: memory leak in 'set ssl cert'
- BUG/MINOR: ssl: memleak of the struct cert_key_and_chain
- BUG/MINOR: connection: always send address-less LOCAL PROXY connections
- BUG/MINOR: peers: Incomplete peers sections should be validated.
- DOC: hashing: update link to hashing functions
- MINOR: version: Show uname output in display_version()
- DOC: Improve documentation on http-request set-src
- BUG/MINOR: ssl: default settings for ssl server options are not used
- BUG/MEDIUM: http-ana: Handle NTLM messages correctly.
- BUG/MINOR: tools: fix the i386 version of the div64_32 function
- BUG/MINOR: http: make url_decode() optionally convert '+' to SP
- DOC: option logasap does not depend on mode
- MEDIUM: memory: make pool_gc() run under thread isolation
- MINOR: contrib: make the peers wireshark dissector a plugin
- BUG/MINOR: check: Update server address and port to execute an external check
- MINOR: checks: Add a way to send custom headers and payload during http chekcs
- BUG/MINOR: checks: Respect the no-check-ssl option
- BUG/MEDIUM: server/checks: Init server check during config validity check
- BUG/MINOR: checks: chained expect will not properly wait for enough data
- BUG/MINOR: obj_type: Handle stream object in obj_base_ptr() function
- BUG/MINOR: mux-fcgi: Be sure to have a connection as session's origin
  to use it
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
- MINOR: haproxy: export run_poll_loop
- MINOR: tools: add new function dump_addr_and_bytes()
- MINOR: tools: add resolve_sym_name() to resolve function pointers
- MINOR: debug: use resolve_sym_name() to dump task handlers
- MINOR: cli: make "show fd" rely on resolve_sym_name()
- MEDIUM: debug: add support for dumping backtraces of stuck threads
- MINOR: debug: call backtrace() once upon startup
- BUILD: Makefile: include librt before libpthread
- MINOR: wdt: do not depend on USE_THREAD
- MINOR: debug: report the number of entries in the backtrace
- MINOR: debug: improve backtrace() on aarch64 and possibly other systems
- MINOR: debug: use our own backtrace function on clang+x86_64
- MINOR: debug: dump the whole trace if we can't spot the starting point
- BUILD: tools: unbreak resolve_sym_name() on non-GNU platforms
- BUILD: tools: rely on __ELF__ not USE_DL to enable use of dladdr()
- BUILD: Makefile: add linux-musl to TARGET
- REGTEST: ssl: test the client certificate authentication
- REGTEST: http-rules: Require PCRE or PCRE2 option to run map_redirect script
- Revert "BUG/MINOR: connection: always send address-less LOCAL PROXY
  connections"
- Revert "BUG/MINOR: connection: make sure to correctly tag local PROXY
  connections"
- BUG/MINOR: checks/server: use_ssl member must be signed
- BUG/MINOR: checks: Compute the right HTTP request length for HTTP health
  checks
- BUG/MINOR: checks: Remove a warning about http health checks
- BUG/MEDIUM: mux_fcgi: Free the FCGI connection at the end of fcgi_release()
- BUG/MEDIUM: mux-fcgi: Fix wrong test on FCGI_CF_KEEP_CONN in fcgi_detach()
- BUG/MEDIUM: connections: force connections cleanup on server changes
- BUG/MEDIUM: h1: Don't compare host and authority if only h1 headers are parsed
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
- BUG/MEDIUM: streams: Remove SF_ADDR_SET if we're retrying due to L7 retry.
- BUG/MEDIUM: stream: Only allow L7 retries when using HTTP.
- BUG/MINOR: cache: Don't needlessly test "cache" keyword in parse_cache_flt()
- BUG/MAJOR: mux-fcgi: Stop sending loop if FCGI stream is blocked for
  any reason
- BUG/MEDIUM: ring: write-lock the ring while attaching/detaching
- BUG/MINOR: checks: Respect check-ssl param when a port or an addr is specified
- BUG/MINOR: server: Fix server_finalize_init() to avoid unused variable
- DOC: retry-on can only be used with mode http
- DOC/MINOR: halog: Add long help info for ic flag
- DOC: SPOE is no longer experimental
- BUG/MINOR: logs: prevent double line returns in some events.
- REGTESTS: checks: Fix tls_health_checks when IPv6 addresses are used
- BUG/MEDIUM: logs: fix trailing zeros on log message.
- BUG/MINOR: lua: Add missing string length for lua sticktable lookup
- BUG/MINOR: nameservers: fix error handling in parsing of resolv.conf

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.4-0
- SCRIPTS: make announce-release executable again
- BUG/MINOR: namespace: avoid closing fd when socket failed in my_socketat
- BUG/MEDIUM: muxes: Use the right argument when calling the destroy method.
- BUG/MINOR: mux-fcgi: Forbid special characters when matching PATH_INFO param
- MINOR: mux-fcgi: Make the capture of the path-info optional in pathinfo regex
- SCRIPTS: announce-release: use mutt -H instead of -i to include the draft
- MINOR: http-htx: Add a function to retrieve the headers size of an HTX message
- MINOR: filters: Forward data only if the last filter forwards something
- BUG/MINOR: filters: Count HTTP headers as filtered data but don't forward them
- BUG/MINOR: http-htx: Don't return error if authority is updated without
  changes
- BUG/MINOR: http-ana: Matching on monitor-uri should be case-sensitive
- MINOR: http-ana: Match on the path if the monitor-uri starts by a /
- BUG/MAJOR: http-ana: Always abort the request when a tarpit is triggered
- MINOR: ist: add an iststop() function
- BUG/MINOR: http: http-request replace-path duplicates the query string
- BUG/MEDIUM: shctx: make sure to keep all blocks aligned
- MINOR: compiler: move CPU capabilities definition from config.h and
  complete them
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
- BUG/MINOR: h2: reject again empty :path pseudo-headers
- BUG/MINOR: sample: Make sure to return stable IDs in the unique-id fetch
- BUG/MINOR: dns: ignore trailing dot
- BUG/MINOR: http-htx: Do case-insensive comparisons on Host header name
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
- BUG/MEDIUM: debug: make the debug_handler check for the thread in
  threads_to_dump
- MINOR: haproxy: export main to ease access from debugger
- BUILD: tools: remove obsolete and conflicting trace() from standard.c
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
- BUG/MINOR: filters: Use filter offset to decude the amount of forwarded data
- BUG/MINOR: filters: Forward everything if no data filters are called
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
- DOC: assorted typo fixes in the documentation
- DOC: ssl: clarify security implications of TLS tickets
- BUILD: wdt: only test for SI_TKILL when compiled with thread support
- BUG/MEDIUM: mt_lists: Make sure we set the deleted element to NULL;
- MINOR: mt_lists: Appease gcc.
- BUG/MEDIUM: random: align the state on 2*64 bits for ARM64
- BUG/MEDIUM: pools: Always update free_list in pool_gc().
- BUG/MINOR: haproxy: always initialize sleeping_thread_mask
- BUG/MINOR: listener/mq: do not dispatch connections to remote threads when
  stopping
- BUG/MINOR: haproxy/threads: try to make all threads leave together
- DOC: proxy_protocol: Reserve TLV type 0x05 as PP2_TYPE_UNIQUE_ID
- DOC: correct typo in alert message about rspirep
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
- BUG/MINOR: http-ana: Reset request analysers on error when waiting for
  response
- BUG/CRITICAL: hpack: never index a header into the headroom after wrapping

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
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
- BUG/MINOR: stream-int: Don't trigger L7 retry if max retries
  is already reached
- BUG/MEDIUM: tasks: Use the MT macros in tasklet_free().
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
- BUG/MINOR: ssl: ssl_sock_load_ocsp_response_from_file memory leak
- BUG/MINOR: ssl: ssl_sock_load_issuer_file_into_ckch memory leak
- BUG/MINOR: ssl: ssl_sock_load_sctl_from_file memory leak
- MINOR: proxy/http-ana: Add support of extra attributes for
  the cookie directive
- BUG/MINOR: http_act: don't check capture id in backend
- BUG/MEDIUM: netscaler: Don't forget to allocate storage for conn->src/dst.
- BUG/MINOR: ssl: ssl_sock_load_pem_into_ckch is not consistent
- BUG/MINOR: ssl/cli: free the previous ckch content once a PEM is loaded
- CLEANUP: stats: shut up a wrong null-deref warning from gcc 9.2
- BUG/MINOR: ssl: increment issuer refcount if in chain
- BUG/MINOR: ssl: memory leak w/ the ocsp_issuer
- BUG/MINOR: ssl: typo in previous patch
- BUG/MINOR: ssl/cli: ocsp_issuer must be set w/ "set ssl cert"
- BUG/MEDIUM: 0rtt: Only consider the SSL handshake.
- BUG/MINOR: stktable: report the current proxy name in error messages
- BUG/MEDIUM: mux-h2: make sure we don't emit TE headers with anything
  but "trailers"
- BUILD: cfgparse: silence a bogus gcc warning on 32-bit machines
- MINOR: lua: Add hlua_prepend_path function
- MINOR: lua: Add lua-prepend-path configuration option
- MINOR: lua: Add HLUA_PREPEND_C?PATH build option
- BUG/MEDIUM: ssl: Don't forget to free ctx->ssl on failure.
- BUG/MINOR: tcpchecks: fix the connect() flags regarding delayed ack
- BUG/MEDIUM: pipe: fix a use-after-free in case of pipe creation error
- BUG/MINOR: ssl: Possible memleak when allowing the 0RTT data buffer.
- BUG/MINOR: connection: fix ip6 dst_port copy in make_proxy_line_v2
- BUG/MEDIUM: connections: Don't forget to unlock when killing a connection.
- BUG/MEDIUM: memory_pool: Update the seq number in pool_flush().
- MINOR: memory: Only init the pool spinlock once.
- BUG/MEDIUM: memory: Add a rwlock before freeing memory.
- BUG/MAJOR: memory: Don't forget to unlock the rwlock if the pool is empty.
- BUG/MINOR: ssl: we may only ignore the first 64 errors
- BUG/MINOR: ssl: clear the SSL errors on DH loading failure
- CONTRIB: debug: add missing flags SF_HTX and SF_MUX
- CONTRIB: debug: add the possibility to decode the value as certain types only
- CONTRIB: debug: support reporting multiple values at once
- MINOR: acl: Warn when an ACL is named 'or'
- CONTRIB: debug: also support reading values from stdin
- SCRIPTS: announce-release: place the send command in the mail's header
- SCRIPTS: announce-release: allow the user to force to overwrite old files
- BUG/MEDIUM: ssl/cli: 'commit ssl cert' wrong SSL_CTX init
- DOC: schematic of the SSL certificates architecture
- BUG/MINOR: unix: better catch situations where the unix socket path length
  is close to the limit
- BUG/MINOR: dns: allow 63 char in hostname
- BUG/MEDIUM: listener: only consider running threads when resuming listeners
- BUG/MINOR: listener: enforce all_threads_mask on bind_thread on init
- BUG/MINOR: tcp: avoid closing fd when socket failed in tcp_bind_listener
- MINOR: build: add aix72-gcc build TARGET and power{8,9} CPUs
- DOC: word converter ignores delimiters at the start or end of input string
- MINOR: htx: Add a function to append an HTX message to another one
- MINOR: htx/channel: Add a function to copy an HTX message in
  a channel's buffer
- BUG/MINOR: http-ana: Don't overwrite outgoing data when an error is reported
- BUG/MINOR: http-ana: Set HTX_FL_PROXY_RESP flag if a server perform a redirect
- BUG/MINOR: tcp: don't try to set defaultmss when value is negative

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.1.2-0
- DOC: clarify the fact that replace-uri works on a full URI
- BUG/MINOR: sample: fix the closing bracket and LF in the debug converter
- BUG/MINOR: sample: always check converters' arguments
- MINOR: sample: Validate the number of bits for the sha2 converter
- BUG/MEDIUM: ssl: Don't set the max early data we can receive too early.
- MINOR: debug: support logging to various sinks
- MINOR: http: add a new "replace-path" action
- MINOR: task: only check TASK_WOKEN_ANY to decide to requeue a task
- BUG/MAJOR: task: add a new TASK_SHARED_WQ flag to fix foreing requeuing
- BUG/MEDIUM: ssl: Revamp the way early data are handled.
- MINOR: fd/threads: make _GET_NEXT()/_GET_PREV() use the volatile attribute
- BUG/MEDIUM: fd/threads: fix a concurrency issue between add and rm on
  the same fd
- BUG/MINOR: ssl: openssl-compat: Fix getm_ defines
- BUG/MEDIUM: state-file: do not allocate a full buffer for each server entry
- BUG/MINOR: state-file: do not store duplicates in the global tree
- BUG/MINOR: state-file: do not leak memory on parse errors
- BUG/MEDIUM: stream: Be sure to never assign a TCP backend to an HTX stream
- BUILD: ssl: improve SSL_CTX_set_ecdh_auto compatibility

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- BUG/MINOR: contrib/prometheus-exporter: decode parameter and value only
- BUG/MINOR: h1: Don't test the host header during response parsing
- BUILD/MINOR: trace: fix use of long type in a few printf format strings
- BUG/MINOR: http-htx: Don't make http_find_header() fail if the value is empty
- DOC: ssl/cli: set/commit/abort ssl cert
- BUG/MINOR: ssl: fix SSL_CTX_set1_chain compatibility for openssl < 1.0.2
- BUG/MINOR: fcgi-app: Make the directive pass-header case insensitive
- BUG/MINOR: stats: Fix HTML output for the frontends heading
- BUG/MINOR: ssl/cli: 'ssl cert' cmd only usable w/ admin rights
- DOC: Clarify behavior of server maxconn in HTTP mode
- DOC: clarify matching strings on binary fetches
- DOC: Fix ordered list in summary
- DOC: move the "group" keyword at the right place
- BUG/MEDIUM: stream-int: don't subscribed for recv when we're trying to
  flush data
- BUG/MINOR: stream-int: avoid calling rcv_buf() when splicing is still possible
- BUG/MINOR: ssl/cli: don't overwrite the filters variable
- BUG/MEDIUM: listener/thread: fix a race when pausing a listener
- BUG/MINOR: ssl: certificate choice can be unexpected with openssl >= 1.1.1
- BUG/MEDIUM: mux-h1: Never reuse H1 connection if a shutw is pending
- BUG/MINOR: mux-h1: Don't rely on CO_FL_SOCK_RD_SH to set H1C_F_CS_SHUTDOWN
- BUG/MINOR: mux-h1: Fix conditions to know whether or not we may receive data
- BUG/MEDIUM: tasks: Make sure we switch wait queues in task_set_affinity().
- BUG/MEDIUM: checks: Make sure we set the task affinity just before connecting.
- BUG/MINOR: mux-h1: Be sure to set CS_FL_WANT_ROOM when EOM can't be added
- BUG/MEDIUM: mux-fcgi: Handle cases where the HTX EOM block cannot be inserted
- BUG/MINOR: proxy: make soft_stop() also close FDs in LI_PAUSED state
- BUG/MINOR: listener/threads: always use atomic ops to clear the FD events
- BUG/MINOR: listener: also clear the error flag on a paused listener
- BUG/MEDIUM: listener/threads: fix a remaining race in the listener's accept()
- DOC: document the listener state transitions
- BUG/MEDIUM: kqueue: Make sure we report read events even when no data.
- BUG/MAJOR: dns: add minimalist error processing on the Rx path
- BUG/MEDIUM: proto_udp/threads: recv() and send() must not be exclusive.
- DOC: listeners: add a few missing transitions
- BUG/MINOR: tasks: only requeue a task if it was already in the queue
- DOC: proxies: HAProxy only supports 3 connection modes
- DOC: remove references to the outdated architecture.txt
- BUG/MINOR: log: fix minor resource leaks on logformat error path
- BUG/MINOR: mworker: properly pass SIGTTOU/SIGTTIN to workers
- BUG/MINOR: listener: do not immediately resume on transient error
- BUG/MINOR: server: make "agent-addr" work on default-server line
- BUG/MINOR: listener: fix off-by-one in state name check
- BUILD/MINOR: unix sockets: silence an absurd gcc warning about strncpy()

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- Initial build for kaos repository
