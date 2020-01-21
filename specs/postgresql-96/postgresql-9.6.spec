################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}
%{!?kerbdir:%define kerbdir "/usr"}
%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}

%if 0%{?fedora} > 21
%{!?plpython3:%global plpython3 1}
%else
%{!?plpython3:%global plpython3 0}
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?sdt:%global sdt 0}
%{!?selinux:%global selinux 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%{!?sdt:%global sdt 1}
%{!?selinux:%global selinux 1}
%endif

%define majorver        9.6
%define minorver        16
%define rel             0
%define fullver         %{majorver}.%{minorver}
%define pkgver          96
%define realname        postgresql
%define shortname       pgsql
%define tinyname        pg
%define service_name    %{realname}-%{majorver}
%define install_dir     %{_usr}/%{shortname}-%{majorver}

%define prev_version    9.5

%define username        postgres
%define groupname       postgres
%define gid             26

%define __perl_requires %{SOURCE9}

################################################################################

Summary:           PostgreSQL %{majorver} client programs and libraries
Name:              %{realname}%{pkgver}
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
Source6:           %{realname}-%{majorver}-libs.conf
Source7:           https://www.postgresql.org/files/documentation/pdf/%{majorver}/%{realname}-%{majorver}-A4.pdf
Source8:           %{realname}.pam
Source9:           filter-requires-perl-Pg.sh
Source10:          %{realname}.sysconfig
Source11:          %{realname}.service

Source100:         checksum.sha512

Patch1:            rpm-%{shortname}.patch
Patch2:            %{realname}-logging.patch
Patch3:            %{realname}-perl-rpath.patch
Patch4:            %{realname}-var-run-socket.patch

%if 0%{?rhel} && 0%{?rhel} <= 5
Patch5:            %{realname}-prefer-ncurses.patch
%endif

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc perl glibc-devel bison flex
BuildRequires:     readline-devel zlib-devel >= 1.0.4

%if %plperl
BuildRequires:     perl-ExtUtils-Embed perl-ExtUtils-MakeMaker
%endif

%if %plpython
BuildRequires:     python-devel
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

Requires:          %{__ldconfig} initscripts
Requires:          %{name}-libs = %{version}

%if %{systemd_enabled}
Requires:          systemd
%endif

Requires(post):    %{__updalt}
Requires(postun):  %{__updalt}

Provides:          %{name} = %{version}-%{release}
Provides:          %{realname} = %{version}-%{release}

################################################################################

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
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
Summary:           The shared libraries required for any PostgreSQL clients
Group:             Applications/Databases

Provides:          %{realname}-libs = %{version}-%{release}

%description libs
The postgresql%{pkgver}-libs package provides the essential shared libraries for
any PostgreSQL client program or interface. You will need to install this
package to use any other PostgreSQL package or any clients that need to connect
to a PostgreSQL server.

################################################################################

%package server
Summary:           The programs needed to create and run a PostgreSQL server
Group:             Applications/Databases

Requires:          %{__useradd} %{__chkconfig}
Requires:          %{name} = %{version} %{name}-libs >= %{version}
Requires:          kaosv >= 2.13 numactl

Provides:          %{realname}-server = %{version}-%{release}

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
Summary:           Extra documentation for PostgreSQL
Group:             Applications/Databases

Provides:          %{realname}-docs = %{version}-%{release}

%description docs
The postgresql%{pkgver}-docs package includes the SGML source for the
documentation as well as the documentation in PDF format and some extra
documentation. Install this package if you want to help with the PostgreSQL
documentation project, or if you want to generate printed documentation. This
package also includes HTML version of the documentation.

################################################################################

%package contrib
Summary:           Contributed source and binaries distributed with PostgreSQL
Group:             Applications/Databases

Requires:          %{name} = %{version}
Provides:          %{realname}-contrib = %{version}-%{release}

%description contrib
The postgresql%{pkgver}-contrib package contains contributed packages that are
included in the PostgreSQL distribution.

################################################################################

%package devel
Summary:           PostgreSQL development header files and libraries
Group:             Development/Libraries

AutoReq:           no
Requires:          %{name} = %{version}
Provides:          %{realname}-devel = %{version}-%{release}

%description devel
The postgresql%{pkgver}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server.

################################################################################

%if %plperl
%package plperl
Summary:           The Perl procedural language for PostgreSQL
Group:             Applications/Databases

Requires:          %{name}-server = %{version}

%ifarch ppc ppc64
BuildRequires:     perl-devel
%endif

Obsoletes:         %{realname}-pl = %{version}
Provides:          %{realname}-plperl = %{version}-%{release}

%description plperl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-plperl package contains the PL/Perl language
for the backend.
%endif

################################################################################

%if %plpython
%package plpython
Summary:           The Python procedural language for PostgreSQL
Group:             Applications/Databases
Requires:          %{name} = %{version}
Requires:          %{name}-server = %{version}

Obsoletes:         %{realname}-pl = %{version}
Provides:          %{realname}-plpython = %{version}-%{release}

%description plpython
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-plpython package contains the PL/Python language
for the backend.
%endif

################################################################################

%if %pltcl
%package pltcl
Summary:           The Tcl procedural language for PostgreSQL
Group:             Applications/Databases

Requires:          %{name} = %{version}
Requires:          %{name}-server = %{version}

Obsoletes:         %{realname}-pl = %{version}
Provides:          %{realname}-pltcl = %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql%{pkgver}-pltcl package contains the PL/Tcl language
for the backend.
%endif

################################################################################

%if %test
%package test
Summary:           The test suite distributed with PostgreSQL
Group:             Applications/Databases

Requires:          %{name}-server = %{version}
Provides:          %{realname}-test = %{version}-%{release}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

%if 0%{?rhel} && 0%{?rhel} <= 5
%patch5 -p1
%endif

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

CFLAGS=`echo "$CFLAGS" | xargs -n 1 | grep -v ffast-math | xargs -n 100`

export LIBNAME=%{_lib}
%{_configure} --disable-rpath \
  --prefix=%{install_dir} \
  --includedir=%{install_dir}/include \
  --mandir=%{install_dir}/share/man \
  --datadir=%{install_dir}/share \
%if %beta
  --enable-debug \
  --enable-cassert \
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
  --with-system-tzdata=%{_datadir}/zoneinfo \
  --sysconfdir=%{_sysconfdir}/sysconfig/%{shortname} \
  --docdir=%{install_dir}/doc \
  --htmldir=%{install_dir}/doc/html

%{__make} %{?_smp_mflags} all
%{__make} %{?_smp_mflags} -C contrib all
%if %uuid
%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{install_dir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%{__make} %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
  pushd src/test/regress
    %{__make} %{?_smp_mflags} all
    cp ../../../contrib/spi/refint.so .
    cp ../../../contrib/spi/autoinc.so .
    %{__make} MAX_CONNECTIONS=5 check
    %{__make} clean
  popd
  pushd src/pl
    %{__make} MAX_CONNECTIONS=5 check
  popd
  pushd contrib
    %{__make} MAX_CONNECTIONS=5 check
  popd
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

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | s390 | s390x)
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
sed -i 's/{{PKG_VERSION}}/%{pkgver}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{PREV_VERSION}}/%{prev_version}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{USER_NAME}}/%{username}/g' %{buildroot}%{_initddir}/%{service_name}
sed -i 's/{{GROUP_NAME}}/%{groupname}/g' %{buildroot}%{_initddir}/%{service_name}

%if %{systemd_enabled}

# Installing and updating systemd config
install -d %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE11} %{buildroot}%{_unitdir}/postgresql-%{majorver}.service

