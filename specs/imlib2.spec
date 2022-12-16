################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            Powerful image loading and rendering library
Name:               imlib2
Version:            1.9.1
Release:            0%{?dist}
License:            BSD
Group:              System Environment/Libraries
URL:                https://docs.enlightenment.org/api/imlib2/html

Source0:            https://prdownloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.xz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ zlib-devel freetype-devel

Requires:           zlib

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

################################################################################

%package devel
Summary:            Imlib2 headers, static libraries and documentation
Group:              Development/Libraries

Requires:           %{name} = %{version}
Requires:           pkgconfig(x11)

%description devel
Headers, static libraries and documentation for Imlib2.

################################################################################

%package filters
Summary:            Imlib2 basic plugin filters set
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description filters
Basic set of plugin filters that come with Imlib2.

################################################################################

%package loader_lbm
Summary:            Imlib2 LBM loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_lbm
LBM image loader/saver for Imlib2.

################################################################################

%package loader_jpeg
Summary:            Imlib2 JPEG loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}
Requires:           libjpeg-turbo

BuildRequires:      libjpeg-turbo-devel

%description loader_jpeg
JPEG image loader/saver for Imlib2.

################################################################################

%package loader_png
Summary:            Imlib2 PNG loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}
Requires:           libpng zlib

BuildRequires:      libpng-devel zlib-devel

%description loader_png
PNG image loader/saver for Imlib2.

################################################################################

%package loader_argb
Summary:            Imlib2 ARGB loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_argb
ARGB image loader/saver for Imlib2.

################################################################################

%package loader_bmp
Summary:            Imlib2 BMP loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_bmp
BMP image loader/saver for Imlib2.

################################################################################

%package loader_ff
Summary:            Imlib2 Farbfeld loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_ff
Farbfeld image loader/saver for Imlib2.

################################################################################

%package loader_gif
Summary:            Imlib2 GIF loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}
Requires:           giflib

BuildRequires:      giflib-devel

%description loader_gif
GIF image loader for Imlib2.

################################################################################

%package loader_ico
Summary:            Imlib2 ICO loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_ico
ICO image loader for Imlib2.

################################################################################

%package loader_pnm
Summary:            Imlib2 PNM loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_pnm
PNM image loader/saver for Imlib2.

################################################################################

%package loader_tga
Summary:            Imlib2 TGA loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_tga
TGA image loader/saver for Imlib2.

################################################################################

%package loader_tiff
Summary:            Imlib2 TIFF loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}
Requires:           libtiff

BuildRequires:      libtiff-devel

%description loader_tiff
TIFF image loader/saver for Imlib2.

################################################################################

%package loader_xpm
Summary:            Imlib2 XPM loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_xpm
XPM image loader/saver for Imlib2.

################################################################################

%package loader_xbm
Summary:            Imlib2 XBM loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_xbm
XBM image loader/saver for Imlib2.

################################################################################

%package loader_bz2
Summary:            Imlib2 .bz2 loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

BuildRequires:      bzip2-devel

%description loader_bz2
Bzip2 compressed image loader/saver for Imlib2.

################################################################################

%package loader_gz
Summary:            Imlib2 .gz loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}

%description loader_gz
gz compressed image loader/saver for Imlib2.

################################################################################

%package loader_id3
Summary:            Imlib2 .id3 loader
Group:              System Environment/Libraries

Requires:           %{name} = %{version}
Requires:           libid3tag

BuildRequires:      libid3tag-devel

%description loader_id3
id3 tag image loader/saver for Imlib2.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{configure} --prefix=%{_prefix} \
%ifarch x86_64
    --disable-mmx \
%endif
%ifarch i386 i486 i586 i686
    --enable-mmx \
