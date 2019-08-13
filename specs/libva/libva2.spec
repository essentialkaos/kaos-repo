################################################################################

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

################################################################################

%define realname          libva

################################################################################

Summary:            Video Acceleration (VA) API for Linux
Name:               %{realname}2
Version:            2.5.0
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            MIT
URL:                https://github.com/01org/libva

Source0:            https://github.com/01org/%{realname}/releases/download/%{version}/%{realname}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool libudev-devel
BuildRequires:      libdrm-devel >= 2.4.23 libpciaccess-devel mesa-libGL-devel
BuildRequires:      libXext-devel libXfixes-devel

Conflicts:          libdrm < 2.4.23
Conflicts:          %{realname} < 2.0.0

Provides:           libva-utils = %{version}-%{release}
Provides:           libva-freeworld = %{version}-%{release}

Obsoletes:          libva-utils < %{version}-%{release}
Obsoletes:          libva-freeworld < %{version}-%{release}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Libva is open source library to provide hardware accelerated video
encoding and decoding. It supported by GStreamer, VLC media player, Mpv and
MPlayer.

################################################################################

%package devel
Summary:            Libraries and headers for (VA) API
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Libva headers and libraries which provides the VA API video acceleration API.

################################################################################

%prep
%setup -qn %{realname}-%{version}

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

################################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_libdir}/%{realname}*.so*
%{_pkgconfigdir}/%{realname}*.pc

%files devel
%defattr(-,root,root,-)
%{_includedir}/va/*.h
%{_libdir}/%{realname}*.so
%{_libdir}/%{realname}*.la

################################################################################

%changelog
* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Correct the comment of color_range.
- Add VA_FOURCC_A2B10G10R10 for format a2b10g10r10.
- Adjust VAEncMiscParameterQuantization structure to be align with
  VAEncMiscParameterBuffer(possible to impact BC)
- Add attribute for max frame size
- Add va_footer.html into distribution build
- va_trace: hevc profiles added
- Add new definition for input/output surface flag
- va/va_trace: add trace support for VAEncMiscParameterTypeSkipFrame structure.
- va/va_trace: add MPEG2 trace support for MiscParam and SequenceParam
- va_openDriver: check strdup return value
- Mark some duplicated field as deprecated
- Add return value into logs
- va/va_trace: add trace support for VAEncMiscParameterEncQuality structure.
- Add newformat foucc defination
- va_backend: remove unneeded linux/videodev2.h include
- va_trace: add missing <sys/time.h> include
- configure: don't build glx if VA/X11 isn't built
- va/va_trace: unbreak with C89 after b369467
- [common] Add A2RGB10 fourcc definition
- build: meson: enables va messaging and visibility
- va/va_trace: add trace support for RIR(rolling intra refresh).
- va/va_trace: add trace support for ROI(region of interest).

* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- va_TraceSurface support for VA_FOURCC_P010
- Add pointer to struct wl_interface for driver to use
- (integrate) va: fix new line symbol in error message
- av: avoid driver path truncation
- Fix compilation warning (uninit and wrong variable types) for Android O MR1
- Allow import of the DRM PRIME 2 memory type
- android: ignore unimportant compile warnnings
- compile: fix sign/unsign compare in va_trace.c
- android: replace utils/Log.h with log/log.h
- High Dynamic Range Tone Mapping: Add a new filter for input metadata and some
  comments.
- Remove restrictions on vaSetDriverName()

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Bump VA-API version to 1.3.0 and libva to 2.3.0
- Add max frame size parameters for multiple pass case in legacy mode
- Add new BRC mode AVBR
- Add new interface for High Dynamic Range tone mapping
- Add missing enum to string conversions
- Add hevc subsets parameters structure
- Add Customized Noise Reduction (HVS) interfaces
- Add new BRC mode definition QVBR
- Add more complete colour properties for use in VPP

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Bump VA-API version to 1.2.0 and libva to 2.2.0
- Add support for hevc range extension decoding
- Add support for fast intra prediction in HEVC FEI
- Add 10/12-bit YUV render target formats
- Add fourcc code for Y210/Y216/Y410/Y416/RGB565/BGR565
- Add VA_STATUS_ERROR_NOT_ENOUGH_BUFFER
- Add VA_SURFACE_ATTRIB_USAGE_HINT_EXPORT
- Improve documentation

* Wed May 30 2018 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-1
- Added livba < 2 to conflicts

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- Bump VA-API version to 1.1.0 and libva to 2.1.0
- Add API for multi-frame processing
- Add entrypoint VAEntrypointStats for Statistics
- Add data structures for HEVC FEI support
- Add new attributes for decoding/encoding/video processing
- Add new VPP filter for Total Color Correction
- Add blending interface in VPP
- Add rotation interface in VPP
- Add mirroring interface in VPP
- Add Chroma siting flags in VPP
- Add new color standard definitions
- Add new interface for exporting surface
- Add message callbacks for drivers to use

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Initial build for kaos repository
