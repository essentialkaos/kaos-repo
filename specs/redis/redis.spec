################################################################################

# rpmbuilder:pedantic true

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

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
%define __sysctl          %{_bindir}/systemctl

################################################################################

Summary:            A persistent key-value database
Name:               redis
Version:            5.0.7
Release:            0%{?dist}
License:            BSD
Group:              Applications/Databases
URL:                https://redis.io

Source0:            https://github.com/antirez/%{name}/archive/%{version}.tar.gz
Source1:            %{name}.logrotate
Source2:            %{name}.init
Source3:            %{name}.sysconfig
Source4:            sentinel.logrotate
Source5:            sentinel.init
Source6:            sentinel.sysconfig
Source7:            %{name}.service
Source8:            sentinel.service
Source9:            %{name}-limit-systemd
Source10:           sentinel-limit-systemd

Source100:          checksum.sha512

Patch0:             %{name}-config.patch
Patch1:             sentinel-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc tcl

Requires:           %{name}-cli >= %{version}
Requires:           logrotate
%if 0%{?rhel} <= 6
Requires:           kaosv >= 2.15
%endif

%if 0%{?rhel} >= 7
Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%else
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts
%endif

################################################################################

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

################################################################################

%package cli

Summary:            Client for working with Redis from console
Group:              Applications/Databases

%description cli
Client for working with Redis from console

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%patch0 -p1
%patch1 -p1

%build
%ifarch %ix86
sed -i '/integration\/logging/d' tests/test_helper.tcl
%{__make} %{?_smp_mflags} 32bit MALLOC=jemalloc
%else
%{__make} %{?_smp_mflags} MALLOC=jemalloc
%endif

%install
rm -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/sentinel
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/sentinel

install -pm 640 %{name}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}

%if 0%{?rhel} <= 6
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -pm 755 %{SOURCE5} %{buildroot}%{_initrddir}/sentinel
%endif

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%endif

chmod 755 %{buildroot}%{_bindir}/%{name}-*

rm -f %{buildroot}%{_bindir}/%{name}-sentinel

install -dm 755 %{buildroot}%{_sbindir}

ln -sf %{_bindir}/%{name}-server %{buildroot}%{_bindir}/%{name}-sentinel
ln -sf %{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} test
%{__make} %{?_smp_mflags} test-sentinel
%endif

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
        -c 'Redis Server' %{name} &> /dev/null

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

chown %{name}:%{name} %{_sysconfdir}/%{name}.conf
chown %{name}:%{name} %{_sysconfdir}/sentinel.conf

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} --no-reload disable sentinel.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
  %{__sysctl} stop sentinel.service &>/dev/null || :
%else
  %{__service} %{name} stop &> /dev/null || :
  %{__service} sentinel stop &> /dev/null || :
  %{__chkconfig} --del %{name} &> /dev/null || :
  %{__chkconfig} --del sentinel &> /dev/null || :
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README.md

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/sentinel
%config(noreplace) %{_sysconfdir}/*.conf

%dir %attr(0755, %{name}, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}

%if 0%{?rhel} <= 6
%{_initrddir}/%{name}
%{_initrddir}/sentinel
%endif

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%endif

%{_bindir}/%{name}-server
%{_bindir}/%{name}-sentinel
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-rdb
%{_sbindir}/%{name}-server

%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README.md
%{_bindir}/%{name}-cli

################################################################################

%changelog
* Thu Jan 23 2020 Anton Novojilov <andy@essentialkaos.com> - 5.0.7-0
- Updated to the latest stable release

* Thu Jan 23 2020 Anton Novojilov <andy@essentialkaos.com> - 5.0.6-0
- Updated to the latest stable release

* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.5-0
- Updated to the latest stable release

* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.4-0
- Updated to the latest stable release

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.3-0
- Updated to the latest stable release

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.2-0
- Updated to the latest stable release

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.1-0
- Updated to the latest stable release

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- Updated to the latest stable release
