################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __sysctl          %{_bindir}/systemctl

################################################################################

%bcond_without snmp
%bcond_without vrrp
%bcond_with profile
%bcond_with debug

################################################################################

Name:              keepalived
Summary:           High Availability monitor built upon LVS, VRRP and service pollers
Version:           2.0.18
Release:           0%{?dist}
License:           GPLv2+
URL:               http://www.keepalived.org
Group:             System Environment/Daemons

Source0:           https://www.keepalived.org/software/%{name}-%{version}.tar.gz
Source1:           %{name}.init

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with snmp}
BuildRequires:     net-snmp-devel
%endif

BuildRequires:     gcc make openssl-devel libnl-devel kernel-devel popt-devel
BuildRequires:     libnfnetlink-devel

%if %{with snmp}
Requires:          net-snmp-libs
%endif

Requires:          lm_sensors-libs

%if 0%{?rhel} >= 7
Requires:          systemd
%else
Requires:          kaosv >= 2.15

Requires(post):    %{__chkconfig}
Requires(preun):   %{__chkconfig}
Requires(preun):   %{__service}
Requires(postun):  %{__service}
%endif

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Keepalived provides simple and robust facilities for load balancing
and high availability to Linux system and Linux based infrastructures.
The load balancing framework relies on well-known and widely used
Linux Virtual Server (IPVS) kernel module providing Layer4 load
balancing. Keepalived implements a set of checkers to dynamically and
adaptively maintain and manage load-balanced server pool according
their health. High availability is achieved by VRRP protocol. VRRP is
a fundamental brick for router failover. In addition, keepalived
implements a set of hooks to the VRRP finite state machine providing
low-level and high-speed protocol interactions. Keepalived frameworks
can be used independently or all together to provide resilient
infrastructures.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure \
    %{?with_debug:--enable-debug} \
    %{?with_profile:--enable-profile} \
    %{!?with_vrrp:--disable-vrrp} \
    %{?with_snmp:--enable-snmp}
%{__make} %{?_smp_mflags} STRIP=/bin/true

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_sysconfdir}/%{name}/samples/

%if 0%{?rhel} <= 6
rm -rf %{buildroot}%{_libdir32}/systemd
rm -rf %{buildroot}%{_sysconfdir}/init/%{name}.conf
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

%if %{with snmp}
  mkdir -p %{buildroot}%{_datadir}/snmp/mibs/
  install -pm 644 doc/KEEPALIVED-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

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
if [[ $1 -ge 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} daemon-reload &>/dev/null || :
%else
  %{__service} %{name} restart &>/dev/null || :
%endif
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README.md TODO
%doc doc/%{name}.conf.SYNOPSIS doc/samples/%{name}.conf.*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/genhash
%{_sbindir}/%{name}
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*
%{_defaultdocdir}/%{name}/README

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%if %{with_snmp}
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

################################################################################

%changelog
* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.18-0
- Set NA_ROUTER flag in gratuitous NA messages appropriately.
  Previously keepalived checked the IPv6 forwarding state of the interface/
  parent interface of a VRRP instance, and used that for all GNA messages.
  However, if addresses are configured on different interfaces, it should
  be the setting for the address's interface that is used.
- Fix memory leak with dbus_instance_name.
- Make set_value() add entry for memcheck identifying where called.
- Add configure option --enable-checksum-debug.
  Issue #1175 identified that intermittently they were getting VRRPv3
  checksum errors. The maintainers of keepalived were unable to reproduce
  the problem despite extensive testing, and so a special patch was produced
  to check and log any checksum changes from previous adverts sent or received.
  Almost two months later there has been no feedback. The patch has now been
  forward ported from v2.0.12 to v2.0.17 and is included here, enabled by
  --enable-checksum-debug option, so that if there are ever any checksum
  problems.
  in the future this code can be used to ascertain what is happening.
- Fix configuring LVS sync daemon in backup state.
  Commit eb929f8 - "Stop LVS sync daemon on shutdown" moved shutting
  down the LVS sync daemon to the wrong place, so that it was called
  whenever a VRRP instance transitioned out of master state. This
  commit moves the shutting down of the sync daemon to shutdown phase 1,
  and it is shutdown before the VRRP instances are shut down.
- Increase open file limit for checker process if no of checkers need it.
  TCP, HTTP/SSL, DNS and SMTP checkers all use a socket. If there is a
  sufficiently large number of checkers, the default open file limit may
  be exceeded. This commits counts the number of such checkers, and also
  thr number of smtp_alerts, and if necessary increases the open file limit
  to allow them all to run at once.
- Ensure MISC_CHECK processes don't get increase open file limit.
- When checking number of open files for vrrp process, allow for smtp
  alerts.
- Combine checker set_max_file_limit() and set_vrrp_max_fds() common
  code.
- DNS_CHECK: correct error info in dns_type_handler func.
  Sometimes, users set two type values by mistake in keepalived.conf,
  and the first is right and the second one is not in DNS_TYPE[].
  Then the dns_check->type is set successfully when parsing first type value
  , which may be different from the default SOA. As for the second one,
  the dns_type_handler func will print error info "Defaulting to SOA",
  actually, currently the dns_check->type may be not equal to SOA.
  Here, we will print the dns_type_name(dns_check->type) instead of "SOA".
- Simplify restoring RLIMIT_NOFILE for child processes.
- Simplify handling incorrect dns_check type.
- Add missing track_process documentation to keepalived.conf(5) man
  page.
- Add weight "reverse" feature to track_bfd.
  The reverse feature allows reducing the priority when the tracker is up
  and reducing the priority when the tracker is down.
- Add weight "reverse" feature to track_interface.
  The reverse feature allows reducing the priority when the tracker is up
  and reducing the priority when the tracker is down.
- Add weight "reverse" feature to track_script.
  The reverse feature allows reducing the priority when the tracker is up
  and reducing the priority when the tracker is down.
- Update alloc_track_file() and alloc_group_track_file() to be
  consistent.
- Allow reverse tracking with weight 0.
  This allows a vrrp instance to go to fault state if an interfaces is UP,
  or a track script or bfd instance is up, or a track process has achieved
  quorum, and down otherwise.
- Fix reverse on track_script when configured on sync group and instance
  If a track script was configured on both a vrrp instance and the sync
  group that the instance was configured in, then the reverse setting
  wasn't being properly carried forward.
- Add weight "reverse" feature to track_file.
  The reverse feature allows reducing the priority when the tracker is up
  and increasing the priority when the tracker is down.
- Make track_bfd reverse handling consistent with other trackers.
- Add track weight reverse to SNMP output.
- Add vrrp track_bfd details to SNMP output.
- Add vrrp track_process details to SNMP output.
- Disallow --enable-track-process-debug with --disable-track-process.
- Add conditional compilation around track_bfd/process SNMP code.
- Remove duplicate code for parsing vrrp and sync group trackers.
  The code for parsing trackers for vrrp instances and sync groups
  was to all intents and purposes identical, so this commit now uses
  common code for both of them.
- sll_protocol should be set to  0x806.
  Some times , send the gratuitous ARP message should set sll_protocol,
  let some drivers can evaluate which protocol we use.
- Neighbor discovery set sll_protocol.
- Fix SNMP VRRPv3 IP address OIDs returned.
  The OIDs returned for SNMPv3 addresses were incorrectly formatted,
  including one extra subid that was the length of the IP address.
- Don't use numeric values of address lengths for VRRP SNMP v3.
- Stop returning not-accessible fields for v2 SNMP.
- Stop return not-accessible fields for v3 SNMP.
- Use common code for VRRP tracker SNMP output.
  Many functions were using the same, fairly large, code block to do
  the same thing. These are now standardised to use the new function
  snmp_find_element().
- make some vrrp snmp function parameters const.
- Make virtual_server_t vsgname const.
- Fix SNMP reporting of virtual server group fwmark and address
  ranges.
- More SNMP fixes for virtual server group fwmark and address ranges.
- If virtual server is fwmark and rs's tunnelled, default to IPv4.
  If a virtual server uses a fwmark, and all the real servers are
  tunnelled, the address family could be IPv4 or IPv6. If the family
  is not specified, default to IPv4 (to match behavious of ipvsadm).
- Make LIST_SIZE safe to use if list is not assigned.
- Optimisations to snmp_header_list_table().
- Optimisations to snmp_find_element().
- Further optimisation to snmp_find_element().
- Add support for IPVS GUE tunnel type
  This functionality was introduced in Linux 5.2.
  To view the IPVS setup with ipvsadm requires ipvsadm v1.30 plus
  commits 2347b504e3ce and c3c2c3c6ae12e3.
- Add support for IPVS GUE tunnel checksum option.
  The kernel functionality is scheduled for Linux 5.3.
- Add support for IPVS GRE tunnels.
  The kernel functionality is scheduled for Linux 5.3.
  In addition to the ipvsadm patch requirements identified for GUE
  tunnels, the patch at
- Add pure attribute to http_get_check_compare().
  GCC was suggesting adding the pure attribute to http_get_check_compare()
  so let's do so.
- Resolve warnings from gcc 9.1.1.
- Resolve all outstanding coverity issues.
- Fix use of getrandom() in BFD rand_intv().
- When resetting priority of child process, don't change parent's priority
  Issue 1358 identified that it was the priority of the parent process,
  rather than the child process, that was being reset. This commit corrects
  that and resets the priority of the child process.
- Add missing bfd_instance vrrp and checker keyword documentation.
- Don't send bfd events to vrrp or checker process if no
  configuration.
  If there is no vrrp configuration, or no checker configuration, there
  is no point sending bfd_event notifications to the relevant processes.
  Actually, since the processes may not be running, sending such
  notifications can cause the pipes to become full, so it is necessary,
  as well as desirable, not to write events to the pipes in those
  circumstances.
- Revert use of getrandom() for bfd jitter.
  This can be called up to 1000 times a second per bfd instance, and
  so risks emptying the entropy pool.
- Use random() rather than rand() in bfd rand_intv().
  The rest of keepalived uses random(), so this changes creates more
  consistency.
- Allow bfd discriminator to be an odd number.
  rand_intv(1, UINT32_MAX) was always returning an even number, since
  RAND_MAX == UINT32_MAX / 2. This commit sets the lsb of the discriminator
  to the lsb of the current time in seconds.
- Ensure BFD source port in range 49152..65535.
  RFC5881 requires the source port for BFD packets to be in the above
  range, but keepalived was allowing the port to be randomly generated
  by the kernel, and hence could be outside the range.
  This commit sets the permitted port range to the intersection of
  [49152, 65535] and the values in /proc/sys/net/ipv4/ip_local_port_range,
  unless the intersection is too small, in which case it just uses the BFD
  specified values.
  keepalived generates a random port number in the required range, and then
  loops through the range starting from the random port number until it
  finds one it can bind to.
- Resolve coverity resource leak issue 218872.
- Resolve coverity Resource leak issue 218875.
- Resolve coverity Resource leak issue 218876.
- Resolve coverity Unexpected control flow issue 218873.
- Change code to avoid coverity String length miscalculation issue 218874
  The code was correct, but as coverity points out, strlen(str + 1) is more
  likely to be an error for strlen(str) + 1, so avoid the use of the former
  construct.
- Added CRC check for all sources

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.17-0
- Add support to define CPU affinity for vrrp, checker & bfd processes
  Created 3 new configurations keywords to set CPU affinity of Keepalived
  processes : vrrp_cpu_affinity, checker_cpu_affinity & bfd_cpu_affinity
  This option can be used to force vrrp, checker and bfd processes to run
  on a restricted CPU set. You can either bind processes to a single CPU
  or define a set of cpu. In that last case Linux kernel will be restricted
  to that cpu set during scheduling. Forcing process binding to single CPU
  can increase performances on heavy loaded box. for example:
  "vrrp_cpu_affinity 2" will force vrrp process to run on cpu_id 2
  "vrrp_cpu_affinity 2 3" will retrict kernel scheduling decision over
  cpu_id 2 & 3.
- correct syntax error when _HAVE_VRRP_VMAC_ && no HAVE_IFLA_LINK_NETNSID.
- Stage libmnl and libnftnl4.
- Add dynamic download of kernels using scriplets Also added
  Linux 5.0.0 build.
- Example build using EOL kernel from old-releases.
- Modify snapcraft.yaml to dynamically source correct kernel versions.
- dump processes CPU Affinity while dumping global conf.
  Add support to dump CPU Affinity for each Keepalived processes where
  CPU Affinity has been changed by configuration.
- Don't enclose /dev/tcp/127.0.0.1/22 in ' chars when running as script
  RedHat identified a problem with scripts like:
  vrrp_script {
    script "</dev/tcp/127.0.0.1/22"
  }
  where returning an exit code of 127 (script not found).
  This was identified to be due to the "script" being enclosed in '
  characters, so the resulting system call was
  system("'</dev/tcp/127.0.0.1/22'"), which failed. Not adding the leading
  and trailing ' characters when the first character of the script is '<'
  or '>' resolves the problem.
- Add support for use_ipvlan (use an ipvlan i/f similar to use_vmac)
  Issue #1170 identified that use_vmac didn't work with systemd-networkd
  since systemd-networkd was removing IP addresses created by keepalived
  (and any other application). It was discovered that systemd-networkd
  did not remove IP addresses from ipvlans.
  This commit adds support for ipvlans, but to work around the problem,
  and because it might have other uses.
  Systemd commit - https://github.com/systemd/systemd/pull/12511 has added
  configuration options to stop systemd-networkd removing IP addresses
  added by other applications, but it is not merged yet, and it will be a
  while before all the distros merge it.
- Fix building with ipvlans before IFLA_IPVLAN_FLAGS was defined.
- Default IPVLANs to bridge mode
  We shouldn't change the behaviour if a kernel is upgraded, so
  default to the original mode supported.
- Ensure that -lm linker library flag is always set
  configure was testing whether it was necessary to add the -lm option,
  but for some reason gcc adds it itself if -Os is not specified, but
  does not add it if -Os is specified. Consequently if configure was
  run without -Os, and make was run with -Os the link failed.
  The commit ensures that -lm is always used.
- Handle checking for -Wl,-z,relro and -Wl,-z,now properly.
- Honour CFLAGS, CPPFLAGS, LDLIBS and LDFLAGS settings when configure runs.
- Propogate CFLAGS, CPPFLAGS, LDFLAGS and LDLIBS from configure to make files
  Make sure any settings in CFLAGS etc at the time configure is run are added
  to the Makefiles, to ensure that the make is run in the same environement
  that configure is run in.
- Use CFLAGS, CPPFLAGS, LDFLAGS and LDLIBS correctly
  Use the correct variable for the relevant option type, e.g. -llib
  should be in LDLIBS, not LDFLAGS, and -Ddefn should be in CPPFLAGS
  not CFLAGS.
- Fix non-ipvlan interfaces broken by adding ipvlans.
- Check bfd instance name length before copying.
- Add lib/container.h to avoid duplicate definition of container_of.
- Revisited code to use const declaration where appropriate.
- Add STRDUP/STRNDUP functions.
- Add FREE_CONST, FREE_CONST_ONLY and REALLOC_CONST.
- Change thread_t * to thread_ref_t except in thread handler code
  Treat the thread reference as a handle, so that the only code that
  manipulates thread structures is in the scheduler.
- Add STRDUPs in check_data.
- Add STRDUP in bfp parser code.
- -U flags should be included in CPPFLAGS
- Update track_process documentation.
  Issue #1265 requested further clarify regarding the track_process
  process specification and use of quote marks.
- Fix building on Linux 3.13 (required for building snaps)
- Ensure 4 extra parameters are set for notify scripts with no shebang.
- Streamline functions returning string matching a define.
- Make addattr8/16/32/64 and rta_addrattr8/16/32/64 inline functions
  Since these functions simply call addattr_l/rta_addattr_l, making the
  functions inline removes the overhead of one function call.
- Add genhash option -P to select HTTP 1.1 or 1.0 with Connection: close
  Max Kellerman (max.kellermann@gmail.com) submitted pull request #1260
  to add "Connection: close" to the HTTP header sent by genhash. In order
  to maintain backwards compatibility, this has been implemented as an
  option '-P 1.0C'. In addition, '-P 1.1' requests that a version 1.1
  header is sent (which includes 'Connection: close').
- Add http_protocol option for HTTP_GET and SSL_GET checkers.
  To be consistent with commit 2ff56f5 - "Add genhash option -P
  to select HTTP 1.1 or 1.0 with Connection: close", this commit
  adds the http_protocol keyword for HTTP_GET and SSL_GET checkers.
  'http_protocol 1.0C' adds 'Connection: close' to a 1.0 header, and
  'http_protocol 1.1' sends an HTTP/1.1 header, which includes the
  'Connection: close' option.
- Tidy up the recieve message processing code loops in genhash.
- Add genhash -t timeout option.
- Simplify thread process in genhash after send HTTP request.
- support http status_code group
  The origin status_code only support one specific code, now we can
  support http status_code of the same class. That's to say, we can
  use 1xx to represent 100-199, 2xx means 200-299 ans so on.
  eg: The configure as follows:
  url {
      path /index.html
      status_code 2xx 3xx
  }
  which means we consider all status_code range in [200,399] is ok.
  Of course the following configure is either 200 or [300,399] is ok.
  url {
      path /index.html
      status_code 2xx 3xx
  }
- Fix compiler warnings introduced in commit c7c23a2
  Commit c7c23a2 - "support http status_code group" introduced
  two compiler warnings, due to isdigit() being undeclared, and
  a shadows declaration. These warnings are now resolved.
- Use standard bit testing and setting functions
  Commit c7c23a2 - "support http status_code group" added additional
  bit testing and setting functions, rather than using the already
  defined ones in bitops.h.
  This commit also resolves the assumption that longs are 64 bits, and
  will allow the code to work with longs of any length.
  The original commit would cause all status codes 100 to 599 to be
  written when the configuration was dumped, regardless of whether
  the specific codes were set. This commit now writes the status codes
  in ranges.
  Finally, if no status code is configured, it sets the bits for the
  default status codes (200-299).
- Change how http status codes are configured
  Commit c7c23a2 - "support http status_code group" allowed status codes to
  be specified as 2xx, meaning 200-299. This commit changes the configuration
  so that 2xx etc is no longer used, but status code ranges can be specified,
  e.g. status_code 150 180-189 200-299 503 510-520
- Update documentation for commit c7c23a2.
- Fix a memory leak and duplicate free in HTTP_GET checker.
- Fix sending SMTP alerts
  Issue #1275 identified that SMTP alerts were not working. The SMTP alerts
  were broken by commit 5860cf2 - "Make checker fail if ENETUNREACH returned
  by connect()", since the SMTP state machine was not updated to handle the
  addition value in enum connect_result.
  This commit adds code to handle the additional enum, but also makes the
  code less sensitive to such changes, and more likely to produce compiler
  warnings/errors if appropriate updates are not done in the future.
- Fix various compilation warnings with certain configure options.
- Update location of PID file to match Filesystem Hierarchy Standard v3.0
  Issue #1277 identified that PID files should be created in /run rather
  than /var/run, and that systemd logged a warning if the service file
  specified PIDFile under /var/run.
  This commit now makes keepalived use the appropriate directory for PID
  files as determined by configued (rather than doing its own thing), and
  configure now uses /run in preference to /var/run.
- Stop LVS sync daemon on shutdown
  The shutdown of the sync daemon was delayed to phase 2 of the shutdown
  which meant that the controlling VRRP instance could never be in the
  master state. We now stop the sync daemon in phase 1, when the VRRP
  instance is transitioned out of master state.
- Use -isystem rather than -I for path to kernel headers
  Using -isystem rather than -I allows the dispensation for some warnings
  to system headers to apply to the kernel header tree we are specifying.
  This stops some warnings that would not occur with kernel headers under
  /usr/include but that were being generated when -I was used (it
  nevertheless has helped identify two bugs).
- Ensure check system headers for definition of NFT_TABLE_MAXNAMELEN
  Prior to Linux 4.1 NFT_TABLE_MAXNAMELEN was not defined, but we must
  include linux/netfilter/nf_tables.h before checking whether it is
  defined or not!
- Improved configure testing for <linux/netfilter/nf_tables.h>
- Add warning -Wwrite-strings and resolve new warnings.
- Add -Wdouble-promotion and resolve new warnings.
- Add -Wformat-signedness and resolve new warnings.
- Fix building on Ubuntu 16.04 with --disable-vrrp
  The addition of including <inttypes.h> was needed on Ubuntu 16.04,
  whereas it wasn't necessary on Fedora or Debian.
- Explicitly include <inttypes.h> where print format names are used.
- Add more -Wformat-* options and resolve new warnings.
- Add -Wframe-larger-than=5120
  The largest frame is just under 4200 bytes (which may be more than we
  want anyway), but adding this warning will at least tell us if a stupidly
  large frame is created in the future.
- Fix spelling of -Wmissing-field-initializers.
- Fix definition of PRI_rlim_t generated by configure on 32 bit systems.
- Rseolve warning re >0 comparison for unsigned value.
- add min max judge
  Although even if min > max, the code works well. We better to print
  the error config to let the user know this.
- Ensure correct definition of MAX_ADDR_LEN is used
  <net/if_arp.h> defines MAX_ADDR_LEN as 7, and <linux/netdevice.h>
  defines MAX_ADDR_LEN as 32. We need to ensure we have the longer one.
- update doc samples of keepalived.conf.status_code.
- Fix compiling on Alpine Linux 3.7.
- Update list of packages to install on Alpine Linux.
- Send GARP/NA message when leaving fault state if using unicast
  If the master's ARP entry for a backup route has expired and we are
  using a short advert interval (< 0.5 seconds), then the backup router
  could timeout receiving adverts before the master sends its next
  ARP/NDISC message; until it has had a reply to that it cannot send any
  adverts to the backup router in question.
  This commit makes a VRRP instance that is using unicast send a GARP/NA
  when it transitions out of fault state, to ensure that the master (or
  local router) can send adverts to us immediately.
- track_process: handle different threads having different names
  prctl(PR_SET_NAME) is a per thread property, not a per process
  property, so when a PROC_EVENT_COMM event is received, we need to
  check that the tid == pid, so ensure that only the main (initial)
  thread that COMM changes are considered for.
- Fix some log_message for specifiers in track_process.c.
- Fix for JSON characters escaping.
- Don't attempt to create a macvlan when using an ipvlan
  netlink_link_add_vmac() detected an interface had been created, and
  so didn't attempt to create a macvlan, but netlink_link_add_vmac()
  shouldn't be called in this circumstance.
- On reload, report addresses being removed as removed, not thos remaining.
- Don't add further iptables entries on reload when using ipsets.
- Stop deleting VMAC/IPVLAN interfaces on reload when still needed.
- Fix formatting of email To: line.
- Improve efficiency of setting up SMTP headers.
- Fix segfault when we do not config vsg.
- Fix issues reported by coverty (unchecked return value, buffer overrun,
  Logically dead code, uinitialized var, explicit null dereferenced, ...)
- Resolve compiler warning in list_sort().
- genhash: make printssl a static function.
- Change strncpy() to strcpy_safe() in smtp_final().
- Convert some snmp list loops to use LIST_FOREACH.
- Make inet_stosockaddr() return bool rather than int.
- Fix checking for VMAC/IPVLAN no longer used after reload
  Pull request 1310 identified that there was a problem building
  keepalived with VLANs but without ipvlans. The code that needed
  changing was also incorrect so this commit resolves both issues.
- Fix false-positive send_instance_notifies calls
  Issue #1311 identified that duplicate notifies were being sent on
  a reload, and pull request #1312 provided a fix. Unfortunately other
  intervening commits stopped the original patch applying, so this
  updates the original patch.
  The patch also stops duplicate logging of vrrp instance states on
  reload when there has been no change.
- Set thread parameter value explicitly to 0 when add timer thread
  It is possible for a function to be called either from a timer thread
  or an event thread. When an event thread is added, a vlue can be passed
  which will be passed to the function, but currently there is no way to
  set the value for a timer thread (a function thread_add_timer_val() can
  be added when needed), but in order to allow the value to be used with
  an event thread, it needs to be explicitly set to something when called
  via a timer thread, so just set it to 0.
- Remove VRRP_DISPATCHER definition - it was not used.
- Some minor tweaks for the format of keepalived.data.
- Make track_process, parser and dump_keywords --debug options.
- Change default to not check for EINTR if use signalfd.
- Don't send prio 0 adverts for deleted VRRP instance that wasn't master
  When a VRRP instance ceases to exist following a config reload, we must
  only send priority 0 adverts if the deleted instance was in master state
  prior to the reload.
- Send notifies when vrrp instance deleted on reload
  This commit makes notifies be send saying that the instance is in
  fault state, since that is the closest we have to the instance being
  deleted (the instance can't run since it is deleted which is quiet
  similar to being in fault state).
- Streamline some HTTP_GET code.
- Simplify HTTP_GET epilog parameters
  Parameters t and c weren't needed, since they can be determined from
  the method parameter if we add REGISTER_CHECKER_FAILED.
- Set checker->has_run for HTTP_GET after failure
  The behaviour we want after a failure of checking a URL at startup
  is the same as if all checks had completed, so if there is a failure,
  just set checker->has_run.
- Make http_get url_it point to list element rather than a counter
  This makes fetching the next URL more efficient.
- When we run the initial HTTP_GET check, we don't want any retries
  It isn't only the first URL that shouldn't have retries, but all of
  them. This commit implements that.
- When an HTTP_GET url check fails, keep checking that URL until success
  When a URL check has failed, there is no point checking other URLs until
  we know the one that has failed is working again. The approach now is
  that the failed URL is checked until it is Ok again, and then all the URLs
  are checked before the checker is successful. This will reduce the recovery
  time once the failed URL recovers.
- When starting up, don't delay between checking all the URLs
  When we start up, particularly in alpha mode, we want to check the
  URLs as quickly as possible, so don't delay by delay_loop between
  checking each URL, but check them immediately one after the other.
- After HTTP_GET URL failure, delay max of delay_loop and delay_before_retry.
- After an HTTP_GET failure, check the URLs without any delay
  This means that recovery will occur as quickly as possible.
- Some cosmetic changes to check_ssl.c.
- Add option fast_recovery for HTTP_GET.
  Commits 3027e0c - "When starting up, don't delay between checking all the
  URLs" and 86e02dd - "After an HTTP_GET failure, check the URLs without
  any delay" removed the delay between URL checks both at startup and after
  a URL check failure. This commit makes that options, and it will only do
  the fast checking if fast_recovery is configured against the checker.
- Make set_value() check for missing parameter
  Pull request #1308 identifed that if set_value() was called when
  there wasn't a parameter on the command line, keepalived could
  segfault since NULL was returned (examples were HTTP_GET with an
  empty path specified, and DNS_CHECK with empty name).
  This commit modifies set_value() so that keepalived will exit if
  it is called with no keyword parameter is missing. Uses of
  set_value() where no parameter did not cause a problem (e.g. where
  the whole option was optional, such as virtual_host) now check if
  the parameter is mising and report a configuration error.
- Handle vrrp tracked interfaces being down on reload
  If the base interface of a vmac interface was down on reload, the
  vrrt instance would not come back up after the base interface came
  back up.
- Don't log error when sending priority 0 advert after interface goes down.
- Cosmetic change to address_exist().
- Add information regarding SElinux and keepalived.
- Fix overflow status code
  Under normal circumstances, status_code returns 100-599,
  but if it is a constructed abnormal reply message,
  it may be out of the range, resulting in the status_code
  array out of bounds, and then keepalived segfault.
- Ensure HTTP status code is preceeded by a space character.
- Fix setting existing macvlan etc base interfaces at startup.
- Add further SELinux references.
- Resolve implicit declaration of function â€˜strdupâ€™ warning.
- Allow location of /run dir to be specified to configure
  The commit adds configure option --with-run-dir=PATH
- Fix reloading when interfaces deleted and recreated
  If have macvlans on a real interface, with vmacs configured on the
  macvlans and the macvlans are deleted, the vmacs from them are removed
  from the configuration, the configuration is reloaded, and this is done
  for more than one macvlan, and then the configuration is reinstated
  one by one with the configuration being reloaded, keepalived was
  incorrectly setting some of the vrrp instances to fault state. This commit
  resolves the issues.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.16-0
- Add log_unknown_vrids keyword.
  Commit 21e6f5f added logging when a VRRP packet was received on an
  interface and the VRID in the advert was not configured on that
  interface.
  Due to valid uses of keepalived having a VRRP instance on an
  interface, but there being other, independent, VRRP instances with
  different VRIDs on the same interface, this patch only enables logging
  of unknown VRIDs if it is specifically configured.
- Stop segfault when reload and using -x option.
- Fix compilation error found by Travis-CI.
- Fix a couple of typos.
- Ensure check command line when needed for track process.
- Check if comm really changed when get PROC_EVENT_COMM_CHANGE.
- Fix debounce delay handling for track_process.
- Optimise add_process().
- Remove processes no longer being monitored.
- Optimise check_process().
- Ignore process threads for track_process.
- Allow matching of process parameters in track_process
  This additional functionality was requested in issue #1190.
- Allow separate delay timers for fork and process exit in
  track_process.
- Add quorum_max for track_process.
  This allows track_process to go to fault state if more than a
  specified number of instances of a process are running. In particular
  it can go to fault state if more than one instance is running, and
  also if any instance of a process is running.
- Add configuring process name.
  With up to 4 processes running all named keepalived, it can be
  difficult to know which is which. The commit adds the option to
  allow process name to be set independantly for each process.
- Handle macvlans/macvtaps being moved into different namespace from parent
  If a macvlan or macvtap interface is moved into a different namespace from
  its parent, and the interface is in the namespace in which keepalived is
  running, keepalived is unable to get information about, or configure, the
  parent interface. In this case, treat the macvlan/macvtap interface as though
  it doesn't have a parent interface.
  There are a couple of consequences of this in this situation:
  1) If a vrrp instance is configured with use_vmac and its configured interface
      is such a macvlan/macvtap interface, keepalived cannot ensure that the
      arp_ignore and arp_filter settings are correct on the parent
  2) keepalived cannot check that there a not duplicate VRIDs being used on the
      interface.