sed -i 's/{{VERSION}}/%{version}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{MAJOR_VERSION}}/%{majorver}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{PKG_VERSION}}/%{pkgver}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{PREV_VERSION}}/%{prev_version}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{USER_NAME}}/%{username}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service
sed -i 's/{{GROUP_NAME}}/%{groupname}/g' %{buildroot}%{_unitdir}/postgresql-%{majorver}.service

%endif

ln -sf %{_initddir}/%{service_name} %{buildroot}%{_initddir}/%{tinyname}%{pkgver}

%if %pam
install -d %{buildroot}%{_sysconfdir}/pam.d
install -pm 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/%{realname}%{pkgver}
%endif

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
install -pm 700 %{SOURCE6} %{buildroot}%{install_dir}/share/

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
  %find_lang pg_basebackup-%{majorver}
  %find_lang pg_config-%{majorver}
  %find_lang pg_controldata-%{majorver}
  %find_lang pg_ctl-%{majorver}
  %find_lang pg_dump-%{majorver}
  %find_lang pg_resetxlog-%{majorver}
  %find_lang pg_rewind-%{majorver}
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

cat pg_config-%{majorver}.lang ecpg-%{majorver}.lang ecpglib6-%{majorver}.lang > pg_devel.lst

cat initdb-%{majorver}.lang pg_ctl-%{majorver}.lang psql-%{majorver}.lang \
         pg_dump-%{majorver}.lang pg_basebackup-%{majorver}.lang pg_rewind-%{majorver}.lang \
         pgscripts-%{majorver}.lang > pg_main.lst

