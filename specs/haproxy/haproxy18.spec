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
%define major_ver         18

%define hp_user           %{orig_name}
%define hp_user_id        188
%define hp_group          %{orig_name}
%define hp_group_id       188
%define hp_homedir        %{_localstatedir}/lib/%{orig_name}
%define hp_confdir        %{_sysconfdir}/%{orig_name}
%define hp_datadir        %{_datadir}/%{orig_name}

%define lua_ver           5.3.6
%define pcre_ver          8.45
%define openssl_ver       1.1.1k
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              %{orig_name}%{major_ver}
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.8.30
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/1.8/src/%{orig_name}-%{version}.tar.gz
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
* Thu Jun 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.30-0
- MINOR: time: also provide a global, monotonic global_now_ms timer
- BUG/MEDIUM: freq_ctr/threads: use the global_now_ms variable
- BUG/MEDIUM: time: make sure to always initialize the global tick
- MINOR: tools: make url2ipv4 return the exact number of bytes parsed
- BUG/MINOR: http_fetch: make hdr_ip() reject trailing characters
- BUG/MINOR: tcp: fix silent-drop workaround for IPv6
- BUILD: tcp: use IPPROTO_IPV6 instead of SOL_IPV6 on FreeBSD/MacOS
- BUG/MINOR: http_fetch: make hdr_ip() resistant to empty fields

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.29-0
- BUG/MINOR: sample: Memory leak of sample_expr structure in case of error
- BUILD/MINOR: lua: define _GNU_SOURCE for LLONG_MAX
- BUG/MINOR: config: fix leak on proxy.conn_src.bind_hdr_name
- DOC: management: fix "show resolvers" alphabetical ordering
- BUG/MINOR: stick-table: Always call smp_fetch_src() with a valid arg list
- BUG/MINOR: xxhash: make sure armv6 uses memcpy()
- CLEANUP: remove unused src/cfgparse-listen.c
- BUG/MINOR: server: re-align state file fields number
- BUG/MINOR: server: Fix server-state-file-name directive
- CLEANUP: deinit: release global and per-proxy server-state variables on deinit
- BUG/MEDIUM: config: don't pick unset values from last defaults section
- BUG/MINOR: server: Don't call fopen() with server-state filepath set to NULL
- CLEANUP: channel: fix comment in ci_putblk.
- BUG/MINOR: server: Remove RMAINT from admin state when loading server state
- BUG/MINOR: session: atomically increment the tracked sessions counter
- BUG/MINOR: checks: properly handle wrapping time in __health_adjust()
- BUG/MINOR: sample: Always consider zero size string samples as unsafe
- BUG/MINOR: server: Init params before parsing a new server-state line
- BUG/MINOR: server: Be sure to cut the last parsed field of a server-state line
- BUG/MEDIUM: proxy: use thread-safe stream killing on hard-stop
- BUG/MEDIUM: cli/shutdown sessions: make it thread-safe
- BUG/MINOR: http-ana: Only consider dst address to process originalto option
- BUG/MINOR: tcp-act: Don't forget to set the original port for
  IPv4 set-dst rule
- BUG/MINOR: connection: Use the client's dst family for adressless servers
- BUG/MEDIUM: spoe: Kill applets if there are pending connections and
  nbthread > 1
- BUG/MAJOR: spoe: Be sure to remove all references on a released spoe applet
- BUG/MEDIUM: spoe: Explicitly wakeup SPOE stream if waiting for more data
- DOC: spoe: Add a note about fragmentation support in HAProxy
- BUG/MEDIUM: dns: Consider the fact that dns answers are case-insensitive
- BUG/MINOR: hlua: Don't strip last non-LWS char in hlua_pushstrippedstring()
- BUG/MINOR: ssl: don't truncate the file descriptor to 16 bits in debug mode
- BUG/MEDIUM: session: NULL dereference possible when accessing the listener
- BUG/MEDIUM: filters: Set CF_FL_ANALYZE on channels when filters are attached
- BUG/MINOR: proxy/session: Be sure to have a listener to increment its counters
- CLEANUP: tcp-rules: add missing actions in the tcp-request error message
- BUG/MINOR: resolvers: Consider server to have no IP on DNS resolution error
- BUG/MINOR: resolvers: Add missing case-insensitive comparisons
  of DNS hostnames
- MINOR: time: export the global_now variable
- OPTIM: freq-ctr: don't take the date lock for most updates
- BUG/MINOR: freq_ctr/threads: make use of the last updated global time

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.28-0
- BUG/MINOR: config: copy extra cookie attributes from dfl proxy
- BUG/MINOR: http-fetch: Extract cookie value even when no cookie name
- BUG/MINOR: http-fetch: Fix calls w/o parentheses of the cookie sample fetches
- MINOR: spoe: Don't close connection in sync mode on processing timeout
- DOC: config: Move req.hdrs and req.hdrs_bin in L7 samples fetches section
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
- DOC: email change of the DeviceAtlas maintainer
- BUG/MINOR: tools: make parse_time_err() more strict on the timer validity
- BUG/MINOR: tools: Reject size format not starting by a digit
- BUG/MEDIUM: lb-leastconn: Reposition a server using the right eweight
- CLEANUP: lua: Remove declaration of an inexistant function
- CLEANUP: stream: remove an obsolete debugging test
- BUG/MEDIUM: mworker: fix again copy_argv()
- BUILD: Makefile: have "make clean" destroy .o/.a/.s in contrib subdirs as well
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
- DOC: fix some spelling issues over multiple files
- SCRIPTS: announce-release: fix typo in help message

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.27-0
- BUG/MINOR: dns: ignore trailing dot
- BUG/MEDIUM: mux-h2: Don't fail if nothing is parsed for a legacy chunk
  response
- BUG/MEDIUM: map/lua: Return an error if a map is loaded during runtime
- BUG/MINOR: lua: Check argument type to convert it to IPv4/IPv6 arg validation
- BUG/MINOR: lua: Check argument type to convert it to IP mask in arg validation
- BUG/MINOR: stats: use strncmp() instead of memcmp() on health states
- BUG/MINOR: reload: do not fail when no socket is sent
- BUG/MINOR: startup: haproxy -s cause 100% cpu
- BUG/MEDIUM: ssl: check OCSP calloc in ssl_sock_load_ocsp()
- BUG/MINOR: threads: work around a libgcc_s issue with chrooting
- BUILD: thread: limit the libgcc_s workaround to glibc only
- MINOR: Commit .gitattributes
- CLEANUP: Update .gitignore
- BUILD: threads: better workaround for late loading of libgcc_s
- BUG/MEDIUM: pattern: Renew the pattern expression revision when it is pruned
- BUG/MEDIUM: pattern: fix memory leak in regex pattern functions
- BUG/MEDIUM: ssl: does not look for all SNIs before chosing a certificate
- BUG/MINOR: ssl: verifyhost is case sensitive
- BUG/MEDIUM: h2: report frame bits only for handled types
- BUG/MINOR: config: Fix memory leak on config parse listen
- BUG/MEDIUM: listeners: do not pause foreign listeners
- DOC: agent-check: fix typo in "fail" word expected reply
- REGTESTS: add a few load balancing tests
- REGTEST: fix host part in balance-uri-path-only.vtc
- REGTEST: make abns_socket.vtc require 1.8
- REGTEST: make map_regm_with_backref require 1.7
- DOC: ssl: crt-list negative filters are only a hint
- MINOR: counters: fix a typo in comment
- BUG/MINOR: stats: fix validity of the json schema
- MINOR: hlua: Display debug messages on stderr only in debug mode
- BUG/MEDIUM: spoe: Unset variable instead of set it if no data provided
- BUG/MEDIUM: lb: Always lock the server when calling server_{take,drop}_conn
- BUG/MINOR: queue: properly report redistributed connections
- BUG/MEDIUM: server: support changing the slowstart value from state-file
- BUG/MAJOR: mux-h2: Don't try to send data if we know it is no longer possible
- BUG/MINOR: extcheck: add missing checks on extchk_setenv()
- BUG/MINOR: server: fix srv downtime calcul on starting
- BUG/MINOR: server: fix down_time report for stats
- BUG/MINOR: lua: initialize sample before using it
- BUG/MINOR: cache: Inverted variables in http_calc_maxage function
- BUG/MEDIUM: filters: Don't try to init filters for disabled proxies
- BUG/MINOR: server: Set server without addr but with dns in RMAINT on startup
- MINOR: server: Copy configuration file and line for server templates
- BUG/MINOR: filters: Skip disabled proxies during startup only

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.26-0
- BUILD: chunk: properly declare pool_head_trash as extern
- BUILD: cache: avoid a build warning with some compilers/linkers
- BUG/MINOR: ssl: default settings for ssl server options are not used
- BUG/MINOR: tools: fix the i386 version of the div64_32 function
- DOC: option logasap does not depend on mode
- BUG/MINOR: check: Update server address and port to execute an external check
- BUG/MINOR: checks: Respect the no-check-ssl option
- BUG/MINOR: checks/server: use_ssl member must be signed
- BUG/MINOR: checks: chained expect will not properly wait for enough data
- BUG/MEDIUM: capture: capture-req/capture-res converters crash without a stream
- BUG/MEDIUM: capture: capture.{req,res}.* crash without a stream
- BUG/MEDIUM: http: the "http_first_req" sample fetch could crash without
  a steeam
