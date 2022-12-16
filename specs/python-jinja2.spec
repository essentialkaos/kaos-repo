################################################################################

%define package_name  jinja

################################################################################

Summary:        Sandboxed template engine
Name:           python-jinja
Version:        2.8
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://jinja.pocoo.org

Source:         https://github.com/mitsuhiko/%{package_name}2/archive/%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
Jinja is a sandboxed template engine written in pure Python. It
provides a Django-like non-XML syntax and compiles templates into
executable python code. It's basically a combination of Django
templates and python code.

################################################################################

%prep
%setup -qn %{package_name}-%{version}

%clean
rm -rf %{buildroot}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

################################################################################

%changelog
* Wed Aug 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Initial build