- Typo writing word error fix.
- Add vrrp instance priority change notifications on FIFOs only.
  Issue #1213 requested notification of vrrp instance priority changes,
  and this commit implements that with new FIFO messages:
  INSTANCE "VI_0" MASTER_PRIORITY 220
  INSTANCE "VI_0" BACKUP_PRIORITY 254
  This has been implemented via notify FIFOs only, since the order of
  processing of scripts is indeterminate if events happen quickly in
  succession, potentially causing the last processed priority by a
  script not to be the lastest priority, and using SMTP notification
  would be ridiculous.
- Allow user and group ownership of FIFOs to be configured.
- Remove extraneous debugging message from process_name commit
  Commit 4ad6d11 - "Add configuring process name" accidentally left
  a debugging log message in the code. This commit removes it.
- Fix FREE error if tracked process has no parameters.
- Fix track processes when reloading.
- Fix route add/delete on reload if only change via address
  If a virtual_iproute
  src 100.100.100.100 2.2.2.2/32 via 100.100.100.2 dev eth0
  is changed to
  src 100.100.100.100 2.2.2.2/32 via 100.100.100.1 dev eth0
  on a reload the route didn't get updated. The reason is that the
  via address wasn't used in the comparison of routes, so keepalived
  didn't detect that it had changed.
- Define TASK_COMM_LEN rather than use numbers in code.
- Fix promote_secondaries.
- Add snmpd.service to keepalived.service if SNMP enabled.
- Add issue templates for github.
- Make utils.c function parameters const where appropriate.
- Add missing info to check process dump file.
- Make ipvs_talk() error message more meaningful
  The error message used to just output the IPVS command number, now
  the name of the command is reported too.
- Make more use of LIST_FOREACH in ipwrapper.c.
- Change VS_ISEQ etc to be functions and correct them.
- Resolve removing virtual servers in virtual server groups after
  reloading.
- Update NOTE_vrrp_vmac.txt re sysctl settings.
- Ignore base interfaces of macvlans if in a different namespace.
- Don't lose sin_addr_l and sin6_addr_l lists from interface when recreate
  Issue #1232 identified that keepalived segfaulted when an interface was
  recreated. This commit resolves the problem of the address lists being
  lost.
- Fix commit 128bfe6 for pre v4.0 kernels
  Commit 128bfe6 - "Ignore base interfaces of macvlans if in a different
  namespace" added using IFLA_LINK_NETNSID to detect if the parent of an
  interface was in a different namespace. Unfortunately that was only
  introduced in Linux v4.0, so don't attempt to use it if it is not
  defined.
  For kernels older than v4.0 if a macvlan interface's parent is in
  another network namespace, but the ifindex of the parent interface also
  exists in the namespace in which keepalived is running, then keepalived
  will believe the parent of the macvlan is the wrong interface.
