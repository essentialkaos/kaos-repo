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
%define openssl_ver       1.1.1c
%define ncurses_ver       6.1
%define readline_ver      8.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.9.8
Release:           0%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           http://www.haproxy.org/download/1.9/src/%{name}-%{version}.tar.gz
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
* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.8-0
- BUG/MEDIUM: mux-h2: properly deal with too large headers frames
- BUG/MINOR: http: Call stream_inc_be_http_req_ctr() only one time per request
- BUG/MEDIUM: spoe: arg len encoded in previous frag frame but len changed
- MINOR: spoe: Use the sample context to pass frag_ctx info during encoding
- DOC: contrib/modsecurity: Typos and fix the reject example
- BUG/MEDIUM: contrib/modsecurity: If host header is NULL, don't try to strdup
  it
- BUG/MAJOR: map/acl: real fix segfault during show map/acl on CLI
- MINOR: examples: Use right locale for the last changelog date in haproxy.spec
- BUG/MEDIUM: listener: Fix how unlimited number of consecutive accepts is
  handled
- MINOR: config: Test validity of tune.maxaccept during the config parsing
- CLEANUP: config: Don't alter listener->maxaccept when nbproc is set to 1
- MINOR: threads: Implement HA_ATOMIC_LOAD().
- BUG/MEDIUM: port_range: Make the ring buffer lock-free.
- BUG/MEDIUM: servers: fix typo "src" instead of "srv"
- BUG/MINOR: haproxy: fix rule->file memory leak
- BUG/MINOR: log: properly free memory on logformat parse error and deinit()
- BUG/MINOR: checks: free memory allocated for tasklets
- BUG/MEDIUM: pattern: fix memory leak in regex pattern functions
- BUG/MEDIUM: channels: Don't forget to reset output in channel_erase().
- BUG/MEDIUM: connections: Make sure we remove CO_FL_SESS_IDLE on disown.
- BUG/MEDIUM: ssl: Use the early_data API the right way.
- BUG/MEDIUM: streams: Don't add CF_WRITE_ERROR if early data were rejected.
- BUG/MEDIUM: checks: make sure the warmup task takes the server lock
- CLEANUP: task: report calls as unsigned in show sess
- BUG/MINOR: activity: always initialize the profiling variable
- MINOR: connection: make the debugging helper functions safer
- BUG/MINOR: logs/threads: properly split the log area upon startup
- DOC: Fix typo in keyword matrix
- BUG/MEDIUM: ssl: Don't attempt to use early data with libressl.
- MINOR: doc: Document allow-0rtt on the server line.
- BUG/MEDIUM: h2: Revamp the way send subscriptions works.
- BUG/MINOR: mux-h2: rely on trailers output not input to turn them to empty
  data
- BUG/MEDIUM: h2/htx: always fail on too large trailers
- MEDIUM: mux-h2: discard contents that are to be sent after a shutdown
- BUG/MEDIUM: mux-h2/htx: never wait for EOM when processing trailers
- BUG/MEDIUM: h2/htx: never leave a trailers block alone with no EOM block
- BUG/MINOR: mworker/ssl: close OpenSSL FDs on reload
- BUG/MINOR: mux-h2: fix the condition to close a cs-less h2s on the backend
- BUG/MEDIUM: spoe: Be sure the sample is found before setting its context
- BUG/MINOR: mux-h1: Fix the parsing of trailers
- BUG/MINOR: htx: Never transfer more than expected in htx_xfer_blks()
- MINOR: htx: Split on DATA blocks only when blocks are moved to an HTX message
- BUG/MEDIUM: h2: Make sure we set send_list to NULL in h2_detach().
- BUILD: ssl: fix again a libressl build failure after the openssl FD leak fix
- BUG/MINOR: stream: Attach the read side on the response as soon as possible
- BUG/MEDIUM: http: Use pointer to the begining of input to parse message
  headers
- BUG/MEDIUM: h2: Don't check send_wait to know if we're in the send_list.
- BUILD: threads: Add __ha_cas_dw fallback for single threaded builds
- BUILD: threads: fix again the __ha_cas_dw() definition
- BUG/MAJOR: mux-h2: do not add a stream twice to the send list
- BUG/MINOR: htx: make sure to always initialize the HTTP method when parsing
  a buffer
- MINOR: spoe: Set the argument chunk size to 0 when SPOE variables are checked
- BUG/MINOR: vars: Fix memory leak in vars_check_arg

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.7-0
- BUILD: makefile: work around an old bug in GNU make-3.80
- BUILD: http: properly mark some struct as extern
- BUILD: chunk: properly declare pool_head_trash as extern
- BUILD: cache: avoid a build warning with some compilers/linkers
- MINOR: tools: make memvprintf() never pass a NULL target to vsnprintf()
- BUILD: re-implement an initcall variant without using executable sections
- BUILD: makefile: fix build of IPv6 header on aix51
- BUILD: makefile: add _LINUX_SOURCE_COMPAT to build on AIX-51
- BUILD: Makefile: disable shared cache on AIX 5.1
- BUG/MINOR: cli: correctly handle abns in 'show cli sockets'
- MINOR: cli: start addresses by a prefix in 'show cli sockets'
- BUG/MINOR: htx: Preserve empty HTX messages with an unprocessed parsing error
- BUG/MEDIUM: peers: fix a case where peer session is not cleanly reset on
  release.
