###############################################################################

# rpmbuilder:gopack    github.com/future-architect/vuls
# rpmbuilder:tag       v0.3.0

###############################################################################

%define  debug_package %{nil}

###############################################################################

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

%define username          cved
%define groupname         cved
%define cved_dir          %{_opt}/cve-dictionary

###############################################################################

Summary:         VULnerability Scanner
Name:            vuls
Version:         0.3.0
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv3
URL:             https://github.com/future-architect/vuls

Source0:         %{name}-%{version}.tar.bz2
Source1:         go-cve-dictionary.tar.bz2
Source2:         cved-server.init
Source3:         cved-server.service
Source4:         cved-server.sysconfig
Source5:         cve-dictionary-fetch.cron
Source6:         cve-dictionary-fetch
Source10:        index.html

Patch0:          cve-dictionary-log-path.patch

BuildRequires:   golang >= 1.8

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        sqlite cve-dictionary

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Vulnerability scanner for Linux/FreeBSD, agentless, written in golang.

###############################################################################

%package -n cve-dictionary

Summary:         CVE data fetcher and server for VULS
Version:         0.1.1
Release:         0%{?dist}

Requires:        kaosv

%if 0%{?rhel} >= 7
Requires:        systemd
%endif

%description -n cve-dictionary
This is tool to build a local copy of the NVD (National Vulnerabilities 
Database) and the Japanese JVN [2], which contain security vulnerabilities 
according to their CVE identifiers [3] including exhaustive information and 
a risk score. The local copy is generated in sqlite format, and the tool has a 
server mode for easy querying.

###############################################################################

%prep
%setup -q

%{__tar} xjfv %{SOURCE1}

pushd go-cve-dictionary/github.com/kotakanbe/go-cve-dictionary/
%patch0 -p1
popd

rm -rf github.com/kotakanbe/go-cve-dictionary
cp -r go-cve-dictionary/* . ; rm -rf go-cve-dictionary
mkdir -p .src ; cp -r * .src/ ; rm -rf * ; mv .src src

%build
export GOPATH=$(pwd)

go build -o %{name} src/github.com/future-architect/vuls/main.go
go build -o go-cve-dictionary src/github.com/kotakanbe/go-cve-dictionary/main.go

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_logdir}/%{name}
install -dm 755 %{buildroot}%{cved_dir}/data
install -dm 755 %{buildroot}%{_logdir}/cve-dictionary

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 755 go-cve-dictionary %{buildroot}%{_bindir}/
install -pm 755 %{SOURCE6} %{buildroot}%{_bindir}/

ln -sf %{_bindir}/go-cve-dictionary %{buildroot}%{_bindir}/cve-dictionary

install -pDm 755 %{SOURCE2} %{buildroot}%{_initddir}/cved-server
install -pDm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/cved-server

%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE3} %{buildroot}%{_unitdir}/cved-server.service
%endif

install -pDm 644 %{SOURCE5} %{buildroot}%{_crondir}/cve-dictionary-fetch

install -pm 644 %{SOURCE10} %{buildroot}%{cved_dir}/
install -pm 644 src/github.com/future-architect/vuls/img/vuls_logo_large.png \
                %{buildroot}%{cved_dir}/logo.png

%clean
rm -rf %{buildroot}

%pre -n cve-dictionary
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{groupname} &>/dev/null || %{__groupadd} -r %{groupname}
  %{__getent} passwd %{username} &>/dev/null || %{__useradd} -r -g %{groupname} -d %{_rundir}/%{name} -s /sbin/nologin %{username}
fi

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload cved-server.service &>/dev/null || :
  %{__systemctl} preset cved-server.service &>/dev/null || :
%else
  %{__chkconfig} --add cved-server &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then 
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable cved-server.service &>/dev/null || :
  %{__systemctl} stop cved-server.service &>/dev/null || :
%else
  %{__service} stop cved-server &>/dev/null || :
%endif
fi 

%postun
if [[ $1 -ge 1 ]] ; then 
%if 0%{?rhel} >= 7
  %{__systemctl} try-restart cved-server.service &>/dev/null || :
%else
  %{__service} restart cved-server &>/dev/null || :
%endif
fi

###############################################################################

%files
%defattr(-,root,root,-)
%dir %{_logdir}/%{name}
%{_bindir}/%{name}

%files -n cve-dictionary
%defattr(-,root,root,-)
%attr(0755,%{username},%{groupname}) %dir %{_logdir}/cve-dictionary
%attr(0755,%{username},%{groupname}) %{cved_dir}
%config(noreplace) %{_sysconfdir}/cved-server
%config %{_crondir}/cve-dictionary-fetch
%{_initddir}/cved-server
%if 0%{?rhel} >= 7
%{_unitdir}/cved-server.service
%endif
%{_bindir}/go-cve-dictionary
%{_bindir}/cve-dictionary
%{_bindir}/cve-dictionary-fetch

###############################################################################

%changelog
* Fri May 12 2017 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- Updated to latest stable release

* Wed Jan 25 2017 Anton Novojilov <andy@essentialkaos.com> - 0.2.0-1
- Improved spec

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.2.0-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.1.7-0
- Updated to latest stable release

* Thu Oct 06 2016 Anton Novojilov <andy@essentialkaos.com> - 0.1.6-0
- Initial build for kaos repository
