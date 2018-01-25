################################################################################

Summary:         Wrapper library for the Video Decode and Presentation API
Name:            libvdpau
Version:         1.1.1
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             http://freedesktop.org/wiki/Software/VDPAU

Source0:         http://cgit.freedesktop.org/~aplattner/%{name}/snapshot/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   autoconf automake doxygen graphviz libtool libX11-devel
BuildRequires:   libXext-devel xorg-x11-proto-devel gcc gcc-c++

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
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

%package docs

Summary:         Documentation for libvdpau
BuildArch:       noarch
Provides:        libvdpau-docs = %{version}-%{release}
Obsoletes:       libvdpau-docs < 0.6-2

%description docs
The libvdpau-docs package contains documentation for libvdpau.

################################################################################

%package devel
Summary:        Development files for libvdpau

Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig libX11-devel  

%description devel
The libvdpau-devel package contains libraries and header files for developing
applications that use libvdpau.

################################################################################

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

find %{buildroot} -name '*.la' -delete

# Let %%doc macro create the correct location in the rpm file, creates a
# versioned docdir in <= f19 and an unversioned docdir in >= f20.
rm -rf %{buildroot}%{_docdir}

mv doc/html-out html

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/%{name}_trace.so*

%files docs
%defattr(-,root,root,-)
%doc html

%files devel
%defattr(-,root,root,-)
%{_includedir}/vdpau/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/vdpau.pc

################################################################################

%changelog
* Fri Mar 24 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Initial build for kaos repository
