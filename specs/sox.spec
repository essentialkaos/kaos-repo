################################################################################

Summary:            A general purpose sound file conversion tool
Name:               sox
Version:            14.4.2
Release:            0%{?dist}
License:            GPLv2+, LGPLv2+ and MIT
Group:              Applications/Multimedia
URL:                http://sox.sourceforge.net

Source0:            https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make autoconf automake libmad-devel
BuildRequires:      libvorbis-devel alsa-lib-devel libtool-ltdl-devel
BuildRequires:      libsamplerate-devel gsm-devel wavpack-devel ladspa-devel
BuildRequires:      libpng-devel flac-devel libao-devel libsndfile-devel
BuildRequires:      libid3tag-devel pulseaudio-libs-devel libtool lame-devel

Requires:           lame gsm libmad libid3tag libpng libao libsndfile wavpack
Requires:           ladspa libsamplerate libvorbis alsa-lib pulseaudio-libs

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
SoX (Sound eXchange) is a sound file format converter SoX can convert
between many different digitized sound formats and perform simple
sound manipulation functions, including sound effects.

################################################################################

%package -n sox-devel
Summary:            The SoX sound file format converter libraries
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description -n sox-devel
This package contains the library needed for compiling applications
which will use the SoX sound file format converter.

################################################################################

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%configure --without-lpc10 \
           --with-gsm \
           --with-alsa=dyn \
           --with-ao=dyn \
           --with-caf=dyn \
           --with-fap=dyn \
           --with-lame=dyn \
           --with-mad=dyn \
           --with-mat4=dyn \
           --with-mat5=dyn \
           --with-paf=dyn \
           --with-pulseaudio=dyn \
           --with-pvf=dyn \
           --with-sd2=dyn \
           --with-sndfile=dyn \
           --with-vorbis=dyn \
           --with-w64=dyn \
           --with-wavpack=dyn \
           --with-xi=dyn \
           --with-distro=Fedora \
           --disable-static \
           --includedir=%{_includedir}/sox

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/libsox.la
rm -f %{buildroot}%{_libdir}/sox/*.la
rm -f %{buildroot}%{_libdir}/sox/*.a

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%dir %{_libdir}/sox/
%{_libdir}/libsox.so.*
%{_libdir}/sox/libsox_fmt_*.so
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox
%{_bindir}/soxi
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n sox-devel
%defattr(-,root,root,-)
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_includedir}/sox
%{_mandir}/man3/*

################################################################################

%changelog
* Fri May 04 2018 Anton Novojilov <andy@essentialkaos.com> - 14.4.2-0
- Initial build for kaos-repo
