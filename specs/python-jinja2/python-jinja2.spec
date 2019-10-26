################################################################################

%define package_name      jinja2

# Fix for https://github.com/pallets/jinja/issues/653
%global _python_bytecompile_errors_terminate_build 0

################################################################################

Summary:        Sandboxed template engine
Name:           python-jinja2
Version:        2.10
Release:        1%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://jinja.pocoo.org

Source:         https://github.com/mitsuhiko/%{package_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools

Requires:       python python-markupsafe

Provides:       %{name} = %{verion}-%{release}
Provides:       python2-jinja2 = %{verion}-%{release}

################################################################################

%description
Jinja is a sandboxed template engine written in pure Python. It
provides a Django-like non-XML syntax and compiles templates into
executable python code. It's basically a combination of Django
templates and python code.

################################################################################

%prep
%setup -qn jinja-%{version}

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
* Sun Oct 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.10-1
- Added python-markupsafe package to dependencies

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.10-0
- Updated to latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.6-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.5-0
- Updated to latest stable release

* Wed Aug 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Initial build
