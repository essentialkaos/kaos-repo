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
%define __ldconfig        %{_sbin}/ldconfig

################################################################################

Summary:           Layer 2 Tunnelling Protocol Daemon (RFC 2661)
Name:              xl2tpd
Version:           1.3.10
Release:           0%{?dist}
License:           GPL+
Group:             System Environment/Daemons
URL:               http://www.xelerance.com/software/xl2tpd/

Source0:           https://github.com/xelerance/%{name}/archive/v%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          ppp >= 2.4.5-5

BuildRequires:     libpcap-devel openssl-devel

Requires(post):    %{__chkconfig}
Requires(preun):   %{__chkconfig}
Requires(preun):   %{__service}

################################################################################

%description
xl2tpd is an implementation of the Layer 2 Tunnelling Protocol (RFC 2661).
L2TP allows you to tunnel PPP over UDP. Some ISPs use L2TP to tunnel user
sessions from dial-in servers (modem banks, ADSL DSLAMs) to back-end PPP
servers. Another important application is Virtual Private Networks where
the IPsec protocol is used to secure the L2TP connection (L2TP/IPsec,
RFC 3193). The L2TP/IPsec protocol is mainly used by Windows and
Mac OS X clients. On Linux, xl2tpd can be used in combination with IPsec
implementations such as Openswan.
Example configuration files for such a setup are included in this RPM.

xl2tpd works by opening a pseudo-tty for communicating with pppd.
It runs completely in userspace.

xl2tpd supports IPsec SA Reference tracking to enable overlapping internak
NAT'ed IP's by different clients (eg all clients connecting from their
linksys internal IP 192.168.1.101) as well as multiple clients behind
the same NAT router.

xl2tpd supports the pppol2tp kernel mode operations on 2.6.23 or higher,
or via a patch in contrib for 2.4.x kernels.

Xl2tpd is based on the 0.69 L2TP by Jeff McAdams <jeffm@iglou.com>
It was de-facto maintained by Jacco de Leeuw <jacco2@dds.nl> in 2002 and 2003.

################################################################################

%prep
%setup -q

rm -f linux/include/linux/if_pppol2tp.h

%build
export CFLAGS="$CFLAGS -fPIC -Wall"
export DFLAGS="$RPM_OPT_FLAGS -g "
export LDFLAGS="$LDFLAGS -pie -Wl,-z,relro -Wl,-z,now"

%{__make} %{?_smp_mflags} DFLAGS="$RPM_OPT_FLAGS -g "

%install
rm -rf %{buildroot}

%{make_install} PREFIX=%{_prefix}

install -pDm 644 examples/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pDm 644 examples/ppp-options.%{name} %{buildroot}%{_sysconfdir}/ppp/options.%{name}
install -pDm 600 doc/l2tp-secrets.sample %{buildroot}%{_sysconfdir}/%{name}/l2tp-secrets
install -pDm 600 examples/chapsecrets.sample %{buildroot}%{_sysconfdir}/ppp/chap-secrets.sample
install -pDm 755 packaging/fedora/%{name}.init %{buildroot}%{_initrddir}/%{name}
install -pDm 755 -d %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -rf %{buildroot}

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{name}
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__service} %{name} condrestart 2>&1 >/dev/null
fi

################################################################################

