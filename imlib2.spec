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

Summary:            Powerful image loading and rendering library
Name:               imlib2
Version:            1.4.8
Release:            0%{?dist}
License:            BSD
Group:              System Environment/Libraries
URL:                https://docs.enlightenment.org/api/imlib2/html

Source0:            http://prdownloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           zlib

BuildRequires:      make gcc gcc-c++ autoconf freetype-devel
BuildRequires:      automake libtool libtool-ltdl-devel

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
%setup -q

%build
autoreconf -fi

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

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING-PLAIN README
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/loaders
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/%{name}/*/*.la
%{_bindir}/%{name}-config
%{_pkgconfigdir}/%{name}.pc
%{_includedir}/*
%{_datadir}/%{name}
%{_bindir}/%{name}_*

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
* Tue Apr 12 2016 Gleb Goncharov <yum@gongled.ru> - 1.4.8-0
- Initial build
