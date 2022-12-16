################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _lib32            %{_posixroot}lib
%define _libdir32         %{_prefix}%{_lib32}

################################################################################

%define realname   fdk-aac

################################################################################

Summary:           Fraunhofer FDK AAC codec library
Name:              lib%{realname}
Version:           2.0.2
Release:           0%{?dist}
License:           Copyright Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e.V.
Group:             System Environment/Libraries
URL:               https://github.com/mstorsjo/fdk-aac

Source0:           https://github.com/mstorsjo/%{realname}/archive/v%{version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make glibc-devel libtool autoconf gcc gcc-c++

Requires:          glibc

Provides:          %{name} = %{version}-%{release}

################################################################################

%description

Modified library of Fraunhofer AAC decoder and encoder.

################################################################################

%package devel
Summary:             Header files and libraries for FDK AAC codec library
Group:               Development/Libraries

Requires:            %{name} = %{version}

%description devel
The %{name}-devel package contains the header files and
libraries to develop applications using Fraunhofer FDK AAC codec.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%build
autoreconf -fiv
%{_configure} --prefix=%{_prefix}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%ifarch x86_64
  mv %{buildroot}%{_libdir32} %{buildroot}%{_libdir}
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc NOTICE OWNERS
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/%{name}.la
%{_includedir}/%{realname}/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/%{realname}.pc

################################################################################

%changelog
* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Minor upstream updates
- Lots of upstream and local fuzzing fixes
- Added CMake project files
- Removed the MSVC specific makefile

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Minor release with a number of crash/fuzz fixes, primarily for the decoder

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Major update in the upstream source base, with support for new
  profiles and features, and numerous crash/fuzz fixes

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 0.1.6-0
- Lots of minor assorted crash/fuzz fixes, mostly for the decoder but also some
  for the encoder

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.1.5-0
- Updated upstream sources
- Fixed building with GCC 3.3 and 3.4
- Fixed building with GCC 6
- AArch64 optimizations
- Makefiles for building with MSVC
- Support building the code in C++11 mode

* Thu Jul 02 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.4-1
- Updated upstream sources, with minor changes to the decoder API
  breaking the ABI. (Calling code using AUDIO_CHANNEL_TYPE may need to
  be updated. A new option AAC_PCM_LIMITER_ENABLE has been added, enabled
  by default, which incurs extra decoding delay)
 - PowerPC optimizations, fixes for building on AIX
 - Support for reading streamed wav files in the encoder example
 - Fix VBR encoding of sample rates over 64 kHz

* Sat Sep 20 2014 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-2
- Fixes and improvements
- Improved spec

* Mon Jun 16 2014 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-1
- Some fixes

* Wed Feb 19 2014 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- Updated upstream sources, with a number of crash fixes and new features
  (including support for encoding 7.1)

* Tue Oct 08 2013 Anton Novojilov <andy@essentialkaos.com> - 0.1.2-0
- First release
