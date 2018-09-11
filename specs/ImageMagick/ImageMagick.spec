################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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

%define patchlevel        11

################################################################################

Summary:            Use ImageMagick to create, edit, compose, or convert bitmap images
Name:               ImageMagick
Version:            6.9.10
Release:            %{patchlevel}%{?dist}
License:            ASL 2.0 and ERPL
Group:              Applications/Multimedia
URL:                https://www.imagemagick.org

Source0:            https://www.imagemagick.org/download/%{name}-%{version}-%{patchlevel}.tar.bz2
Source1:            policy.xml

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++
BuildRequires:      bzip2-devel freetype-devel libjpeg-devel libpng-devel
BuildRequires:      libtiff-devel giflib-devel zlib-devel perl-devel >= 5.8.1
BuildRequires:      ghostscript-devel djvulibre-devel
BuildRequires:      libwmf-devel libX11-devel libXext-devel libXt-devel
BuildRequires:      lcms2-devel libxml2-devel librsvg2-devel OpenEXR-devel
BuildRequires:      fftw-devel OpenEXR-devel libwebp-devel
BuildRequires:      openjpeg2-devel >= 2.1.0
BuildRequires:      autoconf automake libtool-ltdl-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
ImageMagick® is a software suite to create, edit, compose, or convert bitmap
images. It can read and write images in a variety of formats (over 200)
including PNG, JPEG, JPEG-2000, GIF, TIFF, DPX, EXR, WebP, Postscript, PDF,
and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and
transform images, adjust image colors, apply various special effects, or draw
text, lines, polygons, ellipses and Bézier curves.

The functionality of ImageMagick is typically utilized from the command-line or
you can use the features from programs written in your favorite language. Choose
from these interfaces: G2F (Ada), MagickCore (C), MagickWand (C), ChMagick (Ch),
ImageMagickObject (COM+), Magick++ (C++), JMagick (Java), L-Magick (Lisp),
Lua (LuaJIT), NMagick (Neko/haXe), Magick.NET (.NET), PascalMagick (Pascal),
PerlMagick (Perl), MagickWand for PHP (PHP), IMagick (PHP),
PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a language
interface, use ImageMagick to modify or create images dynamically and
automagically.

################################################################################

%package devel

Summary:            Library links and header files for ImageMagick application development
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           %{name}-libs = %{version}-%{release}

Requires:           libX11-devel libXext-devel libXt-devel ghostscript-devel
Requires:           bzip2-devel freetype-devel libtiff-devel libjpeg-devel
Requires:           lcms2-devel libwebp-devel OpenEXR-devel openjpeg2-devel
Requires:           pkgconfig

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

################################################################################

%package libs

Summary:            ImageMagick libraries to link with
Group:              Applications/Multimedia

%description libs
This packages contains a shared libraries to use within other applications.

################################################################################

%package djvu
Summary:            DjVu plugin for ImageMagick
Group:              Applications/Multimedia
Requires:           %{name}-libs = %{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.

################################################################################

%package doc
Summary:            ImageMagick HTML documentation
Group:              Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in HTML format.
Note this documentation can also be found on the ImageMagick website:
https://www.imagemagick.org/.

################################################################################

%package perl

Summary:            ImageMagick perl bindings
Group:              System Environment/Libraries

Requires:           %{name}-libs = %{version}-%{release}
Requires:           perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.

################################################################################

%package c++

Summary:            ImageMagick Magick++ library (C++ bindings)
Group:              System Environment/Libraries

Requires:           %{name}-libs = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.

################################################################################

%package c++-devel

Summary:            C++ bindings for the ImageMagick library
Group:              Development/Libraries

Requires:           %{name}-c++ = %{version}-%{release}
Requires:           %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.

You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.

################################################################################

%prep
%setup -qn %{name}-%{version}-%{patchlevel}

# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --with-perl \
           --with-x \
           --with-threads \
           --with-magick_plus_plus \
           --with-wmf \
           --with-webp \
           --with-openexr \
           --with-rsvg \
           --with-xml \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
           --without-dps \
           --without-gcc-arch \
           --without-gslib \
           --with-openjp2

# perfecto:absolve 1
%{__make}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{version}
rm %{buildroot}%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod -f 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/*/*.so

# perlmagick: fix perl path of demo files
perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" | xargs rm -f
find %{buildroot} -name ".packlist" | xargs rm -f
find %{buildroot} -name "perllocal.pod" | xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find %{buildroot}%{_libdir}/perl* -type f -print \
        | sed "s@^%{buildroot}@@g" > perl-pkg-files
find %{buildroot}%{perl_vendorarch} -type d -print \
        | sed "s@^%{buildroot}@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files
if [[ -z perl-pkg-files ]] ; then
  echo "ERROR: EMPTY FILE LIST"
  exit -1
fi

# fix multilib issues: Rename provided file with platform-bits in name.
# Create platform independant file inplace of provided and conditionally include required.
# $1 - filename.h to process.
function multilibFileVersions(){
mv $1 ${1%%.h}-%{__isa_bits}.h

local basename=$(basename $1)

cat >$1 <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "${basename%%.h}-32.h"
#elif __WORDSIZE == 64
# include "${basename%%.h}-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF
}

multilibFileVersions %{buildroot}%{_includedir}/%{name}-6/magick/magick-config.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-6/magick/magick-baseconfig.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-6/magick/version.h

# Replace default policy file by safe one
cat %{SOURCE1} > %{buildroot}%{_sysconfdir}/%{name}-6/policy.xml

%clean
rm -rf %{buildroot}

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}

%{__make} %{?_smp_mflags} check

%post libs
/sbin/ldconfig

%post c++
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%postun c++
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog Platforms.txt
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%defattr(-,root,root,-)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickCore-6.Q16.so*
%{_libdir}/libMagickWand-6.Q16.so*
%{_libdir}/%{name}-%{version}
%{_datadir}/%{name}-6
%exclude %{_libdir}/%{name}-%{version}/modules-Q16/coders/djvu.*
%dir %{_sysconfdir}/%{name}-6
%config(noreplace) %{_sysconfdir}/%{name}-6/*.xml

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore-6.Q16.so
%{_libdir}/libMagickWand-6.Q16.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-6.Q16.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-6.Q16.pc
%{_libdir}/pkgconfig/Wand.pc
%{_libdir}/pkgconfig/Wand-6.Q16.pc
%dir %{_includedir}/%{name}-6
%{_includedir}/%{name}-6/magick
%{_includedir}/%{name}-6/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%files djvu
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{version}/modules-Q16/coders/djvu.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-6
%doc %{_datadir}/doc/%{name}-%{version}
%doc LICENSE

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-6.Q16.so.*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}-6/Magick++
%{_includedir}/%{name}-6/Magick++.h
%{_libdir}/libMagick++-6.Q16.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_libdir}/pkgconfig/ImageMagick++-6.Q16.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

################################################################################

%changelog
* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 6.9.10-11
- Initial build for kaos repository
