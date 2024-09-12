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

%define lua_ver       5.4.7
%define pcre_ver      10.44
%define openssl_ver   3.2.2
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        3.0.3
Release:        0%{?dist}
License:        GPLv2+
URL:            https://haproxy.1wt.eu
Group:          System Environment/Daemons

Source0:        https://www.haproxy.org/download/3.0/src/%{name}-%{version}.tar.gz
Source1:        %{name}.cfg
Source2:        %{name}.logrotate

Source10:       https://www.lua.org/ftp/lua-%{lua_ver}.tar.gz
Source11:       https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{pcre_ver}/pcre2-%{pcre_ver}.tar.gz
Source12:       https://www.openssl.org/source/openssl-%{openssl_ver}.tar.gz
Source13:       https://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{ncurses_ver}.tar.gz
Source14:       https://ftp.gnu.org/gnu/readline/readline-%{readline_ver}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc-c++ zlib-devel systemd-devel perl perl-IPC-Cmd

Conflicts:      haproxy22 haproxy24 haproxy26 haproxy28 haproxy30

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

%setup -qn %{name}-%{version}

tar xzvf %{SOURCE10}
tar xzvf %{SOURCE11}
tar xzvf %{SOURCE12}
tar xzvf %{SOURCE13}
tar xzvf %{SOURCE14}

%build

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static OpenSSL build
pushd openssl-%{openssl_ver}
  mkdir build
  # perfecto:ignore
  ./config --prefix=$(pwd)/build no-shared no-threads
  %{__make} %{?_smp_mflags}
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
* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- BUG/MINOR: log: fix broken '+bin' logformat node option
- DEBUG: hlua: distinguish burst timeout errors from exec timeout errors
- REGTESTS: ssl: fix some regtests 'feature cmd' start condition
- BUG/MEDIUM: proxy: fix email-alert invalid free
- DOC: configuration: fix alphabetical order of bind options
- DOC: management: document ptr lookup for table commands
- BUG/MAJOR: quic: fix padding with short packets
- SCRIPTS: git-show-backports: do not truncate git-show output
- DOC: api/event_hdl: small updates, fix an example and add some precisions
- BUG/MINOR: h3: fix crash on STOP_SENDING receive after GOAWAY emission
- BUG/MINOR: mux-quic: fix crash on qcs SD alloc failure
- BUG/MINOR: h3: fix BUG_ON() crash on control stream alloc failure
- BUG/MINOR: quic: fix BUG_ON() on Tx pkt alloc failure
- DEV: flags/show-fd-to-flags: adapt to recent versions
- BUG/MINOR: hlua: report proper context upon error in hlua_cli_io_handler_fct()
- BUG/MEDIUM: stick-table: Decrement the ref count inside lock to kill a session
- DOC: configuration: add details about crt-store in bind "crt" keyword
- BUG/MINOR: server: fix first server template name lookup UAF
- MINOR: activity: make the memory profiling hash size configurable at build
  time
- BUG/MEDIUM: server/dns: prevent DOWN/UP flap upon resolution timeout or error
- BUG/MEDIUM: h3: ensure the ":method" pseudo header is totally valid
- BUG/MEDIUM: h3: ensure the ":scheme" pseudo header is totally valid
- BUG/MEDIUM: quic: fix race-condition in quic_get_cid_tid()
- BUG/MINOR: quic: fix race condition in qc_check_dcid()
- BUG/MINOR: quic: fix race-condition on trace for CID retrieval
- BUG/MEDIUM: quic: fix possible exit from qc_check_dcid() without unlocking
- BUG/MINOR: promex: Remove Help prefix repeated twice for each metric
- BUG/MEDIUM: hlua/cli: Fix lua CLI commands to work with applet's buffers
- DOC: configuration: more details about the master-worker mode
- BUG/MEDIUM: server: fix race on server_atomic_sync()
- BUG/MINOR: jwt: don't try to load files with HMAC algorithm
- MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD
- DOC: configuration: update maxconn description
- BUG/MEDIUM: peers: Fix crash when syncing learn state of a peer without appctx
- Revert "MEDIUM: init: set default for fd_hard_limit via DEFAULT_MAXFD"
- BUG/MINOR: jwt: fix variable initialisation
- BUG/MINOR: h1: Fail to parse empty transfer coding names
- BUG/MINOR: h1: Reject empty coding name as last transfer-encoding value
- BUG/MEDIUM: h1: Reject empty Transfer-encoding header
- BUG/MEDIUM: spoe: Be sure to create a SPOE applet if none on the current
  thread
