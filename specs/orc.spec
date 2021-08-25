################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global _vpath_srcdir   .
%global _vpath_builddir %{_target_platform}

################################################################################

Summary:         The Oil Run-time Compiler
Name:            orc
Version:         0.4.31
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         BSD
URL:             https://gitlab.freedesktop.org/gstreamer/orc

Source0:         https://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   meson gcc gtk-doc

Provides:        %{name} = %{version}-%{release}

################################################################################

%package doc
Summary:         Documentation for Orc
Group:           Development/Languages

BuildArch:       noarch

Requires:        %{name} = %{version}-%{release}

%description doc
Documentation for Orc.

################################################################################

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

################################################################################

%package devel
Summary:         Development files and static libraries for Orc
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}
Requires:        %{name}-compiler pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

################################################################################

%package compiler
Summary:         Orc compiler
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description compiler
The Orc compiler, to produce optimized code.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%meson
%meson_build

%install
rm -rf %{buildroot}

%meson_install

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

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/%{name}/

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/%{name}-0.4.pc
%{_libdir}/pkgconfig/%{name}-test-0.4.pc
%{_datadir}/aclocal/%{name}.m4

%files compiler
%defattr(-,root,root,-)
%{_bindir}/orcc

################################################################################

%changelog
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
