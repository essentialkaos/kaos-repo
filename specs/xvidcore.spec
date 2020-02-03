################################################################################

Summary:            Free reimplementation of the OpenDivX video codec
Name:               xvidcore
Version:            1.3.7
Release:            0%{?dist}
License:            XviD
Group:              System Environment/Libraries
URL:                https://labs.xvid.com

Source0:            https://downloads.xvid.com/downloads/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make nasm

Requires:           lib%{name} = %{version}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Xvid is a high quality MPEG-4 ASP video codec. Xvid encoded MPEG-4 videos can i
be played back by other MPEG-4 implementations decoders such as DivX, FFmpeg
MPEG-4 or standalone DVD players capable of MPEG-4 playback.

################################################################################

%package -n lib%{name}-devel
Summary:            Development files of XviD video codec
Group:              Development/Libraries

Requires:           lib%{name} = %{version}

Provides:           xvid-devel = %{version}

Obsoletes:          xvid-devel < %{version}

%description -n lib%{name}-devel
Xvid is a high quality MPEG-4 ASP video codec. Development files of XviD.

################################################################################

%package -n lib%{name}
Summary:            Shared library libxvidcore
Group:              Development/Libraries

%description -n lib%{name}
Xvid is a high quality MPEG-4 ASP video codec. Shared library of XviD.

################################################################################

%prep
%setup -qn %{name}

%build
pushd build/generic
  %configure
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

pushd build/generic
  %{make_install}
popd

%clean
rm -rf %{buildroot}

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README TODO

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%doc CodingStyle doc examples
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so

%files -n lib%{name}
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*

################################################################################

%changelog
* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 1.3.7-0
- Fix for a regression in initializing the Inter matrix with MPEG Quantization

* Mon Feb 03 2020 Anton Novojilov <andy@essentialkaos.com> - 1.3.6-0
- Fix for various, long-standing and potentially critical security
  vulnerabilities in the decoder (credit to OSS-Fuzz)
- Always use .text sections in nasm code for macho target

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 1.3.5-0
- AmigaOS build patch by Fredrik Wikstrom
- Support for applevel multithreading mode also for AVI output in xvid_encraw
- Set interlacing flag in decoder correctly
- Re-add support to decode raw YV12 input FourCC video
- Fix: Produce debug output only when debug option is enabled
- Fixed bug in thumbnail creation on Windows 7
- Fix output buffer stride calculation in MFT
- Setting interlaced flags on output pins correctly in DirectShow and MFT
- Corrected pixel aspect ratio support in MFT

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-0
- Updated to the latest stable release

* Sun Apr 24 2016 Gleb Goncharov <yum@gongled.ru> - 1.3.3-0
- Updated to latest version
