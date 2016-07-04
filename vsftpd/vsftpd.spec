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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

%define service_user         vsftp
%define service_group        vsftp
%define service_name         %{name}
%define service_home         %{_localstatedir}/ftp

###############################################################################

Summary:              Very Secure FTP Daemon
Name:                 vsftpd
Version:              3.0.3
Release:              1%{?dist}
License:              GPL
Group:                System Environment/Daemons
URL:                  http://vsftpd.beasts.org

Source0:              https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
Source1:              %{name}.init
Source2:              %{name}.conf
Source3:              %{name}.logrotate
Source4:              %{name}.sysconfig
Source5:              %{name}.pam
Source6:              %{name}.user_list

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             openssl logrotate kaosv >= 2.7.0

BuildRequires:        gcc-c++ openssl-devel libcap-devel grep

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
vsftpd is a Very Secure FTP daemon. It was written completely from 
scratch.

###############################################################################

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sbindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/pam.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_mandir}/man5
install -dm 755 %{buildroot}%{_mandir}/man8
install -dm 755 %{buildroot}%{service_home}
install -dm 755 %{buildroot}%{_logdir}/%{name}

install -pm 755 %{name} \
                %{buildroot}%{_sbindir}/%{name}
install -pm 600 %{name}.conf \
                %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pm 644 %{name}.conf.5 \
                %{buildroot}%{_mandir}/man5/%{name}.conf.5
install -pm 644 %{name}.8 \
                %{buildroot}%{_mandir}/man8/%{name}.8

install -pm 755 %{SOURCE1} \
                %{buildroot}%{_initrddir}/%{service_name}
install -pm 644 %{SOURCE2} \
                %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pm 644 %{SOURCE3} \
                %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE4} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE5} \
                %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -pm 644 %{SOURCE6} \
                %{buildroot}%{_sysconfdir}/%{name}/%{name}.user_list

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} \
    -s /sbin/nologin -d %{service_home} %{service_user}
exit 0

%post
if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --add %{service_name}
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop
  %{__chkconfig} --del %{service_name}
fi

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD
%doc SPEED TODO BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE 
%dir %{_sysconfdir}/%{name}
%attr(600,root,root) %dir %{_logdir}/%{name}
%attr(555,%{service_user},%{service_group}) %dir %{service_home}
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.*
%config %{_sysconfdir}/sysconfig/%{name}
%config %{_sysconfdir}/logrotate.d/%{name}
%config %{_sysconfdir}/pam.d/%{name}
%{_initrddir}/%{service_name}
%{_sbindir}/%{name}
%{_mandir}/man5/*
%{_mandir}/man8/*

###############################################################################

%changelog
* Fri Jul 01 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 3.0.3-1
- Added vsftpd.user_list
- Added PAM configuration
- Disabled tcp_wrapper by default

* Sun Mar 13 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.3-0
- Initial build

