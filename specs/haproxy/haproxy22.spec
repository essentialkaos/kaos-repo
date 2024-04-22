################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define orig_name  haproxy
%define major_ver  2.2
%define comp_ver   22

%define hp_user      %{orig_name}
%define hp_group     %{orig_name}
%define hp_user_id   188
%define hp_group_id  188
%define hp_homedir   %{_localstatedir}/lib/%{orig_name}
%define hp_confdir   %{_sysconfdir}/%{orig_name}
%define hp_datadir   %{_datadir}/%{orig_name}

%define lua_ver       5.4.6
%define pcre_ver      10.42
%define openssl_ver   1.1.1v
%define ncurses_ver   6.4
%define readline_ver  8.2

################################################################################

Name:           haproxy%{comp_ver}
Summary:        TCP/HTTP reverse proxy for high availability environments
Version:        2.2.33
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

Conflicts:      haproxy haproxy24 haproxy26 haproxy28

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
                          SSL_LIB=openssl-%{openssl_ver}/build/lib \
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

sed "s#@SBINDIR@#%{_sbindir}#g" contrib/systemd/%{orig_name}.service.in > \
                                contrib/systemd/%{orig_name}.service

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
install -pm 644 contrib/systemd/%{orig_name}.service %{buildroot}%{_unitdir}/

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
%{_mandir}/man1/%{orig_name}.1.gz

################################################################################

%changelog
* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.2.33-0
- DOC: configuration: typo req.ssl_hello_type
- BUG/MEDIUM: mux-h2: Report too large HEADERS frame only when rxbuf is empty
- BUG/MEDIUM: stconn: Forward shutdown on write timeout only if it
  is forwardable
- BUG/MEDIUM: spoe: Never create new spoe applet if there is no server up
- BUG/MEDIUM: cli: some err/warn msg dumps add LR into CSV output on stat's CLI
- BUG/MEDIUM: pool: fix rare risk of deadlock in pool_flush()
- BUG/MINOR: h1-htx: properly initialize the err_pos field
- BUG/MEDIUM: h1: always reject the NUL character in header values
- BUG/MAJOR: ssl_sock: Always clear retry flags in read/write functions
- DOC: internal: update missing data types in peers-v2.0.txt
- CI: Update to actions/cache@v4
- BUG/MINOR: hlua: Fix log level to the right value when set via
  TXN:set_loglevel
- BUG/MINOR: cfgparse: report proper location for log-format-sd errors
- BUG/MINOR: ssl: fix possible ctx memory leak in sample_conv_aes_gcm()
- BUG/MEDIUM: spoe: Return an invalid frame on recv if size is too small
- BUG/MINOR: session: ensure conn owner is set after insert into session
- BUG/MINOR: server: 'source' interface ignored from 'default-server' directive
- BUG/MINOR: backend: properly handle redispatch 0
- CLEANUP: pools: remove unused arguments to pool_evict_from_cache()
- BUG/MEDIUM: spoe: Don't rely on stream's expiration to detect processing
  timeout

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.2.32-0
- BUG/MINOR: stktable: allow sc-set-gpt(0) from tcp-request connection
- SCRIPTS: git-show-backports: automatic ref and base detection with -m
- DOC: lua: fix core.register_action typo
- BUG/MEDIUM: stconn: Wake applets on sending path if there is a pending
  shutdown
- BUG/MEDIUM: stconn/stream: Forward shutdown on write timeout
- BUG/MINOR: hlua/action: incorrect message on E_YIELD error
- CI: Update to actions/checkout@v4
- BUG/MEDIUM: hlua: don't pass stale nargs argument to lua_resume()
- MINOR: buf: Add b_force_xfer() function
- BUG/MEDIUM: mux-fcgi: Don't swap trash and dbuf when handling STDERR records
- BUG/MINOR: freq_ctr: fix possible negative rate with the scaled API
- BUG/MAJOR: mux-h2: Report a protocol error for any DATA frame before headers
- MINOR: pattern: fix pat_{parse,match}_ip() function comments
- BUG/MINOR: hlua: fix invalid use of lua_pop on error paths
- BUG/MINOR: hlua_fcn: potentially unsafe stktable_data_ptr usage
- BUILD: ssl: buggy -Werror=dangling-pointer since gcc 13.0
- BUG/MEDIUM: actions: always apply a longest match on prefix lookup
- BUG/MEDIUM: mux-h2: Don't report an error on shutr if a shutw is pending
- BUG/MEDIUM: peers: Be sure to always refresh recconnect timer in sync task
- BUG/MINOR: mux-h2: commit the current stream ID even on reject
- BUG/MINOR: ssl: suboptimal certificate selection with TLSv1.3 and dual
  ECDSA/RSA
