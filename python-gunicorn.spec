###############################################################################

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

%define upstream_name     gunicorn

###############################################################################

Summary:           Python WSGI application server
Name:              python-%{upstream_name}
Version:           18.0
Release:           0%{?dist}
License:           MIT
Group:             Applications/Internet
URL:               http://gunicorn.org/

Source0:           http://pypi.python.org/packages/source/g/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch
Requires:          python-setuptools
BuildRequires:     python2-devel python-setuptools python-nose

###############################################################################

%description
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork 
worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly 
compatible with various web frameworks, simply implemented, light on server 
resources, and fairly speedy.

###############################################################################

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc LICENSE NOTICE README.rst THANKS
%{python_sitelib}/%{upstream_name}*
%{_bindir}/%{upstream_name}
%{_bindir}/%{upstream_name}_django
%{_bindir}/%{upstream_name}_paster

###############################################################################

%changelog
* Mon Sep 30 2013 Anton Novojilov <andy@essentialkaos.com> - 18.0-0
- Created spec based on epel package






