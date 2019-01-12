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
Version:           2.0.11
Release:           0%{?dist}
License:           GPLv2+
URL:               http://www.keepalived.org
Group:             System Environment/Daemons

Source0:           http://www.keepalived.org/software/%{name}-%{version}.tar.gz
Source1:           %{name}.init

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with snmp}
BuildRequires:     net-snmp-devel
%endif

BuildRequires:     gcc make openssl-devel libnl-devel kernel-devel popt-devel
BuildRequires:     libnfnetlink-devel

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

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- doc: ipvs schedulers update
- Fix a couple of typos in configure.ac.
- Fix namespace collision with musl if_ether.h.
- Check if return value from read_value_block() is null before using.
- Fix reporting real server stats via SNMP.
- Make checker process handle RTM_NEWLINK messages with -a option
  Even though the checker process doesn't subscribe to RTNLGRP_LINK
  messages, it appears that older kernels (certainly 2.6.32) can
  send RTM_NEWLINK (but not RTM_DELLINK) messages. This occurs
  when the link is set to up state.
  Only the VRRP process is interested in link messages, and so the
  checker process doesn't do the necessary initialisation to be able
  to handle RTM_NEWLINK messages.
  This commit makes the checker process simply discard RTM_NEWLINK
  and RTM_DELLINK messages, rather than assuming that if it receives
  an RTM_NEWLINK message it must be the VRRP process.
  This problem was reported in issue #848 since the checker process
  was segfaulting when a new interface was added when the -a command
  line option was specified.
- Fix handling RTM_NEWLINK when building without VRRP code.
- Fix building on Fedora 28.
  net-snmp-config output can include compiler and linker flags that
  refer to spec files that were used to build net-snmp but may not
  exist on the system building keepalived. That would cause the build
  done by configure to test for net-snmp support to fail; in particular
  on a Fedora 28 system that doesn't have the redhat-rpm-config package
  installed.
  This commit checks that any spec files in the compiler and linker
  flags returned by net-snmp-config exist on the system building
  keepalived, and if not it removes the reference(s) to the spec file(s).

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- vrrp: setting '0' as default value for ifa_flags to make gcc happy.
- Add additional libraries when testing for presence of SSL_CTX_new().
  It appears that some systems need -lcrypto when linking with -lssl.
- Sanitise checking of libnl3 in configure.ac.
- Report and handle missing '}'s in config files.
- Add missing '\n' in keepalived.data output.
- Stop backup taking over as master while master reloads.
  If a reload was initiated just before an advert, and since it took
  one advert interval after a reload before an advert was sent, if the
  reload itself took more than one advert interval, the backup could
  time out and take over as master.
  This commit makes keepalived send adverts for all instances that are
  master immediately before a reload, and also sends adverts immediately
  after a reload, thereby trippling the time available for the reload
  to complete.
- Add route option fastopen_no_cookie and rule option l3mdev.
- Fix errors in KEEPALIVED-MIB.txt.
- Simplify setting on IN6_ADDR_GEN_MODE.
- Cosmetic changes to keepalived(8) man page.
- Don't set ipvs sync daemon to master state before becoming master
  If a vrrp instance which was the one specified for the ipvs sync
  daemon was configured with initial state master, the sync daemon
  was being set to master mode before the vrrp instance transitioned
  to master mode. This caused an error message when the vrrp instance
  transitioned to master and attempted to make the sync daemon go from
  backup to master mode.
  This commit stops setting the sync daemon to master mode at initialisation
  time, and it is set to master mode when the vrrp instance transitions
  to master.
- Fix freeing vector which has not had any entries allocated.
- Add additional mem-check disgnostics
  vector_alloc, vectot_alloc_slot, vector_free and alloc_strvec all
  call MALLOC/FREE but the functions written in the mem_check log
  are vector_alloc etc, not the functions that call them.
  This commit adds logging of the originating calling function.
- Fix memory leak in parser.c.
- Improve alignment of new mem-check logging.
- Disable all checkers on a virtual server when ha_suspend set.
  Only the first checker was being disabled; this commit now disables
  all of them.
  Also, make the decision to disable a checker when starting/reloading
  when scheduling the checker, so that the existance of the required
  address can be checked.
- Stop genhash segfaulting when built with --enable-mem-check.
- Fix memory allocation problems in genhash.
- Properly fix memory allocation problems in genhash.
- Fix persistence_granularity IPv4 netmask validation.
  The logic test from inet_aton() appears to be inverted.
