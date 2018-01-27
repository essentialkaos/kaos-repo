################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

Summary:              Common Address Redundancy Protocol (CARP)
Name:                 ucarp
Version:              1.5.2
Release:              8%{?dist}
License:              MIT and BSD
Group:                System Environment/Daemons
URL:                  http://www.ucarp.org

Source0:              http://download.pureftpd.org/pub/%{name}/%{name}-%{version}.tar.bz2
Source1:              %{name}.init
Source2:              vip-001.conf.example
Source3:              vip-common.conf
Source4:              vip-up
Source5:              vip-down

Patch0:               ucarp-1.5.2-sighup.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        autoconf automake libtool gettext libpcap-devel make gcc

Requires(post):       /sbin/chkconfig
Requires(preun):      /sbin/chkconfig /sbin/service
Requires(postun):     /sbin/service

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
UCARP allows a couple of hosts to share common virtual IP addresses in order
to provide automatic failover. It is a portable userland implementation of the
secure and patent-free Common Address Redundancy Protocol (CARP, OpenBSD's
alternative to the patents-bloated VRRP).
Strong points of the CARP protocol are: very low overhead, cryptographically
signed messages, interoperability between different operating systems and no
need for any dedicated extra network link between redundant hosts.

################################################################################

%prep
%setup -q

%patch0 -p0

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_libexecdir}/%{name}
install -dm 755 %{buildroot}%{_initddir}

install -pm 755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}

install -pm 600 %{SOURCE2} %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/
install -pm 700 %{SOURCE4} %{SOURCE5} %{buildroot}%{_libexecdir}/%{name}/

%clean
rm -rf %{buildroot}

%pre
# Legacy, in case we update from an older package where the service was "carp"
if [[ -f %{_sysconfdir}/carp ]] ; then
  %{__service} carp stop &>/dev/null || :
  %{__chkconfig} --del carp
fi

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop &>/dev/null || :
  %{__chkconfig} --del %{name}
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %{_libexecdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/vip-common.conf
%{_sysconfdir}/%{name}/vip-001.conf.example
%{_initddir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/locale/*

################################################################################

%changelog
* Mon Nov 23 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-8
- Initial build
