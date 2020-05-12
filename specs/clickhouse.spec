################################################################################

# rpmbuilder:github       yandex/ClickHouse
# rpmbuilder:tag          v20.3.8.53-lts

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
Version:           20.3.8.53
Release:           0%{?dist}
License:           APL 2.0
Group:             Applications/Databases
URL:               https://clickhouse.yandex

Source:            %{name}-%{version}.tar.bz2

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     centos-release-scl devtoolset-8
BuildRequires:     cmake3 openssl-devel libicu-devel libtool-ltdl-devel
BuildRequires:     unixODBC-devel readline-devel librdkafka-devel lz4-devel

Requires:          openssl libicu libtool-ltdl unixODBC readline
Requires:          lz4 librdkafka

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

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
%{crc_check}

%setup -q

%build
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-9/root/usr/bin:$PATH"

mkdir -p build

pushd build
  cmake3 .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
            -DENABLE_EMBEDDED_COMPILER=0 \
            -DENABLE_TESTS=OFF \
            -DUSE_INTERNAL_LZ4_LIBRARY:BOOL=False \
            -DUSE_INTERNAL_RDKAFKA_LIBRARY:BOOL=False \
            -DGLIBC_COMPATIBILITY=OFF \
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
install -dm 755 %{buildroot}%{_rundir}/%{name}-server

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

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 debian/%{name}-server.service \
                %{buildroot}%{_unitdir}/

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
  %{__systemctl} enable %{name}-server.service &>/dev/null || :

  random_pass=$(tr -cd '[:alnum:]' < /dev/urandom | fold -w18 | head -n1)

  # Generate password for default user
  sed -i "s#<password></password>#<password>$random_pass</password>#" \
         %{_sysconfdir}/%{name}-server/users.xml
fi

if [[ -d %{service_data_dir}/build ]] ; then
  rm -f %{service_data_dir}/build/*.cpp %{service_data_dir}/build/*.so &>/dev/null || :
fi

%preun server
if [[ $1 -eq 0 ]]; then
  %{__systemctl} --no-reload disable %{name}-server.service &>/dev/null || :
  %{__systemctl} stop %{name}-server.service &>/dev/null || :
fi

%postun server
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} daemon-reload &>/dev/null || :
fi

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
%{_unitdir}/%{name}-server.service
%{_crondir}/%{name}-server
%{_bindir}/%{name}-copier
%{_bindir}/%{name}-format
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
* Mon Apr 27 2020 Sergey Nikiforov <aquatoid.skynet@gmail.com> - 20.3.8.53-0
- Updated to the latest stable release

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 19.17.5.18-0
- Updated to the latest stable release

* Fri Nov 15 2019 Anton Novojilov <andy@essentialkaos.com> - 19.17.2.4-0
- Updated to the latest stable release

* Fri Oct 25 2019 Anton Novojilov <andy@essentialkaos.com> - 19.15.3.6-0
- Updated to the latest stable release

* Tue Oct 15 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 19.14.7.15-0
- Updated to the latest stable release

* Tue Jul 23 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 19.9.4.34-0
- Updated to the latest stable release

* Wed Jun 05 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 19.7.3.9-0
- Updated to the latest stable release
- Added logrotate configuration

* Tue Apr 09 2019 Anton Novojilov <andy@essentialkaos.com> - 19.4.3.11-0
- Updated to the latest stable release

* Mon Mar 25 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 19.4.1.3-0
- Updated to the latest stable release

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 18.16.1-0
- Initial build for kaos repository
