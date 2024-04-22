################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:          A portable x86 assembler which uses Intel-like syntax
Name:             nasm
Version:          2.16.02
Release:          0%{?dist}
License:          BSD
Group:            Development/Languages
URL:              https://www.nasm.us

Source0:          https://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}.tar.bz2
Source1:          https://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.bz2

Source100:        checksum.sha512

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    make gcc perl(Env) xmlto

Requires(post):   info
Requires(preun):  info

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

################################################################################

%prep
%{crc_check}

%setup -q

tar xjf %{SOURCE1} --strip-components 1

%build
%configure

%{__make} all %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%{make_install}

%clean
rm -rf %{buildroot}

%post
if [[ -e %{_infodir}/nasm.info.gz ]] ; then
  /sbin/install-info %{_infodir}/nasm.info.gz  %{_infodir}/dir || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  if [[ -e %{_infodir}/nasm.info.gz ]] ; then
    /sbin/install-info --delete %{_infodir}/nasm.info.gz %{_infodir}/dir || :
  fi
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE CHANGES README.md
%{_bindir}/nasm
%{_bindir}/ndisasm
%{_mandir}/man1/nasm*
%{_mandir}/man1/ndisasm*

################################################################################

%changelog
* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.16.02-0
- Fix building from the source distribution in a separate directory from
  the source.
- Fix a number of issues when building from source, mostly involving configure
  or dependency generation.
- In particular, more aggressively avoid cross-compilation problems on
  Unix/Linux systems automatically invoking WINE. We could end up invoking WINE
  even when we didn't want to, making configure think it was running native when
  in fact cross-compiling.
- Hopefully fix compiling with the latest versions of MSVC/nmake.
- Windows host: add embedded manifest file. Without a manifest, Windows
  applications force a fixed PATH_MAX limit to any pathname; this is
  unnecessary.
- Add support VEX-encoded SM4-NI instructions.
- Add support for VEX-encoded SM3-NI instructions.
- Add support for VEX-encoded SHA512-NI instructions.
- PTWRITE opcode corrected (F3 prefix required.)
- Disassembler: the SMAP instructions are NP; notably the prefixed versions
  of CLAC are ERETU/ERETS.
- Add support for Flexible Return and Exception Delivery (FRED): the LKGS,
  ERETS and ERETU instructions.
- Fix external references to segments in the obj (OMF) and possibly other
  output formats.
- Always support up to 8 characters, i.e. 64 bits, in a string-to-numeric
  conversion.
- Preprocessor: add %%map() function to expand a macro from a list of arguments,
  see section 4.4.7.
- Preprocessor: allow the user to specify the desired radix for an evaluated
  parameter. It doesn't make any direct difference, but can be nice for
  debugging or turning into strings. See the = modifier in section 4.2.1.
- Update documentation: __USE_package__ is now __?USE_package?__.
- Documentation: correct a minor problem in the expression grammar for Dx
  statements, see section 3.2.1.
- Preprocessor: correctly handle empty %%rep blocks.
- Preprocessor: add options for a base prefix to %%num(), see section 4.4.8.
- Preprocessor: add a %%hex() function, equivalent to %%eval() except that it
  producess hexadecimal values that are nevertheless valid NASM numeric
  constants, see section 4.4.5.
- Preprocessor: fix the parameter number in error messages (should be 1-based,
  like %%num references to multi-line macro arguments.)
- Documentation: be more clear than the bin format is simply a linker built into
  NASM. See section 8.1.
- Adjust the LOCK prefix warning for XCHG.
- LOCK XCHG reg,mem would issue a warning for being unlockable, which
  is incorrect. In this case the reg,mem encoding is simply an alias for the
  mem,reg encoding. However, XCHG is always locked, so create a new warning
  (-w+prefix-lock-xchg) to explicitly flag a user-specified LOCK XCHG; default
  off. Future versions of NASM may remove the LOCK prefix when optimization
  is enabled.
- Fix broken dependency-list generation.
- Add optional warnings for specific relocation types (-w+reloc-*, see
  appendix A), default off.
- Some target environments may have specific restrictions on what kinds of
  relocations are possible or allowed.
- Error out on certain bad syntax in Dx statements, such as db 1 2. See
  section 3.2.1.

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.16.01-0
- Support for the rdf format has been discontinued and all the RDOFF utilities
  has been removed.
- The --reproducible option now leaves the filename field in the COFF object
  format blank. This was always rather useless since it is only 18 characters
  long; as such debug formats have to carry their own filename information
  anyway.
- Fix handling of MASM-syntax reserved memory (e.g. dw ?) when used in
  structure definitions.
- The preprocessor now supports functions, which can be less verbose and more
  convenient than the equivalent code implemented using directives.
- Fix the handling of %%00 in the preprocessor.
- Fix incorrect handling of path names affecting error messages, dependency
  generation, and debug format output.
- Support for the RDOFF output format and the RDOFF tools have been removed. The
  RDOFF tools had already been broken since at least NASM 2.14. For flat code
  the ELF output format recommended; for segmented code the obj (OMF) output
  format.
- New facility: preprocessor functions. Preprocessor functions, which are
  expanded similarly to single-line macros, can greatly simplify code that in
  the past would have required a lengthy list of directives and intermediate
  macros.
