################################################################################

# rpmbuilder:pedantic true

################################################################################

%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

################################################################################

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

################################################################################

Summary:            A persistent key-value database
Name:               redis
Version:            5.0.5
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
Source9:            %{name}-limit-systemd
Source10:           sentinel-limit-systemd

Patch0:             %{name}-config.patch
Patch1:             sentinel-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc tcl

Requires:           %{name}-cli >= %{version}
Requires:           logrotate
%if 0%{?rhel} <= 6
Requires:           kaosv >= 2.15
%endif

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

################################################################################

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

################################################################################

%package cli

Summary:            Client for working with Redis from console
Group:              Applications/Databases

%description cli
Client for working with Redis from console

################################################################################

%prep
%setup -qn %{name}-%{version}

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

%if 0%{?rhel} <= 6
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -pm 755 %{SOURCE5} %{buildroot}%{_initrddir}/sentinel
%endif

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d
install -dm 755 %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
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

################################################################################

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

%if 0%{?rhel} <= 6
%{_initrddir}/%{name}
%{_initrddir}/sentinel
%endif

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/sentinel.service
%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%{_sysconfdir}/systemd/system/sentinel.service.d/limit.conf
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
%{_bindir}/%{name}-cli

################################################################################

%changelog
* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.5-0
- Streams: a bug in the iterator could prevent certain items to be returned in
  range queries under specific conditions.
- Memleak in bitfieldCommand fixed.
- Modules API: Preserve client->id for blocked clients.
- Fix memory leak when rewriting config file in case of write errors.
- New modules API: RedisModule_GetKeyNameFromIO().
- Fix non critical bugs in diskless replication.
- New mdouels API: command filtering. See RedisModule_RegisterCommandFilter();
- Tests improved to be more deterministic.
- Fix a Redis Cluster bug, manual failover may abort because of the master
  sending PINGs to the replicas.

* Thu May 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.4-0
- Hyperloglog different coding errors leading to potential crashes were fixed.
- A replication bug leading to a potential crash in case of plain misuse of
  handshake commands was fixed.
- XCLAIM command incrementing of number of deliveries was fixed.
- LFU field management in objects was improved.
- A potential overflow in the redis-check-aof was fixed.
- A memory leak in case of API misuse was fixed.
- ZPOP* behavior when count is 0 is fixed.
- A few redis-cli --cluster bugs were fixed, plus a few improvements.
- Many other smaller bugs.

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 5.0.3-0
- Redis no longer panics when you send data to a replica-mode connection that
  is in MONITOR or SYNC mode.
- Fixes to certain sorted set edge cases. You are unlikely to ever notice those
  issues, but now it is more correct.
- Certain BSD variants now are better supported: build & register logging
  on crash.
- The networking core now recovers if an IPv6 address is listed in bind but
  is actually not able to work because there is no such protocol in the
  system.
- redis-cli cluster mode improved in many ways. Especially the fix subcommand
  work was enhanced to cover other edge cases that were still not covered
  after the work done for Redis 5.
- MEMORY USAGE is now more accurate.
- DEBUG DIGEST-VALUE added in case you want to make sure a given set of keys
  (and not the whole DB) are excatly the same between two instances.
- Fix a potential crash in the networking code related to recent changes
  to the way the reply is consumed.
- Reject EXEC containing write commands against an instance that changed role
  from master to replica during our transaction.
- Fix a crash in KEYS and other commands using pattern matching, in an edge
  case where the pattern contains a zero byte.
- Fix eviction during AOF loading due to maxmemory triggered by commands
  executed in loading state.

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.2-0
- Release fixes two issues with Streams consumer
  groups, where items could be returned duplicated by XREADGROUP when accessing
  the history, and another bug where XREADGROUP can report some history even
  if the comsumer pending list is empty.

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.1-0
- Sentinel now supports authentication! Check the Sentinel official doc
  for more info.
- Redis-cli cluster "fix" is now able to fix a big number of clusters put
  in a bad condition. Previously many corner cases were not covered.
- Fix RESTORE mismatch reply when certain keys already expired.
- Fix an XCLAIM non trivial issue: sometimes the command returned a wrong
  entry or desynchronized the protocol.
- Stack trace generation on the Raspberry PI (and 32bit ARM) fixed.
- Don't evict expired keys when the KEYS command is called, in order to
  avoid a mass deletion event. However expired keys are not displayed
  by KEYS as usually.
- Improvements in the computation of the memory used, when estimating
  the AOF buffers.
- XRANGE COUNT of 0 fixed.
- "key misses" stats accounting fixed. Many cache misses were not counted.
- When in MULTI state, return OOM while accumulating commands and there
  is no longer memory available.
- Fix build on FreeBSD and possibly others.
- Fix a crash in Redis modules, thread safe context reply accumulation.
- Fix a race condition when producing the RDB file for full SYNC.
- Disable protected mode in Sentinel.
- More commands now have the HELP subcommand.
- Fixed an issue about adaptive server HZ timer.
- Fix cluster-replica-no-failover option name.

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- The new Stream data type. https://redis.io/topics/streams-intro
- New Redis modules APIs: Timers, Cluster and Dictionary APIs.
- RDB now store LFU and LRU information.
- The cluster manager was ported from Ruby (redis-trib.rb) to C code
  inside redis-cli. Check `redis-cli --cluster help` for more info.
