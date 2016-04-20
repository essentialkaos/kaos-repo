###############################################################################

%define _posixroot        /
%define _root             /root
%define _opt              /opt
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ldconfig        %{_sbin}/ldconfig

###############################################################################

Summary:            Video Acceleration (VA) API for Linux
Name:               libva
Version:            1.7.0
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            MIT
URL:                http://freedesktop.org/wiki/Software/vaapi

Source0:            https://www.freedesktop.org/software/vaapi/releases/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool libudev-devel
BuildRequires:      libdrm-devel >= 2.4.23 libpciaccess-devel mesa-libGL-devel
BuildRequires:      libXext-devel libXfixes-devel

Conflicts:          libdrm < 2.4.23

Provides:           libva-utils = %{version}-%{release}
Provides:           libva-freeworld = %{version}-%{release}

Obsoletes:          libva-utils < %{version}-%{release}
Obsoletes:          libva-freeworld < %{version}-%{release}

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
Libva is open source library to provide hardware accelerated video 
encoding and decoding. It supported by GStreamer, VLC media player, Mpv and 
MPlayer.

###############################################################################

%package devel
Summary:            Libraries and headers for (VA) API
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Libva headers and libraries which provides the VA API video acceleration API.

###############################################################################

%prep
%setup -q

%build
libtoolize -f
autoreconf -fi
%configure --disable-static --enable-glx

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

###############################################################################

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/jpegenc
%{_bindir}/loadjpeg
%{_bindir}/mpeg2vaenc
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface
%{_bindir}/vainfo
%{_libdir}/%{name}*.so*
%{_pkgconfigdir}/%{name}*.pc

