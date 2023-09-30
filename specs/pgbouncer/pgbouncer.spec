################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define username   %{name}
%define groupname  %{name}

################################################################################

Summary:           Lightweight connection pooler for PostgreSQL
Name:              pgbouncer
Version:           1.20.1
Release:           0%{?dist}
License:           MIT and BSD
Group:             Applications/Databases
URL:               https://pgbouncer.github.io

Source0:           https://pgbouncer.github.io/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.sysconfig
Source3:           %{name}.logrotate
Source4:           %{name}.service

Source100:         checksum.sha512

Patch0:            %{name}-ini.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc openssl-devel libevent-devel pam-devel systemd-devel

Requires:          kaosv >= 2.16 openssl libevent

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
pgbouncer is a lightweight connection pooler for PostgreSQL. pgbouncer uses
libevent for low-level socket handling.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%patch0 -p1

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

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_initrddir}

install -pm 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
install -pm 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service
%endif

rm -f %{buildroot}%{_docdir}/%{name}/pgbouncer.ini
rm -f %{buildroot}%{_docdir}/%{name}/NEWS
rm -f %{buildroot}%{_docdir}/%{name}/README
rm -f %{buildroot}%{_docdir}/%{name}/userlist.txt

%clean
rm -rf %{buildroot}

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
%doc AUTHORS COPYRIGHT NEWS.md
%attr(-,%{username},%{groupname}) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/*
%{_initrddir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*
%{_docdir}/%{name}/*

################################################################################

%changelog
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
