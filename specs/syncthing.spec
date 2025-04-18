################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define debug_package  %{nil}

################################################################################

Summary:        Open Source Continuous File Synchronization
Name:           syncthing
Version:        1.29.5
Release:        0%{?dist}
Group:          Applications/Internet
License:        MPL-2.0
URL:            https://syncthing.net

Source0:        https://github.com/syncthing/syncthing/releases/download/v%{version}/%{name}-source-v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  golang >= 1.23

Provides:       %{name} = %{version}-%{release}

################################################################################

%description

Syncthing is a continuous file synchronization program. It synchronizes files
between two or more computers. We strive to fulfill the goals below.

Syncthing should be:
1. Safe From Data Loss
2. Secure Against Attackers
3. Easy to Use
4. Automatic
5. Universally Available
6. For Individuals
7. Everything Else

################################################################################

%package tools
Summary:  Additional tools for Syncthing
Group:    Applications/System

%description tools
Syncthing Discovery Server and Syncthing Relay Server.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}

%build
go run build.go -no-upgrade -version=v%{version} build syncthing
go run build.go -no-upgrade -version=v%{version} build strelaysrv
go run build.go -no-upgrade -version=v%{version} build stdiscosrv
go run build.go -no-upgrade -version=v%{version} build strelaypoolsrv
go run build.go -no-upgrade -version=v%{version} build stcrashreceiver

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysctldir}
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_userunitdir}
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_mandir}/man5
install -dm 755 %{buildroot}%{_mandir}/man7

install -pm 755 stcrashreceiver %{buildroot}%{_bindir}/
install -pm 755 stdiscosrv %{buildroot}%{_bindir}/
install -pm 755 strelaypoolsrv %{buildroot}%{_bindir}/
install -pm 755 strelaysrv %{buildroot}%{_bindir}/
install -pm 755 syncthing %{buildroot}%{_bindir}/

install -pm 644 etc/linux-systemd/system/syncthing@.service %{buildroot}%{_unitdir}/
install -pm 644 etc/linux-systemd/user/syncthing.service %{buildroot}%{_userunitdir}/

install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/
install -pm 644 man/*.5 %{buildroot}%{_mandir}/man5/
install -pm 644 man/*.7 %{buildroot}%{_mandir}/man7/

install -pm 644 etc/linux-sysctl/30-syncthing.conf %{buildroot}%{_sysctldir}/

%clean
rm -rf %{buildroot}

%post
%systemd_post 'syncthing@.service'
%systemd_user_post syncthing.service
%sysctl_apply 30-syncthing.conf

%preun
%systemd_preun 'syncthing@*.service'
%systemd_user_preun syncthing.service

%postun
%systemd_postun_with_restart 'syncthing@*.service'
%systemd_user_postun_with_restart syncthing.service

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%config(noreplace) %{_sysctldir}/30-syncthing.conf
%{_bindir}/syncthing
%{_unitdir}/syncthing@.service
%{_userunitdir}/syncthing.service
%{_mandir}/man1/syncthing.*
%{_mandir}/man5/syncthing-*.*
%{_mandir}/man7/syncthing-*.*

%files tools
%defattr(-,root,root,-)
%doc LICENSE AUTHORS
%{_bindir}/stdiscosrv
%{_bindir}/strelaysrv
%{_bindir}/strelaypoolsrv
%{_bindir}/stcrashreceiver
%{_mandir}/man1/stdiscosrv.*
%{_mandir}/man1/strelaysrv.*

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.29.5-0
- https://github.com/syncthing/syncthing/releases/tag/v1.29.5

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.29.2-0
- https://github.com/syncthing/syncthing/releases/tag/v1.29.2

* Tue Dec 03 2024 Anton Novojilov <andy@essentialkaos.com> - 1.28.1-0
- Initial build for kaos repo
