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

%define service_user      netdata
%define service_group     netdata
%define service_home      /
%define service_name      %{name}

################################################################################

Summary:          Linux real time system monitoring, over the web
Name:             netdata
Version:          1.0.0
Release:          0%{?dist}
Group:            Applications/System
License:          GPLv2+
URL:              http://firehol.org

Source0:          http://firehol.org/download/%{name}/releases/v%{version}/%{name}-%{version}.tar.gz
Source1:          %{name}.conf
Source2:          %{name}.sysconfig
Source3:          %{name}.init

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    libmnl-devel
BuildRequires:    zlib-devel
%if 0%{?rhel} >= 7
BuildRequires:    libnetfilter_acct-devel
BuildRequires:    systemd
%endif

Requires:         libmnl
Requires:         zlib

%if 0%{?rhel} >= 7
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%endif


################################################################################

%description
Real-time performance monitoring, in the greatest possible detail!

################################################################################

%prep
%setup -q -n %{name}-%{version}

%build
%configure \
        --docdir="%{_docdir}/%{name}-%{version}" \
        --with-zlib \
        --with-math \
        --with-user=%{service_user} \

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR="%{buildroot}"

find %{buildroot} -name .keep -exec rm -f {} \;

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 system/%{name}.service %{buildroot}/%{_unitdir}
%else
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}
%endif

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin -d %{service_home} %{service_user}
exit 0

%if 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add %{service_name}
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{service_name}
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE.md README.md
%config(noreplace) %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(-,%{service_user},%{service_group}) %dir %{_localstatedir}/cache/%{name}/
%attr(-,%{service_user},%{service_group}) %dir %{_localstatedir}/log/%{name}/
%attr(-,%{service_user},%{service_group}) %{_datadir}/%{name}/
%{_libexecdir}/%{name}/
%{_sbindir}/%{name}

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

################################################################################

%changelog
* Sun Apr 10 2016 Gleb Goncharov <yum@gongled.me> - 1.0.0-0
- Initial build 

