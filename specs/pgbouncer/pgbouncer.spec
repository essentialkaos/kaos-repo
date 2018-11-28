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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __sysctl          %{_bindir}/systemctl

%define username          %{name}
%define groupname         %{name}

################################################################################

Summary:           Lightweight connection pooler for PostgreSQL
Name:              pgbouncer
Version:           1.9.0
Release:           1%{?dist}
License:           MIT and BSD
Group:             Applications/Databases
URL:               https://pgbouncer.github.io

Source0:           https://pgbouncer.github.io/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.sysconfig
Source3:           %{name}.logrotate
Source4:           %{name}.service

Patch0:            %{name}-ini.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc openssl-devel

Requires:          openssl kaosv >= 2.15

%if 0%{?rhel} >= 7
BuildRequires:     libevent-devel
Requires:          libevent

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
BuildRequires:     libevent2-devel
Requires:          libevent2

Requires(post):    chkconfig
Requires(preun):   chkconfig initscripts
Requires(postun):  initscripts
%endif

################################################################################

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

################################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p0

%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

%configure --datadir=%{_datadir}

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_initrddir}

install -pm 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
install -pm 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service
%endif

rm -f %{buildroot}%{_docdir}/%{name}/pgbouncer.ini
rm -f %{buildroot}%{_docdir}/%{name}/NEWS
rm -f %{buildroot}%{_docdir}/%{name}/README
rm -f %{buildroot}%{_docdir}/%{name}/userlist.txt

%clean
rm -rf %{buildroot}

################################################################################

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

chown -R %{username}:%{groupname} %{_sysconfdir}/%{name}

%pre
%{__getent} group %{groupname} >/dev/null || %{__groupadd} -r %{groupname}
%{__getent} passwd %{username} >/dev/null || \
            %{__useradd} -g %{username} -r -s /bin/bash %{username}

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} %{name} stop &>/dev/null || :
  %{__chkconfig} --del %{name} &>/dev/null || :
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
%defattr(-,root,root,-)
%doc AUTHORS COPYRIGHT NEWS.rst NEWS.rst
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/*
%{_initrddir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*
%{_docdir}/%{name}/*

################################################################################

%changelog
* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-1
- Fixed restart logic in init script

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- RECONNECT command
- WAIT_CLOSE command
- Fast close - Disconnect a server in session pool mode immediately if it is
  in "close_needed" (reconnect) mode.
- Add close_needed column to SHOW SERVERS
- Avoid double-free in parse_filename
- Avoid NULL pointer deref in parse_line
- Port mkauth.py to Python 3
- Improve signals documentation
- Improve quick start documentation
- Document SET command
- Correct list of required software
- Fix -Wimplicit-fallthrough warnings
- Add missing documentation for various SHOW fields
- Document reconnect behavior on reload and DNS change
- Document that KILL requires RESUME afterwards
- Clarify documentation of server_lifetime
- Typos and capitalization fixes in messages and docs
- Fix psql invocation in tests
- Various other test setup improvements

* Wed Feb 14 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- Include file include/pam.h into distribution tarball

* Mon Feb 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-5
- Improved init script
- Improved spec

* Tue Feb 06 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.7.2-4
- Fixed typo with systemd unit description

* Thu Dec 07 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-3
- Fixed bug with searching process pid in init script

* Tue Mar 28 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-2
- Rebuilt with latest version of libevent2

* Thu Dec 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-1
- Added systemd support

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- Fix crash on stale pidfile removal. Problem introduced in 1.7.1.
- Disable cleanup - it breaks takeover and is not useful for production loads.
  Problem introduced in 1.7.1.
- After takeover, wait until pidfile is gone before booting. Slow shutdown due
  to memory cleanup exposed existing race.
- Make build reproducible by dropping DBGVER handling.
- Antimake: Sort file list from $(wildcard), newer gmake does not sort it
  anymore.
- Show libssl version in log.
- deb: Turn on full hardening.

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 1.7-0
- Updated to latest stable release

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to latest stable release

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to latest stable release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- Updated to latest stable release

* Fri Mar 20 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- Initial build
