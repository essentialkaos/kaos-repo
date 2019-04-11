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

%define package_name      elasticsearch
%define source_name       %{package_name}-py

################################################################################

Summary:        Python client for Elasticsearch 2.x
Name:           %{python_base}-%{package_name}
Version:        6.3.1
Release:        1%{?dist}
License:        ASLv2.0
Group:          Development/Libraries
URL:            https://github.com/elastic/elasticsearch-py

Source:         https://github.com/elastic/%{source_name}/archive/%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  %{python_base}-devel %{python_base}-setuptools

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

################################################################################

%prep
%setup -qn %{source_name}-%{version}

%clean
rm -rf %{buildroot}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 6.3.1-1
- Updated for compatibility with Python 3.6

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 6.3.1-0
- Updated to latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 6.2.0-0
- Updated to latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 6.1.1-0
- Updated to latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 6.0.0-0
- Updated to latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 5.4.0-0
- Updated to latest stable release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 5.3.0-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 5.1.0-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 5.0.1-0
- Updated to latest stable release

* Tue Sep 06 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.4.0-0
- Initial build
