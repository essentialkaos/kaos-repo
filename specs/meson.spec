################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%if 0%{?rhel} == 8
%global python_base  python38
%global __python3    %{_bindir}/python3.8
%endif

%if 0%{?rhel} >= 9
%global python_base  python3
%global __python3    %{_bindir}/python3
%endif

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%global rpmmacrodir /usr/lib/rpm/macros.d

################################################################################

Summary:        High productivity build system
Name:           meson
Version:        1.8.2
Release:        0%{?dist}
License:        ASL 2.0
Group:          Development/Tools
URL:            https://github.com/mesonbuild/meson

Source0:        https://github.com/mesonbuild/meson/releases/download/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{python_base}-devel %{python_base}-setuptools
BuildRequires:  %{python_base}-wheel pyproject-rpm-macros

Requires:       %{python_base}-setuptools
Requires:       ninja-build

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Meson is a build system designed to optimize programmer productivity. It aims
to do this by providing simple, out-of-the-box support for modern software
development tools and practices, such as unit tests, coverage reports,
Valgrind, CCache and the like.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{pyproject_wheel}

%install
rm -rf %{buildroot}

%{pyproject_install}

install -dm 0755 %{buildroot}%{rpmmacrodir}
install -pm 0644 data/macros.%{name} %{buildroot}%{rpmmacrodir}/macros.%{name}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild/
%{python3_sitelib}/%{name}-*.dist-info/
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy
%{rpmmacrodir}/macros.%{name}

################################################################################

%changelog
* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 1.8.2-0
- https://github.com/mesonbuild/meson/compare/1.7.2...1.8.2

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- https://github.com/mesonbuild/meson/compare/1.6.1...1.7.2

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/mesonbuild/meson/compare/1.5.1...1.6.1

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- https://github.com/mesonbuild/meson/compare/1.4.0...1.5.1

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- https://github.com/mesonbuild/meson/compare/1.3.1...1.4.0

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- https://github.com/mesonbuild/meson/compare/1.3.0...1.3.1

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- https://github.com/mesonbuild/meson/compare/1.1.1...1.3.0

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- https://github.com/mesonbuild/meson/compare/1.1.0...1.1.1

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.64.1-0
- https://github.com/mesonbuild/meson/compare/0.64.0...0.64.1

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.61.5-0
- Initial build
