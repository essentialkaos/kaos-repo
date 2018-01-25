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

%define pcre_ver          8.40
%define boringssl_ver     664e99a6486c293728097c661332f92bf2d847c6

################################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.5.19
Release:           3%{?dist}
License:           GPLv2+
Group:             System Environment/Daemons
URL:               http://haproxy.1wt.eu

Source0:           http://www.haproxy.org/download/1.5/src/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.cfg
Source3:           %{name}.logrotate
Source4:           %{name}.sysconfig
Source5:           %{name}.service

Source10:          http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{pcre_ver}.tar.gz
Source11:          https://boringssl.googlesource.com/boringssl/+archive/%{boringssl_ver}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make zlib-devel

%if 0%{?rhel} >= 7
BuildRequires:     gcc gcc-c++
%else
BuildRequires:     devtoolset-2-gcc-c++ devtoolset-2-binutils
%endif

Requires:          setup >= 2.8.14-14 kaosv >= 2.10

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

%{__tar} xzvf %{SOURCE10}
%{__tar} xzvf %{SOURCE11} -C boringssl

%build

%if 0%{?rhel} < 7
# Use gcc and gcc-c++ from devtoolset for build on CentOS6
export PATH="/opt/rh/devtoolset-2/root/usr/bin:$PATH"
%endif

### DEPS BUILD START ###

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

cp boringssl/build/crypto/libcrypto.a boringssl/build/ssl/libssl.a boringssl/.openssl/lib

# Static PCRE build
pushd pcre-%{pcre_ver}
  mkdir build
  ./configure --prefix=$(pwd)/build --enable-shared=no --enable-utf8 --enable-jit
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
                          SSL_INC=libressl-%{libre_ver}/build/include \
                          SSL_LIB=libressl-%{libre_ver}/build/lib \
                          USE_PCRE_JIT=1 \
                          USE_STATIC_PCRE=1 \
                          PCRE_INC=pcre-%{pcre_ver}/build/include \
                          PCRE_LIB=pcre-%{pcre_ver}/build/lib \
                          USE_ZLIB=1 \
                          ADDLIB="-ldl -lrt" \
                          ${use_regparm}

pushd contrib/halog
  %{__make} halog
