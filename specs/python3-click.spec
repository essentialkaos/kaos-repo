################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define package_name  click

################################################################################

Summary:        A simple wrapper around optparse for powerful command line utilities
Name:           python3-click
Version:        8.1.3
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            https://github.com/mitsuhiko/click

Source0:        https://github.com/mitsuhiko/%{package_name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.7 python3-setuptools

Requires:       python3 >= 3.7

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Click is a Python package for creating beautiful command line interfaces
in a composable way with as little code as necessary. It's the "Command
Line Interface Creation Kit". It's highly configurable but comes with
sensible defaults out of the box.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_name}-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

################################################################################

%changelog
* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 8.1.3-0
- https://click.palletsprojects.com/en/8.1.x/changes/#version-8-1-3

* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 8.0.4-0
- https://click.palletsprojects.com/en/8.0.x/changes/#version-8-0-4

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.0-0
- Updated to the latest stable release

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 6.7-1
- Updated for compatibility with Python 3.6

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.7-0
- Updated to the latest stable release

* Wed Nov 23 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.6-0
- Initial build
