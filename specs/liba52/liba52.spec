################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define pkg_name   a52dec

################################################################################

Summary:           A free library for decoding ATSC A/52 (aka AC-3) streams
Name:              liba52
Version:           0.7.4
Release:           2%{?dist}
License:           GPL
Group:             Applications/Multimedia
URL:               https://liba52.sourceforge.net

Source0:           https://liba52.sourceforge.net/files/%{pkg_name}-%{version}.tar.gz
Source1:           %{name}.pc

Source100:         checksum.sha512

Patch0:            %{pkg_name}-%{version}-fPIC.patch
Patch1:            %{pkg_name}-%{version}-rpath64.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf make gcc

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

################################################################################

%package devel
Summary:           Header files and static libraries for liba52
Group:             Development/Libraries
Requires:          %{name} = %{version}

%description devel
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

These are the header files and static libraries from liba52 that are needed
to build programs that use it.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkg_name}-%{version}

%patch0 -p1 -b .fPIC
%patch1 -p1 -b .rpath64

%build
autoconf

%configure --enable-shared \
           --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -pm 644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog HISTORY INSTALL COPYING README doc/liba52.txt
%{_bindir}/%{pkg_name}
%{_bindir}/extract_a52
%{_libdir}/%{name}.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%{_includedir}/%{pkg_name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sat Sep 24 2022 Anton Novojilov <andy@essentialkaos.com> - 0.7.4-2
- Package improvements

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 0.7.4-1
- Fixed problems with executing ldconfig

* Sat Jun 14 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.4-0
- Updated to latest version
