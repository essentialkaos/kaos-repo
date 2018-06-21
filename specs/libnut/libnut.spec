################################################################################

# rpmbuilder:svn      svn://svn.mplayerhq.hu/nut/src/trunk
# rpmbuilder:revision r690

################################################################################

Summary:            Library for creating and demuxing NUT files
Name:               libnut
Version:            0.0.0
Release:            1%{?dist}
License:            MIT
Group:              Development/Libraries
URL:                http://mplayerhq.hu

Source0:            %{name}-%{version}.tar.gz

Patch0:             %{name}-makefile.patch
Patch1:             %{name}-config.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
NUT is a patent-free, multimedia container format originally conceived
by a few MPlayer and FFmpeg developers that were dissatisfied with the
limitations of all currently available multimedia container formats
such as AVI, Ogg or Matroska.

It aims to be simple, flexible, extensible, compact and error resistant
(error resilient), thus addressing most if not all of the shortcomings
present in alternative formats, like excessive CPU and size overhead,
file size limits, inability to allow fine grained seeking or restrictions
on the type of data they can contain.

################################################################################

%package devel
Summary:            Development files for NUT library
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
libnut is a free library for creating and demuxing NUT files. It
supports frame accurate seeking for active streams, recovery from
errors and dynamic index generation during playback.

################################################################################

%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} PREFIX=%{_prefix} LIBDIR=%{_libdir}

%clean
rm -rf %{buildroot}

################################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/nutmerge
%{_bindir}/nutindex
%{_bindir}/nutparse
%{_libdir}/%{name}.so.0
%{_libdir}/%{name}.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.a
%{_includedir}/%{name}.h

################################################################################

%changelog
* Fri May 13 2016 Gleb Goncharov <inbox@gongled.ru> - 0.0.0-1
- Updated to latest version (r690)

* Fri Apr 15 2016 Gleb Goncharov <inbox@gongled.ru> - 0.0.0-0
- Initial build
