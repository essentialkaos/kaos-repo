################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

%define package_name      click

################################################################################

Summary:        A simple wrapper around optparse for powerful command line utilities.
Name:           python34-click
Version:        6.7
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://github.com/mitsuhiko/click

Source:         https://github.com/mitsuhiko/%{package_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python34-devel python34-setuptools

Requires:       python34

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
Click is a Python package for creating beautiful command line interfaces
in a composable way with as little code as necessary. It's the "Command
Line Interface Creation Kit". It's highly configurable but comes with
sensible defaults out of the box.

################################################################################

%prep
%setup -qn %{package_name}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

################################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.7-0
- Updated to latest stable release

* Wed Nov 23 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.6-0
- Initial build
