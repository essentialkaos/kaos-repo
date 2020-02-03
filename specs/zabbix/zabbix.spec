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
%define service_home      %{_sharedstatedir}/%{name}

################################################################################

Name:                 zabbix
Version:              4.4.5
Release:              0%{?dist}
Summary:              The Enterprise-class open source monitoring solution
Group:                Applications/Internet
License:              GPLv2+
URL:                  https://www.zabbix.com

Source0:              https://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/%{version}/%{name}-%{version}.tar.gz
Source1:              %{name}-web22.conf
Source2:              %{name}-web24.conf
Source3:              %{name}-logrotate.in
Source4:              %{name}-java-gateway.init

Source10:             %{name}-agent.init
Source11:             %{name}-server.init
Source12:             %{name}-proxy.init
Source13:             %{name}-java-gateway.service
Source14:             %{name}_java_gateway

Source20:             %{name}-agent.service
Source21:             %{name}-server.service
Source22:             %{name}-proxy.service
Source23:             %{name}-tmpfiles.conf

Source100:            checksum.sha512

Patch0:               config.patch
Patch1:               fonts-config.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc mysql-devel postgresql96-devel net-snmp-devel
BuildRequires:        openldap-devel openssl-devel iksemel-devel unixODBC-devel
BuildRequires:        libxml2-devel curl-devel >= 7.13.1 sqlite-devel
BuildRequires:        OpenIPMI-devel >= 2 libssh2-devel >= 1.0.0
BuildRequires:        pcre-devel zlib-devel

%if 0%{?rhel} >= 7
Requires:             libevent
BuildRequires:        systemd libevent-devel
%else
Requires:             libevent2
BuildRequires:        libevent2-devel
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
Requires(pre):        %{_sbindir}/useradd
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
Zabbix get command line utility.

################################################################################

%package sender
Summary:              Zabbix Sender
Group:                Applications/Internet

%description sender
Zabbix sender command line utility.

################################################################################

%package js
Summary:              Zabbix JS
Group:                Applications/Internet

%description js
Command line utility that can be used for embedded script testing.

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

%package java-gateway
Summary:              Zabbix java gateway
Group:                Applications/Internet

Requires:             java >= 1.8.0
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

BuildRequires:        java-devel >= 1.8.0 pcre-devel zlib-devel

%description java-gateway
Zabbix java gateway.

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
Zabbix web frontend common package.

################################################################################

%package web-mysql
Summary:              Zabbix web frontend for MySQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-mysql
Requires:             zabbix-web = %{version}-%{release}

Conflicts:            zabbix-web-pgsql

%description web-mysql
Zabbix web frontend for MySQL.

################################################################################

%package web-pgsql
Summary:              Zabbix web frontend for PostgreSQL
Group:                Applications/Internet

BuildArch:            noarch

Requires:             php-pgsql
Requires:             zabbix-web = %{version}-%{release}

Conflicts:            zabbix-web-mysql

%description web-pgsql
Zabbix web frontend for PostgreSQL.

################################################################################

%prep
%{crc_check}

%setup -qn zabbix-%{version}

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
sed -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/mysql/data.sql
sed -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/postgresql/data.sql
sed -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/sqlite3/data.sql

# change log directory for Java Gateway
sed -i -e 's|/tmp/zabbix_java.log|%{_localstatedir}/log/zabbix/zabbix_java_gateway.log|g' src/zabbix_java/lib/logback.xml

%build

export PATH="/usr/pgsql-9.6/bin:$PATH"

build_flags="
        --enable-dependency-tracking
        --sysconfdir=%{_sysconfdir}/%{name}
        --libdir=%{_libdir}/%{name}
        --mandir=%{_mandir}
        --enable-agent
        --enable-proxy
        --enable-ipv6
        --enable-java
        --with-net-snmp
        --with-ldap
        --with-libcurl
        --with-openipmi
        --with-unixodbc
        --with-ssh2
        --with-libxml2
        --with-openssl
        --with-libevent
        --with-libpcre
"

%configure $build_flags --with-mysql --enable-server
%{__make} %{?_smp_mflags}

mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $build_flags --with-postgresql --enable-server
%{__make} %{?_smp_mflags}

mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql

%configure $build_flags --with-sqlite3
%{__make} %{?_smp_mflags}

rm -f src/zabbix_server/zabbix_server
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

%install
rm -rf %{buildroot}

# install
%{make_install}

# clean unnecessary binaries
rm -f %{buildroot}%{_sbindir}/zabbix_server
rm -f %{buildroot}%{_sbindir}/zabbix_proxy
# delete unnecessary files from java gateway
rm -f %{buildroot}%{_sbindir}/zabbix_java/settings.sh
rm -f %{buildroot}%{_sbindir}/zabbix_java/startup.sh
rm -f %{buildroot}%{_sbindir}/zabbix_java/shutdown.sh

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

install -dm 755 %{buildroot}%{service_home}

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

mv %{buildroot}%{_sbindir}/zabbix_java/lib/logback.xml %{buildroot}%{_sysconfdir}/zabbix/zabbix_java_gateway_logback.xml
rm -f %{buildroot}%{_sbindir}/zabbix_java/lib/logback-console.xml
mv %{buildroot}%{_sbindir}/zabbix_java %{buildroot}%{_datadir}/zabbix-java-gateway

%if 0%{?rhel} >= 7
install -pm 755 -p %{SOURCE14} %{buildroot}%{_sbindir}/zabbix_java_gateway
%endif

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
mv frontends/php/assets/fonts/DejaVuSans.ttf frontends/php/assets/fonts/graphfont.ttf

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
# perfecto:absolve 6
cat conf/zabbix_agentd.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
        -e '/^# LogFileSize=.*/a \\nLogFileSize=0' \
        -e '/^# Include=$/a \\nInclude=%{_sysconfdir}/zabbix/zabbix_agentd.d/' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_agentd.conf

# perfecto:absolve 12
cat conf/zabbix_server.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_server.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# AlertScriptsPath=/a \\nAlertScriptsPath=%{_sysconfdir}/zabbix/alertscripts' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=%{_localstatedir}/log/snmptrap/snmptrap.log' \
        -e '/^# SocketDir=.*/a \\nSocketDir=%{_localstatedir}/run/zabbix' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_server.conf

# perfecto:absolve 10
cat conf/zabbix_proxy.conf | sed \
        -e '/^# PidFile=/a \\nPidFile=%{_localstatedir}/run/zabbix/zabbix_proxy.pid' \
        -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_proxy.log|g' \
        -e '/^# LogFileSize=/a \\nLogFileSize=0' \
        -e '/^# ExternalScripts=/a \\nExternalScripts=%{_sysconfdir}/zabbix/externalscripts' \
        -e 's|^DBUser=root|DBUser=zabbix|g' \
        -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=%{_localstatedir}/log/snmptrap/snmptrap.log' \
        -e '/^# SocketDir=.*/a \\nSocketDir=%{_localstatedir}/run/zabbix' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_proxy.conf

# perfecto:absolve 3
cat src/zabbix_java/settings.sh | sed \
        -e 's|^PID_FILE=.*|PID_FILE="%{_localstatedir}/run/zabbix/zabbix_java.pid"|g' \
        > %{buildroot}%{_sysconfdir}/zabbix/zabbix_java_gateway.conf

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
cat %{SOURCE3} | sed \
        -e 's|COMPONENT|java_gateway|g' \
        > %{buildroot}%{_sysconfdir}/logrotate.d/zabbix-java-gateway

# install startup scripts
%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE20} %{buildroot}%{_unitdir}/zabbix-agent.service
install -pDm 644 %{SOURCE21} %{buildroot}%{_unitdir}/zabbix-server.service
install -pDm 644 %{SOURCE22} %{buildroot}%{_unitdir}/zabbix-proxy.service
install -pDm 644 %{SOURCE13} %{buildroot}%{_unitdir}/zabbix-java-gateway.service
%else
install -pDm 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/init.d/zabbix-java-gateway
install -pDm 755 %{SOURCE10} %{buildroot}%{_sysconfdir}/init.d/zabbix-agent
install -pDm 755 %{SOURCE11} %{buildroot}%{_sysconfdir}/init.d/zabbix-server
install -pDm 755 %{SOURCE12} %{buildroot}%{_sysconfdir}/init.d/zabbix-proxy
%endif

# install systemd-tmpfiles conf
%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir32}/tmpfiles.d/zabbix-agent.conf
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir32}/tmpfiles.d/zabbix-server.conf
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir32}/tmpfiles.d/zabbix-proxy.conf
install -pDm 644 %{SOURCE23} %{buildroot}%{_libdir32}/tmpfiles.d/zabbix-java-gateway.conf
%endif

# copy sql files for servers
docdir=%{buildroot}%{_docdir}/zabbix-server-mysql-%{version}
cat database/mysql/schema.sql > $docdir/create.sql
cat database/mysql/images.sql >> $docdir/create.sql
cat database/mysql/data.sql >> $docdir/create.sql
gzip $docdir/create.sql

