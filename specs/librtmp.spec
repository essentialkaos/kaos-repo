################################################################################

#rpmbuilder:git           git://git.ffmpeg.org/rtmpdump

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define pkg_name          rtmpdump

################################################################################

Summary:            RTMPDump Real-Time Messaging Protocol API
Name:               librtmp
Version:            2.4
Release:            0%{?dist}
License:            LGPL
Group:              System Environment/Libraries
URL:                https://rtmpdump.mplayerhq.hu

Source0:            %{pkg_name}-%{version}.tgz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make zlib openssl-devel >= 0.9.8

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
The Real-Time Messaging Protocol (RTMP) is used for streaming multimedia
content across a TCP/IP network. This API provides most client functions and
a few server functions needed to support RTMP, RTMP tunneled in HTTP (RTMPT),
encrypted RTMP (RTMPE), RTMP over SSL/TLS (RTMPS) and tunneled variants of
these encrypted types (RTMPTE, RTMPTS).

The basic RTMP specification has been published by Adobe but this API was
reverse-engineered without use of the Adobe specification. As such, it may
deviate from any published specifications but it usually duplicates the actual
behavior of the original Adobe clients.

################################################################################

%package devel
Summary:            Development files for librtmp
Group:              Development/Libraries
License:            LGPL

Requires:           %{name} = %{version}-%{release}

%description devel
This is the package containing the header files for librtmp library.

################################################################################

%package -n rtmpdump
Summary:            A toolkit for RTMP streams
Group:              Applications/Multimedia
License:            GPLv2

Requires:           %{name} = %{version}-%{release}

%description -n rtmpdump
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are
supported, including rtmp://, rtmpt://, rtmpe://, rtmpte://, and
rtmps://.

################################################################################

%prep
%setup -qn %{pkg_name}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} \
  bindir=%{_bindir} \
  sbindir=%{_sbindir} \
  mandir=%{_mandir} \
  incdir=%{_includedir}/librtmp \
  libdir=%{_libdir}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_mandir}/man3/%{name}.3*
%{_libdir}/%{name}.so*
%{_pkgconfigdir}/%{name}.pc

%files devel
%defattr(-,root,root,-)
%{_includedir}/librtmp/*.h
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so

%files -n rtmpdump
%defattr(-,root,root,-)
%{_bindir}/%{pkg_name}
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpsuck
%{_mandir}/man1/%{pkg_name}.1*
%{_mandir}/man8/rtmpgw.8*

################################################################################

%changelog
* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4-0
- Updated to the latest version from official git repository

* Fri Apr 15 2016 Gleb Goncharov <yum@gongled.ru> - 2.3-0
- Initial build
