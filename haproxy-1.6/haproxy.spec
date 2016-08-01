###############################################################################

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

%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __userdel         %{_sbindir}/userdel
%define __getent          %{_bindir}/getent

###############################################################################

%define hp_user           %{name}
%define hp_user_id        188
%define hp_group          %{name}
%define hp_group_id       188
%define hp_homedir        %{_localstatedir}/lib/%{name}
%define hp_confdir        %{_sysconfdir}/%{name}
%define hp_datadir        %{_datadir}/%{name}
%define lua_ver           5.3.2

###############################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.6.7
Release:           0%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu
Group:             System Environment/Daemons

Source0:           http://www.haproxy.org/download/1.6/src/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.cfg
Source3:           %{name}.logrotate

Source10:          http://www.lua.org/ftp/lua-%{lua_ver}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre):     %{__groupadd}
Requires(pre):     %{__useradd}
Requires(post):    %{__chkconfig}
Requires(preun):   %{__chkconfig}
Requires(preun):   %{__service}
Requires(postun):  %{__service}

BuildRequires:     make gcc pcre-devel openssl-devel readline-devel

Requires:          pcre openssl readline setup >= 2.8.14-14

###############################################################################

%description
HAProxy is a free, fast and reliable solution offering high
availability, load balancing, and proxying for TCP and HTTP-based
applications. It is particularly suited for web sites crawling under
very high loads while needing persistence or Layer7 processing.
Supporting tens of thousands of connections is clearly realistic with
modern hardware. Its mode of operation makes integration with existing
architectures very easy and riskless, while still offering the
possibility not to expose fragile web servers to the net.

###############################################################################

%prep
%setup -q

%build
%{__tar} xzvf %{SOURCE10}

%ifarch %ix86 x86_64
use_regparm="USE_REGPARM=1"
%endif

pushd lua-%{lua_ver}
%{__make} %{?_smp_mflags} linux
%{__make} %{?_smp_mflags} INSTALL_TOP=../../lua53 install
popd

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux26" ${use_regparm} \
  USE_OPENSSL=1 \
  USE_PCRE=1 \
  USE_LUA=1 \
  LUA_LIB=./lua53/lib/ \
  LUA_INC=./lua53/include

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

install -dm 0755 %{buildroot}%{hp_homedir}
install -dm 0755 %{buildroot}%{hp_datadir}
install -dm 0755 %{buildroot}%{_bindir}

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
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]]; then
  %{__service} %{name} stop >/dev/null 2>&1
  %{__chkconfig} --del %{name}
fi

%postun
if [[ $1 -ge 1 ]]; then
  %{__service} %{name} condrestart >/dev/null 2>&1 || :
fi

###############################################################################