docdir=%{buildroot}%{_docdir}/zabbix-server-pgsql-%{version}
cat database/postgresql/schema.sql > $docdir/create.sql
cat database/postgresql/images.sql >> $docdir/create.sql
cat database/postgresql/data.sql >> $docdir/create.sql
gzip $docdir/create.sql

# copy sql files for proxies
docdir=%{buildroot}%{_docdir}/zabbix-proxy-mysql-%{version}
cp database/mysql/schema.sql $docdir/schema.sql
gzip $docdir/schema.sql

docdir=%{buildroot}%{_docdir}/zabbix-proxy-pgsql-%{version}
cp database/postgresql/schema.sql $docdir/schema.sql
gzip $docdir/schema.sql

docdir=%{buildroot}%{_docdir}/zabbix-proxy-sqlite3-%{version}
cp database/sqlite3/schema.sql $docdir/schema.sql
gzip $docdir/schema.sql


%clean
rm -rf %{buildroot}

################################################################################

%pre agent
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre server-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre server-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre proxy-mysql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre proxy-pgsql
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre proxy-sqlite3
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0


%pre java-gateway
%{__getent} group %{service_group} >/dev/null || %{__groupadd} -r %{service_group}
%{__getent} passwd %{service_user} >/dev/null || \
        %{__useradd} -s /sbin/nologin -M -r -c "Zabbix Monitoring System" \
        -g %{service_group} -d %{service_home} %{service_user}
exit 0

%post agent
%if 0%{?rhel} >= 7
%systemd_post zabbix-agent.service
%else
%{__chkconfig} --add zabbix-agent &>/dev/null || :
%endif


%post server-mysql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server &>/dev/null || :
%endif
%{__updalternatives} --install %{_sbindir}/zabbix_server \
        zabbix-server %{_sbindir}/zabbix_server_mysql 10
exit 0


%post server-pgsql
%if 0%{?rhel} >= 7
%systemd_post zabbix-server.service
%else
%{__chkconfig} --add zabbix-server &>/dev/null || :
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


%post java-gateway
%if 0%{?rhel} >= 7
%systemd_post zabbix-java-gateway.service
%else
%{__chkconfig} --add zabbix-java-gateway
%endif

exit 0


%preun agent
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-agent.service
%else
%{__service} zabbix-agent stop &>/dev/null || :
%{__chkconfig} --del zabbix-agent
%endif
fi
exit 0


%preun server-mysql
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-server.service
%else
%{__service} zabbix-server stop &>/dev/null || :
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
%{__service} zabbix-server stop &>/dev/null || :
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
%{__service} zabbix-proxy stop &>/dev/null || :
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
%{__service} zabbix-proxy stop &>/dev/null || :
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
%{__service} zabbix-proxy stop &>/dev/null || :
%{__chkconfig} --del zabbix-proxy
%endif
%{__updalternatives} --remove zabbix-proxy \
        %{_sbindir}/zabbix_proxy_sqlite3
fi
exit 0


%preun java-gateway
if [[ $1 -eq 0 ]]; then
%if 0%{?rhel} >= 7
%systemd_preun zabbix-java-gateway.service
%else
%{__service} zabbix-java-gateway stop &>/dev/null || :
%{__chkconfig} --del zabbix-java-gateway
%endif
fi
exit 0


%postun agent
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-agent.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-agent try-restart &>/dev/null || :
fi
%endif


%postun server-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-server try-restart &>/dev/null || :
fi
%endif


%postun server-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-server.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-server try-restart &>/dev/null || :
fi
%endif


%postun proxy-mysql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart &>/dev/null || :
fi
%endif


%postun proxy-pgsql
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart &>/dev/null || :
fi
%endif


%postun proxy-sqlite3
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-proxy.service
%else
if [[ $1 -ge 1 ]] ; then
%{__service} zabbix-proxy try-restart &>/dev/null || :
fi
%endif

%postun java-gateway
%if 0%{?rhel} >= 7
%systemd_postun_with_restart zabbix-java-gateway.service
%else
if [[ $1 -ge 1 ]]; then
%{__service} zabbix-java-gateway try-restart &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
# no files for you

%files agent
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_sysconfdir}/zabbix/zabbix_agentd.d
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-agent.service
%{_libdir32}/tmpfiles.d/zabbix-agent.conf
%else
%{_sysconfdir}/init.d/zabbix-agent
%endif

%files js
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/zabbix_js

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
%{_libdir32}/tmpfiles.d/zabbix-server.conf
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
%{_libdir32}/tmpfiles.d/zabbix-server.conf
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
%{_libdir32}/tmpfiles.d/zabbix-proxy.conf
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
%{_libdir32}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_pgsql

%files proxy-sqlite3
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_sysconfdir}/zabbix/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%attr(0750,%{service_user},%{service_group}) %dir %{service_home}
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%attr(0640,root,%{service_group}) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf
%{_mandir}/man8/zabbix_proxy.8*
%if 0%{?rhel} >= 7
%{_unitdir}/zabbix-proxy.service
%{_libdir32}/tmpfiles.d/zabbix-proxy.conf
%else
%{_sysconfdir}/init.d/zabbix-proxy
%endif
%{_sbindir}/zabbix_proxy_sqlite3

%files java-gateway
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-java-gateway
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/log/zabbix
%attr(0755,%{service_user},%{service_group}) %dir %{_localstatedir}/run/zabbix
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_java_gateway.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_java_gateway_logback.xml
%{_datadir}/zabbix-java-gateway
%if 0%{?rhel} >= 7
%{_sbindir}/zabbix_java_gateway
%{_unitdir}/zabbix-java-gateway.service
%{_libdir32}/tmpfiles.d/zabbix-java-gateway.conf
%else
%{_sysconfdir}/init.d/zabbix-java-gateway
%endif

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
# no files for you

%files web-pgsql
%defattr(-,root,root,-)
# no files for you

################################################################################

%changelog
* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 4.4.5-0
- Added zabbix_js command line utility for embedded javascript testing
- Added new key vfs.fs.get to collect mounted filesystems information and
  relevant metrics into json
- Added "template app haproxy"
- Added media "pagerduty"
- Added "template db redis" template
- Added housekeeping of unused/deleted items values in value cache
- Added media "slack"
- Added redis plugin for agent2
- Added windows support to agent2 file plugin
- Added strict validation of input parameters in script.get() method
- Reworked template linking with multiselect and loading macro list with ajax
- Fixed maintenance time period update every field validation
- Fixed file change time in vfs.file.time on windows
- Fixed allowing user to enter blank spaces in media type webhook parameter
  names, script and menu entry name and url fields
- Fixed memory leak and wrong type cast; thanks to yudai hashimoto for the patch
- Fixed sql error during prototype removal by adding select for update locks
- Added bulk gathering of attributes for zabbix java gateway when using
  attribute discovery
- Fixed time of check - time of use issues reported by coverity
- Fixed memory leak in alert manager
- Fixed 'opdata' property in event.get and problem.get for events without
  triggers
- Fixed providing notifications for devices without audio support
- Fixed crash on jsonpath function processing
- Fixed deadlock on maintenance table when using oracle database
- Icmppingloss counting all after first 400 ping responses as lost
- Fixed error when creating user with long password
- Fixed httpstepid validation when its value exceeds int32
- Fixed agent2 build failure on 32-bit platforms
- Fixed web scenario step allowing to use 0 timeout
- Fixed duplicate entry errors on 32-bit architecture during item application
  discovery
- Fixed scroll bar visibility in svg graph widget configuration form
- Fixed non well formed numeric value encountered in maintenance
- Fixed indistinguishable validation messages for graph axis and unified graph
  validation messages in overrides
- Fixed db2 data import script
- Fixed spelling issues in the code
- Reverted fix for axis labels calculation
- Fixed dynamic rows losing old input at form error
- Fixed aria-live message partially visible beneath multiselect controls
- Fixed not operator in correlation function expression

* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 4.4.4-0
- Added pushover webhook integration
- Added media "mattermost"
- Added media "opsgenie"
- Added agent2 windows build support
- Implemented 'delete missing' option for imported template linkages
- Updated templates to internal version v0.34
- Added windows services template, updated windows template objects
  descriptions, added missing user macro
- Added missing webhook parameters to default database data
- Fixed url validation before output
- Fixed agent2 plugin configuration not being called if no plugin specific
  parameters are set
- Fixed lld macro substitution when postgrsql is used
- Removed redundant code block
- Added missing get parameters in availability report
- Fixed graph widget dimensions errors on high dpi screens
- Fixed fatal error occurring in user profile and user edit forms when php
  fileinfo extension does not exist
- Fixed incorrect double quotes in history plain text view
- Fixed widget saving with slow internet connection
- Fixed validation of "interfaceid" field for http agent items with large ids
- Fixed support for php 7.4
- Changed condition description message for tag value in actions and event
  correlations
