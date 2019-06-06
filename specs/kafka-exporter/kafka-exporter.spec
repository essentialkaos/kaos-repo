################################################################################

# rpmbuilder:gopack       github.com/danielqsj/kafka_exporter
# rpmbuilder:tag          v1.2.0

################################################################################

%define debug_package     %{nil}

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define pkg_name       kafka_exporter
%define service_user   kafka-exporter
%define service_group  kafka-exporter

################################################################################

Summary:          Kafka Exporter for Prometheus
Name:             kafka-exporter
Version:          1.2.0
Release:          0%{?dist}
Group:            Applications/Utilities
License:          ASL 2.0
URL:              https://github.com/danielqsj/kafka_exporter

Source0:          %{name}-%{version}.tar.gz
Source1:          %{name}.service
Source2:          %{name}.init
Source3:          %{name}.sysconfig
Source4:          %{name}.logrotate

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    golang >= 1.11

Requires:         logrotate

%if 0%{?rhel} >= 7
Requires:         systemd

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
Requires:         initscripts kaosv >= 2.15

Requires(pre):    shadow-utils
Requires(post):   %{__chkconfig}
Requires(preun):  %{__chkconfig} %{__service}
Requires(postun): %{__service}
%endif

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Kafka Exporter for Prometheus.

################################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src ; mv * .src ; mv .src src

%build
export GOPATH=$(pwd)

pushd src/github.com/danielqsj/%{pkg_name}
  %{__make} %{?_smp_mflags} build
popd

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 0755 %{buildroot}%{_logdir}/%{name}

%if 0%{?rhel} >= 7
  install -dm 0755 %{buildroot}%{_unitdir}
%else
  install -dm 0755 %{buildroot}%{_initrddir}
%endif

pushd src/github.com/danielqsj/%{pkg_name}

install -pm 755 %{pkg_name} %{buildroot}%{_bindir}/%{name}

install -pm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?rhel} >= 7
  install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
  install -pm 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

popd

%clean
rm -rf %{buildroot}

################################################################################

%pre
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || %{__useradd} -r \
    -g %{service_group} -d %{_sharedstatedir}/%{name} \
    -s /sbin/nologin %{service_user}

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} %{name} stop &>/dev/null || :
  %{__chkconfig} --del %{name} &>/dev/null || :
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
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755, %{service_user}, %{service_group}) %{_logdir}/%{name}

################################################################################

%changelog
* Wed Jun 05 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.2.0-0
- Initial build

