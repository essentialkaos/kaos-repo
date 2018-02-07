################################################################################

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?rhel} == 5
%define __python /usr/bin/python26
%endif

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
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
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
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

%define shortname         s3

################################################################################

Summary:         Command line tool for managing Amazon S3 and CloudFront services
Name:            s3cmd
Version:         2.0.1
Release:         0%{?dist}
Group:           Applications/System
License:         GPL
URL:             http://s3tools.org/s3cmd

Source0:         https://github.com/s3tools/%{name}/archive/v%{version}.tar.gz

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        python python-dateutil

BuildRequires:   python python-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
S3cmd lets you copy files from/to Amazon S3 (Simple Storage Service) using a
simple to use command line client. Supports rsync-like backup, GPG encryption,
and more. Also supports management of Amazons CloudFront content delivery
network.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
export S3CMD_PACKAGING=1

%{__python} setup.py build

%install
rm -rf %{buildroot}

export S3CMD_PACKAGING=1

%{__python} setup.py install --root=%{buildroot} --prefix=%{_prefix}
%{__ln_s} %{name} %{buildroot}%{_bindir}/%{shortname}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md NEWS LICENSE
%{_bindir}/*
%{python_sitelib}/*

################################################################################

%changelog

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Updated to latest release

* Thu Mar 10 2016 Gleb Goncharov <yum@gongled.ru> - 1.6.1-1
- Fixed incompatibility with CentOS/RHEL 7.x

* Thu Feb 04 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to latest release

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to latest release

* Wed Aug 20 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-rc1
- Updated to release candidate 1

* Sat Dec 21 2013 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-b1
- Initial build
