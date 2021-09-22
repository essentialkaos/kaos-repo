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

%define  debug_package %{nil}

%define  service_user  %{name}
%define  service_group %{name}
%define  service_home  %{_sharedstatedir}/%{name}

################################################################################

Summary:           Tool for managing secrets and protecting sensitive data
Name:              vault
Version:           1.8.2
Release:           0%{?dist}
Group:             Applications/Communications
License:           MPL-2.0
URL:               https://www.vaultproject.io

Source0:           https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz
Source1:           %{name}-agent.sysconfig
Source2:           %{name}-server.sysconfig
Source3:           %{name}-agent.service
Source4:           %{name}-server.service
Source5:           %{name}-agent.conf
Source6:           %{name}-server.conf

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     golang >= 1.16

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Vault secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing.

################################################################################

%package agent
Summary:            Vault Agent
Group:              Applications/Communications

Requires:           %{name} = %{version}-%{release}

Requires:           systemd
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description agent
Vault Agent is a client daemon that can perform useful tasks.

################################################################################

%package server
Summary:            Vault Server
Group:              Applications/Communications

Requires:           %{name} = %{version}-%{release}

Requires:           systemd
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description server
The Vault server provides an API which clients interact with and manages the
interaction between all the secrets engines, ACL enforcement, and secret lease
revocation. Having a server based architecture decouples clients from the
security keys and policies, enables centralized audit logging and simplifies
administration for operators.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

mkdir -p .src/github.com/hashicorp/%{name}
mv * .src/github.com/hashicorp/%{name}/
mv .src src

%build
export GOPATH=$(pwd)
export XC_OS=$(go env GOOS)
export XC_ARCH=$(go env GOARCH)
export CGO_ENABLED=0
export GO111MODULE=auto
export GIT_IMPORT="github.com/hashicorp/%{name}/version"
export GOLDFLAGS="-X $GIT_IMPORT.GitDescribe=%{version}"

pushd src/github.com/hashicorp/%{name}
  sed -i '/replace git.apache.org/d' go.mod

  %{__make} %{?_smp_mflags} bootstrap || :
  $GOPATH/bin/gox -osarch="${XC_OS}/${XC_ARCH}" \
                  -ldflags "${GOLDFLAGS}" \
                  -tags="%{name}" \
                  -output "$GOPATH/%{name}" .
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/server
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/agent
install -dm 755 %{buildroot}%{_rundir}/%{name}-agent
install -dm 755 %{buildroot}%{_rundir}/%{name}-server
install -dm 755 %{buildroot}%{service_home}
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_logdir}/%{name}-server
install -dm 755 %{buildroot}%{_logdir}/%{name}-agent

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-agent
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-server
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{name}/agent/config.hcl
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}/server/config.hcl

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

%post agent
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} enable %{name}-agent.service &>/dev/null || :
fi

%preun agent
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}-agent.service &>/dev/null || :
  %{__systemctl} stop %{name}-agent.service &>/dev/null || :
fi

%postun agent
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

%files agent
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/agent/config.hcl
%{_sysconfdir}/sysconfig/%{name}-agent
%attr(-,%{service_user},%{service_group}) %dir %{_rundir}/%{name}-agent
%attr(-,%{service_user},%{service_group}) %dir %{_logdir}/%{name}-agent
%{_unitdir}/%{name}-agent.service


%files server
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/server/config.hcl
%{_sysconfdir}/sysconfig/%{name}-server
%attr(-,%{service_user},%{service_group}) %dir %{_rundir}/%{name}-server
%attr(-,%{service_user},%{service_group}) %dir %{_logdir}/%{name}-server
%{_unitdir}/%{name}-server.service

################################################################################

%changelog
* Wed Sep 22 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.2-0
- Updated to the latest stable release

* Mon Feb 1 2021 Andrey Kulikov <avk@brewkeeper.net> - 1.6.2-0
- Updated to the latest stable release

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- Updated to the latest stable release

* Fri Jan 11 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.0.1-0
- Initial build
