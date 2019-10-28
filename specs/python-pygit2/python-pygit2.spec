################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define package_name pygit2

################################################################################

Summary:        Python bindings for libgit2
Name:           python-pygit2
Version:        0.28.2
Release:        0%{?dist}
License:        GPLv2 with linking exception
Group:          Development/Libraries
URL:            https://www.pygit2.org

Source:         https://github.com/libgit2/%{package_name}/archive/v%{version}/%{package_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  gcc python-devel >= 2.7 python-setuptools
BuildRequires:  libgit2-devel openssl-devel
BuildRequires:  python-cffi python-nose python-six python-backports-ssl_match_hostname

Requires:       python >= 2.7 python-cffi python-six python-backports-ssl_match_hostname

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
pygit2 is a set of Python bindings to the libgit2 library, which implements
the core of Git.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_name}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitearch}/*

################################################################################

%changelog
* Wed Oct 23 2019 Andrey Kulikov <avk@brewkeeper.net> - 0.28.2-0
- Initial build