- BUILD: fix backport of initcall variant
- BUILD: use inttypes.h instead of stdint.h
- BUILD: connection: fix naming of ip_v field
- BUG/MEDIUM: h2: Don't attempt to recv from h2_process_demux if we subscribed.
- BUG/MEDIUM: htx: fix random premature abort of data transfers
- BUG/MEDIUM: streams: Don't remove the SI_FL_ERR flag in si_update_both().
- BUG/MEDIUM: streams: Store prev_state before calling si_update_both().
- BUG/MEDIUM: stream: Don't clear the stream_interface flags in si_update_both.
- BUG/MEDIUM: pattern: assign pattern IDs after checking the config validity
- BUG/MEDIUM: streams: Only re-run process_stream if we're in a connected state.
- BUG/MEDIUM: stream_interface: Don't bother doing chk_rcv/snd if not connected.
- BUG/MEDIUM: task/threads: address a fairness issue between local and global
  tasks
- BUG/MINOR: tasks: make sure the first task to be queued keeps its nice value
- BUG/MEDIUM: spoe: Queue message only if no SPOE applet is attached to the
  stream
- BUG/MEDIUM: spoe: Return an error if nothing is encoded for fragmented
  messages
- BUG/MINOR: spoe: Be sure to set tv_request when each message fragment is
  encoded
- BUG/MEDIUM: htx: Defrag if blocks position is changed and the payloads wrap
- BUG/MEDIUM: htx: Don't crush blocks payload when append is done on a data
  block
- MEDIUM: htx: Deprecate the option 'http-tunnel' and ignore it in HTX
- MINOR: proto_htx: Don't adjust transaction mode anymore in HTX analyzers
- BUG/MEDIUM: htx: Fix the process of HTTP CONNECT with h2 connections
- MINOR: mux-h1: Simplify handling of 1xx responses
- BUG/MINOR: mux-h1: Handle the flag CS_FL_KILL_CONN during a shutdown
  read/write
- BUG/MEDIUM: map: Fix memory leak in the map converter
- BUG/MINOR: ssl: Fix 48 byte TLS ticket key rotation
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
- MINOR: initcall: Don't forget to define the __start/stop_init_##stg symbols.
- MINOR: skip get_gmtime where tm is unused
- BUG/MEDIUM: h2: Make sure we're not already in the send_list in
  h2_subscribe().
- BUILD: htx: fix a used uninitialized warning on is_cookie2
- BUG/MAJOR: lb/threads: fix insufficient locking on round-robin LB
- BUG/MINOR: mworker: don't exit with an ambiguous value
- BUG/MINOR: mworker: ensure that we still quits with SIGINT
- BUG/MINOR: mux-h1: Process input even if the input buffer is empty
- BUG/MINOR: mux-h1: Don't switch the parser in busy mode if other side has done
- BUG/MEDIUM: mux-h1: Notify the stream waiting for TCP splicing if ibuf is
  empty
- BUG/MEDIUM: mux-h1: Enable TCP splicing to exchange data only
- MINOR: mux-h1: Handle read0 during TCP splicing
- BUG/MEDIUM: htx: Don't return the start-line if the HTX message is empty
- BUG/MAJOR: http_fetch: Get the channel depending on the keyword used
- BUG/MINOR: http_fetch/htx: Allow permissive sample prefetch for the HTX
- MEDIUM: tasks: improve fairness between the local and global queues
- BUILD: task/thread: fix single-threaded build of task.c
- MEDIUM: tasks: only base the nice offset on the run queue depth
- MINOR: tasks: restore the lower latency scheduling when niced tasks are
  present
- BUG/MEDIUM: tasks: Make sure we set TASK_QUEUED before adding a task to the
  rq.