- New sorted set commands: ZPOPMIN/MAX and blocking variants.
- Active defragmentation version 2.
- Improvemenets in HyperLogLog implementations.
- Better memory reporting capabilities.
- Many commands with sub-commands now have an HELP subcommand.
- Better performances when clients connect and disconnect often.
- Many bug fixes and other random improvements.
- Jemalloc was upgraded to version 5.1
- CLIENT UNBLOCK and CLIENT ID.
- The LOLWUT command was added. http://antirez.com/news/123
- We no longer use the "slave" word if not for API backward compatibility.
- Differnet optimizations in the networking layer.
- Lua improvements:
  Better propagation of Lua scripts to slaves / AOF.
  Lua scripts can now timeout and get in -BUSY state in the slave as well.
- Dynamic HZ to balance idle CPU usage with responsiveness.
- The Redis core was refactored and improved in many ways.

* Tue Aug 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.11-0
- The disconnection time between the master and slave was reset in an
  incorrect place, sometimes a good slave will not be able to failover
  because it claims it was disconnected for too much time from the master.
- A replication bug, rare to trigger but non impossible, is in Redis for
  years. It was lately discovered at Redis Labs and fixed by Oran Agra.
  It may cause disconnections, desynchronizations and other issues.
- RANDOMKEY may go in infinite loop on rare situations. Now fixed.
- EXISTS now works in a more consistent way on slaves.
- Sentinel: backport of an option to deny a potential security problem
  when the SENTINEL command is used to configure an arbitrary script
  to execute.

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.10-0
- Important security issues related to the Lua scripting engine.
- A bug with SCAN, SSCAN, HSCAN and ZSCAN, that may not return all the elements.
  We also add a regression test that can trigger the issue often when present,
  and may in theory be able to find unrelated regressions.
- A PSYNC2 bug is fixed: Redis should not expire keys when saving RDB files
  because otherwise it is no longer possible to use such RDB file as a base
  for partial resynchronization. It no longer represents the right state.
- Compatibility of AOF with RDB preamble when the RDB checksum is disabled.
- Sentinel bug that in some cases prevented Sentinel to detect that the master
  was down immediately. A delay was added to the detection.
- Other minor issues.

* Mon Jun 04 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.9-0
- When AOF is enabled with the fsync policy set to "always", we have a
  (rarely used) setup where Redis fsyncs every new write on disk. On this
  setup Redis MUST reply to the client with an OK code to the write, only
  after the write is already persisted on disk.
- Latency monitor could report wrong latencies under certain conditions.
- AOF rewriting could fail when a backgronud rewrite is triggered and
  at the same time the AOF is switched on/off.
- Redis Cluster crash-recovery safety improved
- Other smaller fixes

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.8-0
- Redis 4.0.8 fixes a single critical bug in the radix tree data structure
  used for Redis Cluster keys slot tracking.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.7-0
- Many 32 bit overflows were addressed in order to allow to use Redis with
  a very significant amount of data, memory size permitting.
- MEMORY USAGE fixed for the list type.
- Allow read-only scripts in Redis Cluster.
- Fix AOF pipes setup in edge case.
- AUTH option for MIGRATE.
- HyperLogLogs are no longer converted from sparse to dense in order
  to be merged.
- Fix AOF rewrite dead loop under edge cases.
- Fix processing of large bulk strings
- Added RM_UnlinkKey in modules API.
- Fix Redis Cluster crashes when certain commands with a variable number
  of arguments are called in an improper way.
- Fix memory leak in lazyfree engine.
- Fix many potentially successful partial synchronizations that end
  doing a full SYNC, because of a bug destroying the replication
  backlog on the slave. So after a failover the slave was often not able
  to PSYNC with masters, and a full SYNC was triggered. The bug only
  happened after 1 hour of uptime so escaped the unit tests.
- Improve anti-affinity in master/slave allocation for Redis Cluster
  when the cluster is created.
- Improve output buffer handling for slaves, by not limiting the amount
  of writes a slave could receive.

* Fri Dec 08 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.6-0
- More errors in the fixes for PSYNC2 in Redis 4.0.5 were identified

* Sat Dec 02 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.5-0
- Redis 4.0.4 fix for PSYNC2 was broken, causing the slave to crash when
  receiving an RDB file from the master that contained a duplicated Lua script

* Fri Dec 01 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.4-0
- Several PSYNC2 bugs can corrupt the slave data set after a restart and
  a successful PSYNC2 handshake

* Thu Nov 30 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.3-0
- Several PSYNC2 bugs can corrupt the slave data set after a restart and
  a successful PSYNC2 handshake

* Thu Oct 26 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 4.0.2-0
- A number of bugs were fixed in the area of PSYNC2 replication in the
  specific area of restarting an instance with an RDB file having the
  repliacation meta-data to continue without a full resynchronization. The
  old code allowed several inconsistencies under certain conditions, like
  starting a master with an RDB file generated by a slave, and later using
  such master to connect previous slaves having the same replication history.
  Because of other bugs, sometimes the replication resulted in a full
  synchronization even if actually a partial resynchronization was possible
  and so forth. Several commits by different authors fix different bugs here.
- AOF flush on SHUTDOWN did not cared to really write the AOF buffers
  (not in the kernel but in the Redis process memory) to disk before exiting.
  Calling SHUTDOWN during traffic resulted into not every operation to be
  persisted on disk.
- The SLOWLOG could reference values inside string objects stored at keys,
  creating a race condition during FLUSHALL ASYNC while the DB is reclaimed
  in another thread.

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
