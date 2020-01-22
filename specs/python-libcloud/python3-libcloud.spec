################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%global tarball_name apache-libcloud

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

Summary:          A Python library to address multiple cloud provider APIs
Name:             %{python_base}-libcloud
Version:          2.8.0
Release:          0%{?dist}
License:          ASL 2.0
Group:            Development/Languages
URL:              https://libcloud.apache.org

Source0:          https://apache-mirror.rbc.ru/pub/apache/libcloud/%{tarball_name}-%{version}.tar.bz2

Source100:        checksum.sha512

BuildArch:        noarch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    %{python_base}-setuptools %{python_base}-devel

Requires:         %{python_base}

Provides:         %{name} = %{verion}-%{release}

################################################################################

%description
libcloud is a client library for interacting with many of the popular cloud
server providers.  It was created to make it easy for developers to build
products that work between any of the services that it supports.

################################################################################

%prep
%{crc_check}

%setup -qn %{tarball_name}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python3_sitelib}/*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- Updated to the latest version

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-1
- Updated for compatibility with Python 3.6

* Wed Mar 14 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Updated to the latest version

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Updated to the latest version

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Updated to the latest version

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to the latest version

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to the latest version

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Updated to the latest version

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 0.20.1-0
- Updated to the latest version

* Fri Oct 23 2015 Gleb Goncharov <inbox@gongled.ru> - 0.18.0-0
- Initial build
