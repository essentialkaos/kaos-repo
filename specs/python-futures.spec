################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%global pkgname           futures
%define pypi_subpath      47/04/5fc6c74ad114032cd2c544c575bffc17582295e9cd6a851d6026ab4b2c00

################################################################################

Summary:            Backport of the concurrent.futures package from Python 3.2
Name:               python-%{pkgname}
Version:            3.3.0
Release:            0%{?dist}
License:            BSD
Group:              Development/Libraries
URL:                https://github.com/agronholm/pythonfutures

Source0:            https://pypi.python.org/packages/%{pypi_subpath}/%{pkgname}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      python-setuptools

Provides:           %{name} = %{version}-%{release}
Provides:           python2-%{pkgname} = %{version}-%{release}

################################################################################

%description
The concurrent.futures module provides a high-level interface for
asynchronously executing callables.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkgname}-%{version}

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
%doc LICENSE
%{python_sitelib}/concurrent
%{python_sitelib}/%{pkgname}-*.egg-info*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 3.3.0-0
- Updated to the latest stable release

* Wed Oct 30 2019 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-1
- Added Provides info

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- Updated to the latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- Updated to the latest stable release

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- Updated to the latest version

* Fri Oct 23 2015 Gleb Goncharov <inbox@gongled.ru> - 3.0.3-1
- Initial build
