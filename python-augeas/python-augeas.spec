################################################################################

%define __python2 %{_bindir}/python
%{!?python2_sitelib: %define python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

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

%define pkg_name          python-augeas
%define pypi_subpath      b4/d7/62d335d9df28e2f78207dcd12bbbcee89a7b5ba6d247feaddc9d04f27e1e

################################################################################

Summary:          Python bindings for Augeas
Name:             python-augeas
Version:          1.0.3
Release:          0%{?dist}
License:          LGPL-2.1
Group:            Development/Languages
URL:              http://augeas.net

Source0:          https://pypi.python.org/packages/%{pypi_subpath}/%{pkg_name}-%{version}.tar.gz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    python-devel python-setuptools libffi-devel augeas-libs

Requires:         augeas-libs

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Pure python bindings for augeas http://augeas.net

################################################################################

%prep
%setup -qn %{pkg_name}-%{version}

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}

%{__python2} setup.py install --skip-build --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS README.txt COPYING
%{python2_sitelib}/*

################################################################################

%changelog
* Wed Apr 11 2018 Andrey Kulikov <avk@brewkeeper.net> - 1.0.3-0
- Initial build
