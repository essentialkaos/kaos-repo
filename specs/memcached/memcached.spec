################################################################################

%ifarch i386
  %define optflags -O2 -g -march=i686
%endif

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __sysctl          %{_bindir}/systemctl

################################################################################

%define username          memcached
%define groupname         memcached

################################################################################

Summary:                  High Performance, Distributed Memory Object Cache
Name:                     memcached
Version:                  1.5.10
Release:                  0%{?dist}
Group:                    System Environment/Daemons
License:                  BSD
URL:                      http://memcached.org

Source0:                  https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
Source1:                  %{name}.init
Source2:                  %{name}.sysconf
Source3:                  %{name}.service

BuildRoot:                %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:            gcc automake which

%if 0%{?rhel} <= 6
Requires:                 initscripts kaosv >= 2.15
%endif

%if 0%{?rhel} >= 7
BuildRequires:            libevent-devel

Requires:                 libevent
Requires(pre):            shadow-utils
Requires(post):           systemd
Requires(preun):          systemd
Requires(postun):         systemd
%else
BuildRequires:            libevent2-devel

Requires:                 libevent2
Requires(pre):            shadow-utils
Requires(post):           %{__chkconfig}
Requires(preun):          %{__chkconfig} %{__service}
Requires(postun):         %{__service}
%endif

################################################################################

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

################################################################################

%package devel
Summary:                  Files needed for development using memcached protocol
Group:                    Development/Libraries
Requires:                 %{name} = %{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.

################################################################################

%package debug
Summary:                  Debug version of memcached
Group:                    System Environment/Daemons
Requires:                 %{name} = %{version}-%{release}

%description debug
Version of memcached show more additional information for debugging.

################################################################################

%prep

%setup -q
./autogen.sh

%configure
sed -i 's/-Werror/ /' Makefile
sed -i "s/UNKNOWN/%{version}/" version.m4

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

install -dm 755 %{buildroot}%{_bindir}
%if 0%{?rhel} <= 6
install -dm 755 %{buildroot}%{_initrddir}
%endif
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}

%if 0%{?rhel} <= 6
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
%endif

install -pm 755 %{name}-debug %{buildroot}%{_bindir}/%{name}-debug
install -pm 755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool

touch %{buildroot}%{_logdir}/%{name}/%{name}.log

%clean
rm -rf %{buildroot}

################################################################################

%pre
%{__getent} group %{groupname} >/dev/null || %{__groupadd} -r %{groupname}
%{__getent} passwd %{username} >/dev/null || %{__useradd} -r -g %{groupname} -d %{_rundir}/%{name} -s /sbin/nologin %{username}

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} %{name} stop &>/dev/null || :
  %{__chkconfig} --del %{name} &>/dev/null || :
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(755,%{username},%{groupname}) %{_rundir}/%{name}

%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%if 0%{?rhel} <= 6
%{_initrddir}/%{name}
%endif

%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif

