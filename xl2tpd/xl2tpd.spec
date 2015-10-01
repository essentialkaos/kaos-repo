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
%define __ldconfig        %{_sbin}/ldconfig

###############################################################################

Summary:           Layer 2 Tunnelling Protocol Daemon (RFC 2661)
Name:              xl2tpd
Version:           1.3.6
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

###############################################################################

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

###############################################################################

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

###############################################################################

%files
%defattr(-,root,root)
%doc BUGS CHANGES CREDITS LICENSE README.* TODO doc/rfc2661.txt 
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

###############################################################################

%changelog
* Fri Apr 11 2014 Anton Novojilov <andy@essentialkaos.com> - 1.3.6-0
- Initial build
