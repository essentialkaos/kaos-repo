################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define hp_user      %{name}
%define hp_group     %{name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{name}
%define hp_confdir   %{_sysconfdir}/%{name}
%define hp_datadir   %{_datadir}/%{name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   3.1.1
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.8.1
Release:        0%{?dist}
License:        GPLv2+
URL:            https://haproxy.1wt.eu
Group:          System Environment/Daemons

Source0:        https://www.haproxy.org/download/2.8/src/%{name}-%{version}.tar.gz
Source1:        %{name}.cfg
Source2:        %{name}.logrotate

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

%setup -q

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
                          SSL_LIB=openssl-%{openssl_ver}/build/%{_lib} \
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

sed "s#@SBINDIR@#%{_sbindir}#g" admin/systemd/%{name}.service.in > \
                                admin/systemd/%{name}.service

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

pushd admin/systemd
  %{__make}
popd

install -pDm 0644 %{SOURCE1} %{buildroot}%{hp_confdir}/%{name}.cfg
install -pDm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 admin/systemd/%{name}.service %{buildroot}%{_unitdir}/

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
  systemctl enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  systemctl --no-reload disable %{name}.service &>/dev/null || :
  systemctl stop %{name}.service &>/dev/null || :
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
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{hp_datadir}/*
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz

################################################################################

%changelog
* Fri Jul 14 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- BUG/MINOR: stats: Fix Lua's `get_stats` function
- BUG/MINOR: stream: do not use client-fin/server-fin with HTX
- BUG/MINOR: quic: Possible crash when SSL session init fails
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- DOC: quic: fix misspelled tune.quic.socket-owner
- DOC: config: fix jwt_verify() example using var()
- DOC: config: fix rfc7239 converter examples (again)
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
- BUG/MINOR: proxy/server: free default-server on deinit
- BUG/MEDIUM: hlua: Use front SC to detect EOI in HTTP applets' receive
  functions
- BUG/MINOR: peers: Improve detection of config errors in peers sections
- REG-TESTS: stickiness: Delay haproxys start to properly resolv variables
- BUG/MINOR: ssl: log message non thread safe in SSL Hanshake failure
- BUG/MINOR: quic: Wrong encryption level flags checking
- BUG/MINOR: quic: Address inversion in "show quic full"
- BUG/MINOR: server: inherit from netns in srv_settings_cpy()
- BUG/MINOR: namespace: missing free in netns_sig_stop()
- BUG/MINOR: quic: Missing initialization (packet number space probing)
- BUG/MINOR: quic: Possible crash in quic_conn_prx_cntrs_update()
- BUG/MINOR: quic: Possible endless loop in quic_lstnr_dghdlr()
- BUG/MEDIUM: mworker: increase maxsock with each new worker
- BUG/MINOR: quic: ticks comparison without ticks API use
- DOC: Add tune.h2.be.* and tune.h2.fe.* options to table of contents
- DOC: Add tune.h2.max-frame-size option to table of contents
- REGTESTS: h1_host_normalization : Add a barrier to not mix up log messages
- DOC: Attempt to fix dconv parsing error for tune.h2.fe.initial-window-size
- BUG/MINOR: http_ext: fix if-none regression in forwardfor option
- BUG/MINOR: mworker: leak of a socketpair during startup failure
- BUG/MINOR: quic: Prevent deadlock with CID tree lock
- BUG/MEDIUM: quic: error checking buffer large enought to receive the retry tag
- BUG/MINOR: config: fix stick table duplicate name check
- BUG/MINOR: quic: Missing random bits in Retry packet header
- BUG/MINOR: quic: Wrong Retry paquet version field endianess
- BUG/MINOR: quic: Wrong endianess for version field in Retry token
- IMPORT: slz: implement a synchronous flush() operation
- MINOR: compression/slz: add support for a pure flush of pending bytes
- BUILD: debug: avoid a build warning related to epoll_wait() in debug code
- MINOR: quic: Move QUIC encryption level structure definition
- MINOR: quic: Move packet number space related functions
- MINOR: quic: Reduce the maximum length of TLS secrets
- CLEANUP: quic: Remove server specific about Initial packet number space

* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- MINOR: compression: Improve the way Vary header is added
- BUILD: makefile: search for SSL_INC/wolfssl before SSL_INC
- MINOR: init: pre-allocate kernel data structures on init
- DOC: install: add details about WolfSSL
- BUG/MINOR: ssl_sock: add check for ha_meth
- BUG/MINOR: thread: add a check for pthread_create
- BUILD: init: print rlim_cur as regular integer
- DOC: install: specify the minimum openssl version recommended
- CLEANUP: mux-quic: remove unneeded fields in qcc
- MINOR: mux-quic: remove nb_streams from qcc
- MINOR: quic: fix stats naming for flow control BLOCKED frames
- BUG/MEDIUM: mux-quic: only set EOI on FIN
- BUG/MEDIUM: threads: fix a tiny race in thread_isolate()
- DOC: config: fix rfc7239 converter examples
- DOC: quic: remove experimental status for QUIC
- CLEANUP: mux-quic: rename functions for mux_ops
- CLEANUP: mux-quic: rename internal functions
- BUG/MINOR: mux-h2: refresh the idle_timer when the mux is empty
- DOC: config: Fix bind/server/peer documentation in the peers section
- BUILD: Makefile: use -pthread not -lpthread when threads are enabled
- CLEANUP: doc: remove 21 totally obsolete docs
- DOC: install: mention the common strict-aliasing warning on older compilers
- DOC: install: clarify a few points on the wolfSSL build method
- MINOR: quic: Add QUIC connection statistical counters values to "show quic"
- EXAMPLES: update the basic-config-edge file for 2.8
- MINOR: quic/cli: clarify the "show quic" help message
- MINOR: version: mention that it's LTS now.
