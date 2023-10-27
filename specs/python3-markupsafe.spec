################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define pypi_path  95/7e/68018b70268fb4a2a605e2be44ab7b4dd7ce7808adae6c5ef32e34f4b55a

################################################################################

Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
Name:           python3-markupsafe
Version:        2.1.2
Release:        0%{?dist}
License:        BSD
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/MarkupSafe

Source0:        https://pypi.python.org/packages/%{pypi_path}/MarkupSafe-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python3-devel >= 3.7 python3-setuptools gcc

Requires:       python3 >= 3.7

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
A library for safe markup escaping.

################################################################################

%prep
%{crc_check}

%setup -qn MarkupSafe-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

rm -f %{buildroot}%{python3_sitearch}/markupsafe/*.c

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.rst README.rst
%{python3_sitearch}/*

################################################################################

%changelog
* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.1.2-0
- https://markupsafe.palletsprojects.com/en/2.1.x/changes/#version-2-1-2

* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- https://markupsafe.palletsprojects.com/en/2.0.x/changes/#version-2-0-1

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Updated to the latest version

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 1.0-1
- Updated for compatibility with Python 3.6

* Mon May 15 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Initial build for kaos repository
