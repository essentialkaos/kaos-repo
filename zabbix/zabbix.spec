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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __updalternatives %{_sbindir}/update-alternatives

################################################################################

%define debug_package     %{nil}

################################################################################

%define service_user      %{name}
%define service_group     %{name}
%define service_home      %{_libdir}/%{name}

################################################################################

Name:                 zabbix
Version:              3.2.3
Release:              1%{?dist}
Summary:              The Enterprise-class open source monitoring solution
Group:                Applications/Internet
License:              GPLv2+
URL:                  http://www.zabbix.com

Source0:              http://heanet.dl.sourceforge.net/project/%{name}/ZABBIX%20Latest%20Stable/%{version}/%{name}-%{version}.tar.gz
Source1:              %{name}-web22.conf
Source2:              %{name}-web24.conf
Source3:              %{name}-logrotate.in

Source10:             %{name}-agent.init
Source11:             %{name}-server.init
Source12:             %{name}-proxy.init

Source20:             %{name}-agent.service
Source21:             %{name}-server.service
Source22:             %{name}-proxy.service
Source23:             %{name}-tmpfiles.conf

Patch0:               config.patch
Patch1:               fonts-config.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc mysql-devel postgresql95-devel net-snmp-devel
BuildRequires:        openldap-devel gnutls-devel iksemel-devel unixODBC-devel
BuildRequires:        libxml2-devel curl-devel >= 7.13.1 sqlite-devel
BuildRequires:        OpenIPMI-devel >= 2 libssh2-devel >= 1.0.0

%if 0%{?rhel} >= 7
BuildRequires:        systemd
%endif

################################################################################

%description
Zabbix is the ultimate enterprise-level software designed for
real-time monitoring of millions of metrics collected from tens of
thousands of servers, virtual machines and network devices.

################################################################################

%package agent
Summary:              Zabbix Agent
Group:                Applications/Internet

Requires:             logrotate
Requires(pre):        /usr/sbin/useradd
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(preun):      systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

BuildRequires:        libxml2-devel

%description agent
Zabbix agent to be installed on monitored systems.

################################################################################

%package get
Summary:              Zabbix Get
Group:                Applications/Internet

%description get
Zabbix get command line utility

################################################################################

%package sender
Summary:              Zabbix Sender
Group:                Applications/Internet

%description sender
Zabbix sender command line utility

################################################################################

%package server-mysql
Summary:              Zabbix server for MySQL or MariaDB database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Conflicts:            zabbix-server-pgsql

%description server-mysql
Zabbix server with MySQL or MariaDB database support.

################################################################################

%package server-pgsql
Summary:              Zabbix server for PostgresSQL database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Conflicts:            zabbix-server-mysql

%description server-pgsql
Zabbix server with PostgresSQL database support.

################################################################################

%package proxy-mysql
Summary:              Zabbix proxy for MySQL or MariaDB database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Conflicts:            zabbix-proxy-pgsql
Conflicts:            zabbix-proxy-sqlite3

%description proxy-mysql
Zabbix proxy with MySQL or MariaDB database support.

################################################################################

%package proxy-pgsql
Summary:              Zabbix proxy for PostgreSQL database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Conflicts:            zabbix-proxy-mysql
Conflicts:            zabbix-proxy-sqlite3

%description proxy-pgsql
Zabbix proxy with PostgreSQL database support.

################################################################################

%package proxy-sqlite3
Summary:              Zabbix proxy for SQLite3 database
Group:                Applications/Internet

Requires:             fping
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%else
Requires(post):       %{__chkconfig}
Requires(preun):      %{__chkconfig}
Requires(preun):      %{__service}
Requires(postun):     %{__service}
%endif

Conflicts:            zabbix-proxy-pgsql
Conflicts:            zabbix-proxy-mysql

%description proxy-sqlite3
Zabbix proxy with SQLite3 database support.

################################################################################

%package web
Summary:              Zabbix web frontend common package
Group:                Applications/Internet

BuildArch:            noarch

Requires:             httpd
Requires:             php >= 5.4
Requires:             php-gd
Requires:             php-bcmath
Requires:             php-mbstring
Requires:             php-xml
Requires:             php-ldap
Requires:             dejavu-sans-fonts

