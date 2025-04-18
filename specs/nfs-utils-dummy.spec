################################################################################

Summary:        NFS utilities (Dummy Package)
Name:           nfs-utils-dummy
Version:        100.0.0
Release:        0%{?dist}
Epoch:          99
License:        APLv2
Group:          Applications/System
URL:            https://github.com/essentialkaos

Source0:        https://raw.githubusercontent.com/essentialkaos/kaos-repo/refs/heads/master/LICENSE

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

################################################################################

%files
%defattr(-, root, root, -)
# No files!

################################################################################

%changelog
* Fri Oct 04 2024 Anton Novojilov <andy@essentialkaos.com> - 100.0.0-0
- Initial build
