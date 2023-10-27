################################################################################

Summary:    Test spec
Name:       test
Version:    1.0.0
Release:    0%{?dist}
License:    GPLv2
Group:      Development/Tools
URL:        https://domain.com

Source0:    abcd.tar.gz

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bash
Requires:      bash

Provides:   %{name} = %{version}-%{release}

################################################################################

%description

Test spec.

################################################################################

%prep
%setup -q

%build
%{make} all

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/testapp

################################################################################

%changelog
%changelog
* Mon Feb 25 2019 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Initial build
