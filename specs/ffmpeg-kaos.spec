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

################################################################################

Summary:           Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder
Name:              %{source_name}-kaos
Version:           4.1.4
Release:           0%{?dist}
License:           GPLv3
Group:             System Environment/Libraries
URL:               http://ffmpeg.org

Source:            http://ffmpeg.org/releases/%{source_name}-%{version}.tar.bz2

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc SDL-devel freetype-devel zlib-devel bzip2-devel
BuildRequires:     imlib2-devel liba52-devel libdc1394-devel libraw1394-devel
BuildRequires:     libstdc++-devel libfaad2-devel gsm-devel opus-devel
BuildRequires:     lame-devel libtheora-devel libvorbis-devel vo-amrwbenc-devel
BuildRequires:     libxvidcore-devel x264-devel libfdk-aac openjpeg-devel
BuildRequires:     dirac-devel speex-devel libvpx-devel >= 1.4.0 xavs-devel
BuildRequires:     libvdpau-devel yasm libva-devel frei0r opencore-amr-devel
BuildRequires:     opencv-devel librtmp-devel openssl-devel orc-devel
BuildRequires:     openjpeg2-devel

Requires:          SDL xavs gsm libdc1394 libfdk-aac lame
Requires:          opencore-amr librtmp orc libvpx x264
Requires:          libxvidcore libva opus vo-amrwbenc openjpeg2

Conflicts:         %{source_name}

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

################################################################################

%prep
%setup -qn %{source_name}-%{version}
test -f version.h || echo "#define FFMPEG_VERSION \"%{version}-%{release}\"" > version.h

%build
%{_configure} \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --shlibdir=%{_libdir} \
  --mandir=%{_mandir} \
  --enable-shared \
  --enable-runtime-cpudetect \
  --enable-gpl \
  --enable-version3 \
  --enable-nonfree \
  --enable-postproc \
  --enable-avfilter \
  --enable-pthreads \
  --enable-vdpau \
  --disable-avisynth \
  --enable-frei0r \
  --enable-libopencv \
  --enable-libdc1394 \
  --enable-libgsm \
  --enable-libmp3lame \
  --enable-libopencore-amrnb \
  --enable-libopencore-amrwb \
  --enable-libvo-amrwbenc \
  --enable-libopenjpeg \
  --enable-libopus \
  --enable-librtmp \
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
  --disable-indev=v4l2

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} incdir=%{buildroot}%{_includedir}/%{source_name}

rm -rf doc/Makefile

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING* CREDITS doc/
%{_bindir}/*
%{_datadir}/%{source_name}
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man1/ff*.1.*
%{_mandir}/man3/lib*.3.*

################################################################################

%changelog
* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 4.1.4-0
- Updated to version 4.1.4

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 4.1-0
- Updated to version 4.1

* Fri Sep 14 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.2-1
- Rebuilt with the latest versions of dependencies

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.2-0
- Updated to version 4.0.2

* Fri Jun 22 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Updated to version 4.0.1

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0-0
- Updated to version 4.0

* Tue Feb 20 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.2-0
- Updated to version 3.4.2

* Thu Jan 25 2018 Anton Novojilov <andy@essentialkaos.com> - 3.4.1-0
- Updated to version 3.4.1
- Added vo-amrwbenc support

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4-0
- Updated to version 3.4

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.3.4-0
- Updated to version 3.3.4

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 3.3.2-0
- Updated to version 3.3.2

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 3.3-0
- Updated to version 3.3

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- Updated to version 3.2.4

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Updated to version 3.2.2

* Thu Nov 24 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2-1
- Fixed build dependencies

* Sun Oct 30 2016 Anton Novojilov <andy@essentialkaos.com> - 3.2-0
- Updated to version 3.2.0

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.1.4-0
- Updated to version 3.1.4

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.1.3-0
- Updated to version 3.1.3

* Tue Jun 14 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- Updated to version 3.0.2

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- Updated to version 3.0.1

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- Updated to version 3.0
