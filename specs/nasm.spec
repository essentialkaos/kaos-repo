################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            A portable x86 assembler which uses Intel-like syntax
Name:               nasm
Version:            2.15.05
Release:            0%{?dist}
License:            BSD
Group:              Development/Languages
URL:                https://www.nasm.us

Source0:            https://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}.tar.bz2
Source1:            https://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.bz2

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc perl(Env) xmlto

Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

################################################################################

%package rdoff
Summary:            Tools for the RDOFF binary format, sometimes used with NASM
Group:              Development/Languages

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM). These tools
include linker, library manager, loader, and information dump.

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

%{make_install} install_rdf

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

%files rdoff
%defattr(-,root,root,-)
%{_bindir}/ldrdf
%{_bindir}/rdf2bin
%{_bindir}/rdf2ihx
%{_bindir}/rdf2com
%{_bindir}/rdfdump
%{_bindir}/rdflib
%{_bindir}/rdx
%{_bindir}/rdf2ith
%{_bindir}/rdf2srec
%{_mandir}/man1/rd*
%{_mandir}/man1/ld*

################################################################################

%changelog
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
