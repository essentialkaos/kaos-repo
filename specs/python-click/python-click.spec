################################################################################

%define package_name      click

################################################################################

Summary:        A simple wrapper around optparse for powerful command line utilities.
Name:           python-click
Version:        6.7
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://github.com/mitsuhiko/click

Source:         https://github.com/mitsuhiko/%{package_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools

Requires:       python

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
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

################################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.7-0
- Updated to latest stable release

* Wed Nov 23 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.6-0
- Initial build
