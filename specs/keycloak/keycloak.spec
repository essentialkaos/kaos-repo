################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:    Open Source Identity and Access Management
Name:       keycloak
Version:    26.4.1
Release:    0%{?dist}
Group:      System/Servers
License:    Apache-2.0
URL:        https://www.keycloak.org

Source0:    https://github.com/keycloak/keycloak/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.sysconfig
Source3:    bootstrap.sh
Source4:    startup.sh

Source100:  checksum.sha512

Patch1:     keycloak-paths.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   jre21

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
Add authentication to applications and secure services with minimum effort. No
need to deal with storing users or authenticating users.

Keycloak provides user federation, strong authentication, user management,
fine-grained authorization, and more.

################################################################################

%prep
%{crc_check}

%autosetup -p1 -n %{name}-%{version}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}

rm -f bin/*.bat

cp -rp bin lib providers themes version.txt %{buildroot}%{_sharedstatedir}/%{name}/
cp -rp conf/* %{buildroot}%{_sysconfdir}/%{name}/
rm -f %{buildroot}%{_sysconfdir}/%{name}/README.md

install -pm 755 %{SOURCE3} %{buildroot}%{_sharedstatedir}/%{name}/bin/
install -pm 755 %{SOURCE4} %{buildroot}%{_sharedstatedir}/%{name}/bin/

install -pm 644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -pm 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
        -c 'Keycloak Server' %{name} &> /dev/null

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
systemctl daemon-reload &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.md
%attr(-,%{name},%{name}) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(-,%{name},%{name}) %config(noreplace) %{_sysconfdir}/%{name}/cache-ispn.xml
%attr(-,%{name},%{name}) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/log/%{name}
%{_unitdir}/%{name}.service

################################################################################

%changelog
* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 26.4.1-0
- https://github.com/keycloak/keycloak/releases/tag/26.4.1

* Tue Aug 05 2025 Anton Novojilov <andy@essentialkaos.com> - 26.3.2-0
- https://github.com/keycloak/keycloak/releases/tag/26.3.2

* Mon Jul 21 2025 Anton Novojilov <andy@essentialkaos.com> - 26.3.1-0
- https://github.com/keycloak/keycloak/releases/tag/26.3.1
