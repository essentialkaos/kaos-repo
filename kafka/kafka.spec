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
%define _datadir          %{_localstatedir}/lib
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _logrotatedir     %{_sysconfdir}/logrotate.d
%define _sysconfigdir     %{_sysconfdir}/sysconfig
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

################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

%define major_version     2.11
%define user_name         kafka
%define group_name        kafka
%define service_name      kafka
%define home_dir          %{_opt}/%{name}

################################################################################

Summary:             A high-throughput distributed messaging system
Name:                kafka
Version:             1.0.0
Release:             0%{?dist}
License:             APL v2
Group:               Applications/Databases
URL:                 https://kafka.apache.org

Source0:             https://github.com/apache/%{name}/archive/%{version}.tar.gz
Source1:             %{name}.init
Source2:             %{name}.conf
Source3:             %{name}.logrotate
Source4:             %{name}.sysconfig

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:           noarch

Requires:            kaosv

BuildRequires:       jdk8 gradle

Requires(post):      %{__chkconfig} initscripts
Requires(pre):       %{__chkconfig} initscripts

Provides:            %{name} = %{version}-%{release}

################################################################################

%description
Apache Kafka is a distributed publish-subscribe messaging system. It
is designed to support the following:

* Persistent messaging with O(1) disk structures that provide constant
  time performance even with many TB of stored messages.
* High-throughput: even with very modest hardware Kafka can support
  hundreds of thousands of messages per second.
* Explicit support for partitioning messages over Kafka servers and
  distributing consumption over a cluster of consumer machines while
  maintaining per-partition ordering semantics.
* Support for parallel data load into Hadoop.

################################################################################

%prep
%setup -q

%build
export PATH=$PATH:/opt/gradle/current/bin
gradle releaseTarGz

pushd core/build/distributions
  tar xvfz %{name}_%{major_version}-%{version}.tgz
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_opt}/%{name}
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/%{name}
install -dm 755 %{buildroot}%{_logrotatedir}
install -dm 755 %{buildroot}%{_sysconfigdir}

install -Dm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -Dm 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}
install -pm 644 %{SOURCE3} %{buildroot}%{_logrotatedir}/%{name}
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfigdir}/%{name}

pushd core/build/distributions/%{name}_%{major_version}-%{version}
  mv bin %{buildroot}%{_opt}/%{name}
  mv libs %{buildroot}%{_opt}/%{name}
  mv config %{buildroot}%{_opt}/%{name}
popd

%clean
rm -rf %{buildroot}

%pre
getent group %{group_name} >/dev/null || %{__groupadd} -r %{group_name}
getent passwd %{user_name} >/dev/null || %{__useradd} -s /sbin/nologin -M -r -g %{group_name} -d %{home_dir} %{user_name}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add %{service_name}
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{service_name}
fi

################################################################################

%files
%defattr(-,%{user_name},%{group_name},-)
%dir %{_datadir}/%{name}
%dir %{_logdir}/%{name}
%dir %{_localstatedir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{home_dir}

%defattr(-,root,root,-)
%{_initrddir}/%{name}
%config(noreplace) %{_logrotatedir}/%{name}
%config(noreplace) %{_sysconfigdir}/%{name}

################################################################################

%changelog
* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to latest release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.11.0.1-0
- Updated to latest release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.11.0.0-0
- Updated to latest release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.2.1-0
- Updated to latest release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.2.0-0
- Updated to latest release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.10.1.1-0
- Updated to latest release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.1.0-0
- Updated to latest release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0.1-0
- Updated to latest release

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0.0-0
- Updated to latest release

* Fri Apr 01 2016 Gleb Goncharov <ggoncharov@fun-box.ru> - 0.9.0.1-0
- Updated to latest release

* Thu Jun 25 2015 Anton Novojilov <anovojilov@fun-box.ru> - 0.8.2.1-0
- Initial build
