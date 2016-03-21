## Extra macros ################################################################

%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock

%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include

## Info ########################################################################

Summary:            Tool for installing and managing Python packages
Name:               pip
Version:            8.1.1
Release:            0%{?dist}
License:            MIT
Group:              Development/Libraries
URL:                http://www.pip-installer.org/
Vendor:             Python Packaging Authority

Source0:            http://pypi.python.org/packages/source/p/pip/%{name}-%{version}.tar.gz

BuildArch:          noarch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           python-setuptools python-devel
BuildRequires:      python-devel python-setuptools-devel

Provides:           %{name} = %{version}-%{release}

%description
pip is a tool for installing and managing Python packages, 
such as those found in the Python Package Index. 
It’s a replacement for easy_install.

## Build & Install #############################################################

%prep
%setup -q
%{__sed} -i '1d' %{name}/__init__.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf %{buildroot}%{_bindir}/%{name}-*

%clean
%{__rm} -rf %{buildroot}

## Files #######################################################################

%files
%defattr(-, root, root, -)
%doc PKG-INFO docs
%attr(755, root, root) %{_bindir}/%{name}*
%{python_sitelib}/%{name}*

## Changelog ###################################################################

%changelog
* Sun Mar 20 2016 Gleb Goncharov <yum@gongled.ru> - 8.1.1-0
- Updated to latest stable release

* Wed Jan 22 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Updated to latest stable release

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- Updated to latest stable release

* Mon Nov 18 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- Updated to latest stable release

* Thu Apr 11 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- Updated to latest stable release

* Thu Apr 11 2013 Anton Novojilov <andy@essentialkaos.com> - 1.3-0
- Updated to latest stable release

* Fri Jun 29 2012 Anton Novojilov <andy@essentialkaos.com> - 1.1-0
- Updated to latest stable release
