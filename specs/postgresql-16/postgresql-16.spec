################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?kerbdir:%define kerbdir "/usr"}
%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?icu:%define icu 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}
%{!?llvm:%global llvm 1}
%{!?zstd:%global zstd 1}

%define majorver      16
%define minorver      9
%define rel           0
%define fullver       %{majorver}.%{minorver}
%define pkgver        16
%define realname      postgresql
%define shortname     pgsql
%define tinyname      pg
%define service_name  %{realname}-%{majorver}
%define install_dir   %{_usr}/%{shortname}-%{majorver}

%define prev_version  15

%define username      postgres
%define groupname     postgres
%define gid           26

%define __perl_requires %{SOURCE9}

################################################################################

Summary:           PostgreSQL %{majorver} client programs and libraries
Name:              %{realname}%{majorver}
Version:           %{fullver}
Release:           %{rel}%{?dist}
License:           PostgreSQL
Group:             Applications/Databases
URL:               https://www.postgresql.org

Source0:           https://download.postgresql.org/pub/source/v%{version}/%{realname}-%{version}.tar.bz2
Source1:           %{realname}.init
Source2:           Makefile.regress
Source3:           pg_config.h
Source4:           README.rpm-dist
Source5:           ecpg_config.h
Source7:           https://www.postgresql.org/files/documentation/pdf/%{majorver}/%{realname}-%{majorver}-A4.pdf
Source8:           %{realname}.pam
Source9:           filter-requires-perl-Pg.sh
Source10:          %{realname}.sysconfig
Source11:          %{realname}.service
Source12:          bash_profile
Source13:          %{realname}-tmpfiles.d.conf

Source100:         checksum.sha512

Patch1:            rpm-%{shortname}.patch
Patch2:            %{realname}-logging.patch
Patch3:            %{realname}-perl-rpath.patch
Patch4:            %{realname}-var-run-socket.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc gcc-c++ perl glibc-devel bison flex
BuildRequires:     readline-devel zlib-devel perl-generators

%if %plperl
BuildRequires:     perl(ExtUtils::Embed) perl(ExtUtils::MakeMaker)
%endif

%if %plpython
BuildRequires:     python3-devel
%endif

%if %pltcl
BuildRequires:     tcl-devel
%endif

%if %ssl
BuildRequires:     openssl-devel
%endif

%if %kerberos
BuildRequires:     krb5-devel e2fsprogs-devel
%endif

%if %icu
BuildRequires:     libicu-devel
Requires:          libicu
%endif

%if %nls
BuildRequires:     gettext >= 0.10.35
%endif

%if %xml
BuildRequires:     libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:     pam-devel
%endif

%if %uuid
BuildRequires:     libuuid-devel
%endif

%if %ldap
BuildRequires:     openldap-devel
%endif

%if %llvm
BuildRequires:     llvm-devel >= 13.0 clang-devel >= 13.0
%endif

%if %zstd
BuildRequires:     libzstd-devel > 1.4.0
Requires:          libzstd > 1.4.0
%endif

BuildRequires:     systemd systemd-devel

Requires:          glibc initscripts
Requires:          %{name}-libs = %{version}

Requires(post):    systemd chkconfig
Requires(preun):   systemd
Requires(postun):  systemd chkconfig

Provides:          %{name} = %{version}-%{release}
Provides:          %{realname} = %{version}-%{release}

################################################################################

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server. These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the command-line
utilities for managing PostgreSQL databases on a PostgreSQL server.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql%{pkgver}-server package.

################################################################################

%package libs
Summary:   The shared libraries required for any PostgreSQL clients
Group:     Applications/Databases

Provides:  %{realname}-libs = %{version}-%{release}

%description libs
The postgresql%{pkgver}-libs package provides the essential shared libraries
for any PostgreSQL client program or interface. You will need to install this
package to use any other PostgreSQL package or any clients that need to connect
to a PostgreSQL server.

################################################################################

%package server
Summary:   The programs needed to create and run a PostgreSQL server
Group:     Applications/Databases

Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}
Requires:  glibc kaosv >= 2.16 numactl util-linux
Requires:  %{_sbindir}/useradd %{_sbindir}/chkconfig

Provides:  %{realname}-server = %{version}-%{release}

%description server
The postgresql%{pkgver}-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql%{pkgver}-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql package.

################################################################################

%package docs
Summary:   Extra documentation for PostgreSQL
Group:     Applications/Databases

Provides:  %{realname}-docs = %{version}-%{release}

%description docs
The postgresql%{pkgver}-docs package includes the SGML source for the
documentation as well as the documentation in PDF format and some extra
documentation. Install this package if you want to help with the PostgreSQL
documentation project, or if you want to generate printed documentation. This
package also includes HTML version of the documentation.

################################################################################

%package contrib
Summary:   Contributed source and binaries distributed with PostgreSQL
Group:     Applications/Databases

Requires:  %{name} = %{version}
Provides:  %{realname}-contrib = %{version}-%{release}

%description contrib
The postgresql%{pkgver}-contrib package contains contributed packages that are
included in the PostgreSQL distribution.

################################################################################

%package devel
Summary:   PostgreSQL development header files and libraries
Group:     Development/Libraries

%if %icu
Requires:  libicu-devel
%endif

%if %ssl
Requires:  openssl-devel
%endif

AutoReq:   no
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}
Provides:  %{realname}-devel = %{version}-%{release}

