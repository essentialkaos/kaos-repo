################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%{!?_without_check: %define _with_check 1}

################################################################################

%define         pypi_path b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094

################################################################################

Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
Name:           %{python_base}-markupsafe
Version:        1.1.1
Release:        0%{?dist}
License:        BSD
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/MarkupSafe

Source0:        https://pypi.python.org/packages/%{pypi_path}/MarkupSafe-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{python_base}-devel %{python_base}-setuptools gcc

Requires:       %{python_base}

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
A library for safe markup escaping.

################################################################################

%prep
%{crc_check}

%setup -qn MarkupSafe-%{version}

%build
CFLAGS="%{optflags}" %{__python3} setup.py build

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
%doc LICENSE.rst README.rst
%{python3_sitearch}/*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Updated to the latest version

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.0-1
- Updated for compatibility with Python 3.6

* Mon May 15 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Initial build for kaos repository