Requires(post):       %{_sbindir}/update-alternatives
Requires(preun):      %{_sbindir}/update-alternatives

%description web
Zabbix web frontend common package

################################################################################

%package web-mysql
Summary:              Zabbix web frontend for MySQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-mysql
Requires:             zabbix-web = %{version}-%{release}

Conflicts:            zabbix-web-pgsql

%description web-mysql
Zabbix web frontend for MySQL

################################################################################

%package web-pgsql
Summary:              Zabbix web frontend for PostgreSQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-pgsql
Requires:             zabbix-web = %{version}-%{release}

Conflicts:            zabbix-web-mysql

%description web-pgsql
Zabbix web frontend for PostgreSQL

################################################################################

%prep
%setup -q -n zabbix-%{version}

%patch0 -p1
%patch1 -p1

# remove .htaccess files
rm -f frontends/php/app/.htaccess
rm -f frontends/php/conf/.htaccess
rm -f frontends/php/include/.htaccess
rm -f frontends/php/local/.htaccess

# remove translation source files and scripts
find frontends/php/locale -name '*.po' -delete
find frontends/php/locale -name '*.sh' -delete

# traceroute command path for global script
%{__sed} -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/mysql/data.sql
%{__sed} -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/postgresql/data.sql
%{__sed} -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/sqlite3/data.sql


%build

export PATH="/usr/pgsql-9.5/bin:$PATH"

build_flags="
        --enable-dependency-tracking
        --sysconfdir=%{_sysconfdir}/%{name}
        --libdir=%{_libdir}/%{name}
        --mandir=%{_mandir}
        --enable-agent
        --enable-server
        --enable-proxy
        --enable-ipv6
        --with-net-snmp
        --with-ldap
        --with-libcurl
        --with-openipmi
        --with-jabber
        --with-unixodbc
        --with-ssh2
        --with-libxml2
        --with-openssl
"

%configure $build_flags --with-mysql
make %{?_smp_mflags}

mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $build_flags --with-postgresql
make %{?_smp_mflags}

mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql

%configure $build_flags --with-sqlite3
make %{?_smp_mflags}

rm -f src/zabbix_server/zabbix_server
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

%install
rm -rf %{buildroot}

# install
%{make_install}

# clean unnecessary binaries
rm -f %{buildroot}%{_sbindir}/zabbix_server
rm -f %{buildroot}%{_sbindir}/zabbix_proxy

# install necessary directories
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sbindir}

install -dm 755 %{buildroot}%{_libdir}/zabbix
install -dm 755 %{buildroot}%{_libdir}/zabbix/modules

install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/web
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/alertscripts
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/externalscripts
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_server.d
install -dm 755 %{buildroot}%{_sysconfdir}/zabbix/zabbix_proxy.d

install -dm 755 %{buildroot}%{_localstatedir}/log/zabbix
install -dm 755 %{buildroot}%{_localstatedir}/run/zabbix

install -dm 755 %{buildroot}%{_docdir}/zabbix-agent-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-server-mysql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-server-pgsql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-proxy-mysql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-proxy-pgsql-%{version}
install -dm 755 %{buildroot}%{_docdir}/zabbix-proxy-sqlite3-%{version}

install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_mandir}/man8

install -dm 755 %{buildroot}%{_datadir}/zabbix

install -dm 755 %{buildroot}%{_sysconfdir}/httpd/conf.d

# install binaries
install -pm 755 src/zabbix_agent/zabbix_agentd %{buildroot}%{_sbindir}/
install -pm 755 src/zabbix_server/zabbix_server_* %{buildroot}%{_sbindir}/
install -pm 755 src/zabbix_proxy/zabbix_proxy_* %{buildroot}%{_sbindir}/
install -pm 755 src/zabbix_get/zabbix_get %{buildroot}%{_bindir}/
install -pm 755 src/zabbix_sender/zabbix_sender %{buildroot}%{_bindir}/

# install man
cp man/zabbix_get.man %{buildroot}%{_mandir}/man1/zabbix_get.1
cp man/zabbix_sender.man %{buildroot}%{_mandir}/man1/zabbix_sender.1
cp man/zabbix_agentd.man %{buildroot}%{_mandir}/man8/zabbix_agentd.8
cp man/zabbix_server.man %{buildroot}%{_mandir}/man8/zabbix_server.8
cp man/zabbix_proxy.man %{buildroot}%{_mandir}/man8/zabbix_proxy.8