%description devel
The postgresql%{pkgver}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server.

################################################################################

%if %llvm
%package llvmjit
Summary:   Just-in-time compilation support for PostgreSQL
Group:     Applications/Databases

Requires:  %{name}-server%{?_isa} = %{version}-%{release}
Requires:  llvm >= 13.0

Provides:  %{realname}-llvmjit = %{version}

%description llvmjit
The postgresql%{pkgver}-llvmjit package contains support for
just-in-time compiling parts of PostgreSQL queries. Using LLVM it
compiles e.g. expressions and tuple deforming into native code, with the
goal of accelerating analytics queries.
%endif

################################################################################

%if %plperl
%package plperl
Summary:    The Perl procedural language for PostgreSQL
Group:      Applications/Databases

Requires:   %{name}-server = %{version}

Obsoletes:  %{realname}-pl = %{version}
Provides:   %{realname}-plperl = %{version}-%{release}

%description plperl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-plperl package contains the PL/Perl language
for the backend.
%endif

################################################################################

%if %plpython
%package plpython3
Summary:    The Python procedural language for PostgreSQL
Group:      Applications/Databases

Requires:   %{name} = %{version}
Requires:   %{name}-server = %{version}
Requires:   python3 python3-libs

Obsoletes:  %{realname}-pl = %{version}
Provides:   %{realname}-plpython = %{version}-%{release}

%description plpython3
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-plpython package contains the PL/Python language
for the backend.
%endif

################################################################################

%if %pltcl
%package pltcl
Summary:    The Tcl procedural language for PostgreSQL
Group:      Applications/Databases

Requires:   %{name} = %{version}
Requires:   %{name}-server = %{version}

Obsoletes:  %{realname}-pl = %{version}
Provides:   %{realname}-pltcl = %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-pltcl package contains the PL/Tcl language
for the backend.
%endif

################################################################################

%if %test
%package test
Summary:   The test suite distributed with PostgreSQL
Group:     Applications/Databases

Requires:  %{name}-server = %{version}
Provides:  %{realname}-test = %{version}-%{release}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

################################################################################

%prep
%crc_check
%autosetup -p0 -n %{realname}-%{version}

# Copy pdf with documentation to build directory
cp -p %{SOURCE7} .

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS

%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....
CFLAGS=$(echo "$CFLAGS" | xargs -n 1 | grep -v ffast-math | xargs -n 100)
CFLAGS="$CFLAGS -DLINUX_OOM_SCORE_ADJ=0"
LDFLAGS="-Wl,--as-needed" ; export LDFLAGS

export CFLAGS
export LIBNAME=%{_lib}
export PYTHON=/usr/bin/python3

%{_configure} --disable-rpath \
  --prefix=%{install_dir} \
  --includedir=%{install_dir}/include \
  --mandir=%{install_dir}/share/man \
  --datadir=%{install_dir}/share \
%if %icu
  --with-icu \
%endif
%if %llvm
  --with-llvm \
%endif
%if %plperl
  --with-perl \
%endif
%if %plpython
  --with-python \
%endif
%if %pltcl
  --with-tcl \
  --with-tclconfig=%{_libdir} \
%endif
%if %ssl
  --with-openssl \
%endif
%if %pam
  --with-pam \
%endif
%if %kerberos
  --with-gssapi \
  --with-includes=%{kerbdir}/include \
  --with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
  --enable-nls \
%endif
%if !%intdatetimes
  --disable-integer-datetimes \
%endif
%if %disablepgfts
  --disable-thread-safety \
%endif
%if %uuid
  --with-uuid=e2fs \
%endif
%if %xml
  --with-libxml \
  --with-libxslt \
%endif
%if %ldap
  --with-ldap \
%endif
%if %zstd
  --with-zstd \
%endif
  --with-system-tzdata=%{_datadir}/zoneinfo \
  --sysconfdir=%{_sysconfdir}/sysconfig/%{shortname} \
  --docdir=%{install_dir}/doc \
  --htmldir=%{install_dir}/doc/html

MAKELEVEL=0 %{__make} %{?_smp_mflags} all

%{__make} %{?_smp_mflags} -C contrib all

%if %uuid
%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{install_dir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%{__make} %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path.  When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.

run_testsuite()
{
  %{__make} -C "$1" MAX_CONNECTIONS=5 check && return 0

  test_failure=1

  (
    set +x
    echo "=== trying to find all regression.diffs files in build directory ==="
    find -name 'regression.diffs' | \
    while read line; do
      echo "=== make failure: $line ==="
      cat "$line"
    done
  )
}

%if %runselftest
  run_testsuite "src/test/regress"
  %{__make} %{?_smp_mflags} clean -C "src/test/regress"
  run_testsuite "src/pl"
  run_testsuite "contrib"
%endif

%if %test
  pushd src/test/regress
    %{__make} %{?_smp_mflags} all
  popd
%endif

%install
rm -rf %{buildroot}

%{make_install}
mkdir -p %{buildroot}%{install_dir}/share/extensions/
%{make_install} -C contrib

%if %uuid
%{make_install} -C contrib/uuid-ossp
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
  i386 | x86_64)
    mv %{buildroot}%{install_dir}/include/pg_config.h %{buildroot}%{install_dir}/include/pg_config_`uname -i`.h
    install -pm 644 %{SOURCE3} %{buildroot}%{install_dir}/include/
    mv %{buildroot}%{install_dir}/include/server/pg_config.h %{buildroot}%{install_dir}/include/server/pg_config_`uname -i`.h
    install -pm 644 %{SOURCE3} %{buildroot}%{install_dir}/include/server/
    mv %{buildroot}%{install_dir}/include/ecpg_config.h %{buildroot}%{install_dir}/include/ecpg_config_`uname -i`.h
    install -pm 644 %{SOURCE5} %{buildroot}%{install_dir}/include/
    ;;
  *)
  ;;
