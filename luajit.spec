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

%define api_version       5.1
%define major_version     2
%define minor_version     0.5

###############################################################################

Name:              luajit
Summary:           Just-In-Time Compiler for Lua
Version:           2.0.5
Release:           0%{?dist}
License:           MIT
Group:             Development/Tools
URL:               http://luajit.org

Source:            http://luajit.org/download/LuaJIT-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     gcc make

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
LuaJIT is a Just-In-Time Compiler (JIT) for the Lua programming language.

###############################################################################

%package -n libluajit

Summary:           LuaJIT shared library
Group:             Development/Libraries

%description -n libluajit
LuaJIT shared library.

###############################################################################

%package -n libluajit-devel

Summary:           Headers and static lib for LuaJIT
Group:             Development/Libraries
Requires:          libluajit >= %{version}

%description -n libluajit-devel
Headers and static lib for LuaJIT.

###############################################################################

%prep
%setup -q -n LuaJIT-%{version}

%build
export CFLAGS="$CFLAGS -fPIC"

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install} PREFIX=%{_usr} INSTALL_LIB=%{buildroot}%{_libdir}

ln -sf %{_libdir}/libluajit-%{api_version}.so.%{major_version}.%{minor_version} \
       %{buildroot}%{_libdir}/libluajit-%{api_version}.so

%post -n libluajit
%{__ldconfig}

