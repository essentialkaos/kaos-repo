################################################################################

%define package_name      pygit2

################################################################################

Summary:        Python bindings for libgit2
Name:           python-pygit2
Version:        0.28.2
Release:        0%{?dist}
License:        GPLv2 with linking exception
Group:          Development/Libraries
URL:            http://www.pygit2.org

Source:         https://github.com/libgit2/%{package_name}/archive/v%{version}/%{package_name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  python-devel python-setuptools
BuildRequires:  libgit2-devel
BuildRequires:  openssl-devel
BuildRequires:  python-cffi
BuildRequires:  python-nose
BuildRequires:  python-six
BuildRequires:  python-backports-ssl_match_hostname

Requires:       python
Requires:       python-backports-ssl_match_hostname
Requires:       python-cffi
Requires:       python-six

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
pygit2 is a set of Python bindings to the libgit2 library, which implements
the core of Git.

################################################################################

%prep
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