- BUG/MEDIUM: http: the "unique-id" sample fetch could crash without a steeam
- BUG/MEDIUM: shctx: really check the lock's value while waiting
- BUG/MEDIUM: shctx: bound the number of loops that can happen around the lock
- REGTEST: ssl: test the client certificate authentication
- BUG/MINOR: sample: Set the correct type when a binary is converted to a string
- BUG/MINOR: config: Make use_backend and use-server post-parsing less obscur
- BUG/MEDIUM: http_ana: make the detection of NTLM variants safer
- BUG/MINOR: cfgparse: Abort parsing the current line if an invalid \x sequence
  is encountered
- BUG/MINOR: pollers: remove uneeded free in global init
- BUILD: select: only declare existing local labels to appease clang
- SCRIPTS: publish-release: pass -n to gzip to remove timestamp
- BUG/MINOR: peers: fix internal/network key type mapping.
- BUG/MEDIUM: lua: Reset analyse expiration timeout before executing
  a lua action
- BUG/MEDIUM: hlua: Lock pattern references to perform set/add/del operations
- BUG/MINOR: logs: prevent double line returns in some events.
- BUG/MEDIUM: logs: fix trailing zeros on log message.
- BUG/MINOR: proto-http: Fix detection of NTLM for the legacy HTTP version
- BUG/MEDIUM: mworker: fix the copy of options in copy_argv()
- BUG/MINOR: init: -x can have a parameter starting with a dash
- BUG/MEDIUM: mworker: fix the reload with an -- option
- BUG/MINOR: mworker: fix a memleak when execvp() failed
- BUG/MEDIUM: pattern: fix thread safety of pattern matching
- BUG/MINOR: ssl: fix ssl-{min,max}-ver with openssl < 1.1.0
- BUG/MINOR: tcp-rules: tcp-response must check the buffer's fullness
- BUG/MEDIUM: ebtree: use a byte-per-byte memcmp() to compare memory blocks
- BUG/MINOR: spoe: add missing key length check before checking key names
- BUG/MINOR: systemd: Wait for network to be online
- BUG/MINOR: spoe: correction of setting bits for analyzer
- BUG/MEDIUM: fetch: Fix hdr_ip misparsing IPv4 addresses due to missing NUL
- MINOR: cli: make "show sess" stop at the last known session
- DOC: ssl: add "allow-0rtt" and "ciphersuites" in crt-list
- BUG/MEDIUM: pattern: Add a trailing \0 to match strings only if possible
- BUG/MINOR: proxy: fix dump_server_state()'s misuse of the trash
- BUG/MINOR: proxy: always initialize the trash in show servers state
- BUG/MINOR: http_act: don't check capture id in backend (2)
- BUG/MINOR: sample: Free str.area in smp_check_const_bool
- BUG/MINOR: sample: Free str.area in smp_check_const_meth
- BUG/MEDIUM: channel: Be aware of SHUTW_NOW flag when output data are peeked
- BUILD: ebtree: fix build on libmusl after recent introduction of eb_memcmp()
- BUG/MINOR: cfgparse: don't increment linenum on incomplete lines
- BUG/MEDIUM: mux-h2: Emit an error if the response chunk formatting
  is incomplete
- BUG/MEDIUM: dns: Release answer items when a DNS resolution is freed
- BUG/MINOR: tcp-rules: Set the inspect-delay when a tcp-response action yields
- SCRIPTS: announce-release: add the link to the wiki in the announce messages
- SCRIPTS: git-show-backports: make -m most only show the left branch
- SCRIPTS: git-show-backports: emit the shell command to backport a commit
- DOC: Improve documentation on http-request set-src
- BUG/MINOR: http: make url_decode() optionally convert '+' to SP
- MINOR: checks: Add a way to send custom headers and payload during http checks
- BUG/MINOR: checks: Compute the right HTTP request length for HTTP
  health checks
- BUG/MINOR: checks: Remove a warning about http health checks
- BUG/MINOR: threads: fix multiple use of argument inside HA_ATOMIC_CAS()
- BUG/MINOR: threads: fix multiple use of argument inside
  HA_ATOMIC_UPDATE_{MIN,MAX}()
- BUG/MINOR: pools: use %%u not %%d to report pool stats in "show pools"
- MEDIUM: map: make the "clear map" operation yield
- BUG/MEDIUM: server/checks: Init server check during config validity check
- BUG/MEDIUM: checks: Always initialize checks before starting them
- BUG/MINOR: checks: Respect check-ssl param when a port or an addr is specified
- BUG/MINOR: server: Fix server_finalize_init() to avoid unused variable

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.25-0
- BUG/MINOR: namespace: avoid closing fd when socket failed in my_socketat
- SCRIPTS: announce-release: use mutt -H instead of -i to include the draft
- CONTRIB: debug: add the possibility to decode the value as certain types only
- CONTRIB: debug: support reporting multiple values at once
- CONTRIB: debug: also support reading values from stdin
- BUG/MEDIUM: shctx: make sure to keep all blocks aligned
- MINOR: compiler: move CPU capabilities definition from config.h and complete
  them
- BUG/MEDIUM: ebtree: don't set attribute packed without unaligned access
  support
- BUILD: fix recent build failure on unaligned archs
- MINOR: compiler: add new alignment macros
- BUILD: ebtree: improve architecture-specific alignment
- BUG/MINOR: sample: fix the json converter's endian-sensitivity
- BUG/MINOR: sample: Make sure to return stable IDs in the unique-id fetch
- BUG/MAJOR: list: fix invalid element address calculation
- DOC: fix incorrect indentation of http_auth_*
- BUG/MAJOR: proxy_protocol: Properly validate TLV lengths
- REGTEST: make the PROXY TLV validation depend on version 2.2
- BUG/MINOR: lua: Ignore the reserve to know if a channel is full or not
- BUG/MINOR: http-rules: Preserve FLT_END analyzers on reject action
- BUG/MINOR: http-rules: Fix a typo in the reject action function
- BUG/MINOR: rules: Preserve FLT_END analyzers on silent-drop action
- BUG/MINOR: rules: Increment be_counters if backend is assigned for a
  silent-drop
- DOC: fix typo about no-tls-tickets
- DOC: improve description of no-tls-tickets
- DOC: ssl: clarify security implications of TLS tickets
- DOC: proxy_protocol: Reserve TLV type 0x05 as PP2_TYPE_UNIQUE_ID
- DOC: assorted typo fixes in the documentation
- BUG/MINOR: peers: init bind_proc to 1 if it wasn't initialized
- BUG/MINOR: peers: avoid an infinite loop with peers_fe is NULL
- BUG/MINOR: stats: Fix color of draining servers on stats page
- DOC: internals: Fix spelling errors in filters.txt
- BUG/MEDIUM: http: unbreak redirects in legacy mode
- MINOR: http-rules: Add a flag on redirect rules to know the rule direction
- BUG/MINOR: http_ana: make sure redirect flags don't have overlapping bits
- MINOR: http-rules: Handle the rule direction when a redirect is evaluated
- BUG/MINOR: http-ana: Reset request analysers on error when waiting for
  response
- BUG/CRITICAL: hpack: never index a header into the headroom after wrapping

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.24-0
- DOC: clarify matching strings on binary fetches
- BUG/MEDIUM: listener/thread: fix a race when pausing a listener
- BUG/MINOR: ssl: certificate choice can be unexpected with openssl >= 1.1.1
- BUG/MINOR: proxy: make soft_stop() also close FDs in LI_PAUSED state
- BUG/MINOR: listener/threads: always use atomic ops to clear the FD events
- BUG/MINOR: listener: also clear the error flag on a paused listener
- BUG/MEDIUM: listener/threads: fix a remaining race in the listener's accept()
- DOC: document the listener state transitions
- BUG/MAJOR: dns: add minimalist error processing on the Rx path
- BUG/MEDIUM: proto_udp/threads: recv() and send() must not be exclusive.
- BUG/MEDIUM: kqueue: Make sure we report read events even when no data.
- DOC: listeners: add a few missing transitions
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
- BUG/MINOR: sample: fix the closing bracket and LF in the debug converter
- BUG/MINOR: sample: always check converters' arguments
- BUG/MEDIUM: ssl: Don't set the max early data we can receive too early.
- BUG/MEDIUM: session: do not report a failure when rejecting a session
- BUG/MEDIUM: mworker: remain in mworker mode during reload
- BUG/MAJOR: hashes: fix the signedness of the hash inputs
- BUG/MEDIUM: cli: _getsocks must send the peers sockets
- BUG/MINOR: stream: don't mistake match rules for store-request rules
- BUG/MINOR: pattern: handle errors from fgets when trying to load patterns
- BUG/MINOR: dns: Make dns_query_id_seed unsigned
- BUG/MINOR: http-rules: Remove buggy deinit functions for HTTP rules
- BUG/MINOR: stick-table: Use MAX_SESS_STKCTR as the max track ID during parsing
- BUG/MINOR: tcp-rules: Fix memory releases on error path during action parsing
- MINOR: proxy/http-ana: Add support of extra attributes for the cookie
  directive
