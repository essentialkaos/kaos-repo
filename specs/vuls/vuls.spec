################################################################################

# rpmbuilder:gopack    github.com/future-architect/vuls
# rpmbuilder:tag       v0.6.1

################################################################################

%define  debug_package %{nil}

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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define username          vuls
%define groupname         vuls

%define service_name      vuls-server
%define service_logdir    %{_logdir}/vuls

################################################################################

Summary:         VULnerability Scanner
Name:            vuls
Version:         0.6.1
Release:         0%{?dist}
Group:           Applications/System
License:         GPLv3
URL:             https://github.com/future-architect/vuls

Source0:         %{name}-%{version}.tar.bz2
Source1:         %{name}.toml
Source2:         %{service_name}.init
Source3:         %{service_name}.sysconfig
Source4:         %{service_name}.service

BuildRequires:   golang >= 1.11

Requires:        sqlite kaosv >= 2.15

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Vulnerability scanner for Linux/FreeBSD, agentless, written in golang.

################################################################################

%prep
%setup -q

mkdir -p .src ; cp -r * .src/ ; rm -rf * ; mv .src src

%build
export GOPATH=$(pwd)

export LD_FLAGS="-X github.com/future-architect/vuls/config.Version=%{version} -X github.com/future-architect/vuls/config.Revision=000000"

go build -ldflags "$LD_FLAGS" -o %{name} src/github.com/future-architect/vuls/main.go

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{service_logdir}

install -pm 755 %{name} %{buildroot}%{_bindir}/

install -pDm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.toml
install -pDm 755 %{SOURCE2} %{buildroot}%{_initddir}/%{service_name}
install -pDm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{service_name}

%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{service_name}.service
%endif

%clean
rm -rf %{buildroot}

################################################################################

%pre
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{groupname} &>/dev/null || %{__groupadd} -r %{groupname}
  %{__getent} passwd %{username} &>/dev/null || %{__useradd} -r -g %{groupname} -d %{_rundir}/%{name} -s /sbin/nologin %{username}
fi

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload %{service_name}.service &>/dev/null || :
  %{__systemctl} preset %{service_name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{service_name} &>/dev/null || :
%endif
fi

%postun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{service_name}.service &>/dev/null || :
  %{__systemctl} stop %{service_name}.service &>/dev/null || :
%else
  %{__service} stop %{service_name} &>/dev/null || :
%endif
fi

################################################################################

%files
%defattr(-,root,root,-)
%attr(0755,%{username},%{groupname}) %dir %{service_logdir}
%config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%config(noreplace) %{_sysconfdir}/%{name}.toml
%{_bindir}/%{name}
%{_initddir}/%{service_name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{service_name}.service
%endif

################################################################################

%changelog
* Tue Dec 11 2018 Anton Novojilov <andy@essentialkaos.com> - 0.6.1-0
- Initial build for kaos repository
