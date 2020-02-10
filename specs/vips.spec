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

################################################################################

Name:              vips
Summary:           C/C++ library for processing large images
Version:           8.9.1
Release:           0%{?dist}
License:           LGPLv2+
Group:             System Environment/Libraries
URL:               https://libvips.github.io/libvips/

Source0:           https://github.com/libvips/libvips/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make pkgconfig gettext libtool python-devel swig gtk-doc
BuildRequires:     gcc gcc-c++ libjpeg-turbo-devel libtiff-devel zlib-devel
BuildRequires:     glib2-devel libxml2-devel libexif-devel expat-devel

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.

################################################################################

%package devel
Summary:           Development files for %{name}
Group:             Development/Libraries
Requires:          libjpeg-turbo-devel libtiff-devel zlib-devel
Requires:          vips = %{version}-%{release}

%description devel
Package contains the header files and libraries necessary for developing
programs using VIPS. It also contains a C++ API and development man pages.

################################################################################

%package tools
Summary:           Command-line tools for %{name}
Group:             Applications/Multimedia
Requires:          vips = %{version}-%{release}

%description tools
Package contains command-line tools for working with VIPS.

################################################################################

%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Conflicts:         %{name} < %{version}-%{release}
Conflicts:         %{name} > %{version}-%{release}

%description doc
Package contains extensive documentation about VIPS in both HTML and
PDF formats.

################################################################################

%prep
%{crc_check}

%setup -q

find . -name 'CVS' -type d -print0 | xargs -0 rm -rf

export FAKE_BUILD_DATE=$(date -r %{SOURCE0})
sed -i "s/\\(IM_VERSION_STRING=\\)\$IM_VERSION-\`date\`/\\1\"\$IM_VERSION-$FAKE_BUILD_DATE\"/g" \
  configure
unset FAKE_BUILD_DATE

%build
%configure --disable-static --disable-gtk-doc --without-python
%{__make} %{?_smp_mflags} LIBTOOL=libtool

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} \( -name '*.la' -o -name '*.a' \) -exec rm -f {} ';'

rm -rf %{buildroot}%{_datadir}/doc/%{name}
rm -rf %{buildroot}%{_datadir}/locale

%post -p %{__ldconfig}

%postun -p %{__ldconfig}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc AUTHORS NEWS THANKS COPYING ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

################################################################################

%changelog
* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.9.1-0
- fix new_from_file for openslide from CLI and C
- fix thumbnail autorot
- fix a warning with magicksave with no delay array
- fix a race in tiled tiff load
- better imagemagick init
- lock for metadata changes, fixing a race in highly threaded applications

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.9.0-0
- add vips_image_get/set_array_int()
- disable webp alpha output if all frame fill the canvas and are solid
- support arrays of delays for animated images
- add "unlimited" flag to svgload
- disable webp alpha output if all frames fill the canvas and are solid
- add "compression" option to heifsave
- support webp and zstd compression in tiff
- loaders use "minimise" to close input files earlier
- integrate support for oss-fuzz
- add vips_switch() / vips_case() ... fast many-way ifthenelse
- better const handling for arithmetic operators fixes comparisons against out
  of range values
- sharpen restores input colourspace
- handle alpha in heifload / heifsave
- add @Interpretation and @Format to rawload
- nifti load/save uses double for all floating point metadata
- add vips_error_buffer_copy()
- add VipsSource and VipsTarget: a universal IO class for loaders and savers
- jpeg, png, tiff (though not tiffsave), rad, svg, ppm and webp use the new
  IO class
- rewritten ppm load/save is faster and uses less memory
- add @no_strip option to dzsave
- add iiif layout to dzsave
- fix use of resolution-unit metadata on tiff save
- support TIFF CIELAB images with alpha
- support TIFF with premultiplied alpha in any band
- block metadata changes on shared images
- RGB and sRGB are synonymous

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.4-0
- improve compatibility with older imagemagick versions
- remove realpath, since it can fail on systems with grsec
- block metadata changes on shared images

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.3-0
- revert sharpen restoring the input colourspace
- xres/yres tiffsave params were in pixels/cm

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.2-0
- better early shutdown in readers
- don't attempt to save large XMP to jpeg
- always fetch HEIC metadata from the main image
- fix loop in malformed ppm
- better support for PNGs with long comment names
- fix build with GM
- add locks for pdfium load
- fix build with MSVC
- fix a problem with shinkv tail processing
- fix a read one byte beyond buffer bug in jpegload
- make GIF parsing less strict
- better feof() handling in GIF load
- clip coding and interpretation on vips image read
- check image bounds for GIF load
- prevent over-pre-shrink in thumbnail
- fix sharpen with sigma 0.5
- sharpen restores input colourspace
- verify bands/format for coded images
- improve data_length handling for jpeg metadata

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.1-0
- improve realpath() use on older libc
- better magickload error messages
- more consistent behaviour for page-height metadata
- fix for composite with many small images and some combinations of blend modes
- fix memleak in tiff pyr save to memory
- istiff attempts to read the first directory rather than just testing
  the magic number