# rename font for plots
mv frontends/php/fonts/DejaVuSans.ttf frontends/php/fonts/graphfont.ttf

# install frontend files
find frontends/php -name '*.orig' -delete
cp -a frontends/php/* %{buildroot}%{_datadir}/zabbix

# install frontend configuration files
touch %{buildroot}%{_sysconfdir}/zabbix/web/zabbix.conf.php
mv %{buildroot}%{_datadir}/zabbix/conf/maintenance.inc.php %{buildroot}%{_sysconfdir}/zabbix/web/

# drop config files in place
%if 0%{?rhel} >= 7
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/zabbix.conf
%else
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/zabbix.conf
%endif

# generate config files
cat conf/zabbix_agentd.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
        -e '/^# LogFileSize=.*/a \\nLogFileSize=0' \
        -e '/^# Include=$/a \\nInclude=%{_sysconfdir}/zabbix/zabbix_agentd.d/' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.conf

cat conf/zabbix_server.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_server.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# AlertScriptsPath=/a \\nAlertScriptsPath=%{_sysconfdir}/zabbix/alertscripts' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# DBSocket=/a \\nDBSocket=%{_localstatedir}/lib/mysql/mysql.sock' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptrap/snmptrap.log' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_server.conf

cat conf/zabbix_proxy.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_proxy.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_proxy.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# DBSocket=/a \\nDBSocket=%{_localstatedir}/lib/mysql/mysql.sock' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptrap/snmptrap.log' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_proxy.conf

# install logrotate configuration files
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|server|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-server
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|agentd|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-agent
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|proxy|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-proxy

# install startup scripts
%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE20} %{buildroot}%{_unitdir}/zabbix-agent.service
install -pDm 644 %{SOURCE21} %{buildroot}%{_unitdir}/zabbix-server.service
install -pDm 644 %{SOURCE22} %{buildroot}%{_unitdir}/zabbix-proxy.service
%else
install -pDm 755 %{SOURCE10} %{buildroot}%{_sysconfdir}/init.d/zabbix-agent
install -pDm 755 %{SOURCE11} %{buildroot}%{_sysconfdir}/init.d/zabbix-server
install -pDm 755 %{SOURCE12} %{buildroot}%{_sysconfdir}/init.d/zabbix-proxy
%endif

# install systemd-tmpfiles conf
%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-agent.conf
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-server.conf
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%endif

# copy sql files for servers
docdir=%{buildroot}%{_docdir}/zabbix-server-mysql-%{version}
cat database/mysql/schema.sql > $docdir/create.sql
cat database/mysql/images.sql >> $docdir/create.sql
cat database/mysql/data.sql >> $docdir/create.sql
%{__gzip} $docdir/create.sql

docdir=%{buildroot}%{_docdir}/zabbix-server-pgsql-%{version}
cat database/postgresql/schema.sql > $docdir/create.sql
cat database/postgresql/images.sql >> $docdir/create.sql
cat database/postgresql/data.sql >> $docdir/create.sql
%{__gzip} $docdir/create.sql

# copy sql files for proxies
docdir=%{buildroot}%{_docdir}/zabbix-proxy-mysql-%{version}
cp database/mysql/schema.sql $docdir/schema.sql
%{__gzip} $docdir/schema.sql

docdir=%{buildroot}%{_docdir}/zabbix-proxy-pgsql-%{version}
cp database/postgresql/schema.sql $docdir/schema.sql
%{__gzip} $docdir/schema.sql

docdir=%{buildroot}%{_docdir}/zabbix-proxy-sqlite3-%{version}
cp database/sqlite3/schema.sql $docdir/schema.sql
%{__gzip} $docdir/schema.sql


%clean
rm -rf %{buildroot}

################################################################################

%pre agent
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%post agent
%if 0%{?rhel} >= 7
%systemd_post zabbix-agent.service
%else
%{__chkconfig} --add zabbix-agent || exit 0
%endif


%pre server-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%pre server-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%pre proxy-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%pre proxy-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%pre proxy-sqlite3
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -r -g %{service_user} -s /sbin/nologin -d %{service_home} \
        -c "Zabbix Monitoring System" %{service_user}