- Fix segfault when checker configuration is missing expected parameter
  Issue #806 mentioned as an aside that "nb_get_retry" without a parameter
  was sigfaulting. Commit be7ae80 - "Stop segfaulting when configuration
  keyword is missing its parameter" missed the "hidden" uses of vector_slot()
  (i.e. those used via definitions in header files).
  This commit now updates those uses of vector_slot() to use strvec_slot()
  instead.
- Fix compiling on Linux 2.x kernels.
  There were missing checks for HAVE_DECL_CLONE_NEWNET causing
  references to an undeclared variable if CLONE_NEWNET wasn't defined.
- Improve parsing of kernel release.
  The kernel EXTRAVERSION can start with any character (although
  starting with a digit would be daft), so relax the check for it
  starting with a '-'. Kernels using both '+' and '.' being the
  first character of EXTRAVERSION have been reported.
- Improve grammer.
- add support for SNI in SSL_GET check.
  this adds a `enable_sni` parameter to SSL_GET, making sure the check
  passes the virtualhost in the SNI extension during SSL handshake.
- Optimise setting host name for SSL_GET requests with SNI.
- Allow SNI to be used with SSL_GET with OpenSSL v1.0.0 and LibreSSL.
- Use configure to check for SSL_set_tlsext_host_name()
  Rather than checking for a specific version of the OpenSSL library
  (and it would also need checking the version of the LibreSSL library)
  let configure check for the presence of SSL_set_tlsext_host_name().
  Also omit all code related to SNI of SSL_set_tlsext_host_name() is
  not available.
- Use configure to determine available OpenSSL functionality
  Rather than using version numbers of the OpenSSL library to determine
  what functions are available, let configure determine whether the
  functions are supported.
  The also means that the same tests work for LibreSSL.
- Add support for gratuitous ARPs for IP over Infiniband.
- Use system header definition instead of local definition IF_HWADDR_MAX
  linux/netdevice.h has definition MAX_ADDR_LEN, which is 32, whereas
  IF_HWADDR_MAX was locally defined to be 20.
  Unfortunately we end up with more system header file juggling to ensure
  we don't have duplicate definitions.
- Fix vrrp_script and check_misc scripts of type </dev/tcp/127.0.0.1/80.
- Add the first pre-defined config definition (${_PWD})
  ${_PWD} in a configuration file will be replaced with the full
  path name of the directory that keepalived is reading the current
  configuration file from.
- Open and run the notify fifo and script if no other fifo
  Due to the way the code was structured the notify_fifo for both
  checker and vrrp messages wasn't run if neither the vrrp or checker
  fifo wasn't configured.
  Also, if all three fifos were configured, the general fifo script
  was executed by both the vrrp and checker process, causing problems.
- Add support for Infiniband interfaces when dumping configuration.
- Tidy up layout in vrrp_arp.c.
- Add configure check for support of position independant executables (PIE).
- Add check for -pie support, and fix writing to keepalived.data.

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Make genhash exit with exit code 1 on error.
  Issue #766 identified that genhash always exits with exit code 1
  even if an error has occurred.
- Rationalise printing of http header in genhash.
- Use http header Content-Length field in HTTP_CHECK/SSL_CHECK.
  If a Content-Length is supplied in the http header, use that as a
  limit to the data length (as wget does). If the length of data
  received does not match the Content-Length log a warning.
- Optimise parameter passing to fprintf in genhash.
- Don't declare mark variable if don't have MARK socket option.
- Fix sync groups with only one member.
  Commit c88744a0 allowed sync groups with only 1 member again, but
  didn't stop removing the sync group if there was only 1 member.
  This commit now doesn't remove sync groups with only one member.
- Make track scripts work with --enable-debug config option.
- Add warning if --enable-debug configure option is used.
- Allow more flexibility of layout of { and } in config files.
  keepalived was a bit fussy about where '{'s and '}'s (braces) could
  be placed in terms of after the keyword, or on a line on their own.
  It certainly was not possible to have multiple braces on one line.
  This commit now provides complete flexibility of where braces are, so
  long as they occur in the correct order.
- Make alloc_value_block() report block type if there is an error.
- Simplify alloc_value_block() by using libc string functions.
- Add dumping of garp delay config when using -d option.
- Fix fractions of seconds for garp group garp_interval.
- Make read_value_block() use alloc_value_block().
  This removes quite a bit of duplication of functionality, and
  ensures the configuration parsing will be more consistent.
- Fix build with Linux kernel headers v4.15.
  Linux kernel version 4.15 changed the libc/kernel headers suppression
  logic in a way that introduces collisions.
- Add missing command line options to keepalived(8) man page.
- Fix --dont-release-vrrp.
  On github, ushuz reported that commit 62e8455 - "Don't delete vmac
  interfaces before dropping multicast membership" broke --dont-release-vrrp.
  This commit restores the correct functionality.