- BUG/MEDIUM: tasks: Make sure we modify global_tasks_mask with the rq_lock.
- MINOR: tasks: Don't consider we can wake task with tasklet_wakeup().
- MEDIUM: tasks: No longer use rq.node.leaf_p as a lock.
- MINOR: tasks: Don't set the TASK_RUNNING flag when adding in the tasklet list.
- BUG/MAJOR: task: make sure never to delete a queued task
- BUG/MEDIUM: applets: Don't use task_in_rq().
- REGTESTS: exclude tests that require ssl, pcre if no such feature is enabled
- BUG/MINOR: mworker: disable busy polling in the master process
- BUG/MEDIUM: maps: only try to parse the default value when it's present
- BUG/MINOR: acl: properly detect pattern type SMP_T_ADDR
- MINOR: peers: Add a new command to the CLI for peers.
- DOC: update for "show peers" CLI command.
- MINOR: peers: adds counters on show peers about tasks calls.
- MINOR: init: add a "set-dumpable" global directive to enable core dumps
- BUG/MEDIUM: h1: Don't parse chunks CRLF if not enough data are available
- BUG/MEDIUM: thread/http: Add missing locks in set-map and add-acl HTTP rules
- BUG/MEDIUM: stream: Don't request a server connection if a shutw was scheduled
- BUG/MINOR: 51d: Get the request channel to call CHECK_HTTP_MESSAGE_FIRST()
- BUG/MINOR: da: Get the request channel to call CHECK_HTTP_MESSAGE_FIRST()
- MINOR: ssl/cli: async fd io-handlers printable on show fd
- BUG/MEDIUM: stream: Fix the way early aborts on the client side are handled
- BUG/MINOR: spoe: Don't systematically wakeup SPOE stream in the applet handler
- BUG/MAJOR: lb/threads: fix AB/BA locking issue in round-robin LB
- BUILD: wurfl: build fix for 1.9/2.0 code base
- MINOR: wurfl: enabled multithreading mode
- DOC: wurfl: added point of contact in MAINTAINERS file
- BUG/MAJOR: muxes: Use the HTX mode to find the best mux for HTTP proxies only
- BUG/MINOR: htx: Exclude TCP proxies when the HTX mode is handled during
  startup

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.6-0
- BUG/MEDIUM: mux-h2: Make sure we destroyed the h2s once shutr/shutw is done.
- BUG/MEDIUM: mux-h2: Don't bother keeping the h2s if detaching and nothing
  to send.
- BUG/MEDIUM: mux-h2: Use the right list in h2_stop_senders().
- BUG/MINOR: cache: Fully consume large requests in the cache applet
- BUG/MINOR: stats: Fully consume large requests in the stats applet
- BUG/MEDIUM: lua: Fully consume large requests when an HTTP applet ends
- BUG/MINOR: doc: Be accurate on the behavior on pool-purge-delay.
- BUG/MEDIUM: ssl: ability to set TLS 1.3 ciphers using
  ssl-default-server-ciphersuites
- MINOR: mux-h2: copy small data blocks more often and reduce the number of
  pauses
- BUG/MINOR: log: properly format IPv6 address when LOG_OPT_HEXA modifier is
  used.
- MINOR: lists: add a LIST_DEL_INIT() macro
- BUG/MEDIUM: h2: Try to be fair when sending data.
- BUG/MINOR: proto-http: Don't forward request body anymore on error
- MINOR: mux-h2: Remove useless test on ES flag in h2_frt_transfer_data()
- MINOR: connection: and new flag to mark end of input (EOI)
- MINOR: channel: Report EOI on the input channel if it was reached in the mux
- CONTRIB: debug: report the CS and CF's EOI flags
- MEDIUM: mux-h2: Don't mix the end of the message with the end of stream
- BUG/MEDIUM: mux-h2: make sure to always notify streams of EOS condition
- MINOR: mux-h1: Set CS_FL_EOI the end of the message is reached
- BUG/MEDIUM: http/htx: Fix handling of the option abortonclose
- CLEANUP: muxes/stream-int: Remove flags CS_FL_READ_NULL and SI_FL_READ_NULL
- BUG/MEDIUM: h2: only destroy the h2s if h2s->cs is NULL.
- BUG/MEDIUM: h2: Use the new sending_list in h2s_notify_send().
- BUG/MEDIUM: h2: Follow the same logic in h2_deferred_shut than in h2_snd_buf.
- BUG/MEDIUM: h2: Remove the tasklet from the task list if unsubscribing.
- BUG/MEDIUM: task/h2: add an idempotent task removal fucntion
- REGTEST: Enable again reg tests with HEAD HTTP method usage.
- DOC: The option httplog is no longer valid in a backend.
- REGTEST: remove unexpected "nbthread" statement from Lua test cases
- BUG/MINOR: mux-h1: Only skip invalid C-L headers on output
- BUG/MEDIUM: mworker: don't free the wrong child when not found
- BUG/MEDIUM: checks: Don't bother subscribing if we have a connection error.
- BUG/MAJOR: checks: segfault during tcpcheck_main

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.5-0
- DOC: ssl: Clarify when pre TLSv1.3 cipher can be used
- DOC: ssl: Stop documenting ciphers example to use
- BUG/MINOR: spoe: do not assume agent->rt is valid on exit
- BUG/MINOR: lua: initialize the correct idle conn lists for the SSL sockets
- BUG/MEDIUM: spoe: initialization depending on nbthread must be done last
- BUG/MEDIUM: server: initialize the idle conns list after parsing the config
- CLEANUP: server: fix indentation mess on idle connections
- BUG/MEDIUM: server: initialize the orphaned conns lists and tasks at the end
- BUG/MAJOR: spoe: Don't try to get agent config during SPOP healthcheck
- BUG/MINOR: config: Reinforce validity check when a process number is parsed
- BUG/MINOR: mux-h1: verify the request's version before dropping connection:
  keep-alive
