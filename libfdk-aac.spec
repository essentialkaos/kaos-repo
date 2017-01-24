###############################################################################

%define _posixroot        /
%define _root             /root
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
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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

###############################################################################

Summary:           Fraunhofer FDK AAC codec library
Name:              libfdk-aac
Version:           0.1.5
Release:           0%{?dist}
License:           Copyright Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e.V.
Group:             System Environment/Libraries
URL:               https://github.com/mstorsjo/fdk-aac

Source:            https://github.com/mstorsjo/fdk-aac/archive/v%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make glibc-devel libtool autoconf gcc gcc-c++

Requires:          glibc

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description

Modified library of Fraunhofer AAC decoder and encoder.

###############################################################################

%prep
%setup -qn fdk-aac-%{version}

%build
autoreconf -fiv
%{_configure} --prefix=%{_prefix}
%{__make}

%install
%{__rm} -rf %{buildroot}

%{make_install}

%ifarch x86_64
  %{__mv} %{buildroot}%{_libdir32} %{buildroot}%{_libdir}
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc NOTICE
%{_includedir}/*
%{_libdir}/*

###############################################################################

%changelog
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
