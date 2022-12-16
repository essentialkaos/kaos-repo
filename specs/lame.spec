################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define lib_name  libmp3%{name}

################################################################################

Summary:            MP3 encoder and frame analyzer
Name:               lame
Version:            3.100
Release:            1%{?dist}
License:            LGPLv2+
Group:              Applications/Multimedia
URL:                https://lame.sourceforge.net

Source0:            https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           ncurses >= 5.0

Provides:           lame-libs = %{version}-%{release}
Provides:           mp3encoder = %{version}-%{release}

Obsoletes:          lame-libs < %{version}-%{release}
Obsoletes:          mp3encoder < %{version}-%{release}

BuildRequires:      gcc-c++ make nasm
BuildRequires:      ncurses-devel libsndfile-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve
the psycho acoustics, noise shaping and speed of MP3. Another goal of
the LAME project is to use these improvements for the basis of a patent
free audio compression codec for the GNU project.

################################################################################

%package devel
Summary:            Libraries and headers for lame
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Libraries provide the functions necessary to convert raw PCM and WAV files to
MP3 files.

################################################################################

%prep
%{crc_check}

%setup -q

%ifarch %{ix86} x86_64
  sed -i -e '/define sp/s/+/ + /g' libmp3lame/i386/nasm.h
%endif

%build
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86} x86_64
  --enable-nasm \
%endif
  --enable-decoder \
  --enable-mp3x \
  --enable-mp3rtp

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING LICENSE README TODO USAGE
%{_bindir}/%{name}
%{_bindir}/mp3rtp
%{_libdir}/%{lib_name}.so.*
%{_docdir}/%{name}/html/*.html
%{_mandir}/man1/lame.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/%{name}.h
%{_libdir}/%{lib_name}.so
%{_libdir}/%{lib_name}.la

################################################################################

%changelog
* Sat May 25 2019 Anton Novojilov <andy@essentialkaos.com> - 3.100-1
- Minor spec fix

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.100-0
- Improved detection of MPEG audio data in RIFF WAVE files
- Fix possible race condition causing build failures in libmp3lame
- Don't include the debian directory as one that is needed during builds
- New switch --gain <decibel>, range -20.0 to +12.0, a more convenient way to
  apply Gain adjustment in decibels, than the use of --scale <factor>
- Resurrect Owen Taylor's code dated from 97-11-3 to properly deal with GTK1
- Bug in path handling
- Problem with Tag genre
- No progress indication with pipe input
- Scale (empty) silent encode without warning
- Environment variable LAMEOPT doesn't work anymore
- Input file name displayed with wrong character encoding (on windows console
  with CP_UTF8)
- Fix dereference NULL and Buffer not NULL terminated issues
- Dereference of a null pointer possible in loop
- Make sure functions with SSE instructions maintain their own properly
  aligned stack
- Multiple Stack and Heap Corruptions from Malicious File
- A division by zero vulnerability
- CVE-2017-9410 fill_buffer_resample function in libmp3lame/util.c heap-based
  buffer over-read and ap
- CVE-2017-9411 fill_buffer_resample function in libmp3lame/util.c invalid
  memory read and application crash
- CVE-2017-9412 unpack_read_samples function in frontend/get_audio.c invalid
  memory read and application crash
- clip detect scale suggestion unaware of scale input value
- HIP decoder bug fixed: decoding mixed blocks of lower sample frequency
  Layer3 data resulted in internal buffer overflow (write)
- Add lame_encode_buffer_interleaved_int()

* Thu Apr 14 2016 Gleb Goncharov <yum@gongled.ru> - 3.99.5-0
- Spec refactoring
- Updated to latest version
