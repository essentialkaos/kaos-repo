################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global _vpath_srcdir   .
%global _vpath_builddir %{_target_platform}

################################################################################

Summary:        The Oil Run-time Compiler
Name:           orc
Version:        0.4.40
Release:        0%{?dist}
Group:          System Environment/Libraries
License:        BSD
URL:            https://gitlab.freedesktop.org/gstreamer/orc

Source0:        https://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  meson gcc

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

################################################################################

%package devel
Summary:   Development files and static libraries for Orc
Group:     Development/Libraries

Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-compiler pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

################################################################################

%package compiler
Summary:   Orc compiler
Group:     Development/Libraries

Requires:  %{name} = %{version}-%{release}
Requires:  pkgconfig

%description compiler
The Orc compiler, to produce optimized code.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{meson} -Dgtk_doc=disabled
%{meson_build}

%install
rm -rf %{buildroot}

%{meson_install}

rm -f %{buildroot}%{_libdir}/*.a

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/liborc-*.so.*
%{_bindir}/%{name}-bugreport

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/%{name}-0.4.pc
%{_libdir}/pkgconfig/%{name}-test-0.4.pc

%files compiler
%defattr(-,root,root,-)
%{_bindir}/orcc

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 0.4.40-0
- Security: Minor follow-up fixes for CVE-2024-40897
- powerpc: fix div255w which still used the inexact substitution
- x86: work around old GCC versions (pre 9.0) having broken xgetbv
  implementations
- x86: consider MSYS2/Cygwin as Windows for ABI purposes only
- x86: handle unnatural and misaligned array pointers
- orccodemem: Assorted memory mapping fixes
- Fix include header use from C++
- Some compatibility fixes for Musl
- ppc: Disable VSX and ISA 2.07 for Apple targets
- ppc: Allow detection of ppc64 in Mac OS
- x86: Fix non-C11 typedefs
- meson: Fix detecting XSAVE on older AppleClang
- x86: try fixing AVX detection again by adding check for XSAVE
- Check return values of malloc() and realloc()

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 0.4.39-0
- Security: Fix error message printing buffer overflow leading to possible
  code execution in orcc with specific input files (CVE-2024-40897). This
  only affects developers and CI environments using orcc, not users of liborc
- div255w: fix off-by-one error in the implementations
- x86: only run AVX detection if xgetbv is available
- x86: fix AVX detection by implementing the check recommended by Intel
- Only enable JIT compilation on Apple arm64 if running on macOS, fixes crashes
  on iOS
- Fix potential crash in emulation mode if logging is enabled
- Handle undefined TARGET_OS_OSX correctly
- orconce: Fix typo in GCC __sync-based implementation
- orconce: Fix usage of __STDC_NO_ATOMICS__
- Fix build with MSVC 17.10 + C11
- Support stack unwinding on Windows
- Major opcode and instruction set code clean-ups and refactoring
- Refactor allocation and chunk initialization of code regions
- Fall back to emulation on Linux if JIT support is not available,
  e.g. because of SELinux sandboxing or noexec mounting)

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 0.4.38-0
- x86: account for XSAVE when checking for AVX support, fixing usage on
  hardened linux kernels where AVX support has been disabled
- neon: Use the real intrinsics for divf and sqrtf
- orc.m4 for autotools is no longer shipped. If anyone still uses
  it they can copy it into their source tree

* Wed Oct 11 2023 Anton Novojilov <andy@essentialkaos.com> - 0.4.34-0
- Thread-safety improvements around orc codemem allocation/freeing
- Add orc_parse_code() with more detailed error reporting
- Implement Orc function lazy initialization correctly via atomic operations
- orc program parser fixes and improvements
- build fixes and compiler warning fixes
- coverity and clang scan-build static code analysis fixes
- meson: Do not always generate static library for test library
- ci improvements

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.4.33-0
- Add support for aarch64 (64-bit ARM) architecture (not yet enabled on
  Windows though)
- aarch32: Implement loadupdb instruction used e.g. for video pixel
  format packing/unpacking/conversions
- neon: Fix unsigned only implementation of loadoffb, loadoffw and loadoffl
- neon: Fix testsuite not passing on arm CPUs
- orccodemem: Fix use-after-free in error paths
- orccpu-powerpc: Fix build with kernel < 4.11
- Add support for macOS Hardened Runtime
- Enable only SSE and MMX backends for Windows
- Fix ORC_RESTRICT definition for MSVC
- pkgconfig: add -DORC_STATIC_COMPILATION flag to .pc file for static-only
  builds

* Wed Sep 21 2022 Anton Novojilov <andy@essentialkaos.com> - 0.4.32-0
- Add support for JIT code generation in Universal Windows Platform apps
- Minor Meson build system fixes and improvements

* Fri Feb 14 2020 Anton Novojilov <andy@essentialkaos.com> - 0.4.31-0
- Fix OrcTargetPowerPCFlags enum typedef to revert API change on macOS/iOS
- Fixes for various PowerPC issues
- Enable flush-to-zero mode for float programs on ARM/neon
- Fix some opcodes to support x2/x4 processing on PowerPC

* Fri Feb 14 2020 Anton Novojilov <andy@essentialkaos.com> - 0.4.30-0
- Don't always generate static library but default to shared-only
- Work around false positives in Microsoft UWP certification kit
- Add endbr32/endbr64 instructions on x86/x86-64 for indirect branch tracking
- Fix gtk-doc build when orc is used as a meson subproject
- Switch float comparison in tests to ULP method to fix spurious failures
- Fix flushing of ARM icache when using dual map
- Use float constants/parameters when testing float opcodes
- Add support for Hygon Dhyana processor
- Fix PPC/PPC64 CPU family detection
- Add little-endian PPC support
- Fix compiler warnings with clang
- Mark exec mapping writable in debug mode for allowing breakpoints
- Various codegen refactorings
- autotools support has been dropped in favour of Meson as build system
- Fix PPC CPU feature detection and add support for VSX/v2.07
- Add double/int64 support for PPC

* Fri Feb 14 2020 Anton Novojilov <andy@essentialkaos.com> - 0.4.29-0
- PowerPC: Support ELFv2 ABI and ppc64le
- Mips backend: only enable if the DSPr2 ASE is present
- Windows and MSVC build fixes
- orccpu-arm: Allow 'cpuinfo' fallback on non-android
- pkg-config file for orc-test library
- orcc: add --decorator command line argument to add function decorators
  in header files
- meson: Make orcc detectable from other subprojects
- meson: add options to disable tests, docs, benchmarks, examples, tools, etc.
- meson: misc. other fixes

* Fri Feb 14 2020 Anton Novojilov <andy@essentialkaos.com> - 0.4.28-0
- Numerous undefined behaviour fixes
- Ability to disable tests
- Fix meson dist behaviour

* Fri Feb 14 2020 Anton Novojilov <andy@essentialkaos.com> - 0.4.27-0
- sse: preserve non volatile sse registers, needed for MSVC
- x86: don't hard-code register size to zero in orc_x86_emit_*() functions
- Fix incorrect asm generation on 64-bit Windows when building with MSVC
- Support build using the Meson build system

* Fri Mar 24 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.26-0
- Initial build for kaos repository