%postun -n libluajit
%{__ldconfig}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc COPYRIGHT README
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_datarootdir}/%{name}-%{version}/*
%{_mandir}/man1/%{name}.1*

%files -n libluajit
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.so

%files -n libluajit-devel
%defattr(-,root,root)
%{_includedir}/%{name}-*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.0.5-0
- Add workaround for MSVC 2015 stdio changes
- Limit mcode alloc probing, depending on the available pool size
- Fix overly restrictive range calculation in mcode allocation
- Fix out-of-scope goto handling in parser
- Remove internal __mode = "K" and replace with safe check
- Add "proto" field to jit.util.funcinfo()
- Fix GC step size calculation
- Initialize uv->immutable for upvalues of loaded chunks
- Fix for cdata vs. non-cdata arithmetics/comparisons
- Drop leftover regs in 'for' iterator assignment, too
- Fix PHI remarking in SINK pass
- Don't try to record outermost pcall() return to lower frame
- Add guard for obscure aliasing between open upvalues and SSA slots
- Remove assumption that lj_math_random_step() doesn't clobber FPRs
- Fix handling of non-numeric strings in arithmetic coercions
- Fix recording of select(n, ...) with off-trace vararg
- Fix install for cross-builds
- Don't allocate unused 2nd result register in JIT compiler backend
- Drop marks from replayed instructions when sinking
- Fix unsinking check
- Properly handle OOM in trace_save()
- Limit number of arguments given to io.lines() and fp:lines()
- Fix narrowing of TOBIT
- OSX: Fix build with recent XCode
- x86/x64: Don't spill an explicit REF_BASE in the IR
- x86/x64: Fix instruction length decoder
- x86/x64: Search for exit jumps with instruction length decoder
- ARM: Fix BLX encoding for Thumb interworking calls
- MIPS: Don't use RID_GP as a scratch register
- MIPS: Fix emitted code for U32 to float conversion
- MIPS: Backport workaround for compact unwind tables
- MIPS: Fix cross-endian jit.bcsave
- MIPS: Fix BC_ISNEXT fallback path
- MIPS: Fix use of ffgccheck delay slots in interpreter
- FFI: Fix FOLD rules for int64_t comparisons
- FFI: Fix SPLIT pass for CONV i64.u64
- FFI: Fix ipairs() recording
- FFI: Don't propagate qualifiers into subtypes of complex

* Wed Apr 27 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.4-1
- Improved build process

* Fri May 22 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0.4-0
- Fix stack check in narrowing optimization
- Fix Lua/C API typecheck error for special indexes
- Fix string to number conversion
- Fix lexer error for chunks without tokens
- Don't compile IR_RETF after CALLT to ff with-side effects
- Fix BC_UCLO/BC_JMP join optimization in Lua parser
- Fix corner case in string to number conversion
- Gracefully handle lua_error() for a suspended coroutine
- Avoid error messages when building with Clang
- Fix snapshot #0 handling for traces with a stack check on entry
- Fix fused constant loads under high register pressure
- Invalidate backpropagation cache after DCE
- Fix ABC elimination
- Fix debug info for main chunk of stripped bytecode
- Fix FOLD rule for string.sub(s, ...) == k
- Fix FOLD rule for STRREF of SNEW
- Fix frame traversal while searching for error function
- Prevent GC estimate miscalculation due to buffer growth
- Prevent adding side traces for stack checks
- Fix top slot calculation for snapshots with continuations
- Fix check for reuse of SCEV results in FORL
- Add PS Vita port
- Fix compatibility issues with Illumos
- Fix DragonFly build (unsupported)
- OpenBSD/x86: Better executable memory allocation for W^X mode
- x86: Fix argument checks for ipairs() iterator
- x86: lj_math_random_step() clobbers XMM regs on OSX Clang
- x86: Fix code generation for unused result of math.random()
- x64: Allow building with LUAJIT_USE_SYSMALLOC and LUAJIT_USE_VALGRIND
- x86/x64: Fix argument check for bit shifts
- x86/x64: Fix code generation for fused test/arith ops
- ARM: Fix write barrier check in BC_USETS
- PPC: Fix red zone overflow in machine code generation
- PPC: Don't use mcrxr on PPE
- Various archs: Fix excess stack growth in interpreter
- FFI: Fix FOLD rule for TOBIT + CONV num.u32
- FFI: Prevent DSE across ffi.string()
- FFI: No meta fallback when indexing pointer to incomplete struct
- FFI: Fix initialization of unions of subtypes
- FFI: Fix cdata vs. non-cdata arithmetic and comparisons
- FFI: Fix __index/__newindex metamethod resolution for ctypes
- FFI: Fix compilation of reference field access
- FFI: Fix frame traversal for backtraces with FFI callbacks
- FFI: Fix recording of indexing a struct pointer ctype object itself
- FFI: Allow non-scalar cdata to be compared for equality by address
- FFI: Fix pseudo type conversions for type punning

* Fri Mar 14 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- Add PS4 port
- Add support for multilib distro builds
- Fix OSX build
- Fix MinGW build
- Fix Xbox 360 build
- Improve ULOAD forwarding for open upvalues
- Fix GC steps threshold handling when called by JIT-compiled code
- Fix argument checks for math.deg() and math.rad()
- Fix jit.flush(func|true)
- Respect jit.off(func) when returning to a function, too
- Fix compilation of string.byte(s, nil, n)
- Fix line number for relocated bytecode after closure fixup
- Fix frame traversal for backtraces
- Fix ABC elimination
- Fix handling of redundant PHIs
- Fix snapshot restore for exit to function header
- Fix type punning alias analysis for constified pointers
- Fix call unroll checks in the presence of metamethod frames
- Fix initial maxslot for down-recursive traces
- Prevent BASE register coalescing if parent uses IR_RETF
- Don't purge modified function from stack slots in BC_RET
- Fix recording of BC_VARG
- Don't access dangling reference to reallocated IR
- Fix frame depth display for bytecode dump in -jdump
- ARM: Fix register allocation when rematerializing FPRs
- x64: Fix store to upvalue for lightuserdata values
- FFI: Add missing GC steps for callback argument conversions
- FFI: Properly unload loaded DLLs
- FFI: Fix argument checks for ffi.string()
- FFI/x64: Fix passing of vector arguments to calls
- FFI: Rehash finalizer table after GC cycle, if needed
- FFI: Fix cts->L for cdata unsinking in snapshot restore

* Fri Jan 31 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Initial build