################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%define realname   redis
%define major_ver  7
%define minor_ver  2

################################################################################

Summary:           A persistent key-value database
Name:              redis%{major_ver}%{minor_ver}
Version:           7.2.7
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               https://redis.io

Source0:           https://github.com/redis/%{realname}/archive/%{version}.tar.gz
Source1:           %{realname}.logrotate
Source3:           %{realname}.sysconfig
Source4:           sentinel.logrotate
Source6:           sentinel.sysconfig
Source7:           %{realname}.service
Source8:           sentinel.service
Source9:           %{realname}-limit-systemd
Source10:          sentinel-limit-systemd

Source100:         checksum.sha512

Patch0:            %{realname}-%{major_ver}%{minor_ver}-config.patch
Patch1:            sentinel-%{major_ver}%{minor_ver}-config.patch

BuildRoot:         %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc tcl systemd-devel

Requires:          %{name}-cli >= %{version}
Requires:          logrotate

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Conflicts:         redis redis50 redis60 redis62 redis70 redis74

Provides:          %{name} = %{version}-%{release}
Provides:          %{name}-server = %{version}-%{release}
Provides:          %{name}-sentinel = %{version}-%{release}

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

Summary:  Client for working with Redis from console
Group:    Applications/Databases

%description cli
Client for working with Redis from console

################################################################################

%package devel

Summary:  Development header for Redis module development
Group:    Development/Libraries

Provides:  %{name}-static = %{version}-%{release}

%description devel
Header file required for building loadable Redis modules.

################################################################################

%prep
%crc_check
%autosetup -p1 -n %{realname}-%{version}

%build
export BUILD_WITH_SYSTEMD=yes

%{__make} %{?_smp_mflags} MALLOC=jemalloc

%install
rm -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{realname}
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/sentinel
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{realname}
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/sentinel

install -pm 640 %{realname}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{realname}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{realname}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{realname}

install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{realname}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/systemd/system/%{realname}.service.d/limit.conf
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf

install -dm 755 %{buildroot}%{_includedir}
install -pm 644 src/redismodule.h %{buildroot}%{_includedir}/redismodule.h

chmod 755 %{buildroot}%{_bindir}/%{realname}-*

rm -f %{buildroot}%{_bindir}/%{realname}-sentinel

install -dm 755 %{buildroot}%{_sbindir}

ln -sf %{_bindir}/%{realname}-server %{buildroot}%{_bindir}/%{realname}-sentinel
ln -sf %{_bindir}/%{realname}-server %{buildroot}%{_sbindir}/%{realname}-server

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} test
%{__make} %{?_smp_mflags} test-sentinel
%endif

%pre
getent group %{realname} &> /dev/null || groupadd -r %{realname} &> /dev/null
getent passwd %{realname} &> /dev/null || \
useradd -r -g %{realname} -d %{_sharedstatedir}/%{realname} -s /sbin/nologin \
        -c 'Redis Server' %{realname} &> /dev/null

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{realname}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{realname}.service &>/dev/null || :
  systemctl --no-reload disable sentinel.service &>/dev/null || :
  systemctl stop %{realname}.service &>/dev/null || :
  systemctl stop sentinel.service &>/dev/null || :
fi

%postun
systemctl daemon-reload &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%attr(-,%{realname},%{realname}) %config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{realname}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%config(noreplace) %{_sysconfdir}/sysconfig/%{realname}
%config(noreplace) %{_sysconfdir}/sysconfig/sentinel
%dir %attr(0755,%{realname},root) %{_localstatedir}/lib/%{realname}
%dir %attr(0755,%{realname},root) %{_localstatedir}/log/%{realname}
%dir %attr(0755,%{realname},root) %{_localstatedir}/run/%{realname}
%{_unitdir}/%{realname}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{realname}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%{_bindir}/%{realname}-server
%{_bindir}/%{realname}-sentinel
%{_bindir}/%{realname}-benchmark
%{_bindir}/%{realname}-check-aof
%{_bindir}/%{realname}-check-rdb
%{_sbindir}/%{realname}-server

%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%{_bindir}/%{realname}-cli

%files devel
%doc COPYING
%defattr(-,root,root,-)
%{_includedir}/redismodule.h

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 7.2.7-0
- https://github.com/redis/redis/releases/tag/7.2.7

* Sat Nov 02 2024 Anton Novojilov <andy@essentialkaos.com> - 7.2.6-0
- https://github.com/redis/redis/blob/7.2.6/00-RELEASENOTES

* Tue Aug 20 2024 Anton Novojilov <andy@essentialkaos.com> - 7.2.5-0
- https://github.com/redis/redis/blob/7.2.5/00-RELEASENOTES

* Tue Jan 16 2024 Anton Novojilov <andy@essentialkaos.com> - 7.2.4-0
- https://github.com/redis/redis/blob/7.2.4/00-RELEASENOTES

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 7.2.3-0
- https://github.com/redis/redis/blob/7.2.3/00-RELEASENOTES

* Thu Oct 19 2023 Anton Novojilov <andy@essentialkaos.com> - 7.2.2-0
- https://github.com/redis/redis/blob/7.2.2/00-RELEASENOTES

* Fri Sep 08 2023 Anton Novojilov <andy@essentialkaos.com> - 7.2.1-0
- https://github.com/redis/redis/blob/7.2.1/00-RELEASENOTES

* Wed Aug 16 2023 Anton Novojilov <andy@essentialkaos.com> - 7.2.0-0
- https://github.com/redis/redis/blob/7.2.0/00-RELEASENOTES
