###############################################################################

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

###############################################################################

Summary:            Statistics collection daemon for filling RRD files
Name:               collectd
Version:            5.4.1
Release:            0%{?dist}
License:            GPLv2
Group:              System Environment/Daemons
URL:                http://collectd.org/

Source0:            http://collectd.org/files/%{name}-%{version}.tar.bz2
Source1:            %{name}-collection3.conf

BuildArch:          x86_64 i386
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      iptables-devel kernel-headers kernel-devel libgcrypt-devel
BuildRequires:      libxml2-devel perl perl-ExtUtils-MakeMaker perl-ExtUtils-Embed
BuildRequires:      libcurl-devel libpcap-devel

Requires(pre):      shadow-utils

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
collectd is a small daemon written in C for performance.  It reads various
system  statistics  and updates  RRD files,  creating  them if necessary.
Since the daemon doesn't need to startup every time it wants to update the
files it's very fast and easy on the system. Also, the statistics are very
fine grained since the files are updated every 10 seconds.

###############################################################################

%package devel
Summary:            Header files and libraries for building collectd clients
Group:              Development/Languages

Requires:           %{name} = %{version}

%description devel
Header files and libraries for building collectd clients.

###############################################################################

%package dbi
Summary:            DBI module for collectd
Group:              System Environment/Daemons

BuildRequires:      libdbi-devel

Requires:           %{name} = %{version}

%description dbi
This plugin for collectd provides DBI support.

###############################################################################

%package ipmi
Summary:            IPMI module for collectd
Group:              System Environment/Daemons

BuildRequires:      OpenIPMI-devel

Requires:           %{name} = %{version}

%description ipmi
This plugin for collectd provides IPMI support.

###############################################################################

%package libvirt
Summary:            Libvirt module for collectd
Group:              System Environment/Daemons

BuildRequires:      libvirt-devel

Requires:           %{name} = %{version}

%description libvirt
This plugin for collectd provides libvirt support.

###############################################################################

%package memcachec
Summary:            Memcache module for collectd
Group:              System Environment/Daemons

BuildRequires:      libmemcached-devel

Requires:           %{name} = %{version}

%description memcachec
This plugin for collectd provides Memcache support.

###############################################################################

%package mysql
Summary:            MySQL module for collectd
Group:              System Environment/Daemons

BuildRequires:      mysql-devel

Requires:           %{name} = %{version}

%description mysql
This plugin for collectd provides MySQL support.

###############################################################################

%package notify_email
Summary:            Email notification module for collectd
Group:              System Environment/Daemons

BuildRequires:      libesmtp-devel

Requires:           %{name} = %{version}

%description notify_email
This plugin for collectd provides email notification support.

###############################################################################

%package -n perl-Collectd
Summary:            Perl bindings for collectd
Group:              System Environment/Daemons

Requires:           %{name} = %{version}
Requires:           perl

%description -n perl-Collectd
This package contains Perl bindings and plugin for collectd.

###############################################################################

%package ping
Summary:            Ping module for collectd
Group:              System Environment/Daemons

BuildRequires:      liboping-devel

Requires:           %{name} = %{version}

%description ping
This plugin for collectd provides network latency statistics.

###############################################################################

%package postgresql
Summary:            PostgreSQL module for collectd
Group:              System Environment/Daemons

BuildRequires:      postgresql-devel

Requires:           %{name} = %{version}

%description postgresql
PostgreSQL querying plugin. This plugins provides data of issued commands,
called handlers and database traffic.

###############################################################################

%package rrdtool
Summary:            RRDTool module for collectd
Group:              System Environment/Daemons

BuildRequires:      rrdtool-devel

Requires:           %{name} = %{version}
Requires:           rrdtool

%description rrdtool
This plugin for collectd provides rrdtool support.

###############################################################################

%package sensors
Summary:            Libsensors module for collectd
Group:              System Environment/Daemons

BuildRequires:      lm_sensors-devel

Requires:           %{name} = %{version}
Requires:           lm_sensors

%description sensors
This plugin for collectd provides querying of sensors supported by
lm_sensors.

###############################################################################

%package snmp
Summary:            SNMP module for collectd
Group:              System Environment/Daemons

BuildRequires:      net-snmp-devel

Requires:           %{name} = %{version}
Requires:           net-snmp

%description snmp
This plugin for collectd provides querying of net-snmp.

###############################################################################

%package varnish
Summary:            Varnish module for collectd
Group:              System Environment/Daemons

BuildRequires:      varnish-libs-devel

Requires:           %{name} = %{version}

%description varnish
This plugin for collectd provides varnish support.

###############################################################################

%package web
Summary:            Contrib web interface to viewing rrd files
Group:              System Environment/Daemons

