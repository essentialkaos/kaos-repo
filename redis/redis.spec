###############################################################################

# rpmbuilder:pedantic true 

###############################################################################

%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

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
%define __sysctl          %{_bindir}/systemctl

###############################################################################

Summary:            A persistent key-value database
Name:               redis
Version:            4.0.1
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
Source7:            %{name}.service
Source8:            sentinel.service

Patch0:             %{name}-config.patch
Patch1:             sentinel-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc tcl

Requires:           %{name}-cli >= %{version}
Requires:           logrotate kaosv >= 2.10

%if 0%{?rhel} >= 7
Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%else
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts
%endif

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

%build
%ifarch %ix86
sed -i '/integration\/logging/d' tests/test_helper.tcl
%{__make} %{?_smp_mflags} 32bit MALLOC=jemalloc
%else
%{__make} %{?_smp_mflags} MALLOC=jemalloc
%endif

%install
rm -rf %{buildroot}

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

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
%endif

chmod 755 %{buildroot}%{_bindir}/%{name}-*

rm -f %{buildroot}%{_bindir}/%{name}-sentinel

install -dm 755 %{buildroot}%{_sbindir}

ln -sf %{_bindir}/%{name}-server %{buildroot}%{_bindir}/%{name}-sentinel
ln -sf %{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%check
%if 0%{?with_tests}
%{__make} %{?_smp_mflags} test
%{__make} %{?_smp_mflags} test-sentinel
%endif

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
        -c 'Redis Server' %{name} &> /dev/null

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

chown %{name}:%{name} %{_sysconfdir}/%{name}.conf
chown %{name}:%{name} %{_sysconfdir}/sentinel.conf

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} --no-reload disable sentinel.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
  %{__sysctl} stop sentinel.service &>/dev/null || :
%else
  %{__service} %{name} stop &> /dev/null || :
  %{__service} sentinel stop &> /dev/null || :
  %{__chkconfig} --del %{name} &> /dev/null || :
  %{__chkconfig} --del sentinel &> /dev/null || :
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

%clean
rm -rf %{buildroot}

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

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/sentinel.service
%endif

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
* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Loading two or more modules exporting native data types resulted into the
  inability to reload the RDB file.
- Crash in modules when calling from Lua scripts module commands that would
  block.
- A Redis Cluster crash due to mis-handling of the "migrate-to" internal
  flag.
- Other smaller fixes not worth of a release per se, but nice to add here.

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Different replication fixes to PSYNC2, the new 4.0 replication engine.
- Modules thread safe contexts were introduced. They are an experimental API
  right now, but the API is considered to be stable and usable when needed.
- SLOWLOG now logs the offending client name and address. Note that this is
  a backward compatibility breakage in case old code assumes that the slowlog
  entry is composed of exactly three entries.
- The modules native data types RDB format changed.
- The AOF check utility is now able to deal with RDB preambles.
- GEORADIUS_RO and GEORADIUSBYMEMBER_RO variants, not supporting the STORE
  option, were added in order to allow read-only scaling of such queries.
- HSET is now variadic, and HMSET is considered deprecated (but will be
  supported for years to come). Please use HSET in new code.
- GEORADIUS huge radius (>= ~6000 km) corner cases fixed, certain elements
  near the edges were not returned.
- DEBUG DIGEST modules API added.
- HyperLogLog commands no longer crash on certain input (non HLL) strings.
- Fixed SLAVEOF inside MULTI/EXEC blocks.
- Many other minor bug fixes and improvements.

* Thu May 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.9-0
- This release just fixes bugs that are unlikely to cause serious problems

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.8-0
- Apparently Jemalloc 4.4.0 may contain a deadlock under particular
  conditions. We reverted back to the previously used Jemalloc
  versions and plan to upgrade Jemalloc again after having more
  info about the cause of the bug.
- MIGRATE could crash the server after a socket error.

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.7-0
- MIGRATE could incorrectly move keys between Redis Cluster nodes by turning
  keys with an expire set into persisting keys. This bug was introduced with
  the multiple-keys migration recently. It is now fixed. Only applies to
  Redis Cluster users that use the resharding features of Redis Cluster.