exit 0


%post server-mysql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server || exit 0
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_server \
        zabbix-server %{_sbindir}/zabbix_server_mysql 10
exit 0


%post server-pgsql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server || exit 0
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_server \
        zabbix-server %{_sbindir}/zabbix_server_pgsql 10
exit 0


%post proxy-mysql
%if 0%{?rhel} >= 7
%systemd_post zabbix-proxy.service
%else
%{__chkconfig} --add zabbix-proxy
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_proxy \
        zabbix-proxy %{_sbindir}/zabbix_proxy_mysql 10
exit 0


%post proxy-pgsql
%if 0%{?rhel} >= 7
%systemd_post zabbix-proxy.service
%else
%{__chkconfig} --add zabbix-proxy
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_proxy \
        zabbix-proxy %{_sbindir}/zabbix_proxy_pgsql 10
exit 0


%post proxy-sqlite3
%if 0%{?rhel} >= 7
%systemd_post zabbix-proxy.service
%else
%{__chkconfig} --add zabbix-proxy
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_proxy \
        zabbix-proxy %{_sbindir}/zabbix_proxy_sqlite3 10
exit 0


%preun agent
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-agent.service
%else
%{__service} zabbix-agent stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-agent
%endif
fi
exit 0


%preun server-mysql
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-server.service
%else
%{__service} zabbix-server stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-server
%endif
%{__updalternatives} --remove zabbix-server \
        %{_sbindir}/zabbix_server_mysql
fi
exit 0


%preun server-pgsql
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-server.service
%else
%{__service} zabbix-server stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-server
%endif
%{__updalternatives} --remove zabbix-server \
        %{_sbindir}/zabbix_server_pgsql
fi
exit 0


%preun proxy-mysql
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-proxy.service
%else
%{__service} zabbix-proxy stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_mysql
fi
exit 0


%preun proxy-pgsql
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-proxy.service
%else
%{__service} zabbix-proxy stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_pgsql
fi
exit 0


%preun proxy-sqlite3
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-proxy.service
%else
%{__service} zabbix-proxy stop >/dev/null 2>&1
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_sqlite3
fi
exit 0


%postun agent
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-agent.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-agent try-restart >/dev/null 2>&1 || exit 0
fi
%endif


%postun server-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-server try-restart >/dev/null 2>&1 || exit 0
fi
%endif


%postun server-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-server try-restart >/dev/null 2>&1 || exit 0
fi
%endif


%postun proxy-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart >/dev/null 2>&1 || exit 0
fi
%endif


%postun proxy-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart >/dev/null 2>&1 || exit 0
fi
%endif


%postun proxy-sqlite3
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart >/dev/null 2>&1 || exit 0
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
# no files for you

%files agent
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-agent-%{version}/
%dir %{_sysconfdir}/zabbix/zabbix_agentd.d

%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix

%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-agent.service
%{_libdir}/tmpfiles.d/zabbix-agent.conf
%else
%{_sysconfdir}/init.d/zabbix-agent
%endif


%files get
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README

%{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get.1*


%files sender
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README

%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*


%files server-mysql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-server-mysql-%{version}/
%dir %{_sysconfdir}/zabbix/alertscripts
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf

%{_mandir}/man8/zabbix_server.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-server.service
%{_libdir}/tmpfiles.d/zabbix-server.conf
%else
%{_sysconfdir}/init.d/zabbix-server
%endif
%{_sbindir}/zabbix_server_mysql


%files server-pgsql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-server-pgsql-%{version}/
%dir %{_sysconfdir}/zabbix/alertscripts
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf

%{_mandir}/man8/zabbix_server.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-server.service
%{_libdir}/tmpfiles.d/zabbix-server.conf
%else
%{_sysconfdir}/init.d/zabbix-server
%endif
%{_sbindir}/zabbix_server_pgsql


%files proxy-mysql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-proxy-mysql-%{version}/
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf

%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_mysql


%files proxy-pgsql
%defattr(-,root,root,-)
%doc %{_docdir}/zabbix-proxy-pgsql-%{version}/
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf

%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_pgsql


%files proxy-sqlite3
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_sysconfdir}/zabbix/externalscripts

%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy

