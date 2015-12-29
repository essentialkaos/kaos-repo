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
%define lua_ver           5.3.0

###############################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.6.3
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

BuildRequires:     make gcc pcre-devel openssl-devel

Requires:          pcre openssl setup >= 2.8.14-14

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
%dir %{hp_datadir}/*
%dir %{hp_confdir}
%config(noreplace) %{hp_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_bindir}/halog
%{_mandir}/man1/%{name}.1.gz
%attr(0755, %{hp_user}, %{hp_group}) %dir %{hp_homedir}

###############################################################################

%changelog
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
