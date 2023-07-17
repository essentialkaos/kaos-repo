################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  2.6
%define comp_ver   26

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   3.0.9
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.6.14
Release:        0%{?dist}
License:        GPLv2+
URL:            https://haproxy.1wt.eu
Group:          System Environment/Daemons

Source0:        https://www.haproxy.org/download/%{major_ver}/src/%{orig_name}-%{version}.tar.gz
Source1:        %{orig_name}.cfg
Source2:        %{orig_name}.logrotate

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

Conflicts:      haproxy haproxy22 haproxy24 haproxy28

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

%setup -qn %{orig_name}-%{version}

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

sed "s#@SBINDIR@#%{_sbindir}#g" admin/systemd/%{orig_name}.service.in > \
                                admin/systemd/%{orig_name}.service

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -pDm 0644 %{SOURCE1} %{buildroot}%{hp_confdir}/%{orig_name}.cfg
install -pDm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{orig_name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 admin/systemd/%{orig_name}.service %{buildroot}%{_unitdir}/

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
  systemctl enable %{orig_name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  systemctl --no-reload disable %{orig_name}.service &>/dev/null || :
  systemctl stop %{orig_name}.service &>/dev/null || :
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
%config(noreplace) %{hp_confdir}/%{orig_name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{orig_name}
%{hp_datadir}/*
%{_unitdir}/%{orig_name}.service
%{_sbindir}/%{orig_name}
%{_bindir}/halog
%{_mandir}/man1/%{orig_name}.1.gz

################################################################################

%changelog
* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.6.14-0
- BUG/MINOR: fd: always remove late updates when freeing fd_updt[]
- MINOR: ssl: ssl_sock_load_cert_chain() display error strings
- CI: switch to Fastly CDN to download LibreSSL
- BUILD: ssl: switch LibreSSL to Fastly CDN
- BUG/MEDIUM: spoe: Don't start new applet if there are enough idle ones
- BUG/MINOR: resolvers: Use sc_need_room() to wait more room when dumping stats
- MINOR: quic: use real sending rate measurement
- DEV: haring: automatically disable DEBUG_STRICT
- DEV: haring: update readme to suggest using the same build options for haring
- BUG/MINOR: mux-quic: prevent quic_conn error code to be overwritten
- BUG/MINOR: debug: do not emit empty lines in thread dumps
- BUG/MINOR: quic: Wrong key update cipher context initialization for encryption
- BUILD: ssl: buggy -Werror=dangling-pointer since gcc 13.0
- DOC: configuration: add info about ssl-engine for 2.6
- BUG/MINOR: quic: Possible crash when dumping version information
- BUILD: mjson: Fix warning about unused variables
- MINOR: spoe: Don't stop disabled proxies
- BUG/MEDIUM: filters: Don't deinit filters for disabled proxies during startup
- MINOR: http-rules: Add missing actions in http-after-response ruleset
- BUG/MINOR: quic: Buggy acknowlegments of acknowlegments function
- BUG/MEDIUM: mux-fcgi: Don't request more room if mux is waiting for more data
- BUG/MINOR: proxy: missing free in free_proxy for redirect rules
- MINOR: proxy: add http_free_redirect_rule() function
- BUG/MINOR: http_rules: fix errors paths in http_parse_redirect_rule()
- BUG/MINOR: errors: handle malloc failure in usermsgs_put()
- BUG/MINOR: log: fix memory error handling in parse_logsrv()
- MINOR: htx: add function to set EOM reliably
- MINOR: checks: make sure spread-checks is used also at boot time
- MINOR: clock: measure the total boot time
- BUG/MINOR: checks: postpone the startup of health checks by the boot time
- BUG/MINOR: clock: fix the boot time measurement method for 2.6 and older
- BUG/MINOR: tcp-rules: Don't shortened the inspect-delay when EOI is set
- REGTESTS: log: Reduce response inspect-delay for last_rule.vtc
- DOC: config: Clarify conditions to shorten the inspect-delay for TCP rules
- REGTESTS: log: Reduce again response inspect-delay for last_rule.vtc
- DOC: add size format section to manual
- DOC/MINOR: config: Fix typo in description for `ssl_bc` in configuration.txt
- BUG/MINOR: hlua: unsafe hlua_lua2smp() usage
- SCRIPTS: publish-release: update the umask to keep group write access
- BUG/MINOR: mux-quic: properly handle buf alloc failure
- BUG/MINOR: mux-quic: handle properly recv ncbuf alloc failure
- BUG/MINOR: quic: do not alloc buf count on alloc failure
- BUG/MINOR: mux-quic: differentiate failure on qc_stream_desc alloc
- BUG/MINOR: mux-quic: handle properly Tx buf exhaustion
- MINOR: mux-quic: uninline qc_attach_sc()
- BUG/MEDIUM: mux-quic: fix EOI for request without payload
- BUG/MINOR: quic: Wrong token length check (quic_generate_retry_token())
- BUG/MINOR: quic: Missing Retry token length on receipt
- DOC: config: Fix bind/server/peer documentation in the peers section
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- BUG/MINOR: quic: Possible crash when SSL session init fails
- DOC: config: fix jwt_verify() example using var()
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
