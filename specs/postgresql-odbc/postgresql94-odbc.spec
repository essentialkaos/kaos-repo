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
%define pg_comb_ver   94
%define pg_ver        9.4

%define maj_ver       11
%define min_ver       01
%define patch         0000

%define pkg_ver       %{maj_ver}.%{min_ver}.%{patch}

%define pg_dir        %{_prefix}/pgsql-%{pg_ver}

################################################################################

Summary:              PostgreSQL %{pg_ver} ODBC driver
Name:                 postgresql%{pg_comb_ver}-odbc
Version:              %{pkg_ver}
Release:              0%{?dist}
License:              LGPLv2+
Group:                Applications/Databases
URL:                  https://odbc.postgresql.org

Source0:              https://ftp.postgresql.org/pub/odbc/versions/src/%{short_name}-%{version}.tar.gz

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

BuildRequires:        postgresql%{maj_ver}-libs
BuildRequires:        postgresql%{maj_ver}-devel
BuildRequires:        gcc make unixODBC-devel libtool automake autoconf
BuildRequires:        openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:             postgresql%{pg_comb_ver}-libs unixODBC

Provides:             %{name} = %{version}-%{release}

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
./configure --with-unixodbc \
            --disable-dependency-tracking \
            --disable-static \
            --libdir=%{_libdir}

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p" DESTDIR=%{buildroot}

install -dm 755 %{buildroot}%{pg_dir}/lib

mv %{buildroot}%{_libdir}/psqlodbc* %{buildroot}%{pg_dir}/lib/

pushd %{buildroot}%{pg_dir}/lib
  ln -s psqlodbcw.so psqlodbc.so
  rm -f *.la
popd

%clean
rm -rf %{buildroot}

################################################################################

%post
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbcw.so psqlodbcw  %{pg_dir}/lib/psqlodbcw.so %{pg_comb_ver}
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbca.so psqlodbca  %{pg_dir}/lib/psqlodbca.so %{pg_comb_ver}
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbc.so  psqlodbc   %{pg_dir}/lib/psqlodbc.so  %{pg_comb_ver}

%postun
if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
  %{_sbindir}/update-alternatives --remove psqlodbcw  %{pg_dir}/lib/psqlodbcw.s
  %{_sbindir}/update-alternatives --remove psqlodbca  %{pg_dir}/lib/psqlodbca.so
  %{_sbindir}/update-alternatives --remove psqlodbc   %{pg_dir}/lib/psqlodbc.so
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc license.txt readme.txt docs/*
%attr(755,root,root) %{pg_dir}/lib/psqlodbcw.so
%attr(755,root,root) %{pg_dir}/lib/psqlodbca.so
%{pg_dir}/lib/psqlodbc.so

################################################################################

%changelog
* Tue Jun 04 2019 Anton Novojilov <andy@essentialkaos.com> - 11.01.0000-0
- Initial build
