################################################################################

%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?rhel} > 6 || 0%{?fedora} > 12
%global __python2 /usr/bin/python
%else
%global __python2 /usr/bin/python2.6
%endif

%if 0%{?rhel} == 0 && 0%{?fedora} == 0
%global rhel5 1
%endif

%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global pkgname tornado

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

Summary:            Scalable, non-blocking web server and tools
Name:               python-%{pkgname}
Version:            4.2.1
Release:            1%{?dist}
License:            ASL 2.0
Group:              Development/Libraries
URL:                http://www.tornadoweb.org

Source0:            https://pypi.python.org/packages/source/t/tornado/tornado-%{version}.tar.gz

Patch0:             python-tornado-cert.patch
Patch1:             python-tornado-netutil-cert.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel5}

BuildRequires:      python26-devel
BuildRequires:      python26-distribute
BuildRequires:      python26-backports-ssl_match_hostname
Requires:           python26-backports-ssl_match_hostname
Requires:           python26-pycurl

%else

BuildRequires:      python-devel
BuildRequires:      python-setuptools
BuildRequires:      python-backports-ssl_match_hostname
BuildRequires:      python-unittest2
Requires:           python-backports-ssl_match_hostname
Requires:           python-pycurl

%if 0%{?with_python3}
BuildRequires:      python2-devel
BuildRequires:      python3-setuptools
BuildRequires:      python3-devel
%endif

%endif

################################################################################

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

################################################################################

%package doc
Summary:            Examples for python-tornado
Group:              Documentation
Requires:           python-tornado = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

################################################################################

%if 0%{?rhel5}
%package -n python26-tornado
Summary:            Scalable, non-blocking web server and tools
Group:              Development/Libraries
Requires:           python26-backports-ssl_match_hostname
Requires:           python26-pycurl

%description -n python26-tornado
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

################################################################################

%package -n python26-tornado-doc
Summary:            Examples for python-tornado
Group:              Documentation
Requires:           python26-tornado = %{version}-%{release}

%description -n python26-tornado-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.
%endif # rhel5

################################################################################

%if 0%{?with_python3}
%package -n python3-tornado
Summary:            Scalable, non-blocking web server and tools
Group:              Development/Libraries
%description -n python3-tornado
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

################################################################################

%package -n python3-tornado-doc
Summary:            Examples for python-tornado
Group:              Documentation
Requires:           python3-tornado = %{version}-%{release}

%description -n python3-tornado-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.
%endif # with_python3

################################################################################

%prep
%setup -qc
mv %{pkgname}-%{version} python2
pushd python2
%patch0 -p1 -b .cert
%patch1 -p1 -b .cert

%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
%endif # with_python3

%build
%if 0%{?with_python3}
pushd python3
    %{__python3} setup.py build
popd
%endif # with_python3

pushd python2
    %{__python2} setup.py build
popd

%install
rm -rf %{buildroot}
%if 0%{?with_python3}
pushd python3
    PATH=$PATH:%{buildroot}%{python3_sitearch}/%{pkgname}
    %{__python3} setup.py install --root=%{buildroot}
popd
%endif # with_python3

pushd python2
    PATH=$PATH:%{buildroot}%{python2_sitearch}/%{pkgname}
    %{__python2} setup.py install --root=%{buildroot}
popd

%clean
rm -rf %{buildroot}

################################################################################

%if 0%{?rhel5}

%files -n python26-tornado
%defattr(-,root,root,-)
%doc python2/README.rst python2/PKG-INFO

%{python2_sitearch}/%{pkgname}/
%{python2_sitearch}/%{pkgname}-%{version}-*.egg-info

%files -n python26-tornado-doc
%defattr(-,root,root,-)
%doc python2/demos

%else

%files
%defattr(-,root,root,-)
%doc python2/README.rst python2/PKG-INFO

%{python2_sitearch}/%{pkgname}/
%{python2_sitearch}/%{pkgname}-%{version}-*.egg-info

%files doc
%defattr(-,root,root,-)
%doc python2/demos

%endif

%if 0%{?with_python3}
%files -n python3-tornado
%defattr(-,root,root,-)
%doc python3/README.rst python3/PKG-INFO

%{python3_sitearch}/%{pkgname}/
%{python3_sitearch}/%{pkgname}-%{version}-*.egg-info

%files -n python3-tornado-doc
%defattr(-,root,root,-)
%doc python3/demos
%endif

################################################################################

%changelog
* Fri Oct 23 2015 Gleb Goncharov <inbox@gongled.ru> - 4.2.1-1
- Initial build.

