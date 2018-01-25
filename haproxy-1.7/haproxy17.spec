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

%define lua_ver           5.3.4
%define pcre_ver          8.41
%define boringssl_ver     664e99a6486c293728097c661332f92bf2d847c6
%define ncurses_ver       6.0
%define readline_ver      7.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.7.9
Release:           1%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           http://www.haproxy.org/download/1.7/src/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.cfg
Source3:           %{name}.logrotate
Source4:           %{name}.sysconfig
Source5:           %{name}.service

Source10:          http://www.lua.org/ftp/lua-%{lua_ver}.tar.gz
Source11:          http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{pcre_ver}.tar.gz
Source12:          https://boringssl.googlesource.com/boringssl/+archive/%{boringssl_ver}.tar.gz
Source13:          https://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{ncurses_ver}.tar.gz
Source14:          https://ftp.gnu.org/gnu/readline/readline-%{readline_ver}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make zlib-devel

%if 0%{?rhel} >= 7
BuildRequires:     gcc gcc-c++
%else
BuildRequires:     devtoolset-2-gcc-c++ devtoolset-2-binutils
%endif

Requires:          setup >= 2.8.14-14 kaosv >= 2.10

%if 0%{?rhel} >= 7
Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(pre):     shadow-utils
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

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
%setup -q

mkdir boringssl

%{__tar} xzvf %{SOURCE10}
%{__tar} xzvf %{SOURCE11}
%{__tar} xzvf %{SOURCE12} -C boringssl
%{__tar} xzvf %{SOURCE13}
%{__tar} xzvf %{SOURCE14}

%build

%if 0%{?rhel} < 7
# Use gcc and gcc-c++ from devtoolset for build on CentOS6
export PATH="/opt/rh/devtoolset-2/root/usr/bin:$PATH"
%endif

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static BoringSSL build
mkdir boringssl/build

pushd boringssl/build &> /dev/null
  cmake ../
  %{__make} %{?_smp_mflags}
popd

mkdir -p "boringssl/.openssl/lib"

pushd boringssl/.openssl &> /dev/null
  ln -s ../include
popd

cp boringssl/build/crypto/libcrypto.a boringssl/build/ssl/libssl.a boringssl/.openssl/lib

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
  ./configure --prefix=$(pwd)/build --enable-shared=no --enable-utf8 --enable-jit
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

### DEPS BUILD END ###