- Fix commit 3207f5c - IFLA_LINK_NETNSID is not #define'd
  This fixes commit 3207f5c - "Fix commit 128bfe6 for pre v4.0 kernels".
  A configure test is needed to check for IFLA_LINK_NETNSID.
- Further fixes/improvements for MACVLAN parents in different
  namespaces.
- allow to set zero weight for real server.
- Add comments re needing to enable protocol 112 in an AWS security
  group.
- Check if base i/f of a residual macvlan is in correct namespace.
- Stop segfault if using DBus and have invalid VRRP configuration.
  If a VRRP instance was removed by vrrp_complete_init() it was causing
  a segfault in the DBus code. The commit moves the initialisation of
  DBus until after the validity of the VRRP instances has been checked.
- Handle DBus process properly when reloading.
  DBus may change from being enabled to disabled or vice versa and
  the code didn't handle that.
- Close DBus pipes when stop using DBus.
- Add some more LIST_FOREACH to DBus code.
- Move a g_free() to after last use of the freed string in vrrp_dbus.
- Fix error in man page.
- Handle network namespace name properly when reloading.
- Don't call g_hash_table_remove() when using g_hash_table_foreach_remove()
  g_hash_table_foreach_remove() removes each object from the hash table,
  so calling g_hash_table_remove() as well made it not work properly.
- Resolve various aspects of reloading when also using DBus.
  1. Add ability for DBus to be enabled and disabled at reload
  2. Correctly handle vrrp_instance name change for matching interface/
     family/VRID.
  3. Correct handling of interface/family/VRID change for a vrrp_instance
     with the same name.
- Resolve segfault when a vrrp_instance has no interface specified.
- Fix sending priority 0 adverts after reload for deleted vrrp
  instances.
  During a reload, vrrp_dispatcher_release() was called prior to
  reloading the configuration, and it closed all the vrrp send/receive
  sockets. However it isn't until after the reload that it is known which
  vrrp instances no longer exist, and clear_diff_vrrp() attempted to send 0
  priority adverts for those instances. Since the sockets had already been
  closed, the adverts could not be sent. Worse, the socket_t structures had
  been released, but the released memory was accessed in attempting to send
  the adverts.
  This commit delays calling vrrp_dispatcher_release() until after the new
  configuration has been reloaded, and it sends 0 priority adverts before
  all the old sockets are closed. Following this new sockets are opened.
  It would be possible to make the code more efficient and retain the sockets
  that still need to be used, rather than closing them and opening new ones,
  but that is for another commit.
- Update some comments in vrrp_snmp.c.
- Use structure initialisation to clear struct, rather than memset.
- Fix logging if receive EPOLLHUP, EPOLLERR and add for EPOLLRDHUP.
- Add support for network timestamp debugging.
- Check return code from recvfrom() before other values for
  track_process.
- Use IPV6_RECVPKTINFO rather than IPV6_RECVHOPLIMIT when check
  multicast.
- Ensure virtual servers are properly removed when reloading.
  Pull request #1246 provided a patch to resolve the issue of virtual
  servers in a virtual server group that are deleted from the virtual
  server group on a reload weren't being removed from the IPVS
  configuration. However, the patch didn't quite work with the current
  HEAD of the master branch.
  This commit incorporates that patch provided and makes the necessary
  adjustments for it to work correctly.
- Cosmetic changes to IPVS code.
- Make clear the IPv6 instances use VRRP version 3.
- Delete redundant code.
- Update comments in vrrp_nftables.c.
- Update for gcc v9
  Detect if -Wchkp is no longer supported, and fix a -Wstrict-overflow
  warning in write_backtrace().
- Add additional compiler warnings available in gcc verion 9.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.15-0
- Fix uninitialised variable.
- Fix rpmbuild on CentOS7, and rely on auto-requires.
- Add option to flush lvs on shutdown.
  Currently all known virtual servers and their real servers are
  removed one at a time at shutdown. With large configurations on
  a busy system, this can take some time.
  Add an option just like the existing 'lvs_flush' which operates
  on shutdown. Typical environments with a single keepalived instance
  can take advantage of this option to achieve a faster shutdown or
  restart cycle.
- Make alpha mode checkers on new real servers start down on reload.
  Patch #1180 identified that new real servers with alpha mode checkers
  were being added online immediately, and if the checker then failed
  were being removed. This commit makes real servers that didn't exist
  before the reload start in down state if they have alpha mode checkers.
- Remove duplicate config dump entry.
- Make new real servers at reload start down if have alpha mode
  checkers.
- Close checker and smtp_alert sockets on reload.
  Issue #1177 identified that sockets were being left open (lost) after
  a reload. It transpired that these were sockets opened by TCP_CHECK,
  HTTP_GET, SSL_GET, DNS_CHECK and SMTP_CHECK checkers, and by smtp_alerts
  in the process of being sent.
  This commit adds an extra parameter to thread_add_read() and
  thread_add_write() to allow indicating that the scheduler should close
  the socket when destroying threads.
- Send vrrp group backup notifies at startup.
- Make inhibit_on_failure be inherited by real server from virtual
  server.
- Allow real and sorry servers to be configured with port 0
  This is to maintain backwards compatibility with keepalived prior
  to commit d87f07c - "Ensure always check return from inet_stosockaddr
  when parsing config".
  The proper way to configure this is to omit the port, which requires
  the next commit.
- Don't setup IPVS config with real and virtual servers ports
  different.
  If the real server is using DR or TUN, the port of the real server must
  be the same as the port of the virtual server. This commit uses the
  virtual server port for the real server when configuring IPVS.
- Log warnings if real server and virtual server ports don't match
  This commit adds logging warnings if virtual and real server ports,
  when using TUN or DR, don't match.
  It also sets the real server ports to be the same as the virtual server
  ports. Although listing the IPVS configuration with ipvsadm will look
  different, the kernel ignored the port of a real server when using DR
  or TUN, so the behaviour isn't changed, but when looking at the
  configuration it now shows what is actually happening.
- Fix warning when protocol specified for virtual server with fwmark.
- Add log message that nb_get_retry is deprecated.
- Fix whitespace in configure.ac.
- Fix configure error when systemd not installed
  configure was trying to execute
    pkg-config --variable=systemdsystemunitdir systemd
  even if systemd was not available.
  This commit makes configure only execute the above if it has determined
  that systemd is the correct init package to use.
- Correct references to RFC6527 (VRRPv3 SNMP RFC).
- nsure checker->has_run is always set once a checker has run.
- Fix some indentation in configure.ac.
- Update fopen_safe() to open temporary file in destination directory
  rename() in fopen_safe() was failing if the file being created
  was not on the same filesystem as /tmp.
- Add ${_RANDOM} configuration keyword.
  It might seem strange to introduce random elements to configuration
  files, but it can be useful for testing.
- Fix using ~SEQ() in multiline configuration definitions.
- Make blank lines terminate a multiline definition.
- Minor updates for lvs_flush_on_stop.
- Add option to skip deleting real servers on shutdown or reload
  If a virtual server is removed, the kernel will remove its real servers,
  so keepalived doesn't explicitly need to do so.
  The lvs_flush_onstop option removes all LVS configuration, whereas this
  new option will only remove the virtual servers managed by keepalived.
- Correct error message re checker_log_all_failures.
- Fix syntax error in configure.ac.
- Fix track_process initialisation for processes with PIDs starting 9.
- Remove debugging log message.
- Remove inappropriate function const attributes
  They were causing iptables/ipsets not to be initialised.
- Stop warning: function might be candidate for attribute â€˜constâ€™
  Depending on what configure options are selected, gcc can output
  the above warning for initialise_debug_options().
  This commit ensures that the warning is not produced.
- Enable strict-config-checks option in keepalived.spec RPM file.
- vrrp: relax attribute 'const' warning at iptables helpers.
- Propagate libm to KA_LIBS.
- Fix building on Alpine Linux.
  Alpine (musl) doesn't have a definition of __GNU_PREREQ, so create a
  dummy definition.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.14-0
- Add compiler warning -Wfloat-conversion and fix new warnings.
  It was discovered that passing 0.000001 as a parameter specified
  as uint32_t to a function did not generate any warning of type
  mismatch, or loss of precision.
  This commit adds -Wfloat-conversion and fixes 3 instances of new
  warnings that were generated.
- For non systemd enviroment, it occurs syntax error 'fi'.
  To avoid syntax error, modify keepalived.spec.in.
- When uninstall keepalived with init upstart, stop keepalived process.
- Fix type re LOG_INGO should be LOG_INFO * 6git stash --cached.
  The code was actualy in a #ifdef INCLUDE_UNUSED_CODE block, and
  so isn't currently compiled.
- Register missing thread function for thread debugging.
- Fix reutrn value of notify_script_compare misusing issue.
- Fix typo in keepalived.conf man page re BFD min_rx.
- Fix segfault when bfd process reloads config.
  Issue #1145 reported the bdf process was segfaulting when reloading.
  The bfd process was freeing and allocating a new thread_master_t
  when reloading, which doesn't work. This commit changes the bfd
  process to clean and reinitialise the thread_master_t.
- Fix segfault in handle_proc_ev().
  On Linux 3.10 the ack bit can be set in a connector message, and
  the CPU number is set to UINT32_MAX. This commit skips acks, and
  also checks that CPU number is within range of the number of CPUs
  on the system.
- Fix OpenSSL init failure with OpenSSL v1.1.1.
  OpenSSL v1.1.1, but not v1.1.0h or v1.1.1b failed in SSL_CTX_new()
  if OPENSSL_init_crypto(OPENSSL_INIT_NO_LOAD_CONFIG) had previously
  been called.
  This commit doesn't call OPENSSL_init_crypto() if doing so causes
  SSL_CTX_new() to fail.
- Remove all references to libnfnetlink.
  Commit 2899da6 (Stop using linbl for mcast group membership and
  setting rx buf sizes) stopped using libnfnetlink, but INSTALL and
  keepalived.spec.in were not updated accordingly.
- Fix genhash re OPENSSL_init_crypto bug and improve configure.ac.
  Commit fe6d6ac (Fix OpenSSL init failure with OpenSSL v1.1.1) didn't
  update the identical code in genhash/ssl.c. Also, an improvement for
  the test in configure.ac was suggested.
- Fix log output when real server removed.
  FMT_VS() and FMT_RS() both call inet_sockaddrtotrio which uses a
  static buffer to return the formatted string, but since FMT_VS(),
  wheich simply calls format_vs() copies the returned string to its
  own static buffer, if FMT_VS() was called before FMT_RS() then
  the returned strings from both could be used.
  The problem occurs when both FMT_VS() and FMT_RS() are used as
  parameters to log_message() (or printf etc). It appeared to work
  fine on x86_64, but was writing the same IP address for both the
  real server and virtual server on ARM architectures. This is due
  to the compiler evaluating parameters to the log_message() function
  call in a different order on the different architectures.
  This commit adds inet_sockaddrtotrio_r() which allows the output
  to be in a buffer specified by the caller, and so FMT_VS() and
  FMT_RS() can now be called in either order without one overwriting
  a buffer used by the other.
- Streamline some string formatting with FMT_RS() and FMR_VS().
  Following commit 9fe353d (Fix log output when real server removed)
  some code can be streamlined now that the order of calling FMT_VS()
  and FMT_RS() does not matter.
- Replace FMT_HTTP_RS(), FMT_TCP_RS() and FMT_DNS_RS() with FMT_CHK().
  They were all simply defined to be FMT_CHK() so just replace them
  with that. This made it much simpler to find all used of FMT_CHK().
- Fix building with gcc 4.4.7 (Centos 6.5).
  gcc v4.4.7 doesn't support -Wfloat-conversion, so check for it at
  configure time.
- Add dumping checker config/status when receive SIGUSR1.
- Don't put alpha mode checkers into failed state at reload
  If a new checker is added at a reload, unless the real server aleady
  has failed checkers, then ignore the alpha mode of the checker. This
  means that the real server, if up, won't be taken down and then brought
  back up again almost straight away. If the real server already has
  failed checkers, then setting an alpha mode checker down initially
  won't take down the real server, so we can allow the alpha mode setting
  to apply.
- Handle alpha mode checkers initial failure at startup better.
- Fix compile failure discovered by Travis-CI.
- Fix calling syslog when not using signalfd().
  Pull request #1149 identified that syslog is AS-Unsafe (see signal-safety
  man page), and that therefore signals should be blocked when calling it.
  This commit blocks signals when calling syslog()/vsyslog() when signalfd()
  is not being used.
- Rationalise function attributes.
- Fix enable-optimise configure option.
- Use AS_HELP_STRING for all options in configure.ac.
- Streamline genhash -h option.
- Make genhash -v version match keepalived.
- Fix config check of virtual server quorum against weights of real
  servers.
- Fix some configure tested checks for OPENSSL_init_crypto.
- Add infrastructure for adding additional compiler warnings.
- Add standard and extra compiler warnings.
- Add and resolve missing-declarations and missing-prototypes warnings
  Approximately 16 additional functions are now declared static.
- Add and resolve old-style-definitions warnings
- Add and resolve redundant-decls warnings
- Add and resolve jump-misses-init warnings
- Add and resolve shadow warnings
- Add and resolve unsuffixed-float-constants warnings
- Add and resolve suggest-attribute=const warnings
- Add and resolve suggest-attribute=format warnings
- Add and resolve suggest-attribute=malloc warnings
- Add and resolve suggest-attribute=noreturn warnings
- Add and resolve suggest-attribute=pure warnings
- Add and resolve unused-macros warnings
- Add and resolve null-dereference warnings
- Add and resolve float-equal warnings
- Add and resolve stack-protector warnings
- Add and resolve strict-overflow=4 warnings
- Add and resolve pointer-arith warnings
  This particularly includes adding a number of bytes to a void *.
- Add and resolve cast-qual warnings
- Resolve additional warnings identified on Centos 6.5/gcc 4.4.7
- Remove static from zalloc()
- Fix some compiler warnings on Ubuntu Xenial, and add comments re
  others.
- Rename LIST parameters to lst in list_head.h to avoid upper case.
- Fix real server checkers moving from failed to OK on reload.
- add rs judgement in migrate_checkers.
- Detect connection failure in genhash and exit rather than loop.
- Add another function pure attribute.
- Fix sending notifies for vrrp instances at startup when in sync group
  Issue #1155 idenfified that notify scripts for vrrp instance transition
  to backup state when keepalived started up were not being sent if
  the vrrp instance was in a sync group. It was also the case that SNMP
  traps, SMTP alerts and FIFO notifies were not being sent either.
  This commit make keepalived send the initial notifies when the vrrp
  instance is in a sync group.
- Fix building keepalived RPM on Fedora 26.
  For some reason -fPIC is needed when testing for the presence of
  setns().
- Add vrrp_startup_delay configuration option.
  Some systems that start keepalived at boot time need to delay the
  startup of the vrrp instances, due to network interfaces taking
  time to properly come up. This commit adds a global configuration
  option vrrp_startup_delay that delays the vrrp instances starting
  up, for the specified number of seconds.
- Handle checkers properly when reload immediately after startup.
- Streamline some of the SMTP checker code.
- Create separate checker for each host in SMTP_CHECK block
  Having multiple host entries in an SMTP_CHECK block is deprecated.
  This commit streamlines the SMTP_CHECK code by creating a separate
  SMTP checker for each host declared in the SMTP_CHECK block, so that
  apart from parsing the configuration, the code no longer handles
  multiple hosts per checker.
  The support for parsing configuration with multiple hosts is only
  enabled if WITH_HOST_ENTRIES is defined in check_smtp.c. It is
  currently enabled, but when support for multiple hosts in the
  SMTP_CHECK block is finally removed, it will simply be a matter of
  deleting all code in the WITH_HOST_ENTRIES conditional blocks.
- Make checker fail if ENETUNREACH returned by connect().
  The connect() call can return some immediate errors such as ENETUNREACH.
  These were not being treated as a failure of the checker, since the code
  used to assume that any non success return by connect() meant that the
  connection was in progress.
  keepalived will now treat ENETUNREACH, EHOSTUNREACH, ECONNREFUSED,
  EHOSTDOWN, ENETDOWN, ECONNRESET, ECONNABORTED, ETIMEDOUT, when returned
  by connect(), as meaning that the checker has failed.
