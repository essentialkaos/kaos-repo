################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            Adaptive Multi-Rate Floating-point (AMR) Speech Codec
Name:               opencore-amr
Version:            0.1.6
Release:            0%{?dist}
License:            ASL 2.0
Group:              System Environment/Libraries
URL:                https://sourceforge.net/projects/opencore-amr/

Source0:            https://downloads.sourceforge.net/project/%{name}/%{name}/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
3GPP released reference implementations 3GPP Adaptive Multi-Rate
Floating-point (AMR) Speech Codec (3GPP TS 26.104 V 7.0.0) and 3GPP
AMR Adaptive Multi-Rate - Wideband (AMR-WB) Speech Codec (3GPP TS
26.204 V7.0.0).

################################################################################

%package devel
Summary:            Development files for opencore-amr
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
This is the package containing the header files for opencore-amr libraries.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure --disable-static

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
%doc ChangeLog LICENSE README
%{_libdir}/lib%{name}nb.so.*
%{_libdir}/lib%{name}wb.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}nb/*.h
%{_includedir}/%{name}wb/*.h
%{_libdir}/lib%{name}nb.so
%{_libdir}/lib%{name}wb.so
%{_libdir}/lib%{name}nb.la
%{_libdir}/lib%{name}wb.la
%{_libdir}/pkgconfig/%{name}nb.pc
%{_libdir}/pkgconfig/%{name}wb.pc

################################################################################

%changelog
* Wed Sep 21 2022 Anton Novojilov <andy@essentialkaos.com> - 0.1.6-0
- Fixed an infinite loop when decoding some AMR-NB samples
- Fixed noise spikes when decoding non-voice frames for both AMR-NB and AMR-WB

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.1.5-0
- Fix an autotools issue with cross compiling from the 0.1.4 release

* Sat Mar 17 2012 Paulo Roma <roma@lcg.ufrj.br> - 0.1.3-0
- Updated to latest version

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.1.2-1
- Initial build
