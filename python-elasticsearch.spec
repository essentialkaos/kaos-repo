########################################################################################

%define package_name      elasticsearch
%define source_name       %{package_name}-py

########################################################################################

Summary:        Python client for Elasticsearch 2.x
Name:           python-%{package_name}
Version:        2.4.0
Release:        0%{?dist}
License:        ASLv2.0
Group:          Development/Libraries
URL:            https://github.com/elastic/elasticsearch-py

Source:         https://github.com/elastic/%{source_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Official low-level client for Elasticsearch. Its goal is to provide common ground for 
all Elasticsearch-related code in Python; because of this it tries to be opinion-free 
and very extendable.

########################################################################################

%prep
%setup -qn %{source_name}-%{version}

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

########################################################################################

%changelog
* Tue Sep 06 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.4.0-0
- Initial build
