################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Powerful image loading and rendering library
Name:           imlib2
Version:        1.12.3
Release:        0%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            https://docs.enlightenment.org/api/imlib2/html

Source0:        https://prdownloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ zlib-devel freetype-devel

Requires:       zlib

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Imlib2 is an advanced replacement library for libraries like libXpm that
provides many more features with much greater flexibility and speed than
standard libraries, including font rasterization, rotation, RGBA space
rendering and blending, dynamic binary filters, scripting, and more.

################################################################################

%package devel
Summary:  Imlib2 headers, static libraries and documentation
Group:    Development/Libraries

Requires:  %{name} = %{version}
Requires:  pkgconfig(x11)

%description devel
Headers, static libraries and documentation for Imlib2.

################################################################################

%package filters
Summary:  Imlib2 basic plugin filters set
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description filters
Basic set of plugin filters that come with Imlib2.

################################################################################

%package loader_lbm
Summary:  Imlib2 LBM loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_lbm
LBM image loader/saver for Imlib2.

################################################################################

%package loader_jpeg
Summary:  Imlib2 JPEG loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}
Requires:  libjpeg-turbo

BuildRequires:  libjpeg-turbo-devel

%description loader_jpeg
JPEG image loader/saver for Imlib2.

################################################################################

%package loader_png
Summary:  Imlib2 PNG loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}
Requires:  libpng zlib

BuildRequires:  libpng-devel zlib-devel

%description loader_png
PNG image loader/saver for Imlib2.

################################################################################

%package loader_argb
Summary:  Imlib2 ARGB loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_argb
ARGB image loader/saver for Imlib2.

################################################################################

%package loader_bmp
Summary:  Imlib2 BMP loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_bmp
BMP image loader/saver for Imlib2.

################################################################################

%package loader_ff
Summary:  Imlib2 Farbfeld loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_ff
Farbfeld image loader/saver for Imlib2.

################################################################################

%package loader_gif
Summary:  Imlib2 GIF loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}
Requires:  giflib

BuildRequires:  giflib-devel

%description loader_gif
GIF image loader for Imlib2.

################################################################################

%package loader_ico
Summary:  Imlib2 ICO loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_ico
ICO image loader for Imlib2.

################################################################################

%package loader_pnm
Summary:  Imlib2 PNM loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_pnm
PNM image loader/saver for Imlib2.

################################################################################

%package loader_tga
Summary:  Imlib2 TGA loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_tga
TGA image loader/saver for Imlib2.

################################################################################

%package loader_tiff
Summary:  Imlib2 TIFF loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}
Requires:  libtiff

BuildRequires:  libtiff-devel

%description loader_tiff
TIFF image loader/saver for Imlib2.

################################################################################

%package loader_xpm
Summary:  Imlib2 XPM loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_xpm
XPM image loader/saver for Imlib2.

################################################################################

%package loader_xbm
Summary:  Imlib2 XBM loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_xbm
XBM image loader/saver for Imlib2.

################################################################################

%package loader_bz2
Summary:  Imlib2 .bz2 loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

BuildRequires:  bzip2-devel

%description loader_bz2
Bzip2 compressed image loader/saver for Imlib2.

################################################################################

%package loader_gz
Summary:  Imlib2 .gz loader
Group:    System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_gz
gz compressed image loader/saver for Imlib2.

################################################################################

%package loader_id3
Summary:  Imlib2 .id3 loader
Group:  System Environment/Libraries

Requires:  %{name} = %{version}
Requires:  libid3tag

BuildRequires:  libid3tag-devel

%description loader_id3
id3 tag image loader/saver for Imlib2.

################################################################################

%package loader_ani
Summary:  Imlib2 .ani loader
Group:  System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_ani
Animated Windows cursors loader/saver for Imlib2.

################################################################################

%package loader_qoi
Summary:  Imlib2 .qoi loader
Group:  System Environment/Libraries

Requires:  %{name} = %{version}

%description loader_qoi
Quite OK Image Format loader/saver for Imlib2.

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

%files loader_ani
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/ani.so

%files loader_qoi
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/%{name}/loaders/qoi.so

################################################################################

%changelog
* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.12.3-0
- Updated to version 1.12.3

* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- Updated to version 1.9.1

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to version 1.7.0

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to version 1.6.1

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to version 1.6.0

* Tue Apr 12 2016 Gleb Goncharov <yum@gongled.ru> - 1.4.8-0
- Initial build for kaos repo