- Fixed context-aware lld macro expansion in jsonpath preprocessing
- Fixed multiselect searching suggests in template mass update
- Fixed high memory usage during startup
- Fixed agent2 passive check timemouts exhausting plugin capacity
- Fixed build fail on netbsd
- Fixed request not being cancelled along with popup window in widgets
- Removed templateid from screen api output
- Fixed server check warning width in chrome
- Fixed graph widget scroll disappear
- Fixed widget vertically stretch
- Fixed undefined offset in problem by severity widget
- Fixed "type of information" field in item form being marked as required when
  it is read-only
- Fixed image map elements having a hand cursor when there is no context menu
  available
- Fixed axis labels calculation
- Fixed long snmp oid value goes beyond fields block
- Updated zabbix website links
- Fixed map-type widget clipping in internet explorer
- Fixed memory leak
- Improved zabbix server performance when using maintenance
- Fixed infinite loop when writing export to file fails
- Splitted host_resources templates into 3 subtemplates: for cpu, memory and
  storage
- Fixed graph widget multiselect collapse
- Fixed flexible textarea behavior

* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 4.4.3-0
- Fixed agent memory leak

* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 4.4.2-0
- Moved lld rules from parent templates to linked templates for module
  host-resources-mib snmpv2, module interfaces windows snmpv2, net arista
  snmpv2, os windows snmpv2
- Changed agent2 plugin configuration, moved maxlinespersecond,
  enableremotecommands, logremotecommands from global to plugin configuration
- Fixed not setting the default values of multiselects on initial load
- Reworked custom item select to multiselect
- Added compression support for zabbix agent 2
- Disabled guest user by default
- Added scrollbars for item and problem descriptions
- Implemented in monitoring -> problems the button "export to csv" to export
  all pages
- Fixed performance of history syncers and timer processes by not locking each
  other when suppressing events
- Fixed links to usergroups in user list
- Added range validation and optional conversion to is_double()
- Fixed "y-axis" graph widget field type
- Fixed log rotation on windows
- Fixed dynamic graphs not updating when changing host in combo box
- Fixed "readonly" feature for checkbox and combobox
- Fixed json null value being treated as empty string for lld filters
- Fixed array_db validation when validated value is not an array
- Made user profile icon visible for guest user
- Implemeted webhook returned tags preview in media type test modal window,
  added server improvements in webhook processing, removed webhooks from
  watchdog media type lists
- Moved interface_type_priority definition to misc.c
- Fixed the process of saving the scroll position on the latest data page in
  internet explorer
- Fixed lld not to create items on wrong host if there are failed transactions
- Fixed disappearance of successful modification message while saving the
  dashboards
- Fixed preprocessing regex for ping.time
- Fixed possible out of bounds access in csv to json preprocessing
- Fixed wrong placeholder in graph widget form
- Fixed throttled lld items being shown in queue when monitored through
  zabbix proxy
- Fixed username and password fields resetting and saving for item, item
  prototype and lld rule on type change
- Improved performance of timer process when reading from "problem_tag" table
- Fixed multiselect suggest box clipping when overflowing not allowed in parent
  containers
- Fixed undefined offset error in action operation condition form
- Optimized active logs checks monitoring when buffer flushing fails
- Fixed wrong element label update in map constructor
- Fixed zabbix agent 2 compilation on i386, arm, ppc64le and s390x architectures
- Fixed {trigger.id} to be supported on trigger level in addition to host level
  and template level tags
- Fixed problems by severity widget problem duplication
- Fixed widget form positioing when changing widget type from graph to any
  other type
- Fixed unneeded padding for dashboard url widget
- Fixed oracle performance by using "between" operator in sql queries
- Fixed long text wrapping in the latest data history
- Fixed possible null pointer arithmetic; thanks to mikhail grigorev for
  the patch
- Fixed go compiler check during configuration
- Fixed missing maxlength property for global macros description field
- Fixed sla calculation when requested time window starts during the service
  time; fixed downtime time calculation
- Fixed when the httptest api selects too many entries from the httpstep table
  when editing a specific web scenario
- Fixed disappearing dependent trigger cells and rows in overview
- Added handling of bom to detect encoding for vfs.file.contents, vfs.file.regex
  and vfs.file.regmatch
- Added support of event.tags.<name> macros to trigger based notifications
- Fixed wrong tab number being remembered when several browser tabs are in use
- Fixed sort order in plain text screen
- Fixed checkboxes of "connections from host" in host prototype encryption tab
  not being disabled

* Sun Nov 10 2019 Andrey Kulikov <avk@brewkeeper.net> - 4.4.1-0
- Implemented host api inventory_mode field as part of host object
- Added support of {trigger.id} macro in trigger tags
- Fixed accessibility of localstorage identifier if cookies are made
  unaccessible for client side scripts
- Fixed when widgets content is not stretched over the whole widget area on
  safari
- Fixed visual overlay of timeline dots on widget header
- Fixed oracle character set mismatch error
- Fixed trigger not firing for first collected value if it's timestamp is in
  future
- Fixed stdout and stderr redirection after external log rotation
- Added key 'tests' for bootstrap.sh when working with cmocka tests
- Fixed incorrect displaying of unacknowledged and resolved recent problematic
  triggers in trigger overview and dashboard widget
- Improved performance and memory consumption of script.getscriptsbyhosts()
  method
- Fixed detection of fping minimal interval
- Fixed configuration.export method in api improperly formatting "application"
  property within "httptests" when exporting in json format
- Fixed typo in system templates
- Fixed widgets with hidden headers not reacting on mouse hovering
- Fixed housekeeper to cleanup history not only for current item type of
  information but also for other previously selected types
- Added support for more than 64 cpus in windows agent
- Fixed value mapping in template net hp comware hh3c snmp
- Fixed spelling issues in the code
- Fixed support of libcurl version less than 7.38 for kerberos
  authentification
- Fgixed empty transaction to database in lld worker
- Fixed fping double call
- Fixed log.h is not self-sufficient
- Fixed broken validation of peer certificate issuer and subject strings in
  tls connect, fixed logging
- Ensuring errbuf is emptied before every curl_easy_perform request
- Fixed ipmi poller skips processing if one of the elements is missing
  information
- Fixed server crashing when linking web scenario template
- Fixed zabbix_sender failing to report the error due to closed connection
- Added new macro event.recovery.name to display recovery event name in
  recovery alerts
- Fixed false item insertion into the queue after maintenance
- Fixed to allow custom intervals for active zabbix agent
- Improved embedded script curlhttprequest object internal error handling
- Fixed error in the elastic search clearing history
- Fixed log items graphs drawing with numeric values like trapper items
- Fixed occurrence of an undefined index in discovered graph configuration
- Fixed disappearing new widget placeholder in dashboard edit mode
- Fixed unsupported option "only_hostid" in template screens constructor
- Fixed memory and performance leaks in gtlc.js library
- Fixed incorrect triggers being displayed in availability report when
  filtering by template
- Fixed displaying of "acknowledge" menu option for "not classified" problems
  in the trigger overview page
- Fixed sigbus crash when mmap memory is not accessible
- Fixed freeing locked resources when zabbix agent cannot be started and has
  to exit with failure
- Fixed trailing slash being set in cookie path
- Fixed possibility of high cpu usage on windows
- Fixed race condition between history syncer and escalator that caused
  recovery operations being delayed by step duration
- Getting disk controller type from linked controller label value
- Fixed jsonpath parsing for comma characters inside quoted string
- Fixed empty sql query dbexecute_overflowed_sql call during host availability
  update
- Adjusted timer sleeping period to process maintenances each minute
  at 00 seconds
- Changed agent.ping type to zabbix_passive in template module zabbix agent

* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 4.2.4-0
- Extended preprocessing steps with final result row; improved input validation
  in preprocessing steps
- Added access to vmware datastore at vmware vcenter level
- Added display of maintenance information in configuration section for hosts
  in maitenance
- Added preloader for popup menus
- Added ssl support for agent http checks
- Added option to specify absolute path in loadmodule; thanks to glebs
  ivanovskis for the patch
- Fixed windows agent build
- Fixed value trim in multiline input
- Fixed zabbix_sender does not clean up its semaphores
- Fixed not data loss on saving host prototypes by user with insufficient
  permissions
- Fixed checkbox selection on navigate to inherited template in triggers and
  items
- Fixed errors when trying to create a graph widget for key
  system.cpu.util[,iowait] with y axis placed on the left side of the graph
- Added output sanitization to prevent invalid utf-8 sequences in regexp-based
  text replacement
- Fixed horizontal scrolling in map
- Fixed discovered hosts are not removed from table "dhosts" after removing and
  adding the corresponding discovery check
- Fixed colors for the multiselect disabled elements
- 'it services --> service time --> note' infinite stretching
- Fixed web scenarios pair manager issue when fields are duplicating on post
  type toggle
- Fixed missing sys/ioctl.h from src/libs/zbxsysinfo/openbsd/net.c; thanks to
  andrea biscuola for the patch
- Fixed zabbix fping feature detection does not work with fping builds since
  10 feb 2017
- Fixed distributive can contain untracked backup file include/config.h.in~
- Fixed crash in global event correlation
- Fixed "system.cpu.util" reporting incorrect cpu utilisation due to guest time
  sometimes not being fully included in user time by "/proc/stat"
