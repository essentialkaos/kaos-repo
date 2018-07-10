################################################################################

Summary:        Ansible linter
Name:           ansible-lint
Version:        3.4.23
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/willthames/ansible-lint

Source:         https://github.com/willthames/ansible-lint/archive/v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools libffi-devel

Requires:       ansible python-jinja2 < 2.9 python-markupsafe >= 0.23

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
ansible-lint checks playbooks for practices and behaviour that could potentially
be improved.

################################################################################

%prep
%setup -qn %{name}-%{version}

%clean
rm -rf %{buildroot}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/%{name}

################################################################################

%changelog
* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.23-0
- Updated to latest stable release

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.21-0
- Updated to latest stable release

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.20-0
- Updated to latest stable release

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.17-0
- Updated to latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.15-0
- Updated to latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.13-0
- Updated to latest stable release

* Sat Mar 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.12-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.11-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.10-0
- Updated to latest stable release

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.3.3-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.5-0
- Updated to latest stable release

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