- Define _GNU_SOURCE for all compilation units.
  Rather than defining _GNU_SOURCE when needed, let configure add
  it to the flags passed to the C compiler, so that it is defined
  for all compilation units. This ensures consistence.
- Fix new warnings procuded by gcc 8.
- Fix dumping empty lists.
  Add a check in dump_list() for an empty list, and don't attempt
  to dump it if it is empty.
- Resolve conversion-check compiler warnings.
- Add missing content to installing_keepalived.rst documentation.
  Issue #778 identified that there was text missing at the end of
  the document, and that is now added.
- Fix systemd service to start after network-online.target.
  This fix was merged downstream by RedHat in response to
  RHBZ #1413320.
- Update INSTALL file to describe packages needed for building
  documentation.
- INSTALL: note linux distro package that provides 'sphinx_rtd_theme'
- Clear /proc/sys/net/ipv6/conf/IF/disable_ipv6 when create VMACs.
  An issue was identified where keepalived was reporting permission
  denied when attempting to add an IPv6 address to a VMAC interface.
  It turned out that this was because
  /proc/sys/net/ipv6/conf/default/disable_ipv6
  was set to 1, causing IPv6 to be disables on all interfaces that
  keepalived created.
  This commit clears disable_ipv6 on any VMAC interfaces that
  keepalived creates if the vrrp instance is using IPv6.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- Improve and fix use of getopt_long().
  We musn't use a long option val of 1, since getopt_long() can return
  that value.
  getopt_long() also returns longindex == 0 when there is no matching
  long option, and there needs to be careful checking if there is an
  error to work out whether a long or short option was used, which is
  needed for meaningful error messages.
- Write assert() messages to syslog.
  assert()s are nasty things, but at least let's get the benefit of
  them, and write the messages to syslog, rather than losing them down
  stderr.
- Enable sorry server at startup if quorum down due to alpha mode
  If alpha mode is configured on sufficient checkers so that a
  virtual server doesn't have a quorum, we need to add the sorry
  server at startup, otherwise it won't be added until a quorum has
  been achieved and subsequently lost again. In the case where some
  of the checkers remain in the down state at startup, this would have
  meant that the sorry server never got added.
- For virtual servers, ensure quorum <= number of real servers
  If the quorum were gigher than the number of real servers, the
  quorum for the real server to come up could never be achieved, so
  if the quorum is greater than the number of real servers, reduce it
  to the number of real servers.
- Fix some SNMP keepalived checker integer types and default values.
  Some virtual server and real server values were being sent to SNMP
  with a signed type whereas the value is unsigned, so set the type
  field correctly.
  Some virtual server and real server values that apply to checkers
  are set to nonsense default values in order to determine if a
  value has been specified. Handle these values when reporting them
  to SNMP replying with 0 rather than a nonsense value.
- Fix some MALLOC/FREE issues with notify FIFOs.
-  Add instance_name/config_id to alert emails' subjects if configured.
  If multiple instances of keepalived are running, either different
  instance_names and/or config_ids, it is useful to know which
  keepalived instance the email relates to.
- Ensure that email body string isn't unterminated.
  Using strncpy() needs to ensure that there is a nul termination byte,
  so this commits adds always writing a nul byte to the end of the buffer.
- Remove duplicate fault notification.
- Fix problem with scripts found via PATH with a '/' in parameters.
  Recent discussions on issue #101 led to discovering that if an
  executable without a fully qualified name was specified as a script
  and there was a '/' character in the parameters, then the path
  resolution would not work.
- Send SNMP traps when go from backup to fault due to sync group.
  Commit 020a9ab added executing notify_fault for vrrp instances
  transitioning from backup to fault state due to another instance
  in the sync group going to fault state. This commit adds sending
  SNMP traps in the same circumstance.
- Revert "Add instance_name/config_id to alert emails' subjects if
  configured". This should be handled by setting router_id
- Add config option to send smtp-alerts to file rather than send emails
  This is useful for debugging purposes.
- Add additional entry to Travis-CI build matrix.
- Fix segfault if no sorry server configured for a virtual server.
  Issue #751 identified a segfault in vs_end_handler(), and it
  transpires that the forwarding method of the sorry server was being
  checked without first testing that a sorry server had been configured.
- Improve the log message when a master receives higher priority advert.
  The log message reported in issue #754
  "VRRP_Instance(VI_1) Received advert with higher priority 253, ours 253"
  is somewhat misleading since 253 == 253.
  This commit improves the log message in this case be reporting that
  the sender's IP address is higher and the priority is equal. It also
  states the it was a master receiving the advert.