%files
%defattr(-,root,root)
%doc BUGS CHANGES CREDITS LICENSE README.*
%doc doc/README.patents examples/chapsecrets.sample
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/ppp/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}-control
%{_bindir}/pfc
%{_mandir}/*/*
%dir %{_sysconfdir}/%{name}
%attr(0755,root,root)  %{_initrddir}/%{name}
%ghost %dir %{_rundir}/%{name}
%ghost %attr(0600,root,root) %{_rundir}/%{name}/l2tp-control

################################################################################

%changelog
* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.10-0
- Update STRLEN in file.h to 100 (from 80)
- xl2tpd-control: fix xl2tpd hanged up in "fopen"
- Update version in spec and opewnrt Makefile

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.9-0
- Add xl2tpd-control man pages
- Update spec file with newest Soure0 and version
- Update License file
- Display PID for call in the logs
- Use left shift rather than pow() function.
- Enable Travis integration
- Remove unnecessary casting of malloc() results
- Remove an unused line of code in init_config()
- Fix some undefined behaviour in read_result()
- Fix feature test macro deprecation warnings

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.8-0
- Another one fix for control buf handling in udp_xmit
- Fixing minor bug in Linux that was introduced by 90368
- Fix control buffer handling in udp_xmit
- Avoid using IP_PKTINFO with non-Linux systems
- Remove duplicated UDP checksum disabling
- Handle LDLIBS carefully
- Avoid false-positive warning message from not smart compilers
- Correctly activate XPG4v2 support
- Simplify signal header inclusion
- Adding info on the mailing lists
- Fixing minor spelling typo in code.
- Fixing minor spelling mistakes in xl2tpd.conf.5 and l2tpd.conf.sample
- Removing -fno-builtin from CFLAGS

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.7-0
- Adding defensive code to deal with error when pppd exits
- Minor compilation fixes
- Refresh debian/ from Debian. Thanks!
- Update URL
- Update copyright year
- Add local ip range option.
- Drop RFC 2661 copy.
- debian/control drop legacy Replaces
- Typo fix
- Fix #98 by checking if a valid PID is being killed
- Avoid problems with bad avp lengths and remaining hidlen from previous
  iteration
- Fix minor grammar issues in xl2tpd.conf(5)
- Fix possible NULL reference when removing lac
- Describe autodial option in xl2tpd.conf manpage
- Update URL in BUGS file
- Add size optimization
- Remove useless returns from magic_lac_tunnel
- Remove duplicate xmit for ZLBs
- Fix segfault on lac remove
- Fix paths in man pages
- Stop sending ZLB in response to out of order ZLB from check_control
- Add exponential backoff retransmits
- Fix build errors caused by inline function with gcc 5
- Fix memory leaks and accessing free'd memory
- Fix double-free on dial_no_tmp;
- Change handle_special to return a value indicating if it frees the buffer
- Remove unnecessary NULL check on lac.
- xl2tpd-control: show all available commands in --help.
- Ignore SIGPIPE signal.
- Unlink result file to prevent leftover a regular file.
- Introduce new option -l for using syslog as the logging facility.
- start_pppd: place opts after "plugin pppol2tp.so".
- Fix typo in reporting available lns count.
- xl2tpd-control: enhance output of print_error().
- xl2tpd-control: cleaup result file atexit().
- xl2tpd-control: open control file with O_NONBLOCK.
- xl2tpd-control: define _GNU_SOURCE to use fmemopen() and friends.
- xl2tpd-control: check end-of-file when reading pipe to avoid dead loop.
- Correct CDN message result range
- place the PPP frame buffer to the call structure
- Place the pty read buffer to the call structure
- Pass pointer to call structure to read_packet()
- Remove convert arg of read_packet() function
- Remove dead code
- Fix the list of ignored files
- Add checks before closing sockets
- Add a bit more info about existing tunnels and calls
- Fix endless loop
- Add fix for socket leak to fork children
- Random fixes
- Solve some memory leaks that show up after several days of running with
  flapping tunnels and calls.
- Fix for avoiding xltpd occasionally going into an endless loop.
- Fixed issue with strtok modifying contents when pushing details for ppd
  plugins
- Added the ability to add a pppd plugin and params to an lns
- Modified lns_remove to close each call rather than just calling
  destroy_tunnel()
- Added control method to remove an lns
- Refactored the do_control() method to use a handler approach for processing
- Fixed potential null pointer when creating a new lns
- Added status control command for lns, this returns tunnel and call information
  via the control socket
- Added control support for adding lns and status command in xl2tp-control
- Added control pipe method CONTROL_PIPE_REQ_LNS_ADD_MODIFY to modify LNS
  configuration
- Introduced shared control request types
- Fixed typo in xl2tpd.conf.5
- Some malloc/free sanity patches.
- Better NETBSD support.
- Prevent a DEBUG message from being sent to syslog when not debugging.

* Fri Apr 11 2014 Anton Novojilov <andy@essentialkaos.com> - 1.3.6-0
- Initial build
