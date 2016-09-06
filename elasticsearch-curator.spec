########################################################################################

%define package_name      curator

########################################################################################

Summary:        Utility for tending Elasticsearch indices 
Name:           elasticsearch-%{package_name}
Version:        4.0.6
Release:        0%{?dist}
License:        ASLv2.0
Group:          Development/Libraries
URL:            https://github.com/elastic/curator

Source:         https://github.com/elastic/%{package_name}/archive/v%{version}.tar.gz

BuildRequires:  python-devel python-setuptools

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
Like a museum curator manages the exhibits and collections on display, Elasticsearch 
Curator helps you curate, or manage your indices.

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
%{_bindir}/%{package_name}
%{_bindir}/es_repo_mgr

########################################################################################

%changelog
* Mon Sep 05 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 4.0.6-0
- Initial build
