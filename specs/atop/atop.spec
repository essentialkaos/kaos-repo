################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Advanced System and Process Monitor
Name:           atop
Version:        2.12.1
Release:        0%{?dist}
License:        GPLv2+
Group:          Development/System
URL:            https://www.atoptool.nl

Source0:        https://www.atoptool.nl/download/%{name}-%{version}.tar.gz
Source1:        atopd

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make zlib-devel ncurses-devel systemd glib2-devel

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

# Set path to sysconfig file
sed -i 's#/etc/default/atop#/etc/sysconfig/atop#' atop.daily
sed -i 's#/etc/default/atop#/etc/sysconfig/atop#' atop.service

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sbindir}

install -pm 700 atopacctd %{buildroot}%{_sbindir}/
install -pm 755 atop %{buildroot}%{_bindir}/
install -pm 755 atopcat %{buildroot}%{_bindir}/
install -pm 755 atopconvert %{buildroot}%{_bindir}/
install -pm 755 atophide %{buildroot}%{_bindir}/

ln -sf %{_bindir}/atop %{buildroot}%{_bindir}/atopsar

install -dm 755 %{buildroot}%{_datadir}/%{name}
install -pm 755 %{name}.daily %{buildroot}%{_datadir}/%{name}/atop.daily

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -pm 644 %{name}.default %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_mandir}/man5
install -dm 755 %{buildroot}%{_mandir}/man8
install -pm 644 man/*.1* %{buildroot}%{_mandir}/man1/
install -pm 644 man/*.5* %{buildroot}%{_mandir}/man5/
install -pm 644 man/*.8* %{buildroot}%{_mandir}/man8/

rm -f %{buildroot}%{_mandir}/man8/atopgpud.*

install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}

install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sharedstatedir}/systemd/system-sleep
install -dm 755 %{buildroot}%{_sysconfdir}/default
install -pm 644 atop.service %{buildroot}%{_unitdir}/
install -pm 644 atop-rotate.service %{buildroot}%{_unitdir}/
install -pm 644 atop-rotate.timer %{buildroot}%{_unitdir}/
install -pm 644 atopacct.service %{buildroot}%{_unitdir}/
install -pm 755 atop-pm.sh %{buildroot}%{_sharedstatedir}/systemd/system-sleep/

%clean
rm -rf %{buildroot}

%post
# save today's logfile (format might be incompatible)
mv %{_localstatedir}/log/%{name}/atop_$(date +%Y%m%d) %{_localstatedir}/log/%{name}/atop_$(date +%Y%m%d).save &>/dev/null || :

systemctl daemon-reload &>/dev/null || :
systemctl enable atop &>/dev/null || :
systemctl enable atopacct &>/dev/null || :
systemctl enable atop-rotate.timer &>/dev/null || :
systemctl start atop &>/dev/null || :
systemctl start atopacct &>/dev/null || :
systemctl start atop-rotate.timer &>/dev/null || :

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl stop atop &>/dev/null || :
  systemctl stop atopacct &>/dev/null || :
  systemctl stop atop-rotate.timer &>/dev/null || :
  systemctl disable atop &>/dev/null || :
  systemctl disable atopacct &>/dev/null || :
  systemctl disable atop-rotate.timer &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING
%dir %{_localstatedir}/log/%{name}/
%config(noreplace) %{_sysconfdir}/sysconfig/atop
%config(noreplace) %{_unitdir}/atop.service
%config(noreplace) %{_unitdir}/atopacct.service
%config(noreplace) %{_unitdir}/atop-rotate.service
%config(noreplace) %{_unitdir}/atop-rotate.timer
%{_sharedstatedir}/systemd/system-sleep/atop-pm.sh
%{_datadir}/%{name}/atop.daily
%{_bindir}/atop
%{_bindir}/atopcat
%{_bindir}/atopconvert
%{_bindir}/atophide
%{_bindir}/atopsar
%{_sbindir}/atopacctd
%{_mandir}/man1/atop.1*
%{_mandir}/man1/atopsar.1*
%{_mandir}/man1/atopcat.1*
%{_mandir}/man1/atopconvert.1*
%{_mandir}/man1/atophide.1*
%{_mandir}/man5/atoprc.5*
%{_mandir}/man8/atopacctd.8*

################################################################################

%changelog
* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 2.12.1-0
- Bug solution: tests during append of existing raw log are less strict now

* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 2.12.0-0
- Add PSI bar graphs for CPU, memory and disks
- Improved handling of raw log files
- Support of parallel output streams
- Security-related improvements
- Modified handling of UID/GID
- Recognize fake NUMA
- Consistent highlighting of current sort criterium
- Network interface errors added to output of flags -P and -J
- Branch to end of raw log file by pressing key 'Z'
- Remove double wrefresh call for memory graph that caused screen flashing
  in bar graph mode
- Improved sanity check for number of threads versus number of processes
- Various other bug solutions

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 2.11.1-0
- Security fix for CVE-2025-31160

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.11.0-0
- Cgroups (version 2) support.
- Show the hierarchical structure of cgroups and the related metrics with
  key/option 'G', and define the cgroup depth with the keys/options 2 till 7.
  Key/option 8 also shows the processes per cgroup level, except the kernel
  processes in the root cgroup. Key/option 9 shows the related processes per
  cgroup level including the kernel processes in the root cgroup. With
  key/option 'C' the output is sorted on CPU consumption (default), with
  key/option 'M' on memory consumption, and with key/option 'D' (requires
  root privileges) on disk utilization.
- Note: The collection of cgroup information per process is not supported any
  more.
- Twin mode: live measurement with review option.
- In twin mode atop spawns into a lower level process that gathers the counters
  and writes them to a temporary raw file, and an upper level process that reads
  the counters from the temporary raw file and presents them to the user.
- The reading of the upper level process keeps in pace with the written samples
  of the lower level process for live measurements. However, when pressing the
  'r' (reset to measurement begin), the 'b' (branch to time stamp), or the 'T'
  (previous sample), the upper level process implicitly pauses with the
  possibility to review previous samples. The 'z' (explicit pause) can also be
  used to pause the live measurement. When pressing the 'z' again (continue
  after pause) viewing of the live measurement will be continued.
- Various corrections related to JSON output.
- Improved gathering of current CPU frequency.
- Support more than 500 CPUs.
- The format of the raw file is incompatible with previous versions. Raw files
  from previous versions can be converted to the new layout with the atopconvert
  command.

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 2.10.0-0
- Additional memory statistics on system level: amount of available memory,
  amount of memory used for Transparant Huge Pages, amount of memory used by two
  categories of static huge pages (usually 2MiB and 1GiB), and the number
  of pages transferred to/from zswap.
- Additional counters for the number of idle threads on system level and process
  level.
- Refined view of memory bar graph, including free static huge pages.
- Generic way to determine the container id or pod name for containerized
  processes.
- Support for a BPF-based alternative for the netatop kernel module to gather
  network statistics per process/thread.
- Use the -z flag followed by a regex to prepend matching environment variables
  to the full command line that is shown per process (with key 'c').
- Various bugfixes (like memory leak when switching to bar graph mode) and minor
  improvements.
- Bugfix: failing malloc while starting atopsar (unprivileged) for a live
  measurement.
- The program atophide can be used to make an extraction from an input raw log
  to an output raw log, optionally specifying a begin time and/or an end time.
- The format of the raw file is incompatible with previous versions. Raw files
  from previous versions can be converted to the new layout with the atopconvert
  command.

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.9.0-0
- Introduction of bar graph mode
- Additional counters per thread showing the number of voluntary and
  involuntary context switches (key 's')
- Improved handling of process accounting
- Various bugfixes and minor improvements
- Various bugfixes (to avoid loss of synchronization and race conditions)

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