- Don't set SO_LINGER with a timeout of 0
  SO_LINGER with a timeout of 0 causes a TCP connection to be reset
  rather than cleanly closed. Instead of specifying a timeout of 0,
  use 5 seconds, so that there is an orderly shutdown of the TCP
  connection, but the close socket doesn't remain in TIMED_WAIT state
  for more than a short time.
- nftables: fix build with kernel lower than 4.1.
- Remove dead code and cosmectics.
  Remove code marked as UNUSED where things simply go nowhere even if
  define is set. We keep for the moment UNUSED code related to debug
  helpers used during coding process.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.13-0
- Add BFD build option to keepalived.spec rpm file
  Issue #1114 identified that the keepalived.spec file was not being
  generated to build BFD support even if keepalived had been configured
  to support it.
- Copy tarball to rpmbuild/SOURCES when building in place
  It seems that even when building in place, rpmbuild expects the
  tarball to be in the rpmbuild/SOURCES directory.
- Fix configure check for __always_inline
- Handle interface MAC addresses changing
  When an interface is added to a bond interface, if it is the first
  interface added, the MAC address of the bond interface is changed
  to the MAC address of the added interface. When subsequent interfaces
  are added, their MAC addresses are changed to that of the bond
  interface.
  Issue #1112 identified that if a bond interface is deleted and
  recreated, the gratuitous ARPs were sent with the wrong source MAC
  address.
  This commit now updates interface MAC addresses from the netlink
  RTM_NEWLINK messages, so that the correct MAC address is always
  used.
- Minor tidying up of opening gratuitous ARP socket.
- Streamline setting SOCK_NONBLOCK on vrrp sockets.
- Use netlink reported hardware address length for unsolicited NAs
  ETH_ALEN is correct for Ethernet type interaces, but is not right
  for Infiniband interfaces.
- Minor tidying up of opening gratuitous NA socket.
- Make gratuitous ARP/NA sockets non blocking
  keepalived shouldn't block when sending gratutious ARP/NA messages.
  It is better to lose the messages than for keepalived to block, so
  set the sockets non blocking.
- Use netlink provided broadcast address for gratuitous ARP
  If an interface has a non-standard broadcast address, we should
  honour it.
- Fix building on pre 3.10 kernels re track_process
  Issue #1119 reported that keepalived wouldn't build on CentOS 6.
  Various PROC_EVENT_* declarations were assumed to exist, some of which
  were not introduced until Linux v3.10. Most of them are not needed, but
  PROC_EVENT_COMM is used by the track_process code.
  This commit now checks for the existence of the PROC_EVENT_* declarations,
  but since keepalived uses PROC_EVENT_COMM, track_process is not supported
  prior to Linux v3.2.
- Make track_process work prior to Linux 3.2, but with limitations
  Prior to Linux 3.2 the PROC_EVENT_COMM event did not exist, which
  means that keepalived is unable to detect changes to process name
  (/proc/PID/comm) prior to Linux 3.2. most processes do not change
  their process name, and so using track_process prior to Linux 3.2
  is safe so long as the monitored processes are known not to change
  their process name.
- Stop configure failing when nftables is not supported.
- Streamline socket use with linkbeat.
  Previously the socket used for ioctls was opened and closed twice per
  poll if using MII or ETHTOOL polling, and once per poll if using ioctl
  polling. This commit opens the socket once at startup, uses that socket
  for all linkbeat polls, and closes it on termination.
- Enable linkbeat polling to work with dynamic interfaces.
- Add linkbeat_interfaces configuration block
  It was not possible to indicate that an interface that wasn't used
  as the interface of a vrrp instance, but was used either as a track
  interface, or for virtual/static ip addresses or routes should use
  linkbeat. This commit adds that capability.
- Add ability to specify linkbeat type in linkbeat_interfaces block.
- Add --disable-linkbeat configure option
  Does anyone use linkbeat anymore? This commit enables keepalived to
  be build without the linkbeat code.
- Don't remove link local IPv6 address from VMAC that isn't keepalived's
  If IFLA_INET6_ADDR_GEN_MODE isn't supported and a macvlan interface
  already had a (non-default) link local addresss and the link local
  address that matched the interface's MAC address was added, keepalived
  was removing it as soon as it was added. This commit stop keepalived
  removing the address when we shouldn't.
- Set configure init type correctly in keepalived.spec file.
- Fix handling of VMACs with multiple reloads
  If a configuration is loaded that has a VRRP instance using a VMAC,
  then the configuration is updated to remove that VRRP instance and
  keepalived reloads its configuration, then the configuration is
  updated again to reinstate the VRRP instance and the configuration
  is again reloaded, keepalived thought the VMAC interface still
  existed, whereas it was deleted following the first reload.
  This commit ensures that keepalived properly detects whether an
  interface exists following a reload.
- Remember more than one interface local address per interface
  Keepalived needs a local address for each interface it sends adverts
  on. If the address keepalived is using is deleted and another address
  is configured on the interface, then keepalived should start using
  that address. To do this, a list of configured address on each
  interfaces needs to be maintained.
- Don't consider VIPs as local addresses when restart after crash
  Keepalived maintains a list of addresses per interface that can be
  used as source adddresses for adverts. To build the list, keepalived
  reads the addresses configured on interfaces when it starts. However,
  if keepalived crashed it will have left VIPs configured on interfaces,
  and we don't want to use them as advert source addresses.
  This commit makes keepalived compare the addresses on interfaces
  to VIPs, and ignores any addresses that are VIPs.
- Fix removing left over VIPs at startup.
- Use read_timer() when parsing config where appropriate.
- Allow fractional warmup, delay_loop and delay_before_retry for checkers
  To shorten the real server monitoring interval, make it possible to specify
  decimal value for following items:
  warmup
  delay_loop
  delay_before_retry
- Update connect_timeout configuration options
  Based on the patch submitted by tamu.0.0.tamu@gmail.com this patch
  allows setting the connect_timeout to a resolution of micro-seconds.
  The patch also adds the ability to set a default value at the virtual
  server and real server levels.
- Fix unused variable warning when building only with RFC compliant
  SNMP.
- It enable to set zero value as mintime for delay_loop and connect_timeout.
- Add option not to check for EINTR if using signalfd()
  If keepalived is using signalfd(), there are no asynchronous signal
  handlers, and therefore EINTR cannot be returned.
  Currently the check for EINTR is enabled by default, and configure
  option --disable-eintr-debug disables the check, while
  --enable-eintr-debug enables writing log entries if EINTR is returned.
  Once sufficient testing has been performed, the default will be
  changed not to test for EINTR if signalfd() is supported.
- Make checking for EAGAIN/EWOULDBLOCK consistent
  The code in some places checked errno for EAGAIN and EWOULDBLOCK
  and in other places only checked EAGAIN. On Linux EAGAIN == EWOULDBLOCK,
  so the check is not necessary, but EAGAIN is not guaranteed to be the
  same value as EWOULDBLOCK, so define check_EAGAIN that only checks EAGAIN
  if they are the same value, but checks both if they are different.
- Ensure default connection timeout for smtp checker hosts set.
- Set default connection timeout if no smtp check host specified.
- Fix min timer value, zero to 0.000001Sec.
- Add fixing min time for vs_co_timeout_handler() and rs_co_timeout_handler().
- Fix parameter of read_timer(), it treat Mintime and Maxtime as microseconds.
- vrrp: vrrp_dispatcher_read() performance extension
  We took time with Quentin to simulate and rework this code. We introduced
  2 imbricated while loop:
  (1) First one is catching recvfrom EINTR (this code trig
      only on kernel older than 2.6.22 where signalfd was firstly introduced).
      Newer kernel will immediately break the loop (hey guys: if you are running
      older than 2.6.22 it is worth considering upgrading).
  (2) Second loop will continue reading from socket until same VRID advert
      has been received during the same cycle. After simulating, it appears that
      during contention with a lot of VRRP instances (around 1500), this design
      is needed to relax socket recvq from growing. This can be viewed as a
      Poll-Mode activation during contention and fallback to regular I/O MUX
      during normal operations. This loop breaks immediately and re-submit
      opration to I/O MUX when there is no more to be read.
- Fix conversion from long for double in read_timer().
- Remove variable timer of unsigned long cast in read_timer().
  When Double type variable timer is cast to long type, it's scale falls.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.12-0
- Documentation related.
  Remove keepalived.conf.SYNOPSIS content to make a pointer to manpage.
  Update README manifest to reflect actual Keepalived goal and features.
- Improve error message if process events connector not enabled in
  kernel.
- Add option to disable track-process functionality
  Issue #1099 reported that their kernel did not support the proc events
  connector, and it would therefore be helpful to have an option to build
  keepalived without the track-process functionality.
  This commit adds the --disable-track-process configure option.
- Fix vrrp instances going to fault state when have virtual routes
  If an interface going down caused a vrrp instance to go to fault
  state, and the vrrp instance also had virtual routes, the state
  of the vrrp instance would be set to backup when the deletion of
  the virtual route was detected. This commit ensures that the vrrp
  instance stays in fault state until the interface is brought up
  again.
- Remove Red Hat Linux 9 and RH Enterprise Linux 3 from spec file.
  Red Hat Linux 9 and Red Hat Enterprise Linux 3 are both based on
  Linux 2.4, which is no longer supported by keepalived. The options
  in the spec file for Reh Hat Linux 9 have twice caused people to
  specify wrong options to configure when trying to build keepalived,
  so the options are removed to i) avoid confusion and ii) they are
  not longer relevant.
- Add global option vrrp_min_garp.
  By default keepalived sends 5 gratuitous ARP/NA messages after
  transitioning to master, and 5 more 5 seconds later. This isn't
  necessary with modern switches, and so if the vrrp_min_garp option
  is set, only one gratuitious ARP/NA message is sent after transition
  to master, and no repeat messages are sent 4 seconds later.
- Standardise definition of _INCLUDE_UNUSED_CODE_
- Remove out of date comment re VRRP over IPv6.
- Correct typo in keepalived.conf.5.
- Directly use structure sizes for packet header lengths.
- vrrp_state_fault_rx() is not used.
  Wrap the function in conditional compilation so it is not compiled
- Convert so list loops to use LIST_FOREACH.
- Don't recalculate vrrp packet header address.
  vrrp_get_header() calculates the address of the vrrp header in a
  received packet, but it was being recalculated in vrrp_in_chk().
  This commit passes the already calculated address to vrrp_in_chk().
- Ensure a received packet has an AH header if and only if AH auth.
  Ensure that a received packet has an AH header if we expect AH
  authentication, and doesn't have an AH header if we don't expect
  AH authentication.
- Ensure all protocol headers received before return pointer to vrrp header
  vrrp_get_header() returns a pointer to the vrrp header, but it now returns
  NULL if insufficient data has been received to include all the (IP,
  possibly AH, and VRRP) headers (this does not include the VIPs in the VRRP
  packet).
  This means that when a pointer to the VRRP header is returned, all fields in
  all protocol headers can safely be accessed.
- Add check of received IPv6 hop count in multicast adverts
  The VRRP RFC requires that IPv6 hop count MUST be checked to be 255,
  just as the TTL for IPv6 must be 255. Previously that wasn't being
  checked, since IPv6 raw sockets don't provide access to the IPv6
  header.
  Using recvmsg() rather than recvfrom(), and setting socket option
  IPV6_RECVHOPLIMIT allows keepalived to receive the hop count as
  ancillary data, and that can now be checked.
- Improve reading from vrrp receive sockets.
  Previously no check was made of the return value from recvfrom()/
  recvmsg(). This meant than an error could occur (e.g. EINTR), or no
  data might be returned, and keepalived would still attempt to process
  the receive buffer as though data had been received.
- Enhance and streamline checking of validity of received VRRP packet
  This includes checking that a packet is multicast, unless unicast is
  expected in which case it is checked for unicast, ensuring that if
  AH authentication is used, the next header protocol is VRRP.
  The sequence of some checks is revised to ensure that the fields being
  checked are valid to be accessed prior to accessing them, e.g. check
  that the packet is VRRP version 2 before checking the authentication.
- Stop clearing receive buffer before receiving VRRP packets.
  This is no longer necessary now that the appropriate checks are
  made of the return status of recvmsg(), and also that the checks
  of received packet length and packet headers now do all necessary
  checks.
- Add compile time checks for IPV6_RECVHOPLIMIT/IPV6_RECVPKTINFO
  support.
- Update keepalived.spec.in build-requires.
  The kernel package required for building keepalived is kernel-headers
  not kernel-devel. Also, it is superfluous to have package kernel in
  the build-requires!
- Add missing file (build.setup) to tarball.
- Fix calculating print format to rlim_t in configure.ac.
- Fix compiler warnings on 32 bit systems re HASH_UPDATE.
  Removing all the casts stopped the warnings.
- Use PRI_rlim_t when printing rlim_t types.
- Use %%zd/%%zu for ssize_t/size_t to avoid warnings on 32 bit systems.
- Fix some space/tab formatting.
- Stop declaring some timer definitions unsigned to stop compiler
  warnings.
  TIMER_HZ, TIMER_CENTI_HZ, NSEC_PER_SEC were causing some compiler warnings
  on some systems due to being defined with a 'U' unsigned suffix. Removing
  the unsigned specifier stopped the compiler warnings.
- Fix compiler warning due to incorrect format specifier.
  An int64_t should use %% PRIi64 and not %%ld
- Stop an uninitialized variable compiler warning.
- Fix MEM_CHECK debugging on processors without unaligned memory
  access.
- Don't attempt to use unopened socket for getting ipset version.
- Tidy up an error message.
- vrrp: make vrrp_dispatcher_read() async while catching error.
  During investigations we decided to update previous patch to resubmit
  into I/O MUX on read error. It will make read procedure I/O MUX freindly
  by removing potential sync operation potentially leading to a global
  I/O MUX desync. We aggreed, the situation is really and very exceptionnal
  but could happen.
- vrrp: vrrp_arp_thread split.
  Split the function for maintainability purpose.

* Sun Jan 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.11-0
- Fix segfault while shutting down when SNMP activity occurs.
  Issue #1061 identified that keepalived could segfault when it
  shut down. It appears that this was caused by data being received
  on the file descriptors that the snmp agent requests keepalived
  to monitor with epoll(). Since the read threads weren't being
  processed during a shutdown, the first time an snmp fd was ready,
  keepalived discarded the read thread. The second time that fd became
  ready there was no thread to handle the fd, and, since the assert()
  statement was not compiled in, non existant data was queued to the
  thread ready queue.
  This commit changes the assert() calls to continue, so that non existant
  data is no longer queued to the thread ready queue.
- While shutting down, continue to handle snmp agent fds.
  Since we don't shutdown the snmp connection until the very end of
  the shutdown process (we need to be able to send snmp traps), we
  should continue to handle the snmp fds on behalf of the snmp agent
  while shutting down.
- Ensure snmp agent is in correct state when initialising/closing
  Make sure the snmp agent is not already initialised before
  initialising it, and make sure it has been initialised before
  closing it.
- Disable asserts in bfd code by default and add --enable-asserts
  Asserts were enabled by default in the bfd code, which shouldn't be
  the case.
  Add --enable-asserts configure option so that the asserts tests can
  be enabled while debugging.
- Remove debugging log message accidently left in.
- Update receive buffers when interface is created.
  The receive buffer size used by keepalived is based on the largest
  MTU of any interface that keepalived uses. If dynamic interfaces
  are being used and an interface is created after keepalived has
  started, the MTU of the new interface may be larger than the
  previous largest, so the receive buffer may need to be increased
  in size.
  Further, if vrrp_rx_bufs_policy is MTU, then the kernel receive
  buffers on the receive socket may need to be increased.
- Handle MTU sizes being changed.
  Issue #1068 identified that the MTU size wasn't being updated in
  keepalived if it changed.
  This commit now updates the MTU size and adjusts receive buffer
  sizes accordingly.
- Fix syntax error in configure.ac.
- Fix double free when global data smtp_helo_name copied from local_name
  Issue #1071 identified a double free fault. It occurred when smtp_helo_name
  was not set, in which case it was set to point to the same malloc'd memory
  as local_name. At termination keepalived freed both local_name and
  smtp_helo_name.
  If keepalived needs to use local_name for smtp_helo_name it now malloc's
  additional memory to copy the string into.