esac

# Installing and updating sysv init script
install -d %{buildroot}%{_initddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -pm 755 %{SOURCE1} %{buildroot}%{_initddir}/%{service_name}
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/%{service_name}

sed -i 's/{{VERSION}}/%{version}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{MAJOR_VERSION}}/%{majorver}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{PKG_VERSION}}/%{majorver}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{PREV_VERSION}}/%{prev_version}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{USER_NAME}}/%{username}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{GROUP_NAME}}/%{groupname}/g' %{buildroot}%{_initddir}/%{service_name}

# Installing and updating systemd config
install -d %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE11} %{buildroot}%{_unitdir}/postgresql-%{majorver}.service

sed -i 's/{{VERSION}}/%{version}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{MAJOR_VERSION}}/%{majorver}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{PKG_VERSION}}/%{majorver}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{PREV_VERSION}}/%{prev_version}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{USER_NAME}}/%{username}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{GROUP_NAME}}/%{groupname}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service

ln -sf %{service_name} %{buildroot}%{_initddir}/%{tinyname}%{majorver}

%if %pam
install -d %{buildroot}%{_sysconfdir}/pam.d
install -pm 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/%{realname}%{majorver}
%endif

install -dm 755 %{buildroot}%{_tmpfilesdir}
install -pm 644 %{SOURCE13} %{buildroot}%{_tmpfilesdir}/%{realname}-%{majorver}.conf

# Create the directory for sockets
install -dm 755 %{buildroot}%{_rundir}/%{realname}

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -dm 700 %{buildroot}%{_sharedstatedir}/%{shortname}/%{majorver}/data

# backups of data go here...
install -dm 700 %{buildroot}%{_sharedstatedir}/%{shortname}/%{majorver}/backups

# Create the multiple postmaster startup directory
install -dm 700 %{buildroot}%{_sysconfdir}/sysconfig/%{shortname}/%{majorver}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
install -dm 755 %{buildroot}%{install_dir}/share/
echo "%{install_dir}/lib" > %{buildroot}%{install_dir}/share/%{realname}-%{majorver}-libs.conf

%if %test
  # Tests. There are many files included here that are unnecessary,
  # but include them anyway for completeness.  We replace the original
  # Makefiles, however.
  mkdir -p %{buildroot}%{install_dir}/lib/test
  cp -a src/test/regress %{buildroot}%{install_dir}/lib/test
  install -pm 0755 contrib/spi/refint.so %{buildroot}%{install_dir}/lib/test/regress
  install -pm 0755 contrib/spi/autoinc.so %{buildroot}%{install_dir}/lib/test/regress
  pushd  %{buildroot}%{install_dir}/lib/test/regress
    strip *.so
    rm -f GNUmakefile Makefile *.o
    chmod 0755 pg_regress regress.so
  popd
  cp %{SOURCE2} %{buildroot}%{install_dir}/lib/test/regress/Makefile
  chmod 0644 %{buildroot}%{install_dir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE4} README.rpm-dist
mkdir -p %{buildroot}%{install_dir}/share/doc/html
mv doc/src/sgml/html doc
mkdir -p %{buildroot}%{install_dir}/share/man/
mv doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7 %{buildroot}%{install_dir}/share/man/
rm -rf %{buildroot}%{_docdir}/%{shortname}

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

%if %nls
  %find_lang ecpg-%{majorver}
  %find_lang ecpglib6-%{majorver}
  %find_lang initdb-%{majorver}
  %find_lang libpq5-%{majorver}
  %find_lang pg_amcheck-%{majorver}
  %find_lang pg_archivecleanup-%{majorver}
  %find_lang pg_basebackup-%{majorver}
  %find_lang pg_checksums-%{majorver}
  %find_lang pg_config-%{majorver}
  %find_lang pg_controldata-%{majorver}
  %find_lang pg_ctl-%{majorver}
  %find_lang pg_dump-%{majorver}
  %find_lang pg_resetwal-%{majorver}
  %find_lang pg_rewind-%{majorver}
  %find_lang pg_test_fsync-%{majorver}
  %find_lang pg_test_timing-%{majorver}
  %find_lang pg_upgrade-%{majorver}
  %find_lang pg_verifybackup-%{majorver}
  %find_lang pg_waldump-%{majorver}
  %find_lang pgscripts-%{majorver}

  %if %plperl
    %find_lang plperl-%{majorver}
    cat plperl-%{majorver}.lang > pg_plperl.lst
  %endif

  %find_lang plpgsql-%{majorver}

  %if %plpython
    %find_lang plpython-%{majorver}
    cat plpython-%{majorver}.lang > pg_plpython.lst
  %endif

  %if %pltcl
    %find_lang pltcl-%{majorver}
    cat pltcl-%{majorver}.lang > pg_pltcl.lst
  %endif

  %find_lang postgres-%{majorver}
  %find_lang psql-%{majorver}
%endif

cat libpq5-%{majorver}.lang > pg_libpq5.lst

