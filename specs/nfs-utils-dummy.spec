################################################################################

Summary:        NFS utilities (Dummy Package)
Name:           nfs-utils-dummy
Version:        0.0.0
Release:        0%{?dist}
Epoch:          99
License:        Apache
Group:          Applications/System
URL:            https://github.com/essentialkaos

Source0:        LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       %{name} = %{version}-%{release}
Provides:       nfs-utils = %{version}-%{release}

################################################################################

%description
This is a dummy package that replaces the outdated nfs-utils package.

################################################################################

%prep
%build

%install
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
# No files!

################################################################################

%changelog
* Fri Oct 04 2024 Anton Novojilov <andy@essentialkaos.com> - 0.0.0-0
- Initial build
