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

%define short_name        raven
%define pkg_name          raven-python

################################################################################

Summary:          Python client for Sentry
Name:             python-raven
Version:          6.6.0
Release:          0%{?dist}
License:          BSD
Group:            Development/Libraries
URL:              https://pypi.python.org/pypi/raven/

Source0:          https://github.com/getsentry/%{pkg_name}/archive/%{version}.tar.gz

Patch0:           raven-use-system-cacert.patch
Patch1:           raven-setuptools.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    python-devel python-setuptools
BuildRequires:    python34-devel python34-setuptools

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Raven is a Python client for Sentry <http://getsentry.com>. It provides full
out-of-the-box support for many of the popular frameworks, including Django,
and Flask. Raven also includes drop-in support for any WSGI-compatible web
application.

################################################################################

%package -n python34-raven
Summary:          Python client for Sentry
Group:            Development/Libraries

Provides:         python34-raven = %{version}-%{release}

%description -n python34-raven
Raven is a Python client for Sentry <http://getsentry.com>. It provides full
out-of-the-box support for many of the popular frameworks, including Django,
and Flask. Raven also includes drop-in support for any WSGI-compatible web
application.

################################################################################

%prep
%setup -qn %{pkg_name}-%{version}
%patch0 -p1
%patch1 -p1

rm -f %{short_name}/data/cacert.pem
rm -fr %{short_name}/data
rm -fr %{py3dir}
cp -a . %{py3dir}

%build
pushd %{py3dir}
    %{__python3} setup.py build
popd

%{__python2} setup.py build

%install
rm -rf %{buildroot}

pushd %{py3dir}
    %{__python3} setup.py install --skip-build --root=%{buildroot}
    mv %{buildroot}%{_bindir}/%{short_name} %{buildroot}%{_bindir}/python34-%{short_name}
popd

%{__python2} setup.py install --skip-build --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS README.rst LICENSE
%{_bindir}/%{short_name}
%{python2_sitelib}/*

%files -n python34-raven
%defattr(-,root,root,-)
%doc AUTHORS README.rst LICENSE
%{_bindir}/python34-%{short_name}
%{python3_sitelib}/*

################################################################################

%changelog
* Fri Mar 23 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.6.0-0
- Initial build.

