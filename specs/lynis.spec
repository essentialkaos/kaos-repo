################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:    Security auditing and hardening tool
Name:       lynis
Version:    3.0.9
Release:    0%{?dist}
License:    GPLv3
Group:      Development/Tools
URL:        https://cisofy.com/lynis/

Source0:    https://github.com/CISOfy/%{name}/archive/%{version}.tar.gz

Source100:  checksum.sha512

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   bash >= 4 procps-ng audit e2fsprogs module-init-tools

Provides:   %{name} = %{version}-%{release}

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
%{crc_check}

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
%{_datadir}/%{name}
%{_mandir}/man8/%{name}.*

################################################################################

%changelog
* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 3.0.9-0
- DBS-1820 - Added newer style format for Mongo authorization setting
- FILE-6410 - Locations added for plocate
- SSH-7408 - Only test Compression if sshd version < 7.4
- Improved fetching timestamp
- Minor changes such as typos

* Sat Oct 22 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.8-0
- MALW-3274 - Detect McAfee VirusScan Command Line Scanner
- PKGS-7346 Check Alpine Package Keeper (apk)
- PKGS-7395 Check Alpine upgradeable packages
- EOL for Alpine Linux 3.14 and 3.15
- AUTH-9408 - Check for pam_faillock as well (replacement for pam_tally2)
- FILE-7524 - Test enhanced to support symlinks
- HTTP-6643 - Support ModSecurity version 2 and 3
- KRNL-5788 - Only run relevant tests and improved logging
- KRNL-5820 - Additional path for security/limits.conf
- KRNL-5830 - Check for /var/run/needs_restarting (Slackware)
- KRNL-5830 - Add a presence check for /boot/vmlinuz
- PRNT-2308 - Bugfix that prevented test from storing values correctly
- Extended location of PAM files for AARCH64
- Some messages in log improved

* Sat Oct 22 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.7-0
- MALW-3290 - Show status of malware components
- OS detection for RHEL 6 and Funtoo Linux
- Added service manager openrc
- DBS-1804 - Added alias for MariaDB
- FINT-4316 - Support for newer Ubuntu versions
- MALW-3280 - Added Trend Micro malware agent
- NETW-3200 - Allow unknown number of spaces in modprobe blacklists
- PKGS-7320 - Support for Garuda Linux and arch-audit
- Several improvements for busybox shell
- Russian translation of Lynis extended

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.6-0
- OS detection: Artix Linux, macOS Monterey, NethServer, openSUSE MicroOS
- Check for outdated translation files
- DBS-1826 - Check if PostgreSQL is being used
- DBS-1828 - Test multiple PostgreSQL configuration file(s)
- KRNL-5830 - Sort kernels by version instead of modification date
- PKGS-7410 - Don't show exception for systems using LXC
- GetHostID function: fallback options added for Linux systems
- Fix: macOS Big Sur detection
- Fix: show correct text when egrep is missing
- Fix: variable name for PostgreSQL
- German and Spanish translations extended

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- OS detection of Arch Linux 32, BunsenLabs Linux, and Rocky Linux
- CRYP-8006 - Check MemoryOverwriteRequest bit to protect against
  cold-boot attacks (Linux)
- ACCT-9622 - Corrected typo
- HRDN-7231 - When calling wc, use the short -l flag instead
  of --lines (Busybox compatibility)
- PKGS-7320 - extended to Arch Linux 32
- Generation of host identifiers (hostid/hostid2) extended
- Linux host identifiers are now using ip as preferred input source
- Improved logging in several areas

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.4-0
- ACCT-9670 - Detection of cmd tooling
- ACCT-9672 - Test cmd configuration file
- BOOT-5140 - Check for ELILO boot loader presence
- OS detection of AlmaLinux, Garuda Linux, Manjaro (ARM), and others
- BOOT-5104 - Add service manager detection support for runit
- FILE-6430 - Report suggestion only when at least one kernel module is not
  in the blacklist
- FIRE-4540 - Corrected nftables empy ruleset test
- LOGG-2138 - Do not check for klogd when metalog is being used
- TIME-3185 - Improved support for Debian stretch
- Corrected issue when Lynis is not executed directly from lynis directory

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- HRDN-7231 - Check for registered non-native binary formats
- OS detection of Parrot GNU/Linux
- DBS-1816 - Force test to check only password authentication
- KRNL-5677 - Support for NetBSD
- Bugfix: command 'configure settings' did not work as intended

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- AUTH-9284 - Scan for locked user accounts in /etc/passwd
- LOGG-2153 - Loghost configuration
- TOOL-5130 - Check for active Suricata daemon
- OS detection of Flatcar, IPFire, Mageia, NixOS, ROSA Linux, SLES (extended),
  Void Linux, Zorin OS
- OS detection of OpenIndiana (Hipster and Legacy), Shillix, SmartOS, Tribblix,
  and others
