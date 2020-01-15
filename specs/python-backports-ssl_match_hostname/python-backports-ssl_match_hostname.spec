################################################################################

%define pkgname     backports-ssl_match_hostname
%define module_name backports.ssl_match_hostname
%define pypi_path   76/21/2dc61178a2038a5cb35d14b61467c6ac632791ed05131dda72c20e7b9e23

################################################################################

Summary:        The ssl.match_hostname() function from Python 3
Name:           python-%{pkgname}
Version:        3.5.0.1
Release:        1%{?dist}
License:        Python
Group:          Development/Languages
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname

Source:         https://pypi.python.org/packages/%{pypi_path}/%{module_name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools python-backports

Requires:       python python-backports

Provides:       %{name} = %{verion}-%{release}
Provides:       python2-%{pkgname} = %{verion}-%{release}

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
The actual code is only slightly modified from Python 3.5.

################################################################################

%prep
%setup -qn %{module_name}-%{version}

rm backports/__init__.py

cp backports/ssl_match_hostname/README.txt .
cp backports/ssl_match_hostname/LICENSE.txt .

%build
CFLAGS="%{optflags}" python setup.py build

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/backports*

################################################################################

%changelog
* Wed Oct 23 2019 Andrey Kulikov <avk@brewkeeper.net> - 3.5.0.1-1
- Added backports python module to the build and install requirements list

* Sat Mar 17 2018 Anton Novojilov <andy@essentialkaos.com> - 3.5.0.1-0
- Initial build for kaos repository
