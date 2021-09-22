################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define debug_package %{nil}

%define service_user  %{name}
%define service_group %{name}
%define service_home  %{_sharedstatedir}/%{name}

################################################################################

Summary:           Tool for service discovery, monitoring and configuration
Name:              consul
Version:           1.10.2
Release:           0%{?dist}
Group:             Applications/Communications
License:           MPL-2.0
URL:               https://www.consul.io

Source0:           https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz
Source1:           %{name}-client.sysconfig
Source2:           %{name}-server.sysconfig
Source3:           %{name}-client.service
Source4:           %{name}-server.service
Source5:           %{name}-client.conf
Source6:           %{name}-server.conf

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     golang >= 1.17

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Consul is a tool for service discovery and configuration. Consul is
distributed, highly available, and extremely scalable.

################################################################################

%package client
Summary:            Consul Client
Group:              Applications/Communications

Requires:           %{name} = %{version}-%{release}
Requires:           systemd

BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description client
A client is an agent that forwards all RPCs to a server. The client is
relatively stateless. The only background activity a client performs is taking
part in the LAN gossip pool. This has a minimal resource overhead and consumes
only a small amount of network bandwidth.

################################################################################

%package server
Summary:            Consul Server
Group:              Applications/Communications

Requires:           %{name} = %{version}-%{release}
Requires:           systemd

BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description server
A server is an agent with an expanded set of responsibilities including
participating in the Raft quorum, maintaining cluster state, responding to RPC
queries, exchanging WAN gossip with other datacenters, and forwarding queries
to leaders or remote datacenters.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

mkdir -p .src/github.com/hashicorp/%{name}
mv * .src/github.com/hashicorp/%{name}/
mv .src src

%build
export GOPATH=$(pwd)
export CGO_ENABLED=0
export GO111MODULE=auto
export GIT_IMPORT="github.com/hashicorp/consul/version"
export GOLDFLAGS="-X $GIT_IMPORT.GitDescribe=%{version}"

pushd src/github.com/hashicorp/%{name}
  %{__make} %{?_smp_mflags} tools || :
  go build -ldflags "${GOLDFLAGS}" \
           -tags="consul" \
           -o "$GOPATH/%{name}" main.go
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/server
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/client
install -dm 755 %{buildroot}%{_rundir}/%{name}-client
install -dm 755 %{buildroot}%{_rundir}/%{name}-server
install -dm 755 %{buildroot}%{service_home}
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_logdir}/%{name}-server
install -dm 755 %{buildroot}%{_logdir}/%{name}-client

install -pm 755 %{name} %{buildroot}%{_bindir}/

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-client
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-server
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{name}/client/config.json
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}/server/config.json

%clean
# Fix permissions for files and directories in modules dir
find pkg -type d -exec chmod 0755 {} \;
find pkg -type f -exec chmod 0644 {} \;

rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || \
    useradd -r -M -g %{service_group} -d %{service_home} \
            -s /sbin/nologin %{service_user}
exit 0

%post client
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} enable %{name}-client.service &>/dev/null || :
fi

%preun client
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}-client.service &>/dev/null || :
  %{__systemctl} stop %{name}-client.service &>/dev/null || :
fi

%postun client
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi

%post server
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} enable %{name}-server.service &>/dev/null || :
fi

%preun server
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}-server.service &>/dev/null || :
  %{__systemctl} stop %{name}-server.service &>/dev/null || :
fi

%postun server
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%attr(0755,%{service_user},%{service_group}) %{service_home}
%{_bindir}/%{name}

%files client
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/client/config.json
%attr(-,%{service_user},%{service_group}) %dir %{_logdir}/%{name}-client/
%{_sysconfdir}/sysconfig/%{name}-client
%{_unitdir}/%{name}-client.service

%files server
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/server/config.json
%attr(-,%{service_user},%{service_group}) %dir %{_logdir}/%{name}-server
%{_sysconfdir}/sysconfig/%{name}-server
%{_unitdir}/%{name}-server.service

################################################################################

%changelog
* Wed Sep 22 2021 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- Updated to the latest stable release

* Mon Feb 1 2021 Andrey Kulikov <avk@brewkeeper.net> - 1.9.2-0
- Updated to the latest stable release

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.6.2-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Updated to the latest stable release

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Updated to the latest stable release

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- Updated to the latest stable release

* Tue Oct 23 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.3.0-0
- Updated to the latest stable release

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.3-0
- Updated to the latest stable release

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.2-0
- Updated to the latest stable release

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to the latest stable release

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.6-0
- Updated to the latest stable release

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Updated to the latest stable release

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to the latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Updated to the latest stable release

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 0.8.5-0
- Updated to the latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to the latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.5-0
- Updated to the latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.2-0
- Updated to the latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.0-0
- Updated to the latest stable release

* Tue Mar 22 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.4-0
- Updated to the latest stable release

* Thu Mar 10 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.3-0
- Initial build
