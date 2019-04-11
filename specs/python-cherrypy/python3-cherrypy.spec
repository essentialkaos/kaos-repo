################################################################################

%if 0%{?rhel} >= 7
%global python_base python36
%global __python3   %{_bindir}/python3.6
%else
%global python_base python34
%global __python3   %{_bindir}/python3.4
%endif

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

%global pkgname     cherrypy
%global pypi_path   f3/b3/de69bc6827dfe9a9bd20dd2b5752ba00bddaf0534cd3a51ee4e61767eb5b

################################################################################

Summary:            Pythonic, object-oriented web development framework
Name:               %{python_base}-%{pkgname}
Version:            13.1.0
Release:            1%{?dist}
License:            Python
Group:              Development/Libraries
URL:                http://www.cherrypy.org

Source0:            https://pypi.python.org/packages/%{pypi_path}/CherryPy-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      %{python_base}-devel %{python_base}-setuptools

Requires:           %{python_base}

Provides:           %{name} = %{verion}-%{release}

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
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

find %{buildroot}%{python3_sitelib}/ -type f -exec chmod -x \{\} \;

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/cherryd
%{python3_sitelib}/*

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 13.1.0-1
- Updated for compatibility with Python 3.6

* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 13.1.0-0
- Initial build for kaos repository
