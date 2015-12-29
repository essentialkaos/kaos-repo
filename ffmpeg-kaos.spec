###############################################################################

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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define source_name       ffmpeg

###############################################################################

Summary:           Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder
Name:              %{source_name}-kaos
Version:           2.8.4
Release:           0%{?dist}
License:           GPLv3
Group:             System Environment/Libraries
URL:               http://ffmpeg.org

Source:            http://ffmpeg.org/releases/%{source_name}-%{version}.tar.bz2

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     atrpms-repo

BuildRequires:     make gcc SDL-devel freetype-devel zlib-devel bzip2-devel
BuildRequires:     imlib2-devel a52dec-devel libdc1394-devel libraw1394-devel
BuildRequires:     libstdc++-devel faac-devel faad2-devel gsm-devel
BuildRequires:     lame-devel libtheora-devel libvorbis-devel
BuildRequires:     xvidcore-devel x264-devel libfdk-aac openjpeg-devel
BuildRequires:     dirac-devel schroedinger-devel speex-devel opencore-amr-devel
BuildRequires:     libvdpau-devel yasm libva-devel frei0r-plugins-devel
BuildRequires:     opencv-devel rtmpdump-devel >= 2.2.f openssl-devel
BuildRequires:     libvpx-devel >= 0.9.6 xavs-devel libnut

Requires:          atrpms-repo
Requires:          SDL gsm libdc1394 libfaac0 libfdk-aac libmp3lame0 libopencore-amrnb0
Requires:          libopencore-amrwb0 librtmp0 libva1 libvpx libx264_136 libxavs1
Requires:          libxvidcore4 opencv orc schroedinger unicap

Conflicts:         %{source_name}

###############################################################################

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

###############################################################################

%prep
%setup -q -n %{source_name}-%{version}
test -f version.h || echo "#define FFMPEG_VERSION \"%{version}-%{release}\"" > version.h

%build
%{_configure} --prefix=%{_prefix} --libdir=%{_libdir} \
              --shlibdir=%{_libdir} --mandir=%{_mandir} \
  --enable-shared \
  --enable-runtime-cpudetect \
  --enable-gpl \
  --enable-version3 \
  --enable-nonfree \
  --enable-postproc \
  --enable-avfilter \
  --enable-pthreads \
  --enable-x11grab \
  --enable-vdpau \
  --disable-avisynth \
  --enable-frei0r \
  --enable-libopencv \
  --enable-libdc1394 \
  --enable-libfaac \
  --enable-libgsm \
  --enable-libmp3lame \
  --enable-libnut \
  --enable-libopencore-amrnb \
  --enable-libopencore-amrwb \
  --enable-libopenjpeg \
  --enable-librtmp \
  --enable-libschroedinger \
  --enable-libspeex \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libfdk_aac \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libxavs \
  --enable-libxvid \
%ifarch %ix86
  --extra-cflags="%{optflags}" \
%else
  --extra-cflags="%{optflags} -fPIC" \
%endif
  --disable-stripping \
  --disable-demuxer=v4l \
  --disable-demuxer=v4l2 \
  --disable-indev=v4l \
  --disable-indev=v4l2

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install} incdir=%{buildroot}%{_includedir}/%{source_name}

%{__rm} -rf doc/Makefile

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING* CREDITS doc/
%{_bindir}/*
%{_datadir}/%{source_name}
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man1/ff*.1.*
%{_mandir}/man3/lib*.3.*

###############################################################################

%changelog
* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8.4-0
- Updated to version 2.8.4

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- Updated to version 2.8.2

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Updated to version 2.8

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7.2-0
- Updated to version 2.7.2

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- Updated to version 2.7.1

* Mon Apr 13 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.2-0
- Updated to version 2.6.2

* Wed Mar 11 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6-0
- Updated to version 2.6

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.4-0
- Updated to version 2.5.4

* Sat Jan 17 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.3-0
- Updated to version 2.5.3

* Sat Dec 27 2014 Anton Novojilov <andy@essentialkaos.com> - 2.5.2-0
- Updated to version 2.5.2

* Sat Dec 20 2014 Anton Novojilov <andy@essentialkaos.com> - 2.5.1-0
- Updated to version 2.5.1

* Wed Dec 10 2014 Anton Novojilov <andy@essentialkaos.com> - 2.5-0
- Updated to version 2.5

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4.4-0
- Updated to version 2.4.4

* Sat Oct 11 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- Updated to version 2.4.2

* Fri Sep 19 2014 Anton Novojilov <andy@essentialkaos.com> - 2.4-0
- Updated to version 2.4

* Fri Aug 29 2014 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- Updated to version 2.3.3

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- Updated to version 2.2

* Wed Feb 19 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
- Updated to version 2.1.3

* Tue Oct 08 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.4-0
- Updated to 1.2.4
