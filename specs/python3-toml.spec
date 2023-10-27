################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define package_name  toml
%define pypi_subpath  be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c

################################################################################

Summary:        Python Library for Tom's Obvious, Minimal Language
Name:           python3-%{package_name}
Version:        0.10.2
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/uiri/toml

Source0:        https://files.pythonhosted.org/packages/%{pypi_subpath}/%{package_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python3-devel python3-setuptools

Requires:       python3

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
TOML aims to be a minimal configuration file format that's easy to read due to
obvious semantics. TOML is designed to map unambiguously to a hash table. TOML
should be easy to parse into data structures in a wide variety of languages.
This package loads toml file into python dictionary and dump dictionary into
toml file.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_name}-%{version}

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
%doc LICENSE README.rst
%{python3_sitelib}/*

################################################################################

%changelog
* Mon Mar 27 2023 Anton Novojilov <andy@essentialkaos.com> - 0.10.2-0
- Initial build for kaos repository