- much faster ismagick()
- better behaviour for vips_region_fetch() if request lies partly ouside image
- remove 256 band limit in arithmetic.c
- disable Orc if building with CET
- fix vipsthumbnail with pyr tiff
- text autofit could occasionally terminate early
- fewer warnings on tiffload
- vips_resize() breaks aspect ratio and limits shrink to prevent <1px dimensions

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.0-0
- much faster smartcrop
- add low/high to smartcrop
- add XMP support to png read/write
- deprecate thumbnail auto_rotate, add no_rotate
- implement thumbnail shrink-on-load for openslide images
- add animated webp support
- revise vips_cast() to improve behaviour with uint images
- add bandand()/or()/eor() to cplusplus binding
- implement shrink-on-load for tiff pyramids
- added vips_image_set_blob_copy()
- don't stop composite on first non-transparent image
- add vips_rect_overlapsrect()
- composite is much faster at positioning subimages
- stop tiff pyr layers if width or height drop to 1
- dzsave has a new skip_blanks option
- add vips_CMYK2XYZ() and vips_XYZ2CMYK(), plus associated routes
- include cmyk and srgb fallback profiles
- add vips_profile_load() and use it everywhere
- fix race in temp filename creation
- add @reduction_effort param to webpsave
- add @option_string param to thumbnail_buffer
- add XMP, IPCT, ICC, EXIF etc. support to magickload/magicksave
- much lower memuse for gifload
- tilecache speedups
- add vips_heifload(), vips_heifsave()
- add heif thumbnail support to vips_thumbnail()
- free threadpool earlier, reducing mem growth for some long-running processes
- add vips_region_fetch() / _width() / _height() for language bindings
- vips_text() supports justification
- move vips_image_set_kill() and iskilled() to the public API
- dzsave to szi sets suffix correctly
- dzsave szi writes "scan-properties.xml"
- add vips_image_(get|set)_image()
- add openslideload option to attach all associated images as metadata
- dzsave to szi will write all associated images
- remove old c++ and python interfaces
- vipsthumbnail can thumbnail animated and multipage images
- much better Windows build

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 8.7.4-0
- zero memory on allocate to prevent write of uninitialized memory under some
  error conditions

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 8.7.3-0
- fix infinite loop for autofit with non-scaleable font
- mapim was not offsetting by window offset
- better rounding for scale
- fix a memleak in magick6load

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.2-0
- more info output for temp files to help diagnose problems
- vips_text() could set the wrong DPI in autofit mode
- vips_text() leaked in autofit mode

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.1-0
- update function list in docs
- test for g_str_to_ascii()
- fix temp file open on Windows and fallback on linux

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.0-0
- add magicksave, save image with libMagick [dlemstra]
- remove jpeg thumbnail from EXIF if "jpeg-thumbnail-data" has been removed
  by user
- hough_line scales width to 0 - 180, not 0 - 360
- hough_line is 4x faster
- hough_circle is 2x faster
- add vips_sobel() and vips_canny() edge detectors
- add vips_rotate() ... a convenience method for vips_similarity()
- svgload was missing is_a [lovell]
- better header sniffing for small files
- drop incompatible ICC profiles before save
- better hasalpha rules
- create funcs always make MULTIBAND (ie. no alpha)
- use O_TMPFILE, if available [Alexander--]
- set "interlaced=1" for interlaced JPG and PNG images
- add PDFium PDF loader
- jpegload adds a jpeg-chroma-subsample field with eg. 4:4:4 for no
- chrominance subsampling.
- tiffload, pdfload, magickload set VIPS_META_N_PAGES "n-pages" metadata item
- add fontfile option to vips_text() [fangqiao]
- add vips_transpose3d() -- swap major dimensions in a volumetric image
- remove vips7 stuff from default API ... you must now #include it explicitly
- added vips_argument_get_id() to fix derived classes on win32 [angelmixu]
- fix compile with MSVC 2017 [angelmixu]
- pdfload has a option for background
- vips7 C++ interface defaults off
- make members, getters and operators "const" in cpp API
- composite has params for x/y position of sub-images [medakk]
- add Mitchell kernel
- pyramid builders have a choice of 2x2 shrinkers [harukizaemon]
- add palette option to pngsave [felixbuenemann]
- add basic nifti load/save support
- support writing string-valued fields via libexif
- paste in the test suite from pyvips
- get EXIF tag names from tag plus ifd [@Nan619]
- escape ASCII control characters in XML
- magickload now sniffs some file types itself

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.5-0
- fix a buffer overflow in the tiff reader

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.4-0
- better fitting of fonts with overhanging edges
- revise C++ example
- strict round down on jpeg shrink on load
- configure test for g++ 7.2 and composite.cpp
- don't Ping in magickload, too unreliable
- ensure WebP can add metadata when compiled with libwebpmux
- improve accuracy of vector path convolution

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.3-0
- the 8.6.3-1 windows builds fix a crash in libz configuation
- use pkg-config to find libjpeg, if we can
- better clean of output image in vips_image_write() fixes a crash writing
  twice to memory
