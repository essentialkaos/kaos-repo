###############################################################################

# rpmbuilder:pedantic true 

###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

Summary:            A persistent key-value database
Name:               redis
Version:            3.2.0
Release:            0%{?dist}
License:            BSD
Group:              Applications/Databases
URL:                http://redis.io

Source0:            https://github.com/antirez/%{name}/archive/%{version}.tar.gz
Source1:            %{name}.logrotate
Source2:            %{name}.init
Source3:            %{name}.sysconfig
Source4:            sentinel.logrotate
Source5:            sentinel.init
Source6:            sentinel.sysconfig

Patch0:             %{name}-linenoise-file-access.patch
Patch1:             %{name}-config.patch
Patch2:             sentinel-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc jemalloc-devel

Requires:           %{name}-cli >= %{version}
Requires:           logrotate kaosv >= 2.5

Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts

###############################################################################

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

###############################################################################

%package cli

Summary:            Client for working with Redis from console

%description cli
Client for working with Redis from console

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/sentinel
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/sentinel

install -pm 640 %{name}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}

install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -pm 755 %{SOURCE5} %{buildroot}%{_initrddir}/sentinel

chmod 755 %{buildroot}%{_bindir}/%{name}-*

rm -f %{buildroot}%{_bindir}/%{name}-sentinel

install -dm 755 %{buildroot}%{_sbindir}

