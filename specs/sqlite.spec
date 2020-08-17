################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define tarversion  3330000

################################################################################

Summary:            Embeddable SQL Database Engine
Name:               sqlite
Version:            3.33.0
Release:            0%{?dist}
License:            Public domain
Group:              Development/Tools
URL:                https://www.sqlite.org

Source0:            https://www.sqlite.org/2020/%{name}-autoconf-%{tarversion}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc readline-devel tcl-devel

Provides:           %{name} = %{version}-%{release}

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

%package devel
Group:              Development/Libraries
Summary:            Embeddable SQL Database Engine

Requires:           %{name} = %{version}
Requires:           glibc-devel

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

%package tcl
Group:              Development/Libraries
Summary:            Tcl binding for SQLite

%description tcl
This package contains laguage bindings from the Tcl programming
language SQLite.

SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

################################################################################

%prep
%{crc_check}

%setup -qn sqlite-autoconf-%{tarversion}

%build
export CFLAGS="-DSQLITE_ENABLE_COLUMN_METADATA -DSQLITE_USE_URI"

%configure --disable-static

%{__make} %{?_smp_mflags}

pushd tea
  export CFLAGS=-I..
  export LDFLAGS=-L../.libs
  %configure --with-tcl=%{_libdir} --with-system-sqlite
popd

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la

pushd tea
  %{make_install} libdir=%{tcl_archdir}
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/sqlite3
%{_libdir}/libsqlite*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libsqlite*.so
%{_libdir}/pkgconfig/sqlite3.pc

%files tcl
%defattr(-,root,root,-)
%{_mandir}/mann/*

################################################################################

%changelog
* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.33.0-0
- Updated to the latest stable release

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.3-0
- Updated to the latest stable release

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.2-0
- Updated to the latest stable release

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.1-0
- Updated to the latest stable release

* Mon Aug 17 2020 Anton Novojilov <andy@essentialkaos.com> - 3.32.0-0
- Updated to the latest stable release

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 3.31.1-0
- Updated to the latest stable release

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.26.0-0
- Updated to the latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 3.24.0-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.22.0-0
- Updated to the latest stable release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.20.1-0
- Updated to the latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.19.3-0
- Updated to the latest stable release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.18.0-0
- Updated to the latest stable release

* Thu Mar 23 2017 Anton Novojilov <andy@essentialkaos.com> - 3.17.0-0
- Initial build for kaos repository