cat pg_config-%{majorver}.lang \
    ecpg-%{majorver}.lang \
    ecpglib6-%{majorver}.lang > pg_devel.lst

cat initdb-%{majorver}.lang \
    pg_amcheck-%{majorver}.lang \
    pg_archivecleanup-%{majorver}.lang \
    pg_basebackup-%{majorver}.lang \
    pg_checksums-%{majorver}.lang \
    pg_ctl-%{majorver}.lang \
    pg_dump-%{majorver}.lang \
    pg_rewind-%{majorver}.lang \
    pg_test_fsync-%{majorver}.lang \
    pg_test_timing-%{majorver}.lang \
    pg_upgrade-%{majorver}.lang \
    pg_verifybackup-%{majorver}.lang \
    pg_waldump-%{majorver}.lang \
    psql-%{majorver}.lang \
    pgscripts-%{majorver}.lang > pg_main.lst

cat postgres-%{majorver}.lang \
    pg_resetwal-%{majorver}.lang \
    pg_controldata-%{majorver}.lang \
    plpgsql-%{majorver}.lang > pg_server.lst

# Install bash profile
install -pm 700 %{SOURCE12} %{buildroot}%{install_dir}/share/
sed -i "s#{{PGDATA}}#%{_sharedstatedir}/%{shortname}/%{majorver}/data/#" \
       %{buildroot}%{install_dir}/share/bash_profile

################################################################################

%pre server
if [[ $1 -eq 1 ]] ; then
  getent group %{groupname} >/dev/null || groupadd -g %{gid} -o -r %{groupname}
  getent passwd %{username} >/dev/null || \
              useradd -M -n -g %{username} -o -r -d %{_sharedstatedir}/%{shortname} -s /bin/bash -u %{gid} %{username}
fi

%post server
if [[ $1 -eq 1 ]] ; then
  systemctl daemon-reload %{service_name}.service &>/dev/null || :
  systemctl preset %{service_name}.service &>/dev/null || :
  systemd-tmpfiles --create &>/dev/null || :

  /sbin/ldconfig
fi

# Removing bash_profile generated by previous versions of packages
if [[ ! -L %{_sharedstatedir}/%{shortname}/.bash_profile ]] ; then
  rm -f %{_sharedstatedir}/%{shortname}/.bash_profile
fi

update-alternatives --install %{_sharedstatedir}/%{shortname}/.bash_profile %{shortname}-bash_profile %{install_dir}/share/bash_profile %{pkgver}00

%preun server
if [[ $1 -eq 0 ]] ; then
  update-alternatives --remove %{shortname}-bash_profile %{install_dir}/share/bash_profile
  systemctl --no-reload disable %{service_name}.service &>/dev/null || :
  systemctl stop %{service_name}.service &>/dev/null || :
fi

%postun server
systemctl daemon-reload &>/dev/null || :
/sbin/ldconfig

%if %plperl
%post plperl
/sbin/ldconfig

%postun plperl
/sbin/ldconfig
%endif

%if %plpython
%post plpython3
/sbin/ldconfig

%postun plpython3
/sbin/ldconfig
%endif

%if %pltcl
%post pltcl
/sbin/ldconfig

%postun pltcl
/sbin/ldconfig
%endif

%if %test
%post test
chown -R -h %{username}:%{groupname} %{_datarootdir}/%{shortname}/test &>/dev/null || :
%endif

# Create alternatives entries for common binaries and man files
%post
update-alternatives --install %{_bindir}/psql          %{shortname}-psql          %{install_dir}/bin/psql          %{pkgver}00
update-alternatives --install %{_bindir}/clusterdb     %{shortname}-clusterdb     %{install_dir}/bin/clusterdb     %{pkgver}00
update-alternatives --install %{_bindir}/createdb      %{shortname}-createdb      %{install_dir}/bin/createdb      %{pkgver}00
update-alternatives --install %{_bindir}/createuser    %{shortname}-createuser    %{install_dir}/bin/createuser    %{pkgver}00
update-alternatives --install %{_bindir}/dropdb        %{shortname}-dropdb        %{install_dir}/bin/dropdb        %{pkgver}00
update-alternatives --install %{_bindir}/dropuser      %{shortname}-dropuser      %{install_dir}/bin/dropuser      %{pkgver}00
update-alternatives --install %{_bindir}/pg_basebackup %{shortname}-pg_basebackup %{install_dir}/bin/pg_basebackup %{pkgver}00
update-alternatives --install %{_bindir}/pg_config     %{shortname}-pg_config     %{install_dir}/bin/pg_config     %{pkgver}00
update-alternatives --install %{_bindir}/pg_dump       %{shortname}-pg_dump       %{install_dir}/bin/pg_dump       %{pkgver}00
update-alternatives --install %{_bindir}/pg_dumpall    %{shortname}-pg_dumpall    %{install_dir}/bin/pg_dumpall    %{pkgver}00
update-alternatives --install %{_bindir}/pg_restore    %{shortname}-pg_restore    %{install_dir}/bin/pg_restore    %{pkgver}00
update-alternatives --install %{_bindir}/reindexdb     %{shortname}-reindexdb     %{install_dir}/bin/reindexdb     %{pkgver}00
update-alternatives --install %{_bindir}/vacuumdb      %{shortname}-vacuumdb      %{install_dir}/bin/vacuumdb      %{pkgver}00

