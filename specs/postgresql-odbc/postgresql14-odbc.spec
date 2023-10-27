################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define short_name  psqlodbc
%define pg_ver      14

%define maj_ver     16
%define min_ver     00
%define patch       0000

%define pkg_ver     %{maj_ver}.%{min_ver}.%{patch}

%define pg_dir      %{_prefix}/pgsql-%{pg_ver}

################################################################################

Summary:        PostgreSQL %{pg_ver} ODBC driver
Name:           postgresql%{pg_ver}-odbc
Version:        %{pkg_ver}
Release:        0%{?dist}
License:        LGPLv2+
Group:          Applications/Databases
URL:            https://odbc.postgresql.org

Source0:        https://ftp.postgresql.org/pub/odbc/versions/src/%{short_name}-%{version}.tar.gz

# CAUTION: acinclude.m4 has to be kept in sync with package's aclocal.m4.
# This is a kluge that ought to go away, but upstream currently isn't
# shipping their custom macros anywhere except in aclocal.m4.  (The macros
# actually come from the Postgres source tree, but we haven't got that
# available while building this RPM.)  To generate: in psqlodbc source tree,
#   aclocal -I . -I $PGSRC/config
# then strip aclocal.m4 down to just the PGAC macros.
# BUT: as of 09.01.0200, configure.ac hasn't been updated to use latest
# PG macros, so keep using the previous version of acinclude.m4.
Source1:        acinclude.m4

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  postgresql%{pg_ver}-libs
BuildRequires:  postgresql%{pg_ver}-devel
BuildRequires:  gcc make unixODBC-devel libtool automake autoconf
BuildRequires:  openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:       postgresql%{pg_ver}-libs unixODBC

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

################################################################################

%prep
%{crc_check}

%setup -qn %{short_name}-%{version}

cp -p %{SOURCE1} .
rm -f libtool.m4 config/libtool.m4

libtoolize --force  --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build
export PG_CONFIG=%{pg_dir}/bin/pg_config

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
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbcw.so psqlodbcw  %{pg_dir}/lib/psqlodbcw.so %{pg_ver}0
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbca.so psqlodbca  %{pg_dir}/lib/psqlodbca.so %{pg_ver}0
%{_sbindir}/update-alternatives --install %{_libdir}/psqlodbc.so  psqlodbc   %{pg_dir}/lib/psqlodbc.so  %{pg_ver}0

%postun
if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
  %{_sbindir}/update-alternatives --remove psqlodbcw  %{pg_dir}/lib/psqlodbcw.so
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
* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 16.00.0000-0
- Use autoconf to check for stdbool.h
- Make it possible to use standard bool on Windows

* Thu Feb 23 2023 Anton Novojilov <andy@essentialkaos.com> - 13.02.0000-0
- Initial rebuild for kaos-repo
