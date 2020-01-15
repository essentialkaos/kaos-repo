################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack %{nil}

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

%{!?_without_check: %define _with_check 1}

################################################################################

%define pkg_name          rest-utils
%define pkg_homedir       %{_datadir}/%{name}

################################################################################

Summary:            Utilities and a small framework for building REST services
Name:               confluent-rest-utils
Version:            5.4.0
Release:            0%{?dist}
License:            ASL 2.0
Group:              Development/Tools
URL:                https://github.com/confluentinc/rest-utils

Source0:            https://github.com/confluentinc/%{pkg_name}/archive/v%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           java >= 1.8.0

BuildRequires:      jdk8 maven git

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Confluent REST Utils provides a small framework and utilities for writing
Java REST APIs using Jersey, Jackson, Jetty, and Hibernate Validator.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkg_name}-%{version}

%build

%install
rm -rf %{buildroot}

mvn -Dmaven.test.skip=true install

install -dm 755 %{buildroot}%{_datadir}/java/%{pkg_name}
install -dm 755 %{buildroot}%{_datadir}/doc/%{pkg_name}-%{version}

pushd package/target/%{pkg_name}-package-%{version}-package/share
  cp -a java/%{pkg_name}/*.jar %{buildroot}%{_datadir}/java/%{pkg_name}/
  cp -a doc/%{pkg_name}/* %{buildroot}%{_datadir}/doc/%{pkg_name}-%{version}/
popd

%check
%if %{?_with_check:1}%{?_without_check:0}
mvn test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_datadir}/java/%{pkg_name}
%dir %{_datadir}/doc/%{pkg_name}-%{version}
%{_datadir}/java/%{pkg_name}/*.jar
%{_datadir}/doc/%{pkg_name}-%{version}/*

################################################################################

%changelog
* Wed Jan 15 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 5.4.0-0
- Initial build
