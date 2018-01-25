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

Summary:            Friendly interactive shell (FISh)
Name:               fish
Version:            2.6.0
Release:            0%{?dist}
License:            GPL2
Group:              System Environment/Shells
URL:                http://fishshell.com

Source0:            %{url}/files/%{version}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      ncurses-devel gettext gcc-c++ autoconf

Requires:           bc python which man

################################################################################

%description
fish is a shell geared towards interactive use. Its features are
focused on user friendliness and discoverability. The language syntax
is simple but incompatible with other shell languages.

################################################################################

%prep
%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
if [[ ! `grep "%{_bindir}/%{name}" %{_sysconfdir}/shells` ]] ; then
  echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
fi

%postun
if [[ $1 -eq 0 ]] ; then
  grep -v "%{_bindir}/%{name}" %{_sysconfdir}/shells > %{_sysconfdir}/%{name}.tmp
  mv %{_sysconfdir}/%{name}.tmp %{_sysconfdir}/shells
fi

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config.fish
%{_datadir}/%{name}/
%{_datadir}/doc/%{name}/
%{_datadir}/locale/*
%{_mandir}/man1/*
%{_datadir}/pkgconfig/%{name}.pc
%attr(0755,root,root) %{_bindir}/*

################################################################################

%changelog
* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Updated to latest stable release

* Mon May 23 2016 Gleb Goncharov <inbox@gongled.ru> - 2.3.0-0
- Updated to latest stable release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest stable release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.2-0
- Updated to latest stable release

* Fri Oct 10 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Updated to latest stable release

* Fri Dec 27 2013 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- Initial build