- Fixed widgets flickering on refresh
- Improved trigger expression list in trigger modal form
- Fixed windows agent "eventlog" key for reading big event log files of
  windows 2003
- Fixed hidden error in graphs for php 7.3.5
- Fixed regular expression file systems for discovery does not contain apfs
- Fixed setup page to not to use bclib
- Fixed dashboard map widget sub-map link behaviour
- Fixed to host group limited global scripts to be usable in sub group
- Fixed return value type and added preprocessing steps for items in remote
  internal checks tamplates; fixed unsigned write cache value for remote
  internal checks
- Changed proxy to send timestamps of empty historical values to server, so
  throttled items are not listed in administration/queue
- Fixed http agent support of non-http scheme in url field
- Fixed theoretical possibility of large numbers in json data being truncated,
  added boolean value support to json parser
- Fixed wrong filtering by "age less than" and "show suppressed problems" in
  trigger overview
- Fixed inactive, unmounted, unaccessible vmware datastore causes unknown
  column nan insertion in field list
- Fixed api validation of trigger dependency

* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 4.2.3-0
- Reverted changes that introduced error with write permissions in assets
  directory

* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 4.2.2-0
- Upgraded jquery version v1.10.2 -> v3.3.1 and jqueryui v1.10.3 -> v1.12.1
- Changed application filtering to partial name search
- Fixed linking error if round() is undefined
- Added file revision number generation for compilation on ms windows
- Fixed scrollbar in overlay popups
- Fixed error in ipmi poller causing growing queue
- Fixed division by zero error in svg graph widget if selected time period is
  so small that calculated step between 2 milestones is 0s
- Removed "change password" button when cloning media types
- Changed sorting by type, fixed information disclosure and formatting of
  recipient name in action log screen item and dashboard widget; added new
  sortfields to alert api
- Fixed locale validation in user create and update api methods
- Fixed tab key navigation for safari and edge browsers
- Fixed trigger dependencies are ignored when changing only trigger state
- Fixed api validation messages for linktrigger
- Fixed buffer offset for reading hardware info from long dmi files
- Fixed detection of logical functions (or / and) inside the context of
  user macros
- Deliver human friendly uptime in dashbord
- Fixed transparency of draggable interfaces; changed cursor type for all
  draggable and sortable elements
- Fixed global search box loosing the search phrase after searching
- Fixed several object ids allowing them to be 64 bit integers, added
  asterisk for map navigation tree name field and changed the error message
  to more generic one
- Added state preservation eol
- Fixed map element link coloring when linked problem is acknowledged
- Fixed http poller crashes
- Fixed trigger list checkboxes when filtering by single host
- Fixed problem events to be filtered by "suppressed" instead of "related to
  maintenance"
- Made "test all steps" button be available only when at least 2 preprocessing
  steps are created
- Added warnings when zabbix components have different versions
- Removed sid url argument for form cancel buttons
- Fixed macro not being retained in trigger expression editing wizard
- Increased header value input field max length
- Fixed items being stuck in unsupported state under some conditions when
  "discard unchanged" preprocessing step is used
- Fixed the process of compiling the dummy.c module
- Fixed invalid xpath for vmware "eventlog" key with "skip" option
- Fixed sending log meta information without obvious needs
- Added versioning of browser cached files
- Reduced configuration cache fragmentation when reloading time based triggers
- Improved performance of "remove host", "remove from host group", "unlink
  from template" operations when processing network discovery events and using
  mysql database
- Fixed when undefined index: rows_per_page on global search screen
- Fixed infinite loop and 100% cpu usage when using openipmi 2.0.26 or newer
- Fixed "{{item.value}.regsub(<pattern>,<output>}" and
  "{{item.lastvalue}.regsub(<pattern>,<output>}" being resolved
  to *unknown* during upgrade

* Mon Apr 22 2019 Andrey Kulikov <avk@brewkeeper.net> - 4.2.1-0
- Increased socket response size limit
- Fixed host.conn, host.ip, ipaddress and host.dns macros expansion in global
  scripts
- Fixed uncontrolled memory allocation in regex preprocessing steps
- Fixed guest sign in visibility for disabled guest user group in login page
- Fixed validation of host interface when multiple interfaces set as main
  interface
- Fixed security vulnerability - accepting connections from not allowed
  addresses
- Fixed when long snmp oid expands screen dimensions
- Fixed error message for image uploads
- Fixed not encoded ampersand for in url parameter
- Fixed possible crash of the windows agent when used "net.dns" item key
- Fixed map status to be displayed ok if there are no problem in submaps
- Fixed invalid update intervals being reported on zabbix server when monitored
  through zabbix proxy
- Fixed invalid to valid numbers conversion by del_zeros
- Fixed trimming allowed characters from numeric values
- Improved zabbix java gateway error logging usability by adding item key to
  error message
- Fixed inability to start zabbix server if alert manager process is late after
  alerters; thanks to mikhail makurov for the patch
- Implemented a better network discovery filter
- Fixed top right global search field autocomplete not showing results when host
  name is being typed not first character and technical name when it differs
  from visible name
- Changed user name and password fields from being mandatory to optional in web
  scenarios and http agent type items
- Improved logging performance when high debuglevel is used
- Fixed api returns "countoutput", "select*": "count" results and "suppressed"
  property as integer
- Fixed bigint limit in the user group updating forms
- Fixed sorting of items, item prototypes, lld rules and screens to avoid
  deadlocks in database between server and frontend
- Fixed line length above widgets on global search page
- Fixed password being passed in plain text in media type edit form
- Fixed dashboard widgets incorrect placement while dragged
- Fixed svg graph metric generation in situation when metric have big values
- Fixed element removing from list in different tabs or browsers
- Fixed loss of host name in tooltip on trigger overview page
- Fixed compilation warning regarding too large integer constant
- Fixed item/trigger/graph copy form provides read-only host groups in target
  list; replaced form elements with multiselect
- Fixed last problem name being displayed on map instead of most critical
- Fixed escalation operation not being send multiple times
- Fixed escaping of control characters in json encoder
- Fixed link to pie graph after selecting a time interval on classic graph
- Fixed multiselect does not support case sensitive auto-complete
- Changed placeholder for http proxy input fields
- Fixed map on screen is not centered
- Fixed sending first value of the log as separate message
- Fixed cookie presentation in http header
- Fixed trapper process title to not update time in case of interruption
- Fixed function names that are written to the log file when using
  log_level_debug
- Fixed update intervals of items in vmware templates
- Fixed showing wrench icon for hosts that are in maintenance, but
  maintenance is inaccessible due to insufficient permissions
- Fixed trigger wizard form re-submit
- Fixed problems by severity filter ignoring host group filter
- Fixed empty parent group not listed in the latest data filter
- Moved preprocessing steps into separate tab in items and item prototype
  massupdate form
- Added "unknown command error" to mysql recoverable error list
- Fixed redundant jsloader loading in login page
- Fixed item filtering by application name; added 'select' button for dashboard
  widget and screen item application fields
- Fixed lld item displaying in queue details view
- Fixed labels overlapping on classic graph x axis
- Fixed database monitoring 'dns' item key expressing it as mandatory
- Fixed map.create could attach elements only for first map in request when
  multiple maps are created with one request
- Fixed new widget placeholder being shown outside maximum allowed dashboard
  height area
- Fixed browser build in autofill for passwords field on media type form on
  authentication ldap form and on user edit form
- Fixed application filter persistence when navigating from maps page to
  triggers views page or latest data page
- Removed unnecessary request for non-existing map background and fixed
  undefined index when creating default image
- Added missing keys "zabbix.stats[<ip>,<port>]",
  "zabbix.stats[<ip>,<port>,queue,<from>,<to>]" and
  "zabbix[stats,<ip>,<port>,queue,<from>,<to>]" in item key helper
- Fixed positioning of the overlay dialogue window in map constructor
- Added missing optional parameter "<regex_excl_dir>" for "vfs.dir.count" and
  "vfs.dir.size" item keys in item helper
- Fixed action condition type and operator integrity
- Fixed possible crash when sending custom alerts
- Fixed possible deadlock on host table when processing auto registration
  contents from zabbix proxy
- Added blocking of sigint and sigterm signals on each step of automatic upgrade
  to avoid interruption of statements that cannot be rolled back
- Fixed global regular expression testing not matching actual behavior of zabbix
  components due to missing multiline flag
- Fixed possible crash in history syncer process when processing discovered item
  value
- Fixed slow request of vmware configuration update
- Fixed nodata() function triggering after maintenances with no data collection
  without waiting for the nodata period
- Fixed item prototype update intervals to eliminate trigger status flapping
- Fixed changing process user owner on startup in foreground when allowroot
  disabled
- Optimized unsupported macros parsing
- Fixed network discovery is not reacting to the changes in agent configuration
  if uniqueness criteria is value
- Fixed database monitor item does not use stored credentials; thanks to jose
  deniz for the patch

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 4.0.3-0
- added column "Latest values" in Monitoring->Problems and Dashboard
- implemented widget pausing methods in dashboard; made graph widget paused
  when using selection box or opening a tooltip
