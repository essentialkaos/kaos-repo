################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}


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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

Summary:            Terminal session recorder
Name:               asciinema
Version:            2.0.2
Release:            0%{?dist}
License:            GPLv3
Group:              Applications/Internet
URL:                https://asciinema.org

Source0:            https://github.com/asciinema/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:          noarch

BuildRequires:      python34-devel python34-setuptools

Requires:           python34 python34-setuptools

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Terminal session recorder and the best companion of asciinema.org.

asciinema lets you easily record terminal sessions and replay them in a terminal
as well as in a web browser.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python3} setup.py build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_mandir}/man1/
install -pm 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/*.egg-info
%{_mandir}/man1/%{name}.1*
%{_defaultdocdir}/*

################################################################################

%changelog
* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Official support for Python 3.7
- Recording is now possible on US-ASCII locale
- Improved Android support
- Possibility of programatic recording with asciinema.record_asciicast function
- Uses new JSON response format added recently to asciinema-server
- Tweaked message about how to stop recording
- Added proper description and other metadata to Python package

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Fixed example in asciicast v2 format doc
- Replaced deprecated encodestring (since Python 3.1) with encodebytes
- Fixed location of config dir (you can mv ~/.asciinema ~/.config/asciinema)
- Internal refactorings

* Tue Mar 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Initial build for EK repository