- BUG: 51d: In Hash Trie, multi header matching was affected by the header
  names stored globaly.
- BUG/MAJOR: stream: avoid double free on unique_id
- BUILD/MINOR: stream: avoid a build warning with threads disabled
- BUILD/MINOR: tools: fix build warning in the date conversion functions
- BUILD/MINOR: peers: remove an impossible null test in intencode()
- BUILD/MINOR: htx: fix some potential null-deref warnings with http_find_stline
- BUG/MEDIUM: http_fetch: fix the "base" and "base32" fetch methods in HTX mode
- BUG/MEDIUM: proto_htx: Fix data size update if end of the cookie is removed
- BUG/MEDIUM: http_fetch: fix "req.body_len" and "req.body_size" fetch methods
  in HTX mode
- BUILD/MEDIUM: initcall: Fix build on MacOS.
- BUG/MEDIUM: mux-h2/htx: Always set CS flags before exiting h2_rcv_buf()
- MINOR: h2/htx: Set the flag HTX_SL_F_BODYLESS for messages without body
- BUG/MINOR: mux-h1: Add "transfer-encoding" header on outgoing requests if
  needed
- BUG/MINOR: mux-h2: Don't add ":status" pseudo-header on trailers
- BUG/MINOR: proto-htx: Consider a XFER_LEN message as chunked by default
- BUG/MEDIUM: h2/htx: Correctly handle interim responses when HTX is enabled
- MINOR: mux-h2: Set HTX extra value when possible
- BUG/MEDIUM: htx: count the amount of copied data towards the final count
- BUG/MEDIUM: mux-h2/htx: send an empty DATA frame on empty HTX trailers
- BUG/MEDIUM: servers: Use atomic operations when handling curr_idle_conns.
- BUG/MEDIUM: servers: Add a per-thread counter of idle connections.
- BUG/MAJOR: fd/threads, task/threads: ensure all spin locks are unlocked
- BUG/MAJOR: listener: Make sure the listener exist before using it.
- BUG/MEDIUM: mux-h1: Report the right amount of data xferred in h1_rcv_buf()
- BUG/MINOR: channel: Set CF_WROTE_DATA when outgoing data are skipped
- MINOR: htx: Add function to drain data from an HTX message
- MINOR: channel/htx: Add function to skips output bytes from an HTX channel
- BUG/MAJOR: cache/htx: Set the start-line offset when a cached object is served
- BUG/MEDIUM: cache: Get objects from the cache only for GET and HEAD requests
- BUG/MINOR: cache/htx: Return only the headers of cached objects to HEAD
  requests
- BUG/MINOR: mux-h1: Always initilize h1m variable in h1_process_input()
- BUG/MEDIUM: proto_htx: Fix functions applying regex filters on HTX messages
- BUG/MEDIUM: h2: advertise to servers that we don't support push
- BUG/MINOR: listener: keep accept rate counters accurate under saturation
- MINOR: global: keep a copy of the initial rlim_fd_cur and rlim_fd_max values
- BUG/MINOR: init: never lower rlim_fd_max
- BUG/MINOR: checks: make external-checks restore the original rlim_fd_cur/max
- BUG/MINOR: mworker: be careful to restore the original rlim_fd_cur/max on
  reload
- BUG/MAJOR: mux-h2: fix race condition between close on both ends
- MINOR: htx: unconditionally handle parsing errors in requests or responses
- MINOR: mux-h2: always pass HTX_FL_PARSING_ERROR between h2s and buf on RX
- BUG/MEDIUM: h2/htx: verify that :path doesn't contain invalid chars
- BUG/MEDIUM: logs: Only attempt to free startup_logs once.
- BUG/MEDIUM: 51d: fix possible segfault on deinit_51degrees()
- BUG/MINOR: ssl: fix warning about ssl-min/max-ver support
- MINOR: fd: Remove debugging code.
- BUG/MEDIUM: listeners: Don't call fd_stop_recv() if fd_updt is NULL.
- MEDIUM: threads: Use __ATOMIC_SEQ_CST when using the newer atomic API.
- DOC: Remove tabs and fixed punctuation.
- BUG/MAJOR: tasks: Use the TASK_GLOBAL flag to know if we're in the global rq.
- BUG/MEDIUM: threads/fd: do not forget to take into account epoll_fd/pipes
- BUG/MEDIUM: tasks: Make sure we wake sleeping threads if needed.
- BUG/MINOR: mux-h1: Don't report an error on EOS if no message was received
- BUG/MINOR: stats/htx: Call channel_add_input() when response headers are sent
- BUG/MINOR: lua/htx: Use channel_add_input() when response data are added
- BUG/MINOR: lua/htx: Don't forget to call htx_to_buf() when appropriate
- MINOR: stats: Add the status code STAT_STATUS_IVAL to handle invalid requests
- MINOR: stats: Move stuff about the stats status codes in stats files
- BUG/MINOR: stats: Be more strict on what is a valid request to the stats
  applet