- better rounding behaviour in convolution means we hit the vector path more
  often
- fix a crash if a delayed load failed [gsharpsh00ter]
- icc_import attaches the fallback profile if it used it, making vipsthumbnail
  behaviour with untagged CMYK images saner

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.2-0
- vips_sink_screen() keeps a ref to the input image ... stops a rare race
- fix a minor accidental ABI break in 8.6.0 -> 8.6.1
- fix read of plane-separate TIFFs with large strips
- fix a C++ warning in composite.cpp
- remove number of images limit in composite
- composite allows 1 mode ... reused for all joins
- fix race in vips_sink() for threaded read of sequential images

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.1-0
- fix mmap window new/free cycling
- fix some compiler warnings
- remove the 64-image limit on bandary operations
- better version date
- bump wrapper script version
- fix a memleak on error during jpeg buffer write
- fix misspelling of IPTC as IPCT
- seq could be set on small images opened in random-access mode
- fix small memleak in dzsave
- small speedup for rgb->g

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.0-0
- supports FITS images with leading non-image HDUs
- add vips_image_new_from_image() and vips_image_new_from_image1() ... make a
  constant image
- add new_from_image() to Python as well
- slight change to cpp new_from_image() to match py/C behaviour
- vips_conv(), vips_compass(), vips_convsep() default to FLOAT precision
- add FORCE resize mode to break aspect ratio
- add vips_thumbnail_image()
- better prefix guessing on Windows
- savers support a "page_height" option for multipage save
- rename 'disc' as 'memory' and default off
- add vips_find_trim(), search for non-background areas
- remove lcms1 support, it had bitrotted
- join tagged as seq
- support tiffsave_buffer for pyramids
- thumbnail and vipsthumbnail have an option for rendering intent
- kleisauke
- set file create time on Windows
- remove python tests ... moved to pyvips test suite
- vips7 and vips8 python bindings default to off ... use the new pyvips
- binding instead
- better svgload: larger output, handle missing width/height
- add vips_gravity() ... embed, but with direction rather than position
- vips_text() can autofit text to a box
- add vips_composite() / vips_composite2(): merge a set of images with
  a set of blend modes
- better gobject-introspection annotations
- vips_image_write() severs all links between images, when it can
- vector path for convolution is more accurate and can handle larger masks
  linear and cubic kernels for reduce are higher quality
- added vips_value_set_blob_free()
- "--size Nx" to vipsthumbnail was broken
- fix build with gcc 7
- add vips_fill_nearest() ... fill pixels with nearest colour
- add VIPS_COMBINE_MIN, a new combining mode for vips_compass()
- vips_hist_find_indexed() now has a @combine parameter
- vips_affine() and vips_similarity() have a "background" parameter
- fix nasty jaggies on the edges of affine output
- add gif-delay, gif-comment and gif-loop metadata
- add dispose handling to gifload
- dzsave outputs extra right and bottom overlap-only tiles, for closer spec
  adherence
- deprecate the "centre" option for vips_resize(): it's now always on
- setting the EXIF data block automatically sets other image tags
- add "extend" option to affine; resize uses it to stop black edges

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 8.5.9-0
- make --fail stop jpeg read on any libjpeg warning
- don't build enumtypes so often, removing perl as a compile dependency
- fix a crash with heavy use of draw operations from language bindings

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 8.4.5-0
- Updated to latest release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 8.4.2-0
- Updated to latest release

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.3-0
- Updated to latest release

* Sat Jul 23 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.1-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 7.42.1-0
- Updated to latest release

* Thu Aug 28 2014 Anton Novojilov <andy@essentialkaos.com> - 7.40.6-0
- Initial build
