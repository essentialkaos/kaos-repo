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
%define pcre_ver          8.42
%define boringssl_ver     d61334d187a33336bc4cf4425d997e1ec8bcfa48
%define ncurses_ver       6.0
%define readline_ver      7.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.8.4
Release:           0%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           http://www.haproxy.org/download/1.8/src/%{name}-%{version}.tar.gz
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

BuildRequires:     make cmake golang zlib-devel openssl-devel

%if 0%{?rhel} >= 7
BuildRequires:     gcc gcc-c++
%else
BuildRequires:     devtoolset-2-gcc-c++ devtoolset-2-binutils
%endif

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

mkdir boringssl

tar xzvf %{SOURCE10}
tar xzvf %{SOURCE11}
tar xzvf %{SOURCE12} -C boringssl
tar xzvf %{SOURCE13}
tar xzvf %{SOURCE14}

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

cp boringssl/build/crypto/libcrypto.a \
   boringssl/build/ssl/libssl.a \
   boringssl/.openssl/lib

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
                          TARGET="linux26" \
                          USE_OPENSSL=1 \
                          SSL_INC=boringssl/.openssl/include \
                          SSL_LIB=boringssl/.openssl/lib \
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
