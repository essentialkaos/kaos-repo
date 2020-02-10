################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         An audio codec for use in low-delay speech and audio communication
Name:            opus
Version:         1.3.1
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         BSD
URL:             https://www.opus-codec.org

Source0:         https://archive.mozilla.org/pub/%{name}/%{name}-%{version}.tar.gz
Source1:         https://tools.ietf.org/rfc/rfc6716.txt

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc doxygen

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec.

################################################################################

%package devel

Summary:         Development package for opus
Group:           Development/Libraries

Requires:        libogg-devel
Requires:        opus = %{version}-%{release}

%description devel
Files for development with opus.

################################################################################

%prep
%setup -qn %{name}-%{version}

cp %{SOURCE1} .

%build
%configure --enable-custom-modes --disable-static

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-, root, root, -)
%doc COPYING
%{_libdir}/libopus.so.*

%files devel
%defattr(-, root, root, -)
%doc README doc/html rfc6716.txt
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

################################################################################

%changelog
* Sun Aug 18 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- A new OPUS_GET_IN_DTX query to know if the encoder is in DTX mode (last
  frame was either a comfort noise frame or not encoded at all)
- A new (and still experimental) CMake-based build system that is eventually
  meant to replace the VS2015 build system (the autotools one will stay)

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Improvements to the VAD and speech/music classification using an RNN
- Support for ambisonics coding using channel mapping families 2 and 3
- Improvements to stereo speech coding at low bitrate
- Using wideband encoding down to 9 kb/s
- Making it possible to use SILK down to bitrates around 5 kb/s
- Minor quality improvement on tones
- Enabling the spec fixes in RFC 8251 by default
- Security/hardening improvements
- Fixes to the CELT PLC
- Bandwidth detection fixes

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- This minor release fixes a relatively rare issue where the 1.2 encoder would
  wrongly assume a signal to be bandlimited to 12 kHz and not encode frequencies
  between 12 and 20 kHz.

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Speech quality improvements especially in the 12-20 kbit/s range
- Improved VBR encoding for hybrid mode
- More aggressive use of wider speech bandwidth, including fullband speech
  starting at 14 kbit/s
- Music quality improvements in the 32-48 kb/s range
- Generic and SSE CELT optimizations
- Support for directly encoding packets up to 120 ms
- DTX support for CELT mode
- SILK CBR improvements
- Support for all of the fixes in draft-ietf-codec-opus-update-06 (the mono
  downmix and the folding fixes need --enable-update-draft)
- Many bug fixes, including integer wrap-arounds discovered through fuzzing
  (no security implications)

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.5-0
- Initial build for kaos repository
