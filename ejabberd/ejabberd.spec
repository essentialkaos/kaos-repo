###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd
%define __systemctl       %{_bindir}/systemctl

###############################################################################

%define user_name         ejabberd
%define group_name        ejabberd

###############################################################################

Summary:            Rock Solid, Massively Scalable, Infinitely Extensible XMPP Server
Name:               ejabberd
Version:            17.08
Release:            0%{?dist}
Group:              Development/Tools
License:            GPLv2
URL:                https://www.ejabberd.im

Source0:            https://github.com/processone/%{name}/archive/%{version}.tar.gz
Source1:            %{name}.logrotate

Patch0:             %{name}-conf.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make automake autoconf gcc gcc-c++ git erlang19
BuildRequires:      zlib-devel expat-devel pam-devel sqlite-devel
BuildRequires:      openssl-devel libyaml-devel

Requires:           erlang19 openssl libyaml

%if 0%{?rhel} >= 7
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
ejabberd is an open source Jabber/XMPP server designed from the ground up to
be the building bricks of highly critical messaging systems.

Written in Erlang programming language, ejabberd is cross-platform,
fault-tolerant, clusterable, very modular and highly versatile. It can be
extended in other programming languages, such as Elixir.

Designed to be massively scalable, it is widely used to power web scale
deployments across many software industries: Mobile messaging, Social
Networks, Gaming, Internet of Things.

ejabberd is taking great care of XMPP compliance, implementing most of the
XMPP extensions published by the XMPP Standard Foundation.

To innovate even further, the core development team is constantly working
with other open source communities to create bridges and elegant features.

This ejabberd community site is a hub for all people that are interested in
ejabberd, Erlang, XMPP and messaging in general.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p1

%build
./autogen.sh

%configure --enable-debug \
           --enable-full_xml \
           --enable-odbc \
           --enable-mysql \
           --enable-lager \
           --enable-pgsql \
           --enable-sqlite \
           --enable-pam \
           --enable-zlib \
           --enable-redis \
           --enable-json

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d/
install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}/spool
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_rundir}/%{name}

%if 0%{?rhel} >= 7
sed -i "s#%{buildroot}##g" %{name}.service
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
%else
sed -i "s#%{buildroot}##g" %{name}.init
install -dm 755 %{buildroot}%{_initddir}
install -pm 755 %{name}.init %{buildroot}%{_initddir}/%{name}
%endif

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{group_name} >/dev/null || %{__groupadd} -r %{group_name}
getent passwd %{user_name} >/dev/null || %{__useradd} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -M -r -g %{group_name} %{user_name}

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload %{name}.service &>/dev/null || :
  %{__systemctl} preset %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} stop %{name} &>/dev/null || :
%endif
fi

%postun
if [[ $1 -ge 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} try-restart %{name}.service &>/dev/null || :
%else
  %{__service} restart %{name} &>/dev/null || :
%endif
fi

###############################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(-, %{user_name}, %{group_name}) %{_sysconfdir}/%{name}/ejabberdctl.cfg
%config(noreplace) %attr(-, %{user_name}, %{group_name}) %{_sysconfdir}/%{name}/ejabberd.yml
%dir %attr(-, %{user_name}, %{group_name}) %{_sharedstatedir}/%{name}
%dir %attr(-, %{user_name}, %{group_name}) %{_sharedstatedir}/%{name}/spool
%dir %attr(-, %{user_name}, %{group_name}) %{_logdir}/%{name}
%dir %attr(-, %{user_name}, %{group_name}) %{_rundir}/%{name}
%attr(755, -, -) %{_sbindir}/%{name}ctl
%attr(644, -, -) %{_sysconfdir}/%{name}/inetrc
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif
%{_libdir}/*
%{_docdir}/%{name}/COPYING

###############################################################################

%changelog
* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 17.08-0
- Updated to latest stable release

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 17.07-0
- Updated to latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 17.04-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 17.01-0
- Updated to latest stable release

* Sun Sep 25 2016 Anton Novojilov <andy@essentialkaos.com> - 16.09-0
- Updated to latest stable release

* Fri Sep 09 2016 Anton Novojilov <andy@essentialkaos.com> - 16.08-2
- Fixed bug with wrong config file owner

* Mon Aug 29 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 16.08-1
- Added patch for debugging c2s connections
- Added patch for checking pid existance

* Wed Aug 17 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 16.08-0
- Updated to latest stable release

* Tue Jul 12 2016 Anton Novojilov <andy@essentialkaos.com> - 16.06-0
- Updated to latest stable release

* Sun May 22 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 16.04-0
- Updated to 16.04

* Fri Apr 29 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 16.03-2
- Added lager support

* Tue Apr 26 2016 Anton Novojilov <andy@essentialkaos.com> - 16.03-1
- SysV script fixes

* Thu Apr 07 2016 Anton Novojilov <andy@essentialkaos.com> - 16.03-0
- Updated to 16.03

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 16.01-0
- Updated to 16.01

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 15.11-0
- Updated to 15.11

* Wed Nov 18 2015 Anton Novojilov <andy@essentialkaos.com> - 15.09-1
- Fixed minor bug in init script

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 15.09-0
- Updated to latest stable release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 15.07-0
- Updated to latest stable release

* Sat Jul 18 2015 Anton Novojilov <andy@essentialkaos.com> - 15.06-0
- Initial build
