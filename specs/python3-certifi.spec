################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%global pkgname  certifi

################################################################################

Summary:        Python package for providing Mozilla's CA Bundle
Name:           python3-%{pkgname}
Version:        2022.12.07
Release:        0%{?dist}
License:        MPLv2.0
Group:          Development/Libraries
URL:            https://github.com/certifi/python-certifi

Source0:        https://github.com/certifi/python-%{pkgname}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python3-devel python3-setuptools

Requires:       python3 ca-certificates

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Certifi is a carefully curated collection of Root Certificates for
validating the trustworthiness of SSL certificates while verifying
the identity of TLS hosts. It has been extracted from the Requests project.

################################################################################

%prep
%{crc_check}

%setup -qn python-%{pkgname}-%{version}

rm -rf %{pkgname}.egg-info

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
* Wed Feb 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2022.12.07-0
- Updated to the latest release

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 2019.11.28-0
- Updated to the latest release

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2018.11.29-1
- Updated for compatibility with Python 3.6

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2018.11.29-0
- Updated to the latest release

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.10.15-0
- Updated to the latest release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.08.24-0
- Updated to the latest release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.04.16-0
- Updated to the latest release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.01.18-0
- Updated to the latest release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.11.05-0
- Updated to the latest release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.07.27.1-0
- Updated to the latest release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.04.17-0
- Updated to the latest release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.01.23-0
- Updated to the latest release

* Tue Dec 27 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.09.26-1
- Added certificates bundle to package

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.09.26-0
- Updated to the latest release

* Sun Sep 11 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.8.31-0
- Initial build for kaos repo
