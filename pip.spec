################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

################################################################################

Summary:            Tool for installing and managing Python packages
Name:               pip
Version:            9.0.1
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://github.com/pypa/pip

Source0:            https://github.com/pypa/%{name}/archive/%{version}.tar.gz

BuildArch:          noarch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           python-setuptools python-devel
BuildRequires:      python-devel python-setuptools-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
pip is a tool for installing and managing Python packages, such as those found in the 
Python Package Index. It’s a replacement for easy_install.

################################################################################

%prep
%setup -qn %{name}-%{version}

%{__sed} -i '1d' %{name}/__init__.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_bindir}/%{name}-*

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc docs AUTHORS.txt CHANGES.txt LICENSE.txt MANIFEST.in README.rst
%attr(755, root, root) %{_bindir}/%{name}*
%{python_sitelib}/%{name}*

################################################################################

%changelog
* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 9.0.1-0
- Correct the deprecation message when not specifying a --format so that it
  uses the correct setting name (format) rather than the incorrect one
  (list_format).
- Fix "pip check" to check all available distributions and not just the
  local ones.
- Fix a crash on non ASCII characters from lsb_release.
- Fix an SyntaxError in an an used module of a vendored dependency.
- Fix UNC paths on Windows.

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 8.1.2-0
- Fix a regression on systems with uninitialized locale.
- Use environment markers to filter packages before determining if a
  required wheel is supported.
- Make glibc parsing for `manylinux1` support more robust for the variety of
  glibc versions found in the wild.
- Update environment marker support to fully support PEP 508 and legacy
  environment markers.
- Always use debug logging to the ``--log`` file.
- Don't attempt to wrap search results for extremely narrow terminal windows.

* Sun Mar 20 2016 Gleb Goncharov <yum@gongled.ru> - 8.1.1-0
- Fix regression with non-ascii requirement files on Python 2 and add support
  for encoding headers in requirement files.

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