- BUG/MINOR: http_act: don't check capture id in backend
- BUG/MINOR: dns: allow srv record weight set to 0
- BUG/MEDIUM: pipe: fix a use-after-free in case of pipe creation error
- BUG/MINOR: connection: fix ip6 dst_port copy in make_proxy_line_v2
- MINOR: acl: Warn when an ACL is named 'or'
- SCRIPTS: announce-release: place the send command in the mail's header
- SCRIPTS: announce-release: allow the user to force to overwrite old files
- BUG/MINOR: unix: better catch situations where the unix socket path length is
  close to the limit
- BUG/MINOR: dns: allow 63 char in hostname
- BUG/MEDIUM: listener: only consider running threads when resuming listeners
- BUG/MINOR: tcp: avoid closing fd when socket failed in tcp_bind_listener
- BUG/MINOR: tcp: don't try to set defaultmss when value is negative
- SCRIPTS: make announce-release executable again

* Wed Feb 05 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.23-0
- MINOR: tcp: avoid confusion in time parsing init
- BUG/MINOR: cli: don't call the kw->io_release if kw->parse failed
- BUG/MINOR: config: Update cookie domain warn to RFC6265
- BUG/MEDIUM: stream: Be sure to support splicing at the mux level to enable it
- BUG/MEDIUM: stream: Be sure to release allocated captures for TCP streams
- BUG: dns: timeout resolve not applied for valid resolutions
- BUG/MEDIUM: listeners: always pause a listener on out-of-resource condition
- BUG/MINOR: ssl: fix crt-list neg filter for openssl < 1.1.1
- BUILD/MINOR: ssl: fix compiler warning about useless statement
- MINOR: ist: add ist_find_ctl()
- BUG/MAJOR: h2: reject header values containing invalid chars
- BUG/MAJOR: h2: make header field name filtering stronger
- SCRIPTS: create-release: show the correct origin name in suggested commands
- SCRIPTS: git-show-backports: add "-s" to proposed cherry-pick commands

* Tue Feb 04 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.22-0
- BUILD/MINOR: stream: avoid a build warning with threads disabled
- BUG/MINOR: haproxy: fix rule->file memory leak
- MINOR: connection: add new function conn_is_back()
- BUG/MEDIUM: ssl: Use the early_data API the right way.
- BUG/MEDIUM: checks: make sure the warmup task takes the server lock
- BUG/MINOR: logs/threads: properly split the log area upon startup
- MINOR: doc: Document allow-0rtt on the server line.
- BUG/MEDIUM: spoe: Be sure the sample is found before setting its context
- DOC: fixed typo in management.txt
- BUG/MINOR: mworker: disable SIGPROF on re-exec
- BUG/MEDIUM: listener/threads: fix an AB/BA locking issue in delete_listener()
- BUG/MEDIUM: proto-http: Always start the parsing if there is no outgoing data
- BUG/MEDIUM: http: also reject messages where "chunked" is missing from
  transfer-enoding
- BUG/MINOR: filters: Properly set the HTTP status code on analysis error
- BUG/MINOR: acl: Fix memory leaks when an ACL expression is parsed
- BUG/MEDIUM: check/threads: make external checks run exclusively on thread 1
- BUG/MEDIUM: namespace: close open namespaces during soft shutdown
- BUG/MAJOR: mux_h2: Don't consume more payload than received for skipped frames
- MINOR: tools: implement my_flsl()
- BUG/MEDIUM: spoe: Use a different engine-id per process
- DOC: Fix documentation about the cli command to get resolver stats
- BUG/MEDIUM: namespace: fix fd leak in master-worker mode
- BUG/MINOR: lua: Properly initialize the buffer's fields for string samples
  in hlua_lua2(smp|arg)
- BUG/MEDIUM: cache: make sure not to cache requests with absolute-uri
- DOC: clarify some points around http-send-name-header's behavior
- MINOR: stats: mention in the help message support for "json" and "typed"
- BUG/MINOR: ssl: free the sni_keytype nodes
- BUG/MINOR: chunk: Fix tests on the chunk size in functions copying data
- BUG/MINOR: WURFL: fix send_log() function arguments
- BUG/MINOR: tcp: Don't alter counters returned by tcp info fetchers
- BUG/MINOR: ssl: abort on sni allocation failure
- BUG/MINOR: ssl: abort on sni_keytypes allocation failure
- CLEANUP: ssl: make ssl_sock_load_cert*() return real error codes
- CLEANUP: ssl: make ssl_sock_put_ckch_into_ctx handle errcode/warn
- CLEANUP: ssl: make ssl_sock_load_dh_params handle errcode/warn
- CLEANUP: bind: handle warning label on bind keywords parsing.
- BUG/MEDIUM: ssl: 'tune.ssl.default-dh-param' value ignored with
  openssl > 1.1.1
- BUG/MINOR: mworker/ssl: close OpenSSL FDs on reload
- BUILD: ssl: fix again a libressl build failure after the openssl FD leak fix
- BUG/MINOR: mworker/ssl: close openssl FDs unconditionally
- BUG/MINOR: ssl: Fix fd leak on error path when a TLS ticket keys file
  is parsed
- BUG/MINOR: stick-table: Never exceed (MAX_SESS_STKCTR-1) when fetching
  a stkctr
- BUG/MINOR: sample: Make the `field` converter compatible with `-m found`
- BUG/MINOR: ssl: fix memcpy overlap without consequences.
- BUG/MINOR: stick-table: fix an incorrect 32 to 64 bit key conversion
- BUG/MEDIUM: pattern: make the pattern LRU cache thread-local and lockless

* Thu Oct 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.21-0
- BUG/MINOR: http: Call stream_inc_be_http_req_ctr() only one time per request
- BUG/MEDIUM: spoe: arg len encoded in previous frag frame but len changed
- MINOR: spoe: Use the sample context to pass frag_ctx info during encoding
- DOC: contrib/modsecurity: Typos and fix the reject example
- BUG/MEDIUM: contrib/modsecurity: If host header is NULL, don't try to strdup
  it
- MINOR: examples: Use right locale for the last changelog date in haproxy.spec
- BUG/MAJOR: map/acl: real fix segfault during show map/acl on CLI
- BUG/MEDIUM: listener: Fix how unlimited number of consecutive accepts is
  handled
- MINOR: config: Test validity of tune.maxaccept during the config parsing
- CLEANUP: config: Don't alter listener->maxaccept when nbproc is set to 1
- MINOR: threads: Implement HA_ATOMIC_LOAD().
- BUG/MEDIUM: port_range: Make the ring buffer lock-free.
- BUG/MINOR: http_fetch: Rely on the smp direction for "cookie()" and "hdr()"
- BUG/MEDIUM: dns: make the port numbers unsigned
- BUG/MEDIUM: spoe: Don't use the SPOE applet after releasing it
- DOC: fix typos
- BUG/MINOR: ssl_sock: Fix memory leak when disabling compression
- BUILD: ssl: fix latest LibreSSL reg-test error
- BUG/MAJOR: lb/threads: make sure the avoided server is not full on second pass
- BUG/MEDIUM: http: fix "http-request reject" when not final
- BUG/MINOR: deinit/threads: make hard-stop-after perform a clean exit
- BUG/MEDIUM: connection: fix multiple handshake polling issues
- BUG/MEDIUM: vars: make sure the scope is always valid when accessing vars
- BUG/MEDIUM: vars: make the tcp/http unset-var() action support conditions
- BUG/MEDIUM: mux-h2: make sure the connection timeout is always set
- BUG/MINOR: http-rules: mention "deny_status" for "deny" in the error message
- MINOR: doc: Remove -Ds option in man page
- MINOR: doc: add master-worker in the man page
- BUG/MEDIUM: compression: Set Vary: Accept-Encoding for compressed responses
- BUG/MEDIUM: lb_fwlc: Don't test the server's lb_tree from outside the lock
- BUILD: makefile: use :space: instead of digits to count commits
- BUILD: makefile: do not rely on shell substitutions to determine git version
- BUG/MEDIUM: lb_fas: Don't test the server's lb_tree from outside the lock
- BUG/MEDIUM: da: cast the chunk to string.
- MINOR: task: introduce work lists
- BUG/MAJOR: listener: fix thread safety in resume_listener()
- BUG/MEDIUM: tcp-check: unbreak multiple connect rules again
- BUG/MEDIUM: http/htx: unbreak option http_proxy
- BUG/MEDIUM: tcp-checks: do not dereference inexisting conn_stream
- BUG/MEDIUM: protocols: add a global lock for the init/deinit stuff
- BUG/MINOR: proxy: always lock stop_proxy()
- BUILD: threads: add the definition of PROTO_LOCK
- BUG/MEDIUM: lb-chash: Fix the realloc() when the number of nodes is increased
- DOC: improve the wording in CONTRIBUTING about how to document a bug fix
- BUG/MEDIUM: hlua: Check the calling direction in lua functions of the HTTP
  class