- BUG/MAJOR: spoe: Fix initialization of thread-dependent fields
- MINOR: cfgparse: Add a cast to make gcc happier.
- REGTEST: fix a spurious "nbthread 4" in the connection test
- BUILD: Makefile: allow the reg-tests target to be verbose
- BUILD: Makefile: resolve LEVEL before calling run-regtests
- BUG/MAJOR: stats: Fix how huge POST data are read from the channel
- BUG/MINOR: http/counters: fix missing increment of fe->srv_aborts
- BUG/MEDIUM: mux-h2: Always wakeup streams with no id to avoid frozen streams
- MINOR: mux-h2: Set REFUSED_STREAM error to reset a stream if no data was
  never sent
- MINOR: muxes: Report the Last read with a dedicated flag
- MINOR: proto-http/proto-htx: Make error handling clearer during data
  forwarding

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- BUG/MEDIUM: mux-h1: Don't add "transfer-encoding" if message-body is forbidden
- BUG/MEDIUM: compression: Rewrite strong ETags
- DOC: compression: Update the reasons for disabled compression
- BUG/MINOR: deinit: tcp_rep.inspect_rules not deinit, add to deinit
- DOC: add a missing space in the documentation for bc_http_major
- SCRIPTS: add the issue tracker URL to the announce script
- BUG/MEDIUM: connections: Don't forget to remove CO_FL_SESS_IDLE.
- BUG/MINOR: server: fix logic flaw in idle connection list management
- BUG/MINOR: stream: don't close the front connection when facing a backend
  error
- MINOR: xref: Add missing barriers.
- BUG/MEDIUM: peers: Handle mux creation failure.
- BUG/MEDIUM: checks: Check that conn_install_mux succeeded.
- BUG/MEDIUM: servers: Only destroy a conn_stream we just allocated.
- BUG/MEDIUM: servers: Don't add an incomplete conn to the server idle list.
- BUG/MEDIUM: checks: Don't try to set ALPN if connection failed.
- BUG/MEDIUM: h2: In h2_send(), stop the loop if we failed to alloc a buf.
- BUG/MEDIUM: servers: Close the connection if we failed to install the mux.
- BUG/MEDIUM: buffer: Make sure b_is_null handles buffers waiting for
  allocation.
- DOC: htx: make it clear that htxbuf() and htx_from_buf() always return valid
  pointers
- MINOR: htx: never check for null htx pointer in htx_is_{,not_}empty()
- MEDIUM: stream-int: always mark pending outgoing SI_ST_CON
- MINOR: stream: don't wait before retrying after a failed connection reuse
- MEDIUM: h2: always parse and deduplicate the content-length header
- BUG/MINOR: mux-h2: always compare content-length to the sum of DATA frames
- BUG/MEDIUM: mux-h2: only close connection on request frames on closed streams
- BUG/MEDIUM: mux-h2: wake up flow-controlled streams on initial window update
- BUG/MEDIUM: mux-h2: fix two half-closed to closed transitions
- BUG/MEDIUM: mux-h2: make sure never to send GOAWAY on too old streams
- BUG/MEDIUM: mux-h2: do not abort HEADERS frame before decoding them
- BUG/MINOR: mux-h2: make sure response HEADERS are not received in other
  states than OPEN and HLOC
- MINOR: h2: add a generic frame checker
- MEDIUM: mux-h2: check the frame validity before considering the stream state
- CLEANUP: mux-h2: remove misleading leftover test on h2s' nullity
- CLEANUP: mux-h2: clean the stream error path on HEADERS frame processing
- CLEANUP: mux-h2: remove stream ID and frame length checks from the frame
  parsers
- BUG/MINOR: mux-h2: make sure request trailers on aborted streams don't break
  the connection
- MINOR: mux-h2: consistently rely on the htx variable to detect the mode
- BUG/MEDIUM: mux-h2: wait for the mux buffer to be empty before closing
  the connection
- MINOR: stream-int: add a new flag to mention that we want the connection to
  be killed
- MINOR: connstream: have a new flag CS_FL_KILL_CONN to kill a connection
- BUG/MEDIUM: mux-h2: do not close the connection on aborted streams
- MINOR: mux-h2: max-concurrent-streams should be unsigned
- MINOR: mux-h2: make sure to only check concurrency limit on the frontend
- MINOR: mux-h2: learn and store the peer's advertised MAX_CONCURRENT_STREAMS
  setting
- BUG/MEDIUM: mux-h2: properly consider the peer's advertised
  max-concurrent-streams
- BUG/MEDIUM: backend: always release the previous connection into its own
  target srv_list
- BUG/MEDIUM: htx: check the HTX compatibility in dynamic use-backend rules
- BUG/MINOR: backend: check srv_conn before dereferencing it
- BUG/MEDIUM: mux-h2: always omit :scheme and :path for the CONNECT method
- BUG/MEDIUM: mux-h2: always set :authority on request output
- BUG/MEDIUM: stream: Don't forget to free s->unique_id in stream_free().
- BUG/MINOR: config: fix bind line thread mask validation
- BUG/MINOR: compression: properly report compression stats in HTX mode
- BUG/MINOR: task: close a tiny race in the inter-thread wakeup
- BUG/MAJOR: config: verify that targets of track-sc and stick rules are present
- BUG/MAJOR: spoe: verify that backends used by SPOE cover all their callers'
  processes