- Rename TIMER_MAX to TIMER_MAXIMUM.
  ulibC defines TIMER_MAX, so to avoid naming conflict rename it.
  This issue was reported by Paul Gildea  who also
  provided the patch.
- Fix segfault when smtp alerts configured.
- First working version of nftables.
- Restructed code around how iptables/nftables are called
  This commit also allows building keepalived without iptables
  support, thereby allowing only nftables support.
  Adding any other mechanism to handle no_accept mode, i.e. blocking
  receiving and sending to/from VIPs should be added to vrrp_firewall.c,
  in a similar way to how nftables/iptables are used.
- Update doc files re nftables.
- Make nftables handle dont_track_primary appropriately.
- Fix config reload with nftables.
- Set base chain priorities from configuration.
- Use iptables by default if neither iptables or nftables configured.
  But if the build of keepalived does not include iptables, then use
  nftables default.
- Stop dumping keywords - left turned on after debugging.
- Make umask configuration apply to created file.
- Add libmnl and libnftnl to travis file.
- Fix compilation failure when NFTNL_EXPR_LOOKUP_FLAGS not defined.
- Fix compilation failure when build with nftables but without iptables.
- Fix order of include files in configure COLLISION test.
  Since Linux 4.4.11 (commit 1575c09) including linux/if.h after
  net/if.h works, whereas until glibc fix their headers including
  net/if.h after linux/if.h causes compiler redefinition errors.
  Unfortunately the test for the collision was done the wrong way
  round, as identified in issue #1079. The patch included in the
  issue report corrects the order of inclusion of the header files.
  What we should do is ensure that glibc header files are included
  before Linux header files, so that at least if kernel headers from
  4.4.11 onwards are used, the conflict will not occur.
- Set CLOEXEC on netlink sockets.
- Correct error message for invalid route metric.
- Add track_process for vrrp to monitor if another process is running.
  Configurations frequently include a track_script to check that a process
  is running, often haproxy or nginx. Using any of pgrep, pkill, killall,
  pidof, etc, has an overhead of reading all /proc/[1-9]*/status and/or
  /proc/[1-9]*/cmdline files. In particular reading the cmdline files
  has a significant overhead on a system that is swapping, since the
  cmdline files provide access to part of the address space of each
  process, which may need to be fetched from the swap space.
  This commit reads the /proc/[1-9]*/stat and/or the /proc/[1-9]*/cmdline
  files only when keepalived starts, and after that uses the process events
  connector to track process creation and termination.
  keepalived will ignore zombie processes, whereas pgrep etc include them.
  A minimum number of instances of a process can be specified, and also a
  delay so that if a process is restarted, it won't cause monitoring vrrp
  instances to immediately transition to fault state but to wait the
  configured time and it the monitored process starts again it
  won't transition to fault state.
  There are potential difficulties with the process event connector if a
  large number of process events occur very rapidly, since there can be
  a receive buffer overrun on the netlink socket. This code will detect
  that happening, increase the receive buffer size, and reread the processes
  from /proc.
- Add missing #include to track_process.c.
- Fix number of elements of fd_set read for snmp select info.
- Remove thread_event_t when EPOLL_CTL_DEL fails.
  If snmpd closes a file descriptor, when keepalived attempts to
  unregister the fd from epoll an error is returned. However, we still
  need to remove the thread_event_t from the io_events rbtree.
- Fix connection to snmpd after it has to reconnect.
  Issue #1080 identified that keepalived wasn't handling a connection
  failure and reconnect to snmpd properly. The problem was created when
  the change from select() to epoll() was made.
  This commit makes keepalived unregister and reregister the snmp file
  descriptors after snmpd reconnects.
- Fix retry count for SMTP_CHECK checker.
  The checker was doing one too few retries.
- Make healthchecker failure reporting consistent
  Some healthcheckers were reporting all failures, and others only when
  the retries expired. This commit by default makes the checkers only
  report failure when the retries expire, unless the global keyword
  checker_log_all_failures or log_all_failures on the specific checker
  is configured.
- After reload, reinitialise current track processes state.
- Remove unused variable in track_process.c.
- Add configure checks re --with-kernel-dir.
- Convert remaining select() to epoll_wait().
  keepalived was using select() for handling the termination of child
  processes, but the main scheduling loop now uses epoll_wait(), so
  convert the select() to epoll_wait() from consistency.
- Stop keepalived leaving zombie child processes.
  keepalived wasn't reaping the termination of its child processes,
  so this commit adds waitpid() calls once it knows the processes
  have terminated.
- Fix make distclean and make distcheck.
- Also skip route not configured with down interface.
  Otherwise, if keepalived has virtual_routes configured, we create
  a virtual interface and bring it up and down, current code will bring
  VRRP state to FAULT and never return.
- Stop vrrp process entering infinite loop when track script times out
  Issue #1093 identified that the vrrp process was entering an infinite
  loop after a track script timed out. This was due to a child process
  thread having an RB tree for PIDs as well as for the timeout, and if
  a child process timed out, the thread wasn't being removed from the
  PID RB tree. This commit now ensures it is removed.
- Fix the abbreviation of Shortest Expected Delay.
- Don't free unallocated memory if not tracking processes.
- vrrp: Rewrote JSON code
  Remove dependency to json-c extralib by using a simple streaming JSON writter.
  Refactored code to make it simple to maintain.
- vrrp: Fix JSON handling for v{route;rule}.
- autoconf: fix nftables selection
  We need to inhibit nftable compilation if compiling system has
  kernel header file nf_tables.h but not libnftnl nor libmnl.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.10-0
- Fix compiling on Alpine Linux.
- Stop printf compiler warning on Alpine Linux due to rlim_t.
- manpage cosmetic.
- Fix removing snmpd read threads when snmpd becomes unavailable.
- Update to support libipset version 7.
- Use ipset_printf for ipset messages so can go to log.
- When opening files for write, ensure files can only be read by root.
  Issue #1048 referred to CVE-2018-19046 regarding files used for
  debugging purposes could potentially be read by non root users.
  This commit ensures that such log files cannot be opened by non root
  users.
- Disable fopen_safe() append mode by default
  If a non privileged user creates /tmp/keepalived.log and has it open
  for read (e.g. tail -f), then even though keepalived will change the
  owner to root and remove all read/write permissions from non owners,
  the application which already has the file open will be able to read
  the added log entries.
  Accordingly, opening a file in append mode is disabled by default, and
  only enabled if --enable-smtp-alert-debug or --enable-log-file (which
  are debugging options and unset by default) are enabled.
  This should further alleviate security concerns related to CVE-2018-19046.
- vrrp: add support to constant time memcmp.
  Just an update to use best practise security design pattern. While
  comparing password or hmac you need to ensure comparison function
  is time constant in order to figth against any timing attacks. We
  turn off potential compiler optimizations for this particular
  function to avoid any short circuit.
- Make sure a non privileged user cannot read keepalived file output
  Ensure that when a file such as /tmp/keepalived.data is wriiten,
  no non privileged can have a previous version of that file already
  open, thereby allowing them to read the data.
  This should fully resolve CVE-2018-19046.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.9-0
- Fix updating a timer thread's timeout.
  Issue #1042 identified that the BFD process could segfault. This
  was tracked down to a timer thread which had already expired having
  its timeout updated by timer_thread_update_timeout().
  The sands timer should only be updated if the thread is on a waiting
  queue, and not if it has already timed out or it is unused.
- Don't requeue read thread if it is not waiting.
  This update matches commit 09a2a37 - Fix updating a timer thread's
  timeout should.
- Allow BFD instance to recover after send error.
  If sendto failed in bfd_send_packet(), the bfd instance was put into
  admin down state, but there was no means for the bfd instance to
  transition out of admin down state.
  This commit makes keepalived log the first instance of a sequence of
  failures to send a bfd packet, but does not bring the bfd instance down
  in case the error is a transient error. If the error is longer lasting,
  the remote system will timeout, transition to down state, and send a message
  saying it is down.
  Once the bfd instance can start sending again the bfd instance can now
  transition again to up state.
- Make DGB definition use log_message() rather than syslog().
- Fix building with --enable-debug configure option.
- Start list of required kernel features in INSTALL file.
  Issue #1024 asked what kernel features are needed to support keepalived.
  The simple answer was that it isn't recorded anywhere, so this is a
  start of making a list of the features required.
- Make list_remove() call list free function and add list_transfer().
  If an element is being removed from a list, the free function should
  be called.
  list_transfer() allows a list element to be moved from one list to
  another without freeing and reallocating the list element control
  information.
- Add mem_check diagnostics re calling functions of list functions.
  When using mem_check, mallocs and frees were recorded against the
  list functions, and the originating functions weren't identified.
  This patch adds recording of the functions calling the list
  functions so that the originating function is identified.
- Simplify the processing of comments in configuration files.
  This commit moves the handling (and removal) of comments to a
  single function (called from read_line()) which simplifies the
  processing of config files.
- Add ~SEQ(start, step, end) config functionality
  Where a configuration has repeated blocks of configuration where
  the only thing that changes is a numeric value (e.g. for VRIDs
  from 1 to 255) this allows the block to be defined once, and a
  single line using ~SEQ can then generate all the blocks.
- Use REALLOC when building a multiline definition.
  The code used to use MALLOC, strcpy() and FREE, but REALLOC can do
  all this for us.
- Improve mem-check diagnostics.
  When using an allocation list of over 50,000 entries, it was quite slow
  searching thtough all the entries to find the matching memory allocation,
  and to find free entries. This commit changes to using malloc() to create
  entries, and a red-black tree to hold the entries. It also has a separate
  list of free entries.
  This commit also adds 4 more types of memory allocation error, and
  improves the consistency of the entries in the log files.
- Don't attempt to delete VMAC when underlying interface is deleted.
  If the underlying interface of one of our vmacs is deleted, and we
  know the vmac has been deleted, don't attempt to delete it again.
- Include master state in determining if vmacs are up or down
  Netlink doesn't send messages for a state change of a macvlan when
  the master device changes state, so we have to track that for
  ourselves.
- Turn off parser debugging.
- Make test/mk_if create iptables chains.
- Handle interfaces not existing when keepalived terminates.
  If the underlying interface of a vmac we created has been deleted,
  the vmac will not exist so don't attempt to delete it again. Also,
  don't attempt to reset the configuration of the underlying interface.
- Handle the underlying interface of a macvlan interface going up/down.
  The kernel doesn't send netlink messages for macvlans going up or
  down when the underlying interface transitions (it doesn't even
  update their status to say they are up/down), but the interfaces
  don't work. We need to track the state of the underlying interfaces
  and propagate that to the macvlan interfaces.
- Fix duplicate value in track_t enum.
- Fix check for matching track types.
- Treat macvtap interfaces in the same way as macvlan interfaces.
- Improve handling of interfaces not existing when keepalived starts.
- Fix handling interface deletion and creation of vmacs on macvlan i/fs.
- When interface created, open sockets on it if used by VRRP directly
  If an interface is created that has vrrp instances configured on it
  that don't use VMACs, or use vmac_xmit_base, then the raw sockets
  must be opened.
- Force seeing a transition to up state when an interface is created.
- Fix netlink remnant data error.
- Add command line and configuration option to set umask.
  Issue #1048 identified that files created by keepalived are created
  with mode 0666. This commit changes the default to 0644, and also
  allows the umask to be specified in the configuration or as a command
  line option.
- Fix compile warning introduced in commit c6247a9.
  Commit c6247a9 - "Add command line and configuration option to set umask"
  introduced a compile warning, although the code would have worked OK.
- When opening files for write, ensure they aren't symbolic links.
  Issue #1048 identified that if, for example, a non privileged user
  created a symbolic link from /etc/keepalvied.data to /etc/passwd,
  writing to /etc/keepalived.data (which could be invoked via DBus)
  would cause /etc/passwd to be overwritten.
  This commit stops keepalived writing to pathnames where the ultimate
  component is a symbolic link, by setting O_NOFOLLOW whenever opening
  a file for writing.
  This might break some setups, where, for example, /etc/keepalived.data
  was a symbolic link to /home/fred/keepalived.data. If this was the case,
  instead create a symbolic link from /home/fred/keepalived.data to
  /tmp/keepalived.data, so that the file is still accessible via
  /home/fred/keepalived.data.
  There doesn't appear to be a way around this backward incompatibility,
  since even checking if the pathname is a symbolic link prior to opening
  for writing would create a race condition.
- Make netlink error messages more meaningful.
- Fix compiling without support for macvlans.
- fix uninitialized structure.
  The linkinfo and linkattr structures were not initialized,
  so we should not expect that unexistant attributes are set
  to NULL. Add the missing memset().
- fix socket allocation with dynamic interfaces.
  When there are several vrrp instance binding different interfaces that
  don't exist at startup, their ifindex is set to 0 in the sock. The
  function already_exist_sock() that lookup for an existing socket will
  always return the first sock because the ifindex is the same.
  Later, when an interface appears, the fd will be created for one
  instance, and all instances will wrongly use this fd to send the
  advertisments.
  Fix this by using the interface structure pointer instead of the
  ifindex as the key for sock lookup.
  The problem was identified by Olivier Matz
  who also provided a patch fixing the problem. This patch is a slight
  rework of Olivier's patch, better using the existing data structures
  that keepalived already holds.
- When creating a macvlan interface, use AF_UNSPEC rather than AF_INET.
- Stop using libnl for configuring interfaces.
  Since there is code to configure the interfaces using netlink without
  using libnl, there is no point in having code to do it using libnl.
- Fix building on Centos 6.5.
- Stop including some files not needed after libnl removal for i/fs.
- Fix some compilation issues when building without vrrp support.
- Stop using linbl for mcast group membership and setting rx buf sizes.
  Since there is code to handle multicast group membership and
  setting kernel netlink receive buffer sizes without using libnl,
  there is no point in having code to do it using libnl.
  This now means that the vrrp functionality no longer uses libnl.
- Add some sanity checking of configure options.
  Certain invalid combinations of configure options could cause compile
  errors, e.g. --disable-vrrp --enable-vrrp-fd-debug. This commit ensures
  that invalid combinations aren't allowed, in order to stop the compile
  errors.
- Fix invalid configuration combination caught by previous commit.
- Use netlink to set/clear rp_filter on interfaces.
- Fix configure for building without vrrp.
- Actually update the .travis.yml file to fix the problem.
- Fix conditional compilation re epoll-thread-dump debugging.
- Update INSTALL file now no longer use libnl-route-3.
- Stop cast to incompatible function type warnings from gcc 8.1.
- Update snapcraft.yaml not to include libnl-route-3.
- keepalived exit with non-zero exit code if config file not readable.
- Allow specifying default config file at configure time.
- Use keepalived define for exit code when malloc failure.
- Fix configuring fixed interface type.
- Add configuring keepalived default configuration file.
- Fix return value in get_time_rtt() error path.
- Update generation of git-commit.h.
- snapcraft.yaml: Enable all sensible build options. Preserve build time
  version in the snap version. Expose genhash.
- snapcraft.yaml: Build keepalived with Linux 3.13 headers.
- snap: Add an install hook to make sure a keepalived configuration exists.
- snap: Move the hooks to the correct location.
- snap: Make sure /etc/keepalived exists.
- Fix building with IP_MULTICAST_ALL in linux/in.h but not netinet/in.h
  Issue #1054 identified that configure was checking the definition of
  IP_MULTICAST_ALL in linux/in.h but including netinet/in.h, which also
  has the definition, but only from glibc 2.17.
  This commit creates a local definition (in lib/config.h) of IP_MULTICAST_ALL
  if it is defined in linux/in.h but not in netinet/in.h. The reason for
  this is that compiles using linux/in.h fail due to conflicting definitions.
- Fix creating iptables tables in mk_if.
- Update .travis.yml to use xenial.
- Update .travis.yml to add --enable-regex option.
- Tidy up .travis.yml file.
- snap: Build multiple keepalived binaries.
- Updated snapcraft builds to support multiple kernel versions.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.8-0
- Improve identifing interface as macvlan when reading interface details
- Enslave a VMAC to the VRF master of the underlying interface.
- Use addattr32 rather than addattr_l for if_index.
- Only include VRF support if kernel headers support it.
- Fix --enable-timer-debug configure option.
- Fix some configure.ac enable option tests.
- Include stdbool.h in process.c.
- Fix diagnostic message re ignoring weight of tracked interface.
- Fix track_bfds with weights.
- Correct conditional compilation definition name.
- Fix memory leak in HTTP_GET/SSL_GET.
- Fix two memory leaks in DNS_CHECK.
- Don't consider retries for BFD_CHECK. The BFD_CHECKer doesn't support
  retries, and the check was causing the checker not to transition to
  down state.
