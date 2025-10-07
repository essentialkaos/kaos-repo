################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%define realname   valkey
%define major_ver  8
%define minor_ver  0

################################################################################

Summary:           A persistent key-value database
Name:              %{realname}%{major_ver}%{minor_ver}
Version:           8.0.6
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               https://valkey.io

Source0:           https://github.com/valkey-io/%{realname}/archive/%{version}.tar.gz
Source1:           %{realname}.logrotate
Source2:           sentinel.logrotate
Source3:           %{realname}.service
Source4:           sentinel.service
Source5:           %{realname}-limit-systemd
Source6:           sentinel-limit-systemd

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

Conflicts:         redis

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
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/sentinel

install -pm 640 %{realname}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{realname}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{realname}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{realname}

install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{realname}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/systemd/system/%{realname}.service.d/limit.conf
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf

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
        -c 'Valkey Server' %{realname} &> /dev/null

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
%doc 00-RELEASENOTES COPYING README.md
%attr(-,%{realname},%{realname}) %config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{realname}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%dir %attr(0755,%{realname},root) %{_localstatedir}/lib/%{realname}
%dir %attr(0755,%{realname},root) %{_localstatedir}/log/%{realname}
%dir %attr(0755,%{realname},root) %{_localstatedir}/run/%{realname}
%{_unitdir}/%{realname}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{realname}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
%{_bindir}/%{realname}-*
%{_bindir}/redis-*
%{_sbindir}/%{realname}-server

%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES COPYING README.md
%{_bindir}/%{realname}-cli

%files devel
%doc COPYING
%defattr(-,root,root,-)
%{_includedir}/redismodule.h

################################################################################

%changelog
* Tue Oct 07 2025 Anton Novojilov <andy@essentialkaos.com> - 8.0.6-0
- https://github.com/valkey-io/valkey/releases/tag/8.0.6

* Tue Oct 07 2025 Anton Novojilov <andy@essentialkaos.com> - 8.0.5-0
- https://github.com/valkey-io/valkey/releases/tag/8.0.5

* Tue Oct 07 2025 Anton Novojilov <andy@essentialkaos.com> - 8.0.4-0
- https://github.com/valkey-io/valkey/releases/tag/8.0.4

* Tue Oct 07 2025 Anton Novojilov <andy@essentialkaos.com> - 8.0.3-0
- https://github.com/valkey-io/valkey/releases/tag/8.0.3

* Mon Jan 13 2025 Anton Novojilov <andy@essentialkaos.com> - 8.0.2-0
- https://github.com/valkey-io/valkey/releases/tag/8.0.2

* Tue Dec 24 2024 Anton Novojilov <andy@essentialkaos.com> - 8.0.1-0
- https://github.com/valkey-io/valkey/blob/8.0.1/00-RELEASENOTES