- MINOR: hlua: Don't set request analyzers on response channel for lua actions
- MINOR: hlua: Add a flag on the lua txn to know in which context it can be used
- BUG/MINOR: hlua: Only execute functions of HTTP class if the txn is HTTP ready
- BUG/MAJOR: queue/threads: avoid an AB/BA locking issue in process_srv_queue()
- BUG/MINOR: lua: Set right direction and flags on new HTTP objects
- BUG/MEDIUM: protocols: properly initialize the proto_lock in 1.8
- BUG/MEDIUM: lb-chash: Ensure the tree integrity when server weight is
  increased
- BUG/MINOR: stream-int: also update analysers timeouts on activity
- BUG/MEDIUM: mux-h2: split the stream's and connection's window sizes
- BUG/MEDIUM: fd: Always reset the polled_mask bits in fd_dodelete().
- BUG/MINOR: mux-h2: don't refrain from sending an RST_STREAM after another one
- BUG/MINOR: mux-h2: use CANCEL, not STREAM_CLOSED in h2c_frt_handle_data()
- BUG/MEDIUM: mux-h2: do not recheck a frame type after a state transition
- BUG/MINOR: mux-h2: always send stream window update before connection's
- BUG/MINOR: mux-h2: always reset rcvd_s when switching to a new frame
- MINOR: build: Disable -Wstringop-overflow.
- BUG/MINOR: ssl: fix 0-RTT for BoringSSL
- MINOR: ssl: ssl_fc_has_early should work for BoringSSL
- BUG/MEDIUM: lua: Fix test on the direction to set the channel exp timeout

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.20-0
- BUG/MAJOR: listener: Make sure the listener exist before using it.
- BUG/MINOR: listener: keep accept rate counters accurate under saturation
- BUG/MEDIUM: logs: Only attempt to free startup_logs once.
- BUG/MEDIUM: 51d: fix possible segfault on deinit_51degrees()
- BUG/MINOR: ssl: fix warning about ssl-min/max-ver support
- MEDIUM: threads: Use __ATOMIC_SEQ_CST when using the newer atomic API.
- BUG/MEDIUM: threads/fd: do not forget to take into account epoll_fd/pipes
- BUG/MAJOR: spoe: Fix initialization of thread-dependent fields
- BUG/MAJOR: stats: Fix how huge POST data are read from the channel
- BUG/MINOR: http/counters: fix missing increment of fe->srv_aborts
- BUG/MEDIUM: ssl: ability to set TLS 1.3 ciphers using
  ssl-default-server-ciphersuites
- DOC: The option httplog is no longer valid in a backend.
- BUG/MAJOR: checks: segfault during tcpcheck_main
- BUILD: makefile: work around an old bug in GNU make-3.80
- MINOR: tools: make memvprintf() never pass a NULL target to vsnprintf()
- BUILD: makefile: fix build of IPv6 header on aix51
- BUILD: makefile: add _LINUX_SOURCE_COMPAT to build on AIX-51
- BUILD: Makefile: disable shared cache on AIX 5.1
- BUG/MINOR: cli: correctly handle abns in 'show cli sockets'
- MINOR: cli: start addresses by a prefix in 'show cli sockets'
- BUG/MEDIUM: peers: fix a case where peer session is not cleanly reset on
  release.
- BUILD: use inttypes.h instead of stdint.h
- BUILD: connection: fix naming of ip_v field
- BUG/MEDIUM: pattern: assign pattern IDs after checking the config validity
- BUG/MEDIUM: spoe: Queue message only if no SPOE applet is attached to the
  stream
- BUG/MEDIUM: spoe: Return an error if nothing is encoded for fragmented
  messages
- BUG/MINOR: threads: fix the process range of thread masks
- MINOR: lists: Implement locked variations.
- BUG/MEDIUM: lists: Properly handle the case we're removing the first elt.
- BUG/MEDIUM: list: fix the rollback on addq in the locked liss
- BUG/MEDIUM: list: fix LIST_POP_LOCKED's removal of the last pointer
- BUG/MEDIUM: list: add missing store barriers when updating elements and head
- MINOR: list: make the delete and pop operations idempotent
- BUG/MEDIUM: list: correct fix for LIST_POP_LOCKED's removal of last element
- BUG/MEDIUM: list: fix again LIST_ADDQ_LOCKED
- BUG/MEDIUM: list: fix incorrect pointer unlocking in LIST_DEL_LOCKED()
- MAJOR: listener: do not hold the listener lock in listener_accept()
- BUG/MEDIUM: listener: use a self-locked list for the dequeue lists
- BUG/MEDIUM: listener: make sure the listener never accepts too many conns
- BUILD/MINOR: listener: Silent a few signedness warnings.
- MINOR: skip get_gmtime where tm is unused
- BUG/MAJOR: http_fetch: Get the channel depending on the keyword used
- BUG/MEDIUM: maps: only try to parse the default value when it's present
- BUG/MINOR: acl: properly detect pattern type SMP_T_ADDR
- BUG/MEDIUM: thread/http: Add missing locks in set-map and add-acl HTTP rules
- BUG/MINOR: 51d: Get the request channel to call CHECK_HTTP_MESSAGE_FIRST()
- BUG/MINOR: da: Get the request channel to call CHECK_HTTP_MESSAGE_FIRST()
- BUG/MINOR: spoe: Don't systematically wakeup SPOE stream in the applet handler

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.19-0
- DOC: ssl: Clarify when pre TLSv1.3 cipher can be used
- DOC: ssl: Stop documenting ciphers example to use
- BUG/MINOR: spoe: do not assume agent->rt is valid on exit
- BUG/MINOR: lua: initialize the correct idle conn lists for the SSL sockets
- BUG/MEDIUM: spoe: initialization depending on nbthread must be done last
- BUG/MEDIUM: server: initialize the idle conns list after parsing the config
- BUG/MAJOR: spoe: Don't try to get agent config during SPOP healthcheck
- BUG/MAJOR: stream: avoid double free on unique_id
- BUG/MINOR: config: Reinforce validity check when a process number is parsed

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.18-0
- DOC: http-request cache-use / http-response cache-store expects cache name
- BUG/MAJOR: cache: fix confusion between zero and uninitialized cache key
- BUG/MEDIUM: ssl: Disable anti-replay protection and set max data with 0RTT.
- DOC: Be a bit more explicit about allow-0rtt security implications.
- BUG/MEDIUM: ssl: missing allocation failure checks loading tls key file
- BUG/MINOR: backend: don't use url_param_name as a hint for BE_LB_ALGO_PH
- BUG/MINOR: backend: balance uri specific options were lost across defaults
- BUG/MINOR: backend: BE_LB_LKUP_CHTREE is a value, not a bit
- BUG/MINOR: stick_table: Prevent conn_cur from underflowing
- BUG/MINOR: server: don't always trust srv_check_health when loading a
  server state
- BUG/MINOR: check: Wake the check task if the check is finished in
  wake_srv_chk()
- BUG/MEDIUM: ssl: Fix handling of TLS 1.3 KeyUpdate messages
- DOC: mention the effect of nf_conntrack_tcp_loose on src/dst
- MINOR: h2: add a bit-based frame type representation
- MINOR: h2: declare new sets of frame types
- BUG/MINOR: mux-h2: CONTINUATION in closed state must always return GOAWAY
- BUG/MINOR: mux-h2: headers-type frames in HREM are always a connection error
- BUG/MINOR: mux-h2: make it possible to set the error code on an already closed
  stream
