###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
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

###############################################################################

Summary:            Top-like PostgreSQL statistics viewer
Name:               pgcenter
Version:            0.1.3
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/lesovsky/pgcenter

Source0:            https://github.com/lesovsky/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc postgresql94-devel ncurses-devel

Provides:           %{name} = %{version}-%{release} 

###############################################################################

%description
PostgreSQL provides various statistics which includes information about 
tables, indexes, functions and other database objects and their usage. 
Moreover, statistics has detailed information about connections, current 
queries and database operations (INSERT/DELETE/UPDATE). But most of this 
statistics are provided as permanently incremented counters. The pgcenter 
provides convenient interface to this statistics and allow viewing statistics 
changes in time interval, eg. per second. The pgcenter provides fast access 
for database management task, such as editing configuration files, reloading 
services, viewing log files and canceling or terminating database backends 
(by pid or using state mask). However if need execute some specific 
operations, pgcenter can start psql session for this purposes.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags} PGCONFIG=%{_prefix}/pgsql-9.4/bin/pg_config

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

%{make_install}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md
%{_bindir}/%{name}

###############################################################################

%changelog
* Wed Oct 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- Added pg_stat_statements improvements
- Added query detailed report based on pg_stat_statements
- Added memory system statistics
- Added support for 9.1

* Wed Sep 09 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.2-0
- Initial build