%dir %attr(755,%{username},%{groupname}) %{_logdir}/%{name}
%attr(644,%{username},%{groupname}) %{_logdir}/%{name}/%{name}.log

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/*

%files debug
%defattr(-,root,root,0755)
%{_bindir}/%{name}-debug

################################################################################

%changelog
* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.10-0
- fix alignment issues on some ARM platforms for chunked items
- add missing va_end() call to logger_log()
- basic extstore JBOD support (noted in Overview)
- split storage writer into its own thread

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.9-0
- fix ASCII get error handling (+ extstore leak)
- drop_privileges is no longer default if available.
- remove bad assert from crawler
- Mark seccomp experimental
- Include keys with non-[\w.~-] bytes in memcached-tool dump
- whitelist clock_gettime in seccomp rules
- Fix segfault: Prevent calling sasl_server_step before sasl_server_start
- fix flaky lru-maintainer test (OS X)
- support transparent hugepages on Linux (-L option)

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.8-0
- fix sasl tests
- fix flaky extstore tests
- alignment and 32bit fixes for extstore
- crc32c for aarch64 support
- fix rare partial deadlock during hash table expansion
- Add Dockerfile definitions
- Fix lru-crawler behaviour for seccomp
- Fail loudly if seccomp setup fails

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.7-0
- extstore: fix ref leak when using binary protocol with TOUCH,GAT,GATK
- Drop supplementary groups in addition to setgid
- Use HAVE_SASL_CB_GETCONFPATH
- Fix SASL_CB_GETCONF(PATH) detection
- Rewrite memchached-tool 'dump' method to use new lru_crawler interface.
- Fixes decrement-before-check problem.
- document in manpage that port 0 is off.
- Fix SIGBUS from alignment issues on 64bit ARM
- Update seccomp with syscalls found on Arch
- Enforce seccomp policy (kill process)
- Support seccomp on musl
- update --help for UDP default
- Fix sed options order in rpm specfile

* Sat Mar 03 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.6-0
- Improved systemd unit
- disable UDP port by default
- systemd instancing support & rpm build improvements
- fix gcc warnings in beta GCC
- fix build with clang
- fix for dtrace compilation on freebsd

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- make -I argument less position dependent
- external storage base commit
- lru_crawler metadump output ends with "END\r\n"
- fix: -o no_lru_crawler didn't work

* Mon Nov 06 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.5.3-0
- Added listen option to support bindings on IP address
- Improved systemd unit file
- Added get and touch command for ascii protocol
- Added warning about time on very low TTL's in doc/protocol.txt
- Pledged privdropping support for OpenBSD
- Made for loop more clear in logger watcher
- Fixed theoretical leak in process_bin_stat
- Fixed use of unitialized array in lru_maintainer
- Fixed -o no_hashexpand to disable hash table expansion
- Fixed chunked items set in binprot, read from ascii

* Mon Nov 06 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.5.2-0
- Fixed more binary protocol documentation errors.
- Fixed segfault during 31b -> 32b hash table expand
- Create hashtables larger than 32bit
- Some non-user-facing code changes for supporting future features.

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Add max_connections stat to 'stats' output
- Drop sockets from obviously malicious command strings (HTTP/)
- stats cachedump: now more likely to show data
- memcached-tool: fix slab Full? column
- Fix null pointer ref in logger for bin update cmd
- Default to unix sockets for tests, make them much less flaky
- PARALLEL=9 make test -> runs prove in parallel
- Fix flaky stats.t test
- --enable-seccomp compiles in options for strict privilege reduction in
  linux. see output of -h for more information.

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Fix for musl libc: avoid huge stack allocation
- LRU crawler to background-reclaim memory. Mixed-TTL's and LRU reordering
  leaves many holes, making it difficult to properly size an instance.
- Segmented LRU. HOT/WARM/COLD and background processing should try harder to
  keep semi-active items in memory for longer.
- Automated slab rebalancing. Avoiding slab stagnation as objects change size
  over time.
- Faster hash table lookups with murmur3 algorithm (though it's been so long
  this is now outdated again;)
- Reduce memory requirements per-item by a few bytes here and there
- Immediately close connections when hitting the connection limit, instead of
  hanging until a spot opens up.
- Items larger than 512k (by default) are assembled by stacking multiple chunks
  together. Now raising the item size above 1m doesn't drop memory efficiency
  by spreading out slab classes.

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.39-0
- Fix for CVE-2017-9951
- Save four bytes per item if client flags are 0
- If client flags are "0", no extra storage is used

* Wed Apr 05 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.36-1
- Improved init script

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.36-0
- Fix refcount leak in LRU bump buf

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.34-0
- Add -o modern switches to -h
- metadump: Fix preventing dumping of class 63
- Fix cache_memlimit bug for > 4G values
- metadump: ensure buffer is flushed to client before finishing
- Number of small fixes/additions to new logging
- Add logging endpoint for LRU crawler
- Evicted_active counter for LRU maintainer
- Stop pushing NULL byte into watcher stream
- Scale item hash locks more with more worker threads (minor performance)
- Further increase systemd service hardening
- Missing necessary header for atomic_inc_64_nv() used in logger.c (solaris)
- Fix print format for idle timeout thread
- Improve binary sasl security fixes
- Fix clang compile error
- Widen systemd caps to allow maxconns to increase
- Add -X option to disable cachedump/metadump
- Don't double free in lru_crawler on closed clients
- Fix segfault if metadump client goes away

* Wed Nov 02 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.33-0
- Fixed CVE reported by cisco talos

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.32-0
- Fix missing evicted_time display in stats output
- Update old ChangeLog note to visit Github wiki
- Fix OOM errors with newer LRU
- Misc typo fixes

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.31-0
- More fixes for defaults related to large item support.
- Several improvements to how the LRU crawler's default background job is
  launched. Should be less aggressive.
- Fix LRU crawler rate limiting sleep never actually being used.
