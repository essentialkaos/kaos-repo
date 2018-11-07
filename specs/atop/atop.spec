################################################################################

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%endif

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
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

Summary:         Advanced System and Process Monitor
Name:            atop
Version:         2.3.0
Release:         4%{?dist}
License:         GPL
Group:           Development/System
URL:             http://www.atoptool.nl

Source0:         https://www.atoptool.nl/download/%{name}-%{version}.tar.gz
Source1:         %{name}.daily
Source2:         %{name}.sysconfig

Patch0:          %{name}-%{version}-script-path-fix.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc make zlib-devel ncurses-devel

Requires:        zlib ncurses

%if %{systemd_enabled}
Requires:        systemd
%else
Requires:        initscripts
%endif

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The program atop is an interactive monitor to view the load on
a Linux-system. It shows the occupation of the most critical
hardware-resources (from a performance point of view) on system-level,
i.e. cpu, memory, disk and network. It also shows which processess
(and threads) are responsible for the indicated load (again cpu-,
memory-, disk- and network-load on process-level).
The program atop can also be used to log system- and process-level
information in raw format for long-term analysis.

The program atopsar can be used to view system-level statistics
as reports.

################################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p1

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sbindir}
install -pm 0711 atop %{buildroot}%{_bindir}/
install -pm 0700 atopacctd %{buildroot}%{_sbindir}/
ln -sf %{_bindir}/atop  %{buildroot}%{_bindir}/atopsar

install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -pm 0711 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/

install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -pm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -dm 0755 %{buildroot}%{_mandir}/man1
install -dm 0755 %{buildroot}%{_mandir}/man5
install -dm 0755 %{buildroot}%{_mandir}/man8
install -pm 0644 man/*.1* %{buildroot}%{_mandir}/man1/
install -pm 0644 man/*.5* %{buildroot}%{_mandir}/man5/
install -pm 0644 man/*.8* %{buildroot}%{_mandir}/man8/

install -dm 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 0644 psaccs_atop %{buildroot}%{_sysconfdir}/logrotate.d/
install -pm 0644 psaccu_atop %{buildroot}%{_sysconfdir}/logrotate.d/

install -dm 0755 %{buildroot}%{_logdir}/%{name}

install -dm 0755 %{buildroot}%{_crondir}

%if %{systemd_enabled}
install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_sharedstatedir}/systemd/system-sleep
install -pm 0644 atop.service %{buildroot}%{_unitdir}/atop.service
install -pm 0644 atopacct.service %{buildroot}%{_unitdir}/atopacct.service
install -pm 0644 atop.cronsystemd %{buildroot}%{_crondir}/atop
install -pm 0711 atop-pm.sh %{buildroot}%{_sharedstatedir}/systemd/system-sleep/atop-pm.sh
%else
install -dm 0755 %{buildroot}%{_initddir}
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -pm 0755 atop.init %{buildroot}%{_initddir}/atop
install -pm 0755 atopacct.init %{buildroot}%{_initddir}/atopacct
install -pm 0644 atop.cronsysv %{buildroot}%{_crondir}/atop
install -pm 0711 45atoppm %{buildroot}%{_sysconfdir}/%{name}/45atoppm
%endif

%clean
rm -rf %{buildroot}

%post
# save today's logfile (format might be incompatible)
mv %{_logdir}/%{name}/atop_$(date +%Y%m%d) %{_logdir}/%{name}/atop_$(date +%Y%m%d).save &>/dev/null || :

# create dummy files to be rotated
touch %{_logdir}/%{name}/dummy_before %{_logdir}/%{name}/dummy_after

%if %{systemd_enabled}
%{__systemctl} enable atop &>/dev/null || :
%{__systemctl} start  atop &>/dev/null || :
%{__systemctl} enable atopacct &>/dev/null || :
%{__systemctl} start  atopacct &>/dev/null || :
%else
%{__chkconfig} --add atopacct
%{__chkconfig} --add atop

# install Power Management for suspend/hibernate
if [[ -d %{_libdir}/pm-utils/sleep.d ]] ; then
  cp %{_sysconfdir}/%{name}/45atoppm %{_libdir}/pm-utils/sleep.d/
fi

# activate daily logging for today
%{_sbindir}/atopacctd
%endif

sleep 2
%{_sysconfdir}/%{name}/atop.daily &

%preun
%if %{systemd_enabled}
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} stop    atop &>/dev/null || :
  %{__systemctl} disable atop &>/dev/null || :
  %{__systemctl} stop    atopacct &>/dev/null || :
  %{__systemctl} disable atopacct &>/dev/null || :
fi
%else
killall atopacctd &>/dev/null || :
killall atop &>/dev/null || :

if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --del atopacct
  %{__chkconfig} --del atop
fi

rm -f %{_libdir}/pm-utils/sleep.d/45atoppm &>/dev/null || :
%endif

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING AUTHOR ChangeLog
%config(noreplace) %{_sysconfdir}/sysconfig/atop
%if %{systemd_enabled}
%config(noreplace) %{_unitdir}/atop.service
%config(noreplace) %{_unitdir}/atopacct.service
%{_sharedstatedir}/systemd/system-sleep/atop-pm.sh
%else
%config(noreplace) %{_initddir}/atop
%config(noreplace) %{_initddir}/atopacct
%{_sysconfdir}/%{name}/45atoppm
%endif
%{_bindir}/atop
%{_bindir}/atopsar
%{_sbindir}/atopacctd
%{_mandir}/man1/atop.1*
%{_mandir}/man1/atopsar.1*
%{_mandir}/man5/atoprc.5*
%{_mandir}/man8/atopacctd.8*
%{_sysconfdir}/%{name}/atop.daily
%{_crondir}/atop
%{_sysconfdir}/logrotate.d/psaccs_atop
%{_sysconfdir}/logrotate.d/psaccu_atop
%dir %{_logdir}/%{name}/

################################################################################

%changelog
* Wed Nov 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-4
- Fixed path in cron config and systemd unit

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-3
- Improved atop configuration through sysconfig file

* Mon Jun 26 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.3.0-2
- Added patch with script path fix for systemd unit

* Sun Jun 11 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-1
- Added patch with script path fix

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Updated to latest stable release

* Fri Jan 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.3-0
- Initial build for kaos repository