- Single-line macros can now declare parameters (using a && prefix) that creates
  a quoted string, but does not requote an already quoted string.
- Instruction table updated per public information available as of
  November 2022.
- All warnings in the preprocessor have now been assigned warning classes.
- Fix the invalid use of RELA–type relocations instead of REL–type relocations
  when generating DWARF debug information for the elf32 output format.
- Fix the handling at in istruc when the structure contains local labels.
- When assembling with --reproducible, don't encode the filename in the COFF
  header for the coff, win32 or win64 output formats. The COFF header only has
  space for an 18-character filename, which makes this field rather useless
  in the first place. Debug output data, if enabled, is not affected.
- Fix incorrect size calculation when using MASM syntax for non-byte
  reservations (e.g. dw ?.)
- Allow forcing an instruction in 64-bit mode to have a (possibly redundant)
  REX prefix, using the syntax {rex} as a prefix.
- Add a {vex} prefix to enforce VEX (AVX) encoding of an instruction, either
  using the 2- or 3-byte VEX prefixes.
- The CPU directive has been augmented to allow control of generation of
  VEX (AVX) versus EVEX (AVX-512) instruction formats, see section 7.11.
- Some recent instructions that previously have been only available using EVEX
  encodings are now also encodable using VEX (AVX) encodings. For backwards
  compatibility these encodings are not enabled by default, but can be generated
  either via an explicit {vex} prefix or by specifying either CPU LATEVEX or
  CPU NOEVEX.
- Document the already existing %%unimacro directive.
- Fix a code range generation bug in the DWARF debug format (incorrect
  information in the DW_AT_high_pc field) for the ELF output formats. This bug
  happened to cancel out with a bug in older versions of the GNU binutils
  linker, but breaks with other linkers and updated or other linkers that expect
  the spec to be followed.
- Fix segment symbols with addends, e.g. jmp _TEXT+10h:0 in output formats that
  support segment relocations, e.g. the obj format.
- Fix various crashes and hangs on invalid input.

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 2.15.05-0
- Correct %%ifid $ and %%ifid $$ being treated as true.
- Add --reproducible option to suppress NASM version numbers and timestamps
 in output files.

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.14.02-0
- Fix crash due to multiple errors or warnings during the code generation pass
  if a list file is specified

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.14.01-0
- Create all system-defined macros defore processing command-line given
  preprocessing directives (-p, -d, -u, --pragma, --before).
- If debugging is enabled, define a __DEBUG_FORMAT__ predefined macro.
- Fix an assert for the case in the obj format when a SEG operator refers to an
  EXTERN symbol declared further down in the code.
- Fix a corner case in the floating-point code where a binary, octal or
  hexadecimal floating-point having at least 32, 11, or 8 mantissa digits could
  produce slightly incorrect results under very specific conditions.
- Support -MD without a filename, for gcc compatibility. -MF can be used to set
  the dependencies output filename.
- Fix -E in combination with -MD.
- Fix missing errors on redefined labels; would cause convergence failure
  instead which is very slow and not easy to debug.
- Duplicate definitions of the same label with the same value is now explicitly
  permitted (2.14 would allow it in some circumstances.)
- Add the option --no-line to ignore %%line directives in the source.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.14-0
- Changed -I option semantics by adding a trailing path separator
  unconditionally.
- Fixed null dereference in corrupted invalid single line macros.
- Fixed division by zero which may happen if source code is malformed.
- Fixed out of bound access in processing of malformed segment override.
- Fixed out of bound access in certain EQU parsing.
- Fixed buffer underflow in float parsing.
- Added SGX (Intel Software Guard Extensions) instructions.
- Added +n syntax for multiple contiguous registers.
- Fixed subsections_via_symbols for macho object format.
- Added the --gprefix, --gpostfix, --lprefix, and --lpostfix command line
  options, to allow command line base symbol renaming.
- Allow label renaming to be specified by %%pragma in addition to from the
  command line.
- Supported generic %%pragma namespaces, output and debug.
- Added the --pragma command line option to inject a %%pragma directive.
- Added the --before command line option to accept preprocess statement before
  input.
- Added AVX512 VBMI2 (Additional Bit Manipulation), VNNI (Vector Neural
  Network), BITALG (Bit Algorithm), and GFNI (Galois Field New Instruction)
  instructions.
- Added the STATIC directive for local symbols that should be renamed using
  global-symbol rules.
- Allow a symbol to be defined as EXTERN and then later overridden as GLOBAL
  or COMMON. Furthermore, a symbol declared EXTERN and then defined will
  be treated as GLOBAL.
- The GLOBAL directive no longer is required to precede the definition of
  the symbol.
- Support private_extern as macho specific extension to the GLOBAL directive.
- Updated UD0 encoding to match with the specification
- Added the --limit-X command line option to set execution limits.
- Updated the Codeview version number to be aligned with MASM.
- Added the --keep-all command line option to preserve output files.
- Added the --include command line option, an alias to -P.
- Added the --help command line option as an alias to -h.
- Added -W, -D, and -Q suffix aliases for RET instructions so the operand
  sizes of these instructions can be encoded without using o16, o32 or o64.
