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

%define orig_name         haproxy
%define major_ver         22

%define hp_user           %{orig_name}
%define hp_user_id        188
%define hp_group          %{orig_name}
%define hp_group_id       188
%define hp_homedir        %{_localstatedir}/lib/%{orig_name}
%define hp_confdir        %{_sysconfdir}/%{orig_name}
%define hp_datadir        %{_datadir}/%{orig_name}

%define lua_ver           5.4.2
%define pcre_ver          8.44
%define openssl_ver       1.1.1k
%define ncurses_ver       6.2
%define readline_ver      8.1

################################################################################

Name:              %{orig_name}%{major_ver}
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           2.2.11
Release:           0%{?dist}
License:           GPLv2+
URL:               https://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           https://www.haproxy.org/download/2.2/src/%{orig_name}-%{version}.tar.gz
Source1:           %{orig_name}.init
Source2:           %{orig_name}.cfg
Source3:           %{orig_name}.logrotate
Source4:           %{orig_name}.sysconfig
Source5:           %{orig_name}.service

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

%setup -qn %{orig_name}-%{version}

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
                          ADDLIB="-ldl -lrt -lpthread" \
                          ${use_regparm}

pushd contrib/halog
  %{__make} halog
popd

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -pDm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{orig_name}
install -pDm 0644 %{SOURCE2} %{buildroot}%{hp_confdir}/%{orig_name}.cfg
install -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{orig_name}
install -pDm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{orig_name}

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/

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
  %{__sysctl} enable %{orig_name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  %{__sysctl} --no-reload disable %{orig_name}.service &>/dev/null || :
  %{__sysctl} stop %{orig_name}.service &>/dev/null || :
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
%config(noreplace) %{hp_confdir}/%{orig_name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{orig_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{orig_name}
%{hp_datadir}/*
%{_initrddir}/%{orig_name}
%{_unitdir}/%{orig_name}.service
%{_sbindir}/%{orig_name}
%{_bindir}/halog
%{_mandir}/man1/%{orig_name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.11-0
- BUG/MEDIUM: lists: Avoid an infinite loop in MT_LIST_TRY_ADDQ().
- BUG/MINOR: hlua: Don't strip last non-LWS char in hlua_pushstrippedstring()
- BUG/MINOR: ssl: don't truncate the file descriptor to 16 bits in debug mode
- BUG/MEDIUM: session: NULL dereference possible when accessing the listener
- BUG/MEDIUM: stick-tables: fix ref counter in table entry using
  multiple http tracksc.
- BUG/MEDIUM: filters: Set CF_FL_ANALYZE on channels when filters are attached
- BUG/MINOR: tcpcheck: Update .health threshold of agent inside an agent-check
- BUG/MINOR: proxy/session: Be sure to have a listener to increment its counters
- BUG/MINOR: session: Add some forgotten tests on session's listener
- BUG/MINOR: tcpcheck: Fix double free on error path when parsing tcp/http-check
- CLEANUP: tcp-rules: add missing actions in the tcp-request error message
- Revert "BUG/MINOR: resolvers: Only renew TTL for SRV records with
  an additional record"
- BUG/MINOR: resolvers: Consider server to have no IP on DNS resolution error
- BUG/MINOR: resolvers: Reset server address on DNS error only on status change
- BUG/MINOR: resolvers: Unlink DNS resolution to set RMAINT on SRV resolution
- BUG/MEDIUM: resolvers: Don't set an address-less server as UP
- BUG/MEDIUM: resolvers: Fix the loop looking for an existing ADD item
- MINOR: resolvers: new function find_srvrq_answer_record()
- BUG/MINOR; resolvers: Ignore DNS resolution for expired SRV item
- BUG/MEDIUM: resolvers: Trigger a DNS resolution if an ADD item is obsolete
- MINOR: resolvers: Use a function to remove answers attached to a resolution
- MINOR: resolvers: Purge answer items when a SRV resolution triggers an error
- MINOR: resolvers: Add function to change the srv status based on
  SRV resolution
- MINOR: resolvers: Directly call srvrq_update_srv_state() when possible
- BUG/MEDIUM: resolvers: Don't release resolution from a requester callbacks
- BUG/MEDIUM: resolvers: Skip DNS resolution at startup if SRV resolution is set
- MINOR: resolvers: Use milliseconds for cached items in resolver responses
- MINOR: resolvers: Don't try to match immediatly renewed ADD items
- BUG/MINOR: resolvers: Add missing case-insensitive comparisons
  of DNS hostnames
- MINOR: time: export the global_now variable
- BUG/MINOR: freq_ctr/threads: make use of the last updated global time

* Fri Mar 26 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.10-0
- MINOR: check: do not ignore a connection header for http-check send
- BUILD: ssl: fix typo in HAVE_SSL_CTX_ADD_SERVER_CUSTOM_EXT macro
- BUILD: ssl: guard SSL_CTX_add_server_custom_ext with special macro
- BUILD: ssl: guard SSL_CTX_set_msg_callback with
  SSL_CTRL_SET_MSG_CALLBACK macro
- BUG/MINOR: intops: fix mul32hi()'s off-by-one
- BUG/MINOR: http-ana: Don't increment HTTP error counter on internal errors
- BUG/MEDIUM: mux-h1: Always set CS_FL_EOI for response in MSG_DONE state
- BUG/MINOR: server: re-align state file fields number
- BUG/MINOR: tools: Fix a memory leak on error path in parse_dotted_uints()
- BUG/MINOR: backend: hold correctly lock when killing idle conn
- BUG/MINOR: server: Fix server-state-file-name directive
- CLEANUP: deinit: release global and per-proxy server-state variables on deinit
- BUG/MEDIUM: config: don't pick unset values from last defaults section
- BUG/MINOR: stats: revert the change on ST_CONVDONE
- BUG/MINOR: cfgparse: do not mention "addr:port" as supported on proxy lines
- BUG/MINOR: server: Don't call fopen() with server-state filepath set to NULL
- DOC: tune: explain the origin of block size for ssl.cachesize
- CLEANUP: channel: fix comment in ci_putblk.
- BUG/MINOR: server: Remove RMAINT from admin state when loading server state
- BUG/MINOR: session: atomically increment the tracked sessions counter
- BUG/MINOR: checks: properly handle wrapping time in __health_adjust()
- BUG/MINOR: sample: Always consider zero size string samples as unsafe
- BUILD: ssl: introduce fine guard for OpenSSL specific SCTL functions
- DOC: explain the relation between pool-low-conn and tune.idle-pool.shared
- BUG/MEDIUM: spoe: Resolve the sink if a SPOE logs in a ring buffer
- BUG/MINOR: http-rules: Always replace the response status on a return action
- BUG/MINOR: server: Init params before parsing a new server-state line
- BUG/MINOR: server: Be sure to cut the last parsed field of a server-state line
- BUG/MEDIUM: mux-h1: Fix handling of responses to CONNECT other than 200-ok
- BUG/MINOR: ssl/cli: potential null pointer dereference in "set ssl cert"
- MINOR: Configure the `cpp` userdiff driver for *.[ch] in .gitattributes
- BUG/MINOR: sample: secure convs that accept base64 string and var name as args
- BUG/MEDIUM: vars: make functions vars_get_by_{name,desc} thread-safe
- BUG/MEDIUM: proxy: use thread-safe stream killing on hard-stop
- BUG/MEDIUM: cli/shutdown sessions: make it thread-safe
- BUG/MINOR: proxy: wake up all threads when sending the hard-stop signal
- BUG/MINOR: fd: properly wait for !running_mask in fd_set_running_excl()
- BUG/MINOR: resolvers: Fix condition to release received ARs if not assigned
- BUG/MINOR: resolvers: Only renew TTL for SRV records with an additional record
- BUG/MINOR: resolvers: new callback to properly handle SRV record errors
- BUG/MEDIUM: resolvers: Reset server address and port for obselete SRV records
- BUG/MEDIUM: resolvers: Reset address for unresolved servers
- BUG/MINOR: ssl: potential null pointer dereference in ckchs_dup()
- CLEANUP: muxes: Remove useless if condition in show_fd function
- BUG/MINOR: mux-h1: Immediately report H1C errors from h1_snd_buf()
- BUG/MINOR: http-ana: Only consider dst address to process originalto option
- BUG/MINOR: tcp-act: Don't forget to set the original port for
  IPv4 set-dst rule
- BUG/MINOR: connection: Use the client's dst family for adressless servers
- BUG/MEDIUM: spoe: Kill applets if there are pending connections
  and nbthread > 1
- DOC: spoe: Add a note about fragmentation support in HAProxy
- BUG/MINOR: mux-h2: Fix typo in scheme adjustment
- BUG/MINOR: http-ana: Don't increment HTTP error counter on read error/timeout
- BUG/MEDIUM: checks: don't needlessly take the server lock in health_adjust()

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.9-0
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
- BUG/MEDIUM: mux-h2: fix read0 handling on partial frames
- BUILD/MINOR: lua: define _GNU_SOURCE for LLONG_MAX
- DOC: Improve documentation of the various hdr() fetches
- BUG/MEDIUM: filters/htx: Fix data forwarding when payload length is unknown
- BUG/MINOR: config: fix leak on proxy.conn_src.bind_hdr_name
- BUG/MINOR: ssl: init tmp chunk correctly in ssl_sock_load_sctl_from_file()
- MINOR: contrib: Make the wireshark peers dissector compile for more distribs.
- CLEANUP: tools: make resolve_sym_name() take a const pointer
- CLEANUP: cli: make "show fd" use a const connection to access other fields
- MINOR: cli: make "show fd" also report the xprt and xprt_ctx
- MINOR: xprt: add a new show_fd() helper to complete some "show fd" dumps.
- MINOR: ssl: provide a "show fd" helper to report important SSL information
- MINOR: xprt/mux: export all *_io_cb functions so that "show fd" resolves them
- MINOR: mux-h2: make the "show fd" helper also decode the h2s subscriber when
  known
- MINOR: mux-h1: make the "show fd" helper also decode the h1s subscriber when
  known
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
- BUG/MINOR: xxhash: make sure armv6 uses memcpy()
- BUILD: Makefile: move REGTESTST_TYPE default setting
- BUG/MEDIUM: mux-h2: handle remaining read0 cases
- BUG/MEDIUM: mux-h2: do not quit the demux loop before setting END_REACHED
- MINOR: cli/show_fd: report local and report ports when known
- MINOR: config: Deprecate and ignore tune.chksize global option
- BUG/MAJOR: connection: reset conn->owner when detaching from session list
- BUG/MEDIUM: lists: Lock the element while we check if it is in a list.
- MINOR: task: remove __tasklet_remove_from_tasklet_list()
- BUG/MEDIUM: task: close a possible data race condition on a tasklet's list
  link
- DOC: fix "smp_size" vs "sample_size" in "log" directive arguments
- BUG/MEDIUM: tcpcheck: Don't destroy connection in the wake callback context

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.8-0
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

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.7-0
- BUG/MINOR: lua: missing "\n" in error message
- BUG/MINOR: lua: lua-load doesn't check its parameters
- BUG/MINOR: lua: Post init register function are not executed beyond the first
  one
- BUG/MINOR: lua: Some lua init operation are processed unsafe
- MINOR: actions: Export actions lookup functions
- MINOR: actions: add a function returning a service pointer from its name
- MINOR: cli: add a function to look up a CLI service description
- BUG/MINOR: lua: warn when registering action, conv, sf, cli or applet multiple
  times
- BUG/MAJOR: ring: tcp forward on ring can break the reader counter.
- BUILD/MINOR: haproxy DragonFlyBSD affinity build update.
- DOC/MINOR: Fix formatting in Management Guide
- BUG/MINOR: mux-h1: Handle keep-alive timeout for idle frontend connections
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
- CLEANUP: contrib/prometheus-exporter: typo fixes for ssl reuse metric
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
- BUG/MEDIUM: mux_h2: Add missing braces in h2_snd_buf()around trace+wakeup
- BUILD: hpack: hpack-tbl-t.h uses VAR_ARRAY but does not include compiler.h
- MINOR: atomic: don't use ; to separate instruction on aarch64.
- BUG/MINOR: sink: Return an allocation failure in __sink_new if strdup() fails
- BUG/MINOR: cfgparse: Fail if the strdup() for `rule->be.name` for
  `use_backend` fails
- BUG/MINOR: tcpcheck: Report a L7OK if the last evaluated rule is a send rule
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

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.6-0
- BUG/MINOR: ssl: don't report 1024 bits DH param load error when it's higher
- MINOR: http-htx: Add understandable errors for the errorfiles parsing
- BUG/MINOR: http-htx: Just warn if payload of an errorfile doesn't match
  the C-L
- MINOR: ssl: add ssl_{c,s}_chain_der fetch methods
- BUG/MINOR: ssl: double free w/ smp_fetch_ssl_x_chain_der()
- DOC: config: Fix a typo on ssl_c_chain_der
- BUG/MINOR: pattern: a sample marked as const could be written
- BUG/MINOR: lua: set buffer size during map lookups
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
- REGTEST: make ssl_client_samples and ssl_server_samples require to 2.2
- MINOR: peers: Add traces to peer_treat_updatemsg().
- BUILD: http-htx: fix build warning regarding long type in printf
- BUG/MEDIUM: filters: Forward all filtered data at the end of http filtering
- BUG/MINOR: http-ana: Don't wait for the body of CONNECT requests
- BUG/MINOR: ssl: segv on startup when AKID but no keyid
- BUG/MEDIUM: http-ana: Don't eval http-after-response ruleset on empty messages
- DOC: clarify how to create a fallback crt
- BUG/MINOR: http_htx: Fix searching headers by substring
- DOC: better describes how to configure a fallback crt
- BUG/MAJOR: filters: Always keep all offsets up to date during data filtering
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
- MINOR: plock: use an ARMv8 instruction barrier for the pause instruction

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.5-0
- BUILD: ssl_crtlist: work around another bogus gcc-9.3 warning
- BUILD: makefile: Fix building with closefrom() support enabled
- MINOR: ssl: Add error if a crt-list might be truncated
- BUG/MINOR: Fix several leaks of 'log_tag' in init().
- DOC: tcp-rules: Refresh details about L7 matching for tcp-request content
  rules
- BUG/MINOR: tcpcheck: Set socks4 and send-proxy flags before the connect call
- BUG/MEDIUM: queue: make pendconn_cond_unlink() really thread-safe
- MINOR: ssl: Add warning if a crt-list might be truncated
- MINOR: counters: fix a typo in comment
- BUG/MINOR: stats: fix validity of the json schema
- MINOR: hlua: Display debug messages on stderr only in debug mode
- BUG/MINOR: peers: Inconsistency when dumping peer status codes.
- BUG/MINOR: mux-h1: Be sure to only set CO_RFL_READ_ONCE for the first read
- BUG/MINOR: mux-h1: Always set the session on frontend h1 stream
- DOC: fix a confusing typo on a regsub example
- DOC: Add missing stats fields in the management doc
- BUG/MEDIUM: mux-fcgi: Don't handle pending read0 too early on streams
- BUG/MEDIUM: mux-h2: Don't handle pending read0 too early on streams
- DOC: Fix typos in configuration.txt
- BUG/MINOR: http: Fix content-length of the default 500 error
- BUG/MINOR: http-htx: Expect no body for 204/304 internal HTTP responses
- CLEANUP: tree-wide: use VAR_ARRAY instead of [0] in various definitions
- BUILD: connection: fix build on clang after the VAR_ARRAY cleanup
- BUG/MINOR: init: only keep rlim_fd_cur if max is unlimited
- BUG/MINOR: mux-h2: do not stop outgoing connections on stopping
- MINOR: fd: report an error message when failing initial allocations
- BUG/MINOR: connection: fix loop iter on connection takeover
- BUG/MEDIUM: task: bound the number of tasks picked from the wait queue at once
- BUG/MEDIUM: spoe: Unset variable instead of set it if no data provided
- BUG/MEDIUM: mux-h1: Get the session from the H1S when capturing bad messages
- BUG/MEDIUM: lb: Always lock the server when calling server_{take,drop}_conn
- DOC: fix typo in MAX_SESS_STKCTR
- BUG/MINOR: peers: Possible unexpected peer seesion reset after collisions.
- BUG/MINOR: disable dynamic OCSP load with BoringSSL
- BUILD: ssl: make BoringSSL use its own version numbers
- MINOR: ssl: 'ssl-load-extra-del-ext' removes the certificate extension
- BUG/MINOR: queue: properly report redistributed connections
- BUG/MEDIUM: server: support changing the slowstart value from state-file
- BUG/MINOR: http-ana: Don't send payload for internal responses to HEAD
  requests
- BUG/MAJOR: mux-h2: Don't try to send data if we know it is no longer possible
- Revert "MINOR: ssl: 'ssl-load-extra-del-ext' removes the certificate
  extension"
- BUG/MEDIUM: ssl: OCSP must work with BoringSSL
- BUG/MINOR: extcheck: add missing checks on extchk_setenv()
- BUG/MINOR: log: fix memory leak on logsrv parse error
- BUG/MINOR: log: fix risk of null deref on error path
- BUG/MINOR: server: fix srv downtime calcul on starting
- BUG/MINOR: server: fix down_time report for stats
- BUG/MINOR: lua: initialize sample before using it
- MINOR: ist: Add a case insensitive istmatch function
- BUG/MINOR: cache: Manage multiple values in cache-control header value
- BUG/MINOR: cache: Inverted variables in http_calc_maxage function
- BUG/MEDIUM: filters: Don't try to init filters for disabled proxies
- BUG/MINOR: proxy/server: Skip per-proxy/server post-check for disabled proxies
- BUG/MINOR: checks: Report a socket error before any connection attempt
- BUG/MINOR: server: Set server without addr but with dns in RMAINT on startup
- MINOR: server: Copy configuration file and line for server templates
- BUG/MEDIUM: mux-pt: Release the tasklet during an HTTP upgrade
- BUG/MINOR: filters: Skip disabled proxies during startup only
- BUG/MEDIUM: stick-table: limit the time spent purging old entries
- CLEANUP: mux-h2: Remove the h1 parser state from the h2 stream
- BUG/MEDIUM: server: make it possible to kill last idle connections

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.4-0
- BUILD: threads: better workaround for late loading of libgcc_s
- BUG/MEDIUM: pattern: Renew the pattern expression revision when it is pruned
- BUG/MINOR: Fix type passed of sizeof() for calloc()
- BUG/MINOR: ssl: verifyhost is case sensitive
- BUG/MINOR: server: report correct error message for invalid port on "socks4"
- BUG/MEDIUM: ssl: Don't call ssl_sock_io_cb() directly.
- BUG/MINOR: ssl/crt-list: crt-list could end without a \n
- BUG/MINOR: h2/trace: do not display "stream error" after a frame ACK
- BUG/MINOR: http-fetch: Don't set the sample type during the htx prefetch
- BUG/MINOR: config: Fix memory leak on config parse listen
- BUG/MEDIUM: h2: report frame bits only for handled types
- BUG/MINOR: Fix memory leaks cfg_parse_peers
- MINOR: h2/trace: also display the remaining frame length in traces
- MINOR: backend: make the "whole" option of balance uri take only one bit
- MINOR: backend: add a new "path-only" option to "balance uri"
- REGTESTS: add a few load balancing tests
- BUG/MEDIUM: listeners: do not pause foreign listeners
- BUILD: trace: include tools.h
- REGTESTS: use "command" instead of "which" for better POSIX compatibility
- DOC: agent-check: fix typo in "fail" word expected reply
- BUG/MINOR: ssl/crt-list: exit on warning out of crtlist_parse_line()
- REGTEST: fix host part in balance-uri-path-only.vtc
- REGTEST: make agent-check.vtc require 1.8
- REGTEST: make abns_socket.vtc require 1.8
- REGTEST: make map_regm_with_backref require 1.7

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.3-0
- SCRIPTS: git-show-backports: make -m most only show the left branch
- SCRIPTS: git-show-backports: emit the shell command to backport a commit
- BUG/MEDIUM: mux-h1: Refresh H1 connection timeout after a synchronous send
- CLEANUP: dns: typo in reported error message
- BUG/MAJOR: dns: disabled servers through SRV records never recover
- BUG/MINOR: spoa-server: fix size_t format printing
- DOC: spoa-server: fix false friends `actually`
- BUG/MINOR: ssl: fix memory leak at OCSP loading
- BUG/MEDIUM: ssl: memory leak of ocsp data at SSL_CTX_free()
- BUG/MEDIUM: map/lua: Return an error if a map is loaded during runtime
- MINOR: arg: Add an argument type to keep a reference on opaque data
- BUG/MINOR: converters: Store the sink in an arg pointer for debug() converter
- BUG/MINOR: lua: Duplicate map name to load it when a new Map object is created
- BUG/MINOR: arg: Fix leaks during arguments validation for fetches/converters
- BUG/MINOR: lua: Check argument type to convert it to IPv4/IPv6 arg validation
- BUG/MINOR: lua: Check argument type to convert it to IP mask in arg validation
- MINOR: hlua: Don't needlessly copy lua strings in trash during args validation
- BUG/MINOR: lua: Duplicate lua strings in sample fetches/converters arg array
- MEDIUM: lua: Don't filter exported fetches and converters
- BUG/MINOR: snapshots: leak of snapshots on deinit()
- BUG/MEDIUM: ssl: fix the ssl-skip-self-issued-ca option
- BUG/MINOR: ssl: ssl-skip-self-issued-ca requires >= 1.0.2
- BUG/MINOR: stats: use strncmp() instead of memcmp() on health states
- BUG/MEDIUM: htx: smp_prefetch_htx() must always validate the direction
- BUG/MEDIUM: ssl: never generates the chain from the verify store
- BUG/MEDIUM: ssl: fix ssl_bind_conf double free w/ wildcards
- BUG/MINOR: reload: do not fail when no socket is sent
- BUG/MEDIUM: http-ana: Don't wait to send 1xx responses received from servers
- MINOR: http-htx: Add an option to eval query-string when the path is replaced
- BUG/MINOR: http-rules: Replace path and query-string in "replace-path" action
- BUG/MEDIUM: ssl: crt-list negative filters don't work
- DOC: cache: Use '<name>' instead of '<id>' in error message
- MINOR: cache: Reject duplicate cache names
- BUILD: tools: include auxv a bit later
- BUILD: task: work around a bogus warning in gcc 4.7/4.8 at -O1
- BUG/MAJOR: contrib/spoa-server: Fix unhandled python call leading to memory
  leak
- BUG/MINOR: contrib/spoa-server: Ensure ip address references are freed
- BUG/MINOR: contrib/spoa-server: Do not free reference to NULL
- BUG/MINOR: contrib/spoa-server: Updating references to free in case of failure
- BUG/MEDIUM: contrib/spoa-server: Fix ipv4_address used instead of ipv6_address
- BUG/MINOR: startup: haproxy -s cause 100% cpu
- Revert "BUG/MINOR: http-rules: Replace path and query-string in "replace-path"
  action"
- BUG/MEDIUM: doc: Fix replace-path action description
- MINOR: http-rules: Add set-pathq and replace-pathq actions
- MINOR: http-fetch: Add pathq sample fetch
- REGTEST: Add a test for request path manipulations, with and without the QS
- BUG/MEDIUM: ssl: check OCSP calloc in ssl_sock_load_ocsp()
- MINOR: arg: Use chunk_destroy() to release string arguments
- BUG/MEDIUM: ssl: does not look for all SNIs before chosing a certificate
- BUG/MINOR: threads: work around a libgcc_s issue with chrooting
- BUILD: thread: limit the libgcc_s workaround to glibc only
- MINOR: Commit .gitattributes
- CLEANUP: Update .gitignore
- CLEANUP: dns: remove 45 "return" statements from dns_validate_dns_response()
- BUG/MEDIUM: dns: Don't store additional records in a linked-list
- BUG/MEDIUM: dns: Be sure to renew IP address for already known servers
- MINOR: server: Improve log message sent when server address is updated
- DOC: ssl-load-extra-files only applies to certificates on bind lines
- BUG/MINOR: auth: report valid crypto(3) support depending on build options
- BUG/MEDIUM: mux-h1: always apply the timeout on half-closed connections

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-0
- BUG/MINOR: mux-fcgi: Don't url-decode the QUERY_STRING parameter anymore
- BUILD: tools: fix build with static only toolchains
- BUG/MINOR: debug: Don't dump the lua stack if it is not initialized
- BUG/MAJOR: dns: fix null pointer dereference in snr_update_srv_status
- BUG/MAJOR: dns: don't treat Authority records as an error
- MEDIUM: lua: Add support for the Lua 5.4
- BUG/MEDIUM: dns: Don't yield in do-resolve action on a final evaluation
- BUG/MINOR: lua: Abort execution of actions that yield on a final evaluation
- BUG/MINOR: tcp-rules: Preserve the right filter analyser on content eval abort
- BUG/MINOR: tcp-rules: Set the inspect-delay when a tcp-response action yields
- BUG/MEDIUM: connection: Be sure to always install a mux for sync connect
- MINOR: connection: Preinstall the mux for non-ssl connect
- MINOR: stream-int: Be sure to have a mux to do sends and receives
- SCRIPTS: announce-release: add the link to the wiki in the announce messages
- BUG/MEDIUM: backend: always attach the transport before installing the mux
- BUG/MEDIUM: tcp-checks: always attach the transport before installing the mux

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- BUG/MINOR: sample: Free str.area in smp_check_const_bool
- BUG/MINOR: sample: Free str.area in smp_check_const_meth
- BUG/MEDIUM: lists: add missing store barrier on MT_LIST_BEHEAD()
- BUG/MEDIUM: lists: add missing store barrier in MT_LIST_ADD/MT_LIST_ADDQ
- CONTRIB: da: fix memory leak in dummy function da_atlas_open()
- BUG/MEDIUM: mux-h2: Don't add private connections in available connection list
- BUG/MEDIUM: mux-fcgi: Don't add private connections in available connection
  list
- BUG/MEDIUM: mux-h1: Continue to process request when switching in tunnel mode
- BUG/MINOR: mux-fcgi: Handle empty STDERR record
- BUG/MINOR: mux-fcgi: Set conn state to RECORD_P when skipping the record
  padding
- BUG/MINOR: mux-fcgi: Set flags on the right stream field for empty FCGI_STDOUT
- BUG/MEDIUM: log: issue mixing sampled to not sampled log servers.
- BUG/MEDIUM: fcgi-app: fix memory leak in fcgi_flt_http_headers
- BUG/MEDIUM: server: resolve state file handle leak on reload
- BUG/MEDIUM: server: fix possibly uninitialized state file on close
- BUG/MEDIUM: channel: Be aware of SHUTW_NOW flag when output data are peeked
- BUILD: config: address build warning on raspbian+rpi4
- BUG/MAJOR: tasks: make sure to always lock the shared wait queue if needed
- BUILD: config: fix again bugs gcc warnings on calloc
- DOC: ssl: req_ssl_sni needs implicit TLS
- BUG/MEDIUM: arg: empty args list must be dropped
- BUG/MEDIUM: resolve: fix init resolving for ring and peers section.
- BUG/MAJOR: tasks: don't requeue global tasks into the local queue
- BUG/MAJOR: dns: Make the do-resolve action thread-safe
- BUG/MEDIUM: dns: Release answer items when a DNS resolution is freed
- MEDIUM: htx: Add a flag on a HTX message when no more data are expected
- BUG/MINOR: htx: add two missing HTX_FL_EOI and remove an unexpected one
- BUG/MEDIUM: stream-int: Don't set MSG_MORE flag if no more data are expected
- BUG/MEDIUM: http-ana: Only set CF_EXPECT_MORE flag on data filtering

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Initial build for kaos repository