- fixed zoomout on doubleclick in graph widget
- fixed display parent host groups without hosts in multiselect
- fixed deprecated net-snmp attribute
- fixed configuration sync of interfaces without hosts
- fixed updating nextcheck time in discovery rules to avoid overlaps between
  discovery executions
- fixed regexp validation when pattern contain slash character
- fixed incorrect keycode handling in multiselect input fields
- fixed trigger overview behavior when show "any"
- fixed performance with deletion of item in template linked to many hosts
- added new LLD macros for vmware HV low-level discovery
- fixed colorpicker tooltip update
- fixed "check now" being executed for active items and templates
- fixed custom interval validation; fixed parsing of custom intervals when user
  macros context contains forward slash
- fixed community default value in edit scenario
- fixed memory of performance counters consumed during vmware update
- updated Tomcat template for compatibility with recent Tomcat versions
- fixed API authentication for ldap users having gui access disabled
- fixed misleading ldap authentication error messages
- fixed style of disabled action on high contrast theme
- removed strict-transport-security header from frontend
- fixed negative time selector offset when selecting time range in graph
- fixed creation of unneeded database record if host prototype inventory mode
  is disabled; fixed validation for host and host prototype inventory mode
- fixed SQL error occurred when too long IP address is attempted to be written
  in database
- fixed web scenario item selection in SVG graph widget
- fixed error handling in logrt[] items if regular expression for file name
  is not valid
- fixed resolving of functional macros in graph widget name
- fixed host, trigger and item count calculation; fixed required performance
  calculation
- fixed graph name for cache usage in proxy and server templates
- fixed wrong behaviour when referencing unexisting capture groups in item
  regexp preprocessing, general pcre code improvements

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 4.0.2-0
- added validation of update interval, custom interval, history storage period
  and trend storage period in low-level discovery
- removed hardcoded locations for iconv.h and pthread.h; thanks to Helmut Grohne
  for the patch
- fixed compilation errors on Windows platform with static OpenSSL libraries
- added license information and OpenSSL linking exception to README file, show
  crypto library version when started with '-V'
- fixed crash in ODBC when creating JSON from null db values, fixed memory leak
- fixed a case where a disable multiselect looks like a similar to enabled text
  field
- fixed filter by host group without real hosts in triggers top 100, dashboard
  widgets, screens
- fixed duplication of file system type in global regular expression for file
  systems discovery
- added system.cpu.util[,guest], system.cpu.util[,guest_nice] to OS Linux
  template
- improved error messages for item preprocessing, general pcre code improvements
- fixed curl error handling for elasticsearch history backend
- added optional upgrade patches to rename TRIGGER.NAME macros to EVENT.NAME
  in action operation messages and custom scripts
- fixed processing of unlimited vmware maxQueryMetrics value
- fixed rare LLD failures when moving host between groups
- fixed loss of calc_fnc index in graph edit form
- improved escalator performance during maintenance by checking paused
  escalations less frequently
- fixed focus styles on read-only textarea fields
- fixed percentage calculation on availability reports list page
- fixed error message when receiving compressed data over maximum size
- fixed time period parameters in data overview context menu links
- fixed javascript error when zooming classic graph in edit mode
- fixed dashboard initialization in edit mode
- fixed timetamp position in map
- fixed zoom-out and select box for graphs in kiosk mode
- improved source code comments
- fixed wrong media type status upon creation, if chosen status disabled
- fixed wrong net.tcp.listen values on obsolete Linux systems
- fixed issue with autoreconf/automake for source tarball
- fixed time format for vmware performance counters query
- fixed regexp compilation error for patterns with referenced subpatterns
- fixed breadcrumb jumping in IE browser
- fixed API so that macros {TRIGGER.ID} works in map element URLs
- fixed possible crash when communication problem occurred in the middle of
  vmware update
- fixed excessive memory usage during template full clone
- clarified process type names for log level increase/decrease in help messages
  and man pages
- fixed selectHosts option in dservice.get API method to return the list of
  hosts by IP and proxy
- fixed binary heap trying to reallocate slots on every insert
- fixed unauthorized request error when resetting filter after
  enabling/disabling elements
- fixed translations from en_US to en_GB
- fixed encoding for cookie names and values
- fixed possible crash in web monitoring due to posts not being reset between
  steps
- fixed faulty behaviour of mandatory fields in Trigger expression form
- added support of host macros to trapper, HTTP agent item allowed hosts field
- fixed shared memory leak during configuration cache synchronization
- fixed email alerts being sent twice to one recipient
- fixed possibility to link map widget to itself as filter widget
- fixed undefined offset error in Problems by severity widget
- fixed memory leak when validating regular expression preprocessing step
  parameters during LLD
- changed SNMP OID default value to be displayed as placeholder instead of text
- fixed compiler warning about incompatible pointer type on 32-bit platform
- fixed error suppression during php ldap module initialization
- fixed link coloring in map when related trigger is not monitored
- fixed sBox position in screen's graph item when dynamic item is enabled
- fixed not closed connection with vmware at the end of update session via a
  call to Logout()
- fixed current map refresh in map widget right after update widget
  configuration
- added missing http agent statistic row in queue screen
- fixed missing focus from problem name when opening description editing popup
  in monitoring problems section
- fixed configuration update in administration authentication section
- fixed memory leak in case duplication name of the vmware performance counters
- made widget specific javascript files to be loaded with jsLoader
- fixed the potential crash during vmware update
- removed the notes about sqlite from zabbix_server.conf
- fixed discovery and auto registration escalations being kept for one hour
  instead of deleted immediately
- fixed SQL queries being logged when accessing API, even if debug mode is
  disabled
- fixed error reporting for XML import of hosts and templates
- fixed action popup being unclosable after widget refresh, fixed debug element
  being hidden on widget refresh
- changed focus style for radio buttons
- fixed startup failures due to orphaned or zombie processes remaining when
  zabbix daemon is terminated during startup

* Mon Nov 19 2018 Andrey Kulikov <avk@brewkeeper.net> - 4.0.1-0
- added filter fields to select templates and hosts by directly linked
  templates; made proxy filter field visible in configuration hosts field
- added 'fullscreen' and 'kiosk' URL arguments to allow to set layout mode
  via link
- improve out of memory error message by adding statistics and
  backtrace;
- improve something impossible has just happened error message by adding
  backtrace
- improved escalator performance by using nextcheck index instead of reading
  whole table
- fixed possible PHP errors in "Problem hosts" widget
- fixed possible crash when syncing host groups
- fixed selection box for graphs on monitoring screens
- extended support of system.stat[ent], system.stat[cpu,pc],
  system.stat[cpu,ec] on IBM AIX to LPAR type 'dedicated'
- fixed the host visible name in the event details/messages from server
  when using long utf8 text
- fixed max count of records in the single json that proxy can send
  to the server
- fixed the case where data from non-monitored VMware services are not removed
  from vmware cache
- added support for OpenSSL 1.1.1
- added note on runtime control with PID numbers larger than 65535 to server,
  proxy and agentd help messages and man pages
- fixed the verification of the assignment of two web checks with the same name
  from different templates to one host
- fixed cloning inherited host prototype on host
- fixed calculation of Y zero position in graph
- fixed "Field "parent_itemid" cannot be set to NULL" error message
  while importing multiple templates
- added support of user language specific url link in support icon,
  supported languages: english as default, japanese, russian
- improved preprocessor worker performance
- fixed incorrect zero rounding in date and time fields
- fixed sql error in escalator when working with Oracle,
  PostgreSQL (less than v9.4) databases
- fixed incorrect translation string in en_US locale
- fixed fields becoming writable upon form refresh in host prototype form
- fixed 'follow redirects' checkbox in web scenario step's dialog
- fixed color of the host name in the title of the Screens
- fixed sorting when changing status of media type
- fixed triggers in trigger overview being filtered by trigger severity and
  trigger status change time instead of problem severity
  and problem creation time
- fixed updating of the Graph list of host when selecting a group of hosts
- removed links to templates with no permissions for templated triggers,
  trigger prototypes, graphs, graph prototypes, host prototypes
  and web scenarios
- fixed trigger evaluation result not visible in test dialogue when expression
  is too long
- fixed zoom button for time selector in IE browser
- fixed table markup on overview and system info pages
- fixed plain text Latest data when selecting more than 1 item
- fixed host prototype status checkbox resets after adding template
- fixed minor typos in comments and tests
- fixed icon misplacement in problem view
- fixed incorrect profile update causing page filter to sometimes show
  duplicate values
- fixed validation of double/Numeric(float) values
- fixed selection of data for trigger overview and graphs if first drop down
  entry is "none"
- fixed Java gateway not to mark host unreachable in case of invalid username
  and password
- fixed JMX endpoint not being included in error message in case of connection
  errors
- fixed web.page.regexp item parameters description
- fixed crash that could occur when OpenIPMI pollers are configured
- fixed crash in vmware collector when receiving invalid xml
- fixed crash when processing internal trigger events and deleting triggers
  at the same time

