################################################################################

Summary:        Tool for checking common errors in RPM packages
Name:           rpmlint
Version:        2.4
Release:        0%{?dist}
License:        GPLv2
Group:          Development/Tools
URL:            https://github.com/rpm-software-management/rpmlint

Source0:        https://github.com/rpm-software-management/%{name}/archive/refs/tags/%{version}.0.tar.gz

Patch0:         default-config.patch

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python3-devel >= 3.8 python3-setuptools

Requires:       cpio binutils rpm-build gzip bzip2 xz epel-release
Requires:       python3 >= 3.8 python3-rpm python3-setuptools
Requires:       python3-toml python3-pyxdg python3-beam

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
rpmlint is a tool for checking common errors in rpm packages. rpmlint can be
used to test individual packages before uploading or to check an entire
distribution. By default all applicable checks are performed but specific
checks can be performed by using command line parameters.

rpmlint can check binary rpms (files and installed ones), source rpms, and
plain specfiles, but all checks do not apply to all argument types. For
best check coverage, run rpmlint on source rpms instead of plain specfiles,
and installed binary rpms instead of uninstalled binary rpm files.

################################################################################

%prep
%setup -qn %{name}-%{version}.0

%patch0 -p1

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

install -dDm 755 %{buildroot}%{_sysconfdir}/xdg/rpmlint
install -pm 644 configs/Fedora/*.toml %{buildroot}%{_sysconfdir}/xdg/rpmlint/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md
%dir %{_sysconfdir}/xdg/rpmlint
%config(noreplace) %{_sysconfdir}/xdg/rpmlint/*.toml
%{_bindir}/rpmdiff
%{_bindir}/rpmlint
%{python3_sitelib}/*

################################################################################

%changelog
* Mon Jul 03 2023 Anton Novojilov <andy@essentialkaos.com> - 2.4-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/2.4.0

* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.3-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/2.3.0

* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/2.2.0

* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/2.1.0

* Mon Feb 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.0-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/2.0.0

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.11-0
- https://github.com/rpm-software-management/rpmlint/releases/tag/rpmlint-1.11

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.10-0
- Updated to the latest release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.9-0
- Updated to the latest release

* Sat Nov 14 2015 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- Initial build
