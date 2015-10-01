##########################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
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

###########################################################################

%define shortname       mtl

###########################################################################

Summary:          View one or multiple files like tail but with multiple windows
Name:             multitail
Version:          6.4.2
Release:          0%{?dist}
License:          GPL
Group:            Applications/Text
URL:              http://www.vanheusden.com/%{name}/

Source:           http://www.vanheusden.com/%{name}/%{name}-%{version}.tgz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    make gcc ncurses-devel
Requires:         ncurses

Provides:         %{name} = %{version}-%{release}
Provides:         %{shortname} = %{version}-%{release}

%description
MultiTail lets you view one or multiple files like the original tail
program. The difference is that it creates multiple windows on your console
(with ncurses). Merging of 2 or even more logfiles is possible. It can also
use colors while displaying the logfiles (through regular expressions), for
faster recognition of what is important and what not. It can also filter
lines (again with regular expressions). It has interactive menus for editing
given regular expressions and deleting and adding windows.

###########################################################################

%prep
%setup -q

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man1/
install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}

%{__make} install DESTDIR="%{buildroot}"

rm -f %{buildroot}%{_sysconfdir}/%{name}.conf.new
rm -rf %{buildroot}%{_sysconfdir}/%{name}/

install -pm 644 %{name}.conf %{buildroot}%{_sysconfdir}
install -pm 755 conversion-scripts/* %{buildroot}%{_loc_datarootdir}/%{name}/

rm -f %{buildroot}%{_loc_datarootdir}/%{name}/convert-geoip.pl

ln -sf %{_bindir}/%{name} %{buildroot}%{_bindir}/%{shortname}

%clean
rm -rf %{buildroot}

###########################################################################

%files
%defattr(-, root, root, 0755)
%doc readme.txt license.txt
%doc %{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/%{shortname}
%{_loc_datarootdir}/%{name}/*

###########################################################################

%changelog
* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 6.4.2-0
- Updated to lastes stable release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 6.4.1-0
- Updated to lastes stable release

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 6.2.1-0
- Updated to lastes stable release

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 6.0-0
- Updated to release 6.0

* Mon Sep 30 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.13-3
- Small improvements

* Wed Aug 21 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.13-0
- Updated to release 5.2.13

* Wed Jun 19 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.12-0
- Updated to release 5.2.12