- EOL dates for Alpine, macOS, Mageia, OmniosCE, and Solaris 11
- Support for Solaris svcs (service manager)
- Enumeration of Solaris services
- ACCT-9626 - Detect sysstat systemd unit
- AUTH-9230 - Only fail if both SHA_CRYPT_MIN_ROUNDS and SHA_CRYPT_MAX_ROUNDS
  are undefined
- BOOT-5184 - Support for Solaris
- KRNL-5830 - Improved reboot test by ignoring known bad values
- KRNL-5830 - Ignore rescue kernel such as on CentOS systems
- KRNL-5830 - Detection of Alpine Linux kernel
- NETW-2400 - Compatibility change for hostname check
- NETW-3012 - Support for Solaris
- PKGS-7410 - Don't show exception if no kernels were found on the disk
- TIME-3185 - Supports now checking files at multiple locations (systemd)
- ParseNginx function: Support include on absolute paths
- ParseNginx function: Ignore empty included wildcards
- Set 'RHEL' as OS_NAME for Red Hat Enterprise Linux
- HostID: Use first e1000 interface and break after match
- Translations extended and updated
- Test if pgrep exists before using it
- Better support for busybox shell
- Small code enhancements

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- Detection of Alpine Linux
- Detection of CloudLinux
- Detection of Kali Linux
- Detection of Linux Mint
- Detection of macOS Big Sur (11.0)
- Detection of Pop!_OS
- Detection of PHP 7.4
- Malware detection tool: Microsoft Defender ATP
- New flag: --slow-warning to allow tests more time before showing a warning
- Test TIME-3185 to check systemd-timesyncd synchronized time
- rsh host file permissions
- AUTH-9229 - Added option for LOCKED accounts and bugfix for
  older bash versions
