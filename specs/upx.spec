################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Ultimate Packer for eXecutables
Name:           upx
Version:        4.0.1
Release:        0%{?dist}
License:        GPLv2+ and Public Domain
Group:          Applications/Archiving
URL:            https://upx.github.io

Source0:        https://github.com/upx/upx/releases/download/v%{version}/%{name}-%{version}-src.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} <= 7
BuildRequires:  cmake3 devtoolset-9-gcc-c++ devtoolset-9-binutils
%else
BuildRequires:  cmake gcc-c++
%endif

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
UPX is a free, portable, extendable, high-performance executable
packer for several different executable formats. It achieves an
excellent compression ratio and offers very fast decompression. Your
executables suffer no memory overhead or other drawbacks.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}-src

%build
%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from DevToolSet 9
export PATH="/opt/rh/devtoolset-9/root/usr/bin:$PATH"
%endif

mkdir -p build/release
cd build/release
cmake3 ../..
cmake3 --build .

%install
rm -rf %{buildroot}

install -Dpm 644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -Dpm 755 build/release/%{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING LICENSE README README.SRC THANKS doc/*.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Wed Nov 23 2022 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- bug fixes - see https://github.com/upx/upx/milestone/8

* Wed Nov 23 2022 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Switch to semantic versioning
- SECURITY NOTES: emphasize the security context in the docs
- Support easy building from source code with CMake
- Support easy rebuilding the stubs from source with Podman/Docker
- Add integrated doctest C++ testing framework
- Add support for EFI files (PE x86; Kornel Pal)
- win32/pe and win64/pe: set correct SizeOfHeaders in the PE header
- bug fixes - see https://github.com/upx/upx/milestone/6
- bug fixes - see https://github.com/upx/upx/milestone/7

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 3.96-0
- bug fixes

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 3.95-0
- Flag --android-shlib to work around bad design in Android
- Flag --force-pie when ET_DYN main program is not marked as DF_1_PIE
- Better compatibility with varying layout of address space on Linux
- Support for 4 PT_LOAD layout in ELF generated by binutils-2.31
- bug fixes, particularly better diagnosis of malformed input

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.94-0
- Add support for arm64-linux (aka "aarch64").
- Add support for --lzma compression on 64-bit PowerPC (Thierry Fauck).
- For Mach, "upx -d" will unpack a prefix of the file (and warn).
- Various improvements to the ELF formats.
- bug fixes

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 3.93-0
- Fixed some win32/pe and win64/pe regressions introduced in 3.92
- bug fixes

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.92-0
- IMPORTANT: all PE formats: internal changes: reunited the diverged source
  files - please report all regressions into the bug tracker and try UPX 3.91
  in case of problems.
- Support Apple MacOS 10.12 "Sierra", including more-robust de-compression.
- Explicitly diagnose Go-language bad PT_LOAD; recommend hemfix.c.
- Fix CERT-FI Case 829767 UPX command line tools segfaults.
- bug fixes

* Tue May 06 2014 Anton Novojilov <andy@essentialkaos.com> - 3.91-0
- Initial build for kaos repository
