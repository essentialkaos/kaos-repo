################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _lib32            %{_posixroot}lib
%define _libdir32         %{_prefix}%{_lib32}

################################################################################

%define commit_sha 3db7d31e1e76f04c8f59a7fb8402d3964d42e9d3

################################################################################

Summary:           Yum plugin to lock specified packages from being updated
Name:              yum-plugin-versionlock
Version:           1.1.31
Release:           100%{?dist}
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
This plugin takes a set of name/versions for packages and excludes all other
versions of those packages (including optionally following obsoletes). This
allows you to protect packages from being updated by newer versions,
for example.

################################################################################

%prep
%{crc_check}

%setup -qn yum-utils-%{commit_sha}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir32}/yum-plugins/
install -dm 755 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -dm 755 %{buildroot}%{_mandir}/man1/
install -dm 755 %{buildroot}%{_mandir}/man5/

install -pm 0644 plugins/versionlock/versionlock.conf \
                 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -pm 0644 plugins/versionlock/versionlock.list \
                 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -pm 0644 plugins/versionlock/versionlock.py \
                 %{buildroot}%{_libdir32}/yum-plugins/

install -pm 0644 docs/yum-versionlock.1 \
                 %{buildroot}%{_mandir}/man1/
install -pm 0644 docs/yum-versionlock.conf.5 \
                 %{buildroot}%{_mandir}/man5/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.conf
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/versionlock.list
%{_libdir32}/yum-plugins/versionlock.*
%{_mandir}/man1/yum-versionlock.1.*
%{_mandir}/man5/yum-versionlock.conf.5.*

################################################################################

%changelog
* Mon Sep 26 2022 Anton Novojilov <andy@essentialkaos.com> - 1.1.31-0
- Initial build for kaos repository
