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

%define lua_ver           5.3.5
%define pcre_ver          8.43
%define openssl_ver       1.1.1d
%define ncurses_ver       6.1
%define readline_ver      8.0

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.1.2
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
