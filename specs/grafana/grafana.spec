################################################################################

%define debug_package  %{nil}

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

%define service_user  %{name}
%define service_group %{name}
%define service_home  %{_datadir}/%{name}

################################################################################

Summary:              Metrics dashboard and graph editor
Name:                 grafana
Version:              6.2.5
Release:              0%{?dist}
License:              ASL 2.0
Group:                Applications/System
URL:                  https://grafana.org

Source0:              https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:              %{name}-assets-%{version}.tar.bz2

Source10:             %{name}-tmpfiles.conf

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:               000-%{name}-fhs-fix.patch
Patch1:               001-%{name}-clickhouse-alerting.patch

%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
Requires(pre):        shadow-utils
%else
Requires(pre):        shadow-utils
Requires(post):       chkconfig
Requires(preun):      chkconfig
Requires(preun):      initscripts
Requires(postun):     initscripts
%endif

%if 0%{?rhel} >= 7
BuildRequires:        systemd
%endif

BuildRequires:        gcc golang >= 1.11

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

################################################################################

%prep
%setup -q
%setup -q -T -D -a 1

%patch0 -p1
%patch1 -p1

%build
mkdir -p %{_builddir}/src/github.com/%{name}

ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/%{name}/%{name}

rm -f %{_builddir}/src/github.com/%{name}/%{name}/public/sass/.sass-lint.yml
rm -f %{_builddir}/src/github.com/%{name}/%{name}/public/test/.jshintrc

export GOPATH=%{_builddir}:%{gopath}

pushd %{_builddir}/src/github.com/%{name}/%{name}
  go run build.go build
popd

%install
rm -rf %{buildroot}

[[ ! -d bin/x86_64 ]]  && ln -sf linux-amd64 bin/x86_64
[[ ! -d bin/i386 ]]    && ln -sf linux-386 bin/i386
[[ ! -d bin/ppc64le ]] && ln -sf linux-ppc64le bin/ppc64le
[[ ! -d bin/s390x ]]   && ln -sf linux-s390x bin/s390x
[[ ! -d bin/arm ]]     && ln -sf linux-arm bin/arm
[[ ! -d bin/arm64 ]]   && ln -sf linux-arm64 bin/aarch64
[[ ! -d bin/aarch64 ]] && ln -sf linux-aarch64 bin/aarch64

install -dm 0755 %{buildroot}%{_sbindir}
install -dm 0755 %{buildroot}%{service_home}
install -dm 0755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}/plugins
install -dm 0755 %{buildroot}%{_mandir}/man1
install -dm 0755 %{buildroot}%{_localstatedir}/log/%{name}
%if 0%{?rhel} >= 7
install -dm 0744 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_tmpfilesdir}
%else
install -dm 0755 %{buildroot}%{_initrddir}
%endif

cp -a conf public %{buildroot}%{service_home}

install -pm 0755 bin/%{_arch}/%{name}-cli %{buildroot}%{_sbindir}
install -pm 0755 bin/%{_arch}/%{name}-server %{buildroot}%{_sbindir}
install -pm 0644 docs/man/man1/* %{buildroot}%{_mandir}/man1
install -pm 0644 conf/distro-defaults.ini %{buildroot}%{_sysconfdir}/%{name}/%{name}.ini
install -pm 0644 conf/distro-defaults.ini %{buildroot}%{service_home}/conf/defaults.ini
install -pm 0644 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -pm 0644 packaging/rpm/sysconfig/%{name}-server %{buildroot}%{_sysconfdir}/sysconfig/%{name}-server
%if 0%{?rhel} >= 7
install -pm 0644 %{SOURCE10} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -pm 0644 packaging/rpm/systemd/%{name}-server.service %{buildroot}%{_unitdir}/%{name}-server.service
%else
install -pm 0755 packaging/rpm/init.d/%{name}-server %{buildroot}%{_initrddir}/%{name}-server
%endif

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
  %{__service} %{name} stop &> /dev/null || :
  %{__chkconfig} --del %{name} &> /dev/null || :
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
%defattr(-,root,root,0755)
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md UPGRADING_DEPENDENCIES.md
%doc LICENSE
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%dir %{_sysconfdir}/%{name}
%dir %{_sharedstatedir}/%{name}
%dir %{service_home}
%dir %{service_home}/conf
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/%{name}
%config(noreplace) %attr(0640,root,%{service_group}) %{_sysconfdir}/%{name}/%{name}.ini
%config(noreplace) %attr(0640,root,%{service_group}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server
%if 0%{?rhel} >= 7
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}-server.service
%else
%{_initrddir}/%{name}-server
%endif
%{service_home}/public
%attr(-,%{service_user},%{service_group}) %{_sharedstatedir}/%{name}
%attr(-,root,%{service_group}) %{service_home}/conf/*
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man1/%{name}-cli.1*

################################################################################

%changelog
* Tue Jul 09 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.2.5-0
- Updated to the latest release

* Tue Apr 16 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.1.3-0
- Updated to the latest release

* Mon Apr 15 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.0.2-0
- Initial build
