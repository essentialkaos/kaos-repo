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

################################################################################

%define pkg_name          apache-maven
%define pkg_major_ver     3
%define pkg_homedir       %{_datadir}/%{name}
%define pkg_confdir       %{_sysconfdir}/%{name}

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            Java project management and project comprehension tool
Name:               maven
Version:            3.6.1
Release:            0%{?dist}
License:            ASL 2.0 and MIT
Group:              Development/Tools
URL:                https://maven.apache.org/

Source0:            http://apache-mirror.rbc.ru/pub/apache/%{name}/%{name}-%{pkg_major_ver}/%{version}/source/%{pkg_name}-%{version}-src.tar.gz
Source1:            %{name}-bash-completion

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           java >= 1.7.0
Requires:           %{name}-lib = %{version}-%{release}

BuildRequires:      java >= 1.7.0 java-devel >= 1.7.0
BuildRequires:      maven >= 3.0.5

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

################################################################################

%package lib
Summary:            Core part of Maven
Group:              Development/Tools

Requires:           javapackages-tools

%description lib
Core part of Apache Maven that can be used as a library.

################################################################################

%prep
%setup -qn %{pkg_name}-%{version}

%build

%install
rm -rf %{buildroot}

export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

mvn -Dmaven.test.skip=true -DdistributionTargetDir="%{buildroot}%{pkg_homedir}" clean package

rm -f %{buildroot}%{pkg_homedir}/LICENSE
rm -f %{buildroot}%{pkg_homedir}/NOTICE
rm -f %{buildroot}%{pkg_homedir}/README.txt

rm -f %{buildroot}%{pkg_homedir}/bin/*.cmd

install -dm 755 %{buildroot}%{_datadir}/java/%{name}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_datadir}/bash-completion/completions/
install -dm 755 %{buildroot}%{_mandir}/man1

install -pm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/mvn

for jar in %{buildroot}%{pkg_homedir}/lib/%{name}-*.jar ; do
    jarname=$(basename "$jar" .jar)
    ln -sfv %{pkg_homedir}/lib/${jarname}.jar %{buildroot}%{_datadir}/java/%{name}/${jarname}.jar
done

for b in %{buildroot}%{pkg_homedir}/bin/* ; do
    binaryname=$(basename "$b")
    ln -sfv %{pkg_homedir}/bin/${binaryname} %{buildroot}%{_bindir}/${binaryname}
done

mv %{buildroot}%{pkg_homedir}/bin/m2.conf %{buildroot}%{_sysconfdir}/m2.conf
ln -sf %{_sysconfdir}/m2.conf %{buildroot}%{pkg_homedir}/bin/m2.conf

mv %{buildroot}%{pkg_homedir}/conf/settings.xml %{buildroot}%{_sysconfdir}/%{name}/settings.xml
ln -sf %{_sysconfdir}/%{name}/settings.xml %{buildroot}%{pkg_homedir}/conf/settings.xml

mv %{buildroot}%{pkg_homedir}/conf/logging %{buildroot}%{_sysconfdir}/%{name}/
ln -sf %{_sysconfdir}/%{name}/logging %{buildroot}%{pkg_homedir}/conf/logging

%check
%if %{?_with_check:1}%{?_without_check:0}
mvn test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/bash-completion

%files lib
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md CONTRIBUTING.md
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/logging
%dir %{pkg_homedir}/lib/
%dir %{pkg_homedir}/bin/
%dir %{pkg_homedir}/conf
%dir %{pkg_homedir}/boot
%dir %{_datadir}/java/%{name}
%config(noreplace) %{_sysconfdir}/m2.conf
%config(noreplace) %{_sysconfdir}/%{name}/settings.xml
%{_sysconfdir}/%{name}/logging/*
%{pkg_homedir}/lib/*
%{pkg_homedir}/bin/*
%{pkg_homedir}/boot/*.jar
%{pkg_homedir}/conf/*
%{_datadir}/java/%{name}/*.jar
%exclude %{pkg_homedir}/lib/jansi-native

################################################################################

%changelog
* Tue Jul 09 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.6.1-0
- Initial build.