* Thu Sep 13 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.13-0
- replaced pcreposix library with pcre, lowered backtracking limit, fixed
  libevent build issues
- fixed vmware incorrect memory release
- fixed vmware performance counter retrieval on installations with large
  number of datastores
- fixed memory leak in alert manager when connection to database was lost
- renamed trigger functions by adding function name at the beginning and
  removing the operator and "N" and placing operator in a separate field
  allowing two new operators "<=" and ">=" for selection
- fixed incorrect behavior of zbxregexp library when reusing latest regular
  expression
- fixed error message for invalid vmware endpoint
- fixed trigger dependency link to the template instead of the host during the
  discovery action
- added "zone" parameter to proc.num[] item for Solaris
- fixed typo in string: ouf, not out
- fixed output of information about the error for expressions with functions of
  triggers or calculated items
- fixed several problems in displaying of X axis on the graphs

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.12-0
- fixed the disk usage counters reading for ESX/ESXi hosts
- fixed timeselector period used to select 'all' values of particular item
- fixed agent compilation error on AlphaServer Tru64 5.1B
- fixed Y-axis small value gradation issue in graphs
- fixed Norwegian locale key for windows
- fixed possible data loss due to MariaDB server restart
- fixed crash of poller processes in ODBC checks, simplified code
- fixed deleting of files after compiling a program (make clean) for Solaris
- fixed displaying timeline points of days in Problems widget
- fixed link "show value mappings", which leads to no permission page
- improved function parameter parsing for trigger functions
- disabled preprocessing update for discovered items
- fixed status change for linked template items through parent template if host
  assigned
- removed redundant code and improved performance in event details screen
- improved error message handling in zbx_function_find()
- fixed crash when reporting unknown triggers and using $1-$9 macros at the same
  time
- added limit ZBX_HISTORY_PERIOD for {ITEM.VALUE} macro resolving in trigger
  name
- fixed internal item parameter that does not match documentation

* Sun Jul 08 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.11-0
- added and enabled Norwegian translation to be displayed by default
- updated English (United States), French, Hebrew, Japanese,
  Portuguese (Brazil), Russian, Ukrainian translations; thanks to Zabbix
  translators
- fixed the functions 'net.if.*' for Solaris with empty 64 bits counters
- fixed media type a required password field successfully passing validation
  while being empty and prevented auto-filling stored passwords by browser
- improved "Server" parameter description in Zabbix agent configuration file
- reverted ZBX-13788 fix because of broken server-proxy compatibility between
  minor versions
- fixed logrt[] item to analyze log file from start if no log files match and
  no log files were seen before
- fixed discovered host status update if it was down and a service was
  discovered on that host
- fixed "proc.num" and "proc.mem" items calculation of values when zabbix_agentd
  called in test mode
- fixed use of initialized variable during application discovery
- improved "vmware.hv.datastore.size" through usage the performance counters

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.10-0
- fixed PHP 7.2 error message in the Monitoring->Latest data page
- fixed "Undefined index: master_itemid" and SQL errors in item.update and
  itemprototypr.update methods; fixed updating of discovered items
- fixed displaying of not monitored triggers in maps
- fixed "Automatic icon selection" checkbox not working and displaying two icons
  at once in map constructor
- fixed {ESC.HISTORY} and action log not to display colon without target host
  when executed on Zabbix server
- fixed error messages when configuring an existing item to have an update
  interval
- removed error message for when user has defined media but all of them are
  disabled
- fixed possible deadlock in history syncer when housekeeper is deleting events
- fixed session expiration when changing default authentication method
- fixed action not being cloned due to existing operation id being submitted
- fixed map tree widget border color
- fixed decoding of Unicode characters in JSON
- fixed "undefined index: acknowledges" error on problems page
- fixed subfilter entries with long names going off the screen
- fixed filter being partially reset when using pagination in availability
  report page
- fixed in popup window being allowed to select applications from different
  hosts when editing item mass update form
- fixed host availability stuck in unknown state after proxy changes
- fixed duplication of prefix "/" for second parameter "path" in items
  "web.page.*"
- fixed validation of "max_depth" in "vfs.dir.size" for agent

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.9-0
- fixed trigger level correlation when multiple tags are set
- fixed possible crash in the function "web.page.get" of Zabbix Agentd
- fixed persistent xss in map navigation tree widget
- fixed persistent xss vulnerability in services
- fixed multiple javascript memory leaks
- fixed proxy lastaccess update on 32-bit Zabbix server
- fixed selection of web items in the "Plain text" screen element
- fixed CRLF injection in Zabbix Agentd
- fixed comparison of two large float numbers in expressions
- fixed incorrect parsing of BITS data type in SNMP response
- fixed potential shared memory leak when item is removed
- fixed parsing of the operator "not" in trigger expression
- fixed trigger recovery expression for 'High error rate' trigger
- fixed trigger expression for 'Link down' trigger
- increased command line limit for proc.num checks on hp-ux systems
- fixed problem duration on trigger page being calculated incorrectly
- fixed data types passed to is_ushort() for converting PID, port and process
  number
- fixed displaying of floating point values under the "Latest data" page
- fixed unnecessary data getting when agent becomes available in the
  non-collection data period
- fixed maintenance entries displayed in list when filter is applied
- improved configure script to check iconv library
- added notification in zabbix server log about 'error' in elasticsearch json
  response
- fixed multiselect items not being sorted by name
- fixed autoregistration, discovery and internal notifications not being sent
  due to uninitialized severity
- changed ping script to return success also for timeouts
- fixed slide show refresh interval multiplier menu not working
- added maximum record limit to old session removal in housekeeper
- fixed undefined index in user edit form
- fixed dynamic widget searching for item key in item prototypes
- fixed fractional values in triggers being misinterpreted without a leading 0
- fixed incorrectly displayed pie graph when first item has no data
- fixed undefined index in pie charts
- fixed checkbox selector in problems table
- fixed crash when Zabbix process cannot connect to preprocessing service
- fixed blinking in the problem widget
- fixed acknowledge notifications being visible in the event popup
- fixed missing graph after faulty graph edit form submission

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.8-0
- implemented the widget configuration fields clearing when changing the type
- implemented maximum size for graphs in widgets
- enabled Hebrew translation to be displayed by default
- updated Chinese (China), Czech, English (United States), French, German,
  Hebrew, Japanese, Korean, Russian, Turkish, Ukrainian translations
- fixed http steps on template not inheriting hosts application setting
- fixed wrong variables order in translatable error message
- fixed trigger based actions having a default "not in maintenance" condition
- improved a history syncer when backend elasticsearch is not available
- fixed agent crashes when using regex with 'Log' item for Mac OSX
- fixed lld rules not always saving their state/error message changes
- fixed regression that resulted in slow history data queries on partitioned
  tables
- added possibility to select web items as master items and improved copying of
  dependent items to destination hosts and templates
- fixed undefined index message changing Action "Acknowledgment operations"
  from "Remote command" to "Notify all involved"
- fixed undefined index in API call
- removed "recovery" property from action.get API method response
- fixed displaying of Problem/Recovery time
- fixed server and proxy compilation problem for Solaris 10
- fixed resolving of the macros in map labels for non-superadmin users
- fixed widget placeholder jumping instead of resizing while dashboard edit
- fixed potentially wrong rows deleting by housekeeper in PostgreSQL
- fixed linked trigger is moved to sibling map element
- fixed trigger-based event correlation - suspend creation of event if no
  problems are recovered by it
- improved deallocation of memory
- fixed pie graphs displaying incorrect data
- fixed JS error and wrong form behaviour when changing item type, type of
  information, data type
- fixed display of the latest item in Audit log
- fixed trigger name readability on map in dark theme
- fixed HTML5 placeholder color that previously appeared like actual input data
- improved OpenSSL error messages
- fixed inconsistent number on map navigation tree
- fixed "Inaccessible user" in Dashboard System status widgets acknowledgement
  popup
- fixed description of "Server" and "ServerActive" configuration options
- added frontend error message when templates cannot be linked to LLD host
- fixed incorrect trigger dependencies being set after copying triggers to
  multiple hosts; thanks to Kotaro Miyashita for the patch
- fixed incorrect ordering the list of triggers after saving a map
- fixed content does not fit dialog window
- fixed successful items mass update with invalid update interval
- fixed order by query in frontend Maintenance tab
- fixed partial updating in maintenance.update
- banned using of mutex in threads of metrics collection
- fixed error message of function parameters parse
- fixed configure script for Debian GNU/Linux "buster" and "sid" to work with
  PostgreSQL
- fixed long name of map outside go back button in map widget
- fixed undefined index error in map import
- fixed daily and yearly notification reports not including current day/last
  day of leap-year
- added optional MySQL upgrade patch for "problem" table to drop redundant index
  after another index that can be used to enforce the foreign key constraint has
  been created
- fixed Elasticsearch history storage default value types
- fixed checkbox overlay's position over the checkbox
- fixed translations of Widget parameters window
- fixed field trapper_hosts to optional for trapper item.create
- fixed map scaling and position to the widget left side
- fixed poor performance of changing an item on the template which linked with
  many hosts
