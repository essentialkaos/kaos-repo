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
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define buildpkg github.com/grafana/loki/pkg/build

%define service_user      loki
%define service_group     loki
%define service_home      %{_sharedstatedir}/%{name}

################################################################################

Summary:          Loki: like Prometheus, but for logs
Name:             loki
Version:          2.1.0
Release:          0%{?dist}
Group:            Development/Tools
License:          Apache-2.0
URL:              https://grafana.com/loki

Source0:          https://github.com/grafana/%{name}/archive/v%{version}.tar.gz
Source1:          loki.service
Source2:          loki.sysconfig
Source3:          loki.yaml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    golang >= 1.15

Requires:         systemd

BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

################################################################################

%description
Loki is a horizontally-scalable, highly-available, multi-tenant log
aggregation system inspired by Prometheus.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build

export CGO_ENABLED=0
export GOFLAGS="-mod=vendor -buildmode=pie -tags=netgo"
export GOLDFLAGS="-s -w -X %{buildpkg}.Version=%{version} \
                        -X %{buildpkg}.Revision=%{release} \
                        -X %{buildpkg}.Branch=Unknown \
                        -X %{buildpkg}.BuildUser=Unknown \
                        -X %{buildpkg}.BuildDate=Unknown"

go build -ldflags="$GOLDFLAGS" ./cmd/%{name}

%install
rm -rf %{buildroot}

# Directories
install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sysconfdir}
install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_sharedstatedir}
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}

# Service files
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/loki.service
install -pm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/loki

# Configurations
install -pm 0644 %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}.yaml

# Binaries
install -pm 0755 loki %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} &>/dev/null || groupadd -r %{service_group} &>/dev/null
getent passwd %{service_user} &>/dev/null || \
    useradd -r -g %{service_group} -d %{service_home} -s /sbin/nologin \
    -c "%{service_user} user account" %{service_user} &>/dev/null

%post
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0755, %{service_user}, %{service_group}) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yaml
%{_unitdir}/%{name}.service

################################################################################

%changelog
* Wed Jan 20 2021 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.1.0-0
- Initial build
