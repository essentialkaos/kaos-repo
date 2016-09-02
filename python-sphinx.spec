########################################################################################

%define package_name      sphinx

########################################################################################

Summary:        Python documentation generator 
Name:           python-sphinx
Version:        1.4.6
Release:        0%{?dist}
License:        BSD 
Group:          Development/Libraries
URL:            http://www.sphinx-doc.org

Source:         https://github.com/sphinx-doc/%{package_name}/archive/%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Sphinx is a tool that makes it easy to create intelligent and beautiful documentation, 
written by Georg Brandl and licensed under the BSD license.

########################################################################################

%prep
%setup -qn %{package_name}-%{version}

%clean
rm -rf %{buildroot}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%attr(755,root,root) %{_bindir}/%{package_name}-apidoc
%attr(755,root,root) %{_bindir}/%{package_name}-autogen
%attr(755,root,root) %{_bindir}/%{package_name}-build
%attr(755,root,root) %{_bindir}/%{package_name}-quickstart

########################################################################################

%changelog
* Fri Sep 02 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.4.6-0
- Initial build
