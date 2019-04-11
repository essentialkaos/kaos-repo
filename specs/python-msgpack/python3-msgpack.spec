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

%define pkgname    msgpack
%define pypi_path  8a/20/6eca772d1a5830336f84aca1d8198e5a3f4715cd1c7fc36d3cc7f7185091

################################################################################

Summary:        A Python MessagePack (de)serializer
Name:           %{python_base}-%{pkgname}
Version:        0.5.6
Release:        1%{?dist}
License:        ASL 2.0
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/msgpack-python/

Source:         https://pypi.python.org/packages/%{pypi_path}/%{pkgname}-python-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{python_base}-devel %{python_base}-setuptools

Requires:       %{python_base}

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
MessagePack is a binary-based efficient data interchange format that is
focused on high performance. It is like JSON, but very fast and small.
This is a Python (de)serializer for MessagePack.

################################################################################

%prep
%setup -qn %{pkgname}-python-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.rst COPYING
%{python3_sitearch}/%{pkgname}/
%{python3_sitearch}/%{pkgname}*.egg-info

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 0.5.6-1
- Updated for compatibility with Python 3.6

* Sat Mar 17 2018 Anton Novojilov <andy@essentialkaos.com> - 0.5.6-0
- Initial build for kaos repository
