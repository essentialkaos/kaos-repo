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

%define pkg_name          common
%define pkg_homedir       %{_datadir}/%{name}

################################################################################

Summary:            Common utilities library containing metrics, config and utils
Name:               confluent-common
Version:            5.2.2
Release:            0%{?dist}
License:            ASL 2.0
Group:              Development/Tools
URL:                https://github.com/confluentinc/common

Source0:            https://github.com/confluentinc/%{pkg_name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           java >= 1.7.0

BuildRequires:      java >= 1.7.0 java-devel >= 1.7.0 maven >= 3.2

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Common utilities, including metrics and config.

################################################################################

%prep
%setup -qn %{pkg_name}-%{version}

%build
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

%install
rm -rf %{buildroot}

mvn -Dmaven.test.skip=true install

install -dm 755 %{buildroot}%{_datadir}/java/%{name}
install -dm 755 %{buildroot}%{_datadir}/doc/%{name}-%{version}

pushd package/target/%{pkg_name}-package-%{version}-package/share
  cp -a java/%{name}/*.jar %{buildroot}%{_datadir}/java/%{name}/
  cp -a doc/%{name}/* %{buildroot}%{_datadir}/doc/%{name}-%{version}/
popd

%check
mvn test

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_datadir}/java/%{name}
%dir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/java/%{name}/*.jar
%{_datadir}/doc/%{name}-%{version}/*

################################################################################

%changelog
* Tue Jul 09 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 5.2.2-0
- Initial build.
