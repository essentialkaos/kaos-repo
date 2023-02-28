################################################################################

%global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")

################################################################################

%global pkgname       enchant
%define pypi_subpath  9e/54/04d88a59efa33fefb88133ceb638cdf754319030c28aadc5a379d82140ed

################################################################################

Summary:        Python bindings for Enchant spellchecking library
Name:           python-%{pkgname}
Version:        2.0.0
Release:        0%{?dist}
License:        LGPLv2+
Group:          Development/Languages
URL:            https://pypi.org/project/pyenchant/

Source0:        https://pypi.python.org/packages/%{pypi_subpath}/py%{pkgname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-setuptools python-devel enchant-devel

Requires:       python enchant

Provides:       PyEnchant = %{version}-%{release}
Provides:       python2-%{pkgname} = %{version}-%{release}

################################################################################

%description
PyEnchant is a spellchecking library for Python, based on the Enchant
library by Dom Lachowicz.

################################################################################

%prep
%setup -qn pyenchant-%{version}

%build
%{py2_build}

%install
rm -rf %{buildroot}

%{py2_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt TODO.txt
%{python_sitelib}/*

################################################################################

%changelog
* Sun Feb 26 2023 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Rebuilt from scratch
