################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%ifarch %ix86
%define optflags -O2 -g -pipe -Wall -fexceptions -fstack-protector -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -Wp,-D_FORTIFY_SOURCE=2 --param=ssp-buffer-size=4
%endif

################################################################################

# Found X264_BUILD in (x264.h)
%define pkg_build  164
%define pkg_date   20220602
%define pkg_sha    baee400fa9ced6f5481a728138fed6e867b0ff7f

################################################################################

Summary:        H.264 (MPEG-4 AVC) encoder library
Name:           x264
Version:        0.%{pkg_build}
Release:        %{pkg_date}_0%{?dist}
License:        GPL
Group:          System Environment/Libraries
URL:            https://www.videolan.org/developers/x264.html

Source0:        https://code.videolan.org/videolan/x264/-/archive/%{pkg_sha}/%{name}-%{pkg_sha}.tar.bz2

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc gcc-c++ make nasm >= 2.13 yasm gettext

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
x264 is a free library for encoding H.264/AVC video streams.

################################################################################

%package devel
Summary:  Development files for x264
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
Header files and shared libraries for x264.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{pkg_sha}

%build
# Fail build if header file contains different build version
if [[ $(grep '#define X264_BUILD' x264.h | cut -f3 -d" ") != "%{pkg_build}" ]] ; then
  echo "Header file contains different build version!"
  exit 1
fi

%configure --enable-pic --enable-debug --enable-shared

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
%doc COPYING AUTHORS doc/*.txt
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_includedir}/%{name}_config.h
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sat Dec 17 2022 Anton Novojilov <andy@essentialkaos.com> - 0.164-20220602_0
- Updated to the latest stable snapshot

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 0.159-20200128_0
- Updated to the latest stable snapshot

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 0.157-20190711_0
- Updated to the latest stable snapshot

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 0.155-20190122_0
- Updated to the latest stable snapshot

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 0.155-20181207_0
- Updated to the latest stable snapshot

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 0.152-20180620_0
- Updated to the latest stable snapshot

* Tue Feb 20 2018 Anton Novojilov <andy@essentialkaos.com> - 0.152-20180219_0
- Updated to the latest stable snapshot

* Tue Sep 19 2017 Anton Novojilov <andy@essentialkaos.com> - 0.152-20170918_0
- Updated to the latest stable snapshot

* Wed Jul 12 2017 Anton Novojilov <andy@essentialkaos.com> - 0.151-20170711_0
- Updated to the latest stable snapshot

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 0.150-20170709_0
- Updated to the latest stable snapshot

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 0.149-20170321_0
- Updated to the latest stable snapshot

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 0.148-20160905_0
- Updated to the latest stable snapshot

* Mon Apr 18 2016 Gleb Goncharov <yum@gongled.ru> - 0.148-20160416_0
- Updated to the latest stable snapshot