%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf

%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_sqlite3


%files web
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %attr(0750,apache,apache) %{_sysconfdir}/zabbix/web

%config(noreplace) %{_sysconfdir}/zabbix/web/maintenance.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf

%ghost %attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/zabbix/web/zabbix.conf.php

%{_datadir}/zabbix


%files web-mysql
%defattr(-,root,root,-)


%files web-pgsql
%defattr(-,root,root,-)

################################################################################

%changelog
* Tue Jan 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- updated Czech, English (United States), French, Italian, Japanese, Korean,
  Portuguese (Brazil), Russian, Ukrainian translations; thanks to Zabbix
  translators
- fixed "Response time" graph on "Details of web scenario" page
- fixed paging error in Configuration->Triggers and Monitoring->Web
- fixed crash in IPMI poller, added deleting of inactive IPMI hosts in
  'unreachable poller', improved code correctness and debug logging
- fixed applications and application prototypes being reset in templated
  item prototypes when modifying its parent
- added vm.vmemory.size to active item helper, updated descriptions and
  sorted; thanks richlv for patch
- fixed "system.stat" returning not supported after Zabbix agent restart on AIX
- fixed threaded metric to handle interruption by a signal
- fixed default operation step duration to be included in minimal step
  calculation instead of overriding
- fixed possible crash when polling vmware.hv.health.status
- fixed zabbix_get to match zabbix_server protocol
- changed vmware.vm.cpu.ready item units and description

* Tue Oct 04 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.2.1-0
- improved concurrent VMware item polling speed, reduced size of cached VMware data
- updated Chinese (China), French, Italian, Portuguese (Brazil) translations; 
  thanks to Zabbix translators
- increased width of input fields
- fixed link "Help" to a proper version of Zabbix manual
- fixed parameter parsing in calculated items when it contains double quote 
  escaping
- fixed trigger update after executing event correlation 'close new' operation
- fixed possible delay when proxy sends cached history to server
- fixed long SNMP OID not being accepted
- fixed error when upgrading graph_theme table in proxy database 
  from 1.8 to 2.0
- fixed forms behaviour when enter key is pressed
- fixed escaped double quote parsing in quoted parameters in array in item 
  key parameters
- fixed compilation failure for OpenBSD 5.8, 5.9, 6.0
- fixed validation of new host group when creating/updating template
- changed translation string "Acknowledges" => "Acknowledgements"
- implemented dynamic default sortorder for icon mappings, now default 
  sortorder increases by one with each entry of mapping
- fixed timeline in Problem view which shows "Yesterday" instead of "Today"
- fixed checkbox functionality and display of undefined indexes in trigger 
  expression and recovery expression constructor
- added converting of SNMP lld rules in XML import
- removed mistaken support of {ITEM.VALUE} and {ITEM.LASTVALUE} macros in 
  trigger URLs

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.4-0
- fixed SQL injection vulnerability in "Latest data" page; thanks to 1N3 at
  Early Warning Services, LLC
- updated Chinese (China), Czech, French, German, Italian, Japanese, Polish,
  Portuguese (Brazil), Russian, Slovak translations; thanks to Zabbix
  translators
- fixed remote command execution via SSH with no Zabbix agent interface
- added ability to monitor SNMP devices returning OIDs in decreasing or
  mixed order
- fixed severity filter in map.view action
- fixed selecting of group in popup page filter
- fixed web monitoring automatic refresh
- fixed overlapping of row and table borders
- fixed support of sending several Request object at the same time to JSON-RPC
- fixed option URL value in step of web scenario popup; thanks to Fernando
  Schmitt for patch
- fixed strings being untranslatable in Reports -> Triggers top 100
- fixed calendar time for cases when local time zone differs from servers
  time zone
- fixed starting value of time selector for events, graphs and screens
- fixed default values for "Show", "Area type" and "Automatic icon selection"
  options in Map element popup
- fixed handling of socket connection error messages on Windows; thanks to
  Yuri Volkov for patch
- fixed server/proxy crashes when performing Simple checks with invalid key
  parameters hidden in user macro
