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

%define package_name pygit2

################################################################################

Summary:        Python bindings for libgit2
Name:           %{python_base}-pygit2
Version:        0.28.2
Release:        0%{?dist}
License:        GPLv2 with linking exception
Group:          Development/Libraries
URL:            https://www.pygit2.org

Source:         https://github.com/libgit2/%{package_name}/archive/v%{version}/%{package_name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  %{python_base}-devel %{python_base}-setuptools
BuildRequires:  libgit2-devel openssl-devel
BuildRequires:  %{python_base}-cffi %{python_base}-nose %{python_base}-six

Requires:       %{python_base} %{python_base}-cffi %{python_base}-six

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
pygit2 is a set of Python bindings to the libgit2 library, which implements
the core of Git.

################################################################################

%prep
%setup -qn %{package_name}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitearch}/*

################################################################################

%changelog
* Wed Oct 23 2019 Andrey Kulikov <avk@brewkeeper.net> - 0.28.2-0
- Initial build