%files
%defattr(-, root, root, -)
%doc CHANGELOG LICENSE README doc/*
%doc examples/*.cfg
%dir %{hp_datadir}
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{hp_datadir}/*
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

###############################################################################

%changelog
* Fri Jul 15 2016 Gleb Goncharov <inbox@gongled.ru> - 1.6.7-0
- MINOR: new function my_realloc2 = realloc + free upon failure
- CLEANUP: fixed some usages of realloc leading to memory leak
- Revert "BUG/MINOR: ssl: fix potential memory leak in ssl_sock_load_dh_params()"
- BUG/MEDIUM: dns: fix alignment issues in the DNS response parser
- BUG/MINOR: Fix endiness issue in DNS header creation code

* Fri Jul 15 2016 Gleb Goncharov <inbox@gongled.ru> - 1.6.6-0
- BUG/MAJOR: fix listening IP address storage for frontends
- BUG/MINOR: fix listening IP address storage for frontends (cont)
- DOC: Fix typo so fetch is properly parsed by Cyril's converter
- BUG/MAJOR: http: fix breakage of "reqdeny" causing random crashes
- BUG/MEDIUM: stick-tables: fix breakage in table converters
- BUG/MEDIUM: dns: unbreak DNS resolver after header fix
- BUILD: fix build on Solaris 11
- CLEANUP: connection: fix double negation on memcmp()
- BUG/MEDIUM: stats: show servers state may show an servers from another backend
- BUG/MEDIUM: fix risk of segfault with "show tls-keys"
- BUG/MEDIUM: sticktables: segfault in some configuration error cases
- BUG/MEDIUM: lua: converters doesn't work
- BUG/MINOR: http: add-header: header name copied twice
- BUG/MEDIUM: http: add-header: buffer overwritten
- BUG/MINOR: ssl: fix potential memory leak in ssl_sock_load_dh_params()
- BUG/MINOR: http: url32+src should use the big endian version of url32
- BUG/MINOR: http: url32+src should check cli_conn before using it
- DOC: http: add documentation for url32 and url32+src
- BUG/MINOR: fix http-response set-log-level parsing error
- MINOR: systemd: Use variable for config and pidfile paths
- MINOR: systemd: Perform sanity check on config before reload (cherry picked from commit 68535bddf305fdd22f1449a039939b57245212e7)
- BUG/MINOR: init: always ensure that global.rlimit_nofile matches actual limits
- BUG/MINOR: init: ensure that FD limit is raised to the max allowed
- BUG/MEDIUM: external-checks: close all FDs right after the fork()
- BUG/MAJOR: external-checks: use asynchronous signal delivery
- BUG/MINOR: external-checks: do not unblock undesired signals
- BUILD/MEDIUM: rebuild everything when an include file is changed
- BUILD/MEDIUM: force a full rebuild if some build options change
- BUG/MINOR: srv-state: fix incorrect output of state file
- BUG/MINOR: ssl: close ssl key file on error
- BUG/MINOR: http: fix misleading error message for response captures
- BUG/BUILD: don't automatically run "make" on "make install"
- DOC: add missing doc for http-request deny [deny_status <status>]

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.5-0
- BUG/MINOR: log: Don't use strftime() which can clobber timezone if chrooted
- BUILD: namespaces: fix a potential build warning in namespaces.c
- DOC: add encoding to json converter example
- BUG/MINOR: conf: "listener id" expects integer, but its not checked
- DOC: Clarify tunes.vars.xxx-max-size settings
- BUG/MEDIUM: peers: fix incorrect age in frequency counters
- BUG/MEDIUM: Fix RFC5077 resumption when more than TLS_TICKETS_NO are present
- BUG/MAJOR: Fix crash in http_get_fhdr with exactly MAX_HDR_HISTORY headers
- BUG/MINOR: lua: can't load external libraries
- DOC: "addr" parameter applies to both health and agent checks
- DOC: timeout client: pointers to timeout http-request
- DOC: typo on stick-store response
- DOC: stick-table: amend paragraph blaming the loss of table upon reload
- DOC: typo: ACL subdir match
- DOC: typo: maxconn paragraph is wrong due to a wrong buffer size
- DOC: regsub: parser limitation about the inability to use closing square brackets
- DOC: typo: req.uri is now replaced by capture.req.uri
- DOC: name set-gpt0 mismatch with the expected keyword
- BUG/MEDIUM: stick-tables: some sample-fetch doesn't work in the connection state.
- DOC: fix "needed" typo
- BUG/MINOR: dns: inapropriate way out after a resolution timeout
- BUG/MINOR: dns: trigger a DNS query type change on resolution timeout
- BUG/MINOR : allow to log cookie for tarpit and denied request
- OPTIM/MINOR: session: abort if possible before connecting to the backend
- BUG/MEDIUM: trace.c: rdtsc() is defined in two files
- BUG/MEDIUM: channel: fix miscalculation of available buffer space (2nd try)
- BUG/MINOR: cfgparse: couple of small memory leaks.
- BUG/MEDIUM: sample: initialize the pointer before parse_binary call.
- DOC: fix discrepancy in the example for http-request redirect
- DOC: Clarify IPv4 address / mask notation rules
- CLEANUP: fix inconsistency between fd->iocb, proto->accept and accept()
- BUG/MEDIUM: fix maxaccept computation on per-process listeners
- BUG/MINOR: listener: stop unbound listeners on startup
- BUG/MINOR: fix maxaccept computation according to the frontend process range
- MEDIUM: unblock signals on startup.
- BUG/MEDIUM: channel: don't allow to overwrite the reserve until connected
- BUG/MEDIUM: channel: incorrect polling condition may delay event delivery
- BUG/MEDIUM: channel: fix miscalculation of available buffer space (3rd try)
- BUG/MEDIUM: log: fix risk of segfault when logging HTTP fields in TCP mode
- BUG/MEDIUM: lua: protects the upper boundary of the argument list for converters/fetches.
- BUG/MINOR: log: fix a typo that would cause %%HP to log <BADREQ>
- MINOR: channel: add new function channel_congested()
- BUG/MEDIUM: http: fix risk of CPU spikes with pipelined requests from dead client
- BUG/MAJOR: channel: fix miscalculation of available buffer space (4th try)
- BUG/MEDIUM: stream: ensure the SI_FL_DONT_WAKE flag is properly cleared
- BUG/MEDIUM: channel: fix inconsistent handling of 4GB-1 transfers
- BUG/MEDIUM: stats: show servers state may show an empty or incomplete result
- BUG/MEDIUM: stats: show backend may show an empty or incomplete result
- MINOR: stats: fix typo in help messages
- MINOR: stats: show stat resolvers missing in the help message
- BUG/MINOR: dns: fix DNS header definition
- BUG/MEDIUM: dns: fix alignment issue when building DNS queries
- CLEANUP/MINOR: stats: fix accidental addition of member "env" in the applet ctx

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.4-0
- BUG/MINOR: http: fix several off-by-one errors in the url_param parser
- BUG/MINOR: http: Be sure to process all the data received from a server
- BUG/MINOR: chunk: make chunk_dup() always check and set dst->size
- MINOR: chunks: ensure that chunk_strcpy() adds a trailing zero
- MINOR: chunks: add chunk_strcat() and chunk_newstr()
- MINOR: chunk: make chunk_initstr() take a const string
- MINOR: lru: new function to delete <nb> least recently used keys
- DOC: add Ben Shillito as the maintainer of 51d
- BUG/MINOR: 51d: Ensures a unique domain for each configuration
- BUG/MINOR: 51d: Aligns Pattern cache implementation with HAProxy best practices.
- BUG/MINOR: 51d: Releases workset back to pool.
- BUG/MINOR: 51d: Aligned const pointers to changes in 51Degrees.
- CLEANUP: 51d: Aligned if statements with HAProxy best practices and removed casts from malloc.
- DOC: fix a few spelling mistakes (cherry picked from commit cc123c66c2075add8524a6a9925382927daa6ab0)
- DOC: fix "workaround" spelling
- BUG/MINOR: examples: Fixing haproxy.spec to remove references to .cfg files
- MINOR: fix the return type for dns_response_get_query_id() function
- MINOR: server state: missing LF (\n) on error message printed when parsing server state file
- BUG/MEDIUM: dns: no DNS resolution happens if no ports provided to the nameserver
- BUG/MAJOR: servers state: server port is erased when dns resolution is enabled on a server
- BUG/MEDIUM: servers state: server port is used uninitialized
- BUG/MEDIUM: config: Adding validation to stick-table expire value.
- BUG/MEDIUM: sample: http_date() doesn't provide the right day of the week
- BUG/MEDIUM: channel: fix miscalculation of available buffer space.
- MEDIUM: pools: add a new flag to avoid rounding pool size up
- BUG/MEDIUM: buffers: do not round up buffer size during allocation
- BUG/MINOR: stream: don't force retries if the server is DOWN
- BUG/MINOR: counters: make the sc-inc-gpc0 and sc-set-gpt0 touch the table
- MINOR: unix: don't mention free ports on EAGAIN
- BUG/CLEANUP: CLI: report the proper field states in "show sess"
- MINOR: stats: send content-length with the redirect to allow keep-alive
- BUG: stream_interface: Reuse connection even if the output channel is empty
- DOC: remove old tunnel mode assumptions
- BUG/MAJOR: http-reuse: fix risk of orphaned connections
- BUG/MEDIUM: http-reuse: do not share private connections across backends
- BUG/MINOR: ssl: Be sure to use unique serial for regenerated certificates
- BUG/MINOR: stats: fix missing comma in stats on agent drain
- BUG/MINOR: lua: unsafe initialization
- DOC: lua: fix somme errors
- DOC: add server name at rate-limit sessions example
- BUG/MEDIUM: ssl: fix off-by-one in ALPN list allocation
- BUG/MEDIUM: ssl: fix off-by-one in NPN list allocation
- DOC: LUA: fix some typos and syntax errors
- MINOR: cfgparse: warn for incorrect 'timeout retry' keyword spelling in resolvers
- MINOR: mailers: increase default timeout to 10 seconds
- MINOR: mailers: use <CRLF> for all line endings
- BUG/MAJOR: lua: applets can't sleep.
- BUG/MINOR: server: some prototypes are renamed
- BUG/MINOR: lua: Useless copy
- BUG/MEDIUM: stats: stats bind-process doesn't propagate the process mask correctly
- BUG/MINOR: server: fix the format of the warning on address change
- BUG/MEDIUM: chunks: always reject negative-length chunks
- BUG/MINOR: systemd: ensure we don't miss signals
- BUG/MINOR: systemd: report the correct signal in debug message output
- BUG/MINOR: systemd: propagate the correct signal to haproxy
- MINOR: systemd: ensure a reload doesn't mask a stop
- BUG/MEDIUM: cfgparse: wrong argument offset after parsing server "sni" keyword
- CLEANUP: stats: Avoid computation with uninitialized bits.
- CLEANUP: pattern: Ignore unknown samples in pat_match_ip().
- CLEANUP: map: Avoid memory leak in out-of-memory condition.
- BUG/MINOR: tcpcheck: fix incorrect list usage resulting in failure to load certain configs
- BUG/MAJOR: samples: check smp->strm before using it
- MINOR: sample: add a new helper to initialize the owner of a sample
- MINOR: sample: always set a new sample's owner before evaluating it
- BUG/MAJOR: vars: always retrieve the stream and session from the sample
- CLEANUP: payload: remove useless and confusing nullity checks for channel buffer
- BUG/MINOR: ssl: fix usage of the various sample fetch functions
- MINOR: cfgparse: warn when uid parameter is not a number
- MINOR: cfgparse: warn when gid parameter is not a number
- BUG/MINOR: standard: Avoid free of non-allocated pointer
- BUG/MINOR: pattern: Avoid memory leak on out-of-memory condition
- CLEANUP: http: fix a build warning introduced by a recent fix
- BUG/MINOR: log: GMT offset not updated when entering/leaving DST

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.3-0
- BUG/MINOR: http rule: http capture 'id' rule points to a non existing i
- BUG/MINOR: server: check return value of fgets() in apply_server_state(
- BUG/MINOR: acl: don't use record layer in req_ssl_ve
- BUILD: freebsd: double declaratio
- BUG/MEDIUM: lua: clean output buffe
- BUILD: check for libressl to be able to build against i
- DOC: lua-api/index.rst small example fixes, spelling correction
- DOC: lua: architecture and first step
- DOC: relation between timeout http-request and option http-buffer-reques
- BUILD: Make deviceatlas require PCR
- BUG: http: do not abort keep-alive connections on server timeou
- BUG/MEDIUM: http: switch the request channel to no-delay once done
- BUG/MINOR: lua: don't force-sslv3 LUA's SSL socke
- BUILD/MINOR: http: proto_http.h needs sample.
- BUG/MEDIUM: http: don't enable auto-close on the response sid
- BUG/MEDIUM: stream: fix half-closed timeout handlin
- CLEANUP: compression: don't allocate DEFAULT_MAXZLIBMEM without USE_ZLI
- BUG/MEDIUM: cli: changing compression rate-limiting must require admin leve
- BUG/MEDIUM: sample: urlp can't match an empty valu
- BUILD: dumpstats: silencing warning for printf format specifier / time_
- CLEANUP: proxy: calloc call inverted argument
- MINOR: da: silent logging by default and displaying DeviceAtlas support if built
- BUG/MEDIUM: da: stop DeviceAtlas processing in the convertor if there is no input
- DOC: Edited 51Degrees section of READM
- BUG/MEDIUM: checks: email-alert not working when declared in default
- BUG/MINOR: checks: email-alert causes a segfault when an unknown mailers section is configure
- BUG/MINOR: checks: typo in an email-alert error messag
- BUG/MINOR: tcpcheck: conf parsing error when no port configured on server and last rule is a CONNECT with no por
- BUG/MINOR: tcpcheck: conf parsing error when no port configured on server and first rule(s) is (are) COMMEN
- BUG/MEDIUM: http: fix http-reuse when frontend and backend diffe
- DOC: prefer using http-request/response over reqXXX/rspXXX directive
- BUG/MEDIUM: config: properly adjust maxconn with nbproc when memmax is force
- BUG/MEDIUM: peers: table entries learned from a remote are pushed to others after a random delay
- BUG/MEDIUM: peers: old stick table updates could be repushed
- CLEANUP: haproxy: using _GNU_SOURCE instead of __USE_GNU macro
- MINOR: lua: service/applet can have access to the HTTP headers when a POST is receive
- REORG/MINOR: lua: convert boolean "int" to bitfiel
- BUG/MEDIUM: lua: Lua applets must not fetch samples using http_tx
- BUG/MINOR: lua: Lua applets must not use http_tx
- BUG/MEDIUM: lua: Forbid HTTP applets from being called from tcp ruleset
- BUG/MAJOR: lua: Do not force the HTTP analysers in use-service
- CLEANUP: lua: bad error message
- DOC: lua: fix lua AP
- DOC: mailers: typo in 'hostname' descriptio
- DOC: compression: missing mention of libslz for compression algorith
- BUILD/MINOR: regex: missing heade
- BUG/MINOR: stream: bad return cod
- DOC: lua: fix somme errors and add implicit type

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.2-0
- BUILD: ssl: fix build error introduced in commit 7969a3 with OpenSSL < 1.0.0
- DOC: fix a typo for a "deviceatlas" keyword
- FIX: small typo in an example using the "Referer" header
- BUG/MEDIUM: config: count memory limits on 64 bits, not 32
- BUG/MAJOR: dns: first DNS response packet not matching queried hostname may lead to a loop
- BUG/MINOR: dns: unable to parse CNAMEs response
- BUG/MINOR: examples/haproxy.init: missing brace in quiet_check()
- DOC: deviceatlas: more example use cases.
- BUG/BUILD: replace haproxy-systemd-wrapper with $(EXTRA) in install-bin.
- BUG/MAJOR: http: don't requeue an idle connection that is already queued
- DOC: typo on capture.res.hdr and capture.req.hdr
- BUG/MINOR: dns: check for duplicate nameserver id in a resolvers section was missing
- CLEANUP: use direction names in place of numeric values
- BUG/MEDIUM: lua: sample fetches based on response doesn't work

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- DOC: specify that stats socket doc (section 9.2) is in management
- BUILD: install only relevant and existing documentation
- CLEANUP: don't ignore debian/ directory if present
- BUG/MINOR: dns: parsing error of some DNS response
- BUG/MEDIUM: namespaces: don't fail if no namespace is used
- BUG/MAJOR: ssl: free the generated SSL_CTX if the LRU cache is disabled
- MEDIUM: dns: Don't use the ANY query type

* Thu Oct 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Stable version 1.6