%endif
    --without-x \
    --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/%{name}/filters/*.a
rm -f %{buildroot}%{_libdir}/%{name}/loaders/*.a

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING-PLAIN README
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/loaders
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/%{name}/*/*.la
%exclude %{_libdir}/*.la
%{_bindir}/%{name}_*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_datadir}/%{name}

%files filters
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}/filters
%attr(755,root,root) %{_libdir}/%{name}/filters/*.so

%files loader_lbm
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/lbm.so

%files loader_jpeg
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/jpeg.so

%files loader_png
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/png.so

%files loader_argb
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/argb.so

%files loader_bmp
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/bmp.so

%files loader_ff
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/ff.so

%files loader_gif
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/gif.so

%files loader_ico
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/ico.so

%files loader_pnm
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/pnm.so

%files loader_tga
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/tga.so

%files loader_tiff
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/tiff.so

%files loader_xpm
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/xpm.so

%files loader_xbm
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/xbm.so

%files loader_bz2
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/bz2.so

%files loader_gz
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/zlib.so

%files loader_id3
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/id3.so

################################################################################

%changelog
* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- x11_color: Simplify and fix error paths
- JPEG loader: Use mmap'ed file access
- modules: Eliminate __imlib_TrimLoaderList()
- Introduce strsplit()
- modules: Cosmetics, mostly
- modules: Enable setting multiple loader/filter paths
- test: Add test_misc
- modules: Fix signdness warning
- TIFF loader: Change default save compression type
- imlib2_load: Remove unused macro
- imlib2_conv: Cosmetic changes
- imlib2_conv: Drop obsolete .db stuff, simplify
- imlib2_conv: Enable passing attached data to saver v1.9.1
- check for some alloc failures
- check for alloc failures some more
- modules: check for filepath truncation

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- GIF loader: Don't close file descriptor twice
- Introduce imlib_load_image_from_fd()
- Don't rescan loaders
- XPM loader: Major speedup for cpp > 2
- imlib2_load: Properly check non-full loads (load data too)
- imlib2_load: Use getopt()
- imlib2_load: Add repeated load option
- Simplify __imlib_FileExtension()
- Refactor many __imlib_File...() functions to use common __imlib_FileStat()
- Drop the __imlib_IsRealFile() file check in __imlib_File...() functions
- image.c: Add some space for readability
- image.c: Remove some unnecessary clearing of calloc'ed structs
- image.c: Rework some obscure file name stuff in __imlib_SaveImage()
- image.c: Don't strdup() real_name when not necessary in __imlib_LoadImage()
- image.c: Use real_file to get file time
- image.c: Introduce __imlib_ErrorFromErrno()
- image.c: Use loader return value, not im->w to determine load success
- Loader cleanups
- Saver cleanups
- image.c/h: Cleanups
- image.c: Move image tag functions to separate file
- image.c: Move loader functions to separate file
- image.c: Enable non-dirty pixmap cache cleaning
- image.c: Minor refactoring of pixmap cache cleaners
- image.c: Move data_memory_func assignment to better place
- imlib2_view: Various tweaks
- Fix loader cleanup breakage (gif)
- image.c: Remove redundant pixmap unref
- image.c: Add infrastructure to simplify progress handling
- Loaders: Simplify/fix progress handling
- Savers: Simplify progress handling
- Introduce __imlib_LoadEmbedded()
- Introduce __imlib_LoaderSetFormats()
- Make ImlibLoader struct opaque
- autogen.sh: Add -n as alternative to NOCONFIGURE
- Fix enum conversion warnings (gcc10)
- JPG, PNG loaders: Avoid clobber warnings
- Add a couple of consts
- TIFF loader: Minor speedup
- ID3 loader: Some mostly cosmetic rearrangements
- GZ, BZ2 loaders: Accept more file names
- __imlib_FileExtension: Use basename if there are no dots
- Revert "JPG, PNG loaders: Avoid clobber warnings"
- JPG, PNG loaders: Avoid clobber warnings - Take N+1
- Add infrastructure for new loader entry - load2()
- Move loaders to load2()
- Reduce number of stat() calls during load
- configure.ac: Drop initial config.cache removal
- imlib2_load: Optionally use imlib_load_image_fd()
- Fix build without X11
- Remove a couple of unused includes
- ICO loader: Do not crash on invalid files
- ICO loader: Handle malloc failures

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- gz loader: Use FILE, not fd
- gz, bz2 loaders: Fix recent breakage when file name has more than two dots
- Quit on 'q' or 'esc' key press in all imlib2_... test utilities
- Rename imlib2_test_load to imlib2_load
- imlib2_load: Optionally write to stderr instead of stdout
- imlib2_view: Add progress debug options
- Enable specifying loader/filter paths with environment variables
- BMP loader: Remove some bogus conditions
- XPM loader: Minor optimization for cpp > 2
- LBM loader: Fix header-only loading
- BMP loader: Fix size calculation when saving files

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Allow to use custom memory management functions for loaded images
- Add __imlib_LoadImageWrapper() handling all load() calls
- imlib2_conv: Report error on save failure
- Autofoo cosmetics
- Trivial cleanups in imlib2_... test programs
- Add imlib2_test_load program
- Cleanups in load() functions
- Centralize handling of im->format
- Sort loaders in Makefile.am
- Remove obsolete dmalloc stuff
- Move SWAP.. macro definitions to common.h
- Use common PIXEL_ARGB() macro to compose pixels
- Add new ICO loader
- Spec file simlifications and cleanups
- Fix memory leak in imlib_list_fonts()
- XPM loader: Refactor exit cleanup handling
- XPM loader: Fix potentially uninitialized pixel data
- XPM loader: Fixup after "Refactor exit cleanup handling"
- Revert "XPM loader: Fix potentially uninitialized pixel data"
- XPM loader: Cosmetics (reduce indent level)
- XPM loader: Fix several colormap issues
- XPM loader: Simplify pixel value handling
- XPM loader: Add missing pixels (malformed xpm)
- XPM loader: More simplifications
- JPG loader: Refactor
- JPG loader: Do proper CMYK conversion
- Add new WebP loader
- Remove pointless im->data checks in loaders
- WepP loader: Fix memory leak in error path
- JPG loader: Fix memory leaks in error paths
- Fix ABI break
- ICO loader: Add binary flag to fopen()
- JPG loader: Refactor error handling
- Rename/add byte swap macros
- BMP loader: Major makeover - numerous bug fixes and feature enhancements
- Miscellaneous imlib_test_load tweaks
- GZIP loader: Check filename before uncompress
- imlib2_test_load: Fixup after recent change
- Re-indent everything using indent-2.2.12
- TGA loader: Refactor
- Eliminate WRITE_RGBA()
- Simplify autogen.sh
- Simplify pixel color handling in api.c
- Use pixel instead of r,b,g,a in __imlib_render_str()
- Use macro for pixel color access in savers
- Eliminate READ_RGBA()
- XPM loader: Accept signature not at the very start of the file
- Simplify loader lookup functions
- imlib2_view: Enable selecting next/prev using keys too
- imlib2_view: Fix event processing bug
- imlib2_test_load: Fixup recent breakage for real
- imlib2_test_load: Check progress conditionally
- imlib2_view: Add verbose option, quit on Escape too
- TGA loader - Mostly cosmetic refactoring
- TGA loader: More mostly cosmetic changes
- TGA loader: Support horiontal flip
- TGA loader: Add simple 16 bpp handling
- TGA loader: Tweak error handling
- ICO loader: Fix non-immediate loading
- Remove __imlib_AllocateData() w,h args
- imlib2_view: Fix next/prev selection if last/first image is bad
- ICO loader: Fix memory leak in error path
- XPM loader: Correct signature check (avoid accessing unset data)
- gz, bz2 loaders: Simplify, eliminate unnecessary strdups, cosmetics
- Check filename before opening archive file.
- tga loader: implement handling of palette

* Tue Apr 12 2016 Gleb Goncharov <yum@gongled.ru> - 1.4.8-0
- Initial build for kaos repo
