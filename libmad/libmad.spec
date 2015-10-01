################################################################################

Summary:         MPEG audio decoding library
Name:            libmad
Version:         0.15.1b
Release:         0%{?dist}
License:         GPL
Group:           System Environment/Libraries
URL:             http://www.underbit.com/products/mad/

Source0:         ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz

Patch0:          %{name}-gcc44-compatibily.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc-c++

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
%{makeinstall}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files 
%defattr(-, root, root, -)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%exclude %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*

################################################################################

%changelog
* Tue Mar 24 2015 Anton Novojilov <andy@essentialkaos.com> - 0.15.1b-0
- Initial build