popd

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

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
  %{__chkconfig} --del %{name}
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
%doc examples/url-switching.cfg
%doc examples/acl-content-sw.cfg
%doc examples/content-sw-sample.cfg
%doc examples/cttproxy-src.cfg
%doc examples/haproxy.cfg
%doc examples/tarpit.cfg
%dir %{hp_datadir}
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif
%{hp_datadir}/*
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

################################################################################

%changelog
* Thu Nov 30 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.19-3
- Migrated from LibreSSL to BoringSSL

* Thu Sep 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.19-2
- Fixed systemd ExecReload handler

* Mon Aug 14 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.19-1
- Added ExecReload handler to systemd unit

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.19-0
- BUG/MAJOR: fix listening IP address storage for frontends
- CLEANUP: connection: fix double negation on memcmp()
- BUG/MEDIUM: sticktables: segfault in some configuration error cases
- BUG/MINOR: http: add-header: header name copied twice
- BUG/MINOR: ssl: fix potential memory leak in ssl_sock_load_dh_params()
- BUG/MINOR: http: url32+src should use the big endian version of url32
- BUG/MINOR: http: url32+src should check cli_conn before using it
- DOC: http: add documentation for url32 and url32+src
- MINOR: systemd: Use variable for config and pidfile paths
- MINOR: systemd: Perform sanity check on config before reload
- BUG/MINOR: init: always ensure that global.rlimit_nofile matches actual limits
- BUG/MINOR: init: ensure that FD limit is raised to the max allowed
- Revert "BUG/MINOR: ssl: fix potential memory leak in ssl_sock_load_dh_params()"
- BUG/MEDIUM: stream-int: completely detach connection on connect error
- DOC: minor typo fixes to improve HTML parsing by haproxy-dconv
- BUG/MAJOR: compression: initialize avail_in/next_in even during flush
- BUG/MAJOR: stick-counters: possible crash when using sc_trackers with wrong table
- BUG/MAJOR: stream: properly mark the server address as unset on connect retry
- BUG/MINOR: payload: fix SSLv2 version parser
- MINOR: cli: allow the semi-colon to be escaped on the CLI
- BUG/MINOR: displayed PCRE version is running release
- MINOR: show Built with PCRE version
- MINOR: show Running on zlib version
- BUG/MINOR: ssl: Check malloc return code
- BUG/MINOR: ssl: prevent multiple entries for the same certificate
- BUG/MINOR: systemd: make the wrapper return a non-null status code on error
- BUILD/CLEANUP: systemd: avoid a warning due to mixed code and declaration
- BUG/MINOR: systemd: always restore signals before execve()
- BUG/MINOR: systemd: check return value of calloc()
- MINOR: systemd: report it when execve() fails
- BUG/MEDIUM: systemd: let the wrapper know that haproxy has completed or failed
- BUILD: poll: remove unused hap_fd_isset() which causes a warning with clang
- DOC: Fix typo in description of `-st` parameter in man page
- BUG/MEDIUM: peers: fix use after free in peer_session_create()
- BUG/MEDIUM: systemd-wrapper: return correct exit codes
- BUG/MINOR: stick-table: handle out-of-memory condition gracefully
- BUG/MEDIUM: connection: check the control layer before stopping polling
- BUG/MEDIUM: stick-table: fix regression caused by recent fix for out-of-memory
- BUG/MINOR: cli: properly decrement ref count on tables during failed dumps
- BUG/MINOR: cli: fix pointer size when reporting data/transport layer name
- BUG/MINOR: cli: dequeue from the proxy when changing a maxconn
- BUG/MEDIUM: proxy: return "none" and "unknown" for unknown LB algos
- BUG/MINOR: http: don't send an extra CRLF after a Set-Cookie in a redirect
- DOC: fix small typo in fe_id (backend instead of frontend)
- BUG/MEDIUM: ssl: properly reset the reused_sess during a forced handshake
- BUG/MINOR: backend: nbsrv() should return 0 if backend is disabled
- BUG/MINOR: systemd: potential zombie processes

* Thu Nov 24 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.18-2
- Init script rewritten with kaosv usage
- Added systemd support
- Added LibreSSL and PCRE usage

* Tue Nov 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.18-1
- Improved SSL preferences in configuration file

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.18-0
- DOC: Clarify IPv4 address / mask notation rules
- CLEANUP: fix inconsistency between fd->iocb, proto->accept and accept()
- BUG/MEDIUM: fix maxaccept computation on per-process listeners
- BUG/MINOR: listener: stop unbound listeners on startup
- BUG/MINOR: fix maxaccept computation according to the frontend process range
- MEDIUM: unblock signals on startup.
- BUG/MEDIUM: channel: don't allow to overwrite the reserve until connected
- BUG/MEDIUM: channel: incorrect polling condition may delay event delivery
- BUG/MEDIUM: channel: fix miscalculation of available buffer space (3rd try)
- MINOR: channel: add new function channel_congested()
- BUG/MEDIUM: http: fix risk of CPU spikes with pipelined requests from dead client
- BUG/MAJOR: channel: fix miscalculation of available buffer space (4th try)
- BUG/MEDIUM: stream: ensure the SI_FL_DONT_WAKE flag is properly cleared
- BUG/MEDIUM: channel: fix inconsistent handling of 4GB-1 transfers
- MINOR: stats: fix typo in help messages

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.17-0
- BUG/MINOR: log: Don't use strftime() which can clobber timezone if chrooted
- BUG/MINOR: conf: "listener id" expects integer, but its not checked
- BUG/MAJOR: Fix crash in http_get_fhdr with exactly MAX_HDR_HISTORY headers
- DOC: "addr" parameter applies to both health and agent checks
- DOC: timeout client: pointers to timeout http-request
- DOC: typo on stick-store response
- DOC: typo: ACL subdir match
- DOC: typo: maxconn paragraph is wrong due to a wrong buffer size
- DOC: typo: req.uri is now replaced by capture.req.uri
- DOC: fix "needed" typo
- BUG/MINOR : allow to log cookie for tarpit and denied request
- BUG/MAJOR: channel: fix miscalculation of available buffer space (2nd try)
- DOC: fix discrepancy in the example for http-request redirect

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.16-0
- BUG/BUILD: replace haproxy-systemd-wrapper with $(EXTRA) in install-bin.
- BUG/MINOR: acl: don't use record layer in req_ssl_ver
- BUG: http: do not abort keep-alive connections on server timeout
- BUG/MEDIUM: http: switch the request channel to no-delay once done.
- MINOR: config: extend the default max hostname length to 64 and beyond
- BUG/MEDIUM: http: don't enable auto-close on the response side
- BUG/MEDIUM: stream: fix half-closed timeout handling
- BUG/MEDIUM: cli: changing compression rate-limiting must require admin level
- BUILD: freebsd: double declaration
- BUG/MEDIUM: sample: urlp can't match an empty value
- BUG/MEDIUM: peers: table entries learned from a remote are pushed to others after a random delay.
- BUG/MEDIUM: peers: old stick table updates could be repushed.
- CLEANUP: haproxy: using _GNU_SOURCE instead of __USE_GNU macro.
- BUG/MINOR: chunk: make chunk_dup() always check and set dst->size
- MINOR: chunks: ensure that chunk_strcpy() adds a trailing zero
- MINOR: chunks: add chunk_strcat() and chunk_newstr()
- MINOR: chunk: make chunk_initstr() take a const string
- BUG/MEDIUM: config: Adding validation to stick-table expire value.
- BUG/MEDIUM: sample: http_date() doesn't provide the right day of the week
- BUG/MEDIUM: channel: fix miscalculation of available buffer space.
- BUG/MINOR: stream: don't force retries if the server is DOWN
- MINOR: unix: don't mention free ports on EAGAIN
- BUG/CLEANUP: CLI: report the proper field states in "show sess"
- MINOR: stats: send content-length with the redirect to allow keep-alive
- BUG: stream_interface: Reuse connection even if the output channel is empty
- DOC: remove old tunnel mode assumptions
- DOC: add server name at rate-limit sessions example
- BUG/MEDIUM: ssl: fix off-by-one in ALPN list allocation
- BUG/MEDIUM: ssl: fix off-by-one in NPN list allocation
- BUG/MEDIUM: stats: stats bind-process doesn't propagate the process mask correctly
- BUG/MINOR: http: Be sure to process all the data received from a server
- BUG/MEDIUM: chunks: always reject negative-length chunks
- BUG/MINOR: systemd: ensure we don't miss signals
- BUG/MINOR: systemd: report the correct signal in debug message output
- BUG/MINOR: systemd: propagate the correct signal to haproxy
- MINOR: systemd: ensure a reload doesn't mask a stop
- CLEANUP: stats: Avoid computation with uninitialized bits.
- CLEANUP: pattern: Ignore unknown samples in pat_match_ip().
- CLEANUP: map: Avoid memory leak in out-of-memory condition.
- BUG/MINOR: tcpcheck: conf parsing error when no port configured on server and last rule is a CONNECT with no port
- BUG/MINOR: tcpcheck: fix incorrect list usage resulting in failure to load certain configs
- MINOR: cfgparse: warn when uid parameter is not a number
- MINOR: cfgparse: warn when gid parameter is not a number
- BUG/MINOR: standard: Avoid free of non-allocated pointer
- BUG/MINOR: pattern: Avoid memory leak on out-of-memory condition
- CLEANUP: http: fix a build warning introduced by a recent fix
- BUG/MINOR: log: GMT offset not updated when entering/leaving DST

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.15-0
- BUG/MINOR: log: missing some ARGC_* entries in fmt_directives()
- DOC: usesrc root privileges requirements
- BUILD: ssl: Allow building against libssl without SSLv3.
- DOC/MINOR: fix OpenBSD versions where haproxy works
- BUG/MINOR: http/sample: gmtime/localtime can fail
- DOC: typo in 'redirect', 302 code meaning
- DOC: mention that ms is left-padded with zeroes.
- CLEANUP: .gitignore: ignore more test files
- CLEANUP: .gitignore: finally ignore everything but what is known.
- MEDIUM: config: emit a warning on a frontend without listener
- BUG/MEDIUM: counters: ensure that src_{inc,clr}_gpc0 creates a missing entry
- DOC: ssl: missing LF
- DOC: fix example of http-request using ssl_fc_session_id
- BUG/MINOR: http: remove stupid HTTP_METH_NONE entry
- BUG/MAJOR: http: don't call http_send_name_header() after an error
- BUG/MINOR: tools: make str2sa_range() report unresolvable addresses
- BUG/MEDIUM: acl: always accept match "found"
- DOC: clarify how to make use of abstract sockets in socat
- CLEANUP: config: make the errorloc/errorfile messages less confusing
- BUG/MINOR: config: check that tune.bufsize is always positive
- BUG/MEDIUM: proxy: ignore stopped peers
- BUG/MEDIUM: proxy: do not wake stopped proxies' tasks during soft_stop()
- BUG/MINOR: http: Add OPTIONS in supported http methods (found by find_http_meth)
- BUILD: enable build on Linux/s390x
- DOC: backend section missing parameters
- DOC: stats paramaters available in frontend
- BUG/MINOR: config: make the stats socket pass the correct proxy to the parsers
- BUG/MEDIUM: pattern: fixup use_after_free in the pat_ref_delete_by_id
- CLEANUP: don't ignore debian/ directory if present
- FIX: small typo in an example using the "Referer" header
- BUG/MEDIUM: config: count memory limits on 64 bits, not 32
- DOC: add a CONTRIBUTING file

* Mon Oct 26 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.14-1
- Improved default config

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.14-0
- BUILD/MINOR: tools: rename popcount to my_popcountl
- BUG/MAJOR: buffers: make the buffer_slow_realign() function respect output data

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.13-0
- BUG/MINOR: check: fix tcpcheck error message
- CLEANUP: deinit: remove codes for cleaning p->block_rules
- DOC: Update doc about weight, act and bck fields in the statistics
- MINOR: ssl: add a destructor to free allocated SSL ressources
- BUG/MEDIUM: ssl: fix tune.ssl.default-dh-param value being overwritten
- MEDIUM: ssl: replace standards DH groups with custom ones
- BUG/MINOR: debug: display (null) in place of "meth"
- BUG/MINOR: cfgparse: fix typo in 'option httplog' error message
- BUG/MEDIUM: cfgparse: segfault when userlist is misused
- BUG/MEDIUM: stats: properly initialize the scope before dumping stats
- BUG/MEDIUM: http: don't forward client shutdown without NOLINGER except for tunnels
- CLEANUP: checks: fix double usage of cur / current_step in tcp-checks
- BUG/MEDIUM: checks: do not dereference head of a tcp-check at the end
- CLEANUP: checks: simplify the loop processing of tcp-checks
- BUG/MAJOR: checks: always check for end of list before proceeding
- BUG/MEDIUM: checks: do not dereference a list as a tcpcheck struct
- BUG/MEDIUM: peers: apply a random reconnection timeout
- BUG/MINOR: ssl: fix smp_fetch_ssl_fc_session_id
- MEDIUM: init: don't stop proxies in parent process when exiting
- MINOR: peers: store the pointer to the signal handler
- MEDIUM: peers: unregister peers that were never started
- MEDIUM: config: propagate the table's process list to the peers sections
- MEDIUM: init: stop any peers section not bound to the correct process
- MEDIUM: config: validate that peers sections are bound to exactly one process
- MAJOR: peers: allow peers section to be used with nbproc > 1
- DOC: relax the peers restriction to single-process
- CLEANUP: config: fix misleading information in error message.
- MINOR: config: report the number of processes using a peers section in the error case
- BUG/MEDIUM: config: properly compute the default number of processes for a proxy

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.12-0
- BUG/MINOR: ssl: Display correct filename in error message
- DOC: Fix L4TOUT typo in documentation
- BUG/MEDIUM: Do not consider an agent check as failed on L7 error
- BUG/MINOR: pattern: error message missing
- BUG/MEDIUM: pattern: some entries are not deleted with case insensitive match
- BUG/MEDIUM: buffer: one byte miss in buffer free space check
- BUG/MAJOR: http: don't read past buffer's end in http_replace_value
- BUG/MEDIUM: http: the function "(req|res)-replace-value" doesn't respect the HTTP syntax
- BUG/MEDIUM: peers: correctly configure the client timeout
- BUG/MINOR: compression: consider the expansion factor in init
- BUG/MEDIUM: http: hdr_cnt would not count any header when called without name
- BUG/MEDIUM: listener: don't report an error when resuming unbound listeners
- BUG/MEDIUM: init: don't limit cpu-map to the first 32 processes only
- BUG/MEDIUM: stream-int: always reset si->ops when si->end is nullified
- BUG/MEDIUM: http: remove content-length from chunked messages
- DOC: http: update the comments about the rules for determining transfer-length
- BUG/MEDIUM: http: do not restrict parsing of transfer-encoding to HTTP/1.1
- BUG/MEDIUM: http: incorrect transfer-coding in the request is a bad request
- BUG/MEDIUM: http: remove content-length form responses with bad transfer-encoding
- MEDIUM: http: restrict the HTTP version token to 1 digit as per RFC7230
- MEDIUM: http: add option-ignore-probes to get rid of the floods of 408
- BUG/MINOR: config: clear proxy->table.peers.p for disabled proxies
- MINOR: stick-table: don't attach to peers in stopped state
- MEDIUM: config: initialize stick-tables after peers, not before
- MEDIUM: peers: add the ability to disable a peers section
- DOC: document option http-ignore-probes
- DOC: fix the comments about the meaning of msg->sol in HTTP
- BUG/MEDIUM: http: wait for the exact amount of body bytes in wait_for_request_body
- BUG/MAJOR: http: prevent risk of reading past end with balance url_param
- DOC: update the doc on the proxy protocol

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.11-0
- BUG/MEDIUM: backend: correctly detect the domain when use_domain_only is used
- MINOR: ssl: load certificates in alphabetical order
- BUG/MINOR: checks: prevent http keep-alive with http-check expect
- BUG/MEDIUM: Do not set agent health to zero if server is disabled in config
- MEDIUM/BUG: Only explicitly report "DOWN (agent)" if the agent health is zero
- BUG/MINOR: stats:Fix incorrect printf type.
- DOC: add missing entry for log-format and clarify the text
- BUG/MEDIUM: http: fix header removal when previous header ends with pure LF
- BUG/MEDIUM: channel: fix possible integer overflow on reserved size computation
- BUG/MINOR: channel: compare to_forward with buf->i, not buf->size
- MINOR: channel: add channel_in_transit()
- MEDIUM: channel: make buffer_reserved() use channel_in_transit()
- MEDIUM: channel: make bi_avail() use channel_in_transit()
- BUG/MEDIUM: channel: don't schedule data in transit for leaving until connected
- BUG/MAJOR: log: don't try to emit a log if no logger is set
- BUG/MINOR: args: add missing entry for ARGT_MAP in arg_type_names
- BUG/MEDIUM: http: make http-request set-header compute the string before removal
- BUG/MINOR: http: fix incorrect header value offset in replace-hdr/replace-value
- BUG/MINOR: http: abort request processing on filter failure

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.10-0
- DOC: fix a few typos
- BUG/MINOR: http: fix typo: "401 Unauthorized" => "407 Unauthorized"
- BUG/MINOR: parse: refer curproxy instead of proxy
- DOC: httplog does not support 'no'
- MINOR: map/acl/dumpstats: remove the "Done." message
- BUG/MEDIUM: sample: fix random number upper-bound
- BUG/MEDIUM: patterns: previous fix was incomplete
- BUG/MEDIUM: payload: ensure that a request channel is available
- BUG/MINOR: tcp-check: don't condition data polling on check type
- BUG/MEDIUM: tcp-check: don't rely on random memory contents
- BUG/MEDIUM: tcp-checks: disable quick-ack unless next rule is an expect
- BUG/MINOR: config: fix typo in condition when propagating process binding
- BUG/MEDIUM: config: do not propagate processes between stopped processes
- BUG/MAJOR: stream-int: properly check the memory allocation return
- BUG/MEDIUM: memory: fix freeing logic in pool_gc2()
- BUG/MEDIUM: compression: correctly report zlib_mem

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.9-0
- BUILD: fix "make install" to support spaces in the install dirs
- BUG/MEDIUM: checks: fix conflicts between agent checks and ssl healthchecks
- BUG/MEDIUM: ssl: fix bad ssl context init can cause segfault in case of OOM.
- BUG/MINOR: samples: fix unnecessary memcopy converting binary to string.
- BUG/MEDIUM: connection: sanitize PPv2 header length before parsing address information
- BUG/MEDIUM: pattern: don't load more than once a pattern list.
- BUG/MEDIUM: ssl: force a full GC in case of memory shortage
- BUG/MINOR: config: don't inherit the default balance algorithm in frontends
- BUG/MAJOR: frontend: initialize capture pointers earlier
- BUG/MINOR: stats: correctly set the request/response analysers
- DOC: fix typo in the body parser documentation for msg.sov
- BUG/MINOR: peers: the buffer size is global.tune.bufsize, not trash.size
- MINOR: sample: add a few basic internal fetches (nbproc, proc, stopping)
- BUG/MAJOR: sessions: unlink session from list on out of memory

* Thu Nov 06 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.8-0
- BUG/MAJOR: buffer: check the space left is enough or not when input data in a buffer is wrapped
- BUG/BUILD: revert accidental change in the makefile from latest SSL fix

* Thu Oct 23 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.6-0
- BUG/MEDIUM: systemd: set KillMode to 'mixed'
- MINOR: systemd: Check configuration before start
- BUG/MEDIUM: config: avoid skipping disabled proxies
- BUG/MINOR: config: do not accept more track-sc than configured
- BUG/MEDIUM: backend: fix URI hash when a query string is present

* Thu Oct 23 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- DOC: Address issue where documentation is excluded due to a gitignore rule.
- MEDIUM: Improve signal handling in systemd wrapper.
- BUG/MINOR: config: don't propagate process binding for dynamic use_backend
- MINOR: Also accept SIGHUP/SIGTERM in systemd-wrapper
- DOC: clearly state that the "show sess" output format is not fixed
- MINOR: stats: fix minor typo fix in stats_dump_errors_to_buffer()
- DOC: indicate in the doc that track-sc* can wait if data are missing
- MEDIUM: http: enable header manipulation for 101 responses
- BUG/MEDIUM: config: propagate frontend to backend process binding again.
- MEDIUM: config: properly propagate process binding between proxies
- MEDIUM: config: make the frontends automatically bind to the listeners' processes
- MEDIUM: config: compute the exact bind-process before listener's maxaccept
- MEDIUM: config: only warn if stats are attached to multi-process bind directives
- MEDIUM: config: report it when tcp-request rules are misplaced
- MINOR: config: detect the case where a tcp-request content rule has no inspect-delay
- MEDIUM: systemd-wrapper: support multiple executable versions and names
- BUG/MEDIUM: remove debugging code from systemd-wrapper
- BUG/MEDIUM: http: adjust close mode when switching to backend
- BUG/MINOR: config: don't propagate process binding on fatal errors.
- BUG/MEDIUM: check: rule-less tcp-check must detect connect failures
- BUG/MINOR: tcp-check: report the correct failed step in the status
- DOC: indicate that weight zero is reported as DRAIN

* Sun Jun 22 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- MEDIUM: ssl: ignored file names ending as '.issuer' or '.ocsp'.
- MEDIUM: ssl: basic OCSP stapling support.
- MINOR: ssl/cli: Fix unapropriate comment in code on 'set ssl ocsp-response'
- MEDIUM: ssl: add 300s supported time skew on OCSP response update.
- MINOR: checks: mysql-check: Add support for v4.1+ authentication
- MEDIUM: ssl: Add the option to use standardized DH parameters >= 1024 bits
- MEDIUM: ssl: fix detection of ephemeral diffie-hellman key exchange by using the cipher description.
- MEDIUM: http: add actions "replace-header" and "replace-values" in http-req/resp
- MEDIUM: Break out check establishment into connect_chk()
- MEDIUM: Add port_to_str helper
- BUG/MEDIUM: fix ignored values for half-closed timeouts (client-fin and server-fin) in defaults section.
- BUG/MEDIUM: Fix unhandled connections problem with systemd daemon mode and SO_REUSEPORT.
- MINOR: regex: fix a little configuration memory leak.
- MINOR: regex: Create JIT compatible function that return match strings
- MEDIUM: regex: replace all standard regex function by own functions
- MEDIUM: regex: Remove null terminated strings.
- MINOR: regex: Use native PCRE API.
- MINOR: missing regex.h include
- DOC: Add Exim as Proxy Protocol implementer.
- BUILD: don't use type "uint" which is not portable
- BUILD: stats: workaround stupid and bogus -Werror=format-security behaviour
- BUG/MEDIUM: http: clear CF_READ_NOEXP when preparing a new transaction
- CLEANUP: http: don't clear CF_READ_NOEXP twice
- DOC: fix proxy protocol v2 decoder example
- DOC: fix remaining occurrences of "pattern extraction"
- MINOR: log: allow the HTTP status code to be logged even in TCP frontends
- MINOR: logs: don't limit HTTP header captures to HTTP frontends
- MINOR: sample: improve sample_fetch_string() to report partial contents
- MINOR: capture: extend the captures to support non-header keys
- MINOR: tcp: prepare support for the "capture" action
- MEDIUM: tcp: add a new tcp-request capture directive
- MEDIUM: session: allow shorter retry delay if timeout connect is small
- MEDIUM: session: don't apply the retry delay when redispatching
- MEDIUM: session: redispatch earlier when possible
- MINOR: config: warn when tcp-check rules are used without option tcp-check
- BUG/MINOR: connection: make proxy protocol v1 support the UNKNOWN protocol
- DOC: proxy protocol example parser was still wrong
- DOC: minor updates to the proxy protocol doc
- CLEANUP: connection: merge proxy proto v2 header and address block
- MEDIUM: connection: add support for proxy protocol v2 in accept-proxy
- MINOR: tools: add new functions to quote-encode strings
- DOC: clarify the CSV format
- MEDIUM: stats: report the last check and last agent's output on the CSV status
- MINOR: freq_ctr: introduce a new averaging method
- MEDIUM: session: maintain per-backend and per-server time statistics
- MEDIUM: stats: report per-backend and per-server time stats in HTML and CSV outputs
- BUG/MINOR: http: fix typos in previous patch
- DOC: remove the ultra-obsolete TODO file
- DOC: update roadmap
- DOC: minor updates to the README
- DOC: mention the maxconn limitations with the select poller
- DOC: commit a few old design thoughts files