- MINOR: backend: move url_param_name/len to lbprm.arg_str/len
- MINOR: backend: make headers and RDP cookie also use arg_str/len
- MINOR: backend: add new fields in lbprm to store more LB options
- MINOR: backend: make the header hash use arg_opt1 for use_domain_only
- MINOR: backend: remap the balance uri settings to lbprm.arg_opt{1,2,3}
- MINOR: backend: move hash_balance_factor out of chash
- MEDIUM: backend: move all LB algo parameters into an union
- BUG/MAJOR: htx/backend: Make all tests on HTTP messages compatible with HTX
- BUG/MINOR: config: make sure to count the error on incorrect track-sc/stick
  rules

* Tue Jul 02 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- REGTEST: checks basic stats webpage functionality
- BUG/MEDIUM: checks: fix recent regression on agent-check making it crash
- BUG/MEDIUM: servers: Make assign_tproxy_address work when ALPN is set.
- BUG/MEDIUM: connections: Add the CO_FL_CONNECTED flag if a send succeeded.
- BUG/MINOR: startup: certain goto paths in init_pollers fail to free
- BUG/MINOR: server: don't always trust srv_check_health when loading a
  server state
- BUG/MINOR: check: Wake the check task if the check is finished in
  wake_srv_chk()
- BUG/MEDIUM: ssl: Fix handling of TLS 1.3 KeyUpdate messages
- DOC: mention the effect of nf_conntrack_tcp_loose on src/dst
- BUG/MINOR: proto-htx: Return an error if all headers cannot be received at
  once
- BUG/MEDIUM: mux-h2/htx: Respect the channel's reserve
- BUG/MINOR: mux-h1: Apply the reserve on the channel's buffer only
- BUG/MINOR: mux-h1: avoid copying output over itself in zero-copy
- BUG/MAJOR: mux-h2: don't destroy the stream on failed allocation in
  h2_snd_buf()
- BUG/MEDIUM: backend: also remove from idle list muxes that have no more room
- BUG/MEDIUM: mux-h2: properly abort on trailers decoding errors
- MINOR: h2: declare new sets of frame types
- BUG/MINOR: mux-h2: CONTINUATION in closed state must always return GOAWAY
- BUG/MINOR: mux-h2: headers-type frames in HREM are always a connection error
- BUG/MINOR: mux-h2: make it possible to set the error code on an already closed
  stream
- BUG/MINOR: hpack: return a compression error on invalid table size updates
- MINOR: server: make sure pool-max-conn is >= -1
- BUG/MINOR: stream: take care of synchronous errors when trying to send
- BUG/MINOR: mux-h2: always check the stream ID limit in h2_avail_streams()
- BUG/MINOR: mux-h2: refuse to allocate a stream with too high an ID
- BUG/MEDIUM: backend: never try to attach to a mux having no more stream
  available
- MINOR: server: add a max-reuse parameter
- MINOR: mux-h2: always consider a server's max-reuse parameter
- DOC: nbthread is no longer experimental.
- BUG/MINOR: listener: always fill the source address for accepted socketpairs
- BUG/MINOR: mux-h2: do not report available outgoing streams after GOAWAY
- BUG/MINOR: spoe: corrected fragmentation string size
- BUG/MINOR: task: fix possibly missed event in inter-thread wakeups
- BUG/MEDIUM: servers: Attempt to reuse an unfinished connection on retry.
- BUG/MEDIUM: backend: always call si_detach_endpoint() on async connection
  failure

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- BUG/MAJOR: cache: fix confusion between zero and uninitialized cache key
- BUG/MEDIUM: h1: Make sure we destroy an inactive connectin that did shutw.
- MEDIUM: sessions: Keep track of which connections are idle.
- BUG/MEDIUM: init: Initialize idle_orphan_conns for first server in
  server-template
