################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%define major_ver  7
%define minor_ver  0

################################################################################

Summary:           A persistent key-value database
Name:              redis
Version:           7.0.14
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               https://redis.io

Source0:           https://github.com/redis/%{name}/archive/%{version}.tar.gz
Source1:           %{name}.logrotate
Source3:           %{name}.sysconfig
Source4:           sentinel.logrotate
Source6:           sentinel.sysconfig
Source7:           %{name}.service
Source8:           sentinel.service
Source9:           %{name}-limit-systemd
Source10:          sentinel-limit-systemd

Source100:         checksum.sha512

Patch0:            redis-%{major_ver}%{minor_ver}-config.patch
Patch1:            sentinel-%{major_ver}%{minor_ver}-config.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make tcl systemd-devel

%if 0%{?rhel} <= 7
BuildRequires:     devtoolset-9-gcc
%else
BuildRequires:     gcc
%endif

Requires:          %{name}-cli >= %{version}
Requires:          logrotate

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Conflicts:         redis5 redis6 redis7

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

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%patch0 -p1
%patch1 -p1

%build
%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-9/root/usr/bin:$PATH"
%endif

export BUILD_WITH_SYSTEMD=yes

%{__make} %{?_smp_mflags} MALLOC=jemalloc

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

install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf

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
  systemctl enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{name}.service &>/dev/null || :
  systemctl --no-reload disable sentinel.service &>/dev/null || :
  systemctl stop %{name}.service &>/dev/null || :
  systemctl stop sentinel.service &>/dev/null || :
fi

%postun
systemctl daemon-reload &>/dev/null || :

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%attr(-,%{name},%{name}) %config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/sentinel
%dir %attr(0755,%{name},root) %{_localstatedir}/lib/%{name}
%dir %attr(0755,%{name},root) %{_localstatedir}/log/%{name}
%dir %attr(0755,%{name},root) %{_localstatedir}/run/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%{_bindir}/%{name}-server
%{_bindir}/%{name}-sentinel
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-rdb
%{_sbindir}/%{name}-server

%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%{_bindir}/%{name}-cli

################################################################################

%changelog
* Thu Oct 19 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.14-0
- https://github.com/redis/redis/blob/7.0.14/00-RELEASENOTES

* Thu Oct 19 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.13-0
- https://github.com/redis/redis/blob/7.0.13/00-RELEASENOTES

* Tue Aug 08 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.12-0
- https://github.com/redis/redis/blob/7.0.12/00-RELEASENOTES

* Wed Jul 05 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.11-0
- https://github.com/redis/redis/blob/7.0.11/00-RELEASENOTES

* Wed Jul 05 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.10-0
- https://github.com/redis/redis/blob/7.0.10/00-RELEASENOTES

* Wed Jul 05 2023 Anton Novojilov <andy@essentialkaos.com> - 7.0.9-0
- https://github.com/redis/redis/blob/7.0.9/00-RELEASENOTES

* Wed Jul 05 2023 Anton Novojilov <andy@essentialkaos.com> - 6.2.12-0
- https://github.com/redis/redis/blob/6.2.12/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.7-0
- https://github.com/redis/redis/blob/6.2.7/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.6-0
- https://github.com/redis/redis/blob/6.2.6/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.5-0
- https://github.com/redis/redis/blob/6.2.5/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.4-0
- https://github.com/redis/redis/blob/6.2.4/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.3-0
- https://github.com/redis/redis/blob/6.2.3/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.2-0
- https://github.com/redis/redis/blob/6.2.2/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.1-0
- https://github.com/redis/redis/blob/6.2.1/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2.0-0
- https://github.com/redis/redis/blob/6.2.0/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.16-0
- https://github.com/redis/redis/blob/6.0.16/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.15-0
- https://github.com/redis/redis/blob/6.0.15/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.14-0
- https://github.com/redis/redis/blob/6.0.14/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.13-0
- https://github.com/redis/redis/blob/6.0.13/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.12-0
- https://github.com/redis/redis/blob/6.0.12/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.11-0
- https://github.com/redis/redis/blob/6.0.11/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.10-0
- https://github.com/redis/redis/blob/6.0.10/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.9-0
- https://github.com/redis/redis/blob/6.0.9/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.8-0
- https://github.com/redis/redis/blob/6.0.8/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.7-0
- https://github.com/redis/redis/blob/6.0.7/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.6-0
- https://github.com/redis/redis/blob/6.0.6/00-RELEASENOTES

* Wed May 25 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0.5-0
- https://github.com/redis/redis/blob/6.0.5/00-RELEASENOTES

* Thu Jun 04 2020 Anton Novojilov <andy@essentialkaos.com> - 6.0.4-0
- https://github.com/redis/redis/blob/6.0.4/00-RELEASENOTES

* Sat May 23 2020 Anton Novojilov <andy@essentialkaos.com> - 6.0.3-0
- https://github.com/redis/redis/blob/6.0.3/00-RELEASENOTES

* Fri May 22 2020 Anton Novojilov <andy@essentialkaos.com> - 6.0.2-0
- https://github.com/redis/redis/blob/6.0.2/00-RELEASENOTES

* Fri May 22 2020 Anton Novojilov <andy@essentialkaos.com> - 6.0.1-0
- https://github.com/redis/redis/blob/6.0.1/00-RELEASENOTES

* Fri May 22 2020 Anton Novojilov <andy@essentialkaos.com> - 6.0.0-0
- https://github.com/redis/redis/blob/6.0.0/00-RELEASENOTES

* Thu Jan 23 2020 Anton Novojilov <andy@essentialkaos.com> - 5.0.7-0
- https://github.com/redis/redis/blob/5.0.7/00-RELEASENOTES

* Thu Jan 23 2020 Anton Novojilov <andy@essentialkaos.com> - 5.0.6-0
- https://github.com/redis/redis/blob/5.0.6/00-RELEASENOTES

* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.5-0
- https://github.com/redis/redis/blob/5.0.5/00-RELEASENOTES

* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.4-0
- https://github.com/redis/redis/blob/5.0.4/00-RELEASENOTES

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.3-0
- https://github.com/redis/redis/blob/5.0.3/00-RELEASENOTES

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.2-0
- https://github.com/redis/redis/blob/5.0.2/00-RELEASENOTES

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.1-0
- https://github.com/redis/redis/blob/5.0.1/00-RELEASENOTES

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- https://github.com/redis/redis/blob/5.0.0/00-RELEASENOTES
