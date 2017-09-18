###############################################################################

%define python_version %(%{__python} -c "import sys; sys.stdout.write(sys.version[:3])")

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

%define service_user      syslog-ng
%define service_group     syslog-ng

###############################################################################

Summary:            Next generation logging application
Name:               syslog-ng
Version:            3.11.1
Release:            0%{?dist}
License:            GPL
Group:              System Environment/Daemons
URL:                https://github.com/balabit/syslog-ng

Source0:            https://github.com/balabit/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:            %{name}.sysconfig
Source2:            %{name}.init

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           kaosv >= 2.9 pcre openssl json-c
Requires:           eventlog libhiredis libnet GeoIP

BuildRequires:      make gcc bison flex glib2-devel pkgconfig pcre-devel
BuildRequires:      openssl-devel libnet-devel eventlog-devel
BuildRequires:      libhiredis-devel json-c-devel chrpath

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
The syslog-ng application is a flexible and highly scalable system logging 
tool. It is often used to manage log messages and implement centralized 
logging, where the aim is to collect the log messages of several devices to a 
single, central log server.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%build
./configure --bindir=%{_bindir} \
            --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir}/%{name} \
            --disable-python \
            --enable-spoof-source \
            --enable-json \
            --enable-redis

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} DESTDIR="%{buildroot}"

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 755 %{buildroot}%{_initrddir}

install -pm 644 %{SOURCE1} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -pm 755 %{SOURCE2} \
                %{buildroot}%{_initrddir}/%{name}

install -pm 644 contrib/rhel-packaging/%{name}.logrotate \
                %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%ifarch x86_64
chrpath --delete %{buildroot}%{_loc_libdir32}/%{name}/*.so \
                 %{buildroot}%{_sbindir}/%{name} \
                 %{buildroot}%{_sbindir}/%{name}-ctl \
                 %{buildroot}%{_bindir}/loggen \
                 %{buildroot}%{_bindir}/dqtool \
                 %{buildroot}%{_bindir}/pdbtool \
                 %{buildroot}%{_libdir}/*.so*
%else
chrpath --delete %{buildroot}%{_loc_libdir}/%{name}/*.so \
                 %{buildroot}%{_sbindir}/%{name} \
                 %{buildroot}%{_sbindir}/%{name}-ctl \
                 %{buildroot}%{_bindir}/loggen \
                 %{buildroot}%{_bindir}/dqtool \
                 %{buildroot}%{_bindir}/pdbtool \
                 %{buildroot}%{_libdir}/*.so*
%endif

%clean
rm -rf %{buildroot}

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin -d / %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add %{name}
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop > /dev/null 2>&1
fi

%postun
if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --del %{name} > /dev/null 2>&1
fi

###############################################################################

%files
%defattr(-,root,root,-)
%doc NEWS.md AUTHORS COPYING VERSION
%attr(755,%{service_user},%{service_group}) %dir %{_rundir}/%{name}
%attr(755,%{service_user},%{service_group}) %dir %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}-ctl
%{_sbindir}/%{name}-debun
%{_bindir}/loggen
%{_bindir}/dqtool
%{_bindir}/pdbtool
%{_bindir}/update-patterndb
%{_libdir}/*
%ifarch x86_64
%{_loc_libdir32}/%{name}/*
%else
%{_loc_libdir}/%{name}/*
%endif
%{_includedir}/%{name}/*
%{_datadir}/*

###############################################################################

%changelog
* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.11.1-0
- Updated to latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.10.1-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.9.1-0
- Updated to latest stable release

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 3.8.1-0
- Updated to latest stable release
- Improved init script

* Wed Apr 27 2016 Gleb Goncharov <yum@gongled.ru> - 3.7.3-1
- Added directory to store persist-file.
- Added support of running syslog-ng as non-root user.

* Mon Apr 25 2016 Gleb Goncharov <yum@gongled.ru> - 3.7.3-0
- Updated to latest stable release
- Fixed 'restart' handler in SysV init-script

* Mon Mar 21 2016 Gleb Goncharov <yum@gongled.ru> - 3.7.2-0
- Initial build

