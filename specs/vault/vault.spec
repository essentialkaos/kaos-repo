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
Version:           1.0.1
Release:           0%{?dist}
Group:             Applications/Communications
License:           MPLv2
URL:               https://www.vaultproject.io

Source0:           https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz
Source1:           %{name}-agent.sysconfig
Source2:           %{name}-server.sysconfig
Source3:           %{name}-agent.init
Source4:           %{name}-server.init
Source5:           %{name}-agent.service
Source6:           %{name}-server.service
Source7:           %{name}-agent.conf
Source8:           %{name}-server.conf

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     golang >= 1.10

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

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires:           kaosv

Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts
%else
Requires:           systemd

BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%description agent
Vault Agent is a client daemon that can perform useful tasks.

################################################################################

%package server
Summary:            Vault Server
Group:              Applications/Communications

Requires:           %{name} = %{version}-%{release}

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires:           kaosv

Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts
%else
Requires:           systemd

BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%description server
The Vault server provides an API which clients interact with and manages the
interaction between all the secrets engines, ACL enforcement, and secret lease
revocation. Having a server based architecture decouples clients from the
security keys and policies, enables centralized audit logging and simplifies
administration for operators.

################################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src/github.com/hashicorp/%{name}
mv * .src/github.com/hashicorp/%{name}/
mv .src src

%build
export GOPATH=$(pwd)
export XC_OS=$(go env GOOS)
export XC_ARCH=$(go env GOARCH)
export GO15VENDOREXPERIMENT=1
export CGO_ENABLED=0
export GIT_IMPORT="github.com/hashicorp/%{name}/version"
export GOLDFLAGS="-X $GIT_IMPORT.GitDescribe=%{version}"

pushd src/github.com/hashicorp/%{name}
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
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
install -dm 755 %{buildroot}%{_initrddir}
%else
install -dm 755 %{buildroot}%{_unitdir}
%endif
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}-server
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}-agent

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-agent
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-server
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
install -pm 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-agent
install -pm 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-server
%else
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE6} %{buildroot}%{_unitdir}/
%endif
install -pm 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/%{name}/agent/config.hcl
install -pm 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/%{name}/server/config.hcl

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || \
    useradd -r -M -g %{service_group} -d %{service_home} \
            -s /sbin/nologin %{service_user}
exit 0

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

%post agent
if [[ $1 -eq 1 ]] ; then
    %{__chkconfig} --add %{name}-agent
fi

%preun agent
if [[ $1 -eq 0 ]] ; then
    %{__service} %{name}-agent stop &>/dev/null || :
    %{__chkconfig} --del %{name}-agent
fi

%post server
if [[ $1 -eq 1 ]] ; then
    %{__chkconfig} --add %{name}-server
fi

%preun server
if [[ $1 -eq 0 ]] ; then
    %{__service} %{name}-server stop &>/dev/null || :
    %{__chkconfig} --del %{name}-server
fi

%else

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

%endif

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%attr(0755,%{service_user},%{service_group}) %{service_home}

%files agent
%defattr(-,root,root,-)
%{_sysconfdir}/sysconfig/%{name}-agent
%attr(-,%{service_user},%{service_group}) %dir %{_rundir}/%{name}-agent
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%{_initrddir}/%{name}-agent
%else
%{_unitdir}/%{name}-agent.service
%endif
%attr(-,%{service_user},%{service_group}) %dir %{_localstatedir}/log/%{name}-agent/
%config(noreplace) %{_sysconfdir}/%{name}/agent/config.hcl

%files server
%defattr(-,root,root,-)
%{_sysconfdir}/sysconfig/%{name}-server
%attr(-,%{service_user},%{service_group}) %dir %{_rundir}/%{name}-server
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%{_initrddir}/%{name}-server
%else
%{_unitdir}/%{name}-server.service
%endif
%attr(-,%{service_user},%{service_group}) %dir %{_localstatedir}/log/%{name}-server/
%config(noreplace) %{_sysconfdir}/%{name}/server/config.hcl

################################################################################

%changelog
* Fri Jan 11 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.0.1-0
- Initial build

