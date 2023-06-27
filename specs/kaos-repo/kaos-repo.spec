################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define fm_config  %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf
%define pr_config  %{_sysconfdir}/yum/pluginconf.d/priorities.conf

################################################################################

%define key_name RPM-GPG-KEY-ESSENTIALKAOS

################################################################################

Summary:         ESSENTIAL KAOS Public Repository
Name:            kaos-repo
Version:         12.0
Release:         0%{?dist}
License:         Apache License, Version 2.0
Vendor:          ESSENTIAL KAOS
Group:           Development/Tools
URL:             https://kaos.sh/kaos-repo

Source0:         kaos-release.repo
Source1:         kaos-testing.repo

Source10:        %{key_name}-SHA1
Source11:        %{key_name}-SHA2

Source100:       checksum.sha512

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
This package contains yum/dnf configuration files for access to ESSENTIAL KAOS
YUM repository.

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

%if 0%{?rhel} >= 8
install -pm 644 %{SOURCE11} \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg/%{key_name}
%else
sed -i '/module_hotfixes/d' %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo
install -pm 644 %{SOURCE10} \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg/%{key_name}
%endif

%post
if [[ -f %{fm_config} ]] ; then
  if ! grep -q 'kaos' %{fm_config} ; then
    sed -i 's/^exclude.*/\0, kaos/g' %{fm_config}
    sed -i 's/^#exclude.*/exclude=kaos/g' %{fm_config}
  fi
fi

if [[ -f %{pr_config} ]] ; then
  if ! grep -q 'check_obsoletes=1' ; then
    echo 'check_obsoletes=1' >> %{pr_config}
  fi
fi

if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
  if ! grep -q 'ESSENTIALKAOS' %{_sysconfdir}/abrt/gpg_keys ; then
    echo "%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ESSENTIALKAOS" >> %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%postun
if [[ $1 -eq 0 ]] ; then
  if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
    sed -i '/ESSENTIALKAOS/d' %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

################################################################################

%changelog
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
