################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  3.2
%define comp_ver   32

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.7
%define pcre_ver      10.45
%define openssl_ver   3.5.2
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        3.2.3
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

BuildRequires:  make gcc-c++ systemd-devel perl perl-IPC-Cmd

%if 0%{?rhel} == 10
BuildRequires:  zlib-ng-compat-devel
%else
BuildRequires:  zlib-devel
%endif

Conflicts:      haproxy haproxy22 haproxy24 haproxy26 haproxy28 haproxy30

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

### DEPS BUILD START ###

export BUILDDIR=$(pwd)

# Static OpenSSL build
pushd openssl-%{openssl_ver}
  mkdir build
  # perfecto:ignore
  ./config --prefix=$(pwd)/build no-shared no-threads no-tests
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
                          ADDLIB="-ldl -lrt -lpthread"

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
%doc CHANGELOG LICENSE doc/* examples/*.cfg
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
* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- CI: enable USE_QUIC=1 for OpenSSL versions >= 3.5.0
- CI: github: add an OpenSSL 3.5.0 job
- CI: github: update the stable CI to ubuntu-24.04
- BUILD: quic: QUIC build against OpenSSL 3.5 broken
- BUG/MEDIUM: quic: SSL/TCP handshake failures with OpenSSL 3.5
- CI: github: update to OpenSSL 3.5.1
- BUG/MINOR: quic: Missing TLS 1.3 QUIC cipher suites and groups inits
  (OpenSSL 3.5 QUIC API)
- BUG/MINOR: ssl/ocsp: fix definition discrepancies with ocsp_update_init()
- BUG/MINOR: ssl: crash in ssl_sock_io_cb() with SSL traces and idle
  connections
- BUG/MINOR: http-act: Fix parsing of the expression argument for pause action
- BUILD/MEDIUM: deviceatlas: fix when installed in custom locations.

* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- BUG/MINOR: config/server: reject QUIC addresses
- BUG/MINOR: http-ana: Properly handle keep-query redirect option if no QS
- BUG/MINOR: quic: Fix OSSL_FUNC_SSL_QUIC_TLS_got_transport_params_fn
  callback (OpenSSL3.5)
- BUG/MEDIUM: cli: Don't consume data if outbuf is full or not available
- MINOR: cli: handle EOS/ERROR first
- BUG/MEDIUM: check: Set SOCKERR by default when a connection error is
  reported
- DOC: config: prefer-last-server: add notes for non-deterministic algorithms
- BUG/MINOR: mux-quic/h3: properly handle too low peer fctl initial stream
- BUG/MAJOR: fwlc: Count an avoided server as unusable.
- MINOR: fwlc: Factorize code.
- BUG/MINOR: tools: only reset argument start upon new argument
- BUG/MINOR: stream: Avoid recursive evaluation for unique-id based on itself
- BUG/MINOR: log: Be able to use %%ID alias at anytime of the stream's
  evaluation
- DOC: configuration: add details on prefer-client-ciphers
- BUG/MINOR: quic: wrong QUIC_FT_CONNECTION_CLOSE(0x1c) frame encoding
- MINOR: quic: Useless TX buffer size reduction in closing state
- DOC: config: crt-list clarify default cert + cert-bundle
- SCRIPTS: drop the HTML generation from announce-release
- BUG/MINOR: tools: use my_unsetenv instead of unsetenv
- MINOR: ssl: check TLS1.3 ciphersuites again in clienthello with recent
  AWS-LC
- BUG/MEDIUM: hlua: Forbid any L6/L7 sample fetche functions from lua
  services
- BUG/MEDIUM: mux-h2: Properly handle connection error during preface sending
- BUG/MINOR: jwt: Copy input and parameters in dedicated buffers in jwt_verify
  converter
- DOC: Fix 'jwt_verify' converter doc
- BUG/MINOR: httpclient: wrongly named httpproxy flag
- BUILD: dev/phash: remove the accidentally committed a.out file

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- BUILD: tools: properly define ha_dump_backtrace() to avoid a build warning
- DOC: config: Fix a typo in 2.7 (Name format for maps and ACLs)
- BUG/MAJOR: leastconn: Protect tree_elt with the lbprm lock
- BUG/MEDIUM: check: Requeue healthchecks on I/O events to handle check timeout
- BUG/MINOR: mux-spop: Fix null-pointer deref on SPOP stream allocation failure
- BUG/MEDIUM: cli: Properly parse empty lines and avoid crashed
- BUG/MINOR: config: emit warning for empty args only in discovery mode
- BUG/MINOR: config: fix arg number reported on empty arg warning
- BUG/MINOR: quic: Missing SSL session object freeing
- BUG/MEDIUM: fd: Use the provided tgid in fd_insert() to get tgroup_info
- BUG/MINIR: h1: Fix doc of 'accept-unsafe-...-request' about URI parsing

* Wed Jun 18 2025 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- Initial build for kaos repository
