################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:    ESSENTIAL KAOS Public Repository
Name:       kaos-repo
Version:    12.2
Release:    0%{?dist}
License:    Apache License, Version 2.0
Vendor:     ESSENTIAL KAOS
Group:      Development/Tools
URL:        https://kaos.sh/kaos-repo

Source0:    kaos-release.repo
Source1:    kaos-testing.repo
Source2:    RPM-GPG-KEY-ESSENTIALKAOS

Source100:  checksum.sha512

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
This package contains configuration files for access to ESSENTIAL KAOS Public
repository.

################################################################################

%prep
%{crc_check}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -dm 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -pm 644 %{SOURCE0} \
                %{buildroot}%{_sysconfdir}/yum.repos.d/
install -pm 644 %{SOURCE1} \
                %{buildroot}%{_sysconfdir}/yum.repos.d/

install -pm 644 %{SOURCE2} \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

%post
if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
  if ! grep -q 'RPM-GPG-KEY-ESSENTIALKAOS' %{_sysconfdir}/abrt/gpg_keys ; then
    echo "%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ESSENTIALKAOS" >> %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%postun
if [[ $1 -eq 0 ]] ; then
  if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
    sed -i '/RPM-GPG-KEY-ESSENTIALKAOS/d' %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ESSENTIALKAOS

################################################################################

%changelog
* Fri Oct 24 2025 Anton Novojilov <andy@essentialkaos.com> - 12.2-0
- Removed unsupported configuration options

* Thu Jan 16 2025 Anton Novojilov <andy@essentialkaos.com> - 12.1-0
- Spec refactoring

* Tue Jun 27 2023 Anton Novojilov <andy@essentialkaos.com> - 12.0-0
- Migrate from yum.kaos.st to pkgs.kaos.st

* Mon Dec 05 2022 Anton Novojilov <andy@essentialkaos.com> - 11.0-0
- Added EL8/EL9 support
- Added SHA2 key for EL8+

* Thu Jul 07 2022 Anton Novojilov <andy@essentialkaos.com> - 10.0-0
- Removed yum-plugin-priorities from required dependencies
- Spec improvements

* Wed May 29 2019 Anton Novojilov <andy@essentialkaos.com> - 9.2-0
- Added obsoletes check in priorities plugin

* Fri Feb 16 2018 Anton Novojilov <andy@essentialkaos.com> - 9.1-0
- Added bugtracker URL

* Thu Feb 01 2018 Anton Novojilov <andy@essentialkaos.com> - 9.0-0
- Migrated from kaos.io to kaos.st

* Thu Mar 23 2017 Anton Novojilov <andy@essentialkaos.com> - 8.0-0
- Dropped support of x32 arch

* Thu Nov 17 2016 Anton Novojilov <andy@essentialkaos.com> - 7.2-0
- Removed mirrors

* Thu Jun 16 2016 Anton Novojilov <andy@essentialkaos.com> - 7.1-0
- Added abrt configuration

* Thu May 05 2016 Anton Novojilov <andy@essentialkaos.com> - 7.0-0
- Added multiver configuration

* Sat Apr 02 2016 Anton Novojilov <andy@essentialkaos.com> - 6.8-1
- Fixed wrong urls of x64 repo

* Sun Oct 12 2014 Anton Novojilov <andy@essentialkaos.com> - 6.8-0
- Changed versioning scheme
