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

###############################################################################

Summary:           A Curl-like tool for humans
Name:              httpie
Version:           0.8.0
Release:           0%{?dist}
License:           BSD
Group:             Applications/Internet
URL:               https://github.com/jakubroztocil/httpie

Source0:           https://github.com/jakubroztocil/%{name}/archive/%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          python python-pygments python-argparse
Requires:          python-requests python-setuptools

BuildRequires:     python python-pygments python-requests python-setuptools
BuildRequires:     python-argparse sed

###############################################################################

%description
HTTPie is a CLI HTTP utility built out of frustration with existing tools. The
goal is to make CLI interaction with HTTP-based services as human-friendly as
possible.

HTTPie does so by providing an http command that allows for issuing arbitrary
HTTP requests using a simple and natural syntax and displaying colorized
responses.

###############################################################################

%prep
%setup -qn %{name}-%{version}
sed -i '/#!\/usr\/bin\/env/d' %{name}/__main__.py
sed -i 's/Pygments>=1.5/Pygments>=1.1/' setup.py
sed -i 's/requests>=2.0.0/requests>=1.1.0/' setup.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}*
%{_bindir}/http

###############################################################################

%changelog
* Tue Jul 29 2014 Anton Novojilov <andy@essentialkaos.com> - 0.8.0-0
- Initial build
