################################################################################

%global __python26 /usr/bin/python2.6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

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
Name:             python-libcloud
Version:          2.2.1
Release:          0%{?dist}
License:          ASL 2.0
Group:            Development/Languages
URL:              http://libcloud.apache.org

Source0:          http://apache-mirror.rbc.ru/pub/apache/libcloud/%{tarball_name}-%{version}.tar.bz2

BuildArch:        noarch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    python-setuptools python-devel

################################################################################

%description
libcloud is a client library for interacting with many of the popular cloud
server providers.  It was created to make it easy for developers to build
products that work between any of the services that it supports.

################################################################################

%prep
%setup -qn %{tarball_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python_sitelib}/*

################################################################################

%changelog
* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Updated to latest version

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Updated to latest version

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to latest version

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to latest version

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Updated to latest version

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 0.20.1-0
- Updated to latest version

* Fri Oct 23 2015 Gleb Goncharov <inbox@gongled.ru> - 0.18.0-0
- Initial build