update-alternatives --install %{_mandir}/man1/clusterdb.1     %{shortname}-clusterdbman     %{install_dir}/share/man/man1/clusterdb.1     %{pkgver}00
update-alternatives --install %{_mandir}/man1/createdb.1      %{shortname}-createdbman      %{install_dir}/share/man/man1/createdb.1      %{pkgver}00
update-alternatives --install %{_mandir}/man1/createuser.1    %{shortname}-createuserman    %{install_dir}/share/man/man1/createuser.1    %{pkgver}00
update-alternatives --install %{_mandir}/man1/dropdb.1        %{shortname}-dropdbman        %{install_dir}/share/man/man1/dropdb.1        %{pkgver}00
update-alternatives --install %{_mandir}/man1/dropuser.1      %{shortname}-dropuserman      %{install_dir}/share/man/man1/dropuser.1      %{pkgver}00
update-alternatives --install %{_mandir}/man1/pg_basebackup.1 %{shortname}-pg_basebackupman %{install_dir}/share/man/man1/pg_basebackup.1 %{pkgver}00
update-alternatives --install %{_mandir}/man1/pg_dump.1       %{shortname}-pg_dumpman       %{install_dir}/share/man/man1/pg_dump.1       %{pkgver}00
update-alternatives --install %{_mandir}/man1/pg_dumpall.1    %{shortname}-pg_dumpallman    %{install_dir}/share/man/man1/pg_dumpall.1    %{pkgver}00
update-alternatives --install %{_mandir}/man1/pg_restore.1    %{shortname}-pg_restoreman    %{install_dir}/share/man/man1/pg_restore.1    %{pkgver}00
update-alternatives --install %{_mandir}/man1/psql.1          %{shortname}-psqlman          %{install_dir}/share/man/man1/psql.1          %{pkgver}00
update-alternatives --install %{_mandir}/man1/reindexdb.1     %{shortname}-reindexdbman     %{install_dir}/share/man/man1/reindexdb.1     %{pkgver}00
update-alternatives --install %{_mandir}/man1/vacuumdb.1      %{shortname}-vacuumdbman      %{install_dir}/share/man/man1/vacuumdb.1      %{pkgver}00

%post libs
# Create link to linker configuration file
update-alternatives --install %{_sysconfdir}/ld.so.conf.d/%{realname}-pgdg-libs.conf  %{shortname}-ld-conf  %{install_dir}/share/%{service_name}-libs.conf %{pkgver}00
# Update shared libs cache
/sbin/ldconfig

%post devel
# Create links to pkgconfig configuration files
update-alternatives --install %{_libdir}/pkgconfig/libpq.pc           %{shortname}-pkgconfig-libpq           %{install_dir}/lib/pkgconfig/libpq.pc          %{pkgver}00
update-alternatives --install %{_libdir}/pkgconfig/libpgtypes.pc      %{shortname}-pkgconfig-libpgtypes      %{install_dir}/lib/pkgconfig/libpgtypes.pc     %{pkgver}00
update-alternatives --install %{_libdir}/pkgconfig/libecpg.pc         %{shortname}-pkgconfig-libecpg         %{install_dir}/lib/pkgconfig/libecpg.pc        %{pkgver}00
update-alternatives --install %{_libdir}/pkgconfig/libecpg_compat.pc  %{shortname}-pkgconfig-libecpg_compat  %{install_dir}/lib/pkgconfig/libecpg_compat.pc %{pkgver}00

# Drop alternatives entries for common binaries and man files
%postun
if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system (vs. just being upgraded)
  update-alternatives --remove %{shortname}-psql          %{install_dir}/bin/psql
  update-alternatives --remove %{shortname}-clusterdb     %{install_dir}/bin/clusterdb
  update-alternatives --remove %{shortname}-createdb      %{install_dir}/bin/createdb
  update-alternatives --remove %{shortname}-createuser    %{install_dir}/bin/createuser
  update-alternatives --remove %{shortname}-dropdb        %{install_dir}/bin/dropdb
  update-alternatives --remove %{shortname}-dropuser      %{install_dir}/bin/dropuser
  update-alternatives --remove %{shortname}-pg_basebackup %{install_dir}/bin/pg_basebackup
  update-alternatives --remove %{shortname}-pg_config     %{install_dir}/bin/pg_config
  update-alternatives --remove %{shortname}-pg_dump       %{install_dir}/bin/pg_dump
  update-alternatives --remove %{shortname}-pg_dumpall    %{install_dir}/bin/pg_dumpall
  update-alternatives --remove %{shortname}-pg_restore    %{install_dir}/bin/pg_restore
  update-alternatives --remove %{shortname}-reindexdb     %{install_dir}/bin/reindexdb
  update-alternatives --remove %{shortname}-vacuumdb      %{install_dir}/bin/vacuumdb

  update-alternatives --remove %{shortname}-clusterdbman     %{install_dir}/share/man/man1/clusterdb.1
  update-alternatives --remove %{shortname}-createdbman      %{install_dir}/share/man/man1/createdb.1
  update-alternatives --remove %{shortname}-createuserman    %{install_dir}/share/man/man1/createuser.1
  update-alternatives --remove %{shortname}-dropdbman        %{install_dir}/share/man/man1/dropdb.1
  update-alternatives --remove %{shortname}-dropuserman      %{install_dir}/share/man/man1/dropuser.1
  update-alternatives --remove %{shortname}-pg_basebackupman %{install_dir}/share/man/man1/pg_basebackup.1
  update-alternatives --remove %{shortname}-pg_dumpallman    %{install_dir}/share/man/man1/pg_dumpall.1
  update-alternatives --remove %{shortname}-pg_dumpman       %{install_dir}/share/man/man1/pg_dump.1
  update-alternatives --remove %{shortname}-pg_restoreman    %{install_dir}/share/man/man1/pg_restore.1
  update-alternatives --remove %{shortname}-psqlman          %{install_dir}/share/man/man1/psql.1
  update-alternatives --remove %{shortname}-reindexdbman     %{install_dir}/share/man/man1/reindexdb.1
  update-alternatives --remove %{shortname}-vacuumdbman      %{install_dir}/share/man/man1/vacuumdb.1
