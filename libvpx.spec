################################################################################

%global majorver 1
%global minorver 7
%global patchver 0

%ifarch %{ix86}
%global vpxtarget x86-linux-gcc
%else
%global vpxtarget x86_64-linux-gcc
%endif

################################################################################

Summary:            VP8/VP9 Video Codec SDK
Name:               libvpx
Version:            %{majorver}.%{minorver}.%{patchver}
Release:            0%{?dist}
License:            BSD
Group:              System Environment/Libraries
URL:                https://chromium.googlesource.com/webm/libvpx/

Source:             https://chromium.googlesource.com/webm/%{name}/+archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc nasm

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications
with the VP8/VP9 video codec, a high quality, royalty free, open source codec
deployed on millions of computers and devices worldwide.

################################################################################

%package devel
Summary:            Development files for libvpx
Group:              Development/Libraries
Requires:           %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
libvpx.

################################################################################

%package utils
Summary:            VP8/VP9 utilities and tools
Group:              Development/Tools
Requires:           %{name}%{?_isa} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8/VP9, including a sample encoder
and decoder.

################################################################################

%prep
%setup -cqn %{name}-%{version}

%build
./configure --target=%{vpxtarget} \
            --enable-pic \
            --disable-install-srcs \
            --as=nasm \
            --enable-shared \
            --prefix=%{_prefix} \
            --libdir=%{_libdir}

# Hack our optflags in.
sed -i "s|-O3|%{optflags}|g" libs-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" examples-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" docs-%{vpxtarget}.mk

%{__make} %{?_smp_mflags} verbose=true target=libs

%install
rm -rf %{buildroot}

%{__make} DIST_DIR=%{buildroot}%{_prefix} dist

pushd %{buildroot}%{_usr}
# Stuff we don't need.
rm -rf build/ md5sums.txt lib*/*.a CHANGELOG README
chmod 755 bin/*
popd

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/*

################################################################################

%changelog
* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Initial build for kaos repository
