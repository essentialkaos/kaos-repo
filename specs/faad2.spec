################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define pkg_name   faad
%define ver_major  2
%define ver_minor  10
%define ver_patch  0

################################################################################

Summary:           Freeware Advanced Audio (AAC) Decoder including SBR decoding
Name:              faad2
Version:           %{ver_major}.%{ver_minor}.%{ver_patch}
Release:           0%{?dist}
License:           GPLv2
Group:             Applications/Multimedia
URL:               https://github.com/knik0/faad2

Source0:           https://github.com/knik0/%{name}/archive/refs/tags/%{ver_major}_%{ver_minor}_%{ver_patch}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf automake libtool gcc gcc-c++
BuildRequires:     libsndfile-devel >= 1.0.0 id3lib-devel zlib-devel

Obsoletes:         faad2-libs <= %{version}

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Freeware Advanced Audio (AAC) Decoder including SBR decoding

FAAD2 is a HE, LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder.
FAAD2 includes code for SBR (HE AAC) decoding.
FAAD2 is licensed under the GPL.

################################################################################

%package -n libfaad2
Summary:           Libraries for faad2
Group:             Development/Libraries

Requires:          %{name} = %{version}

%description -n libfaad2
Libraries from faad2 that are needed to build programs that use it.

################################################################################

%package -n libfaad2-devel
Summary:           Header files for faad2
Group:             Development/Libraries

Requires:          %{name} = %{version}

%description -n libfaad2-devel
Header files from faad2 that are needed to build programs that use it.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{ver_major}_%{ver_minor}_%{ver_patch}

%build
autoreconf -fi

%configure \
  --without-xmms \
  --with-mpeg4ip \
  --with-drm

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/%{pkg_name}
%{_mandir}/man1/faad.*

%files -n lib%{name}
%defattr(-,root,root,-)
%{_libdir}/libfaad.so.*
%{_libdir}/libfaad_drm.so.*

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_includedir}/faad.h
%{_includedir}/neaacdec.h
%{_libdir}/libfaad.a
%{_libdir}/libfaad_drm.a
%{_libdir}/libfaad.so
%{_libdir}/libfaad_drm.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sun Sep 25 2022 Anton Novojilov <andy@essentialkaos.com> - 2.10.0-0
- updated Visual Studio projects to VS 2019
- mp4read.c: fix stack-buffer-overflow in stringin()/ftypin()
- fix heap-buffer-overflow in mp4read.c
- Remove non-ASCII characters
- Remove trailing whitespace
- Check return value of ltp_data.
- Restrict SBR frame length to 960 and 1024 samples.
- Support object type 29.
- Support implicit SBR signaling in frontend.
- Fix PNS decoding when only right channel is noise.
- Initialize element_id array with an invalid id.
- Fix NULL pointer dereferences.
- Fix infinite loop in adts_parse.
- Fix infinite loop in huffman_getescape.
- Check for error after each channel decode.
- Check for inconsistent number of channels.

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.8-0
- MSVC build fixes
- fixed a coulple bugs

* Mon Sep 05 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.7-0
- Initial build