- BOOT-5122 - Presence check for grub.d added
- CRYP-7902 - Added support for certificates in DER format
- CRYP-7931 - Added data to report
- CRYP-7931 - Redirect errors (e.g. when swap is not encrypted)
- FILE-6430 - Don't grep nonexistent modprobe.d files
- FIRE-4535 - Set initial firewall state
- INSE-8312 - Corrected text on screen
- KRNL-5728 - Handle zipped kernel configuration correctly
- KRNL-5830 - Improved version detection for non-symlinked kernel
- MALW-3280 - Extended detection of BitDefender
- TIME-3104 - Find more time synchronization commands
- TIME-3182 - Corrected detection of time peers
- Fix: hostid generation routine would sometimes show too short IDs
- Fix: language detection
- Generic improvements for macOS
- German translation updated
- End-of-life database updated
- Several minor code enhancements

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- Security: test PATH and warn or exit on discovery of dangerous location
- Security: additional safeguard by testing if common system tools are available
- Security: test parameters and arguments for presence of control characters
- Security: filtering out unexpected characters from profiles
- Security: test if setuid bit is set on Lynis binary
- New function: DisplayException
- New function: DisplayWarning
- New function: Equals
- New function: GetReportData
- New function: HasCorrectFilePermissions
- New function: Readonly
- New function: SafeFile
- New function: SafeInput
- New option: --usecwd - run from the current working directory
- New profile option: disable-plugin - disables a single plugin
- New profile option: ssl-certificate-paths-to-ignore - ignore a path
- New test: AUTH-9229 - check used password hashing methods
- New test: AUTH-9230 - check group password hashing rounds
- New test: BOOT-5109 - test presence rEFInd boot loader
- New test: BOOT-5264 - run systemd-analyze security
- New test: CRYP-7930 - test for LUKS encryption
- New test: CRYP-7931 - determine if system uses encrypted swap
- New test: CRYP-8004 - presence of hardware random number generator
- New test: CRYP-8005 - presence of software random number generator
- New test: DBS-1828 - PostgreSQL configuration files
- New test: FILE-6394 - test virtual memory swappiness (Linux)
- New test: FINT-4316 - presence of AIDE database and size test
- New test: FINT-4340 - check dm-integrity status (Linux)
- New test: FINT-4341 - verify status of dm-verity (Linux)
- New test: INSE-8314 - test for NIS client
- New test: INSE-8316 - test for NIS server
- New test: NETW-2400 - test hostname for valid characters and length
- New test: NETW-2706 - check DNSSEC (systemd)
- New test: NETW-3200 - determine enabled network protocols
- New test: PHP-2382 - detect listen option in PHP (FPM)
- New test: PROC-3802 - check presence of prelink tooling
- New test: TIME-3180 - report if ntpctl cannot communicate with OpenNTPD
- New test: TIME-3181 - check status of OpenNTPD time synchronisation
- New test: TIME-3182 - check OpenNTPD has working peers
- New report key: openssh_daemon_running
- New command: lynis generate systemd-units
- Sending USR1 signal to Lynis process will show active status
- Measure timing of tests and report slow tests (10+ seconds)
- Initial support for Clear Linux OS
- Initial support for PureOS
- Support for X Binary Package (xbps)
- Added end-of-life data for Arch Linux and Debian
- Detection and end-of-life data added for Amazon Linux
- Detection of linux-lts on Arch Linux
- Translations: Russian added
- Function: CheckItem() now returns only exit code (ITEM_FOUND is dropped)
- Function: IsRunning supports the --user flag to define a related user
- Function: PackageIsInstalled extended with pacman support
- Profiles: unused options removed
- Profiles: message is displayed when old format "key:value" is used
- Binaries: skip pacman when it is the game instead of package manager
- Security: the 'nounset' (set -u) parameter is now activated by default
- AUTH-9228 - HP-UX support
- AUTH-9234 - NetBSD support
- AUTH-9252 - corrected permission check
- AUTH-9266 - skip .pam-old files in /etc/pam.d
- AUTH-9268 - Perform test also on DragonFly, FreeBSD, and NetBSD
- AUTH-9282 - fix: temporary variable was overwritten
- AUTH-9408 - added support for pam_tally2 to log failed logins
- AUTH-9489 - test removed as it is merged with AUTH-9218
- BANN-7126 - additional words for login banner are accepted
- BOOT-5122 - check for defined password in all GRUB configuration files
- CONT-8106 - support newer 'docker info' output
- CRYP-7902 - optionally check also certificates provided by packages
- CRYP-8002 - gather kernel entropy on Linux systems
- FILE-6310 - support for HP-UX
- FILE-6330 - corrected description
- FILE-6374 - changed log and allow root location to be changed
- FILE-6374 - corrected condition to find 'defaults' flag in /etc/fstab
- FILE-6430 - minor code improvements and show suggestion with more details
- FILE-7524 - optimized file permissions testing
- FINT-4328 - corrected text in log
- FINT-4334 - improved process detection for lfd
- HOME-9304 - improved selection for normal users
- HOME-9306 - improved selection for normal users
- INSE-8050 - added com.apple.ftp-proxy and improved text output
- INSE-8050 - corrected function call for showing suggestion
- INSE-8116 - added rsync service
- INSE-8314 - changed text of suggestion
- INSE-8318 - test for TFTP client tools
- INSE-8320 - test for TFTP server tools
- INSE-8342 - renamed to INSE-8304
- KRNL-5788 - don't complain about missing /vmlinuz for Raspi
- KRNL-5820 - extended check to include limits.d directory
- KRNL-5830 - skip test partially when running non-privileged
- KRNL-5830 - detect required reboots on Raspbian
- KRNL-6000 - check more sysctls
- LOGG-2154 - added support for rsyslog configurations
- LOGG-2190 - skip mysqld related entries
- MACF-6234 - SELinux tests extended
- MAIL-8804 - replaced static strings with translation-aware strings
- MALW-3280 - Kaspersky detection added
- MALW-3280 - CrowdStrike falcon-sensor detection added
- NAME-4402 - check if /etc/hosts exists before performing test
- NAME-4404 - improved screen and log output
- NAME-4408 - corrected Report function call
- NETW-3032 - small rewrite of test and extended with addrwatch
- PHP-2372 - don't look in the cli configuration files
- PKGS-7388 - only perform check for Debian/Ubuntu/Mint
- PKGS-7410 - use multiple package managers when available
- PKGS-7410 - added support for Zypper to test number of kernels
- PRNT-2308 - check also for Port and SSLListen statements
- PROC-3602 - allow different root directory
- PROC-3612 - show 'Not found' instead of 'OK'
- PROC-3614 - show 'Not found' instead of 'OK'
- PROC-3802 - limit to Linux only (prelink package check)
- SCHD-7702 - removed hardening points
- SINT-7010 - limit test to only macOS systems
- SSH-7402 - detect other SSH daemons like dropbear
- SSH-7406 - strip OpenSSH patch version and remove characters (carriage return)
- SSH-7408 - changed text in suggestion and report
- SSH-7408 - added forced-commands-only option
- SSH-7408 - VerifyReverseMapping removed (deprecated)
- SSH-7408 - corrected OpenSSH server version check
- STRG-1840 - renamed to USB-1000
- STRG-1842 - added default authorized devices and renamed to USB-2000
- TIME-3104 - use find to discover files in cron directories
- TOOL-5002 - differentiate between a discovered binary and running process
- TOOL-5160 - added support for OSSEC agent daemon
- Perform additional check to ensure pacman package manager is used
- Use 'pre-release/release' (was: 'dev/final') with 'lynis show release'
- Use only locations from PATH environment variable, unless it is not defined
- Show tip to use 'lynis generate hostids' when host IDs are missing
- The 'show changelog' command works again for newer versions
- Several code cleanups, simplification of commands, and code standardization
- Tests using lsof may ignore individual threads (if supported)
- Corrected end-of-life detection for CentOS 7 and CentOS 8
- Tests can require detected package manager (--package-manager-required)
- Do not show tool tips when quiet option is used
- Improved screen output in several tests
- Extended output of 'lynis update info'
- Improved support for NetBSD
- Test if profiles are readable
- systemd service file adjusted
- bash completion script extended
- Updated man page