fi

%postun libs
if [[ $1 -eq 0 ]] ; then
  # Remove link to linker configuration file
  update-alternatives --remove %{shortname}-ld-conf %{install_dir}/share/%{service_name}-libs.conf
  # Update shared libs cache
  /sbin/ldconfig
fi

%postun devel
if [[ $1 -eq 0 ]] ; then
  # Remove links to pkgconfig configuration files
  update-alternatives --remove %{shortname}-pkgconfig-libpq           %{install_dir}/lib/pkgconfig/libpq.pc
  update-alternatives --remove %{shortname}-pkgconfig-libpgtypes      %{install_dir}/lib/pkgconfig/libpgtypes.pc
  update-alternatives --remove %{shortname}-pkgconfig-libecpg         %{install_dir}/lib/pkgconfig/libecpg.pc
  update-alternatives --remove %{shortname}-pkgconfig-libecpg_compat  %{install_dir}/lib/pkgconfig/libecpg_compat.pc
fi

################################################################################

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES COPYRIGHT README.rpm-dist
%dir %{install_dir}/lib/bitcode
%{install_dir}/bin/clusterdb
%{install_dir}/bin/createdb
%{install_dir}/bin/createuser
%{install_dir}/bin/dropdb
%{install_dir}/bin/dropuser
%{install_dir}/bin/pg_archivecleanup
%{install_dir}/bin/pg_basebackup
%{install_dir}/bin/pg_config
%{install_dir}/bin/pg_dump
%{install_dir}/bin/pg_dumpall
%{install_dir}/bin/pg_isready
%{install_dir}/bin/pg_receivewal
%{install_dir}/bin/pg_restore
%{install_dir}/bin/pg_rewind
%{install_dir}/bin/pg_test_fsync
%{install_dir}/bin/pg_test_timing
%{install_dir}/bin/pg_upgrade
%{install_dir}/bin/pg_verifybackup
%{install_dir}/bin/pg_waldump
%{install_dir}/bin/pgbench
%{install_dir}/bin/psql
%{install_dir}/bin/reindexdb
%{install_dir}/bin/vacuumdb
%{install_dir}/share/errcodes.txt
%{install_dir}/share/man/man1/clusterdb.*
%{install_dir}/share/man/man1/createdb.*
%{install_dir}/share/man/man1/createuser.*
%{install_dir}/share/man/man1/dropdb.*
%{install_dir}/share/man/man1/dropuser.*
%{install_dir}/share/man/man1/pg_archivecleanup.1
%{install_dir}/share/man/man1/pg_basebackup.*
%{install_dir}/share/man/man1/pg_config.*
%{install_dir}/share/man/man1/pg_dump.*
%{install_dir}/share/man/man1/pg_dumpall.*
%{install_dir}/share/man/man1/pg_isready.*
%{install_dir}/share/man/man1/pg_receivewal.*
%{install_dir}/share/man/man1/pg_restore.*
%{install_dir}/share/man/man1/pg_rewind.*
%{install_dir}/share/man/man1/pg_test_fsync.1
%{install_dir}/share/man/man1/pg_test_timing.1
%{install_dir}/share/man/man1/pg_upgrade.1
%{install_dir}/share/man/man1/pg_verifybackup.1
%{install_dir}/share/man/man1/pg_waldump.1
%{install_dir}/share/man/man1/pgbench.1
%{install_dir}/share/man/man1/psql.*
%{install_dir}/share/man/man1/reindexdb.*
%{install_dir}/share/man/man1/vacuumdb.*
%{install_dir}/share/man/man3/*
%{install_dir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/* *-A4.pdf src/tutorial doc/html

%files contrib
%defattr(-,root,root)
%doc %{install_dir}/doc/extension/*.example
%{install_dir}/lib/_int.so
%{install_dir}/lib/adminpack.so
%{install_dir}/lib/amcheck.so
%{install_dir}/lib/auth_delay.so
%{install_dir}/lib/autoinc.so
%{install_dir}/lib/auto_explain.so
%{install_dir}/lib/basebackup_to_shell.so
%{install_dir}/lib/basic_archive.so
%{install_dir}/lib/bloom.so
%{install_dir}/lib/btree_gin.so
%{install_dir}/lib/btree_gist.so
%{install_dir}/lib/citext.so
%{install_dir}/lib/cube.so
%{install_dir}/lib/dblink.so
%{install_dir}/lib/earthdistance.so
%{install_dir}/lib/file_fdw.so*
%{install_dir}/lib/fuzzystrmatch.so
%{install_dir}/lib/insert_username.so
%{install_dir}/lib/isn.so
%{install_dir}/lib/hstore.so
%if %plperl
%{install_dir}/lib/hstore_plperl.so
%{install_dir}/lib/jsonb_plperl.so
%{install_dir}/share/extension/jsonb_plperl*.sql
%{install_dir}/share/extension/jsonb_plperl*.control
%endif
%{install_dir}/lib/passwordcheck.so
%{install_dir}/lib/pg_freespacemap.so
%{install_dir}/lib/pg_stat_statements.so
%{install_dir}/lib/pgrowlocks.so
%{install_dir}/lib/postgres_fdw.so
%{install_dir}/lib/sslinfo.so
%{install_dir}/lib/lo.so
%{install_dir}/lib/ltree.so
%if %plpython
%{install_dir}/lib/ltree_plpython3.so
%endif
%{install_dir}/lib/moddatetime.so
%{install_dir}/lib/old_snapshot.so
%{install_dir}/lib/pageinspect.so
%{install_dir}/lib/pg_buffercache.so
%{install_dir}/lib/pg_prewarm.so
%{install_dir}/lib/pg_surgery.so
%{install_dir}/lib/pg_trgm.so
%{install_dir}/lib/pg_visibility.so
%{install_dir}/lib/pg_walinspect.so
%{install_dir}/lib/pgcrypto.so
%{install_dir}/lib/pgstattuple.so
%{install_dir}/lib/refint.so
%{install_dir}/lib/seg.so
%{install_dir}/lib/tablefunc.so
%{install_dir}/lib/tcn.so
%{install_dir}/lib/test_decoding.so
%{install_dir}/lib/tsm_system_rows.so
%{install_dir}/lib/tsm_system_time.so
%{install_dir}/lib/unaccent.so
%if %xml
%{install_dir}/lib/pgxml.so
%endif
%if %uuid
%{install_dir}/lib/uuid-ossp.so
%endif
%{install_dir}/share/extension/adminpack*
%{install_dir}/share/extension/amcheck*
%{install_dir}/share/extension/autoinc*
%{install_dir}/share/extension/bloom*
%{install_dir}/share/extension/btree_gin*
%{install_dir}/share/extension/btree_gist*
%{install_dir}/share/extension/citext*
%{install_dir}/share/extension/cube*
%{install_dir}/share/extension/dblink*
%{install_dir}/share/extension/dict_int*
%{install_dir}/share/extension/dict_xsyn*
%{install_dir}/share/extension/earthdistance*
%{install_dir}/share/extension/file_fdw*
%{install_dir}/share/extension/fuzzystrmatch*
%{install_dir}/share/extension/hstore*
%{install_dir}/share/extension/insert_username*
%{install_dir}/share/extension/intagg*
%{install_dir}/share/extension/intarray*
%{install_dir}/share/extension/isn*
%{install_dir}/share/extension/lo*
%{install_dir}/share/extension/ltree*
%{install_dir}/share/extension/moddatetime*
%{install_dir}/share/extension/old_snapshot*
%{install_dir}/share/extension/pageinspect*
%{install_dir}/share/extension/pg_buffercache*
%{install_dir}/share/extension/pg_freespacemap*
%{install_dir}/share/extension/pg_prewarm*
%{install_dir}/share/extension/pg_stat_statements*
%{install_dir}/share/extension/pg_surgery*
%{install_dir}/share/extension/pg_trgm*
%{install_dir}/share/extension/pg_visibility*
%{install_dir}/share/extension/pg_walinspect*
%{install_dir}/share/extension/pgcrypto*
%{install_dir}/share/extension/pgrowlocks*
%{install_dir}/share/extension/pgstattuple*
%{install_dir}/share/extension/postgres_fdw*
%{install_dir}/share/extension/refint*
%{install_dir}/share/extension/seg*
%{install_dir}/share/extension/sslinfo*
%{install_dir}/share/extension/tablefunc*
%{install_dir}/share/extension/tcn*
%{install_dir}/share/extension/tsm_system*
%{install_dir}/share/extension/unaccent*
%if %uuid
%{install_dir}/share/extension/uuid-ossp*
%endif
%{install_dir}/share/extension/xml2*
%{install_dir}/bin/oid2name
%{install_dir}/bin/pg_amcheck
%{install_dir}/bin/pg_recvlogical
%{install_dir}/bin/vacuumlo
%{install_dir}/share/man/man1/oid2name.1
%{install_dir}/share/man/man1/pg_amcheck.1
%{install_dir}/share/man/man1/pg_recvlogical.1
%{install_dir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%config(noreplace) %{install_dir}/share/%{service_name}-libs.conf
%{install_dir}/lib/libecpg.so*
%{install_dir}/lib/libecpg_compat.so.*
%{install_dir}/lib/libpgcommon_shlib.a
%{install_dir}/lib/libpgfeutils.a
%{install_dir}/lib/libpgport_shlib.a
%{install_dir}/lib/libpgtypes.so.*
%{install_dir}/lib/libpq.so.*
%{install_dir}/lib/libpqwalreceiver.so

%files server -f pg_server.lst
%defattr(-,root,root)
%config(noreplace) %{_initddir}/%{service_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%config(noreplace) %{_unitdir}/%{realname}-%{majorver}.service
%config(noreplace) %{_tmpfilesdir}/%{realname}-%{majorver}.conf
%attr(755,%{username},%{groupname}) %dir %{_rundir}/%{realname}
%{_initddir}/%{tinyname}%{majorver}
%if %pam
%config(noreplace) %{_sysconfdir}/pam.d/%{realname}%{majorver}
%endif
%dir %{install_dir}/share/extension
%{install_dir}/bin/initdb
%{install_dir}/bin/pg_checksums
%{install_dir}/bin/pg_controldata
%{install_dir}/bin/pg_ctl
%{install_dir}/bin/pg_resetwal
%{install_dir}/bin/postgres
%{install_dir}/share/man/man1/initdb.*
%{install_dir}/share/man/man1/pg_checksums.*
%{install_dir}/share/man/man1/pg_controldata.*
%{install_dir}/share/man/man1/pg_ctl.*
%{install_dir}/share/man/man1/pg_resetwal.*
%{install_dir}/share/man/man1/postgres.*
%{install_dir}/share/postgres.bki
%{install_dir}/share/system_constraints.sql
%{install_dir}/share/system_functions.sql
%{install_dir}/share/system_views.sql
%{install_dir}/share/*.sample
%{install_dir}/share/timezonesets/*
%{install_dir}/share/tsearch_data/*.affix
%{install_dir}/share/tsearch_data/*.dict
%{install_dir}/share/tsearch_data/*.ths
%{install_dir}/share/tsearch_data/*.rules
%{install_dir}/share/tsearch_data/*.stop
%{install_dir}/share/tsearch_data/*.syn
%{install_dir}/lib/dict_int.so
%{install_dir}/lib/dict_snowball.so
%{install_dir}/lib/dict_xsyn.so
%{install_dir}/lib/euc2004_sjis2004.so
%{install_dir}/lib/pgoutput.so
%{install_dir}/lib/plpgsql.so
%{install_dir}/share/extension/plpgsql*
%{install_dir}/share/fix-CVE-*.sql

%config(noreplace) %attr(700,%{username},%{groupname}) %{install_dir}/share/bash_profile

%dir %{install_dir}/lib
%dir %{install_dir}/share
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}/data
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}/backups
%{install_dir}/lib/*_and_*.so
%{install_dir}/share/information_schema.sql
%{install_dir}/share/snowball_create.sql
%{install_dir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{install_dir}/include/*
%{install_dir}/bin/ecpg
%{install_dir}/lib/libpq.so
%{install_dir}/lib/libecpg.so
%{install_dir}/lib/libpq.a
%{install_dir}/lib/libpgcommon.a
%{install_dir}/lib/libecpg.a
%{install_dir}/lib/libecpg_compat.so
%{install_dir}/lib/libecpg_compat.a
%{install_dir}/lib/libpgport.a
%{install_dir}/lib/libpgtypes.so
%{install_dir}/lib/libpgtypes.a
%{install_dir}/lib/pgxs/*
%{install_dir}/lib/pkgconfig/*
%{install_dir}/share/man/man1/ecpg.*

%if %llvm
%files llvmjit
%defattr(-,root,root)
%{install_dir}/lib/bitcode/*
%{install_dir}/lib/llvmjit.so
%{install_dir}/lib/llvmjit_types.bc
%endif

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{install_dir}/lib/bool_plperl.so
%{install_dir}/lib/plperl.so
%{install_dir}/lib/hstore_plperl.so
%{install_dir}/share/extension/plperl*
%{install_dir}/share/extension/bool_plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{install_dir}/lib/pltcl.so
%{install_dir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython3 -f pg_plpython.lst
%defattr(-,root,root)
%{install_dir}/lib/plpython*.so
%{install_dir}/lib/hstore_plpython3.so
%{install_dir}/lib/jsonb_plpython3.so
%{install_dir}/lib/ltree_plpython3.so
%{install_dir}/share/extension/jsonb_plpython*
%{install_dir}/share/extension/plpython3u*
%endif

%if %test
%files test
%defattr(-,%{username},%{groupname})
%attr(-,%{username},%{groupname}) %{install_dir}/lib/test/*
%attr(-,%{username},%{groupname}) %dir %{install_dir}/lib/test
%endif

################################################################################

%changelog
* Tue Jun 17 2025 Anton Novojilov <andy@essentialkaos.com> - 16.9-0
- https://www.postgresql.org/docs/16/release-16-9.html

* Tue Jun 17 2025 Anton Novojilov <andy@essentialkaos.com> - 16.8-0
- https://www.postgresql.org/docs/16/release-16-8.html

* Tue Jun 17 2025 Anton Novojilov <andy@essentialkaos.com> - 16.7-0
- https://www.postgresql.org/docs/16/release-16-7.html

* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 16.6-0
- https://www.postgresql.org/docs/16/release-16-6.html

* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 16.5-0
- https://www.postgresql.org/docs/16/release-16-5.html

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 16.4-0
- https://www.postgresql.org/docs/16/release-16-4.html

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 16.3-0
- https://www.postgresql.org/docs/16/release-16-3.html

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 16.2-0
- https://www.postgresql.org/docs/16/release-16-2.html

* Sat Dec 09 2023 Anton Novojilov <andy@essentialkaos.com> - 16.1-0
- https://www.postgresql.org/docs/16/release-16-1.html

* Sun Oct 29 2023 Anton Novojilov <andy@essentialkaos.com> - 16.0-1
- Improved init script compatibility with systemd

* Fri Sep 22 2023 Anton Novojilov <andy@essentialkaos.com> - 16.0-0
- Initial build for kaos-repo
