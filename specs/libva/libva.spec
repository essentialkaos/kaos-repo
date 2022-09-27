################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            Video Acceleration (VA) API for Linux
Name:               libva
Version:            1.8.3
Release:            2%{?dist}
Group:              System Environment/Libraries
License:            MIT
URL:                https://github.com/intel/libva

Source0:            https://github.com/intel/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool libudev-devel
BuildRequires:      libdrm-devel libpciaccess-devel mesa-libGL-devel
BuildRequires:      libXext-devel libXfixes-devel

Conflicts:          libdrm < 2.4.23

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

%setup -q

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
%{_libdir}/libva-tpi.so.*
%{_libdir}/libva-x11.so.*
%{_libdir}/libva.so.*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_includedir}/va/*.h
%{_libdir}/libva-drm.so
%{_libdir}/libva-glx.so
%{_libdir}/libva-tpi.so
%{_libdir}/libva-x11.so
%{_libdir}/libva.so
%{_libdir}/pkgconfig/libva-drm.pc
%{_libdir}/pkgconfig/libva-glx.pc
%{_libdir}/pkgconfig/libva-tpi.pc
%{_libdir}/pkgconfig/libva-x11.pc
%{_libdir}/pkgconfig/libva.pc

################################################################################

%changelog
* Tue Sep 27 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-2
- Minor spec improvements

* Fri Sep 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-1
- Minor spec improvements

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-0
- Updated to the latest version

* Fri Apr 15 2016 Gleb Goncharov <yum@gongled.ru> - 1.7.0-0
- Updated to latest version
- Bump VA API version to 0.39
- Add support for VP9 10bit decode API
- Allow libva to load the vaapi driver provided by Mesa Gallium for nouveau
  and radeon
- Fix libva-glx against OpenGL 3.1 or above
