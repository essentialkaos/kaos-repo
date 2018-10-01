################################################################################

%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

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

%global pkgname certifi

################################################################################

Summary:            Python package for providing Mozilla's CA Bundle
Name:               python-%{pkgname}
Version:            2018.08.24
Release:            0%{?dist}
License:            MPLv2.0
Group:              Development/Libraries
URL:                https://github.com/certifi/python-certifi

Source0:            https://github.com/certifi/%{name}/archive/%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      python-setuptools

Requires:           ca-certificates

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Certifi is a carefully curated collection of Root Certificates for
validating the trustworthiness of SSL certificates while verifying
the identity of TLS hosts. It has been extracted from the Requests project.

################################################################################

%prep
%setup -qn %{name}-%{version}

rm -rf %{pkgname}.egg-info

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python_sitelib}/*

################################################################################

%changelog
* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.08.24-0
- Updated to latest release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.04.16-0
- Updated to latest release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.01.18-0
- Updated to latest release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.11.05-0
- Updated to latest release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.07.27.1-0
- Updated to latest release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.04.17-0
- Updated to latest release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.01.23-0
- Updated to latest release

* Tue Dec 27 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.09.26-1
- Added certificates bundle to package

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.09.26-0
- Updated to latest release

* Sun Sep 11 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.8.31-0
- Initial build for kaos repo
