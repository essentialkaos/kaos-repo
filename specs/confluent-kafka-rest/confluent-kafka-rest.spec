################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack %{nil}

################################################################################

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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define pkg_name          kafka-rest
%define pkg_homedir       %{_datadir}/%{name}

%define service_user      kafka-rest
%define service_group     kafka-rest

################################################################################

Summary:            Confluent REST Proxy for Kafka
Name:               confluent-kafka-rest
Version:            6.0.0
Release:            0%{?dist}
License:            ASL 2.0
Group:              Development/Tools
URL:                https://docs.confluent.io/current/kafka-rest/docs/index.html

Source0:            https://github.com/confluentinc/%{pkg_name}/archive/v%{version}.tar.gz
Source1:            %{pkg_name}.service
Source2:            %{pkg_name}.init
Source3:            %{pkg_name}.sysconfig
Source4:            %{pkg_name}.logrotate

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           jdk11
Requires:           confluent-common = %{version}-%{release}
Requires:           confluent-rest-utils = %{version}-%{release}
Requires:           logrotate
%if 0%{?rhel} >= 7
Requires:           systemd
%else
Requires:           kaosv >= 2.15 initscripts
%endif

BuildRequires:      jdk11 maven git

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
The Kafka REST Proxy provides a RESTful interface to a Kafka cluster. It makes
it easy to produce and consume messages, view the state of the cluster, and
perform administrative actions without using the native Kafka protocol or
clients.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkg_name}-%{version}

%build

%install
rm -rf %{buildroot}

mvn -Dmaven.test.skip=true install

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{pkg_name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_datadir}/java/%{pkg_name}-bin
install -dm 755 %{buildroot}%{_datadir}/java/%{pkg_name}-lib
install -dm 755 %{buildroot}%{_datadir}/doc/%{pkg_name}-%{version}
install -dm 755 %{buildroot}%{_logdir}/%{pkg_name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
%else
install -dm 755 %{buildroot}%{_initrddir}
%endif

pushd %{pkg_name}/target/%{pkg_name}-%{version}-package
  cp -a share/java/%{pkg_name}-bin/*.jar %{buildroot}%{_datadir}/java/%{pkg_name}-bin/
  cp -a share/java/%{pkg_name}-lib/*.jar %{buildroot}%{_datadir}/java/%{pkg_name}-lib/
  cp -a share/doc/%{pkg_name}/* %{buildroot}%{_datadir}/doc/%{pkg_name}-%{version}/
  cp -a bin/* %{buildroot}%{_bindir}
  cp -a etc/%{pkg_name}/* %{buildroot}%{_sysconfdir}/%{pkg_name}/
popd

mv %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.properties \
   %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.conf

%if 0%{?rhel} >= 7
install -pm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{pkg_name}.service
%else
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{pkg_name}
%endif

install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{pkg_name}
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} &> /dev/null || groupadd -r %{service_group} &> /dev/null
getent passwd %{service_user} &> /dev/null || \
useradd -r -g %{service_group} -d /tmp -s /sbin/nologin \
        -c 'Confluent Kafka REST Proxy' %{service_user} &> /dev/null

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} enable %{pkg_name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{pkg_name}
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{pkg_name}.service &>/dev/null || :
  %{__systemctl} stop %{pkg_name}.service &>/dev/null || :
%else
  %{__service} %{pkg_name} stop &>/dev/null || :
  %{__chkconfig} --del %{pkg_name}
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_datadir}/java/%{pkg_name}-bin
%dir %{_datadir}/java/%{pkg_name}-lib
%dir %{_datadir}/doc/%{pkg_name}-%{version}
%attr(755,%{service_user},%{service_group}) %dir %{_logdir}/%{pkg_name}
%{_bindir}/%{pkg_name}-run-class
%{_bindir}/%{pkg_name}-start
%{_bindir}/%{pkg_name}-stop
%{_bindir}/%{pkg_name}-stop-service
%{_datadir}/java/%{pkg_name}-bin/*.jar
%{_datadir}/java/%{pkg_name}-lib/*.jar
%{_datadir}/doc/%{pkg_name}-%{version}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{pkg_name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%config(noreplace) %attr(640,%{service_user},%{service_group}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}.conf
%config(noreplace) %attr(640,%{service_user},%{service_group}) %{_sysconfdir}/%{pkg_name}/log4j.properties
%if 0%{?rhel} >= 7
%{_unitdir}/%{pkg_name}.service
%else
%{_initrddir}/%{pkg_name}
%endif

################################################################################

%changelog
* Mon Feb 15 2021 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.0.0-0
- Updated to the latest release

* Wed Jan 15 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 5.4.0-0
- Initial build
