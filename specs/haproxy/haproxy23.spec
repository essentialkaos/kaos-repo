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

%define lua_ver           5.4.2
%define pcre_ver          8.44
%define openssl_ver       1.1.1j
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.3.5
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.3/src/%{name}-%{version}.tar.gz
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

Requires:          setup >= 2.8.14-14 kaosv >= 2.16

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

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
  %{__sysctl} enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGELOG LICENSE README doc/* examples/*.cfg
%dir %{hp_datadir}
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{hp_datadir}/*
%{_initrddir}/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.5-0
- BUG/MINOR: init: Use a dynamic buffer to set HAPROXY_CFGFILES env variable
- MINOR: config: Add failifnotcap() to emit an alert on proxy capabilities
- MINOR: server: Forbid server definitions in frontend sections
- BUG/MINOR: threads: Fixes the number of possible cpus report for Mac.
- MINOR: peers: Add traces for peer control messages.
- BUG/MINOR: dns: SRV records ignores duplicated AR records (v2)
- BUILD: peers: fix build warning about unused variable
- BUG/MEDIUM: stats: add missing INF_BUILD_INFO definition
- BUG/MINOR: peers: Possible appctx pointer dereference.
- MINOR: build: discard echoing in help target
- BUG/MINOR: peers: Wrong "new_conn" value for "show peers" CLI command.
- BUG/MINOR: mux_h2: missing space between "st" and ".flg" in the "show fd"
  helper
- BUG/MINOR: mworker: define _GNU_SOURCE for strsignal()
- BUG/MEDIUM: tcpcheck: Don't destroy connection in the wake callback context
- BUG/MEDIUM: mux-h2: fix read0 handling on partial frames
- BUILD/MINOR: lua: define _GNU_SOURCE for LLONG_MAX
- DOC: Improve documentation of the various hdr() fetches
- BUG/MEDIUM: filters/htx: Fix data forwarding when payload length is unknown
- BUG/MINOR: config: fix leak on proxy.conn_src.bind_hdr_name
- BUG/MINOR: ssl: init tmp chunk correctly in ssl_sock_load_sctl_from_file()
- BUG/MEDIUM: session: only retrieve ready idle conn from session
- REORG: backend: simplify conn_backend_get
- BUG/MEDIUM: backend: never reuse a connection for tcp mode
- BUG/MINOR: backend: check available list allocation for reuse
- MINOR: contrib: Make the wireshark peers dissector compile for more distribs.
- CLEANUP: tools: make resolve_sym_name() take a const pointer
- CLEANUP: cli: make "show fd" use a const connection to access other fields
- MINOR: cli: make "show fd" also report the xprt and xprt_ctx
- MINOR: xprt: add a new show_fd() helper to complete some "show fd" dumps.
- MINOR: ssl: provide a "show fd" helper to report important SSL information
- MINOR: xprt/mux: export all *_io_cb functions so that "show fd" resolves them
- MINOR: mux-h2: make the "show fd" helper also decode the h2s subscriber
  when known
- MINOR: mux-h1: make the "show fd" helper also decode the h1s subscriber
  when known
- MINOR: mux-fcgi: make the "show fd" helper also decode the fstrm subscriber
  when known
- MINOR: cli: give the show_fd helpers the ability to report a suspicious entry
- MINOR: cli/show_fd: report some easily detectable suspicious states
- MINOR: ssl/show_fd: report some FDs as suspicious when possible
- MINOR: mux-h2/show_fd: report as suspicious an entry with too many calls
- MINOR: mux-h1/show_fd: report as suspicious an entry with too many calls
- MINOR: h1: Raise the chunk size limit up to (2^52 - 1)
- DOC: management: fix "show resolvers" alphabetical ordering
- BUG/MINOR: stick-table: Always call smp_fetch_src() with a valid arg list
- BUG/MEDIUM: ssl/cli: abort ssl cert is freeing the old store
- BUG/MEDIUM: ssl: check a connection's status before computing a handshake
- BUG/MINOR: mux_h2: fix incorrect stat titles
- BUG/MINOR: xxhash: make sure armv6 uses memcpy()
- BUG/MINOR: ssl: do not try to use early data if not configured
- BUILD: ssl: fix build breakage with last commit
- MINOR: cli/show_fd: report local and report ports when known
- BUILD: Makefile: move REGTESTST_TYPE default setting
- BUG/MEDIUM: mux-h2: handle remaining read0 cases
- BUG/MEDIUM: mux-h2: do not quit the demux loop before setting END_REACHED
- BUG/MINOR: sock: Unclosed fd in case of connection allocation failure
- MINOR: config: Deprecate and ignore tune.chksize global option

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.4-0
- MINOR: reg-tests: add a way to add service dependency
- BUG/MINOR: sample: check alloc_trash_chunk return value in concat()
- BUG/MINOR: reg-tests: fix service dependency script
- MINOR: reg-tests: add base prometheus test
- Revert "BUG/MINOR: dns: SRV records ignores duplicated AR records"
- BUG/MINOR: sample: Memory leak of sample_expr structure in case of error
- BUG/MINOR: check: Don't perform any check on servers defined in a frontend
- BUG/MINOR: init: enforce strict-limits when using master-worker
- MINOR: contrib/prometheus-exporter: avoid connection close header
- MINOR: contrib/prometheus-exporter: use fill_info for process dump

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- MINOR: plock: use an ARMv8 instruction barrier for the pause instruction
- BUG/MEDIUM: lists: Lock the element while we check if it is in a list.
- MINOR: task: remove __tasklet_remove_from_tasklet_list()
- BUG/MEDIUM: task: close a possible data race condition on a tasklet's
  list link
- BUG/MEDIUM: local log format regression.
- BUG/MINOR: mux-h2/stats: make stream/connection proto errors more accurate
- BUG/MINOR: mux-h2/stats: not all GOAWAY frames are errors
- BUG/MINOR: lua: missing "\n" in error message
- BUG/MINOR: lua: lua-load doesn't check its parameters
- BUG/MINOR: lua: Post init register function are not executed beyond
  the first one
- BUG/MINOR: lua: Some lua init operation are processed unsafe
- MINOR: actions: Export actions lookup functions
- MINOR: actions: add a function returning a service pointer from its name
- MINOR: cli: add a function to look up a CLI service description
- BUG/MINOR: lua: warn when registering action, conv, sf, cli or applet
  multiple times
- BUG/MAJOR: ring: tcp forward on ring can break the reader counter.
- BUILD/MINOR: haproxy DragonFlyBSD affinity build update.
- DOC/MINOR: Fix formatting in Management Guide
- BUG/MINOR: listener: use sockaddr_in6 for IPv6
- BUG/MINOR: mux-h1: Handle keep-alive timeout for idle frontend connections
- MINOR: protocol: add a ->set_port() helper to address families
- MINOR: listener: automatically set the port when creating listeners
- MINOR: listener: now use a generic add_listener() function
- MEDIUM: ssl: fatal error with bundle + openssl < 1.1.1
- BUG/MAJOR: spoa/python: Fixing return None
- DOC: spoa/python: Fixing typo in IP related error messages
- DOC: spoa/python: Rephrasing memory related error messages
- DOC: spoa/python: Fixing typos in comments
- BUG/MINOR: spoa/python: Cleanup references for failed Module Addobject
  operations
- BUG/MINOR: spoa/python: Cleanup ipaddress objects if initialization fails
- BUG/MEDIUM: spoa/python: Fixing PyObject_Call positional arguments
- BUG/MEDIUM: spoa/python: Fixing references to None
- DOC: email change of the DeviceAtlas maintainer
- BUG/MINOR: http-check: Use right condition to consider HTX message as full
- BUG/MINOR: tcpcheck: Don't rearm the check timeout on each read
- MINOR: tcpcheck: Only wait for more payload data on HTTP expect rules
- BUG/MINOR: tools: make parse_time_err() more strict on the timer validity
- BUG/MINOR: tools: Reject size format not starting by a digit
- BUG/MEDIUM: lb-leastconn: Reposition a server using the right eweight
- BUG/MEDIUM: ssl/crt-list: bad behavior with "commit ssl cert"
- REGTESTS: make use of HAPROXY_ARGS and pass -dM by default
- BUILD: SSL: fine guard for SSL_CTX_add_server_custom_ext call
- BUILD: Makefile: have "make clean" destroy .o/.a/.s in contrib subdirs as well
- BUG/MINOR: mux-h1: Don't set CS_FL_EOI too early for protocol upgrade requests
- BUG/MEDIUM: http-ana: Never for sending data in TUNNEL mode
- BUG/MEDIUM: mux-h1: Handle h1_process() failures on a pipelined request
- CONTRIB: halog: fix build issue caused by %%L printf format
- CONTRIB: halog: mark the has_zero* functions unused
- CONTRIB: halog: fix signed/unsigned build warnings on counts and timestamps
- CONTRIB: debug: address "poll" utility build on non-linux platforms
- BUILD: plock: remove dead code that causes a warning in gcc 11
- BUILD: ssl: fine guard for SSL_CTX_get0_privatekey call
- BUG/MINOR: dns: SRV records ignores duplicated AR records
- DOC: fix "smp_size" vs "sample_size" in "log" directive arguments
- BUG/MEDIUM: mux_h2: Add missing braces in h2_snd_buf()around trace+wakeup
- BUILD: hpack: hpack-tbl-t.h uses VAR_ARRAY but does not include compiler.h
- MINOR: atomic: don't use ; to separate instruction on aarch64.
- BUG/MINOR: sink: Return an allocation failure in __sink_new if strdup() fails
- BUG/MINOR: cfgparse: Fail if the strdup() for `rule->be.name` for
  `use_backend` fails
- BUG/MINOR: tcpcheck: Report a L7OK if the last evaluated rule is a send rule
- DOC: Improve the message printed when running `make` w/o `TARGET`
- BUG/MINOR: stats: Make stat_l variable used to dump a stat line thread local
- SCRIPTS: improve announce-release to support different tag and versions
- SCRIPTS: make announce release support preparing announces before tag exists
- BUG/MINOR: srv: do not init address if backend is disabled
- BUG/MINOR: srv: do not cleanup idle conns if pool max is null
- MINOR: converter: adding support for url_enc
- BUILD: Makefile: exclude broken tests by default
- CLEANUP: cfgparse: replace "realloc" with "my_realloc2" to fix to memory
  leak on error
- MINOR: contrib/prometheus-exporter: export build_info
- DOC: fix some spelling issues over multiple files
- SCRIPTS: announce-release: fix typo in help message
- DOC: Add maintainers for the Prometheus exporter
- BUG/MINOR: sample: fix concat() converter's corruption with non-string
  variables

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- BUILD: http-htx: fix build warning regarding long type in printf
- CLEANUP: cfgparse: remove duplicate registration for transparent build options
- BUG/MEDIUM: filters: Forward all filtered data at the end of http filtering
- BUG/MINOR: http-ana: Don't wait for the body of CONNECT requests
- DOC: add missing 3.10 in the summary
- BUG/MINOR: ssl: segv on startup when AKID but no keyid
- BUG/MEDIUM: http-ana: Don't eval http-after-response ruleset on empty messages
- BUG/MEDIUM: ssl/crt-list: bundle support broken in crt-list
- BUG/MEDIUM: ssl: error when no certificate are found
- BUG/MINOR: ssl/crt-list: load bundle in crt-list only if activated
- BUG/MEDIUM: ssl/crt-list: fix error when no file found
- BUILD: makefile: enable crypt(3) for OpenBSD
- DOC: clarify how to create a fallback crt
- CLEANUP: connection: do not use conn->owner when the session is known
- BUG/MAJOR: connection: reset conn->owner when detaching from session list
- BUG/MINOR: http_htx: Fix searching headers by substring
- DOC: better describes how to configure a fallback crt
- BUG/MAJOR: filters: Always keep all offsets up to date during data filtering
- MEDIUM: cache: Change caching conditions
- DOC: cache: Add new caching limitation information
- REGTESTS: Add sample_fetches/cook.vtc
- REGTESTS: converter: add url_dec test
- MINOR: http_act: Add -m flag for del-header name matching method
- BUILD: Make DEBUG part of .build_opts
- BUILD: Show the value of DEBUG= in haproxy -vv
- BUG/MEDIUM: http_act: Restore init of log-format list
- BUG/MAJOR: peers: fix partial message decoding
- DOC: better document the config file format and escaping/quoting rules
- DOC: Clarify %%HP description in log-format
- BUG/MINOR: tcpcheck: Don't forget to reset tcp-check flags on new kind of
  check
- MINOR: tcpcheck: Don't handle anymore in-progress send rules in tcpcheck_main
- BUG/MAJOR: tcpcheck: Allocate input and output buffers from the buffer pool
- DOC: config: Move req.hdrs and req.hdrs_bin in L7 samples fetches section
- BUG/MINOR: http-fetch: Fix smp_fetch_body() when called from a health-check

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- BUG/MINOR: ssl: don't report 1024 bits DH param load error when it's higher
- MINOR: http-htx: Add understandable errors for the errorfiles parsing
- DOC: config: Fix a typo on ssl_c_chain_der
- BUG/MEDIUM: ssl/crt-list: correctly insert crt-list line if crt already loaded
- BUG/MINOR: pattern: a sample marked as const could be written
- BUG/MINOR: lua: set buffer size during map lookups
- BUG/MINOR: stats: free dynamically stats fields/lines on shutdown
- BUG/MINOR: peers: Do not ignore a protocol error for dictionary entries.
- BUG/MINOR: peers: Missing TX cache entries reset.
- BUG/MEDIUM: peers: fix decoding of multi-byte length in stick-table messages
- BUG/MINOR: http-fetch: Extract cookie value even when no cookie name
- BUG/MINOR: http-fetch: Fix calls w/o parentheses of the cookie sample fetches
- BUG/MEDIUM: check: reuse srv proto only if using same mode
- MINOR: check: report error on incompatible proto
- MINOR: check: report error on incompatible connect proto
- BUG/MINOR: http-htx: Handle warnings when parsing http-error and http-errors
- BUG/MAJOR: spoe: Be sure to remove all references on a released spoe applet
- MINOR: spoe: Don't close connection in sync mode on processing timeout
- BUG/MINOR: tcpcheck: Don't warn on unused rules if check option is after
- MINOR: init: Fix the prototype for per-thread free callbacks
- MINOR: config/mux-h2: Return ERR_ flags from init_h2() instead of a status
- MINOR: cfgparse: tighten the scope of newnameserver variable, free it on
  error.
- REGTEST: ssl: test wildcard and multi-type + exclusions
- REGTEST: ssl: mark reg-tests/ssl/ssl_crt-list_filters.vtc as broken
- MINOR: peers: Add traces to peer_treat_updatemsg().
- REGTEST: make ssl_client_samples and ssl_server_samples require to 2.2

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Initial build for kaos repository
