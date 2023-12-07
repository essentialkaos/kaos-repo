################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        The compression and decompression library
Name:           zlib
Version:        1.3
Release:        0%{?dist}
License:        zlib and Boost
Group:          System Environment/Libraries
URL:            https://www.zlib.net

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://www.zlib.net/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRequires:  make automake autoconf libtool

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

################################################################################

%package devel

Summary:  Header files and libraries for Zlib development
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

################################################################################

%package static

Summary:  Static libraries for Zlib development
Group:    Development/Libraries

Requires:  %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

################################################################################

%package -n minizip

Summary:  Library for manipulation with .zip archives
Group:    System Environment/Libraries

Requires:  %{name} = %{version}-%{release}

%description -n minizip
Minizip is a library for manipulation with files from .zip archives.

################################################################################

%package -n minizip-devel

Summary:  Development files for the minizip library
Group:    Development/Libraries

Requires:  minizip = %{version}-%{release}
Requires:  %{name}-devel = %{version}-%{release}

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

################################################################################

%prep
%{crc_check}

%setup -q

iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog.tmp
mv ChangeLog.tmp ChangeLog

%build
export CFLAGS="%{optflags}"
export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"

./configure --libdir=%{_libdir} \
            --includedir=%{_includedir} \
            --prefix=%{_prefix}

%{__make} %{?_smp_mflags}

pushd contrib/minizip
  autoreconf --install
  %configure --enable-static=no
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install}

pushd contrib/minizip
  %{make_install}
popd

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_includedir}/minizip/crypt.h

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post -n minizip
/sbin/ldconfig

%postun -n minizip
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/algorithm.txt test/example.c
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

################################################################################

%changelog
* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 1.3-0
- Building using K&R (pre-ANSI) function definitions is no longer supported
- Fixed a bug in deflateBound() for level 0 and memLevel 9
- Fixed a bug when gzungetc() is used immediately after gzopen()
- Fixed a bug when using gzflush() with a very small buffer
- Fixed a crash when gzsetparams() is attempted for a transparent write
- Fixed test/example.c to work with FORCE_STORED
- Fixed minizip to allow it to open an empty zip file
- Fixed reading disk number start on zip64 files in minizip
- Fixed a logic error in minizip argument processing

* Thu Oct 27 2022 Anton Novojilov <andy@essentialkaos.com> - 1.2.13-0
- Fix a bug when getting a gzip header extra field with inflateGetHeader().
  This remedies CVE-2022-37434.
- Fix a bug in block type selection when Z_FIXED used. Now the smallest block
  type is selected, for better compression.
- Fix a configure issue that discarded the provided CC definition.
- Correct incorrect inputs provided to the CRC functions. This mitigates a
  bug in Java.
- Repair prototypes and exporting of the new CRC functions.
- Fix inflateBack to detect invalid input with distances too far.

* Thu Oct 27 2022 Anton Novojilov <andy@essentialkaos.com> - 1.2.12-0
- Fix a deflate bug when using the Z_FIXED strategy that can result in
  out-of-bound accesses.
- Fix a deflate bug when the window is full in deflate_stored().
- Speed up CRC-32 computations by a factor of 1.5 to 3.
- Use the hardware CRC-32 instruction on ARMv8 processors.
- Speed up crc32_combine() with powers of x tables.
- Add crc32_combine_gen() and crc32_combine_op() for fast combines.

* Wed Jun 05 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.11-0
- Initial build for kaos repository
