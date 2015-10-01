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
Version:            3.0.4
Release:            0%{?dist}
License:            BSD
Group:              Applications/Databases
URL:                http://redis.io

Source0:            https://github.com/antirez/%{name}/archive/%{version}.tar.gz
Source1:            %{name}.logrotate
Source2:            %{name}.init
Source3:            %{name}.sysconfig

Patch0:             %{name}-config.patch
Patch1:             %{name}-linenoise-file-access.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc jemalloc-devel

Requires:           %{name}-cli >= %{version}
Requires:           logrotate kaosv >= 2.0

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

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -pm 640 %{name}.conf %{buildroot}%{_sysconfdir}/
install -pm 640 sentinel.conf %{buildroot}%{_sysconfdir}/

install -dm 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}

install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

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
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/*.conf
%dir %attr(0755, %{name}, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}
%{_initrddir}/%{name}
%{_bindir}/%{name}-server
%{_bindir}/%{name}-sentinel
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-dump
%{_sbindir}/%{name}-server


%files cli
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README
%{_bindir}/redis-cli

###############################################################################

%changelog
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

* Tue Dec 16 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.19-0
- 02d465c Don't log admin commands in MONITOR. (antirez)
- 4d8f426 List of commands flagged as admin commands modified. (antirez)
- e47e460 Lua cmsgpack lib updated to latest version. (antirez)
- 5509c14 Add symlink to redis-sentinel during make install (Rhommel Lamas)
- 7de1ef7 SORT: Don't sort Set elements if not needed. (antirez)
- e945a54 Fix zero-ordering SORT when called against lists (Matt Stancliff)
- d81c383 Update redis_init_script.tpl (Ben Dowling)
- dba57ea FIXED redis-benchmark's idle mode.With idle mode shouldn't create write event (zhanghailei)
- 888ea17 zipmap.c: update comments above (Sun He)
- 86ebc13 replaced // comments  #2150 (Deepak Verma)
- 3d73f08 redis-benchmark AUTH command to be discarded after the first send #2150 (azure provisioned user)
- 76d53a6 sds.c: Correct two spelling mistakes in comments (Sun He)
- 4848cf9 sds.c/sdscatvprintf: set va_end to finish va_list cpy (Sun He)
- d2f584f sds.c: Correct some comments (Sun He)
- 2ed3f09 Update whatisdoing.sh (Serghei Iakovlev)
- 77b997d Include stropts only if __sun is defined. (antirez)
- d409371 Fix implicit declaration of ioctl on Solaris (Jan-Erik Rediger)
- 23b96c0 Silence _BSD_SOURCE warnings in glibc 2.20 and forward (Johan Bergström)
- a47a042 Mark whatisdoing.sh as deprecated in top-comment. (antirez)
- b5737d2 getting pid fixes (Serghei Iakovlev)
- a598e08 sparkline.c: AddSample skip Empty label (Sun He)
- 7d480ab sparkline.c: mov label-ini into the AddSample Function (Sun He)
- 2f3c860 Only ignore sigpipe in interactive mode (Jan-Erik Rediger)
- 0c211a1 Simplify lua_cmsgpack macro and fix build on old Linux distros. (antirez)

* Thu Dec 04 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.18-0
- [FIX] Linenoise updated to be more VT100 compatible. (Salvatore Sanfilippo)
- [FIX] A number of typos fixed inside comments. (Various authors)
- [FIX] redis-cli no longer quits after long timeouts. (Matt Stancliff)
- [FIX] Test framework improved to detect never terminating scripts, cleanup
        instances on crashes. (Salvatore Sanfilippo)
- [FIX] PFCOUNT can be used on slaves now. (Salvatore Sanfilippo)
- [FIX] ZSCAN no longer report very small scores as 0. (Matt Stancliff,
        Michael Grunder, Salvatore Sanfilippo)
- [FIX] Don't show the ASCII logo if syslog is enabled. Redis is now
        an Enterprise Grade product. (Salvatore Sanfilippo)
- [NEW] EXPERIMENTAL: Diskless replication, for more info check the doc at
        http://redis.io/topics/replication. (Salvatore Sanfilippo).
- [NEW] Transparent Huge Pages detection and reporting in logs and
        LATENCY DOCTOR output. (Salvatore Sanfilippo)
- [NEW] Many Lua scripting enhancements: Bitops API, cjson upgrade and tests,
        cmsgpack upgrade. (Matt Stancliff)
- [NEW] Total and instantaneous Network bandwidth tracking in INFO.
- [NEW] DEBUG POPULATE two args form implemented (old form still works).
        The second argument is the key prefix. Default is "key:" (Salvatore
        Sanfilippo)
- [NEW] Check that tcp-backlog is matched by /proc/sys/net/core/somaxconn, and
        warn about it if not. (Salvatore Sanfilippo)

* Tue Nov 25 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.17-2
- Fixed ip binding in config file

* Tue Oct 28 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.17-1
- Init script migrated to kaosv2

* Fri Sep 26 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.17-0
- [FIX] Resolved a memory leak in the hiredis library causing a memory leak
        in Redis Sentinel when a monitored instance or another Sentinel is
        unavailable. Every reconnection attempt will leak a small amount of
        memory, but in the long run the process can reach a considerable size.

* Wed Sep 17 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.16-0
- Improved spec
- [FIX] The ability to load truncated AOF files introduced with Redis 2.8.15
        contains a bug fixed in this release: after loading the file was not
        truncated to the last valid command, so the new commands are appended
        after a non well formed command. This means that:

        1) The first AOF rewrite triggered by the server will automatically
           fix the problem.
        2) However, if the server is restarted before the rewrite, Redis may
           not be able to load the file and you need to manually fix it.

        In order to fix a corrupted file you should start the redis-check-aof
        utility WITHOUT the --fix option, just to check the offset where the
        corruption is found. Around the offset reported by the check utility
        you'll find, inside your AOF file, a command which is not complete
        according to the Redis protocol. Just remove this incomplete command
        leafing the file unaltered before and after the offending command,
        and restart the server.

        IMPORTANT #1: Redis 2.8.15 is the only stable version of Redis with
        this bug so probably no actual real-world problem happened since the
        problem is automatically fixed at the first automatic AOF rewrite.

        IMPORTANT #2: Before upgrading to Redis 2.8.16, if you are using Redis
        2.8.15 with AOF enabled, make sure to trigger a manual AOF rewrite
        using the BGREWRITEAOF command.

- [FIX] SAVE is no longer propagated to AOF / slaves.

* Tue Sep 16 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.15-0
- [FIX] Sentinel critical bug fixed: the absolute majority was computed in a
        wrong way because of a programming error. Now the implementation does
        what the specification says and the majority to authorize a failover
        (that should not be confused with the ODOWN quorum) is the majority of
        *all- the Sentinels ever seen for a given master, regardless of their
        current state.
- [FIX] GETRANGE test no longer fails for 32 bit builds (Matt Stancliff).
- [FIX] Limit SCAN latency when the hash table is in an odd state (very few
        populted buckets because rehashing is in progress). (Xiaost and
        Salvatore Sanfilippo)
- [NEW] Redis is now able to load truncated AOF files without requiring a
        redis-check-aof utility run. The default now is to load truncated
        (but apparently not corrupted) AOFs, you can change this in redis.conf.
        (Salvatore Sanfilippo).
- [NEW] Sentinel: ability to announce itself with an arbitrary IP/port to work
        in the context of natted networks. However this is probably still
        not enough since there is no equivalent mechanism for slaves listed
        in the master INFO output. (Dara Kong and Salvatore Sanfilippo)

* Tue Sep 09 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.14-0
- [FIX] Don't prevent use of shared integers if maxmemory policy is non-LRU.
        (Salvatore Sanfilippo)
- [FIX] Fail SYNC if background save child aborted due to a signal.
        (Yossi Gottlieb)
- [FIX] Different small redis-cli fixes. (Dov Murik, Charsyam, cubicdaiya,
        Kashif Rasul, Jan-Erik Rediger, Matt Stancliff)
- [FIX] AIX compilation fixes. (Siah Lyimo)
- [FIX] A number of other smaller issues.
- [FIX] Improved SIGINT handling (Matt Stancliff, Salvatore Sanfilippo)
- [FIX] Use unsigned types in SDS header to raise limit to 4GB.
        (Matt Stancliff, Salvatore Sanfilippo)
- [FIX] Handle signed/unsigned comparisons with more care around the code.
        (Salvatore Sanfilippo)
- [FIX] Colorized test output fixed to don't change the background color.
        (Mariano Pérez Rodríguez)
- [FIX] More Sentinel IPv6 fixes. (Eiichi Sato)
- [FIX] Deny CLIENT command in scripts. (Matt Stancliff)
- [FIX] Allow datasets with more than 2 billion of keys, initial work.
- [FIX] Fix a Lua scripting crash by storing the length of the static
        argv when first allocated. (Paddy Byers)
- [NEW] Pub/Sub PING. (Salvatore Sanfilippo)
- [NEW] Much faster ZUNIONSTORE. (Kyle Hubert, Salvatore Sanfilippo)
- [NEW] Faster ll2string() implementation. (Salvatore Sanfilippo)
- [NEW] **WARNING, minor API change**: PUBSUB NUMSUB: return type modified
        to integer. (Matt Stancliff)
- [NEW] redis-benchmark support for AUTH. (CharSyam)

* Fri Aug 08 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.13-1
- Improved init script

* Tue Jul 15 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.13-0
- [FIX] CLIENT KILL minor backward compatibility fixes. (Salvatore Sanfilippo)
- [FIX] Enable HAVE_ATOMIC for PowerPC. (Matt Stancliff)
- [FIX] More robust PSYNC and AOF rewrites tests. (Salvatore Sanfilippo)
- [FIX] Solaris build fixed. (Matt Stancliff, Salvatore Sanfilippo)

- [NEW] The new latency monitoring feature, as documented at
        http://redis.io/topics/latency-monitor (Salvatore Sanfilippo)
- [NEW] The COMMAND command, exposing the Redis command table
        as an API. (Matt Stancliff)
- [NEW] Update used memory with C11 __atomic. (Matt Stancliff)

* Tue Jul 15 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.12-0
- [FIX / BREAKS BACKWARD COMPATIBILITY] Using SELECT inside Lua scripts no
       longer makes the selected DB to be set in the calling client.
       So Lua can still use SELECT, but the client calling the script will
       remain set to the original DB. Thix fixes an issue with Redis
       replication of Lua scripts that called SELECT without reverting the
       selected DB to the original one. (Salvatore Sanfilippo)
- [FIX] Sentinel failover was instalbe if the master was detected as available
        during the failover (especially during manual failovers) because
        of an implementation error (lack of checking of
        SRI_PROMOTED flag). (Salvatore Sanfilippo)
- [FIX] Cancel SHUTDOWN if initial AOF is being written. (Matt Stancliff)
- [FIX] Sentinel: bind source address for outcoming connections. (Matt
        Stancliff).
- [FIX] Less timing sensitive Sentinel tests. (Salvatore Sanfilippo).
- [NEW] redis-cli --intrinsic-latency stopped with SIGINT still reports
        stats (Matt Stancliff)
- [NEW] Sentinels broadcast an HELLO message ASAP after a failover in order to
        reach a consistent state faster (before it relied for periodic HELLO
        messages). (Salvatore Sanfilippo).
- [NEW] Jemalloc updated to 3.6.0. (Salvatore Sanfilippo)
- [NEW] CLIENT LIST speedup. (Salvatore Sanfilippo)
- [NEW] CLIENT LIST new unique incremental ID to every client. (Salvatore
        Sanfilippo)
- [NEW] ROLE command added. (Salvatore Sanfilippo)
- [NEW] CLIENT KILL new form to kill by client type and ID (see doc at
        redis.io for more info). (Salvatore Sanfilippo)
- [NEW] Sentinel now disconnects clients when instances are reconfigured
        (see http://redis.io/topics/sentinel-clients). (Salvatore Sanfilippo)
- [NEW] Hiredis update to latest version. (Matt Stancliff)

* Wed Jun 18 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.11-1
- Some minor improvements in init script

* Mon Jun 16 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.11-0
- [FIX] A previous fix for Lua -> Redis numerical precision enhancement
        introduced a new problem. In Redis 2.8.10 commands called from Lua
        passing a string that "looks like" a very large number, may actually
        use as argument the string converted as a float. This bug is now
        fixed.
- [FIX] Now commands other than *PUSH- adding elements to a list will be able
        to awake clients blocked in a blocking POP operation.
- [FIX] Cygwin compilation fixes.

* Tue Jun 10 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.10-0
- [FIX] IMPORTANT! A min-slaves-to-write option active in a slave totally
        prevented the slave from acception the master stream of commands.
        This release includes testes for min-slaves-to-write, and a fix
        for this issue.
- [FIX] Sometimes DEL returned 1 for already expired keys. Fixed.
- [FIX] Fix test false positive because new osx 'leaks' output.
- [FIX] PFCOUNT HLL cache invalidation fixed: no wrong value was reported
        but the cache was not used at all, leading to lower performances.
- [FIX] Accept(2) multiple clients per readable-event invocation, and better
        processing of I/O while loading or busy running a timedout script.
        Basically now the LOADING / BUSY errors are reported at a decent
        speed.
- [FIX] A softwaer watchdog crash fixed.
- [FIX] Fixed a Lua -> Redis numerical precision loss.
- [NEW] Lua scripting engine speed improved.
- [NEW] Sentinel generates one new event for humans to understand better
        what is happening during a failover:config-update-from.
        Also the time at which a failover will be re-attempted is logged.

* Tue Apr 22 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.9-0
- [NEW] The HyperLogLog data structure. You can read more about it
        in this blog post. http://antirez.com/news/75
- [NEW] The Sorted Set data type has now support for lexicographic range
        queries, check the new commands ZRANGEBYLEX, ZLEXCOUNT and
        ZREMRANGEBYLEX, which are documented at http://redis.io.

* Mon Apr 21 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.8-1
- Added security patch for linenoise

* Tue Mar 25 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.8-0
- [FIX] Fixed data loss when SHUTDOWN was used with a disk full condition.
- [FIX] Fixed a memory leak in the SORT syntax error processing.
- [FIX] When Sentinel down-after-milliseconds parameter is modified at runtime
        now it gets propagated to all the slaves and sentinel instances
        of the master.
- [FIX] `install_server.sh` script finally fixed.
- [FIX] Different fixes to maxclients handling.
- [NEW] Sentinels are now able to send update messages in a peer-to-peer
        fashion even if no Redis instances are available. Now the Sentinel
        liveness property that the most updated configuration in a given
        partition is propagated to all the Sentinels is extended to partitions
        without reachable instances.
- [NEW] Sentinel safety properties are now ensured in a crash-recovery system
        model since some state is persisted on disk before replying to other
        nodes, and reloaded at startup.
- [NEW] Sentinel now uses CLIENT SETNAME so that it is easy to identify
        Sentinels using CLIENT LIST among other clients.
- [NEW] Sentinel failure detection and reconnection code improved.
- [NEW] Use all 24 bits (instead of 22) for the Redis objects LRU field.
        Note that the new LRU algorithm using eviction pools was not backported
        from unstable for safery / code maturity concerns.
- [NEW] Majory speedup for the INFO command (it is now 6 times faster).
- [NEW] More Sentinel unit tests.
- [NEW] New command DEBUG ERROR returns the specified error. Example:
        DEBUG ERROR "LOADING database". This is handy to write Redis client
        libraries unit tests.
- [NEW] redis-cli now supports multi-line editing via updated linenoise lib.

* Wed Mar 05 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.7-0
- [FIX] Sometimes the absolute config file path was obtained in a wrong way.
        This happened when there was a "dir" directive inside the config file
        and at the same time the configuration file was given as a relative
        path to redis-server or redis-sentinel executables.
- [FIX] redis-cli: Automatically enter --slave mode when SYNC or PSYNC are
        called during an interactive session.
- [FIX] Sentinel "IDONTKNOW" error removed as it does not made sense with the
        new Sentinel design. This error was actually a fix for a design error
        in the first implementation of Sentinel.
- [FIX] Sentinel: added a missing exit() call to abort after config file
        checks at startup. This error was introduced with an improvement in
        a previous 2.8 release.
- [FIX] BITCOUNT: fixed unaligned access causing issues in sparc and other
        archs not capable of dealing with unaligned accesses. This also makes
        the code faster in archs where unaligned accesses are allowed.
- [FIX] Sentinel: better nodes fail over start time desynchronization to avoid
        split-brain during the voting process needed to get authorization to
        fail over. This means the system is less likely to need to retry
        and will fail over faster. No changes in behavior / correctness.
- [FIX] Force INFO used_memory_peak to match peak memory. This generated some
        confusion among users even if it was not an actual bug.
- [NEW] Sentinel unit tests and framework. More tests needed and units must
        be improved in order to have less false positives, but it is a start
        and features a debugging console that is useful to fix tests or to
        inspect bugs causing tests failures.
- [NEW] New Sentinel events: +/-monitor and +set used to monitor when an
        instance to monitor is added or removed, or when a configuration
        is modified via SENTINEL SET.
- [NEW] Redis-cli updated to use SCAN instead of random sampling via
        RANDOMKEY in order to implement --bigkeys feature. Moreover the
        implementation now supports pipelining and reports more information
        at the end of the scan. Much faster, much better. A special thank
        you to Michael Grunder for this improvement.
- [NEW] redis-cli now supports a new --intrinsic-latency mode that is able
        to meter the latency of a system due to kernel / hypervisor.
        How to use it is explained at http://redis.io/topics/latency.
- [NEW] New command BITPOS: find first bit set or clear in a bitmap.
- [NEW] CONFIG REWRITE calls are now logged.

* Thu Feb 13 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.6-0
- [FIX] Fixed an critical EVALSHA script cache bug: scripts executed may not
        propagate to AOF / Slaves correctly under certain conditions.
        See issue #1549 at Github for more information.
- [FIX] Fixed multiple bugs resulting into closing the link with master or slave
        during replication without good reasons. This will result in useless
        resynchronizations, or infinite loops where the replication link can't
        be established.
- [FIX] Don't count the time needed to populate the buffers of clients waiting
        in MONITOR mode when populating the Slow Log entries.
- [NEW] AOF write errors (like no space on device) no longer abort Redis if the
        fsync policy is none or every second. The database enters a read-only
        mode where every write is refused with an error. Normal operations are
        restored as soon as Redis is able to append again data to the AOF file.
- [NEW] Sentinel now accepts SHUTDOWN command.

* Fri Feb 07 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.5-1
- Init script migrated to kaosv
- Fixed some minor problems in spec

* Tue Feb 04 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.5-0
- [FIX] Fixed a replication bug caused by Lua scripts + expired keys: keys could
        expire in the middle of scripts causing non-deterministic behavior.
- [FIX] MISCONFIG error if condition fixed, the server was no longer able
        to stop writes on RDB misconfiguration after this error was introduced.
- [FIX] REDIS_AOF_REWRITE_MIN_SIZE is now 64mb like example redis.conf default.
- [FIX] Perform fflush() before fsync() in rio.c (bug without actual effects).
- [FIX] Don't log MONITOR clients as disconnecting slaves.
- [FIX] SENTINEL MASTER arity check fixed. Crashed the Sentinel instance when
        the command was given without arguments.
- [NEW] Allow CONFIG and SHUTDOWN while in stale-slave state.
- [NEW] Support for configurable TCP listen(2) backlog size.
- [NEW] redis-cli supports SCAN via the --scan and --pattern options.
- [NEW] SENTINEL SET master quorum via runtime API implemented.

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 2.8.4-0
- [FIX] Makefile compatibility with non common make variants improved.
- [FIX] SDIFF crash in very unlikely to trigger state fixed.
- [FIX] Config rewriting fixed: don't wipe options unknown to the rewrite
        process.
- [FIX] Set TCP port to 0 works again to disable TCP networking.
- [FIX] Fixed replication with old Redis instances as masters by not
        sending REPLCONF ACK to them.
- [FIX] Fix keyspace notifications rewrite and CONFIG GET output.
- [FIX] Fix RESTORE TTL handling in 32 bit systems (32 bit overflow).
- [NEW] Sentinel now has a run time configuration API.
- [NEW] Log when we lost connection with master or slave.
- [NEW] When instance is turned from slave to master now inherits the
        old master replication offset when possible. This improves the
        Sentinel failover procedure.
        
* Mon Dec 16 2013 Anton Novojilov <andy@essentialkaos.com> - 2.8.3-0
- [FIX] Sentinel instance role sampling fixed, the system is now more
        reliable during failover and when reconfiguring instances with
        non matching configuration.
- [FIX] Inline requests are now handled even when terminated with just LF.
- [FIX] Replication timeout handling greatly improved, now the slave is able
        to ping the master while removing the old data from memory, and while
        loading the new RDB file. This avoid false timeouts sensed by
        masters.
- [FIX] Fixed a replication bug involving 32 bit instances and big datasets
        hard to compress that resulted into more than 2GB of RDB file sent.
- [FIX] Return error for inline requests with unbalanced quotes.
- [FIX] Publish the slave replication offset even when disconnected from the
        master if there is still a cached master instance.

* Mon Dec 02 2013 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- [FIX] Sentinel better desynchronization to avoid split-brain elections
  where no Sentinel managed to get elected.
- [FIX] Stop accepting writes on "MISCONF" error only if master, not slave.
- [FIX] Reply to PING with an error on "MISCONF" errors.

* Tue Nov 26 2013 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- [FIX] Fixed a bug in "new Sentinel" config propagation.
- [FIX] Fixed a false positive in Redis tests.