- fixed invalid value for "Update interval" field in mass update form on submit
  was redirecting to items list

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.7-0
- allowed proxy to execute remote commands on agents using encrypted connection
- fixed crashes in case of failures (e.g. timeouts) during VMware hypervisor
  discovery
- fixed performance of map.get API method and map-related views
- fixed compilation failure in Alpine Linux due to missing res_ninit() function
- fixed incorrect processing of zabbix[wcache,value,*] internal check
- added limitation for meaningless server reconnection attempts to incorrectly
  configured passive proxy
- fixed vfs.dir.size with symbol links on Windows
- improved error log message in case Zabbix server database cannot be used due
  to empty "users" table
- fixed memory leak which breaks vfs.fs.size, vfs.fs.inode and vfs.dir.size
  items if compiled with LeakSanitizer
- fixed truncated multiline text values from network discovery SNMP checks
- fixed last trends update clock caching
- fixed trend.get() method with Oracle backend
- fixed graphs duplication in graph preview
- fixed problems with DNS resolver interface on NetBSD
- removed SID from URL in screen edit mode
- added support of \0 matching group for regsub and iregsub methods
- eliminated race condition that caused history collection for newly created
  items to start before preprocecessing steps finished syncing
- fixed Zabbix proxy not to generate high network traffic when server does not
  accept data
- fixed image ghosting for mass update of map elements
- fixed processing of command line arguments which are longer than 2KB for
  proc.num and proc.mem items on AIX

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.6-0
- fixed compatibility issue with Elasticsearch versions starting from 6.0
- fixed latest data host group filter
- removed 'empty' button in trigger selection window for map constructor item
  modal form
- fixed Low-level discovery of dependent items not working after being edited
  and resulting in undefined offset error or foreign key constraint violation
- fixed 'skip' parameter behaviour for log[], log.count[], logrt[],
  logrt.count[] items in case log files initially do not exist
- fixed losing the 1st record by log[] and logrt[] items if 'skip' parameter
  is used and log file initially is empty
- fixed slow housekeeping of events on MySQL
- fixed IP fragmentation handling in Zabbix server response to Zabbix proxy
- fixed Java gateway compilation without libpcre
- removed default values for "active_since" and "active_till" fields in
  maintenance.create API method
- fixed default selection of the required host permissions radio in the global
  scripts form
- fixed slow housekeeping of events due to missing index on foreign key
- fixed color and label for event status on event details page
- fixed spelling of Elasticsearch
- fixed memory leak on Zabbix server when executing remote commands through
  proxy
- fixed ipc_path value in error message

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.5-0
- fixed compilation problem with old curl version for Elasticsearch support
- fixed problem when items might be synced without preprocessing steps if they
  were created during configuration cache synchronization
- fixed sort param logic for elasticseach
- fixed possibility of endless loop during unrecoverable database error; fixed
  incomplete handling of database error
- fixed database configuration error reporting and message filtering when
  messages are received from clear_messages function
- fixed last item value retrieval errors in history manager
- fixed empty host filter when adding dependent trigger in trigger edit form
- fixed parsing "request" parameter for URLs without input parameters
- fixed possibility that proxy last access updates are lost during cache reload
- fixed possible crash in history syncer when processing deleted item
- fixed cookie http-only attribute to prevent XSS attacks
- fixed reflected XSS vulnerability in popup forms
- fixed permissions check in script execution form
- fixed check for permissions to enable/disable actions
- performed network templates cleanup
- fixed TLS connection to passive proxy error handling
- fixed overflow property of svg
- fixed logic of commit/rollback operations
- fixed incomplete data in notification reports for yearly report types
- fixed alert error message visibility to unrelated users
- improved VMware event log data collection and processing
- relieved windows agent of dependency on MFC
- fixed missed url search part in request login parameter
- added --with-libpcre-lib configure option
- fixed undefined index when setting strict-transport-security http header
- fixed error causing empty list in popup window when opened from page having
  host group filter
- fixed percentile visibility in dashboard graph widgets
- added filter on event details page to show messages sent to users only from
  same groups
- fixed memory leak in preprocessing manager
- fixed mysql m4 configuration script for mariadb C connector
- fixed retaining the scrollbar position on page reload
- fixed multiselect not showing results for read-only objects in screen
  configuration
- fixed warning message shown by deprecated PHP 7.2 function create_function()
- fixed max length validation in textarea fields
- fixed floating range validation during conversion from uint64 to float
- fixed possibility of foreign key constraint failure due to events being
  removed before trigger data storage period expires
- fixed potentially incorrect delete procedure for problems and events
- fixed zabbix[java,,ping] to stay supported when java gateway is down
- improved performance of DB patch for updating data in the alerts table
- fixed possibility of host availability being stuck in unknown state when
  monitoring though proxy
- fixed Zabbix proxy not to send same host availability more than once
- fixed incorrect trigger dependency calculation when processing dependent
  triggers in the same history syncer batch
- fixed inheritance of template properties in web scenarios
- fixed translation string on administration general housekeeping page
- added missing key "vfs.dir.size" for active agent in item edit form
- fixed wrong default value for host filter when adding dependent trigger in
  trigger edit form
- fixed possibility to select triggers with same name in multiselect
- added missing fields to webscenario data handling
- fixed displaying highest severity when dashboard filter options contain
  unacknowledged only
- fixed CPU guest time utilization accounting in Linux
- improved performance of preprocessor manager, alert manager/worker, IPMI
  manager/poller by reducing frequency of log rotation checks that handle
  stdout/stderr
- improved SQL performance by updating proxy last access in bulks
- added check for collisions and unsupported characters in macro names in
  jmx.discovery
- fixed processing of alerts when related event is removed
- fixed compilation warnings

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.4-0
- added service sorting by name if multiple services has same 'sortorder' value
- added Windows service configuration check to determine if service can be
  trigger started
- implemented default widget refresh interval
- improved error message for case when none of supported database modules exists
- fixed multiple security issues
- fixed target list to be meaningless if custom set of commands is executed
  on zabbix server
- fixed update proxy lastaccess value when receiving data
- fixed crash of VMware collector with DebugLevel=4
- added floating value range validation for metrics calculated by server
- added validation for groupid and hostid parameters in dashboard view
- fixed error in action update when changing media type
- fixed CPU count for LPAR partitions in IBM AIX
- fixed problem.get and event.get API methods when "selectTags" option contains
  extended output
- fixed windows agent to support UTF-16LE, UCS-2, UCS-2LE encodings
- fixed last access not being updated for passive proxies after getting
  historical data
- fixed use of current host as filter when selecting items for graph forms
  and trigger forms
- fixed scrollbar causing a JS error in "500 latest values" page due to
  unnecessarily initialization
- fixed problem counting in host groups in navigation tree widget
- fixed OS type detection logic
- fixed problems with session management
- fixed {HOST.*} macro support in map trigger elements
- fixed advanced label support in map editing mode
- fixed ETag comparison check in jsLoader for web server with enabled
  compression
- fixed undefined index error in dashboard problems widget
- improved pre-processing manager performance when processing large number
  of values
- added an informative warning about lack of data for macros used in LLD
  rule filter

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.3-0
- modified server, proxy and agent to follow changes in /etc/resolv.conf
- fixed missing information in "Status of Zabbix" widget with huge sessions
  table
- fixed error when template is added to hosts via mass update form
- fixed trap, snmptrap items of log type not being processed by proxy
- fixed default value for JMX endpoint on item type change in edit form and mass
  update form
- fixed system.run, user parameter and external check not to become unsupported
  when exit code is different than zero
- fixed IT services calculation in parallel transactions not seeing each other
  changes when calculating common parent service
- fixed hanging of preprocessing manager process due to file descriptor limit
  exhaustion when too many data gathering processes are configured to start
- fixed IE and Opera specific javascript bug; improved the depth control of
  navigation tree items; improved coding style and performance
- fixed simple graph widget item support: only supported dynamic items, only
  real hosts, show only hosts with items
- added 'filter field should not be empty' validation for sysmap widget form
- fixed user permission check for macros containing user personal information
  in notification messages
- improved task database operations to handle/prevent creation of tasks without
  corresponding data records
- fixed {HOST.*} macro expansion for map trigger elements in map constructor
- fixed detection of PostgreSQL 10
- fixed simultaneous sending of the same history data from passive proxy
- fixed links in select popup for user groups; updated group selection field
  in Administration->Users
- fixed difference between item and web scenario item graphs on simple graph
  widget
- improved performance of hostgeneral.unlink() method; fixed SQL statement
- added horizontal scrollbar to the map in view mode; removed homepage label
  in maps and graphs; made graph timestamp visible only if debug-mode is on
- fixed error in simple graph widget for web scenario items
- fixed problem box stretching in navigation tree in IE11; fixed position of
  all navigation tree problem boxes in Edge
- fixed escaping of translation strings with apostrophe in forms: dashboard
  sharing and monitoring, administration of housekeeper and trigger options,
  item edit and mass update, xml import, host edit, web scenario, trigger
  configuration.
