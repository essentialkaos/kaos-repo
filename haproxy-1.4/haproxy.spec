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

###############################################################################

Name:              haproxy
Summary:           TCP/HTTP reverse proxy for high availability environments
Version:           1.4.26
Release:           1%{?dist}
License:           GPLv2+
URL:               http://haproxy.1wt.eu/
Group:             System Environment/Daemons

Source0:           http://haproxy.1wt.eu/download/1.4/src/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.cfg
Source3:           %{name}.logrotate

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre):     %{__groupadd}
Requires(pre):     %{__useradd}
Requires(post):    %{__chkconfig}
Requires(preun):   %{__chkconfig}
Requires(preun):   %{__service}
Requires(postun):  %{__service}

BuildRequires:     make gcc pcre-devel

Requires:          pcre setup >= 2.8.14-14

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
%ifarch %ix86 x86_64
use_regparm="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux26" USE_PCRE=1 ${use_regparm}

pushd contrib/halog
  %{__make} halog
popd

%install
rm -rf %{buildroot}

%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix}
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -pDm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -pDm 0644 %{SOURCE2} %{buildroot}%{hp_confdir}/%{name}.cfg
%{__install} -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__install} -dm 0755 %{buildroot}%{hp_homedir}
%{__install} -dm 0755 %{buildroot}%{hp_datadir}
%{__install} -dm 0755 %{buildroot}%{_bindir}

%{__install} -pm 0755 ./contrib/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -pm 0644 ./examples/errorfiles/* %{buildroot}%{hp_datadir}

for file in $(find . -type f -name '*.txt') ; do
  iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
  %{__touch} -r $file $file.new && \
  %{__mv} $file.new $file
done

%clean
%{__rm} -rf %{buildroot}

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
%doc examples/url-switching.cfg
%doc examples/acl-content-sw.cfg
%doc examples/content-sw-sample.cfg
%doc examples/cttproxy-src.cfg
%doc examples/haproxy.cfg
%doc examples/tarpit.cfg
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
* Mon Oct 26 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.26-1
- Improved default config

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.26-0
- BUG/MINOR: stats: fix a typo on a closing tag for a server tracking another one
- BUG/MEDIUM: auth: fix segfault with http-auth and a configuration with an unknown encryption algorithm
- BUG/MEDIUM: config: userlists should ensure that encrypted passwords are supported
- BUG/MINOR: log: fix request flags when keep-alive is enabled
- BUG/MINOR: checks: prevent http keep-alive with http-check expect
- BUG/MEDIUM: backend: Update hash to use unsigned int throughout
- BUG/MINOR: http: fix typo: "401 Unauthorized" => "407 Unauthorized"
- BUG/MINOR: build: handle whitespaces in wc -l output
- DOC: httplog does not support 'no'
- BUG/MEDIUM: regex: fix risk of buffer overrun in exp_replace()
- BUILD: fix Makefile.bsd
- BUILD: also fix Makefile.osx
- BUG/MAJOR: http: fix again http-send-name-header
- BUG/MAJOR: buffer: fix possible integer overflow on reserved size computation
- BUG/MAJOR: buffer: don't schedule data in transit for leaving until connected
- BUG/MINOR: http: don't report server aborts as client aborts
- DOC: stop referencing the slow git repository in the README
- DOC: remove the ultra-obsolete TODO file
- BUILD: remove TODO from the spec file and add README
- MINOR: log: make MAX_SYSLOG_LEN overridable at build time
- DOC: remove references to CPU=native in the README
- BUG/MEDIUM: http: don't dump debug headers on MSG_ERROR
- BUG/MAJOR: cli: explicitly call cli_release_handler() upon error
- BUG/MEDIUM: tcp: don't use SO_ORIGINAL_DST on non-AF_INET sockets
- BUG/MINOR: config: don't inherit the default balance algorithm in frontends
- BUG/MEDIUM: http: fix header removal when previous header ends with pure LF
- BUG/MINOR: http: abort request processing on filter failure

* Sun May 11 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.25-0
- DOC: typo: nosepoll self reference in config guide
- BUG/MINOR: deinit: free fdinfo while doing cleanup
- BUG/MEDIUM: server: set the macro for server's max weight SRV_UWGHT_MAX to SRV_UWGHT_RANGE
- BUG/MINOR: use the same check condition for server as other algorithms
- BUG/MINOR: stream-int: also consider ENOTCONN in addition to EAGAIN for recv()
- BUG/MINOR: fix forcing fastinter in "on-error"
- BUG/MEDIUM: http/auth: Sometimes the authentication credentials can be mix between two requests
- BUG/MAJOR: http: don't emit the send-name-header when no server is available
- BUG/MEDIUM: http: "option checkcache" fails with the no-cache header
- MEDIUM: session: disable lingering on the server when the client aborts
- MINOR: config: warn when a server with no specific port uses rdp-cookie
- MEDIUM: increase chunk-size limit to 2GB-1
- DOC: add a mention about the limited chunk size
- MEDIUM: http: add "redirect scheme" to ease HTTP to HTTPS redirection
- BUILD: proto_tcp: remove a harmless warning
- BUG/MINOR: acl: remove patterns from the tree before freeing them
- BUG/MEDIUM: checks: fix slow start regression after fix attempt
- BUG/MAJOR: server: weight calculation fails for map-based algorithms
- BUG/MINOR: backend: fix target address retrieval in transparent mode
- BUG/MEDIUM: stick: completely remove the unused flag from the store entries
- BUG/MEDIUM: stick-tables: complete the latest fix about store-responses
- BUG/MEDIUM: checks: tracking servers must not inherit the MAINT flag
- BUG/MINOR: stats: report correct throttling percentage for servers in slowstart
- BUG/MINOR: stats: correctly report throttle rate of low weight servers
- BUG/MINOR: checks: successful check completion must not re-enable MAINT servers
- BUG/MEDIUM: stats: the web interface must check the tracked servers before enabling
- BUG/MINOR: channel: initialize xfer_small/xfer_large on new buffers
- BUG/MINOR: stream-int: also consider ENOTCONN in addition to EAGAIN
- BUG/MEDIUM: http: don't start to forward request data before the connect
- DOC: fix misleading information about SIGQUIT
- BUILD: simplify the date and version retrieval in the makefile
- BUILD: prepare the makefile to skip format lines in SUBVERS and VERDATE
- BUILD: use format tags in VERDATE and SUBVERS files

* Tue Oct 29 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.24-0
- Initial build




















