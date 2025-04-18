################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%define major_ver  7
%define minor_ver  2

################################################################################

Summary:           A persistent key-value database
Name:              valkey
Version:           7.2.8
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               https://valkey.io

Source0:           https://github.com/valkey-io/%{name}/archive/%{version}.tar.gz
Source1:           %{name}.logrotate
Source2:           sentinel.logrotate
Source3:           %{name}.service
Source4:           sentinel.service
Source5:           %{name}-limit-systemd
Source6:           sentinel-limit-systemd

Source100:         checksum.sha512

Patch0:            valkey-%{major_ver}%{minor_ver}-config.patch
Patch1:            sentinel-%{major_ver}%{minor_ver}-config.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc tcl systemd-devel

Requires:          %{name}-cli >= %{version}
Requires:          logrotate

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Conflicts:         redis valkey72

Provides:          %{name} = %{version}-%{release}
Provides:          %{name}-server = %{version}-%{release}
Provides:          %{name}-sentinel = %{version}-%{release}

################################################################################

%description
Valkey is a high-performance data structure server that primarily serves
key/value workloads. It supports a wide range of native structures and an
extensible plugin system for adding new data structures and access patterns.

################################################################################

%package cli

Summary:  Client for working with Valkey from console
Group:    Applications/Databases

%description cli
Client for working with Valkey from console

################################################################################

%package devel

Summary:  Development header for Valkey module development
Group:    Development/Libraries

Provides:  %{name}-static = %{version}-%{release}

%description devel
Header file required for building loadable Valkey modules.

################################################################################

%prep
%crc_check
%autosetup -p1 -n %{name}-%{version}

%build
export BUILD_WITH_SYSTEMD=yes

%{__make} %{?_smp_mflags} MALLOC=jemalloc

%install
rm -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/sentinel

install -pm 640 %{name}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}

install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf

install -dm 755 %{buildroot}%{_includedir}
install -pm 644 src/redismodule.h %{buildroot}%{_includedir}/redismodule.h

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
        -c 'Valkey Server' %{name} &> /dev/null

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

################################################################################

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%attr(-,%{name},%{name}) %config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%dir %attr(0755,%{name},root) %{_localstatedir}/lib/%{name}
%dir %attr(0755,%{name},root) %{_localstatedir}/log/%{name}
%dir %attr(0755,%{name},root) %{_localstatedir}/run/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%{_bindir}/%{name}-*
%{_bindir}/redis-*
%{_sbindir}/%{name}-server

%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README.md
%{_bindir}/%{name}-cli

%files devel
%doc COPYING
%defattr(-,root,root,-)
%{_includedir}/redismodule.h

################################################################################

%changelog
* Mon Jan 13 2025 Anton Novojilov <andy@essentialkaos.com> - 7.2.8-0
- https://github.com/valkey-io/valkey/releases/tag/7.2.8

* Fri Dec 20 2024 Anton Novojilov <andy@essentialkaos.com> - 7.2.7-0
- https://github.com/valkey-io/valkey/blob/7.2.7/00-RELEASENOTES
