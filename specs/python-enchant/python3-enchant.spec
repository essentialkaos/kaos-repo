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

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

%global pkgname           enchant
%define pypi_subpath      9e/54/04d88a59efa33fefb88133ceb638cdf754319030c28aadc5a379d82140ed

################################################################################

Summary:            Python bindings for Enchant spellchecking library
Name:               %{python_base}-%{pkgname}
Version:            2.0.0
Release:            1%{?dist}
License:            LGPLv2+
Group:              Development/Languages
URL:                https://pypi.org/project/pyenchant/

Source0:            https://pypi.python.org/packages/%{pypi_subpath}/py%{pkgname}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      %{python_base}-setuptools %{python_base}-devel enchant-devel

Provides:           PyEnchant = %{version}-%{release}

################################################################################

%description
PyEnchant is a spellchecking library for Python, based on the Enchant
library by Dom Lachowicz.

################################################################################

%prep
%setup -qn pyenchant-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --single-version-externally-managed

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt TODO.txt
%{python3_sitelib}/*

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-1
- Updated for compatibility with Python 3.6

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Updated to latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.11-0
- Updated to latest stable release

* Tue Dec 13 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.8-0
- Initial build for kaos repo
