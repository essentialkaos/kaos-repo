################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define ver_major  1
%define ver_minor  30

################################################################################

Summary:        ISO/MPEG 2/4 AAC Encoder library
Name:           faac
Version:        %{ver_major}.%{ver_minor}
Release:        0%{?dist}
License:        LGPL
Group:          Applications/Multimedia
URL:            https://github.com/knik0/faac

Source0:        https://github.com/knik0/faac/archive/refs/tags/%{ver_major}_%{ver_minor}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf automake make libtool gcc gcc-c++ chrpath

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
FAAC is an encoder for a lossy sound compression scheme specified in MPEG-2
Part 7 and MPEG-4 Part 3 standards and known as Advanced Audio Coding (AAC).

This encoder is useful for producing files that can be played back on iPod.
Moreover, iPod does not understand other sound compression schemes in video
files.

################################################################################

%package devel
Summary:   Header files and static libraries for faac
Group:     Development/Libraries
Requires:  %{name} = %{version}

%description devel
These are the header files and static libraries from faac that are needed
to build programs that use it.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{ver_major}_%{ver_minor}

sed -e '/obj-type/d' \
    -e '/Long Term/d' \
    -i frontend/main.c

%build
./bootstrap

%{configure} \
    --disable-static \
    --with-mp4v2

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

chrpath --delete %{buildroot}%{_bindir}/faac

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO docs/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/%{name}*.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

################################################################################

%changelog
* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 1.30-0
- https://github.com/knik0/faac/releases/tag/1_30

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.29.9.2-0
- Updated to latest stable release

* Sun Mar 01 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.28-0
- Initial build
