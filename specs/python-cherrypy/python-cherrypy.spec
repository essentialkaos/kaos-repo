################################################################################

%global pkgname     cherrypy
%global pypi_path   f3/b3/de69bc6827dfe9a9bd20dd2b5752ba00bddaf0534cd3a51ee4e61767eb5b

################################################################################

Summary:            Pythonic, object-oriented web development framework
Name:               python-%{pkgname}
Version:            13.1.0
Release:            0%{?dist}
License:            Python
Group:              Development/Libraries
URL:                http://www.cherrypy.org

Source0:            https://pypi.python.org/packages/%{pypi_path}/CherryPy-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      python-devel python-setuptools

Requires:           python

Provides:           %{name} = %{verion}-%{release}
Provides:           python2-%{pkgname} = %{verion}-%{release}

################################################################################

%description
CherryPy allows developers to build web applications in much the same way
they would build any other object-oriented Python program. This usually
results in smaller source code developed in less time.

This is a compat package for programs which still need the 2.x branch of
CherryPy.

################################################################################

%prep
%setup -qn CherryPy-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build --root %{buildroot}

find %{buildroot}%{python_sitelib}/ -type f -exec chmod -x \{\} \;

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/cherryd
%{python_sitelib}/*

################################################################################

%changelog
* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 13.1.0-0
- Initial build for kaos repository
