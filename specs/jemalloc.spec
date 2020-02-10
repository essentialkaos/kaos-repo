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
%define __ldconfig        %{_sbin}/ldconfig
%define __chkconfig       %{_sbin}/chkconfig

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            General-purpose scalable concurrent malloc implementation
Name:               jemalloc
Version:            5.2.1
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            BSD
URL:                http://jemalloc.net

Source0:            https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make libxslt

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of jemalloc.

################################################################################

%package devel

Summary:        Development files for jemalloc
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}

%description devel
The jemalloc-devel package contains libraries and header files for
developing applications that use jemalloc.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

%clean
rm -rf %{buildroot}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%doc COPYING README VERSION
%doc doc/jemalloc.html
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%{_bindir}/%{name}.sh
%{_bindir}/jeprof

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

################################################################################

%changelog
* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 5.2.1-0
- Fix a severe virtual memory leak on Windows. This regression was first
  released in 5.0.0.
- Fix size 0 handling in posix_memalign(). This regression was first released
  in 5.2.0.
- Fix the prof_log unit test which may observe unexpected backtraces from
  compiler optimizations. The test was first added in 5.2.0.
- Fix the declaration of the extent_avail tree. This regression was first
  released in 5.1.0.
- Fix an incorrect reference in jeprof. This functionality was first released
  in 3.0.0.
- Fix an assertion on the deallocation fast-path. This regression was first
  released in 5.2.0.
- Fix the TLS_MODEL attribute in headers. This regression was first released
  in 5.0.0.
- Implement opt.retain on Windows and enable by default on 64-bit.
- Optimize away a branch on the operator delete path.
- Add format annotation to the format generator function.
- Refactor and improve the size class header generation.
- Remove best fit.
- Avoid blocking on background thread locks for stats.
- Added CRC check for all sources.

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-0
- Implement oversize_threshold, which uses a dedicated arena for allocations
  crossing the specified threshold to reduce fragmentation.
- Add extents usage information to stats.
- Log time information for sampled allocations.
- Support 0 size in sdallocx.
- Output rate for certain counters in malloc_stats.
- Add configure option --enable-readlinkat, which allows the use of readlinkat
  over readlink.
- Add configure options --{enable,disable}-{static,shared} to allow not building
  unwanted libraries.
- Add configure option --disable-libdl to enable fully static builds.
- Add mallctl interfaces.
- Update MSVC builds.
- Workaround a compiler optimizer bug on s390x.
- Make use of pthread_set_name_np(3) on FreeBSD.
- Implement malloc_getcpu() to enable percpu_arena for windows.
- Link against -pthread instead of -lpthread.
- Make background_thread not dependent on libdl.
- Add stringify to fix a linker directive issue on MSVC.
- Detect and fall back when 8-bit atomics are unavailable.
- Fall back to the default pthread_create(3) if dlsym(3) fails.
- Refactor the TSD module.
- Avoid taking extents_muzzy mutex when muzzy is disabled.
- Avoid taking large_mtx for auto arenas on the tcache flush path.
- Optimize ixalloc by avoiding a size lookup.
- Implement opt.oversize_threshold which uses a dedicated arena for requests
  crossing the threshold, also eagerly purges the oversize extents. Default
  the threshold to 8 MiB.
- Clean compilation with -Wextra.
- Refactor the size class module.
- Refactor the stats emitter.
- Optimize pow2_ceil.
- Avoid runtime detection of lazy purging on FreeBSD.
- Optimize mmap(2) alignment handling on FreeBSD.
- Improve error handling for THP state initialization.
- Rework the malloc() fast path.
- Rework the free() fast path.
- Refactor and optimize the tcache fill / flush paths.
- Optimize sync / lwsync on PowerPC.
- Bypass extent_dalloc() when retain is enabled.
- Optimize the locking on large deallocation.
- Reduce the number of pages committed from sanity checking in debug build.
- Deprecate OSSpinLock.
- Lower the default number of background threads to 4 (when the feature is
  enabled).
- Optimize the trylock spin wait.
- Use arena index for arena-matching checks.
- Avoid forced decay on thread termination when using background threads.
- Disable muzzy decay by default.
- Only initialize libgcc unwinder when profiling is enabled.
- Fix background thread index issues with max_background_threads.
- Fix stats output for opt.lg_extent_max_active_fit.
- Fix opt.prof_prefix initialization.
- Properly trigger decay on tcache destroy.
- Fix tcache.flush.
- Detect whether explicit extent zero out is necessary with huge pages or
  custom extent hooks, which may change the purge semantics.
- Fix a side effect caused by extent_max_active_fit combined with decay-based
  purging, where freed extents can accumulate and not be reused for an
  extended period of time.
- Fix a missing unlock on extent register error handling.

* Sat Mar 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.1.0-0
- Initial build for kaos repository