- BUG/MINOR: hpack: return a compression error on invalid table size updates
- DOC: nbthread is no longer experimental.
- BUG/MINOR: spoe: corrected fragmentation string size
- BUG/MINOR: deinit: tcp_rep.inspect_rules not deinit, add to deinit
- SCRIPTS: add the slack channel URL to the announce script
- SCRIPTS: add the issue tracker URL to the announce script
- BUG/MINOR: stream: don't close the front connection when facing a backend
  error
- MINOR: xref: Add missing barriers.
- BUG/MEDIUM: mux-h2: wake up flow-controlled streams on initial window update
- BUG/MEDIUM: mux-h2: fix two half-closed to closed transitions
- BUG/MEDIUM: mux-h2: make sure never to send GOAWAY on too old streams
- BUG/MEDIUM: mux-h2: wait for the mux buffer to be empty before closing the
  connection
- MINOR: stream-int: expand the flags to 32-bit
- MINOR: stream-int: add a new flag to mention that we want the connection to
  be killed
- MINOR: connstream: have a new flag CS_FL_KILL_CONN to kill a connection
- BUG/MEDIUM: mux-h2: do not close the connection on aborted streams
- BUG/MEDIUM: stream: Don't forget to free s->unique_id in stream_free().
- BUG/MINOR: config: fix bind line thread mask validation
- BUG/MAJOR: config: verify that targets of track-sc and stick rules are present
- BUG/MAJOR: spoe: verify that backends used by SPOE cover all their callers'
  processes
- BUG/MINOR: config: make sure to count the error on incorrect track-sc/stick
  rules

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.17-0
- BUG/MAJOR: stream-int: Update the stream expiration date in
  stream_int_notify()
- MINOR: mux-h2: only increase the connection window with the first update
- BUG/MEDIUM: mux-h2: mark that we have too many CS once we have more than the
  max
- BUG/MEDIUM: server: Also copy "check-sni" for server templates.
- MINOR: lb: allow redispatch when using consistent hash
- MINOR: stream/cli: fix the location of the waiting flag in "show sess all"
- MINOR: stream/cli: report more info about the HTTP messages on "show sess all"
- BUG/MEDIUM: cli: make "show sess" really thread-safe
- BUG/MINOR: lua: Return an error if a legacy HTTP applet doesn't send anything
- BUG/MINOR: lua: bad args are returned for Lua actions
- BUG/MEDIUM: lua: dead lock when Lua tasks are trigerred
- BUG/CRITICAL: mux-h2: re-check the frame length when PRIORITY is used

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.16-0
- BUG/MINOR: logs: leave startup-logs global and not per-thread
- BUG/MEDIUM: dns: Don't prevent reading the last byte of the payload in
  dns_validate_response()
- BUG/MEDIUM: dns: overflowed dns name start position causing invalid dns error

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.15-0
- OpenSSL updated to 1.1.0j
- ncurses updated to 6.1
- readline updated to 8.0
- Lua updated to 5.3.5
- MINOR: threads: Make sure threads_sync_pipe is initialized before using it.
- DOC: clarify force-private-cache is an option
- BUG/MINOR: connection: avoid null pointer dereference in send-proxy-v2
- BUG/MINOR: backend: check that the mux installed properly
- BUG/MEDIUM: buffers: Make sure we don't wrap in buffer_insert_line2/replace2.
- MEDIUM: ssl: add support for ciphersuites option for TLSv1.3
- BUG/MEDIUM: Cur/CumSslConns counters not threadsafe.
- BUG/MINOR: checks: queues null-deref
- BUG/MEDIUM: mworker: segfault receiving SIGUSR1 followed by SIGTERM.
- BUG/MEDIUM: stream: don't crash on out-of-memory
- BUILD: ssl: fix null-deref warning in ssl_fc_cipherlist_str sample fetch
- BUILD: ssl: fix another null-deref warning in ssl_sock_switchctx_cbk()
- BUILD: stick-table: make sure not to fail on task_new() during initialization
- BUILD: peers: check allocation error during peers_init_sync()
- DOC: Fix a few typos
- BUG/MEDIUM: threads: fix thread_release() at the end of the rendez-vous point
- BUG/MEDIUM: threads: make sure threads_want_sync is marked volatile
- BUILD: compiler: add a new statement "__unreachable()"
- MINOR: lua: all functions calling lua_yieldk() may return
- BUILD: lua: silence some compiler warnings about potential null derefs (#2)
- BUILD: lua: silence some compiler warnings after WILL_LJMP
- CLEANUP: stick-tables: Remove unneeded double (()) around conditional clause
- BUILD: Makefile: add a "make opts" target to simply show the build options
- BUILD: Makefile: speed up compiler options detection
- BUILD: Makefile: silence an option conflict warning with clang
- MINOR: server: Use memcpy() instead of strncpy().
- MINOR: cfgparse: Write 130 as 128 as 0x82 and 0x80.
- MINOR: peers: use defines instead of enums to appease clang.
- DOC: fix reference to map files in MAINTAINERS
- BUILD: compiler: rename __unreachable() to my_unreachable()
- BUG/MEDIUM: pools: Fix the usage of mmap()) with DEBUG_UAF.
- BUG/MEDIUM: h2: Close connection if no stream is left an GOAWAY was sent.
- BUILD: Makefile: add the new ERR variable to force -Werror
- BUG/MINOR: cache: Crashes with "total-max-size" > 2047(MB).
- BUG/MINOR: cache: Wrong usage of shctx_init().
- BUG/MINOR: ssl: Wrong usage of shctx_init().
- DOC: cache: Missing information about "total-max-size"
- BUG/MINOR: only mark connections private if NTLM is detected
- BUG/MINOR: only auto-prefer last server if lb-alg is non-deterministic
- BUG/MAJOR: http: http_txn_get_path() may deference an inexisting buffer
- BUG/MEDIUM: auth/threads: use of crypt() is not thread-safe
- BUG/MINOR: config: better detect the presence of the h2 pattern in npn/alpn
- BUG/MEDIUM: Make sure stksess is properly aligned.
- BUG/MINOR: config: Copy default error messages when parsing of a backend
  starts
- BUG/MEDIUM: hpack: fix encoding of "accept-ranges" field
- BUG/MINOR: ssl: ssl_sock_parse_clienthello ignores session id
- BUG/MINOR: cfgparse: Fix transition between 2 sections with the same name
- BUG/MINOR: cfgparse: Fix the call to post parser of the last sections parsed
- BUG/MINOR: lb-map: fix unprotected update to server's score
- BUG/MEDIUM: sample: Don't treat SMP_T_METH as SMP_T_STR.
- BUG/MINOR: hpack: fix off-by-one in header name encoding length calculation
- BUG/MINOR: mux-h2: refrain from muxing during the preface
- BUG/MINOR: mux-h2: advertise a larger connection window size
- BUILD: compression: fix build error with DEFAULT_MAXZLIBMEM
- BUILD: threads: fix minor build warnings when threads are disabled
- MINOR: stats: report the number of active jobs and listeners in "show info"
- MINOR: servers: Free [idle|safe|priv]_conns on exit.
- DOC: clarify that check-sni needs an argument.
- DOC: refer to check-sni in the documentation of sni
- BUG: dns: Prevent stack-exhaustion via recursion loop in dns_read_name
- BUG: dns: Prevent out-of-bounds read in dns_read_name()
- BUG: dns: Prevent out-of-bounds read in dns_validate_dns_response()
- BUG: dns: Fix out-of-bounds read via signedness error in
  dns_validate_dns_response()
- BUG: dns: Fix off-by-one write in dns_validate_dns_response()
- DOC: Update configuration doc about the maximum number of stick counters.
- DOC: restore note about "independant" typo
- DOC: Fix typos in README and CONTRIBUTING
- DOC: Fix typos in different subsections of the documentation
- DOC: fix a few typos in the documentation

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.14-0
- BUG/MEDIUM: servers: check the queues once enabling a server
- BUG/MEDIUM: queue: prevent a backup server from draining the proxy's
  connections
- MINOR: dns: fix wrong score computation in dns_get_ip_from_response
- MINOR: dns: new DNS options to allow/prevent IP address duplication
- BUG/MEDIUM: lua: possible CLOSE-WAIT state with '\n' headers
- MINOR: threads: Introduce double-width CAS on x86_64 and arm.
- BUG/MEDIUM: threads: fix the double CAS implementation for ARMv7
- MINOR: threads: add more consistency between certain variables in no-thread
  case
- BUG/MEDIUM: threads: fix the no-thread case after the change to the sync point
- MEDIUM: hathreads: implement a more flexible rendez-vous point
- BUG/MEDIUM: cli: make "show fd" thread-safe
- BUG/MINOR: ssl: empty connections reported as errors.
- BUG/MEDIUM: ssl: fix missing error loading a keytype cert from a bundle.
- BUG/MEDIUM: ssl: loading dh param from certifile causes unpredictable error.
- BUG/MINOR: map: fix map_regm with backref
- DOC: dns: explain set server ... fqdn requires resolver
- DOC: ssl: Use consistent naming for TLS protocols
- BUG/MEDIUM: lua: socket timeouts are not applied
- BUG/MEDIUM: cli/threads: protect all "proxy" commands against concurrent
  updates
