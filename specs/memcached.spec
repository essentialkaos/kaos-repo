################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define username   memcached
%define groupname  memcached

################################################################################

Summary:        High Performance, Distributed Memory Object Cache
Name:           memcached
Version:        1.6.38
Release:        0%{?dist}
Group:          System Environment/Daemons
License:        BSD
URL:            https://memcached.org

Source0:        https://www.memcached.org/files/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc automake which libevent-devel

Requires:       libevent

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

################################################################################

%package devel
Summary:   Files needed for development using memcached protocol
Group:     Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.

################################################################################

%package debug
Summary:   Debug version of memcached
Group:     System Environment/Daemons

Requires:  %{name} = %{version}-%{release}

%description debug
Version of memcached show more additional information for debugging.

################################################################################

%prep
%{crc_check}

%setup -q
%{configure}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_unitdir}

install -pm 644 scripts/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 scripts/%{name}.service %{buildroot}%{_unitdir}/

install -pm 755 %{name}-debug %{buildroot}%{_bindir}/%{name}-debug
install -pm 755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool

install -pm 644 scripts/%{name}-tool.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || useradd -r -g %{groupname} -d %{_localstatedir}/run/%{name} -s /sbin/nologin %{username}

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{name}.service &>/dev/null || :
  systemctl stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  systemctl daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/run/%{name}
%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/log/%{name}
%{_unitdir}/%{name}.service
%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/*

%files debug
%defattr(-,root,root,0755)
%{_bindir}/%{name}-debug

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.38-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1638

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.37-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1637

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.36-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1636

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.35-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1635

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.34-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1634

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.33-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1633

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.32-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1632

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.31-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1631

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.30-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1630

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.29-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1629

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.28-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1628

* Thu May 30 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.27-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1627

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.26-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1626

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.25-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1625

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.24-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1624

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.6.23-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1623

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.6.22-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1622

* Thu Jul 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.6.21-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1621

* Thu Jul 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.6.20-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1620

* Thu Jul 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.6.19-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes1619

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.6.2-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes162

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes161

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- https://github.com/memcached/memcached/wiki/ReleaseNotes160
