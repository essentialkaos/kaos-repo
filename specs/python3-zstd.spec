################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
