################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global _vpath_srcdir   .
%global _vpath_builddir %{_target_platform}

################################################################################

Summary:         Wrapper library for the Video Decode and Presentation API
Name:            libvdpau
Version:         1.5
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             https://freedesktop.org/wiki/Software/VDPAU

Source0:         https://gitlab.freedesktop.org/vdpau/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   doxygen graphviz libtool libX11-devel meson
BuildRequires:   libXext-devel xorg-x11-proto-devel gcc gcc-c++

%if 0%{?rhel} >= 7
BuildRequires:   tex(latex)
%else
BuildRequires:   tetex-latex
%endif

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
VDPAU is the Video Decode and Presentation API for UNIX. It provides an
interface to video decode acceleration and presentation hardware present in
modern GPUs.

################################################################################

%package devel
Summary:         Development files for libvdpau
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig libX11-devel

%description devel
The libvdpau-devel package contains libraries and header files for developing
applications that use libvdpau.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{meson} -D documentation=false
%{meson_build}

%install
rm -rf %{buildroot}

%{meson_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/%{name}_trace.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/vdpau/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/vdpau.pc

################################################################################

%changelog
* Sat Dec 10 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- https://gitlab.freedesktop.org/vdpau/libvdpau/-/releases/1.5

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3-0
- https://gitlab.freedesktop.org/vdpau/libvdpau/-/releases/1.3

* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2-0
- https://gitlab.freedesktop.org/vdpau/libvdpau/-/tags/libvdpau-1.2

* Fri Mar 24 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Initial build for kaos repository