- Fix memory leak with BFD_CHECK.
- Restart global notify FIFO handler after reload.
- modify @WITH_REGEX@ to @WITH_REGEX_TRUE@
- Fix compiling without BFD support.
- Stop bfd process sending double the number of packets.
  If a bfd process received an initial bfd packet, it scheduled a
  second bfd_sender_thread thereby causing two packets to be sent
  in every interval.
- Use timerfd for select timeouts rather than select timeout parameter
  This is a precursor to moving to using epoll.
- Use epoll rather than select.
  epoll is both more efficient than select and also doesn't have a
  file descriptor limit of 1024, which limited the number of vrrp
  instances that could be managed.
  This commit also introduces read-black trees and the list_head
  list type.
- Add --enable-timer-check option for logging calls for getting time
  Calls to update the current time from the kernel are made too
  frequently, and this patch logs when the calls are made, and how
  long since the previous call, so unnecessary calls can be removed.
- Add debug option for monitoring epoll queues.
  This is enabled by --enable-epoll-debug and replaces
  --enable-timer-debug.
- Use system monotonic clock to generate a monotonic clock.
  Rather than have our own code for creating a monotonic clock, use
  the kernel's monotonic clock.
- Make some functions in timer.c inline.
  The functions had one line of code so inlining them is more
  efficient.
- Fix requeueing read and write threads after read/write timeouts.
- Fix initial allocating and final freeing of thread_master epoll_events.
- When cleaning up threads, also clean up their thread_events.
- Add thread_close_fd() function to release thread_event_t on close
  When a file descriptor that has been monitored by epoll is closed
  the thread_event_t structure used for managing epoll for that fd
  has to be release. Therefore calls to close() and replace by calls
  to thread_close_fd().
- Make parent process write log entry when it is reloading.
- Move checking for thread timeouts to timerfd_handler
  There is no point in checking for thread timeouts if the timerfd
  isn't readable; in other words only check for thread timeouts if
  the timer has expired.
- Make bfd reschuling timer threads more efficient.
- Streamline DNS_CHECK code.
- Fix buffer overrun with track file path names.
- Add timestamp when writing mem_check entries to file.
- Ensure thread_event_t released for ready threads at termination.
- Increase open file limit if large number of VRRP instances.
  Each VRRP instance can use up to 2 file descriptors, and so if there
  are more than 500 ish VRRP instances the number of open files
  can exceed the default per process limit (1024 on my system).
  The commit allows 2 file descriptors per vrrp instance plus a few more,
  and if the RLIMIT_NOFILE value returned by getrlimit isn't high enough,
  keepalived will increase the limit.
- Ensure that child processes run with standard priorities/limits.
  When child processes such as notify scripts, track_scripts and
  MISC_CHECK scripts are run, they should not inherit any elevated
  priorities, system limits etc from the parent keepalived process.
- Change multiple spaces to tabs in scheduler.h.
- Add family to sockpool listing.
- Fix a multiline definition expansion issue.
- Free allocated cache when closing/freeing netlink socket.
  When running on a system with 500+ interfaces configured and adding
  1000 VMAC interfaces, the heap was growing by 340Mb due the netlink
  cahce not being freed after creating each VMAC interface. With this
  patch the heap only grow by 3.7Mb (if creating 1000 VMAC interfaces
  the heap grep by 905Mb now reduced to 6.1Mb).
- Stop using netlink cache when adding and configuring VMAC interfaces.
  When running on a system with 500+ interfaces configured and adding
  1000 VMAC interfaces, it was taking 2.3 seconds to add the interfaces.
  Without populating a netlink cache each time a VMAC interface is created
  it now takes 0.38 seconds to add the interfaces (if creating 1000 VMAC
  interfaces it was taking 6.1 seconds, now reduced to 0.89 seconds, and
  the heap growth is reduced from 6.1Mb to 3.9Mb).
- Add function rtnk_link_get_kernel for dynamic linking.
- Fix compiling without JSON support.
- Add support for recording perf profiling data for vrrp process.
- Add comment re usage of MAX_ALLOC_LIST.
- Some streamlining of scheduler.c.
- Merge --enable-epoll-debug and --enable-dump-threads functionality.
- Let thread_add_unuse() set thread type, and use thread_add_unuse() more.
- Use break rather than return in process_threads().
- Fix segfault when reloading with HTTP_GET and no regex configured.
- Merge the next-generation scheduler.
- Make all debug options need enabling at runtime.
  Previously if configure enabled a debug option its output was always
  recorded, which meant that if one didn't want the output, configure/
  compile was needed. This commit adds command line options that need to
  be set in order to turn the debugging on.
- Remove unwanted debug message.
- Fix parsing --debug options.
- Fix rb tree insertion with timers.
- Add missing functions for thread debugging.
- Add vrrp instance VMAC flags when dumping configuration.
- Ensure parent thread terminates if child has permanant config error.
- Ensure don't delete VMAC interface if keepalived didn't create it.
  and sundry fixes.
- If receive lower priority advert, send GARP messages for sync group.
  A recent update to issue #542 identified that following recovery
  from a split brain situation, GARP messages weren't being sent. It
  transpired that, if a member of a sync group in master state received
  a lower priority advert and vrrp_higher_prio_send_advert is set, a
  further (lower priority) advert is sent, and the instance and all the
  members of the sync group transition to backup (the other members of
  the sync group don't send a further advert since they haven't received
  a higher priority advert). This meant that the other members of the
  sync group on the keepalived instance that remained master didn't
  receive a lower priority advert, and so didn't send further GARP
  messages.
  This commit changes keepalived's behaviour, so that if a vrrp instance
  is sending GARP messages due to receiving a lower priority advert
  and it is a member of a sync group, keepalived will also send GARP
  messages for any other member of the sync group that have
  garp_lower_prio_rep set.
- Allow 0.0.0.0 and default/default6 for rule/route to/from addresses.
- Check return value of SSL_CTX_new().
- Check return values of SSL_new() and BIO_new_socket().
- Only allow subnet masks with routes or virtual IP addresses.
  For example, if specifying a via address or preferred source address
  for a route, it isn't valid to specify a subnet mask.
- Add inet/inet6 to specify ip route/rule family if ambiguous.
- Remove superfluous parameter from parse_route().
- Add "any" and "all" as synonyms for "default".
- Fix memory leak if route destination address is wrong address family.
- Add ttl-propagate route option.
- Fix checking return status of kill().
- Fix building with --enable-debug configure option.
- Stop delay in reload when using network namespaces.
  If running in a network namespace, getaddrinfo() could take over
  30 seconds before timing out while trying to contact a name
  server. To alleviate this, the hostname is remembered from when
  keepalived started.
- Fix spelling of propagate in propagate_signal().
- Fix effective_priority after reload if tracked interface down.
- Cosmetic grammatical changes.
- Add debug option for dumping vrrp fd lists.
- Fix calculation for vrrp fd timers.
  Starting or reloading keepalived when an interface that was tracked
  interface was failed was stopping other vrrp instances that were on
  the same interface but not using VMACs coming up.
- Move code for initialising tracking priorities to vrrp_track.c.
- Don't overwrite track file on reload.
- Don't attempt to write track file if path not specified.
- Fix compiling when not using --enable-vrrp-fd-debug.
- Fix compiling with configure --enable-vrrp-fd-debug.
- Add sync group track_bfds and track file status to config dump.
- Move initialisation of track_files.
- Don't alter effective_priority if track_file take vrrp instance down.
- Don't log vrrp instance in fault state at reload if already fault.
- Fix calculating fd timer if all vrrp sands are set to TIMER_DISABLED.
- Don't make all sync groups transition to backup on reload
  If a sync group was in master state, and can still be after a reload
  then allow it to stay in master state.
- Don't have track_bfd list in vrrp_sgroup_t in BFD not enabled.
- Fix memory leak re vrrp_sgroup_t track lists.
- Tidy up some freeing of MALLOC'd memory.
  Use FREE_PTR if it is not known if the pointer is valid, and don't
  clear the pointer afterr FREE/FREE_PTR since FREE does it anyway.
- Add memory.c list size definition and move definition from memory.h.
- Increase size of checksum value for MEM_CHECK.
- Don't store checksum of memory allocation block. It can be calculated
  from the size, so do so.
- Make the checksum for memory allocation blocks unsigned.
- Use an enum for memory allocation block types.
- Update comment re debug bit for memory detect error.
- In memory alloc debug code report free or realloc for not alloc'd.
- Allow for PIDs up to 2^22 (7 decimal digits).
- Add function for dumping memory allocation while running.
- Fix max memory allocation size calculations.
- Fix reporting original and new file/line/func for realloc.
- Check matching block for realloc is allocated.
  The same memory block may have been previously allocated and freed,
  so we need to make sure that the block we find is currently marked
  as allocated.
- Use a new MEMCHECK struct for realloc overrun detected
  It was marking the allocated block as an overrun block, whereas it
  needs to be an allocated block, so use a new block to mark the
  overrun.
- Tidy up working of a couple of memory allocation messages.
- Use for loops rather than while blocks in memory allocation code.
- Report number of mallocs and reallocs with MEMCHECK.
- Attempt to log first free after double free in MEMCHECK.
- Streamline use of buf/buffer in memory.c.
- Always use first free entry in alloc_list for MEMCHECK.
- Define MEMCHECK alloc_list size via configure.
- Align keepalived_free() and keepalived_realloc().
- Make char * const where possible for MEMCHECK.
- Merge MEMCHECK keepalived_free() and keepalived_realloc().
  Most of the code was common between the two (or should have been),
  so it makes sense for them to use common code.
- Ensure only relevant thread types run during shutdown.
- Fix building without --enable-mem-check.
- Use rbtree search for finding child thread on child termination.
  It was doing a linear search of the rbtree in timeout order. This
  commit adds another rbtree for child processes (vrrp track scripts
  and check_misc scripts), sorted by PID, to make the search by PID
  more efficient.
- Make rbtree compare function thread_timer_cmp() more efficient.
- Remove child_remover functionality - it was superfluous.
- Fix checking that there are no duplicate vrrp instances configured
  The tuple {interface, family, vrid} must be unique. The check for
  this was being made completely incorrectly.
- Delay creating vrrp notify FIFO.
- Remove struct sockaddr_storage saddr from sock_t.
- Use an rbtree for finding vrrp instance for received advert.
  Previously the code search a list of pointers to vrrp instances and
  looked for a matching fd and vrid. In order to optimise this, it was
  implemented using an mlist whose index was a hash of the fd and vrid.
  This commit changes the approach and uses an rbtree for each sock_t.
  Since the sock_t that the advert was received on is known, the rbtree
  search is only searching for a match on the vrid.
  Not only is this more efficient, but it is simpler, uses standard code,
  and reduces the code by over 60 lines.
- Use an rbtree for finding vrrp instance for socket timeout.
  Previously the code search a list of pointers to vrrp instances and
  looked for matching file descriptor and sands < time_now. In order to
  optimise this, it was implemented using an mlist whose index was a hash
  of the fd.
  This commit changes the approach and uses a second rbtree for each sock_t.
  Since the sock_t that the timeout occurred on is known, the rbtree
  search is only searching for a match of the sands.
  Not only is this more efficient, but it is simpler, uses standard code,
  and reduces the code by over 220 lines.
- Remove superfluous checks of rbtree node != NULL in rb_move().
- Remove superfluous check of node != NULL in rb_next().
- Update rbtree code to Linux 4.18.10.
- Fix debug logging of sands timers before time_now.
- Update rb_for_each_entry etc and rb_move to use rb_entry_safe.
  With the added definition of rb_entry_safe in the rbtree code
  updated to Linux 4.18.10, the refinition of rb_entry was reverted
  to the kernel definition. That meant that rb_for_each_entry,
  rb_for_eacn_entry_safe and rb_move neded to be updated to use
  rb_entry_safe rather than rb_entry.
- Add support functions for rbtree rb_root_cached.
  This is in preparation for the use of rb_root_cached in the next
  patch.
- Use cached rbtrees where the key is a timeval_t sands
  When the key of an rbtree is a timeval_t sands keepalived will frequently
  need to access the first node of the tree in order to calculate the next
  timeout. This applies to the read, write, child and timer threads queues,
  and also the vrrp queues on a sock_t.
  The use of cached rbtrees for these is ideal since it gives direct access
  to the first node of the queue.
- Add thread_add_read_sands to avoid introducing timer errors.
  When using thread_add_read and the timeout was held as timeval_t,
  it was converted to and offset from time_now, and then converted
  back to a timeval_t, but time_now was updated, resulting in a
  slightly different value being used as the timeout. Using
  thread_add_read_sands() avoids the double conversion and results in the
  timeout being more accurate.
- Replace NETLINK_TIMER with TIMER_NEVER.
  It makes the code easier to read, and since NETLINK_TIMER was defined
  to be TIMER_NEVER it doesn't change the functionality.
- Handle preempt delays not expiring at same time on sync group
  If different vrrp instances in a sync group had preempt delays
  that expired at different times keepalived looped with very small
  to epoll_wait() until all preempt delays had expired, causing high
  CPU utilisation.
  Keepalived now reschedules vrrp instances with a delay of
  3 * advert_int + skew time while waiting for all vrrp instances in
  the sync group to expire their preempt delays.
- Fix segfault when receive netlink message for default route added.
- Move vrf_master_index into conditional compilation block.
- Store interface macvlan type.
- Make vrp_master_ifp point to self for VRF master interfaces.
- Log if cannot create a VMAC due to existing interface with same name.
- Handle delete/create of macvlan i/fs which aren't keepalived's.
- Tidying up keepalived_netlink.c.
- Handle VRFs changing on macvlan i/fs which have VMACs configured on them.
- Fix recreating our VMACs if they are deleted.
- Fix detecting address add/deletion from underlying i/f of our vmacs.
- Don't use configured_ifp or base_ifp if not _HAVE_VRRP_VMAC_.
- Distinguish between VMAC on real i/f and no VMAC on macvlan i/f
  If keepalived is configured to have a non VMAC interface on a macvlan
  interface, we want to use the macvlan interface rather than the
  underlying interface, whereas if we have a VMAC interface on a macvlan
  interface, we create the VMAC on the underlying interface of the macvlan.
- Update duplicate VRID check where vrrp instance configured on macvlan.
  If a VRRP instance is configured on a macvlan interface, the duplicate
  VRID check needs to be done on the underlying interface.
- Check for VRID conflicts when changeable interfaces are added
  For example, a vrrp instance could be configured on a macvlan, and
  that macvlan could be deleted and recreated with another base interface.
  The VRIDs in this case need to be checked for duplicates against the
  base interface, and so the VRID check needs to be done dynamically.
  In order to allow VRID conflicts to produce config errors at startup,
  by default keepalived assumes that there won't be interface movements
  as described above, and will only handle it if the global_defs option
  'dynamic_interfaces' is used along with the option 'allow_if_changes'.
- Remove some comments inserted for tracking changes to code.
- Fix building with --enable-debug configure option.
- Check that '{'s and '}'s are balanced in the configuration file.
- Allow more flexibility re placing of { and }.
- Improve reporting additional '}'s in configuration.
- Minor improvements re thread handling and cancellation.
- Remove unused THREAD_IF_UP and THREAD_IF_DOWN.
- Replace getpagesize() with sysconf(_SC_PAGESIZE).
- Increase netlink receive buffer for dumps to 16KiB.
- Dynamically set the netlink receive buffer size.
- Sort out setting netlink receive buffer size.

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.7-0
- Fix buffer overflow in extract_status_code().
  Issue #960 identified that the buffer allocated for copying the
  HTTP status code could overflow if the http response was corrupted.
  This commit changes the way the status code is read, avoids copying
  data, and also ensures that the status code is three digits long,
  is non-negative and occurs on the first line of the response.
- Some fixes for config-test.
- Change ka_config_error() to report_config_error().
- Read interface addresses when doing config-test.
- Update documentation re garp_lower_prio_repeat.
- Add comment re tracking routes with nexthops doesn't work.
- Fix handling of default_interface
  Issue #963 identified that default_interface wasn't being set
  correctly. The problem was that the configuration was read by the
  parent process, but the parent process doesn't know about the
  system interfaces.
  Fix commit makes the vrrp process set the default interface when
  it starts.
