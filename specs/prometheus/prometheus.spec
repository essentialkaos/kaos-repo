################################################################################

%define debug_package  %{nil}

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

%define service_user   prometheus
%define service_group  prometheus

################################################################################

Summary:          Monitoring system and time series database
Name:             prometheus
Version:          2.5.0
Release:          0%{?dist}
Group:            Applications/Databases
License:          ASL 2.0
URL:              https://prometheus.io

Source0:          https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:          %{name}.service
Source2:          %{name}.init
Source3:          %{name}.sysconfig
Source4:          %{name}.logrotate

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    golang >= 1.10

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

Conflicts:        prometheus < 2.0

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
export GOPATH=$(pwd)
go get -v github.com/%{name}/%{name}/cmd/...

%{__make} %{?_smp_mflags} build

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 0755 %{buildroot}%{_datarootdir}/%{name}/consoles
install -dm 0755 %{buildroot}%{_datarootdir}/%{name}/console_libraries
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 0755 %{buildroot}%{_logdir}/%{name}

%if 0%{?rhel} >= 7
  install -dm 0755 %{buildroot}%{_unitdir}
%else
  install -dm 0755 %{buildroot}%{_initrddir}
%endif

install -pm 755 prometheus %{buildroot}%{_bindir}/%{name}
install -pm 755 promtool %{buildroot}%{_bindir}/promtool

for dir in consoles console_libraries; do
  for file in ${dir}/*; do
    install -pm 0644 ${file} %{buildroot}%{_datarootdir}/%{name}/${file}
  done
done

install -pm 0644 documentation/examples/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml
install -pm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?rhel} >= 7
  install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
  install -pm 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

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
%{_bindir}/promtool
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yml
%{_datarootdir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755, %{service_user}, %{service_group}) %{_sharedstatedir}/%{name}

################################################################################

%changelog
* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to the latest stable release

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Updated to the latest stable release

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Updated to the latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Updated to the latest stable release

* Tue Mar 27 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.2.1-0
- Initial build
