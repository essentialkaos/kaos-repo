################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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

################################################################################

Summary:            Security auditing and hardening tool
Name:               lynis
Version:            2.6.9
Release:            0%{?dist}
License:            GPLv3
Group:              Development/Tools
URL:                https://cisofy.com/lynis/

Source0:            https://github.com/CISOfy/%{name}/archive/%{version}.tar.gz

BuildArch:          noarch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           bash >= 4

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Lynis is a security auditing for Unix derivatives like Linux, BSD, and
Solaris. It performs an in-depth security scan on the system to detect
software and security issues. Besides information related to security,
it will also scan for general system information, vulnerable software
packages, and possible configuration issues.

We believe software should be simple, updated on a regular basis and open.
You should be able to trust, understand, and even alter the software.
Many agree with us, as the software is being used by thousands every
day to protect their systems.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man8/
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}

install -pm 755 %{name}     %{buildroot}%{_bindir}/%{name}
install -pm 444 %{name}.8   %{buildroot}%{_mandir}/man8/
install -pm 644 default.prf %{buildroot}%{_sysconfdir}/%{name}

cp -r db extras include plugins %{buildroot}%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md CONTRIBUTORS.md FAQ LICENSE README.md
%{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.*
%{_datadir}/%{name}

################################################################################

%changelog
* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.9-0
- Man page has been updated
- Command 'lynis show options' provides up-to-date list
- Option '--dump-options' is deprecated
- Several options and commands have been extended with more examples
- OS detection now supports openSUSE specific distribution names
- Changed command output when using 'lynis audit system remote'
- DBS-1882 - added /usr/local/redis/etc path and QNAP support
- PKGS-7322 - updated solution text
- KRNL-5788 - ignore exception when no vmlinuz file was discovered
- TIME-3104 - extended logging for test

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.8-0
- BOOT-5104 - improved parsing of boot parameters to init process
- PHP-2372 - test all PHP files for expose_php and improved logging
- Alpine Linux detection for Docker audit
- Docker check now tests also for CMD, ENTRYPOINT, and USER configuration
- Improved display in Docker output for showing which keys are used for signing

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.7-0
- BOOT-5104 - Added busybox as a service manager
- KRNL-5677 - Limit PAE and no-execute test to AMD64 hardware only
- LOGG-2190 - Ignore /dev/zero and /dev/[aio] as deleted files
- SSH-7408 - Changed classification of SSH root login with keys
- Docker scan uses new format for maintainer value
- New URL structure on CISOfy website implemented for Lynis controls

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.6-0
- New format of changelog (https://keepachangelog.com/en/1.0.0/)
- KRNL-5830 - improved log text about running kernel version
- Under some condition no hostid2 value was reported
- Solved 'extra operand' issue with tr command

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.5-0
- [MAIL-8804] - Exim configuration test
- [NETW-2704] - Use FQDN to test status of a nameserver instead of own IP
  address
- [SSH-7402] - Improved test to allow configurations with a Match block

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.4-0
- Several contributions merged, including grammar improvements
- Initial support for Ubuntu 18.04 LTS
- Small enhancements for usage
- [AUTH-9308] - Made 'sulogin' more generic for systemd rescue shell
- [DNS-1600] - Initial work on DNSSEC validation testing
- [NETW-2704] - Added support for local resolver 127.0.0.53
- [PHP-2379] - Suhosin test disbled
- [SSH-7408] - Removed 'DELAYED' from OpenSSH Compression setting
- [TIME-3160] - Improvements to detect step-tickers file and entries

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.3-0
- Change in routine for host identifiers
- [CRYP-7902] - Do prevalidation for certificates before testing them
- [HRDN-7222] - Enhanced compiler permission test
- [NAME-4402] - Improved test to filter out empty lines
- [PKGS-7384] - Changes to detect yum-utils package and related tooling
- [PLGN-2680] - cron file permissions

* Sat Feb 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.2-0
- Bugfix for Arch Linux (binary detection)
- Textual changes for several tests
- Update of tests database

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.1-0
- Tests can have more than 1 required OS (e.g. Linux OR NetBSD)
- Added 'system-groups' option to profile (Enterprise users)
- Overhaul of default profile and migrate to new style (setting=value)
- Show warning if old profile options are used
- Improved detection of binaries
- New group 'usb' for tests related to USB devices
- [FILE-6363] - New test for /var/tmp (sticky bit)
- [MAIL-8802] - Added exim4 process name to improve detection of Exim
- [NETW-3030] - Changed name of dhcp client name process and added udhcpc
- [SSH-7408] - Restored UsePrivilegeSeparation
- [TIME-3170] - Added chrony configuration file for NetBSD

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.7-0
- Update of Portuguese translation
- Added --silent as alias for --quiet
- Reduced screen output when running non-privileged
- IsRunning function now allows full name process match

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.5-0
- Minor release to solve errors on screen
- CRYP-7902 - certificate validation changed

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.1-0
- Hebrew translation by Dolev Farhi
- Improved detection of SSL certificate files
- Minor changes to improve logging and results
- BOOT-5104 - Added support for macOS
- FIRE-4524 - Determine if CSF is in testing mode
- HTTP-6716 - Improved log message

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Use ROOTDIR variable instead of fixed paths
- Introduction of IsEmpty and HasData functions for readability of code
- Renamed some variables to better indicate their purpose (counting, data type)
- Removal of unused code and comments
- Deleted unused tests from database file
- Correct levels of identation
- Support for older mac OS X versions (Lion and Mountain Lion)
- Initialized variables for more binaries
- Additional sysctls are tested
- MALW-3280 - Extended test with Symantec components
- PKGS-7332 - Detection of macOS ports tool and installed packages
- TOOL-5120 - Snort detection
- TOOL-5122 - Snort configuration file

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4.6-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Updated to latest stable release

* Thu Oct 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.4-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- Updated to latest stable release

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest stable release

* Wed Oct 07 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Initial build
