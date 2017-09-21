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

###############################################################################

%define pkg_name          frei0r-plugins

###############################################################################

Summary:            A minimalistic plugin API for video effects
Name:               frei0r
Version:            1.6.1
Release:            0%{?dist}
License:            GPLv2+
Group:              System Environment/Libraries
URL:                http://frei0r.dyne.org

Source0:            https://github.com/dyne/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ automake libtool
BuildRequires:      autoconf opencv-devel >= 1.0.0 gavl-devel >= 0.2.3

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
Frei0r is a minimalistic plugin API for video effects.

The main emphasis is on simplicity for an API that will round up the
most common video effects into simple filters, sources and mixers that
can be controlled by parameters.

###############################################################################

%prep
%setup -q

%build
%{__libtoolize} --force
%{__aclocal}
%{__autoheader}
%{__automake} --force-missing --add-missing
%{__autoconf}

%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README.md TODO
%{_includedir}/%{name}.h
%{_docdir}/%{pkg_name}/*
%{_libdir}/%{name}-1/*.so
%{_pkgconfigdir}/%{name}.pc

###############################################################################

%changelog
* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to latest stable release

* Wed Apr 13 2016 Gleb Goncharov <yum@gongled.ru> - 1.5-0
- Updated to latest version 

* Mon Mar 17 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.4-0
- Updated to latest version 

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3-0
- Initial build