- Fix a segfault in checker process on reload
  Issue #955 identified a segfault when keepalived reloads. This
  was caused by attempting to set the receive buffer size on a
  netlink socket that was not open. It now only attempts to set
  buffer sizes on the netlink sockets that are open.
- Use report_config_error() in check_parser.c.
- Don't run a sublevel close handler on a skipped configuration block
  If a configuration block was skipped due to an error, the configuration
  read won't be valid and may not even exist, so make sure the sublevel
  end handler isn't run.
  An example is if a virtual_server block is skipped, then the sublevel
  end handler would have run against the previous (if any) virtual_server,
  and if there hadn't been a previous virtual_server block it could
  segfault.
- Tidy up use of inet_stosockaddr.
- Add more error checking to read_timer() and its uses.
- Add validation of lvs_sched.
- Use report_config_error() in checker parsers
  Thwese should have been included in commit ead70947 -
  "Update config-test".
- Add stronger validation of numeric fields
  Issue #955 identified that invalid parameters in advert_int, delay_loop,
  lb_algo/lvs_sched, lb_kind/lvs_method, quorum, ip_family, virtual_server
  and real_server ports, weights and connect_timeout were not being reported.
  This commit will now report any errors in those fields, and a number of
  other fields.
- Improve parsing of virtual_router_id.
- Allow virtual server ports not to be specified
  If the service is persistent, a "wild-card" port can be used.
- Prepend WARNING to read_int/unsigned/double messages if not rejecting
  read_int()/read_unsigned()/read_double() can output log messages if
  the syntax is invalid but the configuration is being accepted, e.g.
  parsing 12zyx will return 12 if _STRICT_CONFIG_ is not defined. In
  this case we want to indicate that the entry is not valid, but we
  are still processing it, so prepend the error message with WARNING.
- Improve parsing of virtual server group address ranges
  An address range of 10.9.8.7-10.9.8.15 was parsed as 10.9.8.7-10
  and no error was reported, although someone might have expected
  that this would mean 10.9.8.7-15.
  keepalived will now report a configuration warning, and if
  keepalived is configured with --enable-strict-config-checks the
  configuration will be rejected.
- Restore original string in inet_stosockaddr()
  If there was a '-' or a '/' after the address, the string was modified
  to terminate at that point. This commit now restores the original string.
- Allow keepalived to run with --config-test when live instance running.
- Report errors for invalid smtp_server.
- Remove inet_stom() - it was not used
  inet_stom used atoi which is unsafe. Since the function was not used,
  it has been simply removed.
- Rename read_(int|unsigned|double) read_(int|unsigned|double)_strvec
  Want to be able to have equivalent functions just being passed a string,
  so rename the functions using strvec to be explicit about that.
- Fix config dump for vrrp_garp_lower_prio_delay.
- Fix config dump of vrrp garp_refresh.
- Make config dump write fraction part of vrrp preempt delay.
- Simplify config dump of garp/gna_interval.
- dd config dump for VRRP/checker/BFD realtime_priority/limit.
- Ensure structure fully initialised for sched_setscheduler.
- Make set_process_dont_swap() and set_process_priority() static functions.
- Minimise time when keepalived runs with realtime priority
  keepalived shouldn't use realtime priority when it is loading or
  reloading configurations, so delay setting realtime priorities, and
  revert to stardard scheduling when terminating or reloading.
- Report user/system CPU time used when exit with detailed logging.
- Make default rlimit_rtime 10000 microseconds
  The previous default of 1000 microseconds was insufficient
- Stop using atoi for readong configuration weight.
- Make read_unsigned, read_int, read_double for parsing strings
  These functions are analogous to read_unsigned_strvec, read_int_strvec
  and read_double_strvec, but take strings as the parameter rather than
  a strvec.
- Stop using atoi for parsing mask of ip addresses.
- Stop using atoi for reading VRID in Dbus code.
- Stop using atoi for reading vrrp debug level, and add to conf dump.
- Stop using atoi for parsing garp_refresh.
- Stop using atoi for parsing preempt_delay.
- Stop using atoi for parsing garp_lower_prio_repeat.
- Stop using atoi for parsing vrrp script rise.
- Stop using atoi for parsing vrrp script fall.
- Stop using atoi for parsing garp_interval/gna_interval
- Stop using atoi for parsing smtp status code
- Stop using atoi for parsing realtime scheduling priority
- Stop using atoi for parsing process priorities
- Stop using atoi for parsing global garp/gna_interval
- top using atoi for parsing genhash port number
- Stop using atoi for parsing tcp_server port number
- Stop using atoi for parsing command line log facility.
- update documentation to show range of bfd weights
- Ensure read_unsigned() detects negative numbers.
- Stop using atoi to parse HTTP_GET status code.
- Stop using atoi to parse checker port numbers.
- Use read_unsigned() for domain/inet_stosockaddr port.
- Make read_unsigned_strvec() recognise minus sign after spaces
  It is possible have a word read from the configuration start with
  spaces it is is enclosed in quotes, which are then removed, but
  the leading spaces aren't removed.
- Make get_u8()/get_u16()/get_u32() use read_unsigned().
- Make get_u64() properly detect -ve numbers.
- Make get_time_rtt() properly detect -ve numbers.
- Make get_addr64() handle whitespace properly and disallow '-' signs
  Skip leading whitespace, don't allow embedded whitespace, and don't
  allow minus signs.
- Make get_addr64() and parse_mpls_address handle whitespace
- Change more log_message() to report_config_error() in vrrp_iproute.c.
- Improve use of strtoul() in rttables.c.
- Implement get_u64() in same way as get_u8() etc.
- Fix print format specifier in read_unsigned_base
- Correct error message for garp_master_refresh
- Remove \n from error message.
- Allow round trip time to be UINT32_MAX
- Change mix_rx to min_rx for bfd_instance in documentation.
- Make bfd_parser use read_unsigned_strvec() etc rather than strtoul().
- Fix config dump for BFD instance timers.
- Fix handling of ip rule ipproto option.
- Add read_unsigned_base_strvec() to allow number base to be specified
  This requires renaming static functions read_int_int() etc to
  read_int_base() etc.
- Minimise and improve use of strtoul() etc in parsing ip rules.
- Use read_int_strvec() for vrrp_version.
- Use read_int_strvec() instead of strtol() in vrrp_parser.c.
- Use read_int_strvec() instead of strtol() etc in check_parser.c.
- Use read_int_strvec() instead of strtol() etc in check_data.c.
- Improve strtoul handling for '--log_facility' command line option.
- Add documentation for lvs_timeouts config option.
- Allow vrrp garp_delay to be 0 in accordance with documentation.
- Use read_int_strvec() instead of strtol() etc in global_parser.c.
- Corret end of line detection in genhash.
- Improve genhash command line parsing use of strtoul.
- Replace CHECKER_VALUE_INT with read_unsigned_strvec due to use of strtoul.
- Remove CHECKER_VALUE_UINT definition since no longer used.
- Add conditional compilation around variable not always used.
- Only read interfaces in VRRP process.
- Enable --config-test to work with BFD configuration.
- Only add garp_delay_t's to interfaces used by VRRP instances
  There is no point allocating a garp_delay_t to an interface that
  isn't used by a VRRP instance, so this commit make keepalived only
  allocate garp_delay_t scructures to the used interfaces.
  In addition, when the configuration is dumped, list the interfaces
  relevant to each garp_delay_t.
- Add logging command line options if keepalived segfaults.
- Don't free tcp checker data field on exit, since not used.
- Report configuration file line numbers when errors
  Following the recent series of commits for better validation of
  the configuration, and the move to reporting all configuration
  errors through report_config_error(), it is now feasible to report
  the configuration file line number on when the error occurs.
- Rationalise error messages when reading configuration
  Now that configuration file line numbers are reported, the error
  messages can be simplified since the context doesn't need to be
  given in the detail as before.
- Return NULL rather than false as a pointer in parser.c
- Fix an infinite loop when parsing certain parameter substitutions
  If a multiline definition had text after the '=' sign, keepalived
  would loop.
- Fix a multiline parameter substitution having a replacement on 1st line
  If a multiline parameter definition had a replaceable parameter or a
  definition on the first non-blank line, it wasn't being handled. This commit
  ensures that replaceable parameters/definitions on the first line are
  handled correctly.
- Add logging command line options when keepalived starts.
- Change some log_message() to report_config_error() in vrrp_sync.c.
- Improve handling of select() returning an error
  If select returned an error, the code was processing the returned
  timeout and fds as though they were valid. This commits logs an
  error the first time, sleeps for 1 second if it is a programming
  error, and then sets up the select call again.
- Remove DBG() statement left over in previous commit.
- improve doc spelling.
- Add mh scheduler for LVS
  This is similar to the sh scheduler. Options are the same but we
  duplicate everything. An alternative would have been to reuse the
  names for the sh scheduler.
  The mh scheduler is supported starting from Linux 4.18. It's a
  consistent hash scheduler.
- manpage update and re-visited.
  keepalived.conf.5 be considered as THE exhaustive source of information
  in order to configure Keepalived. This documenation is supported and
  maintained by Keepalived Core-Team.
- Fix errors in KEEPALIVED-MIB.txt
  Commit 181858d - "Add mh scheduler for LVS" introduced a couple
  of formatting errors, and didn't update the revision date.
- Some SNMP library handling improvements.
- Stop bfd -> vrrp pipe read timing out
  There is no need for a timeout on reading the pipe, so set the
  timeout to TIMER_NEVER.
- manpage updates
  Update manpage to make html convertion easy. This manpage is now
  sitting in documentation tab of Keepalived website.
- Update libnl_link.c
  SegFault when launch with dynamic LIBNL because of loading symbol
  from wrong library.
- Fix building rpm package and instructions
  Issue #977 identified that the instructions in the INSTALL file
  were incorrect.
- Adds regex pattern matching for HTTP_GET and SSL_GET.
- Remove pcre build tests from Travis-CI
  Travis-CI environments are too old to support libpcre2, so we have
  to remove it.
- Fix #980: coredump on start when logfile cannot be accessed.
- Don't loop forever if configuration has unknown replaceable parameter.

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.6-0
- Fix genhash digest calculation. The bracketting in HASH_UPDATE was wrong.
- Bring keepalived(8) man page up to date.
- Fix segfault when IPVS_DEST_ATTR_ADDR_FAMILY not defined.
  Issue #938 identified a segfault on the checker process when using
  CentOS/RHEL 6. It turned out that conditional compilation check
  for IPVS_DEST_ATTR_ADDR_FAMILY was not being handled correctly.
