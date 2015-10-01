###############################################################################

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

###############################################################################

%bcond_without snmp
%bcond_without vrrp
%bcond_with profile
%bcond_with debug

###############################################################################

Name:              keepalived
Summary:           High Availability monitor built upon LVS, VRRP and service pollers
Version:           1.2.19
Release:           0%{?dist}
License:           GPLv2+
URL:               http://www.keepalived.org
Group:             System Environment/Daemons

Source0:           http://www.keepalived.org/software/%{name}-%{version}.tar.gz
Source1:           %{name}.init

Requires(post):    %{__chkconfig}
Requires(preun):   %{__chkconfig}
Requires(preun):   %{__service}
Requires(postun):  %{__service}

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with snmp}
BuildRequires:     net-snmp-devel
%endif

BuildRequires:     gcc make openssl-devel libnl-devel kernel-devel popt-devel

Requires:          kaosv
 
###############################################################################

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

###############################################################################

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
%{__rm} -rf %{buildroot}

%{make_install}

%{__rm} -rf %{buildroot}%{_sysconfdir}/%{name}/samples/
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%if %{with snmp}
  %{__mkdir_p} %{buildroot}%{_datadir}/snmp/mibs/
  %{__install} -pm 644 doc/KEEPALIVED-MIB %{buildroot}%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop >/dev/null 2>&1
  %{__chkconfig} --del %{name}
fi

%postun
if [[ $1 -eq 1 ]] ; then
  %{__service} %{name} restart >/dev/null 2>&1 || :
fi

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO
%doc doc/%{name}.conf.SYNOPSIS doc/samples/%{name}.conf.*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_bindir}/genhash
%{_sbindir}/%{name}
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*

%if %{with snmp}
  %{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
  %{_datadir}/snmp/mibs/KEEPALIVED-MIB
  %{_datadir}/snmp/mibs/VRRP-MIB
%endif

###############################################################################

%changelog
* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.19-0
- Updated to latest release

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.18-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.16-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.15-0
- Updated to latest release

* Sat Dec 20 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.14-0
- Updated to latest release

* Tue Oct 28 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.13-1
- Init script migrated to kaosv2

* Sat Aug 09 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.13-0
- Updated to latest release
- Init script now use kaosv

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.12-0
- Updated to latest release

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.11-0
- Updated to latest release

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2.10-0
- Updated to latest release

* Mon Dec 23 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.9-0
- Updated to latest release

* Tue Oct 22 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.8-0
- Initial build