ln -sf %{_bindir}/%{name}-server %{buildroot}%{_bindir}/%{name}-sentinel
ln -sf %{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
        -c 'Redis Server' %{name} &> /dev/null

%post
%{__chkconfig} --add %{name}

chown %{name}:%{name} %{_sysconfdir}/%{name}.conf
chown %{name}:%{name} %{_sysconfdir}/sentinel.conf

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop &> /dev/null || :
fi

%postun
if [[ $1 -eq 0 ]] ; then
  %{__chkconfig} --del %{name} &> /dev/null || :
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/sentinel
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/sentinel
%config(noreplace) %{_sysconfdir}/*.conf
%dir %attr(0755, %{name}, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}
%{_initrddir}/%{name}
%{_initrddir}/sentinel
%{_bindir}/%{name}-server
%{_bindir}/%{name}-sentinel
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-rdb
%{_sbindir}/%{name}-server


%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README.md
%{_bindir}/redis-cli

###############################################################################

%changelog
* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- A critical bug in Sentinel was hopefully fixed. During the big 3.2
  refactoring of Redis Sentinel, in order to implement connection sharing
  to make Sentinel able to scale better (few Sentinels to monitor many
  masters), a bug was introduced that mis-counted the number of pending
  commands in the Redis link. This in turn resulted into an inability to talk
  with certain Redis instances. A common result of this bug was the inability
  of Redis Sentinel to reconfigure back the old master, after a failover,
  when it is reachable again, as the slave of the new master. This was due
  to the inability to talk with the old master at all.
- BITFIELD bugs fixed.
- GEO commands fixes on syntax errors and edge cases.
- RESTORE now accepts dumps generated by older Redis versions.
- Jemalloc now is really configured to save you memory, for a problem a
  change in the jemalloc configuration did not really survived when the
  3.2.0 release was finalized.
- TTL and TYPE command no longer alter the last access time of a key, for
  LRU evictions purposes. A new TOUCH command was introduced *just* to
  update the access time of a key.
- A bug was fixed in redis-cli, that connected to the instance running on the
  port 6379 if there was one, regardless of what was specified.
- TCP keep alive is now enabled by default. This should fix most ghost
  connections problems without resulting in any practical change in otherwise
  sane deployments.
- A Sentinel crash that could happen during failovers was fixed.

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.7-0
- [FIX] avg_ttl reporting in INFO improved. (Salvatore Sanfilippo)
- [FIX] Redis Cluster address update (via gossip section) processing improved
        to avoid initiating inwanted handshakes.
- [FIX] Many fixes to MIGRATE multiple keys implementation. The command
        could handle errors in a faulty way leading to crashes or other
        unexpected behaviors. MIGRATE command refactoring.
        (The analysis of the faulty conditions was conducted by
         Kevin McGehee. The fix was developed by Salvatore Sanfilippo)
- [FIX] A Redis Cluster node crash was fixed because of wrong handling of
        node->slaveof pointers.
        (Reported by JackyWoo, fixed by Salvatore Sanfilippo)
- [FIX] Fix redis-trib rebalance when nodes need to be left empty because
        the specified weight is zero.
        (Reported by Shahar Mor, fixed by Salvatore Sanfilippo)
- [FIX] MIGRATE: Never send -ASK redirections for MIGRATE when there are
        open slots. Redis-trib and other cluster management utility must
        always be free to move keys between nodes about open slots, in order
        to reshard, fix the cluster configuration, and so forth.
        (Salvatore Sanfilippo)
- [FIX] Redis-trib is now able to fix more errors. A new CLUSTER subcommand
        called BUMPEPOCH was introduced in order to support new modes
        for the "fix" subcommand. (Salvatore Sanfilippo)
- [NEW] Cluster/Sentinel tests now use OSX leak to perform leak detection
        at the end of every unit. (Salvatore Sanfilippo)
- [NEW] Detect and show server crashes during Cluster/Sentinel tests.
        (Salvatore Sanfilippo)
- [NEW] More reliable Cluster/Sentinel test becuase of timing errors and
        -LOADING errors. (Salvatore Sanfilippo)

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.6-0
- [FIX] lua_struct.c/getnum security issue fixed. (Luca Bruno discovered it,
        patched by Sun He and Chris Lamb)
- [FIX] Redis Cluster replica migration fixed. See issue 2924 for details.
        (Salvatore Sanfilippo)
- [FIX] Fix a race condition in processCommand() because of interactions
        with freeMemoryIfNeeded(). Details in issue 2948 and especially
        in the commit message d999f5a. (Race found analytically by
        Oran Agra, patch by Salvatore Sanfilippo)

- [NEW] Backported from the upcoming Redis 3.2:
        MIGRATE now supports an extended multiple-keys pipelined mode, which
        is an order of magnitude faster. Redis Cluster now uses this mode
        in order to perform reshardings and rebalancings. (Salvatore Sanfilippo)
- [NEW] Backported from the upcoming Redis 3.2:
        Redis Cluster has now support for rebalancing via the redis-trib
        rebalance command. Demo here:
        https://asciinema.org/a/0tw2e5740kouda0yhkqrm5790
        Official documentation will be available ASAP. (Salvatore Sanfilippo)
- [NEW] Redis Cluster redis-trib.rb new "info" subcommand.
- [NEW] Redis Cluster tests improved. (Salvatore Sanfilippo)
- [NEW] Log offending memory access address on SIGSEGV/SIGBUS

* Sat Oct 24 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- [FIX] MOVE now moves the TTL as well. A bug lasting forever... finally
        fixed thanks to Andy Grunwald that reported it.
        (reported by Andy Grunwald, fixed by Salvatore Sanfilippo)
- [FIX] Fix a false positive in HSTRLEN test.
- [FIX] Fix a bug in redis-cli --pipe mode that was not able to read back
        replies from the server incrementally. Now a mass import will use
        a lot less memory, and you can use --pipe to do incremental streaming.
        (reported by Twitter user @fsaintjacques, fixed by Salvatore
        Sanfilippo)
- [FIX] Slave detection of master timeout. (fixed by Kevin McGehee, refactoring
        and regression test by Salvatore Sanfilippo)
- [NEW] Cluster: redis-trib fix can fix an additional case for opens lots.
        (Salvatore Sanfilippo)
- [NEW] Cluster: redis-trib import support for --copy and --replace options
        (David Thomson)

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.4-0
- [FIX] A number of bugs related to replication PSYNC and the (yet experimental)
        diskless replication feature were fixed. The bugs could lead to
        inconsistency between masters and slaves. (Salvatore Sanfilippo, Oran
        Agra fixed the issue found by Yuval Inbar)
- [FIX] A replication bug in the context of PSYNC partial resynchonization was
        found and fixed. This bug happens even when diskless replication is off
        in the case different slaves connect at different times while the master
        is creating an RDB file, and later a partial resynchronization is
        attempted by a slave that connected not as the first one. (Salvatore
        Sanfilippo, Oran Agra)
- [FIX] Chained replication and PSYNC interactions leading to potential stale
        chained slaves data set, see issue #2694. (Salvatore Sanfilippo fixed
        an issue reported by "GeorgeBJ" user at Github)
- [FIX] redis-cli --scan iteration fixed when returned cursor overflows
        32 bit signed integer. (Ofir Luzon, Yuval Inbar)
- [FIX] Sentinel: fixed a bug during the master switch process, where for a
        failed conditional check, the new configuration is rewritten, during
        a small window of time, in a corrupted way where the master is
        also reported to be one of the slaves. This bug is rare to trigger
        but apparently it happens in the wild, and the effect is to see
        a replication loop where the master will try to replicate with itself.
        The bug was found by Jan-Erik Rediger using a static analyzer and
        fixed by Salvatore Sanfilippo.
- [FIX] Sentinel lack of arity checks for certain commands.
        (Rogerio Goncalves, Salvatore Sanfilippo)
- [NEW] Replication internals rewritten in order to be more resistant to bugs.
        The replication handshake in the slave side was rewritten as a non
        blocking state machine. (Salvatore Sanfilippo, Oran Agra)
- [NEW] New "replication capabilities" feature introduced in order to signal
        from the master to the slave what are the features supported, so that
        the master can choose the kind of replication to start (diskless or
        not) when master and slave are of different versions. (Oran Agra,
        Salvatore Sanfilippo)
- [NEW] Log clients details when SLAVEOF command is received. (Salvatore
        Sanfilippo with inputs from Nick Craver and Marc Gravell). 

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- [FIX] Fix blocking operations timeout precision when HZ is at its default
        value (not increased) and there are thousands of clients connected
        at the same time. This bug affected Sidekiq users that experienced
        a very long delay for BLPOP and similar commands to return for
        timeout. Check commit b029ff1 for more info. (Salvatore Sanfilippo)
- [FIX] MIGRATE "creating socket: Invalid argument" error fix. Check
        issues #2609 and #2612 for more info. (Salvatore Sanfilippo)
- [FIX] Be able to connect to the master even when the slave is bound to
        just the loopback interface and has no valid public address in the
        network the master is reacahble. (Salvatore Sanfilippo)
- [FIX] ZADD with options encoding promotion fixed. (linfangrong)
- [FIX] Reset aof_delayed_fsync on CONFIG RESETSTATS. (Tom Kiemes)
- [FIX] PFCOUNT key parsing in cluster fixed. (MOON_CLJ)
- [FIX] Fix Solaris compilation of Redis 3.0. (Jan-Erik Rediger)

* Thu Jun 04 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- [FIX] Critical security issue fix by Ben Murphy: http://t.co/LpGTyZmfS7
- [FIX] SMOVE reply fixed when src and dst keys are the same. (Glenn Nethercutt)
- [FIX] Lua cmsgpack lib updated to support str8 type. (Sebastian Waisbrot)
- [NEW] ZADD support for options: NX, XX, CH. See new doc at redis.io.
        (Salvatore Sanfilippo)
- [NEW] Senitnel: CKQUORUM and FLUSHCONFIG commands back ported.
        (Salvatore Sanfilippo)

* Tue May 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- [FIX] Sentinel memory leak due to hiredis fixed. (Salvatore Sanfilippo)
- [FIX] Sentinel memory leak on duplicated instance. (Charsyam)
- [FIX] Redis crash on Lua reaching output buffer limits. (Yossi Gottlieb)
- [FIX] Sentinel flushes config on +slave events. (Bill Anderson)

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- Redis Cluster: a distributed implementation of a subset of Redis.
- New "embedded string" object encoding resulting in less cache
  misses. Big speed gain under certain work loads.
- AOF child -> parent final data transmission to minimize latency due
  to "last write" during AOF rewrites.
- Much improved LRU approximation algorithm for keys eviction.
- WAIT command to block waiting for a write to be transmitted to
  the specified number of slaves.
- MIGRATE connection caching. Much faster keys migraitons.
- MIGARTE new options COPY and REPLACE.
- CLIENT PAUSE command: stop processing client requests for a
  specified amount of time.
- BITCOUNT performance improvements.
- CONFIG SET accepts memory values in different units (for example
  you can use "CONFIG SET maxmemory 1gb").
- Redis log format slightly changed reporting in each line the role of the
  instance (master/slave) or if it's a saving child log.
- INCR performance improvements.
