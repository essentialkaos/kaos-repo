################################################################################

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

################################################################################

Summary:            Top-like PostgreSQL statistics viewer
Name:               pgcenter
Version:            0.6.4
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/lesovsky/pgcenter

Source0:            https://github.com/lesovsky/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make golang >= 1.13

Provides:           %{name} = %{version}-%{release}

################################################################################

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

################################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src/github.com/lesovsky/%{name}
mv * .src/github.com/lesovsky/%{name}/
mv .src src

mv src/github.com/lesovsky/%{name}/COPYRIGHT \
   src/github.com/lesovsky/%{name}/README.md \
   .

%build
export GOPATH=$(pwd)
export GO111MODULE=on

pushd src/github.com/lesovsky/%{name}

go mod download
go build -ldflags "-X main.COMMIT=000000 -X main.BRANCH=master" \
         -o "$GOPATH/%{name}" %{name}.go
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 %{name} %{buildroot}%{_bindir}/

%clean
# Fix permissions for files and directories in modules dir
find pkg -type d -exec chmod 0755 {} \;
find pkg -type f -exec chmod 0644 {} \;

rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md
%{_bindir}/%{name}

################################################################################

%changelog
* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.4-0
- attempt to fix goreleaser builds
- goreleaser: clean before build
- update travis config

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.3-0
- Accept /proc/diskstat metrics with extra fields.
- added help description about pg_stat_progress_create_index view
- added menu for switching between progress stats in top utility
- added pg_stat_progress_cluster stats to top/record/report utils
- added pg_stat_progress_create_index stats
- added stats context related to pg_stat_progress_cluster view
- added support for pg_stat_database.checksum_failures
- adjust header's styles of iostat/nicstat tabs in top utility
- another try of aligning refactoring - skip aligning if no rows in result
  set - don't truncate long values, such as names
- avoid rude disconnection from postgres at top-program exit
- describe "pgcenter config" doc more verbosely
- fix crashes when postgres is not running
- fix units
- implemented switching between two progress stats
- improve input args for progress stats in report utility
- inject version info at build time
- moved psql hotkey from 'p' to '~'
- readme/changelog changes
- report: print header at the beginning of the output
- rethinking pg_stat_progress_vacuum query: - wait events merged into single
  column - changed order of columns - move 'wait events' after 'state' - changed
  totals to percents for scanned and vacuumed numbers changed reports' buitin
  docs

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.2-0
- Cursor handling improvements
- Hide cursor when canceling operation
- Quitting from help and main screens with 'q' key
- fix code formatting, misspeling, etc.
- fixed acidentally used case-sensitive pattern matching when accounting number
  of user-started vacuums
- record/report: extend "--help" messages
- record/report: improve aligning and truncation of pg_stat_statements.query
- reworked pg_stat_statements queries
- rewrite PQconnectdb using connection setup in a loop
- top-like UI highlighting improvements
- top: do polling pg_stat_statements only if it's available (issue #59)
- top: fixed handling of libpq errors during connection establishment
- top: printLogtail() tiny refactoring, removed unnecessary retval
- top: read remote stats only if pgcenter schema exists
- top: removed notes about deprecated hotkeys; issue #57

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.1-0
- README: add badges
- top: fix wrong assembling of path to logfile

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.0-0
- Added dependencies downloading before building
- Changelog file is returned
- Merge pull request #46 from andyone/master
- added CGO_ENABLED=0
- added goreleaser support
- added wait events profiling
- cast all numeric to the same precision
- command management refactoring: config: moved parameters check from main
  program code to command management code config: emit error if neither '-i'
  nor '-u' specified profile: emit error if '-P' is not specified
- doc improvements and fixes
- fix division by zero in query to pg_stat_user_functions
- fix travis config
- fix travis config, try 2
- fixed GoReport recommendations top: fix wrong masks handling when
  cancel/terminate group of backends fixed cyclomatic complexity in
  functions added proper comments for variables and methods done code
  formatting
- lib/stat: fix wrong calculation of hits values
- lib/utils/postgres: remove explicit sslmode from connectin string
- output aligning rewritten: - fixed aligning for 'top' command - dynamic
  aligning for 'report' command - two new hotkeys in 'top', have been
  introduced which allow to change width of active columns
  (up/down arrows) - column width map moved from PGresult level to
  Context - aligning is performed once when first stats displayed - stat.Print()
  marked as deprecated - fixed couple IDE's warnings (unused variables)
- pg_stat_database query fixes: - strict cast of blk_read_time and
  blk_write_time to numeric helps to avoid some kind of errors in diff/sort
  operations - show blks_read in kilobytes - clarify builtin help add error
  check into PGresult.New()
- profile: added docs and examples
- release 0.6.0
- remove tabs from queries (looks ugly when log_destination=syslog)
- removed old commented and unused code
- report: extend built-in help
- report: show last processed stats file on error\ when something goes wrong
  and pgcenter is failed to read stats, it shows name of\ last processes stats
  file within tar file. It helps to debug what was happened.
- some refactoring in connection handling module: added error handling of pq
  (go driver) related errors added extra error handling in
  replaceEmptySettings() rewriten PGhost(), use advanced query for getting
  'host' value fixed error when attepmting to connect to non-SSL postgres:
  'pq: SSL is not enabled on the server'

* Wed Oct 03 2018 Anton Novojilov <andy@essentialkaos.com> - 0.5.0-0
- pgcenter rewritten on Go from scratch
- pgcenter functionality divided into sub-commands (git/perf-style)
- added new functionality: record/report statistics (worked as additional
  sub-commands)
- a lot of hotkeys are changed in 'top' sub-command (see builtin help)
- removed tabs support
- removed pgcenterrc support
- show activity statistics by default
- activity shows background processes
- hide/show idle activity (hidden by default)
- show recovery status in postgres summary
- tables and tables IO stats merged into one single view
- filtering supports regexps now

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
