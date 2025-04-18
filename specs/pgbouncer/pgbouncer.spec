################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define username   %{name}
%define groupname  %{name}

################################################################################

Summary:           Lightweight connection pooler for PostgreSQL
Name:              pgbouncer
Version:           1.24.1
Release:           0%{?dist}
License:           MIT and BSD
Group:             Applications/Databases
URL:               https://www.pgbouncer.org

Source0:           https://www.pgbouncer.org/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source1:           %{name}.service
Source2:           %{name}.logrotate
Source3:           %{name}.pam
Source4:           %{name}.tmpd

Source100:         checksum.sha512

Patch0:            %{name}-ini.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc openssl-devel libevent-devel pam-devel systemd-devel

Requires:          openssl libevent

Provides:          %{name} = %{version}-%{release}

################################################################################

%package utils
Summary:  Optional utilities and scripts for pgbouncer
Group:    Development/Tools

Requires:  python3 python3-psycopg2

%description utils
Optional utilities and scripts for pgbouncer.

################################################################################

%description
pgbouncer is a lightweight connection pooler for PostgreSQL. pgbouncer uses
libevent for low-level socket handling.

################################################################################

%prep
%crc_check
%autosetup -p1 -n %{name}-%{version}

%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

%configure --enable-debug \
           --with-pam \
           --with-systemd

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_rundir}/%{name}

install -pm 600 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}/
install -pm 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

touch %{buildroot}%{_sysconfdir}/%{name}/userlist.txt
chmod 600 %{buildroot}%{_sysconfdir}/%{name}/userlist.txt

install -pDm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -pDm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -pDm 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf

rm -f %{buildroot}%{_docdir}/%{name}/pgbouncer.ini
rm -f %{buildroot}%{_docdir}/%{name}/NEWS
rm -f %{buildroot}%{_docdir}/%{name}/README
rm -f %{buildroot}%{_docdir}/%{name}/userlist.txt

################################################################################

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{name}.service &>/dev/null || :
fi

%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || useradd -g %{username} -r -s /bin/bash %{username}

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
%doc AUTHORS COPYRIGHT
%attr(-,%{username},%{groupname}) %dir %{_sysconfdir}/%{name}
%attr(-,%{username},%{groupname}) %dir %{_rundir}/%{name}
%attr(600,%{username},%{groupname}) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%attr(600,%{username},%{groupname}) %config(noreplace) %{_sysconfdir}/%{name}/userlist.txt
%attr(700,%{username},%{groupname}) %{_localstatedir}/log/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_tmpfilesdir}/%{name}.conf
%{_bindir}/*
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_docdir}/%{name}/*
%ghost %{_rundir}/%{name}/%{name}.pid

%files utils
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}/mkauth.py
%exclude %{_sysconfdir}/%{name}/mkauth.py?

################################################################################

%changelog
* Thu Apr 17 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-124x

* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-124x

* Thu Oct 31 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.1-1
- Improve systemd unit file

* Mon Sep 09 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-123x

* Mon Sep 09 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-122x
- Remove init script usage
- Added tmpfiles.d configuration
- Added pam configuration

* Tue Oct 17 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-121x

* Sun Oct 01 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-120x

* Sun Oct 01 2023 Anton Novojilov <andy@essentialkaos.com> - 1.19.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-119x

* Sun Oct 01 2023 Anton Novojilov <andy@essentialkaos.com> - 1.18.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-118x

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 1.17.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-117x

* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.1-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-116x

* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-116x

* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.15.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-115x

* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.14.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-114x

* Sat May 23 2020 Anton Novojilov <andy@essentialkaos.com> - 1.13.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-113x

* Wed Feb 12 2020 Anton Novojilov <andy@essentialkaos.com> - 1.12.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-112x

* Wed Feb 12 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-0
- https://www.pgbouncer.org/changelog.html#pgbouncer-111x
