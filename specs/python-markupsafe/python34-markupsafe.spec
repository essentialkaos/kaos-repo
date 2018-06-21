################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

%{!?_without_check: %define _with_check 1}

################################################################################

%define         pypi_path 4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b

################################################################################

Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
Name:           python34-markupsafe
Version:        1.0
Release:        0%{?dist}
License:        BSD
Group:          Development/Languages
URL:            http://pypi.python.org/pypi/MarkupSafe

Source:         https://pypi.python.org/packages/%{pypi_path}/MarkupSafe-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python34-devel python34-setuptools

Requires:       python34

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
A library for safe markup escaping.

################################################################################

%prep
%setup -qn MarkupSafe-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

rm -f %{buildroot}%{python_sitearch}/markupsafe/*.c

%check
%if %{?_with_check:1}%{?_without_check:0}
python setup.py test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python3_sitearch}/*

################################################################################

%changelog
* Mon May 15 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Initial build for kaos repository
