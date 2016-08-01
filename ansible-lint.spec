########################################################################################

%define subpath b5/4f/dd446c962ff09da8df88c7698761a603ab9038fcc97ec15e1eebebf0b427

########################################################################################

Summary:        Ansible linter
Name:           ansible-lint
Version:        3.0.0
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries 
URL:            https://github.com/willthames/ansible-lint

Source:         https://pypi.python.org/packages/%{subpath}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools libffi-devel

Requires:       ansible

Provides:       %{name} = %{verion}-%{release}

########################################################################################

%description
ansible-lint checks playbooks for practices and behaviour that could potentially 
be improved.

########################################################################################

%prep
%setup -qn %{name}-%{version}

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
%{_bindir}/%{name}

########################################################################################

%changelog
* Thu Jun 23 2016 Gleb Goncharov <inbox@gongled.ru> - 3.0.0-0
- Updated to latest stable release

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- Updated to latest stable release

* Mon May 23 2016 Gleb Goncharov <inbox@gongled.ru> - 2.6.2-0
- Updated to latest stable release

* Sat Apr 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest stable release

* Tue Mar 08 2016 Gleb Goncharov <inbox@gongled.ru> - 2.3.9-0
- Initial build