- BUG/MEDIUM: cli/threads: protect some server commands against concurrent
  operations
- DOC: Fix spelling error in configuration doc
- BUG/MEDIUM: unix: provide a ->drain() function
- BUG/MINOR: lua: Bad HTTP client request duration.
- BUG/MEDIUM: mux_pt: dereference the connection with care in mux_pt_wake()
- BUG/MEDIUM: lua: reset lua transaction between http requests
- BUG/MEDIUM: hlua: Make sure we drain the output buffer when done.
- BUG/MAJOR: thread: lua: Wrong SSL context initialization.
- BUG/MEDIUM: hlua: Don't call RESET_SAFE_LJMP if SET_SAFE_LJMP returns 0.
- BUG/MEDIUM: dns/server: fix incomatibility between SRV resolution and server
  state file
- BUG/MEDIUM: ECC cert should work with TLS < v1.2 and openssl >= 1.1.1
- MINOR: thread: implement HA_ATOMIC_XADD()
- BUG/MINOR: stream: use atomic increments for the request counter
- BUG/MEDIUM: session: fix reporting of handshake processing time in the logs
- BUG/MEDIUM: h2: fix risk of memory leak on malformated wrapped frames
- BUG/MINOR: dns: check and link servers' resolvers right after config parsing
- BUG/MINOR: http/threads: atomically increment the error snapshot ID
- BUG/MEDIUM: snapshot: take the proxy's lock while dumping errors
- BUG/MAJOR: kqueue: Don't reset the changes number by accident.
- BUG/MINOR: server: Crash when setting FQDN via CLI.
- DOC: Fix typos in lua documentation
- BUG/MEDIUM: patterns: fix possible double free when reloading a pattern list
- BUG/MINOR: tools: fix set_net_port() / set_host_port() on IPv4
- BUG/MINOR: cli: make sure the "getsock" command is only called on connections
- BUG/CRITICAL: hpack: fix improper sign check on the header index value

* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.13-0
- MINOR: systemd: consider exit status 143 as successful
- BUG/MINOR: ssl: properly ref-count the tls_keys entries
- MINOR: mux: add a "show_fd" function to dump debugging information for
  "show fd"
- MINOR: h2: implement a basic "show_fd" function
- BUG/MINOR: h2: remove accidental debug code introduced with show_fd function
- MINOR: h2: keep a count of the number of conn_streams attached to the mux
- MINOR: h2: add the mux and demux buffer lengths on "show fd"
- BUG/MEDIUM: h2: don't accept new streams if conn_streams are still in excess
- BUG/MEDIUM: h2: never leave pending data in the output buffer on close
- BUG/MEDIUM: h2: make sure the last stream closes the connection after a
  timeout
- BUG/MINOR: http: Set brackets for the unlikely macro at the right place
- BUILD: Generate sha256 checksums in publish-release
- MINOR: debug: Add check for CO_FL_WILL_UPDATE
- MINOR: debug: Add checks for conn_stream flags
- BUG/MEDIUM: threads: Fix the exit condition of the thread barrier
- MINOR: h2: add the error code and the max/last stream IDs to "show fd"
- BUG/MEDIUM: stream-int: don't immediately enable reading when the buffer was
  reportedly full
- BUG/MEDIUM: stats: don't ask for more data as long as we're responding
- BUG/MINOR: servers: Don't make "server" in a frontend fatal.
- BUG/MEDIUM: threads/sync: use sched_yield when available
- BUG/MEDIUM: h2: prevent orphaned streams from blocking a connection forever
- BUG/MINOR: config: stick-table is not supported in defaults section
- BUG/MINOR: threads: Handle nbthread == MAX_THREADS.
- BUG/MEDIUM: threads: properly fix nbthreads == MAX_THREADS
- MINOR: threads: move "nbthread" parsing to hathreads.c
- BUG/MEDIUM: threads: unbreak "bind" referencing an incorrect thread number
- MEDIUM: proxy_protocol: Convert IPs to v6 when protocols are mixed
- SCRIPTS: git-show-backports: add missing quotes to "echo"

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.12-0
- BUG/MAJOR: stick_table: Complete incomplete SEGV fix
- MINOR: stick-tables: make stktable_release() do nothing on NULL

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.11-0
- BUG/MAJOR: Stick-tables crash with segfault when the key is not in the
  stick-table
- BUG/BUILD: threads: unbreak build without threads

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.10-0
- BUG/MINOR: lua: Socket.send threw runtime error: 'close' needs 1 arguments.
- BUG/MEDIUM: spoe: Flags are not encoded in network order
- BUG/MEDIUM: contrib/mod_defender: Use network order to encode/decode flags
- BUG/MEDIUM: contrib/modsecurity: Use network order to encode/decode flags
- BUG/MINOR: ssl/lua: prevent lua from affecting automatic maxconn computation
- BUG/MEDIUM: cache: don't cache when an Authorization header is present
- BUG/MEDIUM: dns: Delay the attempt to run a DNS resolution on check failure.
- BUG/BUILD: threads: unbreak build without threads
- BUG/BUILD: fd: fix typo causing a warning when threads are disabled
- BUG/MEDIUM: fd: Only check update_mask against all_threads_mask.
- BUG/MEDIUM: servers: Add srv_addr default placeholder to the state file
- BUG/MEDIUM: lua/socket: Length required read doesn't work
- BUG/MEDIUM: stick-tables: Decrement ref_cnt in table_* converters
- BUG/MEDIUM: spoe: Return an error when the wrong ACK is received in sync mode
- MINOR: task/notification: Is notifications registered ?
- BUG/MEDIUM: lua/socket: wrong scheduling for sockets
- BUG/MAJOR: lua: Dead lock with sockets
- BUG/MEDIUM: lua/socket: Notification error
- BUG/MEDIUM: lua/socket: Sheduling error on write: may dead-lock
- BUG/MEDIUM: lua/socket: Buffer error, may segfault
- MAJOR: spoe: upgrade the SPOP version to 2.0 and remove the support for 1.0
- BUG/MINOR: contrib/spoa_example: Don't reset the status code during disconnect
- BUG/MINOR: contrib/mod_defender: Don't reset the status code during disconnect
- BUG/MINOR: contrib/modsecurity: Don't reset the status code during disconnect
- BUG/MINOR: contrib/mod_defender: update pointer on the end of the frame
- BUG/MINOR: contrib/modsecurity: update pointer on the end of the frame
- DOC: SPOE.txt: fix a typo
- DOC: contrib/modsecurity: few typo fixes
- BUG/MINOR: unix: Make sure we can transfer abns sockets on seamless reload.
- BUG/MEDIUM: threads: handle signal queue only in thread 0
- BUG/MINOR: don't ignore SIG{BUS,FPE,ILL,SEGV} during signal processing
- BUG/MINOR: signals: ha_sigmask macro for multithreading
- MINOR: lua: Increase debug information
- BUG/MAJOR: map: fix a segfault when using http-request set-map
- BUG/MINOR: lua: Segfaults with wrong usage of types.
- BUG/MAJOR: ssl: Random crash with cipherlist capture
- BUG/MAJOR: ssl: OpenSSL context is stored in non-reserved memory slot
- BUG/MEDIUM: fd: Don't modify the update_mask in fd_dodelete().
- BUG/MEDIUM: threads: Use the sync point to check active jobs and exit
- MINOR: threads: Be sure to remove threads from all_threads_mask on exit

* Sat Jun 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.9-0
- BUG/MINOR: pattern: Add a missing HA_SPIN_INIT() in pat_ref_newid()
- BUG/MAJOR: channel: Fix crash when trying to read from a closed socket
- BUG/MINOR: log: t_idle (%Ti) is not set for some requests
- BUG/MEDIUM: lua: Fix segmentation fault if a Lua task exits
- MINOR: h2: detect presence of CONNECT and/or content-length
- BUG/MEDIUM: h2: implement missing support for chunked encoded uploads
- BUG/MINOR: lua/threads: Make lua's tasks sticky to the current thread
- BUG/MINOR: config: disable http-reuse on TCP proxies
- BUG/MINOR: checks: Fix check->health computation for flapping servers
- BUG/MEDIUM: threads: Fix the sync point for more than 32 threads
- BUG/MINOR: lua: Put tasks to sleep when waiting for data
- DOC/MINOR: clean up LUA documentation re: servers & array/table.
- BUG/MINOR: map: correctly track reference to the last ref_elt being dumped
- BUG/MEDIUM: task: Don't free a task that is about to be run.
- BUG/MINOR: lua: schedule socket task upon lua connect()
- BUG/MINOR: lua: ensure large proxy IDs can be represented
- BUG/MEDIUM: http: don't always abort transfers on CF_SHUTR
- BUG/MEDIUM: pollers: Use a global list for fd shared between threads.
- BUG/MEDIUM: ssl: properly protect SSL cert generation
- BUG/MINOR: spoe: Mistake in error message about SPOE configuration

