################################################################################

%define __jar_repack                       0
%define __find_requires                    %{nil}
%define _use_internal_dependency_generator 0
%define __find_provides                    %{nil}
%define debug_package                      %{nil}

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
%define _sysctldir        %{_sysconfdir}/sysctl.d
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
%define __sysctl          %{_sbindir}/sysctl
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define sonar_name       sonar-application
%define short_name       sonar
%define sonar_prefix     %{_opt}/%{name}-%{version}

%define service_user     sonarqube
%define service_group    sonarqube

################################################################################

Summary:              SonarQube Continuous Inspection
Name:                 sonarqube
Version:              7.9.1
Release:              0%{?dist}
License:              LGPLv3
Group:                System Environment/Daemons
URL:                  https://www.sonarqube.org/

Source0:              https://github.com/SonarSource/%{name}/archive/%{version}.tar.gz
Source1:              %{name}.service
Source2:              %{name}.properties
Source3:              %{name}.sysctl

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        java-11-openjdk java-11-openjdk-devel

Requires:             java-11-openjdk java-11-openjdk-headless

Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd

Provides:             %{name} = %{version}-%{release}

ExclusiveArch:        x86_64

################################################################################

%description
SonarQube provides the capability to not only show health of an application but
also to highlight issues newly introduced. With a Quality Gate in place, you
can fix the leak and therefore improve code quality systematically.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
./gradlew build -DbuildNumber=1 -x test

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_opt}
install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_sysctldir}
install -dm 0755 %{buildroot}%{_logdir}/%{name}
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}/data
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}/temp

pushd %{sonar_name}/build/distributions
  unzip %{sonar_name}-%{version}.zip -d %{buildroot}%{_opt}
  ln -sf %{sonar_prefix} %{buildroot}%{_opt}/%{name}
popd

rm -rf %{buildroot}%{sonar_prefix}/bin/windows-x86-64
rm -rf %{buildroot}%{sonar_prefix}/bin/macosx-universal-64

ln -sf %{_logdir}/%{name} %{buildroot}%{sonar_prefix}/logs

install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -pm 0644 %{SOURCE2} %{buildroot}%{sonar_prefix}/conf/%{short_name}.properties
install -pm 0644 %{SOURCE3} %{buildroot}%{_sysctldir}/%{name}.conf

%clean
rm -rf %{buildroot}

################################################################################

%pre
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
  %{__getent} passwd %{service_user} >/dev/null || \
              %{__useradd} -M -n -g %{service_user} -r -d %{sonar_prefix} -s /sbin/nologin %{service_user}
fi

%post
%systemd_post %{name}.service
%sysctl -p

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%sysctl -p

################################################################################

%files
%defattr(-,root,root)
%{_opt}/%{name}
%{_sysctldir}/%{name}.conf
%attr(0750,%{service_user},%{service_group}) %{_sharedstatedir}/%{name}/data
%attr(0750,%{service_user},%{service_group}) %{_sharedstatedir}/%{name}/temp
%attr(0755,%{service_user},%{service_group}) %{_logdir}/%{name}
%doc %{sonar_prefix}/COPYING
%config(noreplace) %attr(0644,%{service_user},%{service_group}) %{sonar_prefix}/conf/%{short_name}.properties
%attr(0644,%{service_user},%{service_group}) %{sonar_prefix}/conf/wrapper.conf
%{_unitdir}/%{name}.service
%attr(0755,%{service_user},%{service_group}) %{sonar_prefix}/bin/
%attr(0755,%{service_user},%{service_group}) %{sonar_prefix}/data/
%attr(0755,%{service_user},%{service_group}) %{sonar_prefix}/temp/
%{sonar_prefix}/elasticsearch/
%attr(0755,%{service_user},%{service_group}) %{sonar_prefix}/extensions/
%{sonar_prefix}/lib/
%attr(0755,%{service_user},%{service_group}) %{sonar_prefix}/logs/
%{sonar_prefix}/web/

################################################################################

%changelog
* Wed Dec 25 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 7.9.1-0
- Initial build.
