################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _logdir  %{_localstatedir}/log

%define __systemctl  %{_bindir}/systemctl

################################################################################

Summary:        Advanced System and Process Monitor
Name:           atop
Version:        2.8.1
Release:        0%{?dist}
License:        GPLv2+
Group:          Development/System
URL:            https://www.atoptool.nl

Source0:        https://www.atoptool.nl/download/%{name}-%{version}.tar.gz
Source1:        atopd

Patch0:         atop-newer-gcc.patch

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make zlib-devel ncurses-devel systemd

Requires:       zlib ncurses systemd

Provides:       %{name} = %{version}-%{release}

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
%{crc_check}

%setup -qn %{name}-%{version}

%patch0 -p1

# Set path to sysconfig file
sed -i 's#/etc/default/atop#/etc/sysconfig/atop#' atop.daily
sed -i 's#/etc/default/atop#/etc/sysconfig/atop#' atop.service

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sbindir}

install -pm 0755 atop %{buildroot}%{_bindir}/
install -pm 0755 atopcat %{buildroot}%{_bindir}/
install -pm 0755 atopconvert %{buildroot}%{_bindir}/
install -pm 0700 atopacctd %{buildroot}%{_sbindir}/

ln -sf %{_bindir}/atop %{buildroot}%{_bindir}/atopsar

install -dm 0755 %{buildroot}%{_datadir}/%{name}
install -pm 0755 %{name}.daily %{buildroot}%{_datadir}/%{name}/atop.daily

install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -pm 0644 %{name}.default %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -dm 0755 %{buildroot}%{_mandir}/man1
install -dm 0755 %{buildroot}%{_mandir}/man5
install -dm 0755 %{buildroot}%{_mandir}/man8
install -pm 0644 man/*.1* %{buildroot}%{_mandir}/man1/
install -pm 0644 man/*.5* %{buildroot}%{_mandir}/man5/
install -pm 0644 man/*.8* %{buildroot}%{_mandir}/man8/
rm -f %{buildroot}%{_mandir}/man8/atopgpud.*

install -dm 0755 %{buildroot}%{_logdir}/%{name}

install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_sharedstatedir}/systemd/system-sleep
install -dm 0755 %{buildroot}%{_sysconfdir}/default
install -pm 0644 atop.service %{buildroot}%{_unitdir}/
install -pm 0644 atop-rotate.service %{buildroot}%{_unitdir}/
install -pm 0644 atop-rotate.timer %{buildroot}%{_unitdir}/
install -pm 0644 atopacct.service %{buildroot}%{_unitdir}/
install -pm 0755 atop-pm.sh %{buildroot}%{_sharedstatedir}/systemd/system-sleep/

%clean
rm -rf %{buildroot}

%post
# save today's logfile (format might be incompatible)
mv %{_logdir}/%{name}/atop_$(date +%Y%m%d) %{_logdir}/%{name}/atop_$(date +%Y%m%d).save &>/dev/null || :

%{__systemctl} daemon-reload &>/dev/null || :
%{__systemctl} enable atop &>/dev/null || :
%{__systemctl} enable atopacct &>/dev/null || :
%{__systemctl} enable atop-rotate.timer &>/dev/null || :
%{__systemctl} start atop &>/dev/null || :
%{__systemctl} start atopacct &>/dev/null || :
%{__systemctl} start atop-rotate.timer &>/dev/null || :

%preun
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} stop atop &>/dev/null || :
  %{__systemctl} stop atopacct &>/dev/null || :
  %{__systemctl} stop atop-rotate.timer &>/dev/null || :
  %{__systemctl} disable atop &>/dev/null || :
  %{__systemctl} disable atopacct &>/dev/null || :
  %{__systemctl} disable atop-rotate.timer &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/atop
%config(noreplace) %{_unitdir}/atop.service
%config(noreplace) %{_unitdir}/atopacct.service
%config(noreplace) %{_unitdir}/atop-rotate.service
%config(noreplace) %{_unitdir}/atop-rotate.timer
%{_sharedstatedir}/systemd/system-sleep/atop-pm.sh
%{_datadir}/%{name}/atop.daily
%{_bindir}/atop
%{_bindir}/atopcat
%{_bindir}/atopsar
%{_bindir}/atopconvert
%{_sbindir}/atopacctd
%{_mandir}/man1/atop.1*
%{_mandir}/man1/atopsar.1*
%{_mandir}/man1/atopcat.1*
%{_mandir}/man1/atopconvert.1*
%{_mandir}/man5/atoprc.5*
%{_mandir}/man8/atopacctd.8*
%dir %{_logdir}/%{name}/

################################################################################

%changelog
* Tue Feb 28 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- Bug solution: wrong conversion of NUMA statistics (for systems with multiple
  NUMA nodes)
- Bug solution: string formatting might result in buffer overflow

* Thu Dec 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Avoid using perf counters in VM
- Improve daily rotation of logfile for systemd-based systems
- Bug fixes

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Support for Nvidia GPU statistics
- Support for Infiniband statistics
- Support for Pressure Stall Information (PSI)
- Faster startup of atop
- Configurable options for atop running in the background
- CPU Instructions Per Cycle (IPC)
- Various NFS counters corrected
- Recognition of nvme and nbd disks
- Recognition of DEADLINE scheduling policy
- Proper handling of memory locking (improper handling caused malloc failures
  in previous versions)
- Added atopconvert

* Wed Nov 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-4
- Fixed path in cron config and systemd unit

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-3
- Improved atop configuration through sysconfig file

* Mon Jun 26 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.3.0-2
- Added patch with script path fix for systemd unit

* Sun Jun 11 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-1
- Added patch with script path fix

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Support for Docker containers
- Improved gathering of process data
- Improved memory figures for processes
- Variable width for PID column
- Minor improvements

* Fri Jan 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.3-0
- Initial build for kaos repository