- Don't create a link-local address for vmac when vmac_xmit_base is set
  Since commit 18ec95add483 ("Make vmac_xmit_base work for IPv6
  instances") VRRP advertisements are sent from the base interface and not
  from the vmac interface when vmac_xmit_base is set.
  Therefore, there is no need to configure a link-local address on the
  vmac interface. This also means that we don't need to regenerate a
  link-local address for the vmac if the link-local address was removed
  from the base interface, or inherit a link-local address in case one was
  configured on the base interface.
- Fix setting i/f params on a bridge underlying i/f of a VMAC
  Issue #944 identified that when the underlying interface of a VMAC
  interface was a bridge, keepalived was failing to set arp_ignore and
  arp_filter in the underlying bridge interface. The problem appears to
  lie in the libnl3 library. The description of the problem given in the
  issue report was:
    Problem is that ifi_family is set to AF_BRIDGE, whereas it should be set
    to AF_UNSPEC. The kernel function that handles RTM_SETLINK messages for
  AF_BRIDGE doesn't know how to process the IFLA_AF_SPEC attribute.
  This commit stops using libnl3 for setting/clearing arp_ignore and
  arp_filter, and directly constructs the netlink messages in keepalived.
- Use RTM_NEWLINK rather than RTM_SETLINK for setting i/f options
  libnl3 uses RTM_NEWLINK rather than RTM_SETLINK for setting
  interface options when ifi_family is AF_UNSPEC, so update commit
  9b2b2c9 - "Fix setting i/f params on a bridge underlying i/f of
  a VMAC" to do likewise.
- Fix creating VMACs on 2.6.32 and earlier kernels
  RTM_NEWLINK didn't support specifying interface by name until
  Linux 2.6.33, and if using an earlier kernel, the netlink call
  failed. This meant that the VMAC was not enabled.
- Fix setting arp_ignore and arp_filter on bridge interfaces.
- Add diagnostic message if vrrp script time out and kill fails.
- Fix compile errors and warnings when building with --enable-debug.
- Don't do md5 check unless configured.
- In http_handle_response() combine fetched_url and url
  fetched_url and url always pointed to the same url, so only use
  one variable.
- Store and handle HTTP_GET digest in binary form
  Configured digests were being stored in character string form, and
  the calculated digests were converted to strings. This commit now
  handles digests as fixed length binary data, and validates the
  configured digests to make sure they are valid hex strings with
  the correct length.
- Add support for quote and escape handling of notify and other scripts.
  Notify and other scripts need to be able to be configured with embedded
  spaces, quotes and special characters for the command and the parameters.
  This commit adds that ability.
- When checking script file path, only replace name part if same file.
  Some executables are in the filesystem as symbolic links, and alter
  their functionality based on the file part of the name. This was being
  incorrectly handled by keepalived, which now checks whether a file exists
  using the original name, and it it does whether it is the same file.
- Remove cmd_str from notify_script_t
  The cmd_str string (sort of) duplicated what was in the args array
  of a notify_script_t, but was not always accurate. With the removal
  of cmd_str, whenever it needs to be output, the string is now
  generated from the args array, so accurately reflects what is
  actually executed.
- Add quoting and escaping for script configuration, and other minor changes.
- Use vsyslog() if available instead of syslog().
- Report virtual server as well as real server when config dump checker.
- Only report IP_MULTICAST_ALL unset for IPv4 sockets
  Commit 6fb5980 - "Stop receive message queues not being read on send
  sockets" added a warning if data was received on vrrp send sockets, since
  setting IP_MULTICAST_ALL should stop packets being received, but older
  kernels still queued packets.
  It has now been discovered the IP_MULTICAST_ALL (of course) only applies
  to IPv4 and so the warning only makes sense for IPv4 sockets.
  I haven't been able to find a way to stop IPv6 multicast packets being
  received on the send socket. It appears that if any socket adds an IPv6
  multicast group on an interface, then any raw socket using that interface
  will recieve all enabled multicast packets, and the receive socket has to
  add the multicast group.
- Properly stop packets being queued on vrrp send sockets
  Commit 6fb5980 - "Stop receive message queues not being read on
  send sockets" did stop messages building up on the receive queue
  of vrrp send sockets, but it wasn't an ideal solution, and it also
  made the assumption that the problem was only occurring due to
  multicast packets not being filtered when IP_MULTICAST_ALL was set,
  which appears not to work properly between at least Linux 3.6.11 and
  3.16. In fact the problem also occurred when using IPv4 unicast and
  IPv6 in any form, and so has been a long term issue in keepalived.
  The original solution was to listen on the send socket and discard any
  packets that were received. This commit takes a completely different
  solution (many thanks to Simon Kirby for the suggestion) and sets a
  BPF filter on send sockets that filter out all received packets on the
  sockets.
  This commit effectively reverts commit 6fb5980, and the subsequent
  commits 88c698d8 - "Cancel read thread on send sockets when closing",
  f981b55d - "Only allow vrrp_rx_bufs_policy NO_SEND_RX if have
  IP_MULTICAST_ALL", 7ff7ea1f - "Another fix to listening on send socket",
  and 77d947f7 - "Only report IP_MULTICAST_ALL unset for IPv4 sockets"
  and partially reverts 4297f0a - "Add options to set vrrp socket receive
  buffer sizes".
  This commit removes the configuration option NO_SEND_RX from
  vrrp_tx_bufs_policy introduced in commit 4297f0a since it is now
  no longer relevant, because no packets are queued to the send socket.
- Add newlines to the keepalived.stats output for better readability.
- Add notify_master_rx_lower_pri script option and FIFO output.
  If a lower priority router has transitioned to master, there has presumably
  been an intermittent communications break between the master and backup. It
  appears that servers in an Amazon AWS environment can experience this.
  The problem then occurs if a notify_master script is executed on the backup
  that has just transitioned to master and the script executes something like
  a `aws ec2 assign-private-ip-addresses` command, thereby removing the address
  from the 'proper' master. Executing notify_master_rx_lower_pri notification
  allows the 'proper' master to recover the secondary addresses.
- Fix malloc'd memory length in open_log_file().

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.5-0
- Update config-test option so keepalived exits with status 1 on failure.
- Fix config write of virtual server group ip addresses.
- Document default and default6 for virtual/static route destinations.
- Cancel read thread on send sockets when closing.
  Commit 4297f0a - "Add options to set vrrp socket receive buffer sizes"
  added reading on vrrp send sockets to stop receive queues building up
  on some 3.x kernels. The commit didn't cancel the read thread on the
  send sockets when the socket was closed, causing several thousand
  log writes. This commit cancels the read thread.
- Exit with status 1 if config check fails, and fix terminating when
  reading send sockets.
- Stop segfaulting when receive a packet (fixing commit 97aec76).
  Commit 97aec76 - "Update config-test option so keepalived exits
  with status 1 on failure" had a test for __test_bit(CONFIG_TEST_BIT)
  the wrong way round. This commit fixes that.
- Don't assume rpm is available.
- Only allow vrrp_rx_bufs_policy NO_SEND_RX if have IP_MULTICAST_ALL.
- Improve setting up virtual/real servers with virtual server groups.
  When setting up virtual servers defined by virtual server groups,
  keepalived was getting confused between fwmarks and ip addresses.
  This still needs further work, but the setting up of virtual/real
  servers now works.
- Fix setting up and deletion of virtual servers with groups
  Virtual server entries in virtual server groups can be used
  by multiple virtual_server entries. This commit ensures that
  virtual servers are not deleted until the last virtual_server
  instance using the virtual server is removed.
- Allocate vrrp send buffer during vrrp_complete_instance()
  Issue #926 identified a segfault. The vrrp send buffer was not being
  allocated early enough, and was being accessed before being allocated
  if the checksum algorithm needed updating.
- Fix vrrp v3 with unicast and IPv4.
  The checksum calculations were happening in the wrong way, with the
  wrong data. This commit sorts all that out.
- Don't set effective priority to 254 when specify dont_track_primary.
- Make csum_incremental_update16/32 inline.
- Add --enable-optimise=LEVEL configure option.
- Remove debug message left in configure.ac from adding --enable-optimise.
- Fix compiling on CentOS 6.
  Issue #932 identified that keepalived would not compile on CentOS 6.
  The problem is that kernel header file linux/rtnetlink.h needs
  sys/socket.h to be included before linux/rtnetlink.h when using old
  (e.g. 2.6) kernel headers.
- Another fix to listening on send socket.
  Commit 4297f0a - "Add options to set vrrp socket receive buffer sizes"
  added reading on vrrp send sockets to stop receive queues building up
  on some 3.x kernels. The commit didn't save the new thread in
  sock->thread_out when it was added for reading in vrrp_write_fd_read_thread.
  It now does so.

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.4-0
- Make vmac_xmit_base work for IPv6 instances.
  Issue #917 identified that for IPv6 even when vmac_xmit_base was
  configured, the adverts were being sent from the vmac interface.
  This commit makes the packets be sent from the underlying interface
  when vmac_xmit_base is configured.
- Handle vmac_xmit_base when interfaces are recreated.
- Add -t config-test option.
  Issue #389 has received increasing support to add a configuration
  validation option. This commit adds the -t/--commit-test option
  to report any detected configururation errors and exit.
  Errors are logged to the system log by default, but use of the -g
  and -G options can make the errors be logged to files.

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- Fix building with --disables-routes configure option.
- Fix some compiler warnings on Travis-CI.
- Fix setting vrrp effective priority on reload.
- Add tracking of static addresses, routes and rules
  By default a static address, route or rule will now be reinstated
  if it is deleted, unless the no_track option is specified.
  In addition, if a track_group is specified for an address/route/rule
  then if the address/route/rule cannot be reinstated (e.g. if the
  specified interface is down or has been deleted), then the vrrp
  instances specified in the track group will transition to fault state
  until the interface comes back up.
  This commit completes the monitoring and reinstatement of addresses
  routes and rules and means that keepalived should now fully support
  hot-swap devices.
- Log when restoring static addresses, routes or rules.
- Allow static addresses/routes/rules to be configured on VMACs.
  When VMACs were using an interface name generated by keepalived,
  if static address/routes/rules had beeon configured on a VMAC
  interface name, then a different name would be generated for
  the vrrp instance. This commit now allows the same name to be used.
- Fix configure when pkg-config --libs returns -L entries.
- Add log message for advert receive timeout when using log detail (-D).
- Stop receive message queues not being read on send sockets.
  We shouldn't receive anything on vrrp send sockets since IP_MULTICAST_ALL is
  cleared, and no multicast groups are subscribed to on the socket. However,
  Debian Jessie with a 3.16.0 kernel, CentOS 7 with a 3.10.0 kernel,
  and Fedora 16 with a 3.6.11 kernel all exhibit the problem of multicast
  packets being queued on the send socket. Whether this was a kernel problem
  that has been subsequently resolved, or a system default configuration
  problem isn't yet known.
  The workaround to the problem is to read on the send sockets, and to discard
  any received data.
  If anyone can provide more information about this issue it would be
  very helpful.
- Ensure sorry server/virtual server same address family unless tunnelled.
  A real server and a virtual server can only be of the same address family
  if the forwarding method is tunnelled, and also must have a kernel that
  supports IPVS_DEST_ATTR_ADDR_FAMILY.
- Add options to set vrrp socket receive buffer sizes.
  Some systems have very large settings for net.core.rmem_default
  allowing very large receive queues to build if the sockets aren't
  read. keepalived doesn't need large buffers for receive queues,
  so this commit allows options for setting the maximum buffer sizes
  to be much smaller. It also adds the option of setting the receive
  buffer size on the vrrp send sockets to be as small as possible,
  since we shouldn't be receiving anything on those.
  Following commit 6fb5980 - "Stop receive message queues not being
  read on send sockets", this commit also adds the option not to
  read the send sockets, which can be used where it is known that the
  kernel will not queue unwanted multicasts to the send socket.
- Consider eVIPs when determining if need GARP/NDISC send buffers.
- Fix sending IPv6 unicast vrrp adverts.

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Only compile code in rttables.c that is needed by the
  configuration.
- Set default preferences for ip rules if not specified.
  Since different vrrp instances can become master in different
  orders, if preferences (priorities) are not specified for
  ip rules, the order in which they are specified will be
  indeterminate. In order to give some consistency, keepalived
  will not allocate a default preference to each rule, and will
  also warn that this is probably not going to work as intended.
  The solution is to specify a preference for each rule.
- Require preference if an ip rule specifies goto.
  Since preferences are now auto-generated if not specified, a
  rule with a goto must now specify a preference.
- Add tracking of virtual rules.
  If a virtual rule is deleted, the vrrp instance will transition
  to backup. When it becomes master again the rule will be re-added.
- Fix compilation failure found by Travis-CI.
- In configure.ac check if SHA1_Init() needs -fpic.
- Fix make rpm when rpmbuild doesn't support --build-in-place.
- Update INSTALL file to describe how to build rpm files.
- Fix instructions for building rpm packages.

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Remove '\n' characters from log_message() text.
- Allow IPv6 ip rules to be specified using fwmarks.
- Fix configure generation of keepalived.spec file.
- Stop rebuilding scheduler.o every make.
- Remove ' characters from configure args in keepalived -v output.
- Remove duplicate reporting of network namespace in config dumps
- Add ${_INSTANCE} config parameter.
- Remove debugging log message.
- Recalculate max_fd used for select if it should reduce.
- Add tracking of virtual routes.
  If a virtual route is deleted, by default to vrrp instance will
  now transition to backup mode, and if it transitions to master
  again the route will be re-added. If an interface on which a
  route is configured is down, then the instance will go to fault
  state, since the route cannot be added.
  This commit also adds a no-track option for routes, which means
  that deletion of the route will not cause the vrrp instance to
  transition to backup.
- Handle interface down at startup with tracked route configured on it
  If a virtual route which is tracked is configured on an interface that
  is down at startup, then the vrrp instance needs to start in fault
  state.
- Rename netlink_reflect_filter() to netlink_link_filter()
  The function only handles RTM_NEWLINK/RTM_DELLINK messages and there
  are other functions to handle other message types.
- Fix compilation warning.
- Make recreating deleted VMACs work.
- Fix Travis-CI compilation failure and warning.
- Stop duplicate definition and duplicate include in vrrp_iproute.c.
- Add new ip rule options for Linux 4.17
  FRA_PROTOCOL, FRA_IP_PROTO, FRA_SPORT_RANGE and FRA_DPORT_RANGE have
  been added in Linux 4.17.

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Transition to master as soon as decision is made to do so
    Previously keepalived waited one further advert interval before
    transitioning.
    This meant that previously if a master went down and sent priority
    0 message, there was one extra advert interval before the highest
    priority backup configured the VIP addresses.
    Now if vrrp instances have high priorities (i.e. close to 255),
    then the transition to master and configuration of addresses will
    now occur in a small multiple of advert_interval/256.
- Process interface state changes immediately.
    Previously keepalived waited for advert timer expiry. The problem
    was that if an interface went down and came back up before the
    next timer expiry, and addresses, routes and VMACs that we had
    configured on that interface would be removed, but we wouldn't
    know about it.
- Add support for hot-swappable NICs
    This also handles interfaces being deleted and restored.
- Add vrrp_track_file option.
    This allows track_scripts, which are run on a frequent scheduled
    basis, to be replaced with a vrrp_track_file, which contains a
    number as a text string which is used in the same way as the exit
    status from a track script. The track_files are only read if they
    are changed, so external events can update a track file, rather
    than their status needing to be detected by polling by track
    scripts.
- Add notify fifos.
    Rather than sending notifications via notify scripts it is now
    possible to send notify messages via fifos. Not only does this
    mean that the overhead of executing script for each notification
    is removed, but it also guarantees the delivery of notifications
    in the correct order, whereas if the notification is via scripts,
    there is no guarantee that the scripts will execute in the desired
    order if two or more notifications are sent in quick succession.
    There can be a global fifo to process all notifies, and also
    separate fifos for vrrp and checkers. It is possible to specify a
    script for keepalived to execute to process the messages on the
    fifo(s).
- Stop logging address addition/deletions if addresses not ours
    The -a option can be used to override this behaviour and log all
    address changes.
- Transition to fault state if source address for adverts is deleted
   from interface
- Transition to backup state if a VIP or eVIP is removed
    When we next transition to master the addresses will be restored.
    If nopreempt is not set, that will be almost immediately.
- Make address owner (priority 255) transition to master immediately
- Don't process a received advert if the authentication fails
- Ignore invalid received adverts totally
    Previously the master down timer was being updated, which meant
    that a backup could be stuck in backup state even if the only
    received adverts were invalid.
- Don't reset timer before sending next advert if receive a lower
  priority advert.
    This was stopping a higher priority backup instance to stay in
    backup state.
- Log if receive invalid authentication header
- Ignore lower priority adverts when backup (to comply with RFCs)
    This also means that the master down timer wasn't reset, which
    was causing a delay to becoming master
- Fix first advert interval of vrrp instances in a sync group.
- Stop two vrrp instances with preempt delay and equal priorities
  flip-flopping between master and backup state
- Make sync group members transition state at same time
    When first instance makes transition (i.e. when the trigger event
    occurs) rather than wait for next timer expiry
- Process vrrp track script returning a new status code immediately
    For all instances (and their sync group members), rather than
    waiting for the next timer expiry on each instance, the instance
    will transition update it's state immediately.
- On reload, make track scripts inherit the state from before reload
    This stops vrrp instances transitioning to down and coming back up
    once the script has run.
- Correct the use of adver_int and master_adver_int
- Ensure when leaving fault state that a vrrp instance transitions
  to backup unless it has priority 255
- Remove quick_sync functionality since no longer needed.
- Improved code efficiency:
  - Finding vrrp instance after read timeout
  - When getting interface information for a new vmac, only request
     information for that i/f.
  - Directly update effective priority of vrrp instances when scripts
     return new status rather than scheduling a thread to do it
  - Don't run a read timeout on vrrp instance in fault state
  - Don't run a track script if no vrrp instance is tracking it
  - Stop checking interface status after every timer expiry since
     processing interface state changes is now done synchronously
  - The timeout for the select call had a maximum timeout of 1 second,
     it now times out only when something needs to happen
  - The timeout on netlink reads was 500 seconds and this has been
     extended to 1 day.
  - Streamline signal handling between main process and child process
     by using signalfd if available, rather than using a pipe
  - Minimise searching for an interface struct based on its index by
     using pointers to the interface structures
  - Stop opening and closing vrrp scripts before running them. We can
     detect they are missing from the return of the exec call.
  - Allow threads that don't need a timeout to never timeout
  - Calculate the maximum fd number when calling select() rather than
     specifying the maximum of 1024.
  - Ignore netlink NEWLINK messages that are only wireless state
     changes.
  - Don't check whether timers have expired after select() returns if
     its timeout didn't expire.
  - Termination of child processes (scripts) were being handled twice
  - Don't generate the IP header checksum since the kernel will always
     generate it.
  - Maintain pointers to tracking scripts to save seaching a list to
     find the relevant script.
  - Vrrp instances to have pointer to interface structure to avoid
      having to search based in index
- Fix the checksum calculation for VRRPv3 unicast peers.
- Don't regenerate the full advert packet each time an advert is sent
    Keepalived now simply updates the necessary fields and calculates
    the change needed to the checksum.
- Detect a vmac interface going down, and make the vrrp instance
  transition to fault state.
    Previously the instance would only go down if the underlying
    interface went down.
- Stop weighted track scripts updating priority of sync group members
- Make vrrp instances go straight to fault state at startup if a
  relevant interface is down
    Previously an instance would start in up state and transition to
    fault at next timer expiry
- Ensure that a sync group starts in backup state unless all members
  are address owners
- Restore master down timer after leaving fault state
- Use execve() to execute scripts rather than system().
    This saves a fork and an extra process, and also allows the
    parameters to be parsed once only at startup, rather than each
    time the script is invoked.
- Don't treat a failure to execute a script as a failure of the script
- Ensure all scripts receive TERM signal when keepalived terminates
- If keepalived is running with an elevated priority, stop running
  scripts with that elevated priority.
- Enable an unweighted tracking script make a vrrp instance which is
  an address owner transition to fault state
- Delay bringing vrrp instances up at startup until after the first
  completion of the tracking scripts
    This stops an instance coming up an then being brought back down
    again after the script completes with a failure.
- Reduce number of error messages if a script is not executable
- Add linkbeat option per vrrp instance
- Fix timer addition on 32-bit systems
- Ignore netlink messages for interfaces using linkbeat polling
- If priority of vrrp instance changes when in backup due to a vrrp
  script, reschedule the read timeout
- If re-using a VMAC after a reload, ensure it is correctly configured
- Don't send priority 0 adverts when transition to fault state unless
  were in master mode
- Identify routes added by keepalived as belonging to keepalived
- Enable vrrp instances to be put into fault state if their routes are
  removed
- Add track scripts, track files and track_if to sync groups and
  deprecate global_tracking
    (use sync_group_tracking_weight instead, but only if necessary).
- Improve AH authentication sequence number handling, and (re)enable
  sequence number checking for VMACs and sync groups
- Remove autoconf/automake generated files from git repo.
    Script build_setup will create the necessary build environment.
- Improve and standardise notifications
- Fix not sending RS and VS notifies if omega set
- Add no_checker_emails to not send emails every time a checker
    changes state, but only if a real server changes state
- Monitor VIP/eVIP deletion and transition to backup if a VIP/eVIP
    is removed unloes it is configured with the no-track option.*
* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- Update snapcraft.yaml for 1.4.x+git
- Fix generation of git-commit.h with git commit number.
- Set virtual server address family correctly.
- Set virtual server address family correctly when using tunnelled
  real servers.
- Fix handling of virtual servers with no real servers at config time.
- Add warning if virtual and real servers are different address families.
  Although normally the virtual server and real servers must have the
  same address family, if a real server is tunnelled, the address families
  can be different. However, the kernel didn't support that until 3.18,
  so add a check that the address families are the same if different
  address families are not supported by the kernel.
- Send correct status in Dbus VrrpStatusChange notification.
  When an instance transitioned from BACKUP to FAULT, the Dbus
  status change message reported the old status (BACKUP) rather than
  the new status (FAULT). This commit attempts to resolved that.
