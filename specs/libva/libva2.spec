################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define realname    libva

################################################################################

Summary:            Video Acceleration (VA) API for Linux
Name:               %{realname}2
Version:            2.15.0
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            MIT
URL:                https://github.com/intel/libva

Source0:            https://github.com/intel/%{realname}/releases/download/%{version}/%{realname}-%{version}.tar.bz2

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool libudev-devel
BuildRequires:      libdrm-devel libpciaccess-devel mesa-libGL-devel
BuildRequires:      libXext-devel libXfixes-devel

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
Requires:           pkgconfig(x11) pkgconfig(gl)

%description devel
Libva headers and libraries which provides the VA API video acceleration API.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%build
libtoolize -f
autoreconf -fi

%configure --disable-static --enable-glx

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_libdir}/libva-drm.so.*
%{_libdir}/libva-glx.so.*
%{_libdir}/libva-x11.so.*
%{_libdir}/libva.so.*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_includedir}/va/*.h
%{_libdir}/libva-drm.so
%{_libdir}/libva-glx.so
%{_libdir}/libva-x11.so
%{_libdir}/libva.so
%{_libdir}/pkgconfig/libva-drm.pc
%{_libdir}/pkgconfig/libva-glx.pc
%{_libdir}/pkgconfig/libva-x11.pc
%{_libdir}/pkgconfig/libva.pc

################################################################################

%changelog
* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.15.0-0
- Add: new display HW attribute to report PCI ID
- Add: sample depth related parameters for AV1e
- Add: refresh_frame_flags for AV1e
- Add: missing fields in va_TraceVAEncSequenceParameterBufferHEVC.
- Add: nvidia-drm to the drm driver map
- Add: type and buffer for delta qp per block
- Deprecation: remove the va_fool support
- Fix:Correct the version of meson build on master branch
- Fix:X11 DRI2: check if device is a render node
- Build:Use also strong stack protection if supported
- Trace:print the string for profile/entrypoint/configattrib

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.14.0-0
- add: Add av1 encode interfaces
- add: VA/X11 VAAPI driver mapping for crocus DRI driver
- doc: Add description of the fd management for surface importing
- ci: fix freebsd build
- meson: Copy public headers to build directory to support subproject

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.13.0-0
- fix: Check the function pointer before using
- code style:unify the code styles using the style_unify script
- doc: Fix av1 dec doc page link issue
- add: (sep_layer) add new surface format fourcc XYUV

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.12.0-0
- add: Report the capability of vaCopy support
- add: Report the capability of sub device
- add: Add config attributes to advertise HEVC/H.265 encoder features
- add: Video processing HVS Denoise: Added 4 modes
- add: Introduce VASurfaceAttribDRMFormatModifiers
- add: Add 3DLUT Filter in Video Processing.
- doc: Update log2_tile_column description for vp9enc
- trace: Correct av1 film grain trace information
- ci: Fix freebsd build by switching to vmactions/freebsd-vm@v0.1.3

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.11.0-0
- add: LibVA Protected Content API
- add: Add a configuration attribute to advertise AV1d LST feature
- fix: wayland: don't try to authenticate with render nodes
- autotools: use shell grouping instead of sed to prepend a line
- trace: Add details data dump for mpeg2 IQ matrix.
- doc: update docs for VASurfaceAttribPixelFormat
- doc: Libva documentation edit for AV1 reference frames
- doc: Modify AV1 frame_width_minus1 and frame_height_minus1 comment
- doc: Remove tile_rows and tile_cols restriction to match AV1 spec
- doc: Format code for doxygen output
- doc: AV1 decode documentation edit for superres_scale_denominator
- ci: upgrade FreeBSD to 12.2
- ci: disable travis build
- ci: update cache before attempting to install packages
- ci: avoid running workloads on other workloads changes
- ci: enable github actions

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.10.0-0
- add: Pass offset and size of pred_weight_table
- add: add vaCopy interface to copy surface and buffer
- add: add definition for different execution
- add: New parameters for transport controlled BRC were added
- add: add FreeBSD support
- add: add a bufer type to adjust context priority dynamically
- fix: correct the api version in meson.build
- fix: remove deprecated variable from va_trace.c
- fix: Use va_deprecated for the deprecate variable
- fix: Mark chroma_sample_position as deprecated
- doc: va_dec_av1: clarifies CDEF syntax element packing
- doc: [AV1] Update documented ranges for loop filter and quantization params.
- doc: Update va.h for multi-threaded usages
- trace: va/va_trace: ignore system gettid() on Linux

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.9.0-0
- trace: Refine the va_TraceVAPictureParameterBufferAV1.
- doc: Add comments for backward/forward reference to avoid confusion
- doc: Modify comments in av1 decoder interfaces
- doc: Update mailing list
- Add SCC fields trace for HEVC SCC encoding.
- Add FOURCC code for Y212 and Y412 format.
- Add interpolation method for scaling.
- add attributes for context priority setting
- Add vaSyncBuffer for output buffers synchronization
- Add vaSyncSurface2 with timeout

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- trace: enable return value trace for successful function call
- trace: divide va_TraceEndPicture to two seperate function
- trace: add support for VAProfileHEVCSccMain444_10
- trace:Convert VAProfileAV1Profile0 VAProfileAV1Profile1 to string
- trace: Fix format string warnings
- trace: List correct field names in va_TraceVAPictureParameterBufferHEVC
- fix:Fixes file descriptor leak
- fix:Fix clang warning (reading garbage)
- fix: Fix HDR10 MaxCLL and MaxFALL documentation
- travis: Add a test that code files don't have the exec bit set
- add fourcc code for P012 format
- Remove the execute bit from all source code files
- meson: Allow for libdir and includedir to be absolute paths
- add definition to enforce both reflist not empty
- change the return value to be UNIMPLEMENTED when the function pointer is NULL
- remove check of vaPutSurface implementation
- Add new slice structure flag for CAPS reporting
- VA/X11: VAAPI driver mapping for iris DRI driver
- VA/X11: enable driver candidate selection for DRI2
- Add SCC flags to enable/disable features
- Add VAProfileHEVCSccMain444_10 for HEVC
- change the compatible list to be dynamic one

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- VA/X11: enable driver candidate selection for DRI2
- VA/X11: VAAPI driver mapping for iris DRI driver

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- trace: av1 decode buffers trace
- trace: Add HEVC REXT and SCC trace for decoding.
- Add av1 decode interfaces
- Fix crashes on system without supported hardware
- Add 2 FourCC for 10bit RGB(without Alpha) format: X2R10G10B10 and X2B10G10R10
- Fix android build issue #365 and remove some trailing whitespace
- Adjust call sequence to ensure authenticate operation is executed to fix

* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- enable the mutiple driver selection logic and enable it for DRM.
- drm: Add iHD to driver_name_map
- Add missed slice parameter 'slice_data_num_emu_prevn_bytes'
- ensure that all meson files are part of the release tarball
- configure: use correct comparison operator
- trace: support VAConfigAttribMultipleFrame in trace
- remove incorrect field of VAConfigAttribValDecJPEG
- va/va_trace: Dump VP9 parameters for profile 1~3
- add multiple frame capability report
- add variable to indicate layer infromation
- trace: fix memory leak on closing the trace
- add prediction direction caps report
- Add comments for colour primaries and transfer characteristics
  in VAProcColorProperties

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