- First stage of making --enable-debug work
  Issue #582 identified that compiling with --enable-debug produced
  an executable that didn't work.
  This commit largely makes that option work, but there needs to be
  more work to make signals work.
- Generalise handling of signals.
- Don't assume json header files are in /usr/include/json-c
  Use pkg-config to find the location of the json header files
  when testing for the presence of the header files in configure.
- Add file updated by configure.ac change.
- Log more helpful message when healthchecker activated or suspended
  Include the realserver in the log message
- Fix building with musl libc.
- fix spelling mistakes about keyword promote_secondaries in man page.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Add Linux build and runtime versions to -v output.
- Log kernel version and build kernel version to log at startup.
- Fix compiling with --enable-debug.
- Don't sleep for 1 send when exiting vrrp process if no vrrp instances.
- Streamline and rationalise use of child_finder function.
  The child_finder function is simplified, and also stop using the
  parent process' child_finder function in the checker process.
- Don't request bug report if script terminates due to seg fault.
  The report_child_status() function would log a message requesting a
  bug report if a check_misc script or a vrrp_track script exited due
  to a seg fault.
-  Handle vrrp track and check_misc scripts being killed by signal.
-  Rationalise reporting of child process exit status.
  report_child_status() is now only called in the main keepalived
  program. The reporting of the exit status of vrrp track scripts
  and MISC_CHECK scripts is now handled in the specific code for
  those scripts. This means that non 0 exit statuses aren't
  repeatedly reported for vrrp track scripts.
- eally fix reporting of child process exit status.
- Log a helpful message i using mem-check and too many allocs.
  keepalived simply being terminated by SIGABRT with no diagnostic
  message was unhelpful.
- Rename child_finder() to child_finder_name() etc
  The function only finds the name of the child process, and not
  the thread for the child process, so rename the function accordingly.
- Add log to file and no syslog options.
  With large configurations the syslog can get flooded and drop output.
  This commit adds options to not log to syslog, and also to log all
  output to files.
- Add option to only flush log files before forking.
- Don't poll netlink for all interfaces each time add a VMAC.
  We can poll for the individual interface details which significantly
  reduces what we have to process.
- Print interface details in keepalived.data output.
- Be consistent with type of size parameter for mlists.
- Fix sign conversion warnings.
- Add high performace child finder code.
  The code to find the relevant thread to execute afer a child process
  (either a vrrp track script or a misc_check healthchecker) was doing
  a linear search for the matching pid, which if there are a large number
  of child processes running could become time consuming.
  The code now will enable high performance child finding, based on using
  mlists hashed by the pid, if there are 32 or more vrrp track scripts or
  misc check healthcheckers. The size of the mlist is based on the number
  of scripts, with a limit of 256.
- Improve high performance child termination timeout code.
- Fix high performance child finder cleanup code.
- Preserve filename in script path name resolution.
  Some executables change their behaviour depending on the name by
  which they are invoked (e.g. /usr/sbin/pidof when it is a link to
  /usr/sbin/killall5). Using realpath() changes the file name part
  if it is a symbolic link. This commit resolves all symbolic links
  to directories, but leaves the file name part unaltered. It then
  checks the security of both the path to the link and the path to
  the real file.
- Handle scripts names that are symbolic links properly.
- Use fstatat() rather than stat() for checking script security.
  If we use fstatat() we can discover if a file is a symbolic
  link and treat it accordingly.
- Fix building with kernels older than v4.4.
- Fix building with --disable-lipiptc and --enable-dynamic-linking.
- Fix building with --without-vrrp configure option.
- Resolve unused return value warning.
- Fix some RFC SNMP issues.
- Attempt to fix mock builds.
- Fix parsing of broadcast + and broadcast -
- check_http.c: http_get_check_compare crash fixed in case of absense
  of digest.
- Add -pie linker option.
  Since -fPIE is specified for the compiler, -pie should be specified
  for the linker.
- check_http.c: http_get_check_compare crash fixed in case of absense o.
- Fix use S_PATH and fchdir().
  S_PATH wasn't defined until Linux 2.6.39 and fchdir() doesn't work
  with S_PATH until Linux 3.5 (according to open(2) man page).
- Fix building with Linux versions between 2.6.39 and 3.3
  Linux 2.6.39 introduced ipsets, but the kernel had some omissions
  from linux/netfilter/ipset/ip_set.h header file, so the libipset
  provided version needed to be used.
  Note: RedHat backported ipsets to at least 2.6.32, so the problem
  applied to earlier versions of RedHat Linux and Centos.
