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

%define lua_ver           5.3.5
%define pcre_ver          8.43
%define openssl_ver       1.1.1d
%define ncurses_ver       6.1
%define readline_ver      8.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.0.7
Release:           0%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           http://www.haproxy.org/download/2.0/src/%{name}-%{version}.tar.gz
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

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make zlib-devel
BuildRequires:     devtoolset-3-gcc-c++ devtoolset-3-binutils

Requires:          setup >= 2.8.14-14 kaosv >= 2.15

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

tar xzvf %{SOURCE10}
tar xzvf %{SOURCE11}
tar xzvf %{SOURCE12}
tar xzvf %{SOURCE13}
tar xzvf %{SOURCE14}

%build

# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-3/root/usr/bin:$PATH"

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
  %{__service} %{name} stop &>/dev/null || :
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