* Sat Jun 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.8-0
- BUG/MEDIUM: threads: Fix the max/min calculation because of name clashes
- BUG/MEDIUM: connection: Make sure we have a mux before calling detach().
- BUG/MINOR: http: Return an error in proxy mode when url2sa fails
- BUG/MEDIUM: kqueue: When adding new events, provide an output to get errors.
- BUG/MINOR: cli: Guard against NULL messages when using CLI_ST_PRINT_FREE
- MINOR: cli: Ensure the CLI always outputs an error when it should
- DOC: lua: update the links to the config and Lua API
- BUG/CRITICAL: h2: fix incorrect frame length check

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.5-0
- BoringSSL replaced by OpenSSL (build fails with latest version of BoringSSL)
- BUG/MINOR: threads: fix missing thread lock labels for 1.8
- BUG/MEDIUM: ssl: Don't always treat SSL_ERROR_SYSCALL as unrecovarable.
- BUG/MEDIUM: ssl: Shutdown the connection for reading on SSL_ERROR_SYSCALL
- BUG/MINOR: init: Add missing brackets in the code parsing -sf/-st
- BUG/MINOR: ssl/threads: Make management of the TLS ticket keys files
  thread-safe
- BUG/MEDIUM: http: Switch the HTTP response in tunnel mode as earlier as
  possible
- BUG/MEDIUM: ssl/sample: ssl_bc_* fetch keywords are broken.
- DOC: lua: new prototype for function "register_action()"
- DOC: cfgparse: Warn on option (tcp|http)log in backend
- BUG/MINOR: debug/pools: properly handle out-of-memory when building with
  DEBUG_UAF
- MINOR: debug/pools: make DEBUG_UAF also detect underflows
- BUG/MINOR: h2: Set the target of dbuf_wait to h2c
- MINOR: stats: display the number of threads in the statistics.
- BUG/MEDIUM: h2: always consume any trailing data after end of output buffers
- BUG/MEDIUM: buffer: Fix the wrapping case in bo_putblk
- BUG/MEDIUM: buffer: Fix the wrapping case in bi_putblk
- Revert "BUG/MINOR: send-proxy-v2: string size must include ('\0')"
- MINOR: systemd: Add section for SystemD sandboxing to unit file
- MINOR: systemd: Add SystemD's Protect*= options to the unit file
- MINOR: systemd: Add SystemD's SystemCallFilter option to the unit file
- MINOR/BUILD: fix Lua build on Mac OS X
- BUILD/MINOR: fix Lua build on Mac OS X (again)
- BUG/MINOR: session: Fix tcp-request session failure if handshake.
- CLEANUP: .gitignore: Ignore binaries from the contrib directory
- BUG/MINOR: unix: Don't mess up when removing the socket from the
  xfer_sock_list.
- BUG/MEDIUM: h2: also arm the h2 timeout when sending
- BUG/MINOR: cli: Fix a crash when passing a negative or too large value
  to "show fd"
- CLEANUP: ssl: Remove a duplicated #include
- CLEANUP: cli: Remove a leftover debug message
- BUG/MINOR: cli: Fix a typo in the 'set rate-limit' usage
- BUG/MEDIUM: fix a 100% cpu usage with cpu-map and nbthread/nbproc
- BUG/MINOR: force-persist and ignore-persist only apply to backends
- BUG/MEDIUM: spoe: Remove idle applets from idle list when HAProxy is stopping
- BUG/MEDIUM: threads/unix: Fix a deadlock when a listener is temporarily
  disabled
- BUG/MAJOR: threads/queue: Fix thread-safety issues on the queues management
- BUG/MINOR: dns: don't downgrade DNS accepted payload size automatically
- BUG/MINOR: seemless reload: Fix crash when an interface is specified.
- BUG/MINOR: cli: Fix a crash when sending a command with too many arguments
- BUILD: ssl: Fix build with OpenSSL without NPN capability
- BUG/MINOR: spoa-example: unexpected behavior for more than 127 args
- BUG/MINOR: lua: return bad error messages
- BUG/MEDIUM: tcp-check: single connect rule can't detect DOWN servers
- BUG/MINOR: tcp-check: use the server's service port as a fallback
- BUG/MEDIUM: threads/queue: wake up other threads upon dequeue
- MINOR: log: stop emitting alerts when it's not possible to write on the socket
- BUILD/BUG: enable -fno-strict-overflow by default
- DOC: log: more than 2 log servers are allowed
- DOC: don't suggest using http-server-close
- BUG/MEDIUM: h2: properly account for DATA padding in flow control
- BUG/MINOR: h2: ensure we can never send an RST_STREAM in response to an
  RST_STREAM
- BUG/MINOR: listener: Don't decrease actconn twice when a new session is
  rejected

* Tue Apr 03 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.4-1
- Using GCC from devtoolset-3 for build

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.4-0
- BoringSSL updated to latest version
- PCRE updated to 8.42
- BUG/MEDIUM: h2: properly handle the END_STREAM flag on empty DATA frames
- BUILD: ssl: silence a warning when building without NPN nor ALPN support
- BUG/MEDIUM: ssl: cache doesn't release shctx blocks
- BUG/MINOR: lua: Fix default value for pattern in Socket.receive
- DOC: lua: Fix typos in comments of hlua_socket_receive
- BUG/MEDIUM: lua: Fix IPv6 with separate port support for Socket.connect
- BUG/MINOR: lua: Fix return value of Socket.settimeout
- MINOR: dns: Handle SRV record weight correctly.
- BUG/MEDIUM: mworker: execvp failure depending on argv[0]
- MINOR: hathreads: add support for gcc < 4.7
- BUILD/MINOR: ancient gcc versions atomic fix
- BUG/MEDIUM: stream: properly handle client aborts during redispatch
- DOC: clarify the scope of ssl_fc_is_resumed
- CONTRIB: debug: fix a few flags definitions
- BUG/MINOR: poll: too large size allocation for FD events
- BUG/MEDIUM: peers: fix expire date wasn't updated if entry is modified
  remotely.
- MINOR: servers: Don't report duplicate dyncookies for disabled servers.
- MINOR: global/threads: move cpu_map at the end of the global struct
- MINOR: threads: add a MAX_THREADS define instead of LONGBITS
- MINOR: global: add some global activity counters to help debugging
- MINOR: threads/fd: Use a bitfield to know if there are FDs for a thread in
  the FD cache
- BUG/MEDIUM: threads/polling: Use fd_cache_mask instead of fd_cache_num
- BUG/MEDIUM: fd: maintain a per-thread update mask
- MINOR: fd: add a bitmask to indicate that an FD is known by the poller
- BUG/MEDIUM: epoll/threads: use one epoll_fd per thread
- BUG/MEDIUM: kqueue/threads: use one kqueue_fd per thread
- BUG/MEDIUM: threads/mworker: fix a race on startup
- BUG/MINOR: mworker: only write to pidfile if it exists
- MINOR: threads: Fix build when we're not compiling with threads.
- BUG/MINOR: threads: always set an owner to the thread_sync pipe
- BUG/MEDIUM: threads/server: Fix deadlock in
  srv_set_stopping/srv_set_admin_flag
- BUG/MEDIUM: checks: Don't try to release undefined conn_stream when a check
  is freed
- BUG/MINOR: kqueue/threads: Don't forget to close kqueue_fd[tid] on each thread
- MINOR: threads: Use __decl_hathreads instead of #ifdef/#endif
- BUILD: epoll/threads: Add test on MAX_THREADS to avoid warnings when complied
  without threads
- BUILD: kqueue/threads: Add test on MAX_THREADS to avoid warnings when complied
  without threads
- CLEANUP: sample: Fix comment encoding of sample.c
- CLEANUP: sample: Fix outdated comment about sample casts functions
- BUG/MINOR: sample: Fix output type of c_ipv62ip
- CLEANUP: Fix typo in ARGT_MSK6 comment
- BUG/MINOR: cli: use global.maxsock and not maxfd to list all FDs
- BUG/MINOR: threads: Update labels array because of changes in lock_label enum
- BUG/MINOR: epoll/threads: only call epoll_ctl(DEL) on polled FDs
- BUG/MEDIUM: spoe: Always try to receive or send the frame to detect shutdowns
- BUG/MEDIUM: spoe: Allow producer to read and to forward shutdown on request
  side
