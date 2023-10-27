################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define package_name  pycurl
%define pypi_path     a8/af/24d3acfa76b867dbd8f1166853c18eefc890fc5da03a48672b38ea77ddae

# Used cURL version fo build
# DO NOT FORGOT TO UPDATE IF NEWER VERSION IS USED!
%define curl_version  7.86.0

################################################################################

Summary:        A Python 3 interface to libcurl
Name:           python3-%{package_name}
Version:        7.45.2
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://pycurl.io

Source0:        https://files.pythonhosted.org/packages/%{pypi_path}/%{package_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  python3-devel python3-setuptools
BuildRequires:  gcc openssl-devel curl-devel >= %{curl_version}

Requires:       python3 python3-libs libcurl >= %{curl_version}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_name}-%{version}

%build
%py3_build -- --with-openssl

%install
rm -rf %{buildroot}

%{py3_install}

rm -rf %{buildroot}%{_datadir}/doc/pycurl

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING-LGPL COPYING-MIT ChangeLog README.rst doc
%{python3_sitearch}/curl/
%{python3_sitearch}/%{package_name}.*.so
%{python3_sitearch}/%{package_name}-%{version}-*.egg-info

################################################################################

%changelog
* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 7.45.2-0
- https://github.com/pycurl/pycurl/compare/REL_7_43_0_4...REL_7_45_2

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.4-0
- Updated to the latest version

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.3-0
- Updated to the latest version

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0-1
- Rebuilt with the latest version of curl
- Added CRC check for all sources

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.-1
- Hardcoded minimal required libcurl version

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0-0
- Initital build for kaos repository
