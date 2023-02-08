################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define package_name  pybeam

################################################################################

Summary:        Python module to parse Erlang BEAM files
Name:           python3-%{package_name}
Version:        0.7
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/matwey/pybeam

Source0:        https://github.com/matwey/%{package_name}/archive/refs/tags/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python3-construct >= 2.9
BuildRequires:  python3-devel python3-setuptools python3-sphinx

Requires:       python3 python3-construct >= 2.9 python3-six >= 1.4.0

Provides:       %{name} = %{version}-%{release}
Provides:       python3-beam = %{version}-%{release}

################################################################################

%description
Python module to parse Erlang BEAM files.

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
%doc LICENSE README.md
%{python3_sitelib}/*

################################################################################

%changelog
* Mon Feb 06 2023 Anton Novojilov <andy@essentialkaos.com> - 0.7-0
- Initial build for kaos repository
