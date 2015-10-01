###############################################################################

# rpmbuilder:strict       true

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
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

###############################################################################

%define shortname         mongo
%define daemon            mongod
%define uid               184

###############################################################################

Name:              mongodb
Version:           2.4.9
Release:           1%{?dist}
Summary:           High-performance, schema-free document-oriented database
Group:             Applications/Databases
License:           AGPLv3 / zlib / ASL 2.0
URL:               http://www.mongodb.org

Source0:           http://fastdl.mongodb.org/src/%{name}-src-r%{version}.tar.gz
Source1:           %{name}.logrotate
Source2:           %{name}.sysconfig
Source3:           %{name}.conf
Source4:           %{name}.init

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     python-devel scons readline-devel libpcap-devel

Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(pre):     shadow-utils
Requires(postun):  initscripts

Requires:          lib%{name} = %{version}-%{release} kaosv

###############################################################################

%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. MongoDB is written in C++ and offers the following
features:
    * Collection oriented storage: easy storage of object/JSON-style data
    * Dynamic queries
    * Full index support, including on inner objects and embedded arrays
    * Query profiling
    * Replication and fail-over support
    * Efficient storage of binary data including large objects (e.g. photos
    and videos)
    * Auto-sharding for cloud-level scalability (currently in early alpha)
    * Commercial Support Available

A key goal of MongoDB is to bridge the gap between key/value stores (which are
fast and highly scalable) and traditional RDBMS systems (which are deep in
functionality).

###############################################################################

%package -n lib%{name}
Summary:           MongoDB shared libraries
Group:             Development/Libraries

%description -n lib%{name}
This package provides the shared library for the MongoDB client.

###############################################################################

%package devel
Summary:           MongoDB header files
Group:             Development/Libraries
Requires:          lib%{name} = %{version}-%{release}

%description devel
This package provides the header files, static client lib and C++ driver for 
MongoDB. MongoDB is a high-performance, open source, schema-free 
document-oriented database.

###############################################################################

%package server
Summary:           MongoDB server, sharding server and support scripts
Group:             Applications/Databases
Requires:          %{name} = %{version}-%{release}

%description server
This package provides the mongo server software, mongo sharding server
software, default configuration files, and init scripts.

###############################################################################

%prep
%setup -qn mongodb-src-r%{version}

%{__chmod} -x README
%{__sed} -i 's/\r//' README

%build
scons \
  %{?_smp_mflags} \
  --sharedclient \
  --prefix=%{_prefix} \
  --extrapath=%{_prefix} \
  --usev8 \
  --nostrip \
  --ssl \
  --full \
  --release

%install
%{__rm} -rf %{buildroot}

scons install \
  %{?_smp_mflags} \
  --sharedclient \
  --prefix=%{buildroot}%{_prefix} \
  --extrapath=%{_prefix} \
  --usev8 \
  --nostrip \
  --ssl \
  --full \
  --release

%{__rm} -f %{buildroot}%{_libdir32}/libmongoclient.a
%{__rm} -f %{buildroot}%{_libdir64}/libmongoclient.a

%{__mkdir_p} %{buildroot}%{_sharedstatedir}/%{shortname}
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{shortname}
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/%{shortname}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig

install -pDm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{daemon}
install -pDm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{daemon}
install -pDm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{daemon}.conf
install -pDm 755 %{SOURCE4} %{buildroot}%{_initddir}/%{daemon}

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__cp} -p debian/*.1 %{buildroot}%{_mandir}/man1/

%{__mkdir_p} %{buildroot}%{_rundir}/%{shortname}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%post 
%{__ldconfig}

%postun 
%{__ldconfig}

%pre server
getent group %{daemon} >/dev/null || groupadd -r %{daemon}
getent passwd %{daemon} >/dev/null || useradd -r -g %{daemon} -u %{uid} -d %{_sharedstatedir}/%{shortname} -s /sbin/nologin %{daemon}

%post server
%{__chkconfig} --add %{daemon}

%preun server
if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --del %{daemon}
fi

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/bsondump
%{_bindir}/mongo
%{_bindir}/mongodump
%{_bindir}/mongoexport
%{_bindir}/mongofiles
%{_bindir}/mongoimport
%{_bindir}/mongooplog
%{_bindir}/mongoperf
%{_bindir}/mongorestore
%{_bindir}/mongostat
%{_bindir}/mongosniff
%{_bindir}/mongotop

%{_mandir}/man1/mongo.1*
%{_mandir}/man1/mongodump.1*
%{_mandir}/man1/mongoexport.1*
%{_mandir}/man1/mongofiles.1*
%{_mandir}/man1/mongoimport.1*
%{_mandir}/man1/mongooplog.1*
%{_mandir}/man1/mongosniff.1*
%{_mandir}/man1/mongostat.1*
%{_mandir}/man1/mongorestore.1*
%{_mandir}/man1/mongoperf.1*
%{_mandir}/man1/mongotop.1*
%{_mandir}/man1/bsondump.1*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc README GNU-AGPL-3.0.txt APACHE-2.0.txt
%{_libdir32}/libmongoclient.so

%files server
%defattr(-,root,root,-)
%{_bindir}/mongod
%{_bindir}/mongos
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongos.1*
%dir %attr(0755, %{daemon}, root) %{_sharedstatedir}/%{shortname}
%dir %attr(0755, %{daemon}, root) %{_localstatedir}/log/%{shortname}
%dir %attr(0755, %{daemon}, root) %{_localstatedir}/run/%{shortname}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{daemon}
%config(noreplace) %{_sysconfdir}/%{daemon}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemon}
%{_initddir}/%{daemon}

%files devel
%defattr(-,root,root,-)
%{_includedir}

###############################################################################

%changelog
* Thu Feb 20 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4.9-1
- Rewritten init script for kaosv usage
- Rewritten config

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4.9-0
- New sharded connections to a namespace trigger setShardVersion on all shards
- Mongos cannot do slaveOk queries when primary is down
- Shell stops working after long autocomplete operation
- Passing $where predicate to db.currentOp() crashes mongod
- Logging in ~ReplicaSetMonitor() crashes
- clang compiled mongo shell crashes on exit with a stack trace in v8
- Non-numeric expiresAfterSeconds causes bad TTL query
- textIndexVersion compatibility check not complete
- Misplaced openssl callback registration can cause crashes
- $where inside of projection $elemMatch causes segmentation fault
- Slaveok versioning logic in mongos should also apply to read prefs
- Retry logic for read preferences should also apply on lazy recv() network failure
- Modifying collection options can cause restores of collection to fail
- Cannot set false setParameter options in config file
- Writeback listener may not get correct code back from ClientInfo::getLastError

* Sat Nov 02 2013 Anton Novojilov <andy@essentialkaos.com> - 2.4.8-0
- Initial build