- BUG/MINOR: time/threads: ensure the adjusted time is always correct
- BUG/MEDIUM: standard: Fix memory leak in str2ip2()
- MINOR: init: emit warning when -sf/-sd cannot parse argument
- DOC: Describe routing impact of using interface keyword on bind lines
- DOC: Mention -Ws in the list of available options
- BUG/MINOR: config: don't emit a warning when global stats is incompletely
  configured

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-0
- BUG/MEDIUM: h2: properly handle and report some stream errors
- BUG/MEDIUM: h2: improve handling of frames received on closed streams
- DOC/MINOR: configuration: typo, formatting fixes
- BUG/MEDIUM: h2: ensure we always know the stream before sending a reset
- BUG/MEDIUM: mworker: don't close stdio several time
- MINOR: don't close stdio anymore
- BUG/MEDIUM: http: don't automatically forward request close
- BUG/MAJOR: hpack: don't return direct references to the dynamic headers table
- MEDIUM: h2: prepare a graceful shutdown when the frontend is stopped

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.2-0
- BUG/MINOR: action: Don't check http capture rules when no id is defined
- BUG/MAJOR: hpack: don't pretend large headers fit in empty table
- BUG/MINOR: ssl: support tune.ssl.cachesize 0 again
- BUG/MEDIUM: mworker: also close peers sockets in the master
- BUG/MEDIUM: ssl engines: Fix async engines fds were not considered to fix fd
  limit automatically.
- BUG/MEDIUM: checks: a down server going to maint remains definitely stucked
  on down state.
- BUG/MEDIUM: peers: set NOLINGER on the outgoing stream interface
- BUG/MEDIUM: h2: fix handling of end of stream again
- MINOR: mworker: Update messages referencing exit-on-failure
- MINOR: mworker: Improve wording in `void mworker_wait()`
- CONTRIB: halog: Add help text for -s switch in halog program
- BUG/MEDIUM: email-alert: don't set server check status from a email-alert task
- BUG/MEDIUM: threads/vars: Fix deadlock in register_name
- MINOR: systemd: remove comment about HAPROXY_STATS_SOCKET
- DOC: notifications: add precisions about thread usage
- BUG/MEDIUM: lua/notification: memory leak
- MINOR: conn_stream: add new flag CS_FL_RCV_MORE to indicate pending data
- BUG/MEDIUM: stream-int: always set SI_FL_WAIT_ROOM on CS_FL_RCV_MORE
- BUG/MEDIUM: h2: automatically set CS_FL_RCV_MORE when the output buffer is
  full
- BUG/MEDIUM: h2: enable recv polling whenever demuxing is possible
- BUG/MEDIUM: h2: work around a connection API limitation
- BUG/MEDIUM: h2: debug incoming traffic in h2_wake()
- MINOR: h2: store the demux padding length in the h2c struct
- BUG/MEDIUM: h2: support uploading partial DATA frames
- MINOR: h2: don't demand that a DATA frame is complete before processing it
- BUG/MEDIUM: h2: don't switch the state to HREM before end of DATA frame
- BUG/MEDIUM: h2: don't close after the first DATA frame on tunnelled responses
- BUG/MEDIUM: http: don't disable lingering on requests with tunnelled responses
- BUG/MEDIUM: h2: fix stream limit enforcement
- BUG/MINOR: stream-int: don't try to receive again after receiving an EOS
- BUG: MAJOR: lb_map: server map calculation broken
- BUG: MINOR: http: don't check http-request capture id when len is provided
- BUILD/MINOR: Makefile : enabling USE_CPU_AFFINITY
- BUG/MEDIUM: mworker: Set FD_CLOEXEC flag on log fd
- DOC/MINOR: intro: typo, wording, formatting fixes
- MINOR: netscaler: respect syntax
- MINOR: netscaler: remove the use of cip_magic only used once
- MINOR: netscaler: rename cip_len to clarify its uage
- BUG/MEDIUM: netscaler: use the appropriate IPv6 header size
- BUG/MAJOR: netscaler: address truncated CIP header detection
- CONTRIB: iprange: Fix compiler warning in iprange.c
- CONTRIB: halog: Fix compiler warnings in halog.c
- BUG/MINOR: h2: properly report a stream error on RST_STREAM
- MINOR: mux: add flags to describe a mux's capabilities
- MINOR: stream-int: set flag SI_FL_CLEAN_ABRT when mux supports clean aborts
- BUG/MEDIUM: stream: don't consider abortonclose on muxes which close cleanly
- MINOR: netscaler: check in one-shot if buffer is large enough for IP and TCP
  header
- MEDIUM: netscaler: do not analyze original IP packet size
- MEDIUM: netscaler: add support for standard NetScaler CIP protocol
- BUG/MEDIUM: checks: a server passed in maint state was not forced down.
- BUG/MEDIUM: lua: fix crash when using bogus mode in register_service()
- MINOR: http: adjust the list of supposedly cacheable methods
- MINOR: http: update the list of cacheable status codes as per RFC7231
- MINOR: http: start to compute the transaction's cacheability from the request
- BUG/MINOR: http: do not ignore cache-control: public
- BUG/MINOR: http: properly detect max-age=0 and s-maxage=0 in responses
- BUG/MINOR: cache: do not force the TX_CACHEABLE flag before checking
  cacheability
- MINOR: http: add a function to check request's cache-control header field
- BUG/MEDIUM: cache: do not try to retrieve host-less requests from the cache
- BUG/MEDIUM: cache: replace old object on store
- BUG/MEDIUM: cache: respect the request cache-control header
- BUG/MEDIUM: cache: don't cache the response on no-cache="set-cookie"
- BUG/MAJOR: connection: refine the situations where we don't send shutw()
- BUG/MEDIUM: checks: properly set servers to stopping state on 404

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- BUG/MEDIUM: kqueue: Don't bother closing the kqueue after fork.
- DOC: cache: update sections and fix some typos
- BUILD/MINOR: deviceatlas: enable thread support
- BUG/MEDIUM: tcp-check: Don't lock the server in tcpcheck_main
- BUG/MEDIUM: ssl: don't allocate shctx several time
- BUG/MEDIUM: cache: bad computation of the remaining size
- BUILD: checks: don't include server.h
- BUG/MEDIUM: stream: fix session leak on applet-initiated connections
- BUILD/MINOR: haproxy : FreeBSD/cpu affinity needs pthread_np header
- BUG/MINOR: ssl: CO_FL_EARLY_DATA removal is managed by stream
- BUG/MEDIUM: threads/peers: decrement, not increment jobs on quitting
- BUG/MEDIUM: h2: don't report an error after parsing a 100-continue response
- BUG/MEDIUM: peers: fix some track counter rules dont register entries for
  sync.
- BUG/MAJOR: thread/peers: fix deadlock on peers sync.
- BUILD/MINOR: haproxy: compiling config cpu parsing handling when needed
- BUG/MINOR: mworker: fix validity check for the pipe FDs
- BUG/MINOR: mworker: detach from tty when in daemon mode
- MINOR: threads: Fix pthread_setaffinity_np on FreeBSD.
- BUG/MAJOR: thread: Be sure to request a sync between threads only once at a
  time
- BUILD: Fix LDFLAGS vs. LIBS re linking order in various makefiles
- BUG/MEDIUM: checks: Be sure we have a mux if we created a cs.
- BUG/MINOR: hpack: fix debugging output of pseudo header names
- BUG/MINOR: hpack: must reject huffman literals padded with more than 7 bits
- BUG/MINOR: hpack: reject invalid header index
- BUG/MINOR: hpack: dynamic table size updates are only allowed before headers
- BUG/MAJOR: h2: correctly check the request length when building an H1 request
- BUG/MINOR: h2: immediately close if receiving GOAWAY after the last stream
- BUG/MINOR: h2: try to abort closed streams as soon as possible
- BUG/MINOR: h2: ":path" must not be empty
- BUG/MINOR: h2: fix a typo causing PING/ACK to be responded to
- BUG/MINOR: h2: the TE header if present may only contain trailers
- BUG/MEDIUM: h2: enforce the per-connection stream limit
- BUG/MINOR: h2: do not accept SETTINGS_ENABLE_PUSH other than 0 or 1
- BUG/MINOR: h2: reject incorrect stream dependencies on HEADERS frame
- BUG/MINOR: h2: properly check PRIORITY frames
- BUG/MINOR: h2: reject response pseudo-headers from requests
- BUG/MEDIUM: h2: remove connection-specific headers from request
- BUG/MEDIUM: h2: do not accept upper case letters in request header names
- BUG/MINOR: h2: use the H2_F_DATA_* macros for DATA frames

* Wed Nov 29 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.8.0-0
- Initial build