BuildArch:          noarch

Requires:           %{name} = %{version}
Requires:           %{name}-rrdtool = %{version}
Requires:           perl-Config-General perl-Regexp-Common
Requires:           perl-HTML-Entities-Numbered rrdtool-perl

%description web
This package will allow for a simple web interface to view rrd files created
by collectd.

###############################################################################

%prep
%setup -q

%build
export CFLAGS="%{optflags} -DLT_LAZY_OR_NOW='RTLD_LAZY|RTLD_GLOBAL'"
%{configure} \
  --with-libiptc \
  --with-perl-bindings=INSTALLDIRS=vendor \
  --with-python=/usr/bin/python2.6 \
  --disable-static \
  --disable-ascent \
  --disable-apple_sensors \
  --disable-gmond \
  --disable-lpar \
  --disable-modbus \
  --disable-netapp \
  --disable-netlink \
  --disable-notify_desktop \
  --disable-nut \
  --disable-onewire \
  --disable-oracle \
  --disable-pinba \
  --disable-routeros \
  --disable-rrdcached \
  --disable-tape \
  --disable-tokyotyrant \
  --disable-xmms \
  --disable-zfs_arc \
  --enable-apache \
  --enable-apcups \
  --enable-battery \
  --enable-bind \
  --enable-conntrack \
  --enable-contextswitch \
  --enable-cpu \
  --enable-cpufreq \
  --enable-csv \
  --enable-curl \
  --enable-curl_json \
  --enable-curl_xml \
  --enable-dbi  \
  --enable-df \
  --enable-disk \
  --enable-dns \
  --enable-email \
  --enable-entropy \
  --enable-ethstat \
  --enable-exec \
  --enable-filecount \
  --enable-fscache \
  --enable-hddtemp \
  --enable-interface \
  --enable-iptables \
  --enable-ipvs \
  --enable-irq \
  --enable-ipmi \
  --enable-libvirt \
  --enable-load \
  --enable-logfile \
  --enable-madwifi \
  --enable-match_empty_counter \
  --enable-match_hashed \
  --enable-match_regex \
  --enable-match_timediff \
  --enable-match_value \
  --enable-mbmon \
  --enable-md \
  --enable-memcachec \
  --enable-memcached \
  --enable-memory \
  --enable-multimeter \
  --enable-mysql \
  --enable-network \
  --enable-nfs \
  --enable-nginx \
  --enable-notify_email \
  --enable-ntpd \
  --enable-numa \
  --enable-olsrd \
  --enable-openvpn \
  --enable-perl \
  --enable-ping \
  --enable-postgresql \
  --enable-powerdns \
  --enable-processes \
  --enable-protocols \
  --enable-python \
  --enable-rrdtool \
  --enable-sensors \
  --enable-serial \
  --enable-snmp \
  --enable-swap \
  --enable-syslog \
  --enable-table \
  --enable-tail \
  --enable-target_notification \
  --enable-target_replace \
  --enable-target_scale \
  --enable-target_set \
  --enable-tcpconns \
  --enable-teamspeak2 \
  --enable-ted \
  --enable-thermal \
  --enable-unixsock \
  --enable-uptime \
  --enable-users \
  --enable-uuid \
  --enable-varnish \
  --enable-vmem \
  --enable-vserver \
  --enable-wireless \
  --enable-write_graphite \
  --enable-write_http

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__rm} -rf contrib/SpamAssassin

%{make_install}

%{__chmod} 644 %{buildroot}%{_sysconfdir}/%{name}.conf

%{__sed} -i \
  -e 's|^#BaseDir.*|BaseDir     "/var/lib/%{name}"|g' \
  -e 's|^#PIDFile.*|PIDFile     "/var/run/%{name}.pid"|g' \
  %{buildroot}%{_sysconfdir}/%{name}.conf

echo -e "jmx_memory\t\tvalue:GAUGE:0:U" >> %{buildroot}/%{_datadir}/%{name}/types.db

install -Dmp 755 contrib/fedora/init.d-%{name} %{buildroot}%{_initrddir}/%{name}

install -dm 755 %{buildroot}%{plugindir}/python
install -dm 755 %{buildroot}%{_localstatedir}/lib/%{name}/
install -dm 755 %{buildroot}%{_datadir}/%{name}/collection3/

