###############################################################################

Summary:            Library for creating and demuxing NUT files
Name:               libnut
Version:            0.0.0
Release:            0_f3476bb%{?dist}
License:            MIT
Group:              Development/Libraries
URL:                https://github.com/TimothyGu/libnut

Source0:            %{name}-%{version}.tar.gz

Patch0:             %{name}-makefile.patch
Patch1:             %{name}-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:      gcc-c++ make

###############################################################################

%description
NUT is a patent-free, multimedia container format originally conceived
by a few MPlayer and FFmpeg developers that were dissatisfied with the
limitations of all currently available multimedia container formats
such as AVI, Ogg or Matroska. It aims to be simple, flexible,
extensible, compact and error resistant (error resilient), thus
addressing most if not all of the shortcomings present in alternative
formats, like excessive CPU and size overhead, file size limits,
inability to allow fine grained seeking or restrictions on the type of
data they can contain.

libnut is a free library for creating and demuxing NUT files. It
supports frame accurate seeking for active streams, recovery from
errors and dynamic index generation during playback.

###############################################################################

%package devel
Summary:            Development files for NUT library
Group:              Development/Libraries

Requires:           %{name}-%{version}

%description devel
Header file for NUT library.

###############################################################################

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir}

%clean
rm -rf %{buildroot}

###############################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/nutmerge
%attr(755,root,root) %{_bindir}/nutindex
%attr(755,root,root) %{_bindir}/nutparse
%attr(755,root,root) %{_libdir}/libnut.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnut.so
%attr(755,root,root) %{_libdir}/libnut.a
%{_includedir}/libnut.h

###############################################################################

%changelog
* Sat Nov 21 2009 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