- DEV: flags/quic: decode quic_conn flags
- BUG/MEDIUM: bwlim: Be sure to never set the analyze expiration date in past

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- MINOR: log: fix "http-send-name-header" ignore warning message
- BUG/MINOR: proxy: fix server_id_hdr_name leak on deinit()
- BUG/MINOR: proxy: fix log_tag leak on deinit()
- BUG/MINOR: proxy: fix email-alert leak on deinit()
- BUG/MINOR: proxy: fix check_{command,path} leak on deinit()
- BUG/MINOR: proxy: fix dyncookie_key leak on deinit()
- BUG/MINOR: proxy: fix source interface and usesrc leaks on deinit()
- BUG/MINOR: proxy: fix header_unique_id leak on deinit()
- BUG/MEDIUM: log: fix lf_expr_postcheck() behavior with default section
- DOC: config: move "hash-key" from proxy to server options
- DOC: config: add missing section hint for "guid" proxy keyword
- DOC: config: add missing context hint for new server and proxy keywords
- BUG/MINOR: promex: Skip resolvers metrics when there is no resolver section
- MINOR: proxy: add proxy_free_common() helper function
- BUG/MEDIUM: proxy: fix UAF with {tcp,http}checks logformat expressions
- CLEANUP: log/proxy: fix comment in proxy_free_common()
- BUG/MAJOR: mux-h1: Prevent any UAF on H1 connection after draining a request
- BUG/MINOR: quic: fix padding of INITIAL packets
- DOC/MINOR: management: add missed -dR and -dv options
- DOC/MINOR: management: add -dZ option
- DOC: management: rename show stats domain cli "dns" to "resolvers"

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- BUG/MINOR: cfgparse: remove the correct option on httpcheck send-state warning
- BUG/MINOR: tcpcheck: report correct error in tcp-check rule parser
- BUG/MINOR: tools: fix possible null-deref in env_expand() on out-of-memory
- DOC: configuration: add an example for keywords from crt-store
- BUG/MINOR: hlua: use CertCache.set() from various hlua contexts
- BUG/MEDIUM: h1-htx: Don't state interim responses are bodyless
- MEDIUM: stconn: Be able to unblock zero-copy data forwarding from done_fastfwd
- BUG/MEDIUM: mux-quic: Unblock zero-copy forwarding if the txbuf can be
  released
- BUG/MINOR: quic: prevent crash on qc_kill_conn()
- CLEANUP: hlua: use hlua_pusherror() where relevant
- BUG/MINOR: hlua: don't use lua_pushfstring() when we don't expect LJMP
- BUG/MINOR: hlua: fix unsafe hlua_pusherror() usage
- BUG/MINOR: hlua: prevent LJMP in hlua_traceback()
- BUG/MINOR: hlua: fix leak in hlua_ckch_set() error path
- CLEANUP: hlua: simplify ambiguous lua_insert() usage in hlua_ctx_resume()
- BUG/MEDIUM: mux-quic: Don't unblock zero-copy fwding if blocked during nego
- BUG/MEDIUM: ssl: wrong priority whem limiting ECDSA ciphers in ECDSA+RSA
  configuration
- BUG/MEDIUM: ssl: bad auth selection with TLS1.2 and WolfSSL
- BUG/MINOR: quic: fix computed length of emitted STREAM frames
- BUG/MINOR: quic: ensure Tx buf is always purged
- BUG/MEDIUM: stconn/mux-h1: Fix suspect change causing timeouts
- BUG/MAJOR: mux-h1:  Properly copy chunked input data during zero-copy nego
- BUG/MINOR: mux-h1: Use the right variable to set NEGO_FF_FL_EXACT_SIZE flag

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- Switched to 3.0.x version
