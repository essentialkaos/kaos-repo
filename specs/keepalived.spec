################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%bcond_without  snmp
%bcond_without  vrrp
%bcond_with     profile
%bcond_with     debug

################################################################################

Name:           keepalived
Summary:        High Availability monitor built upon LVS, VRRP and service pollers
Version:        2.4.3
Release:        0%{?dist}
License:        GPLv2+
URL:            https://www.keepalived.org
Group:          System Environment/Daemons

Source0:        https://www.keepalived.org/software/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make openssl-devel kernel-devel popt-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  libnl3-devel


%if %{with snmp}
BuildRequires:  net-snmp-devel
Requires:       net-snmp-libs
%endif

Requires:       systemd lm_sensors-libs

Provides:       %{name} = %{version}-%{release}

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

mv %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.sample \
   %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%if %{with snmp}
  mkdir -p %{buildroot}%{_datadir}/snmp/mibs/
  install -pm 644 doc/KEEPALIVED-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{name}.service &>/dev/null || :
  systemctl stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  systemctl daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README.md TODO
%doc doc/%{name}.conf.SYNOPSIS doc/samples/%{name}.conf.*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_bindir}/genhash
%{_sbindir}/%{name}
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*
%{_defaultdocdir}/%{name}/README
%if %{with_snmp}
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

################################################################################

%changelog
* Fri Oct 23 2026 Anton Novojilov <andy@essentialkaos.com> - 2.4.3-0
- https://www.keepalived.org/release-notes/Release-2.4.3/

* Fri Oct 23 2026 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- https://www.keepalived.org/release-notes/Release-2.4.2/

* Fri Oct 23 2026 Anton Novojilov <andy@essentialkaos.com> - 2.4.1-0
- https://www.keepalived.org/release-notes/Release-2.4.1/

* Fri Jun 26 2026 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- https://www.keepalived.org/release-notes/Release-2.4.0/

* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 2.3.4-0
- https://www.keepalived.org/release-notes/Release-2.3.4/

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- https://www.keepalived.org/release-notes/Release-2.3.3/

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- https://www.keepalived.org/release-notes/Release-2.3.2/

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- https://www.keepalived.org/release-notes/Release-2.3.1/

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- https://www.keepalived.org/release-notes/Release-2.3.0/

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.2.8-0
- https://www.keepalived.org/release-notes/Release-2.2.8/