cat postgres-%{majorver}.lang pg_resetxlog-%{majorver}.lang pg_controldata-%{majorver}.lang plpgsql-%{majorver}.lang > pg_server.lst

################################################################################

%pre server
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{groupname} >/dev/null || %{__groupadd} -g %{gid} -o -r %{groupname}
  %{__getent} passwd %{username} >/dev/null || \
              %{__useradd} -M -n -g %{username} -o -r -d %{_sharedstatedir}/%{shortname} -s /bin/bash -u %{gid} %{username}
fi

touch %{_logdir}/%{shortname}
chown %{username}:%{groupname} %{_logdir}/%{shortname}
chmod 0700 %{_logdir}/%{shortname}

%post server
if [[ $1 -eq 1 ]] ; then
%if %{systemd_enabled}
  %{__systemctl} daemon-reload %{service_name}.service &>/dev/null || :
  %{__systemctl} preset %{service_name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{service_name} &>/dev/null || :
%endif
  %{__ldconfig}
fi

# Migrate from official shitty packages
if [[ -f %{_rundir}/postmaster-%{majorver}.pid ]] ; then
  cat %{_rundir}/postmaster-%{majorver}.pid > %{_rundir}/%{name}.pid
  touch %{_lockdir}/%{name}
  rm -f %{_rundir}/postmaster-%{majorver}.pid
  rm -f %{_lockdir}/%{realname}-%{majorver}
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
# perfecto:absolve 3
echo "[[ -f /etc/profile ]] && source /etc/profile
PGDATA=/var/lib/pgsql/%{majorver}/data
export PGDATA" > %{_sharedstatedir}/%{shortname}/.bash_profile

chown %{username}: %{_sharedstatedir}/%{shortname}/.bash_profile

%preun server
if [[ $1 -eq 0 ]] ; then
%if %{systemd_enabled}
  %{__systemctl} --no-reload disable %{service_name}.service &>/dev/null || :
  %{__systemctl} stop %{service_name}.service &>/dev/null || :
%else
  %{__service} %{service_name} stop &>/dev/null || :
  %{__chkconfig} --del %{service_name} &>/dev/null || :
%endif
fi

%postun server
%{__ldconfig}
%if %{systemd_enabled}
%{__systemctl} daemon-reload &>/dev/null || :
%endif

%if %plperl
%post   plperl
%{__ldconfig}

%postun plperl
%{__ldconfig}
%endif

%if %plpython
%post   plpython
%{__ldconfig}

%postun plpython
%{__ldconfig}
%endif

%if %pltcl
%post   pltcl
%{__ldconfig}

%postun pltcl
%{__ldconfig}
%endif

%if %test
%post test
chown -R %{username}:%{groupname} %{_datarootdir}/%{shortname}/test &>/dev/null || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{__updalt} --install %{_bindir}/psql          %{shortname}-psql          %{install_dir}/bin/psql          %{pkgver}0
%{__updalt} --install %{_bindir}/clusterdb     %{shortname}-clusterdb     %{install_dir}/bin/clusterdb     %{pkgver}0
%{__updalt} --install %{_bindir}/createdb      %{shortname}-createdb      %{install_dir}/bin/createdb      %{pkgver}0
%{__updalt} --install %{_bindir}/createlang    %{shortname}-createlang    %{install_dir}/bin/createlang    %{pkgver}0
%{__updalt} --install %{_bindir}/createuser    %{shortname}-createuser    %{install_dir}/bin/createuser    %{pkgver}0
%{__updalt} --install %{_bindir}/dropdb        %{shortname}-dropdb        %{install_dir}/bin/dropdb        %{pkgver}0
%{__updalt} --install %{_bindir}/droplang      %{shortname}-droplang      %{install_dir}/bin/droplang      %{pkgver}0
%{__updalt} --install %{_bindir}/dropuser      %{shortname}-dropuser      %{install_dir}/bin/dropuser      %{pkgver}0
%{__updalt} --install %{_bindir}/pg_basebackup %{shortname}-pg_basebackup %{install_dir}/bin/pg_basebackup %{pkgver}0
%{__updalt} --install %{_bindir}/pg_config     %{shortname}-pg_config     %{install_dir}/bin/pg_config     %{pkgver}0
%{__updalt} --install %{_bindir}/pg_dump       %{shortname}-pg_dump       %{install_dir}/bin/pg_dump       %{pkgver}0
%{__updalt} --install %{_bindir}/pg_dumpall    %{shortname}-pg_dumpall    %{install_dir}/bin/pg_dumpall    %{pkgver}0
%{__updalt} --install %{_bindir}/pg_restore    %{shortname}-pg_restore    %{install_dir}/bin/pg_restore    %{pkgver}0
%{__updalt} --install %{_bindir}/reindexdb     %{shortname}-reindexdb     %{install_dir}/bin/reindexdb     %{pkgver}0
%{__updalt} --install %{_bindir}/vacuumdb      %{shortname}-vacuumdb      %{install_dir}/bin/vacuumdb      %{pkgver}0

%{__updalt} --install %{_mandir}/man1/clusterdb.1     %{shortname}-clusterdbman     %{install_dir}/share/man/man1/clusterdb.1     %{pkgver}0
%{__updalt} --install %{_mandir}/man1/createdb.1      %{shortname}-createdbman      %{install_dir}/share/man/man1/createdb.1      %{pkgver}0
%{__updalt} --install %{_mandir}/man1/createlang.1    %{shortname}-createlangman    %{install_dir}/share/man/man1/createlang.1    %{pkgver}0
%{__updalt} --install %{_mandir}/man1/createuser.1    %{shortname}-createuserman    %{install_dir}/share/man/man1/createuser.1    %{pkgver}0
%{__updalt} --install %{_mandir}/man1/dropdb.1        %{shortname}-dropdbman        %{install_dir}/share/man/man1/dropdb.1        %{pkgver}0
%{__updalt} --install %{_mandir}/man1/droplang.1      %{shortname}-droplangman      %{install_dir}/share/man/man1/droplang.1      %{pkgver}0
%{__updalt} --install %{_mandir}/man1/dropuser.1      %{shortname}-dropuserman      %{install_dir}/share/man/man1/dropuser.1      %{pkgver}0
%{__updalt} --install %{_mandir}/man1/pg_basebackup.1 %{shortname}-pg_basebackupman %{install_dir}/share/man/man1/pg_basebackup.1 %{pkgver}0
%{__updalt} --install %{_mandir}/man1/pg_dump.1       %{shortname}-pg_dumpman       %{install_dir}/share/man/man1/pg_dump.1       %{pkgver}0
%{__updalt} --install %{_mandir}/man1/pg_dumpall.1    %{shortname}-pg_dumpallman    %{install_dir}/share/man/man1/pg_dumpall.1    %{pkgver}0
%{__updalt} --install %{_mandir}/man1/pg_restore.1    %{shortname}-pg_restoreman    %{install_dir}/share/man/man1/pg_restore.1    %{pkgver}0
%{__updalt} --install %{_mandir}/man1/psql.1          %{shortname}-psqlman          %{install_dir}/share/man/man1/psql.1          %{pkgver}0
%{__updalt} --install %{_mandir}/man1/reindexdb.1     %{shortname}-reindexdbman     %{install_dir}/share/man/man1/reindexdb.1     %{pkgver}0
%{__updalt} --install %{_mandir}/man1/vacuumdb.1      %{shortname}-vacuumdbman      %{install_dir}/share/man/man1/vacuumdb.1      %{pkgver}0

%post libs
%{__updalt} --install %{_sysconfdir}/ld.so.conf.d/%{realname}-pgdg-libs.conf  %{shortname}-ld-conf  %{install_dir}/share/%{service_name}-libs.conf %{pkgver}0
%{__ldconfig}

# Drop alternatives entries for common binaries and man files
%postun
if [[ $1 -eq 0 ]] ; then
  # Only remove these links if the package is completely removed from the system (vs. just being upgraded)
  %{__updalt} --remove %{shortname}-psql          %{install_dir}/bin/psql
  %{__updalt} --remove %{shortname}-clusterdb     %{install_dir}/bin/clusterdb
  %{__updalt} --remove %{shortname}-createdb      %{install_dir}/bin/createdb
  %{__updalt} --remove %{shortname}-createlang    %{install_dir}/bin/createlang
  %{__updalt} --remove %{shortname}-createuser    %{install_dir}/bin/createuser
  %{__updalt} --remove %{shortname}-dropdb        %{install_dir}/bin/dropdb
  %{__updalt} --remove %{shortname}-droplang      %{install_dir}/bin/droplang
  %{__updalt} --remove %{shortname}-dropuser      %{install_dir}/bin/dropuser
  %{__updalt} --remove %{shortname}-pg_basebackup %{install_dir}/bin/pg_basebackup
  %{__updalt} --remove %{shortname}-pg_config     %{install_dir}/bin/pg_config
  %{__updalt} --remove %{shortname}-pg_dump       %{install_dir}/bin/pg_dump
  %{__updalt} --remove %{shortname}-pg_dumpall    %{install_dir}/bin/pg_dumpall
  %{__updalt} --remove %{shortname}-pg_restore    %{install_dir}/bin/pg_restore
  %{__updalt} --remove %{shortname}-reindexdb     %{install_dir}/bin/reindexdb
  %{__updalt} --remove %{shortname}-vacuumdb      %{install_dir}/bin/vacuumdb

  %{__updalt} --remove %{shortname}-clusterdbman     %{install_dir}/share/man/man1/clusterdb.1
  %{__updalt} --remove %{shortname}-createdbman      %{install_dir}/share/man/man1/createdb.1
  %{__updalt} --remove %{shortname}-createlangman    %{install_dir}/share/man/man1/createlang.1
  %{__updalt} --remove %{shortname}-createlangman    %{install_dir}/share/man/man1/createlang.1
  %{__updalt} --remove %{shortname}-createuserman    %{install_dir}/share/man/man1/createuser.1
  %{__updalt} --remove %{shortname}-dropdbman        %{install_dir}/share/man/man1/dropdb.1
  %{__updalt} --remove %{shortname}-droplangman      %{install_dir}/share/man/man1/droplang.1
  %{__updalt} --remove %{shortname}-dropuserman      %{install_dir}/share/man/man1/dropuser.1
  %{__updalt} --remove %{shortname}-pg_basebackupman %{install_dir}/share/man/man1/pg_basebackup.1
  %{__updalt} --remove %{shortname}-pg_dumpallman    %{install_dir}/share/man/man1/pg_dumpall.1
  %{__updalt} --remove %{shortname}-pg_dumpman       %{install_dir}/share/man/man1/pg_dump.1
  %{__updalt} --remove %{shortname}-pg_restoreman    %{install_dir}/share/man/man1/pg_restore.1
  %{__updalt} --remove %{shortname}-psqlman          %{install_dir}/share/man/man1/psql.1
  %{__updalt} --remove %{shortname}-reindexdbman     %{install_dir}/share/man/man1/reindexdb.1
  %{__updalt} --remove %{shortname}-vacuumdbman      %{install_dir}/share/man/man1/vacuumdb.1
fi

%postun libs
if [[ $1 -eq 0 ]] ; then
  %{__updalt} --remove %{shortname}-ld-conf %{install_dir}/share/%{service_name}-libs.conf
  %{__ldconfig}
fi

%clean
rm -rf %{buildroot}

################################################################################

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{install_dir}/bin/pgbench
%{install_dir}/bin/clusterdb
%{install_dir}/bin/createdb
%{install_dir}/bin/createlang
%{install_dir}/bin/createuser
%{install_dir}/bin/dropdb
%{install_dir}/bin/droplang
%{install_dir}/bin/dropuser
%{install_dir}/bin/pg_archivecleanup
%{install_dir}/bin/pg_basebackup
%{install_dir}/bin/pg_config
%{install_dir}/bin/pg_dump
%{install_dir}/bin/pg_dumpall
%{install_dir}/bin/pg_isready
%{install_dir}/bin/pg_restore
%{install_dir}/bin/pg_rewind
%{install_dir}/bin/pg_test_fsync
%{install_dir}/bin/pg_receivexlog
%{install_dir}/bin/pg_test_timing
%{install_dir}/bin/pg_upgrade
%{install_dir}/bin/pg_xlogdump
%{install_dir}/bin/psql
%{install_dir}/bin/reindexdb
%{install_dir}/bin/vacuumdb
%{install_dir}/share/man/man1/clusterdb.*
%{install_dir}/share/man/man1/createdb.*
%{install_dir}/share/man/man1/createlang.*
%{install_dir}/share/man/man1/createuser.*
%{install_dir}/share/man/man1/dropdb.*
%{install_dir}/share/man/man1/droplang.*
%{install_dir}/share/man/man1/dropuser.*
%{install_dir}/share/man/man1/pg_archivecleanup.1
%{install_dir}/share/man/man1/pg_basebackup.*
%{install_dir}/share/man/man1/pg_config.*
%{install_dir}/share/man/man1/pg_dump.*
%{install_dir}/share/man/man1/pg_dumpall.*
%{install_dir}/share/man/man1/pg_isready.*
%{install_dir}/share/man/man1/pg_receivexlog.*
%{install_dir}/share/man/man1/pg_restore.*
%{install_dir}/share/man/man1/pg_rewind.*
%{install_dir}/share/man/man1/pg_test_fsync.1
%{install_dir}/share/man/man1/pg_test_timing.1
%{install_dir}/share/man/man1/pg_upgrade.1
%{install_dir}/share/man/man1/pg_xlogdump.1
%{install_dir}/share/man/man1/pgbench.1
%{install_dir}/share/man/man1/psql.*
%{install_dir}/share/man/man1/reindexdb.*
%{install_dir}/share/man/man1/vacuumdb.*
%{install_dir}/share/man/man3/*
%{install_dir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%doc %{install_dir}/doc/extension/*.example
%{install_dir}/lib/_int.so
%{install_dir}/lib/adminpack.so
%{install_dir}/lib/auth_delay.so
%{install_dir}/lib/autoinc.so
%{install_dir}/lib/auto_explain.so
%{install_dir}/lib/bloom.so
%{install_dir}/lib/btree_gin.so
%{install_dir}/lib/btree_gist.so
%{install_dir}/lib/chkpass.so
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
%endif
%if %plpython
%{install_dir}/lib/hstore_plpython2.so
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
%{install_dir}/lib/ltree_plpython2.so
%endif
%{install_dir}/lib/moddatetime.so
%{install_dir}/lib/pageinspect.so
%{install_dir}/lib/pgcrypto.so
%{install_dir}/lib/pgstattuple.so
%{install_dir}/lib/pg_buffercache.so
%{install_dir}/lib/pg_prewarm.so
%{install_dir}/lib/pg_trgm.so
%{install_dir}/lib/pg_visibility.so
%{install_dir}/lib/refint.so
%{install_dir}/lib/seg.so
%{install_dir}/lib/tablefunc.so
%{install_dir}/lib/tcn.so
%{install_dir}/lib/test_decoding.so
%{install_dir}/lib/timetravel.so
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
%{install_dir}/share/extension/autoinc*
%{install_dir}/share/extension/bloom*
%{install_dir}/share/extension/btree_gin*
%{install_dir}/share/extension/btree_gist*
%{install_dir}/share/extension/chkpass*
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
%{install_dir}/share/extension/pageinspect*
%{install_dir}/share/extension/pg_buffercache*
%{install_dir}/share/extension/pg_freespacemap*
%{install_dir}/share/extension/pg_prewarm*
%{install_dir}/share/extension/pg_stat_statements*
%{install_dir}/share/extension/pg_trgm*
%{install_dir}/share/extension/pg_visibility*
%{install_dir}/share/extension/pgcrypto*
%{install_dir}/share/extension/pgrowlocks*
%{install_dir}/share/extension/pgstattuple*
%{install_dir}/share/extension/postgres_fdw*
%{install_dir}/share/extension/refint*
%{install_dir}/share/extension/seg*
%{install_dir}/share/extension/sslinfo*
%{install_dir}/share/extension/tablefunc*
%{install_dir}/share/extension/tcn*
%{install_dir}/share/extension/timetravel*
%{install_dir}/share/extension/tsearch2*
%{install_dir}/share/extension/tsm_system*
%{install_dir}/share/extension/unaccent*
%if %uuid
%{install_dir}/share/extension/uuid-ossp*
%endif
%{install_dir}/share/extension/xml2*
%{install_dir}/bin/oid2name
%{install_dir}/bin/vacuumlo
%{install_dir}/bin/pg_recvlogical
%{install_dir}/bin/pg_standby
%{install_dir}/share/man/man1/oid2name.1
%{install_dir}/share/man/man1/pg_recvlogical.1
%{install_dir}/share/man/man1/pg_standby.1
%{install_dir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{install_dir}/lib/libpq.so.*
%{install_dir}/lib/libecpg.so*
%{install_dir}/lib/libpgfeutils.a
%{install_dir}/lib/libpgtypes.so.*
%{install_dir}/lib/libecpg_compat.so.*
%{install_dir}/lib/libpqwalreceiver.so
%config(noreplace) %{install_dir}/share/%{service_name}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%config(noreplace) %{_initddir}/%{service_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%if %{systemd_enabled}
%config(noreplace) %{_unitdir}/postgresql-%{majorver}.service
%endif
%attr(755,%{username},%{groupname}) %dir %{_rundir}/%{realname}
%{_initddir}/%{tinyname}%{pkgver}
%if %pam
%config(noreplace) %{_sysconfdir}/pam.d/%{realname}%{pkgver}
%endif
%{install_dir}/bin/initdb
%{install_dir}/bin/pg_controldata
%{install_dir}/bin/pg_ctl
%{install_dir}/bin/pg_resetxlog
%{install_dir}/bin/postgres
%{install_dir}/bin/postmaster
%{install_dir}/share/man/man1/initdb.*
%{install_dir}/share/man/man1/pg_controldata.*
%{install_dir}/share/man/man1/pg_ctl.*
%{install_dir}/share/man/man1/pg_resetxlog.*
%{install_dir}/share/man/man1/postgres.*
%{install_dir}/share/man/man1/postmaster.*
%{install_dir}/share/postgres.bki
%{install_dir}/share/postgres.description
%{install_dir}/share/postgres.shdescription
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
%{install_dir}/lib/plpgsql.so
%dir %{install_dir}/share/extension
%{install_dir}/share/extension/plpgsql*
%{install_dir}/lib/tsearch2.so

%dir %{install_dir}/lib
%dir %{install_dir}/share
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}/data
%attr(700,%{username},%{groupname}) %dir %{_sharedstatedir}/%{shortname}/%{majorver}/backups
%{install_dir}/lib/*_and_*.so
%{install_dir}/share/conversion_create.sql
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

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{install_dir}/lib/plperl.so
%{install_dir}/lib/hstore_plperl.so
%{install_dir}/share/extension/plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{install_dir}/lib/pltcl.so
%{install_dir}/bin/pltcl_delmod
%{install_dir}/bin/pltcl_listmod
%{install_dir}/bin/pltcl_loadmod
%{install_dir}/share/unknown.pltcl
%{install_dir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{install_dir}/lib/plpython*.so
%{install_dir}/lib/hstore_plpython2.so
%{install_dir}/lib/ltree_plpython2.so
%{install_dir}/share/extension/plpython2u*
%{install_dir}/share/extension/plpythonu*
%endif

%if %plpython3
%files plpython3 -f pg_plpython3.lst
%defattr(-,%{username},%{groupname})
%{pgbaseinstdir}/share/extension/plpython3*
%{pgbaseinstdir}/lib/plpython3.so
%endif

%if %test
%files test
%defattr(-,%{username},%{groupname})
%attr(-,%{username},%{groupname}) %{install_dir}/lib/test/*
%attr(-,%{username},%{groupname}) %dir %{install_dir}/lib/test
%endif

################################################################################

%changelog
* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 9.6.16-0
- Updated to the latest stable release

* Sun Aug 18 2019 Anton Novojilov <andy@essentialkaos.com> - 9.6.15-0
- Updated to the latest stable release

* Sun Aug 18 2019 Anton Novojilov <andy@essentialkaos.com> - 9.6.14-0
- Updated to the latest stable release

* Tue May 14 2019 Anton Novojilov <andy@essentialkaos.com> - 9.6.13-0
- Updated to the latest stable release

* Tue Feb 26 2019 Anton Novojilov <andy@essentialkaos.com> - 9.6.12-0
- Updated to the latest stable release

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.11-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.10-0
- Updated to the latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.9-0
- Updated to the latest stable release

* Sat Mar 03 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.8-0
- Updated to the latest stable release

* Sat Mar 03 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.7-0
- Updated to the latest stable release

* Sat Jan 27 2018 Anton Novojilov <andy@essentialkaos.com> - 9.6.6-1
- Improved spec

* Sun Nov 12 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.6-0
- Updated to the latest stable release

* Tue Oct 10 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.5-1
- Improved init script

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.5-0
- Updated to the latest stable release

* Tue May 16 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.3-0
- Updated to the latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.2-0
- Updated to the latest stable release

* Wed Jan 18 2017 Anton Novojilov <andy@essentialkaos.com> - 9.6.1-1
- Improved init script

* Sun Nov 20 2016 Anton Novojilov <andy@essentialkaos.com> - 9.6.1-0
- Updated to the latest stable release
- Added systemd support

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 9.6.0-0
- Initial build
