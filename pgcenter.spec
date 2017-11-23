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
Version:            0.4.0
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/lesovsky/pgcenter

Source0:            https://github.com/lesovsky/%{name}/archive/%{version}.tar.gz

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
install -dm 755 %{buildroot}%{_mandir}/man1

%{make_install}

%{__make} install-man PREFIX=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/*.sql
%{_mandir}/man1/%{name}.1.*

###############################################################################

%changelog
* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-0
- PostgreSQL 10 support
- Extended general overview
- Add xact_age and time_age fields into pg_stat_replications
- Add backend_type into pg_stat_activity
- Add stats_age into pg_stat_database
- Some bug fixes and code optimizations

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- use qsort_r() instead of hand-made sorting - sort is now available for all
  columns;
- add filtration feature - it's possible to filter out unnecessary
  tables/indexes/queries/etc;
- add pg_stat_progress_vacuum (since 9.6);
- add compatibility with pg-9.6 (pg_stat_activity) - added wait_event and
  wait_event_type fields;
- added autovacuum info: print number of user vacuum and autovac max worker
  limit;
- exclude (auto)vacuum tasks accounting in xact_maxtime field;
- pg_stat_replication rewritten and now works on standbys too;
- change long queries min age from 500ms to 0ms - now all queries are shown
  in activity stats;
- allow to use connection settings from libpq env vars;
- pg_stat_statements: add local IO information context;
- pg_stat_statements: use menu and switching; c, v, V hotkeys are removed
  and X is used instead;
- remove unnecessary WHERE from pg_stat_statements queries;
- show details and hint if query has failed;
- and many many fixes and internal refactoring.

* Sat Dec 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.2.0-0
- Added iostat
- Added nicstat
- pg_stat_statements fixes
- One key shortcut for config editing
- Other fixes and improvements

* Wed Oct 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- Added pg_stat_statements improvements
- Added query detailed report based on pg_stat_statements
- Added memory system statistics
- Added support for 9.1

* Wed Sep 09 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.2-0
- Initial build
