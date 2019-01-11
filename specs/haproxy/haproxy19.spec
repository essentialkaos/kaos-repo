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
%define pcre_ver          8.42
%define openssl_ver       1.1.1a
%define ncurses_ver       6.1
%define readline_ver      8.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.9.1
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
                          TARGET="linux2628" \
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
