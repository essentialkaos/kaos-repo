###############################################################################

# rpmbuilder:github   TimothyGu/libnut
# rpmbuilder:revision f3476bb3ccf5acc1b0be76fc881f1e804c475391

###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __ldconfig        %{_sbin}/ldconfig
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

Summary:            Library for creating and demuxing NUT files
Name:               libnut
Version:            0.0.0
Release:            0%{?dist}
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
such as AVI, Ogg or Matroska. 

It aims to be simple, flexible, extensible, compact and error resistant
(error resilient), thus addressing most if not all of the shortcomings 
present in alternative formats, like excessive CPU and size overhead, 
file size limits, inability to allow fine grained seeking or restrictions 
on the type of data they can contain.

###############################################################################

%package devel
Summary:            Development files for NUT library
Group:              Development/Libraries

Requires:           %{name}-%{version}

%description devel
libnut is a free library for creating and demuxing NUT files. It
supports frame accurate seeking for active streams, recovery from
errors and dynamic index generation during playback.

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
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/nutmerge
%{_bindir}/nutindex
%{_bindir}/nutparse
%{_libdir}/%{name}.so.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_includedir}/%{name}.h

###############################################################################

%changelog
* Fri Apr 15 2016 Gleb Goncharov <yum@gongled.ru> - 0.0.0-0
- Initial build.