- BUG/MEDIUM: ssl: segfault when cipher is NULL
- BUG/MINOR: tcpcheck: Report hexstring instead of binary one on check failure
- BUG/MINOR: stktable: missing free in parse_stick_table()
- BUG/MINOR: cfgparse/stktable: fix error message on stktable_init() failure
- BUG/MINOR: stick-table/cli: Check for invalid ipv4 key
- DOC: management: -q is quiet all the time
- DOC: config: use the word 'backend' instead of 'proxy' in 'track' description
- BUG/MINOR: stconn: Handle abortonclose if backend connection was already
  set up
- MINOR: connection: Add a CTL flag to notify mux it should wait for reads again
- MEDIUM: mux-h1: Handle MUX_SUBS_RECV flag in h1_ctl() and susbscribe for reads
- BUG/MEDIUM: stream: Properly handle abortonclose when set on backend only
- REGTESTS: http: Improve script testing abortonclose option
- BUG/MEDIUM: stream: Don't call mux .ctl() callback if not implemented
- MINOR: htx: Use a macro for overhead induced by HTX
- MINOR: channel: Add functions to get info on buffers and deal with HTX streams
- BUG/MINOR: stconn: Fix streamer detection for HTX streams
- BUG/MINOR: stconn: Use HTX-aware channel's functions to get info on buffer
- BUG/MEDIUM: mux-h2: fail earlier on malloc in takeover()
- BUG/MEDIUM: mux-h1: fail earlier on malloc in takeover()
- BUG/MEDIUM: mux-fcgi: fail earlier on malloc in takeover()
- REGTESTS: http: add a test to validate chunked responses delivery
- DOC: 51d: updated 51Degrees repo URL for v3.2.10
- DOC: config: specify supported sections for "max-session-srv-conns"
- DOC: config: add matrix entry for "max-session-srv-conns"
- REGTESTS: sample: Test the behavior of consecutive delimiters for the field
  converter