%ifarch %ix86 x86_64
use_regparm="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" \
                          TARGET="linux26" \
                          USE_OPENSSL=1 \
                          SSL_INC=libressl-%{libre_ver}/build/include \
                          SSL_LIB=libressl-%{libre_ver}/build/lib \
                          USE_PCRE_JIT=1 \
                          USE_STATIC_PCRE=1 \
                          PCRE_INC=pcre-%{pcre_ver}/build/include \
                          PCRE_LIB=pcre-%{pcre_ver}/build/lib \
                          USE_LUA=1 \
                          LUA_INC=lua-%{lua_ver}/build/include \
                          LUA_LIB=lua-%{lua_ver}/build/lib \
                          USE_ZLIB=1 \
                          ADDLIB="-ldl -lrt" \
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
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]]; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} %{name} stop >/dev/null 2>&1
  %{__chkconfig} --del %{name} &>/dev/null || :
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGELOG LICENSE README doc/*
%doc examples/*.cfg
%dir %{hp_datadir}
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{hp_datadir}/*
%{_initrddir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Thu Nov 30 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.9-1
- Migrated from LibreSSL to BoringSSL

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.9-0
- BUG/MINOR: peers: peer synchronization issue (with several peers sections).
- BUG/MINOR: lua: In error case, the safe mode is not removed
- BUG/MINOR: lua: executes the function destroying the Lua session in safe
  mode
- BUG/MAJOR: lua/socket: resources not detroyed when the socket is aborted
- BUG/MEDIUM: lua: bad memory access
- DOC: update CONTRIBUTING regarding optional parts and message format
- DOC: update the list of OpenSSL versions in the README
- MINOR: tools: add a portable timegm() alternative
- BUILD: lua: replace timegm() with my_timegm() to fix build on Solaris 10
- DOC: Updated 51Degrees git URL to point to a stable version.
- BUG/MINOR: http: Set the response error state in http_sync_res_state
- MINOR: http: Reorder/rewrite checks in http_resync_states
- MINOR: http: Switch requests/responses in TUNNEL mode only by checking txn
  flags
- BUG/MEDIUM: http: Switch HTTP responses in TUNNEL mode when body length is
  undefined
- BUG/MAJOR: http: Fix possible infinity loop in http_sync_(req|res)_state
- BUG/MINOR: lua: Fix Server.get_addr() port values
- BUG/MINOR: lua: Correctly use INET6_ADDRSTRLEN in Server.get_addr()
- BUG/MINOR: lua: always detach the tcp/http tasks before freeing them
- BUG/MINOR: lua: Fix bitwise logic for hlua_server_check_* functions.

* Mon Aug 14 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.8-1
- Added ExecReload handler to systemd unit

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.8-0
- BUG/MINOR: stream: flag TASK_WOKEN_RES not set if task in runqueue
- BUG/MAJOR: cli: fix custom io_release was crushed by NULL.
- BUG/MAJOR: map: fix segfault during 'show map/acl' on cli.
- BUG/MAJOR: compression: Be sure to release the compression state in all cases
- DOC: fix references to the section about time format.
- BUG/MEDIUM: map/acl: fix unwanted flags inheritance.
- BUG/MINOR: stream: Don't forget to remove CF_WAKE_ONCE flag on response channel
- BUG/MINOR: http: Don't reset the transaction if there are still data to send
- BUG/MEDIUM: filters: Be sure to call flt_end_analyze for both channels
- BUG/MINOR: http: properly handle all 1xx informational responses

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.7-0
- BUG/MINOR: Wrong peer task expiration handling during synchronization processing.
- BUG/MEDIUM: http: Drop the connection establishment when a redirect is performed
- BUG/MEDIUM: cfgparse: Check if tune.http.maxhdr is in the range 1..32767
- DOC: fix references to the section about the unix socket
- BUG/MINOR: haproxy/cli : fix for solaris/illumos distros for CMSG* macros
- BUG/MINOR: log: pin the front connection when front ip/ports are logged

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.6-0
- DOC: changed "block"(deprecated) examples to http-request deny
- DOC: add few comments to examples.
- DOC: update sample code for PROXY protocol
- DOC: mention lighttpd 1.4.46 implements PROXY
- DOC: stick-table is available in frontend sections
- BUG/MINOR: dns: Wrong address family used when creating IPv6 sockets.
- BUG/MINOR: config: missing goto out after parsing an incorrect ACL character
- BUG/MINOR: arg: don't try to add an argument on failed memory allocation
- BUG/MEDIUM: arg: ensure that we properly unlink unresolved arguments on error
- BUG/MEDIUM: acl: don't free unresolved args in prune_acl_expr()
- MINOR: lua: ensure the memory allocator is used all the time
- CLEANUP: logs: typo: simgle => single
- BUG/MEDIUM: acl: proprely release unused args in prune_acl_expr()
- BUG/MAJOR: Use -fwrapv.
- BUG/MINOR: server: don't use "proxy" when px is really meant.
- BUG/MINOR: server: missing default server 'resolvers' setting duplication.
- DOC: add layer 4 links/cross reference to "block" keyword.
- DOC: errloc/errorloc302/errorloc303 missing status codes.
- BUG/MEDIUM: lua: memory leak
- MEDIUM: config: don't check config validity when there are fatal errors
- BUG/MINOR: hash-balance-factor isn't effective in certain circumstances
- MINOR/DOC: lua: just precise one thing
- BUG/MINOR: http: Fix conditions to clean up a txn and to handle the next request
- DOC: update RFC references
- BUG/MINOR: checks: don't send proxy protocol with agent checks
- BUG/MAJOR: dns: Broken kqueue events handling (BSD systems).
- BUG/MEDIUM: lua: segfault if a converter or a sample doesn't return anything
- BUG/MINOR: Makefile: fix compile error with USE_LUA=1 in ubuntu16.04
- BUG/MAJOR: http: call manage_client_side_cookies() before erasing the buffer
- BUG/MINOR: buffers: Fix bi/bo_contig_space to handle full buffers
- BUG/MINOR: acls: Set the right refflag when patterns are loaded from a map
- BUG/MINOR: http/filters: Be sure to wait if a filter loops in HTTP_MSG_ENDING
- BUG/MEDIUM: peers: Peers CLOSE_WAIT issue.
- BUG/MAJOR: server: Segfault after parsing server state file.
- BUG/MEDIUM: unix: never unlink a unix socket from the file system
- scripts: create-release pass -n to tail
- SCRIPTS: create-release: enforce GIT_COMMITTER_{NAME|EMAIL} validity

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.5-0
- BUG/MEDIUM: peers: fix buffer overflow control in intdecode.
- BUG/MEDIUM: buffers: Fix how input/output data are injected into buffers
- BUG/MEDIUM: http: Fix blocked HTTP/1.0 responses when compression is enabled
- BUG/MINOR: filters: Don't force the stream's wakeup when we wait in
  flt_end_analyze
- DOC: fix parenthesis and add missing "Example" tags
- DOC: update the contributing file
- DOC: log-format/tcplog/httplog update
- MINOR: config parsing: add warning when log-format/tcplog/httplog is
  overriden in "defaults" sections

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- MINOR: config: warn when some HTTP rules are used in a TCP proxy
- BUG/MINOR: spoe: Fix soft stop handler using a specific id for spoe filters
- BUG/MINOR: spoe: Fix parsing of arguments in spoe-message section
- BUG/MEDIUM: ssl: Clear OpenSSL error stack after trying to parse OCSP file
- BUG/MEDIUM: cli: Prevent double free in CLI ACL lookup
- BUG/MINOR: Fix "get map <map> <value>" CLI command
- BUG/MAJOR: connection: update CO_FL_CONNECTED before calling the data layer
- BUG/MEDIUM: ssl: switchctx should not return SSL_TLSEXT_ERR_ALERT_WARNING
- BUG/MINOR: checks: attempt clean shutw for SSL check
- CONTRIB: tcploop: add limits.h to fix build issue with some compilers
- CONTRIB: tcploop: make it build on FreeBSD
- CONTRIB: tcploop: fix time format to silence build warnings
- CONTRIB: tcploop: report action 'K' (kill) in usage message
- CONTRIB: tcploop: fix connect's address length
- CONTRIB: tcploop: use the trash instead of NULL for recv()
- BUG/MEDIUM: listener: do not try to rebind another process' socket
- BUG/MEDIUM: filters: Fix channels synchronization in flt_end_analyze
- BUG/MAJOR: stream-int: do not depend on connection flags to detect connection
- BUG/MEDIUM: connection: ensure to always report the end of handshakes
- BUG: payload: fix payload not retrieving arbitrary lengths
- BUG/MAJOR: http: fix typo in http_apply_redirect_rule
- MINOR: doc: 2.4. Examples should be 2.5. Examples
- BUG/MEDIUM: stream: fix client-fin/server-fin handling
- MINOR: fd: add a new flag HAP_POLL_F_RDHUP to struct poller
- BUG/MINOR: raw_sock: always perfom the last recv if RDHUP is not available
- DOC/MINOR: Fix typos in proxy protocol doc
- DOC: Protocol doc: add checksum, TLV type ranges
- DOC: Protocol doc: add SSL TLVs, rename CHECKSUM
- DOC: Protocol doc: add noop TLV
- MEDIUM: global: add a 'hard-stop-after' option to cap the soft-stop time
- BUG/MINOR: cfgparse: loop in tracked servers lists not detected by
  check_config_validity().
- MINOR: server: irrelevant error message with 'default-server' config file
  keyword.
- MINOR: doc: fix use-server example (imap vs mail)
- BUG/MEDIUM: tcp: don't require privileges to bind to device
- BUILD: make the release script use shortlog for the final changelog
- BUILD: scripts: fix typo in announce-release error message

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- BUG/MINOR: stream: Fix how backend-specific analyzers are set on a stream
- BUILD: ssl: fix build on OpenSSL 1.0.0
- BUILD: ssl: silence a warning reported for ERR_remove_state()
- BUILD: ssl: eliminate warning with OpenSSL 1.1.0 regarding 
  RAND_pseudo_bytes()
- BUG/MEDIUM: tcp: don't poll for write when connect() succeeds
- BUG/MINOR: unix: fix connect's polling in case no data are scheduled
- DOC: lua: improve links
- BUG/MINOR: lua: Map.end are not reliable because "end" is a reserved
  keyword
- MINOR: dns: give ability to dns_init_resolvers() to close a socket when
  requested
- BUG/MAJOR: dns: restart sockets after fork()
- MINOR: chunks: implement a simple dynamic allocator for trash buffers
- BUG/MEDIUM: http: prevent redirect from overwriting a buffer
- BUG/MEDIUM: filters: Do not truncate HTTP response when body length is
  undefined
- BUG/MEDIUM: http: Prevent replace-header from overwriting a buffer
- BUG/MINOR: http: Return an error when a replace-header rule failed on
  the response
- BUG/MINOR: sendmail: The return of vsnprintf is not cleanly tested
- BUG/MAJOR: lua segmentation fault when the request is like 
  'GET ?arg=val HTTP/1.1'
- BUG/MEDIUM: config: reject anything but "if" or "unless" after a
  use-backend rule
- MINOR: http: don't close when redirect location doesn't start with "/"

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- BUG/MEDIUM: lua: In some case, the return of sample-fetches is ignored (2)
- SCRIPTS: git-show-backports: fix a harmless typo
- SCRIPTS: git-show-backports: add -H to use the hash of the commit message
- BUG/MINOR: stream-int: automatically release SI_FL_WAIT_DATA on SHUTW_NOW
- DOC: lua: documentation about time parser functions
- DOC: lua: section declared twice
- BUG/MINOR: lua/cli: bad error message
- DOC: fix small typo in fe_id (backend instead of frontend)
- BUG/MINOR: Fix the sending function in Lua's cosocket
- BUG/MINOR: lua: memory leak executing tasks
- BUG/MINOR: lua: bad return code
- BUG/MEDIUM: ssl: properly reset the reused_sess during a forced handshake
- BUG/MEDIUM: ssl: avoid double free when releasing bind_confs
- BUG/MINOR: stats: fix be/sessions/current out in typed stats
- BUG/MINOR: backend: nbsrv() should return 0 if backend is disabled
- BUG/MEDIUM: ssl: for a handshake when server-side SNI changes
- BUG/MINOR: systemd: potential zombie processes
- DOC: Add timings events schemas
- BUILD: lua: build failed on FreeBSD.
- BUG/MINOR: option prefer-last-server must be ignored in some case
- MINOR: stats: Support "select all" for backend actions
- BUG/MINOR: sample-fetches/stick-tables: bad type for the sample fetches sc*_get_gpt0
- BUG/MAJOR: channel: Fix the definition order of channel analyzers
- BUG/MINOR: http: report real parser state in error captures
- BUILD: scripts: automatically update the branch in version.h when releasing
- BUG/MAJOR: http: fix risk of getting invalid reports of bad requests
- MINOR: http: custom status reason.
- MINOR: connection: add sample fetch "fc_rcvd_proxy"
- BUG/MINOR: config: emit a warning if http-reuse is enabled with incompatible options
- BUG/MINOR: tools: fix off-by-one in port size check
- BUG/MEDIUM: server: consider AF_UNSPEC as a valid address family
- MEDIUM: server: split the address and the port into two different fields
- MINOR: tools: make str2sa_range() return the port in a separate argument
- MINOR: server: take the destination port from the port field, not the addr
- MEDIUM: server: disable protocol validations when the server doesn't resolve
- BUG/MEDIUM: tools: do not force an unresolved address to AF_INET:0.0.0.0
- BUG/MINOR: ssl: EVP_PKEY must be freed after X509_get_pubkey usage
- MINOR: proto_http.c 502 error txt typo.
- DOC: add deprecation notice to "block"
- BUG/MINOR: Reset errno variable before calling strtol(3)

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- BUG/MEDIUM: proxy: return "none" and "unknown" for unknown LB algos
- BUG/MINOR: stats: make field_str() return an empty string on NULL
- DOC: Spelling fixes
- BUG/MEDIUM: http: Fix tunnel mode when the CONNECT method is used
- BUG/MINOR: http: Keep the same behavior between 1.6 and 1.7 for tunneled txn
- BUG/MINOR: filters: Protect args in macros HAS_DATA_FILTERS and IS_DATA_FILTER
- BUG/MINOR: filters: Invert evaluation order of HTTP_XFER_BODY and XFER_DATA analyzers
- BUG/MINOR: http: Call XFER_DATA analyzer when HTTP txn is switched in tunnel mode
- BUG/MAJOR: stream: fix session abort on resource shortage
- BUG/MINOR: cli: allow the backslash to be escaped on the CLI
- BUG/MEDIUM: cli: fix "show stat resolvers" and "show tls-keys"
- DOC: Fix map table's format
- DOC: Added 51Degrees conv and fetch functions to documentation.
- BUG/MINOR: http: don't send an extra CRLF after a Set-Cookie in a redirect
- DOC: mention that req_tot is for both frontends and backends
- BUG/MEDIUM: variables: some variable name can hide another ones
- BUG/MINOR: stats: fix be/sessions/max output in html stats
- MINOR: proxy: Add fe_name/be_name fetchers next to existing fe_id/be_id
- DOC: lua: Documentation about some entry missing
- MINOR: Do not forward the header "Expect: 100-continue" when the option http-buffer-request is set
- DOC: Add undocumented argument of the trace filter
- DOC: Fix some typo in SPOE documentation
- BUG/MINOR: cli: be sure to always warn the cli applet when input buffer is full
- MINOR: applet: Count number of (active) applets
- MINOR: task: Rename run_queue and run_queue_cur counters
- BUG/MEDIUM: stream: Save unprocessed events for a stream
- BUG/MAJOR: Fix how the list of entities waiting for a buffer is handled
- BUILD/MEDIUM: Fixing the build using LibreSSL

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- SCRIPTS: make publish-release also copy the new SPOE doc
- BUILD: http: include types/sample.h in proto_http.h
- BUILD: debug/flags: remove test for SF_COMP_READY
- CONTRIB: debug/flags: add check for SF_ERR_CHK_PORT
- MINOR: lua: add function which return true if the channel is full.
- MINOR: lua: add ip addresses and network manipulation function
- CONTRIB: tcploop: scriptable TCP I/O for debugging purposes
- CONTRIB: tcploop: implement fork()
- CONTRIB: tcploop: implement logging when called with -v
- CONTRIB: tcploop: update the usage output
- CONTRIB: tcploop: support sending plain strings
- CONTRIB: tcploop: don't report failed send() or recv()
- CONTRIB: tcploop: add basic loops via a jump instruction
- BUG/MEDIUM: channel: bad unlikely macro
- CLEANUP: lua: move comment
- CLEANUP: lua: control executed twice
- BUG/MEDIUM: ssl: Store certificate filename in a variable
- BUG/MINOR: ssl: Print correct filename when error occurs reading OCSP
- CLEANUP: ssl: Remove goto after return dead code
- CLEANUP: ssl: Fix bind keywords name in comments
- DOC: ssl: Use correct wording for ca-sign-pass
- CLEANUP: lua: avoid directly calling getsockname/getpeername()
- BUG/MINOR: stick-table: handle out-of-memory condition gracefully
- MINOR: cli: add private pointer and release function
- MEDIUM: lua: Add cli handler for Lua
- BUG/MEDIUM: connection: check the control layer before stopping polling
- DEBUG: connection: mark the closed FDs with a value that is easier to detect
- BUG/MEDIUM: stick-table: fix regression caused by recent fix for out-of-memory
- BUG/MINOR: cli: properly decrement ref count on tables during failed dumps
- BUG/MEDIUM: lua: In some case, the return of sample-fetche is ignored
- MINOR: filters: Add check_timeouts callback to handle timers expiration on streams
- MINOR: spoe: Add 'timeout processing' option to limit time to process an event
- MINOR: spoe: Remove useless 'timeout ack' option
- MINOR: spoe: Add 'option continue-on-error' statement in spoe-agent section
- MINOR: spoe: Add "maxconnrate" and "maxerrrate" statements
- MINOR: spoe: Add "option set-on-error" statement
- MINOR: stats: correct documentation of process ID for typed output
- BUILD: contrib: fix ip6range build on Centos 7
- BUILD: fix build on Solaris 10/11
- BUG/MINOR: cli: fix pointer size when reporting data/transport layer name
- BUG/MINOR: cli: dequeue from the proxy when changing a maxconn
- BUG/MINOR: cli: wake up the CLI's task after a timeout update
- MINOR: connection: add a few functions to report the data and xprt layers' names
- MINOR: connection: add names for transport and data layers
- REORG: cli: split dumpstats.c in src/cli.c and src/stats.c
- REORG: cli: split dumpstats.h in stats.h and cli.h
- REORG: cli: move ssl CLI functions to ssl_sock.c
- REORG: cli: move map and acl code to map.c
- REORG: cli: move show stat resolvers to dns.c
- MINOR: cli: create new function cli_has_level() to validate permissions
- MINOR: server: create new function cli_find_server() to find a server
- MINOR: proxy: create new function cli_find_frontend() to find a frontend
- REORG: cli: move 'set server' to server.c
- REORG: cli: move 'show pools' to memory.c
- REORG: cli: move 'show servers' to proxy.c
- REORG: cli: move 'show sess' to stream.c
- REORG: cli: move 'show backend' to proxy.c
- REORG: cli: move get/set weight to server.c
- REORG: cli: move "show stat" to stats.c
- REORG: cli: move "show info" to stats.c
- REORG: cli: move dump_text(), dump_text_line(), and dump_binary() to standard.c
- REORG: cli: move table dump/clear/set to stick_table.c
- REORG: cli: move "show errors" out of cli.c
- REORG: cli: make "show env" also use the generic keyword registration
- REORG: cli: move "set timeout" to its own handler
- REORG: cli: move "clear counters" to stats.c
- REORG: cli: move "set maxconn global" to its own handler
- REORG: cli: move "set maxconn server" to server.c
- REORG: cli: move "set maxconn frontend" to proxy.c
- REORG: cli: move "shutdown sessions server" to stream.c
- REORG: cli: move "shutdown session" to stream.c
- REORG: cli: move "shutdown frontend" to proxy.c
- REORG: cli: move "{enable|disable} frontend" to proxy.c
- REORG: cli: move "{enable|disable} server" to server.c
- REORG: cli: move "{enable|disable} health" to server.c
- REORG: cli: move "{enable|disable} agent" to server.c
- REORG: cli: move the "set rate-limit" functions to their own parser
- CLEANUP: cli: rename STAT_CLI_* to CLI_ST_*
- CLEANUP: cli: simplify the request parser a little bit
- CLEANUP: cli: remove assignments to st0 and st2 in keyword parsers
- BUILD: server: remove a build warning introduced by latest series
- BUG/MINOR: log-format: uncatched memory allocation functions
- CLEANUP: log-format: useless file and line in json converter
- CLEANUP/MINOR: log-format: unexport functions parse_logformat_var_args() and parse_logformat_var()
- CLEANUP: log-format: fix return code of the function parse_logformat_var()
- CLEANUP: log-format: fix return code of function parse_logformat_var_args()
- CLEANUP: log-format: remove unused arguments
- MEDIUM: log-format: strict parsing and enable fail
- MEDIUM: log-format/conf: take into account the parse_logformat_string() return code
- BUILD: ssl: make the SSL layer build again with openssl 0.9.8
- BUILD: vars: remove a build warning on vars.c
- MINOR: lua: add utility function for check boolean argument
- MINOR: lua: Add tokenize function.
- BUG/MINOR: conf: calloc untested
- MINOR: http/conf: store the use_backend configuration file and line for logs
- MEDIUM: log-format: Use standard HAProxy log system to report errors
- CLEANUP: sample: report "converter" instead of "conv method" in error messages
- BUG: spoe: Fix parsing of SPOE actions in ACK frames
- MINOR: cli: make "show stat" support a proxy name
- MINOR: cli: make "show errors" support a proxy name
- MINOR: cli: make "show errors" capable of dumping only request or response
- BUG/MINOR: freq-ctr: make swrate_add() support larger values
- CLEANUP: counters: move from 3 types to 2 types
- CLEANUP: cfgparse: cascade the warnif_misplaced_* rules
- REORG: tcp-rules: move tcp rules processing to their own file
- REORG: stkctr: move all the stick counters processing to stick-tables.c
- DOC: update the roadmap file with the latest changes