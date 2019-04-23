################################################################################

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

################################################################################

%define short_name    psqlodbc

################################################################################

Summary:              PostgreSQL ODBC driver
Name:                 postgresql-odbc
Version:              10.03.0000
Release:              0%{?dist}
License:              LGPLv2+
Group:                Applications/Databases
URL:                  https://odbc.postgresql.org

Source0:              http://ftp.postgresql.org/pub/odbc/versions/src/%{short_name}-%{version}.tar.gz
# CAUTION: acinclude.m4 has to be kept in sync with package's aclocal.m4.
# This is a kluge that ought to go away, but upstream currently isn't
# shipping their custom macros anywhere except in aclocal.m4.  (The macros
# actually come from the Postgres source tree, but we haven't got that
# available while building this RPM.)  To generate: in psqlodbc source tree,
#   aclocal -I . -I $PGSRC/config
# then strip aclocal.m4 down to just the PGAC macros.
# BUT: as of 09.01.0200, configure.ac hasn't been updated to use latest
# PG macros, so keep using the previous version of acinclude.m4.
Source1:              acinclude.m4

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:             %{name} = %{version}-%{release}

BuildRequires:        gcc unixODBC-devel
BuildRequires:        libtool make automake autoconf postgresql10-devel
BuildRequires:        openssl-devel krb5-devel pam-devel zlib-devel readline-devel

################################################################################

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

################################################################################

%prep
%setup -qn %{short_name}-%{version}

cp -p %{SOURCE1} .
rm -f libtool.m4 config/libtool.m4

libtoolize --force  --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build
%configure --with-unixodbc \
           --disable-dependency-tracking \
           --disable-static

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p" DESTDIR=%{buildroot}

pushd %{buildroot}%{_libdir}
    ln -s psqlodbcw.so psqlodbc.so
    rm -f *.la
popd

%clean
rm -rf %{buildroot}

################################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc license.txt readme.txt docs/*
%attr(755,root,root) %{_libdir}/psqlodbcw.so
%attr(755,root,root) %{_libdir}/psqlodbca.so
%{_libdir}/psqlodbc.so

################################################################################

%changelog
* Tue Apr 23 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 10.03.0000-0
- Initial build