- fixed drawing graphs with items that have scheduling intervals
- fixed agent compilation on AIX 5.2, AIX 5.3
- fixed copying triggers to groups with multiple hosts or templates
- fixed selection of application in application popup
- fixed applications getting unlinked from undiscovered items
- fixed server/proxy compilation error on Solaris 10
- fixed length limit for host prototype name
- fixed whitespace between elements in host, host mass update, host prototype
  and proxy forms
- moved image type selection to top in administration->general->images
- added "No data found." message in administration->general->images
- fixed textarea visibility in monitoring->maps properties
- forced quoting of item key parameter if macro resolution resulted in unquoted
  parameter with leading spaces
- reverted table header capitalization. fixed calendar header
- allowed "noSuchName" to be returned for SNMPv2 and SNMPv3
- fixed saving of "Show text as HTML" checkbox in Monitoring->Screens
- decreased padding and margins in tables and across the whole UI
- added compression of generated CSS files to reduce size from 99K to around 56K
- fixed agent, get and sender being erroneously linked against UnixODBC
- removed disabled status for "Export to CSV" button
- fixed vertical scrollbar overlapping in messages
- fixed users online status in users.php users table
- fixed access_deny() message layout for not logged in page visitors
- fixed access to popup_media for Zabbix Admin user in profile->media
- fixed whitespace between elements in the IT services form

* Thu Aug 04 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-2
- Fixed dependency bug

* Thu Jun 23 2016 Gleb Goncharov <inbox@gongled.ru> - 3.0.3-1
- removed unnecessary patch for fping3 support
- improved spec

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- added script name and command into a script execution form
- enabled Chinese (China) translation to be displayed by default
- updated Chinese (China), English (United States), French, Italian, Japanese,
  Korean, Polish, Portuguese (Brazil), Russian, Slovak, Spanish, Ukrainian
  translations; thanks to Zabbix translators
- fixed Windows compilation error and time zone related issues
- fixed array formatting in exported JSON
- fixed deletion of the items which used in graph Y axis min/max parameters
- fixed possible buffer overruns in discovery macro substitution and other
  macro context issues
- fixed unexpected reset of group and host filter
- removed redundant closing PHP tags in configuration example file and when
  generating PHP files
- enforced bash usage in mysql.size user parameter configuration script to
  avoid issues with different default shells; thanks to Timo Lindfors
  for reporting it
- fixed color picker wrapping
- fixed crash when resolving {TRIGGER.NAME} of the trigger with expression
  containing unknown user macro
- fixed validation of JSON import source data in configuration.import method
- fixed timeout being too low when sending configuration data to active proxy
- fixed crash during configuration update when context is added to a macro
  without context
- fixed potential incorrect data from icmppingsec item with low latency hosts
- fixed proxy sorting in "Monitored by proxy" dropdown in host edit form
- fixed inventory mode not being inherited for host prototypes when linking
  template to a template/host
- fixed loss of trailing whitespace in unquoted function parameters when
  creating calculated items with low level discovery
- improved performance of alert.get method
- updated success and error messages for triggers, items and graphs
  'Copy' operations
- fixed API configuration.import method for importing template and/or host
  with trigger prototype dependency
- added finishing touches to encryption support
- fixed encoding reset when Zabbix process auto-reconnects MySQL database
- fixed disabling of script confirmation in Administration -> Script -> Edit
  form
- fixed display of form fields for different types of script in
  Administration -> Script -> Edit form
- fixed monitoring discovery and monitoring map data refresh
- fixed agent compilation on Solaris without zone support (e.g. Solaris 9),
  added awareness of running on a newer Solaris with zones
- changed incorrect labels in item filters and host filters
- added hint for action operation steps on how to proceed infinitely
- prohibited 'band' operator for counting float values
- fixed count() evaluation for numeric values with operator and empty pattern
- fixed possible crash when constants are extracted from invalid trigger
  expression containing '{' without matching '}'
- fixed adding trigger prototype dependencies when cloning a host or template
- fixed pagination throwing an error after performing enable or disable via
  link on an object
- changed sum(), str(), regexp(), iregexp() trigger functions to return 0 if
  there are no data in the requested range

* Fri Mar 18 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.1-1
- 'update-alternatives' for zabbix-proxy doesn't work properly. Fixed.
- added zabbix-proxy-sqlite3

* Thu Mar 17 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.1-0
- Updated to latest version

* Wed Feb 17 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.0-0
- Initial build

