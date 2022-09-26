################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _lib32            %{_posixroot}lib
%define _libdir32         %{_prefix}%{_lib32}

################################################################################

%define commit_sha 3db7d31e1e76f04c8f59a7fb8402d3964d42e9d3

################################################################################

Summary:           Yum plugin to give priorities to packages from different repos
Name:              yum-plugin-priorities
Version:           1.1.31
Release:           0%{?dist}
License:           GPLv2+
Group:             System Environment/Base
URL:               https://github.com/rpm-software-management/yum-utils

Source0:           https://github.com/rpm-software-management/yum-utils/archive/%{commit_sha}.zip

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          yum

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
This plugin allows repositories to have different priorities.
Packages in a repository with a lower priority can't be overridden by packages
from a repository with a higher priority even if repo has a later version.

################################################################################

%prep
%{crc_check}

%setup -qn yum-utils-%{commit_sha}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir32}/yum-plugins/
install -dm 755 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/

install -pm 0644 plugins/priorities/priorities.conf \
                 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -pm 0644 plugins/priorities/priorities.py \
                 %{buildroot}%{_libdir32}/yum-plugins/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/priorities.conf
%{_libdir32}/yum-plugins/priorities.*

################################################################################

%changelog
* Mon Sep 26 2022 Anton Novojilov <andy@essentialkaos.com> - 1.1.31-0
- Initial build for kaos repository
