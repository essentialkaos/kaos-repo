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

%define pkgname     backports-ssl_match_hostname
%define module_name backports.ssl_match_hostname
%define pypi_path   ff/2b/8265224812912bc5b7a607c44bf7b027554e1b9775e9ee0de8032e3de4b2

################################################################################

Summary:        The ssl.match_hostname() function from Python 3
Name:           %{python_base}-%{pkgname}
Version:        3.7.0.1
Release:        0%{?dist}
License:        Python
Group:          Development/Languages
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname

Source0:        https://pypi.python.org/packages/%{pypi_path}/%{module_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  %{python_base}-devel %{python_base}-setuptools

Requires:       %{python_base}

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code is only slightly modified from Python 3.7.

################################################################################

%prep
%{crc_check}

%setup -qn %{module_name}-%{version}

rm backports/__init__.py

%build
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python3_sitelib}/backports*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 3.7.0.1-0
- Updated to the latest stable release

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 3.5.0.1-1
- Updated for compatibility with Python 3.6

* Sat Mar 17 2018 Anton Novojilov <andy@essentialkaos.com> - 3.5.0.1-0
- Initial build for kaos repository