- BUG/MEDIUM: connection: properly unregister the mux on failed initialization
- MINOR: checks: Store the proxy in checks.
- BUG/MEDIUM: checks: Avoid having an associated server for email checks.
- BUG/MINOR: lua/htx: Respect the reserve when data are send from an HTX applet
- BUG/MEDIUM: ssl: Disable anti-replay protection and set max data with 0RTT.
- DOC: Be a bit more explicit about allow-0rtt security implications.
- BUG/MEDIUM: ssl: missing allocation failure checks loading tls key file
- BUG/MINOR: backend: don't use url_param_name as a hint for BE_LB_ALGO_PH
- BUG/MINOR: backend: balance uri specific options were lost across defaults
- BUG/MINOR: backend: BE_LB_LKUP_CHTREE is a value, not a bit
- REGTEST: "capture (request|response)" regtest.
- REGTEST: filters: add compression test
- REGTESTS: test case for map_regm commit 271022150d
- REGTESTS: Basic tests for concat,strcmp,word,field,ipmask converters
- REGTESTS: Basic tests for using maps to redirect requests / select backend
- DOC: REGTESTS README varnishtest -Dno-htx= define.
- REGTEST: Switch to vtest.
- REGTEST: Adapt reg test doc files to vtest.
- BUILD/MEDIUM: da: Necessary code changes for new buffer API.
- BUG/MINOR: base64: dec func ignores padding for output size checking
- MINOR: ssl: add support of aes256 bits ticket keys on file and cli.
- BUG/MINOR: stick_table: Prevent conn_cur from underflowing
- MINOR: spoe: Make the SPOE filter compatible with HTX proxies
- MINOR: h2: add a bit-based frame type representation
- MEDIUM: mux-h2: remove padlen during headers phase
- MINOR: mux-h2: remove useless check for empty frame length in
  h2s_decode_headers()
- MEDIUM: mux-h2: decode HEADERS frames before allocating the stream
- MINOR: mux-h2: make h2c_send_rst_stream() use the dummy stream's error code
- MINOR: mux-h2: add a new dummy stream for the REFUSED_STREAM error code
- MINOR: mux-h2: fail stream creation more cleanly using RST_STREAM
- MINOR: buffers: add a new b_move() function
- MINOR: mux-h2: make h2_peek_frame_hdr() support an offset
- MEDIUM: mux-h2: handle decoding of CONTINUATION frames
- BUG/MINOR: mux-h2: set the stream-full flag when leaving h2c_decode_headers()
- BUG/MINOR: mux-h2: mark end-of-stream after processing response HEADERS,
  not before
- BUG/MINOR: mux-h2: only update rxbuf's length for H1 headers
- MINOR: mux-h2: make h2c_decode_headers() return a status, not a count
- MINOR: mux-h2: add a new dummy stream : h2_error_stream
- MEDIUM: mux-h2: make h2c_decode_headers() support recoverable errors
- BUG/MINOR: mux-h2: detect when the HTX EOM block cannot be added after headers
- MINOR: mux-h2: check for too many streams only for idle streams
- MINOR: mux-h2: set H2_SF_HEADERS_RCVD when a HEADERS frame was decoded
- BUG/MEDIUM: mux-h2: decode trailers in HEADERS frames
- MINOR: h2: add h2_make_h1_trailers to turn H2 headers to H1 trailers
- MEDIUM: mux-h2: pass trailers to H1 (legacy mode)
- MINOR: htx: add a new function to add a block without filling it
- MINOR: h2: add h2_make_htx_trailers to turn H2 headers to HTX trailers
- MEDIUM: mux-h2: pass trailers to HTX
- MINOR: mux-h2: make HTX_BLK_EOM processing idempotent
- MINOR: h1: make the H1 headers block parser able to parse headers only
- BUG/MEDIUM: h1: Get the h1m state when restarting the headers parsing
- MEDIUM: mux-h2: emit HEADERS frames when facing HTX trailers blocks
- BUG: 51d: Changes to the buffer API in 1.9 were not applied to the 51Degrees
  code.
- BUG/MEDIUM: stats: Get the right scope pointer depending on HTX is used or not

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- BUG/MEDIUM: tasks: Decrement tasks_run_queue in tasklet_free().
- BUG/MEDIUM: log: don't mark log FDs as non-blocking on terminals
- BUG/MAJOR: stream-int: Update the stream expiration date in
  stream_int_notify()
- BUG/MAJOR: connections: Close the connection before freeing it.
- BUG/MEDIUM: h2: Don't forget to quit the sending_list if SUB_CALL_UNSUBSCRIBE.
- BUG/MEDIUM: mux-h2: Don't forget to quit the send list on error reports
- BUG/MEDIUM: mux-h2: don't needlessly wake up the demux on short frames
- MINOR: mux-h2: only increase the connection window with the first update
- REGTESTS: remove the expected window updates from H2 handshakes
- BUG/MINOR: mux-h2: make empty HEADERS frame return a connection error
- BUG/MEDIUM: mux-h2: mark that we have too many CS once we have more than
  the max
- BUG/MEDIUM: mux_h2: Don't add to the idle list if we're full.
- BUG/MEDIUM: mux-h2: always restart reading if data are available
- BUG/MINOR: mux-h2: don't check the CS count in h2c_bck_handle_headers()
- BUG/MEDIUM: dns: Don't prevent reading the last byte of the payload in
  dns_validate_response()