%files devel
%defattr(-,root,root,-)
%{_includedir}/va/*.h
%{_libdir}/%{name}*.so
%{_libdir}/%{name}*.la
%{_libdir}/dri/dummy_drv_video.so
%{_libdir}/dri/dummy_drv_video.la

###############################################################################

%changelog
* Fri Apr 15 2016 Gleb Goncharov <yum@gongled.ru> - 1.7.0-0
- Updated to latest version
  + Bump VA API version to 0.39
  + Add support for VP9 10bit decode API
  + Allow libva to load the vaapi driver provided by Mesa Gallium for nouveau and radeon
  + Fix libva-glx against OpenGL 3.1 or above

* Sat Jun  7 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.1-11
- Update to 1.3.1.

* Sat Jun  7 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.1-10
- Update to 1.2.1.

* Sat Jun  7 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.1-9
- Update to 1.1.1.

* Sat Jun  7 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.16-8
- Update to 1.0.16.

* Sun Nov  6 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.15-7
- Update to 1.0.15.

* Mon Jun 27 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.0.13-6
- Update to 1.0.13
- Added BR libpciaccess-devel.
- New avcenc binary.

* Mon Apr 11 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.0.12-5
- Update to 1.0.12
- Removed all patches.

* Sun Mar 07 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.0.10-4
- Switch to upstream.

* Sun Jan 30 2011 Paulo Roma <roma@lcg.ufrj.br> - 0.32.0-3.sds1
- Update to 0.32.0-1.sds1

* Sun Jan 30 2011 Paulo Roma <roma@lcg.ufrj.br> - 0.31.1-2.sds5
- Update to 0.31.1-1.sds5

* Sun Jul 18 2010 Paulo Roma <roma@lcg.ufrj.br> - 0.31.1-1.sds4
- Rebuilt as libva for ATrpms.

* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.1-1.sds4
- Update to 0.31.1-1+sds4
- Add BR libudev-devel
- Obsoletes libva-utils 
 (tests files aren't installed anymore).

* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds13-3
- Revert to the previous version scheme
- Fix mix use of spaces and tabs

* Wed Jul 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0-1.sds13
- Move to libva-freeworld
- Virtual provides libva bumped with epoch
- Remove duplicate licence file.

* Mon Jul 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds130-1
- Update to 0.31.0-1+sds13

* Fri Mar 12 2010 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds10-1
- new SDS patch version (sds10):
 + Add detection of Broadcom Crystal HD chip.
 + Require vaDriverInit() function to include SDS API version. 
 + OpenGL extensions updates:
 - Drop the 'bind' API. Only keep vaCopySurfaceGLX().
 - Fix FBO check for the generic implementation with TFP.
 + Compat: strip vaPutSurface() flags to match older API.
 - This fixes deinterlacing support with GMA500 "psb" driver.
 + Upgrade to GIT snapshot 2009/12/17:
 - Add a "magic" number to VADisplayContext.
 - Add more test programs, including h264 encoding.
- add -utils package for the various new binaries in this build

* Thu Dec 3 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds9-1
- new SDS patch version (sds9):
 + Add extra picture info for VDPAU/MPEG-4

* Mon Nov 23 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds8-1
- new SDS patch version (sds8) - note sds7 package actually contained
 sds5 due to an error on my part:
 + Fix detection of ATI chipsets with fglrx >= 8.69-Beta1.
 + Upgrade to GIT snapshot 2009/11/20:
  + Merge in some G45 fixes and additions.
  + Add VA_STATUS_ERROR_SURFACE_IN_DISPLAYING.

* Tue Nov 17 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds7-1
- new SDS patch version:
 + Fix compatibility with older programs linked against libva.so.0
 + G45 updates:
  + Fix vaCreateImage() and vaDestroyImage()
  + Fix subpictures association to parent surfaces
  + Fix rendering of subpictures (extra level of scaling)
  + Fix subpicture palette upload (IA44 and AI44 formats for now)
  + Add RGBA subpicture formats
  + Add YV12 vaGetImage() and vaPutImage()
  + Fix subpicture rendering (flickering)
  + Fix return value for unimplemented functions
  + Fix vaPutSurface() to handle cliprects (up to 80)

* Thu Oct 8 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-2
- enable the i965 driver build

* Tue Oct 6 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-1
- new SDS patch version:
 + G45 updates:
 + Fix VA driver version
 + Fix vaAssociateSubpicture() arguments
 + Add vaQueryDisplayAttributes() as a no-op
 + Fix vaQueryImageFormats() to return 0 formats at this time

* Tue Sep 22 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds4-1
- new SDS patch version:
 + Fix chek for GLX extensions
 + Fix libva pkgconfig dependencies
 + Fix vainfo dependencies (Konstantin Pavlov)
 + Add C++ guards to <va/va_glx.h>
 + Don't search LIBGL_DRIVERS_PATH, stick to extra LIBVA_DRIVERS_PATH
 + Upgrade to GIT snapshot 2009/09/22:
 - Merge in SDS patches 001, 201, 202
 - i965_drv_driver: use the horizontal position of a slice

* Thu Sep 10 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds3-1
- new upstream + SDS patch version:
 + Add OpenGL extensions (v3)
 + Upgrade to VA API version 0.31 (2009/09/07 snapshot)
 + Add drmOpenOnce() / drmCloseOnce() replacements for libdrm < 2.3
 + Add generic VA/GLX implementation with TFP and FBO
 + Fix detection of ATI chipsets with fglrx >= 8.66-RC1
 + Add VASliceParameterBufferMPEG2.slice_horizontal_position for i965 
   driver

* Thu Sep 3 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-3
- don't declare the stack as executable when creating libva.so.0

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-2
- enable glx support

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-1
- new SDS patch version:
 + Add VA_STATUS_ERROR_UNIMPLEMENTED
 + Add vaBindSurfaceToTextureGLX() and vaReleaseSurfaceFromTextureGLX()

* Wed Aug 26 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds4-1
- new SDS patch version:
 + Add OpenGL extensions
 + Fix NVIDIA driver version check
 + Fix libva-x11-VERSION.so.* build dependencies

* Wed Aug 12 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds3-1
- initial package