- Fix segfault when parsing invalid real server.
  If the first real server ip address doesn't match the address
  family of the virtual server, then we need to skip parsing the
  rest of the real_server block.
- Make when vs_end_handler is executed
  Commit 1ba7180b ('ipvs: new service option "ip_family"') added a
  sublevel_end_handler vs_end_handler, but this was being executed
  at the end of each real_server rather than after the virtual_server.
  This commit adds a new parser function install_root_end_handler(),
  and vs_end_handler is now installed using that function so that it
  is executed at the end of the virtual_server rather than after each
  real_server.
- Allow tunnelled rs address family not to match vs family.
  The address family of a tunnelled real server does not have to
  match the address family of its virtual server, so we need to
  delay any setting of the vs address family from an rs address
  until the end of the real_server block, so that we know whether
  the forwarding method is tunnelling or not. Likewise the check
  of the sorry server has to be delayed until the end of the
  virtual server configuration (the tunnelling method may be
  specified after the address of the real/sorry server).
  The address family of a virtual server is only not determined
  by the virtual server configuration itself if the virtual server
  is defined by a fwmark and all of the real/sorry servers are
  tunnelled. In this case the address family cannot properly be
  determined from the address family of any tunnelled real servers.
  However, to maintain backward compatibility with configurations
  used prior to this commit, the address family of the virtual
  server will be taken from the address family of the (tunnelled)
  real/sorry servers if they are all the same; if they are not all
  the same it will default to IPv4 (this is not incompatible since
  previously mixed IPv4 and IPv6 real/sorry servers were not allowed,
  even if tunnelled).
- Remove bogus warning for fwmark virtual servers.
  "Warning: Virtual server FWM 83: protocol specified for fwmark
  - protocol will be ignored" should not be given if no protocol has
  been specified.
- Fix removing left-over addresses if keepalived aborts.
- Fix use of init_state after a reload.
  Issue #627 identified that vrrp->init_state was being incorrectly
  used in vrrp_fault(), since it is modified at a reload.
  Instead of using init_state, we now use the configured priority
  of the vrrp instance, so if the vrrp instance is the address owner
  (priority 255) it will transition to master after leaving to fault
  state, otherwise it transitions to backup.
- Remove init_state from vrrp structure
  init_state is no longer used, so remove it from the vrrp structure.
  Since it has been included in keepalived SNMP, it is preserved
  solely for reporting in SNMP requests.
- Change conditional compilation _WITH_SNMP_KEEPALIVED_ to
  _WITH_SNMP_VRRP_
  The functionality that the conditional compilation enabled was snmp
  vrrp functionality, so make the name more relevant.
- Update error message in configure.ac.
- Add more configure options to Travis build matrix.
- Install additional libraries in Travis environment for new options.
- Fix some problem found by Travis-ci.
- Fix configure --disable-checksum-compat option.
- Remove DOS file formatting from .travis.yml.
- Add more configuration option to Travis builds and some build fixes.
- Tidy up some code alignment.
- Update openssl use to stop using deprecated functions
  openssl from version 1.1 deprecated certain functions that keepalived
  was using. This commit ceases using those functions if the version
  of openssl is >= 1.1.
- Fix some issues identified by valgrind.
  Some file descriptors weren't being closed at exit, and also one
  or two mallocs weren't being freed.
- Set pointer to NULL after FREE_PTR() unless exiting.
- Allow sync groups with only 1 member, but issue a warning.
- Fix building with LibreSSL version of OpenSSL.
  Unfortunately LibreSSL updates OPENSSL_VERSION_NUMBER, and its value
  is higher that OpenSSL's latest version. When checking the version
  number we need to check that we are not using LibreSSL (by checking
  whether LIBRESSL_VERSION_NUMBER is defined).
  LibreSSL also hasn't implemented the new functions that OpenSSL has
  provided to replace functions that are deprecated or it is recommended
  should not be used, and so if using LibreSSL the old functions need
  to be used.
- Update genhash to stop using deprecated functions openssl functions.
- Remove last few Subversion source file version Id strings.
  Some of the genhash source code still had Subversion Id strings,
  and these are now removed.
- Add copyright update script.
- Copyright update.
- Remove outdated Version comment.
- Fix update copyright script.
- Include Makefile.in files in copyright update.
- Add replaceable parameters in configuration files.
- Fix some MALLOC/FREE issues with config parameters.
- Add multiline configuration definitions.
- Remove debugging messages left in lib/parser.c.
- Fix a FREE error.
- Fix keepalived.conf(5) man page.
- Fix type in keepalived.conf(5) man page.
- Suppress error message when removing leftover addresses at startup.