- BUG/MINOR: sample: Make the `word` converter compatible with `-m found`
- DOC: Clarify the differences between field() and word()
- BUG/MINOR: startup: set GTUNE_SOCKET_TRANSFER correctly
- BUILD: ssl: work around bogus warning in gcc 12's -Wformat-truncation
- BUG/MEDIUM: ssl: fix the gcc-12 broken fix :-(

* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 2.2.31-0
- BUG/MINOR: server: inherit from netns in srv_settings_cpy()
- BUG/MINOR: namespace: missing free in netns_sig_stop()
- BUG/MEDIUM: mworker: increase maxsock with each new worker
- DOC: Add tune.h2.max-frame-size option to table of contents
- BUG/MINOR: ring: maxlen warning reported as alert
- BUG/MINOR: sample: Fix wrong overflow detection in add/sub conveters
- BUG/MINOR: http: Return the right reason for 302
- CI: explicitely highlight VTest result section if there's something
- BUG/MINOR: h1-htx: Return the right reason for 302 FCGI responses
- DOC: configuration: describe Td in Timing events
- BUG/MINOR: chunk: fix chunk_appendf() to not write a zero if buffer is full
- BUG/MAJOR: http-ana: Get a fresh trash buffer for each header value
  replacement
- BUG/MAJOR: http: reject any empty content-length header value
- MINOR: ist: add new function ist_find_range() to find a character range
- MINOR: ist: Add istend() function to return a pointer to the end of the string
- MINOR: http: add new function http_path_has_forbidden_char()
- MINOR: h2: pass accept-invalid-http-request down the request parser
- BUG/MINOR: h1: do not accept '#' as part of the URI component
- BUG/MINOR: h2: reject more chars from the :path pseudo header
- REGTESTS: http-rules: verify that we block '#' by default for normalize-uri
- DOC: clarify the handling of URL fragments in requests
- BUG/MINOR: http: skip leading zeroes in content-length values

* Mon Jul 10 2023 Anton Novojilov <andy@essentialkaos.com> - 2.2.30-0
- DOC/MINOR: reformat configuration.txt's "quoting and escaping" table
- BUG/MINOR: mworker: stop doing strtok directly from the env
- BUG/MEDIUM: mworker: don't register mworker_accept_wrapper() when master FD
  is wrong
- BUG/MINOR: mworker: prevent incorrect values in uptime
- BUG/MINOR: ring: do not realign ring contents on resize
- DOC: config: Fix description of options about HTTP connection modes
- DOC: config: Add the missing tune.fail-alloc option from global listing
- DOC: config: Clarify the meaning of 'hold' in the 'resolvers' section
- BUG/MINOR: http-check: Don't set HTX_SL_F_BODYLESS flag with a log-format body
- BUG/MINOR: http-check: Skip C-L header for empty body when it's not mandatory
- BUG/MINOR: ssl: Use 'date' instead of 'now' in ocsp stapling callback
- BUG/MINOR: mux-h2: make sure the h2c task exists before refreshing it
- BUG/MEDIUM: spoe: Don't set the default traget for the SPOE agent frontend
- BUG/MEDIUM: mux-h2: erase h2c->wait_event.tasklet on error path
- BUG/MEDIUM: mux-h1: Wakeup H1C on shutw if there is no I/O subscription
- BUILD: da: extends CFLAGS to support API v3 from 3.1.7 and onwards.
- MINOR: proxy/pool: prevent unnecessary calls to pool_gc()
- DOC: config: strict-sni allows to start without certificate
- BUG/MINOR: stick_table: alert when type len has incorrect characters
- CI: bump "actions/checkout" to v3 for cross zoo matrix
- BUG/MINOR: cfgparse: make sure to include openssl-compat
- BUG/MEDIUM: proxy/sktable: prevent watchdog trigger on soft-stop
- BUG/MEDIUM: Update read expiration date on synchronous send
- BUG/MINOR: mux-h2: make sure to produce a log on invalid requests
- MINOR: checks: make sure spread-checks is used also at boot time
- MINOR: clock: measure the total boot time
- BUG/MINOR: checks: postpone the startup of health checks by the boot time
- BUILD: checks: fix build failure on macos after last fix
- BUG/MEDIUM: mux-h1: do not refrain from signaling errors after end of input
- BUG/MINOR: tcp-rules: Don't shortened the inspect-delay when EOI is set
- DOC: config: Clarify conditions to shorten the inspect-delay for TCP rules
- DOC/MINOR: config: Fix typo in description for `ssl_bc` in configuration.txt
- BUG/MINOR: hlua: unsafe hlua_lua2smp() usage
- SCRIPTS: publish-release: update the umask to keep group write access
- BUG/MINOR: log: fix memory error handling in parse_logsrv()
- BUG/MINOR: proxy: missing free in free_proxy for redirect rules
- MINOR: spoe: Don't stop disabled proxies
- BUG/MEDIUM: filters: Don't deinit filters for disabled proxies during startup
- BUG/MINOR: debug: do not emit empty lines in thread dumps
- BUG/MEDIUM: spoe: Don't start new applet if there are enough idle ones
- CI: switch to Fastly CDN to download LibreSSL
- BUILD: ssl: switch LibreSSL to Fastly CDN
- BUG/MINOR: server: incorrect report for tracking servers leaving drain
- MINOR: server: explicitly commit state change in srv_update_status()
- BUG/MINOR: server: don't miss proxy stats update on server state transitions
- BUG/MINOR: server: don't miss server stats update on server state transitions
- BUG/MINOR: server: don't use date when restoring last_change from state file
- CI: cirrus-ci: bump FreeBSD image to 13-1
- DOC: config: Fix bind/server/peer documentation in the peers section
- CONTRIB: Add vi file extensions to .gitignore
- BUG/MINOR: spoe: Only skip sending new frame after a receive attempt
- BUG/MINOR: cfgparse-tcp: leak when re-declaring interface from bind line
- BUG/MINOR: proxy: add missing interface bind free in free_proxy
