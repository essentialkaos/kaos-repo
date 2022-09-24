################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define realname mad

################################################################################

Summary:         MPEG audio decoding library
Name:            lib%{realname}
Version:         0.15.1b
Release:         1%{?dist}
License:         GPL
Group:           System Environment/Libraries
URL:             https://www.underbit.com/products/mad/

Source0:         https://downloads.sourceforge.net/project/%{realname}/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:         %{realname}.pc

Source100:       checksum.sha512

Patch0:          %{name}-gcc44-compatibily.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make autoconf automake gcc-c++

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

MAD does not yet support MPEG-2 multichannel audio (although it should be
backward compatible with such streams) nor does it currently support AAC.

################################################################################

%package devel
Summary:        Header and library for developing programs that will use libmad
Group:          Development/Libraries

Requires:       %{name} = %{version} pkgconfig

%description devel
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

This package contains the header file as well as the static library needed
to develop programs that will use libmad for mpeg audio decoding.

################################################################################

%prep
%{crc_check}

%setup -q
%patch0 -p1

%build
%configure \
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -pm 644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/%{realname}.pc

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGES COPYING COPYRIGHT CREDITS README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-, root, root, -)
%exclude %{_libdir}/%{name}.la
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
%{_includedir}/%{realname}.h
%{_libdir}/pkgconfig/%{realname}.pc

################################################################################

%changelog
* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.1b-1
- Added package config file
- Minor package improvements

* Tue Mar 24 2015 Anton Novojilov <andy@essentialkaos.com> - 0.15.1b-0
- Initial build
