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

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __sysctl          %{_bindir}/systemctl

################################################################################

Summary:            A program for synchronizing files over a network
Name:               rsync
Version:            3.1.3
Release:            0%{?dist}
License:            GPLv3+
Group:              Applications/Internet
URL:                http://rsync.samba.org

Source0:            https://download.samba.org/pub/%{name}/src/%{name}-%{version}.tar.gz
Source1:            https://download.samba.org/pub/%{name}/src/%{name}-patches-%{version}.tar.gz
Source2:            rsyncd.conf
Source3:            rsyncd.sysconfig
Source4:            rsyncd.socket
Source5:            rsyncd.service
Source6:            rsyncd@.service
Source7:            rsyncd.init

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc autoconf
BuildRequires:      libacl-devel libattr-devel popt-devel

Patch0:             rsync-man.patch

%if 0%{?rhel} >= 7
Requires:           systemd systemd-units
%else
Requires:           chkconfig initscripts
%endif

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

################################################################################

%package daemon
Summary:            Service for anonymous access to rsync
Group:              Applications/Internet
BuildArch:          noarch
Requires:           %{name} = %{version}-%{release}

%description daemon
Rsync can be used to offer read only access to anonymous clients. This
package provides the anonymous rsync service.

################################################################################

%prep

%setup -q
%setup -q -b 1

chmod -x support/*

#Needed for compatibility with previous patched rsync versions
patch -p1 -i patches/acls.diff
patch -p1 -i patches/xattrs.diff

#Enable --copy-devices parameter
patch -p1 -i patches/copy-devices.diff

%patch0 -p1 -b .man

%build

%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{makeinstall} INSTALLCMD='install -p' INSTALLMAN='install -p'

install -Dm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyncd.conf
install -Dm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rsyncd

%if 0%{?rhel} >= 7
install -Dm 644 %{SOURCE4} %{buildroot}%{_unitdir}/rsyncd.socket
install -Dm 644 %{SOURCE5} %{buildroot}%{_unitdir}/rsyncd.service
install -Dm 644 %{SOURCE6} %{buildroot}%{_unitdir}/rsyncd@.service
%else
install -Dm 755 %{SOURCE7} %{buildroot}%{_initddir}/rsyncd
%endif

%clean
rm -rf %{buildroot}

%post daemon
%if 0%{?rhel} >= 7
if [[ $1 -eq 1 ]] ; then
  %{__sysctl} preset rsyncd.service &>/dev/null || :
fi
%else
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add rsyncd &>/dev/null || :
fi
%endif

%preun daemon
%if 0%{?rhel} >= 7
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable rsyncd.service &>/dev/null || :
  %{__sysctl} stop rsyncd.service &>/dev/null || :
fi
%else
if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --del rsyncd &>/dev/null || :
  %{__service} rsyncd stop &>/dev/null || :
fi
%endif

%postun daemon
%if 0%{?rhel} >= 7
%{__sysctl} daemon-reload rsyncd.service &>/dev/null || :

if [[ $1 -ge 1 ]] ; then
  %{__sysctl} try-restart rsyncd.service &>/dev/null || :
fi
%else
if [[ $1 -ge 1 ]] ; then
  %{__service} rsyncd restart &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING NEWS OLDNEWS README support/ tech_report.tex
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files daemon
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rsyncd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_mandir}/man5/rsyncd.conf.5*
%if 0%{?rhel} >= 7
%{_unitdir}/rsyncd.socket
%{_unitdir}/rsyncd.service
%{_unitdir}/rsyncd@.service
%else
%{_initddir}/rsyncd
%endif

################################################################################

%changelog
* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.1.3-0
- Updated to latest stable release

* Wed Feb 15 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.2-0
- Initial build for kaos repository
