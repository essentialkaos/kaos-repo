################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%global pkgname       enchant
%define pypi_subpath  b1/a3/86763b6350727ca81c8fcc5bb5bccee416e902e0085dc7a902c81233717e

################################################################################

Summary:        Python bindings for Enchant spellchecking library
Name:           python3-%{pkgname}
Version:        3.2.2
Release:        0%{?dist}
License:        LGPLv2+
Group:          Development/Languages
URL:            https://pypi.org/project/pyenchant/

Source0:        https://pypi.python.org/packages/%{pypi_subpath}/py%{pkgname}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.5 python3-setuptools enchant-devel

Requires:       python3 >= 3.5 enchant

Provides:       PyEnchant = %{version}-%{release}

################################################################################

%description
PyEnchant is a spellchecking library for Python, based on the Enchant
library by Dom Lachowicz.

################################################################################

%prep
%{crc_check}

%setup -qn pyenchant-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst Changelog
%{python3_sitelib}/*

################################################################################

%changelog
* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Add support for Python 3.10

* Sun Oct 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-2
- Added enchant package to dependencies

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-1
- Updated for compatibility with Python 3.6

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Removed deprecated `is_in_session` method, for compatibility
  with enchant 2.

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.11-0
- Updated to the latest stable release

* Tue Dec 13 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.8-0
- Initial build for kaos repo