- fixed the housekeeper for not deleting events in open problem state
- moved item state,lastlogsize,mtime,lastclock configuration cache update
  from value reception to value processing
- reduced memory used by pre-processor manager item cache
- fixed error displaying of zabbix server status widget
- fixed SQL errors in event.get() method
- fixed possibility to enter deleys with suffixes for new elements of slideshows
- fixed behavior for graph prototypes when item prototype is deleted
- fixed response for script.get() method with "editable" flag
- fixed dcheck.get(), dhost.get() and dservice.get() permission checks for admin
  users

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.2-0
- improved permission schema of the dashboards for normal adminitrators
- removed starting point from all OIDs; shortened old IOS Cisco templates names
- added preprocessing_queue item/graph/screen widget in Template App Zabbix
  Server
- renamed action acknowledgment operation 'Notify all who left acknowledgement
  and comments' to 'Notify all involved'
- added users who received notifications regarding the problem to 'Notify all
  involved' acknowledgment operation recipient list
- enabled Turkish translation to be displayed by default
- updated Chinese (China), English (United States), Japanese, Korean, Turkish
  translations; thanks to Zabbix translators
- implemented feature to open first available dashboard from the list
- implemented dashboard widget minimum height limit
- fixed losing "now" on timeline
- fixed data conversion for ssh checks of numeric value type
- fixed service port validation if auto-discovery is performed by the zabbix
  proxy
- fixed crash when using item of log value type as master item for dependent
  items
- fixed processing of log keys with non log value types for items monitored
  by proxies
- fixed non well formed numeric value encaunteration in slideshow; implemented
  getBBox workaround for Firefox
- fixed false positives on 'High bandwidth usage' trigger in
  Template_Module_Interfaces_* templates
- fixed crash that could occur during connection failures to MySQL
- fixed sorting by host name for items on availability report page
- added support of strings in "sortfield" and "sortorder" parameters, and added
  sorting by "name" for dashboard.get()
- added item select filter for simple graph to allow select only supported item
- fixed map minimum severity option in screens
- fixed trigger not being calculated for newly received item values if last one
  of those is unsupported value
- fixed notification sound not being played for message with timeout set to
  greater than minute
- fixed heap corruption in Windows agent; thanks to Ronnie Kaech for the patch
- fixed result of hostinterface.replacehostinterfaces method
- added new context for 'Second' string to be properly translated in maintenance
  period form
- fixed trapper item "Allowed hosts" field user macro support
- fixed address and ports array size in zbx_init_ipmi_host() to match OpenIPMI
  internals
- fixed potential loss of data when server/proxy processes zabbix_sender data
- eliminated sending of DNS AAAA queries when checking IPv4 incoming connection
  in agent or for trapper item and A queries in case of IPv6
- fixed multiple browser sensitive javascript bugs in navigation tree widget
  and improved coding style
- fixed label macro resolving in maps
- implemented widget field validation before dashboard is loaded and fixed
  undefined index for tag field in dashboard widgets
- fixed macro expansion in map editor
- fixed graph not being displayed if item update interval contains macro
- fixed delayed first refresh in map widget; improved coding style
- fixed regular expression pre-processing step to fail if the pattern does
  not match input data
- allowed libcurl to choose SMTP authentication mechanism other than PLAIN
- fixed frontend side DNS parser logic to be same as server side DNS parser
  logic
- fixed trigger expression validation test form
- fixed scroll duration in dashboard after adding a new widget
- fixed housekeeping of problems and events for deleted items and triggers;
  added optional database patch to cleanup problems for deleted items and
  triggers
- fixed incorrect SQL query in availability reports
- fixed undefined index error on latest data page when host was deleted in
  another session
- optimized data selection of user preferences stored in profiles
- fixed removal of multiselect options using backspace button
- fixed a rounding of large unsigned numbers
- removed delay between sending batches of cached historical data by active
  proxies
- fixed item helper description for proc_info and diplay order for vfs.dir.size
- fixed line graph was displayed as points for data taken from trends
- fixed visibility of item data first row for 'latest data' page and 'audit log'
  page
- fixed maps not loading without built-in JSON support
- fixed incorrect subnet mask calculation when CIDR is less than 8
- fixed processing of lld rules in not supported state
- fixed parallel processing of multiple values for same lld rule
- fixed inconsistency of 'mode' parameter check in vfs_dir_size(); thanks to
  MATSUDA Daiki for patch
- fixed XML import when preprocessing param value is space character
- fixed possible SQL errors in dashboard.create() and dashboard.update() methods
- fixed improper DB::refreshIds() call when selected row is locked
- fixed memory related bugs in item preprocessing
- fixed trigger resolving in services configuration; fixed popup window size
- fixed an error in screens if screen trigger overview element contains
  deleted host group
- fixed template replacement in mass update form

* Thu Sep 14 2017 Andrey Kulikov <avk@brewkeeper.net> - 3.4.1-0
- fixed display of previously opened dashboard
- fixed displaying of graphs in the dashboard widgets;
  fixed displaying of the right axis in the graph test form
- updated Czech, English (United States), French, Italian, Japanese, Korean,
  Portuguese (Brazil), Russian, Ukrainian translations;
  thanks to Zabbix translators
- fixed an unneeded data sharing to map widget on navigation tree refresh
- fixed requeueing of items from unreachable poller to normal poller
- fixed sbox selection zone in monitoring web graphs
- fixed crash when syncing actions without operations
- removed usage of SVG viewBox attribute in IE and disabled map scaling in
  screens
- fixed wrong response and error message when invalid or unavailable dashboardid
  has been requested
- fixed overlay window displaying on different browsers and removed horizontal
  scrollbar from widget configuration dialogue
- fixed error when linking one template to another in template edit form
- fixed extra new lines in Templates
- fixed clock and map widget scaling on Safari
- fixed crash when linking templates with web scenarios during auto registration
- fixed XML import of web scenarios
- fixed DB upgrade patch for map shapes on DB2
- fixed multiple issues with dependent items
- fixed macro name field length in host configuration form

* Thu May 11 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.6-0
- fixed translation string and validation of TLS settings in host.create(),
  host.update() and host.massUpdate() methods; added variables to hosts array
  required by CHost::validateUpdate() method
- fixed problem generation by timer process
- fixed missing operator in event correlation form
- fixed collision of cookies name responsible for storing selected checkboxes
- fixed undefined index 'ns' in options output array
- fixed pagination in Maintenance page
- fixed limit option in event.get method
- fixed new line handling in SSH agent with numeric type of information
- fixed wrongly displayed list view after mass update failure

* Fri Apr 28 2017 Andrey Kulikov <avk@brewkeeper.net> - 3.2.4-1
- Fixed path to tmpfiles configuration files

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- improved bulk inserts for Oracle database backend
- optimized trigger expression batch processing to avoid recalculation of
  identical functions
- added option to control amount of queued items
- fixed wrong number round for cpu statistics
- fixed wrong averages in web monitoring if a web server doesn't respond to
  a request
- fixed button and multiselect positioning in action operations edit form
- fixed empty value handling in event correlation on oracle databases
- fixed Oracle and MySQL column limit calculation when using UTF-8
- removed possibility to execute commit without transaction in processing LLD
  rules
- fixed event correlation when using databases other than mysql
- fixed unnecessary notification sending from dependent triggers
- fixed handling database failure during transaction commit
- fixed resolving of user macros with context wich are defined on host or
  template level
- fixed cause of error with EventID 5858 in Windows EventLog when using
  wmi.get key
- fixed selection of ntext data from Microsoft SQL Server using 'db.odbc.select'
  item key
- fixed copying sharing properties while cloning slide shows
- fixed undefined index on Problem page with disabled guest user
- fixed possible deadlocks when removing obsolete VMWare services
- prevented requesting all screens in slide show when slide show screens are
  deleted
- fixed displaying maintenance icon for trigger element in maps
- fixed resolving macros for ip and dns fields in interfaces that are linked to
  main interface with {HOST.IP} and {HOST.DNS} macros
- fixed global regexps to be extracted from log.count[] and logrt.count[] keys
- improved performance for getting last value of web items by limiting query
  results for values in last 24h; thanks to D.Spindel Ljungmark for patch
- fixed dependency validation and update when trigger expression is changed
- fixed event acknowledgement in screens and dashboard widgets when last event
  is a recovery event
- added escaping '"', ''', '&', '<' and '>' characters in SOAP XML for VMware
  requests
- ensured unique value timestamps (clock, ns) from active agents and senders
- fixed removing trigger dependencies for triggers that are created from LLD
  prototypes
- fixed interfaces displaying in host inventory page
- fixed potential crash in case of failure in zbx_tls_connect() with mbed TLS
- fixed compilation warnings regarding gnutls_transport_set_ptr() with GnuTLS
- fixed certificates with empty issuer and subject fields being rejected with
  OpenSSL
- fixed daemon behavior being affected by logging level when processing TLS
  connections

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
- improved concurrent VMware item polling speed, reduced size of cached VMware
  data
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
