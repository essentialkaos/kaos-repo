################################################################################

# rpmbuilder:github       yandex/ClickHouse
# rpmbuilder:tag          v19.4.1.3-stable

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

%define service_user       clickhouse
%define service_group      clickhouse
%define service_data_dir   %{_sharedstatedir}/clickhouse
%define service_log_dir    %{_logdir}/clickhouse-server

################################################################################

Summary:           Yandex ClickHouse DBMS
Name:              clickhouse
Version:           19.4.1.3
Release:           0%{?dist}
License:           APL 2.0
Group:             Applications/Databases
URL:               https://clickhouse.yandex

Source:            %{name}-%{version}.tar.bz2

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     centos-release-scl devtoolset-7
BuildRequires:     cmake3 openssl-devel libicu-devel libtool-ltdl-devel
BuildRequires:     unixODBC-devel readline-devel

Requires:          openssl libicu libtool-ltdl unixODBC readline

%if 0%{?rhel} >= 7
Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(pre):     shadow-utils
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
ClickHouse is an open-source column-oriented database management
system that allows generating analytical data reports in real time.

################################################################################

%package client

Summary:           ClickHouse client binary
Group:             Applications/Databases

Requires:          %{name}-server = %{version}-%{release}

%description client
This package contains client binary for ClickHouse DBMS.

################################################################################

%package common-static

Summary:           ClickHouse common static binaries
Group:             Applications/Databases

%description common-static
This package contains static binaries for ClickHouse DBM.

################################################################################

%package server-common

Summary:           Common configuration files for ClickHouse
Group:             Applications/Databases

%description server-common
This package contains common configuration files for ClickHouse DBMS.

################################################################################

%package server

Summary:           Server files for ClickHouse
Group:             Applications/Databases

Requires:          %{name}-common-static = %{version}-%{release}
Requires:          %{name}-server-common = %{version}-%{release}

%description server
This package contains server files for ClickHouse DBMS.

################################################################################

%package test
Summary:           ClickHouse test suite
Group:             Applications/Databases

Requires:          %{name}-server = %{version}-%{release}

%description test
This package contains test suite for ClickHouse DBMS.

################################################################################

%prep
%setup -q

%build
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-7/root/usr/bin:$PATH"

%if 0%{?rhel} == 6
export CMAKE_OPTIONS="$CMAKE_OPTIONS -DENABLE_JEMALLOC=0"
%endif

mkdir -p build

pushd build
  cmake3 .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
            -DCMAKE_BUILD_TYPE:STRING=Release \
            $CMAKE_OPTIONS
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

pushd build
  for daemon in clickhouse clickhouse-test clickhouse-compressor clickhouse-client clickhouse-server ; do
    DESTDIR=%{buildroot} cmake3 -DCOMPONENT=$daemon -P cmake_install.cmake;
  done
popd

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_crondir}
install -dm 755 %{buildroot}%{_sysconfdir}/security/limits.d

# Server
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_datadir}/%{name}/bin
install -dm 755 %{buildroot}%{_datadir}/%{name}/headers
install -dm 700 %{buildroot}%{service_data_dir}
install -dm 775 %{buildroot}%{service_log_dir}

# Client
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}-client
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}-client/conf.d

install -pm 644 debian/%{name}-server.cron.d \
                %{buildroot}%{_crondir}/%{name}-server

install -pm 644 debian/%{name}.limits \
                %{buildroot}%{_sysconfdir}/security/limits.d/%{name}.conf

install -pm 644 dbms/programs/server/config.xml \
                dbms/programs/server/users.xml \
                %{buildroot}%{_sysconfdir}/%{name}-server/

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 debian/%{name}-server.service \
                %{buildroot}%{_unitdir}/
%else
install -dm 755 %{buildroot}%{_initddir}
install -pm 755 debian/%{name}-server.init \
                %{buildroot}%{_initddir}/%{name}-server
%endif

%clean
rm -rf %{buildroot}

%pre server
getent group %{service_group} >/dev/null || %{__groupadd} %{name} 2> /dev/null || true
getent passwd %{service_user} >/dev/null || %{__useradd} -r -M -d %{service_data_dir} -s /sbin/nologin -g %{service_group} -c "ClickHouse Server" %{name} 2>/dev/null || true
exit 0

%pre client
getent group %{service_group} >/dev/null || %{__groupadd} %{name} 2> /dev/null || true
getent passwd %{service_user} >/dev/null || %{__useradd} -r -M -d %{service_data_dir} -s /sbin/nologin -g %{service_group} -c "ClickHouse Server" %{name} 2>/dev/null || true
exit 0

%post server
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} enable %{name}-server.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name}-server &>/dev/null || :
%endif
fi

if [[ -d %{service_data_dir}/build ]] ; then
  rm -f %{service_data_dir}/build/*.cpp %{service_data_dir}/build/*.so &>/dev/null || :
fi

%preun server
if [[ $1 -eq 0 ]]; then
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}-server.service &>/dev/null || :
  %{__systemctl} stop %{name}-server.service &>/dev/null || :
%else
  %{__service} %{name}-server stop &>/dev/null || :
  %{__chkconfig} --del %{name}-server &>/dev/null || :
%endif
fi

%postun server
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-, root, root, -)
# No files for you

%files common-static
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/security/limits.d/%{name}.conf
%{_bindir}/%{name}
%{_datadir}/%{name}

%files client
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/%{name}-client/config.xml
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-client
%{_bindir}/%{name}-compressor
%{_bindir}/%{name}-extract-from-config
%{_bindir}/%{name}-local
%attr(0755, %{service_user}, %{service_group}) %{_sysconfdir}/%{name}-client/conf.d

%files server
%defattr(-, root, root, -)
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}-server.service
%else
%{_initddir}/%{name}-server
%endif
%{_crondir}/%{name}-server
%{_bindir}/%{name}-clang
%{_bindir}/%{name}-copier
%{_bindir}/%{name}-format
%{_bindir}/%{name}-lld
%{_bindir}/%{name}-obfuscator
%{_bindir}/%{name}-odbc-bridge
%{_bindir}/%{name}-report
%{_bindir}/%{name}-server
%attr(0700, %{service_user}, %{service_group}) %dir %{service_data_dir}
%attr(0775, root, %{service_group}) %dir %{service_log_dir}

%files server-common
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/%{name}-server/config.xml
%config(noreplace) %{_sysconfdir}/%{name}-server/users.xml

%files test
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/%{name}-client/client-test.xml
%config(noreplace) %{_sysconfdir}/%{name}-server/server-test.xml
%{_bindir}/%{name}-test
%{_bindir}/%{name}-test-server
%{_bindir}/%{name}-performance-test
%{_datadir}/%{name}-test

################################################################################

%changelog
* Mon Mar 25 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 19.4.1.3-0
- Updated to the latest release

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 18.16.1-0
- Initial build for kaos repository