- BUG/MEDIUM: dns: overflowed dns name start position causing invalid dns error
- BUG/MINOR: compression/htx: Don't compress responses with unknown body length
- BUG/MINOR: compression/htx: Don't add the last block of data if it is empty
- BUG/MEDIUM: server: Also copy "check-sni" for server templates.
- BUG/MEDIUM: servers: Don't try to reuse connection if we switched server.
- BUG/MEDIUM: servers: Fail if we fail to allocate a conn_stream.
- BUG/MAJOR: servers: Use the list api correctly to avoid crashes.
- BUG/MAJOR: servers: Correctly use LIST_ELEM().
- BUG/MAJOR: sessions: Use an unlimited number of servers for the conn list.
- BUG/MEDIUM: servers: Flag the stream_interface on handshake error.
- MEDIUM: servers: Be smarter when switching connections.
- MINOR: channel: Add the function channel_add_input
- MINOR: stats/htx: Call channel_add_input instead of updating channel state by
  hand
- BUG/MEDIUM: cache: Be sure to end the forwarding when XFER length is unknown
- BUG/MAJOR: htx: Return the good block address after a defrag
- BUG/MEDIUM: mux-h1: use per-direction flags to indicate transitions
- BUG/MEDIUM: mux-h1: make HTX chunking consistent with H2
- MINOR: mux-h1: parse the content-length header on output and set H1_MF_CLEN
- BUG/MEDIUM: mux-h1: don't enforce chunked encoding on requests
- BUG/MEDIUM: mux-h1: Add a task to handle connection timeouts
- BUG/MEDIUM: proto-htx: Set SI_FL_NOHALF on server side when request is done
- BUG/MINOR: htx: send the proper authenticate header when using http-request
  auth
- MINOR: lb: allow redispatch when using consistent hash
- MINOR: ssl: Add ssl_sock_set_alpn().
- MEDIUM: checks: Add check-alpn.
- MEDIUM: mux_h1: Implement h1_show_fd.
- MINOR: payload: add sample fetch for TLS ALPN
- REGTEST: Require the option LUA to run lua tests
- REGTEST: script: Process script arguments before everything else
- REGTEST: script: Evaluate the varnishtest command to allow quoted parameters
- REGTEST: script: Add the option --clean to remove previous log direcotries
- REGTEST: script: Add the option --debug to show logs on standard ouput
- REGTEST: script: Add the option --keep-logs to keep all log directories
- REGTEST: script: Add the option --use-htx to enable the HTX in regtests
- REGTEST: script: Print only errors in the results report
- REGTEST: Add option to use HTX prefixed by the macro 'no-htx'
- REGTEST: Make reg-tests target support argument.
- REGTEST: Fix a typo about barrier type.
- REGTEST: Be less Linux specific with a syslog regex.
- REGTEST: Missing enclosing quotes for ${tmpdir} macro.
- REGTEST: Exclude freebsd target for some reg tests.
- REGTEST: script: Add support of alternatives in requited options list
- REGTEST: Add a basic test for the compression
- REGTEST: A basic test for "http-buffer-request"
- BUG/MINOR: cache/htx: Be sure to count partial trailers
- MINOR: stream/htx: Add info about the HTX structs in "show sess all" command
- MINOR: stream/htx: add the HTX flags output in "show sess all"
- MINOR: stream: Add the subscription events of SIs in "show sess all" command
- MINOR: stream/cli: fix the location of the waiting flag in "show sess all"
- MINOR: stream/cli: report more info about the HTTP messages on "show sess all"
- MINOR: mux-h1: Add the subscription events in "show fd" command
- BUG/MEDIUM: h1: In h1_init(), wake the tasklet instead of calling h1_recv().
- BUG/MEDIUM: server: Defer the mux init until after xprt has been initialized.
- BUG/MEDIUM: cli: make "show sess" really thread-safe
- BUG/MINOR: lua: bad args are returned for Lua actions
- BUG/MEDIUM: lua: dead lock when Lua tasks are trigerred
- MINOR: htx: Add an helper function to get the max space usable for a block
- MINOR: channel/htx: Add HTX version for some helper functions
- BUG/MEDIUM: cache/htx: Respect the reserve when cached objects are served
- BUG/MINOR: stats/htx: Respect the reserve when the stats page is dumped
- DOC: regtest: make it clearer what the purpose of the "broken" series is
- REGTEST: mailers: add new test for 'mailers' section
- REGTEST: Add a reg test for health-checks over SSL/TLS.
- BUG/MINOR: mux-h1: Close connection on shutr only when shutw was really done
- MEDIUM: mux-h1: Clarify how shutr/shutw are handled
- BUG/MINOR: compression: Disable it if another one is already in progress
- BUG/MINOR: filters: Detect cache+compression config on legacy HTTP streams
- BUG/MINOR: cache: Disable the cache if any compression filter precedes it
- REGTEST: Add some informatoin to test results.
- MINOR: htx: Add a function to truncate all blocks after a specific offset
- MINOR: channel/htx: Add the HTX version of channel_truncate/erase
- BUG/MINOR: proto_htx: Use HTX versions to truncate or erase a buffer
- BUG/CRITICAL: mux-h2: re-check the frame length when PRIORITY is used
- DOC: Fix typo in req.ssl_alpn example (commit 4afdd138424ab...)
- DOC: http-request cache-use / http-response cache-store expects cache name

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- Initial build
