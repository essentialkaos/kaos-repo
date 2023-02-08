################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define package_name  zstd
%define zstd_version  1.5.2

################################################################################

Summary:        Zstd Bindings for Python
Name:           python3-%{package_name}
Version:        %{zstd_version}.6
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/sergey-dryabzhinsky/python-zstd

Source0:        https://github.com/sergey-dryabzhinsky/python-%{package_name}/archive/refs/tags/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  gcc python3-devel python3-setuptools
BuildRequires:  libzstd-devel >= %{zstd_version}

Requires:       python3 libzstd >= %{zstd_version}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Simple Python bindings for the Zstd compression library.

################################################################################

%prep
%{crc_check}

%setup -qn python-%{package_name}-%{version}

%build
# Remove bundled zstd
rm -rf zstd

%py3_build -- --legacy --external

%install
rm -rf %{buildroot}

%{py3_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python3_sitearch}/%{package_name}-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{package_name}*.so

################################################################################

%changelog
* Mon Feb 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.5.2.6-0
- Initial build for kaos repository
