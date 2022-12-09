################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%if 0%{?rhel} == 7
%global python_base  python36
%global __python3  %{_bindir}/python3.6
%endif

%if 0%{?rhel} == 8
%global python_base  python38
%global __python3  %{_bindir}/python3.8
%endif

%if 0%{?rhel} == 9
%global python_base  python3
%global __python3  %{_bindir}/python3
%endif

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

Summary:        High productivity build system
Name:           meson
Version:        0.64.1
Release:        0%{?dist}
License:        ASL 2.0
Group:          Development/Tools
URL:            https://mesonbuild.com

Source0:        https://github.com/mesonbuild/meson/releases/download/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{python_base}-devel
BuildRequires:  %{python_base}-setuptools

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
%py3_build

%install
rm -rf %{buildroot}

%py3_install

install -dm 0755 %{buildroot}%{_sharedstatedir}/rpm/macros.d
install -pm 0644 data/macros.%{name} \
                 %{buildroot}%{_sharedstatedir}/rpm/macros.d/macros.%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/%{name}
%{python3_sitelib}/mesonbuild/
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy
%{_sharedstatedir}/rpm/macros.d/macros.%{name}

################################################################################

%changelog
* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.64.1-0
- https://github.com/mesonbuild/meson/compare/0.64.0...0.64.1

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.58.2-0
- Initial build