- As Redis 4.0 beta and the unstable branch already did (for some months at
  this point), Redis 3.2.7 also aliases the Host: and POST commands to QUIT
  avoiding to process the remaining pipeline if there are pending commands.
  This is a security protection against a "Cross Scripting" attack, that
  usually involves trying to feed Redis with HTTP in order to execute commands.
  Example: a developer is running a local copy of Redis for development
  purposes. She also runs a web browser in the same computer. The web browser
  could send an HTTP request to http://127.0.0.1:6379 in order to access the
  Redis instance, since a specially crafted HTTP requesta may also be partially
  valid Redis protocol. However if POST and Host: break the connection, this
  problem should be avoided. IMPORTANT: It is important to realize that it
  is not impossible that another way will be found to talk with a localhost
  Redis using a Cross Protocol attack not involving sending POST or Host: so
  this is only a layer of protection but not a definitive fix for this class
  of issues.
- A ziplist bug that could cause data corruption, could crash the server and
  MAY ALSO HAVE SECURITY IMPLICATIONS was fixed. The bug looks complex to
  exploit, but attacks always get worse, never better (cit). The bug is very
  very hard to catch in practice, it required manual analysis of the ziplist
  code in order to be found. However it is also possible that rarely it
  happened in the wild. Upgrading is required if you use LINSERT and other
  in-the-middle list manipulation commands.
- We upgraded to Jemalloc 4.4.0 since the version we used to ship with Redis
  was an early 4.0 release of Jemalloc. This version may have several
  improvements including the ability to better reclaim/use the memory of
  system.

* Wed Dec 07 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.6-0
- A bug with BITFIELD that may cause the bitmap corruption when setting offsets
  larger than the current string size.
- A GEORADIUS bug that may happen when using very large radius lengths, in
  the range of 10000km or alike, due to wrong bounding box calculation.
- A bug with Redis Cluster which crashes when reading a nodes configuration
  file with zero bytes at the end, which sometimes happens with certain ext4
  configurations after a system crash.

* Fri Nov 18 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.5-1
- Using bundled jemalloc

* Thu Oct 27 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.5-0
- This release only fixes a compilation issue due to the missing -ldl
  at linking time

* Mon Oct 03 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- Security: CONFIG SET client-output-buffer-limit overflow fixed
- TCP binding bug fixed when only certain addresses were available for
  a given port
- A much better crash report that includes part of the Redis binary:
  this will allow to fix bugs even when we just have a crash log and
  no other help from the original poster oft the issue
- A fix for Redis Cluster redis-trib displaying of info after creating
  a new cluster

* Tue Aug 02 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- Fix a bug to delay bgsave while AOF rewrite in progress for replication
- Update linenoise to fix insecure redis-cli history file creation

* Tue Aug 02 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Ability of slave to announce arbitrary ip/port to master
- redis-benchmark: new option to show server errors on stdout
- Multiple GEORADIUS bugs fixed
- Replication: when possible start RDB saving ASAP
- Sentinel: new test unit 07 that tests master down conditions
- Sentinel: check Slave INFO state more often when disconnected
- Avoid simultaneous RDB and AOF child process
- Replication: start BGSAVE for replication always in replicationCron()
- Regression test for issue #3333
- getLongLongFromObject: use string2ll() instead of strict_strtoll()
- redis-cli: check SELECT reply type just in state updated
- Fix for redis_cli printing default DB when select command fails
- Sentinel: fix cross-master Sentinel address update
- CONFIG GET is now no longer case sensitive
- Fix test for new RDB checksum failure message
- Make tcp-keepalive default to 300 in internal conf
- In Redis RDB check: more details in error reportings
- In Redis RDB check: log decompression errors
- In Redis RDB check: log object type on error
- Added a trivial program to randomly corrupt RDB files in /utils
- In Redis RDB check: minor output message changes
- In Redis RDB check: better error reporting
- In Redis RDB check: initial POC
- A string with 21 chars is not representable as a 64-bit integer
- Test: new randomized stress tester for #3343 alike bugs
- Stress tester WIP
- Regression test for issue #3343 exact min crash sequence
- Fix quicklistReplaceAtIndex() by updating the quicklist ziplist size

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
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

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- There is a new very powerful BITFIELD command.
- CONFIG GET is allowed during the loading of the dataset.
- The DEBUG command have new features and can show an help with DEBUG HELP.
- redis-cli show hits about the commands arguments to the right.
- GEORADIUS got a STORE / STOREDIST option to store the result into a target
  key (as as orted set) instead of reporting it to the user.
- Redis Cluster replicas migration now works in a slightly different way. In
  the past a slave could migrate only to a master that used to have slaves
  in the past (and if there was still trace of this information). Now instead
  if a new slave gets at least a slot, and at least one other master in the
  cluster has a slave, then the new master is considered a valid target for
  replica migration. So if it will be orphaned and there is a spare slave
  it will get one.
- CLUSTER SLOTS output now includes the node ID (in a backward compatible
  manner).

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
