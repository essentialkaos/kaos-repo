################################################################################

%global _python_bytecompile_errors_terminate_build 0

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
%define __sysctl          %{_bindir}/systemctl

################################################################################

%define service_user      netdata
%define service_group     netdata

################################################################################

Summary:          Real-time performance monitoring tool
Name:             netdata
Version:          1.8.0
Release:          0%{?dist}
Group:            Applications/System
License:          GPLv2+
URL:              http://netdata.firehol.org

Source0:          https://github.com/firehol/netdata/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Source1:          %{name}.sysconfig
Source2:          %{name}.init

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    libmnl-devel zlib-devel libuuid-devel
BuildRequires:    make gcc autoconf automake xz PyYAML

Requires:         kaosv >= 2.10 libmnl zlib curl jq pkgconfig lm_sensors PyYAML

%if 0%{?rhel} >= 7
BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts
%endif

################################################################################

%description
Real-time performance monitoring, in the greatest possible detail!

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure \
        --docdir="%{_docdir}/%{name}-%{version}" \
        --with-zlib \
        --with-math \
        --with-user=%{service_user}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} -name .keep -exec rm -f {} \;

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}

install -pm 644 system/netdata.conf %{buildroot}%{_sysconfdir}/%{name}/
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 system/%{name}.service %{buildroot}%{_unitdir}/
%else
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -M -g %{service_group} -s /sbin/nologin %{service_user}
exit 0

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
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE.md README.md
%config(noreplace) %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(-, %{service_user}, %{service_group}) %dir %{_localstatedir}/cache/%{name}/
%attr(-, %{service_user}, %{service_group}) %dir %{_localstatedir}/log/%{name}/
%attr(-, %{service_user}, %{service_group}) %{_sharedstatedir}/%{name}/
%attr(-, root, %{service_group}) %{_datadir}/%{name}/
%{_libexecdir}/%{name}/
%{_sbindir}/%{name}

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

################################################################################

%changelog
* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- Updated to latest stable release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to latest stable release

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Updated to latest stable release

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to latest stable release

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to latest stable release

* Sun Apr 10 2016 Gleb Goncharov <yum@gongled.me> - 1.0.0-0
- Initial build