install -dm 755 %{buildroot}%{perl_vendorlib}
%{__mv} %{buildroot}/usr/lib/perl5/* %{buildroot}%{perl_vendorlib}/
%{__rm} -rf %{buildroot}%{_libdir}/perl5
%{__mv} %{buildroot}/usr/man/man3 %{buildroot}%{_mandir}/
%{__rm} -rf %{buildroot}/usr/man

find %{buildroot} -name .packlist -exec rm {} \;
find %{buildroot} -name perllocal.pod -exec rm {} \;
%{__rm} -f %{buildroot}%{_libdir}/{%{name}/,}*.la
%{__rm} %{buildroot}%{_datadir}/%{name}/postgresql_default.conf

%{__mkdir} apache-config
install -Dmp 644 %{SOURCE1} apache-config
%{__cp} -ad contrib/collection3/* %{buildroot}%{_datadir}/%{name}/collection3/
%{__chmod} +x %{buildroot}%{_datadir}/%{name}/collection3/bin/*.cgi
%{__rm} -f %{buildroot}%{_datadir}/%{name}/collection3/{bin,etc,lib,share}/.htaccess

%{__mkdir} perl-examples
find contrib -name '*.p[lm]' -exec mv {} perl-examples/ \;

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}
%{__chkconfig} --add %{name}

%preun
if [[ $1 = 0 ]]; then
  %{__service} %{name} stop >/dev/null 2>&1
  %{__chkconfig} --del %{name}
fi

%postun
%{__ldconfig}
if [[ $1 -ge 1 ]]; then
  %{__service} %{name} condrestart > /dev/null 2>&1 || :
fi

###############################################################################

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING INSTALL README
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_initrddir}/%{name}
%{_sbindir}/*
%{_bindir}/*
%dir %{_localstatedir}/lib/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/python
%{_libdir}/%{name}/*.so
%exclude %{plugindir}/dbi.so
%exclude %{plugindir}/ipmi.so
%exclude %{plugindir}/libvirt.so
%exclude %{plugindir}/memcachec.so
%exclude %{plugindir}/mysql.so
%exclude %{plugindir}/notify_email.so
%exclude %{plugindir}/perl.so
%exclude %{plugindir}/ping.so
%exclude %{plugindir}/postgresql.so
%exclude %{plugindir}/redis.so
%exclude %{plugindir}/rrdtool.so
%exclude %{plugindir}/sensors.so
%exclude %{plugindir}/snmp.so
%exclude %{plugindir}/varnish.so
%exclude %{plugindir}/write_redis.so
%{_datadir}/%{name}/types.db
%{_libdir}/*.so.*
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{name}-nagios.1*
%doc %{_mandir}/man1/%{name}-tg.1*
%doc %{_mandir}/man1/%{name}ctl.1*
%doc %{_mandir}/man1/%{name}mon.1*
%doc %{_mandir}/man5/%{name}.conf.5*
%doc %{_mandir}/man5/%{name}-email.5*
%doc %{_mandir}/man5/%{name}-exec.5*
%doc %{_mandir}/man5/%{name}-python.5*
%doc %{_mandir}/man5/%{name}-threshold.5*
%doc %{_mandir}/man5/%{name}-unixsock.5*
%doc %{_mandir}/man5/types.db.5*

%files dbi
%defattr(-, root, root, -)
%{plugindir}/dbi.so

%files devel
%defattr(-, root, root, -)
%{_includedir}/%{name}
%{_libdir}/libcollectdclient.so
%{_libdir}/pkgconfig/*.pc

%files ipmi
%defattr(-, root, root, -)
%{plugindir}/ipmi.so

%files libvirt
%defattr(-, root, root, -)
%{plugindir}/libvirt.so

%files memcachec
%defattr(-, root, root, -)
%{plugindir}/memcachec.so

%files mysql
%defattr(-, root, root, -)
%{plugindir}/mysql.so

%files notify_email
%defattr(-, root, root, -)
%{plugindir}/notify_email.so

%files -n perl-Collectd
%defattr(-, root, root, -)
%doc perl-examples
%{plugindir}/perl.so
%{perl_vendorlib}/Collectd.pm
%{perl_vendorlib}/Collectd/
%doc %{_mandir}/man5/%{name}-perl.5*
%doc %{_mandir}/man3/Collectd::Unixsock.3pm*

%files ping
%defattr(-, root, root, -)
%{plugindir}/ping.so

%files postgresql
%defattr(-, root, root, -)
%{plugindir}/postgresql.so
%doc src/postgresql_default.conf

%files rrdtool
%defattr(-, root, root, -)
%{plugindir}/rrdtool.so

%files sensors
%defattr(-, root, root, -)
%{plugindir}/sensors.so

%files snmp
%defattr(-, root, root, -)
%{plugindir}/snmp.so
%doc %{_mandir}/man5/%{name}-snmp.5*

%files varnish
%defattr(-, root, root, -)
%{plugindir}/varnish.so

%files web
%defattr(-, root, root, -)
%doc apache-config
%{_datadir}/%{name}/collection3/

###############################################################################

%changelog
* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 5.4.1-0
- Initial build