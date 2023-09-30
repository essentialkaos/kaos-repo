################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define ver_major     3
%define ver_minor     41
%define ver_patch     2
%define release_year  2023
%define tarversion    %{ver_major}%{ver_minor}0%{ver_patch}00

################################################################################

Summary:        Embeddable SQL Database Engine (SQLite)
Name:           sqlite
Version:        %{ver_major}.%{ver_minor}.%{ver_patch}
Release:        0%{?dist}
License:        Public domain
Group:          Development/Tools
URL:            https://www.sqlite.org

Source0:        https://www.sqlite.org/%{release_year}/%{name}-autoconf-%{tarversion}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc glibc-devel readline-devel zlib-devel

Requires:       %{name}-libs = %{version}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.

################################################################################

%package libs
Group:    Development/Libraries
Summary:  Shared library for SQLite

%if 0%{?rhel} == 7
Requires:  %{name} = %{version}
%endif

%description libs
This package contains the shared library for SQLite.

################################################################################

%package devel
Group:     Development/Libraries
Summary:   Embeddable SQL Database Engine

Requires:  %{name}-libs = %{version}
Requires:  glibc-devel

%description devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server; SQLite is the server. The SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command-line tool or via any
application which supports the Qt database plug-ins.

################################################################################

%prep
%{crc_check}

%setup -qn sqlite-autoconf-%{tarversion}

%build
export CFLAGS="%{optflags} %{build_ldflags} \
               -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 \
               -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
               -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 \
               -DSQLITE_ENABLE_DBPAGE_VTAB \
               -Wall -fno-strict-aliasing"

%configure --enable-rtree \
           --enable-fts3 \
           --enable-fts4 \
           --enable-fts5 \
           --enable-threadsafe

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.txt
%{_bindir}/sqlite3
%{_libdir}/libsqlite*.so.*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libsqlite*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libsqlite*.so
%{_libdir}/pkgconfig/sqlite3.pc

################################################################################

%changelog
* Sat Sep 30 2023 Anton Novojilov <andy@essentialkaos.com> - 3.41.2-0
- https://www.sqlite.org/releaselog/3_41_2.html

* Sat Sep 30 2023 Anton Novojilov <andy@essentialkaos.com> - 3.40.1-0
- https://www.sqlite.org/releaselog/3_40_1.html

* Thu Dec 01 2022 Anton Novojilov <andy@essentialkaos.com> - 3.40.0-0
- https://www.sqlite.org/releaselog/3_40_0.html

* Mon Mar 15 2021 Anton Novojilov <andy@essentialkaos.com> - 3.35.0-0
- https://www.sqlite.org/releaselog/3_35_0.html

* Mon Mar 15 2021 Anton Novojilov <andy@essentialkaos.com> - 3.34.1-0
- https://www.sqlite.org/releaselog/3_34_1.html

* Mon Mar 15 2021 Anton Novojilov <andy@essentialkaos.com> - 3.34.0-0
- https://www.sqlite.org/releaselog/3_34_0.html

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.33.0-0
- https://www.sqlite.org/releaselog/3_33_0.html

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.3-0
- https://www.sqlite.org/releaselog/3_32_3.html

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.2-0
- https://www.sqlite.org/releaselog/3_32_2.html

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.1-0
- https://www.sqlite.org/releaselog/3_32_1.html

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.0-0
- https://www.sqlite.org/releaselog/3_32_0.html

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 3.31.1-0
- https://www.sqlite.org/releaselog/3_31_1.html

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.26.0-0
- https://www.sqlite.org/releaselog/3_26_0.html

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 3.24.0-0
- https://www.sqlite.org/releaselog/3_24_0.html

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.22.0-0
- https://www.sqlite.org/releaselog/3_22_0.html

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.20.1-0
- https://www.sqlite.org/releaselog/3_20_1.html

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.19.3-0
- https://www.sqlite.org/releaselog/3_19_3.html

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.18.0-0
- https://www.sqlite.org/releaselog/3_18_0.html

* Thu Mar 23 2017 Anton Novojilov <andy@essentialkaos.com> - 3.17.0-0
- Initial build for kaos repository
