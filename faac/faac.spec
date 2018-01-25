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

################################################################################

Summary:           ISO/MPEG 2/4 AAC Encoder library
Name:              faac
Version:           1.28
Release:           0%{?dist}
License:           LGPL
Group:             Applications/Multimedia
URL:               http://www.audiocoding.com

Source0:           http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

Patch0:            %{name}-%{version}-glibc_fixes-1.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf automake make libtool gcc gcc-c++

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
FAAC is an encoder for a lossy sound compression scheme specified in MPEG-2
Part 7 and MPEG-4 Part 3 standards and known as Advanced Audio Coding (AAC).

This encoder is useful for producing files that can be played back on iPod.
Moreover, iPod does not understand other sound compression schemes in video
files.

################################################################################

%package devel
Summary:           Header files and static libraries for faac.
Group:             Development/Libraries
Requires:          %{name} = %{version}

%description devel
These are the header files and static libraries from faac that are needed
to build programs that use it.

################################################################################

%prep
%setup -q
%patch0 -p1 -b .glibc_fixes-1

sed -e '/obj-type/d' \
    -e '/Long Term/d' \
    -i frontend/main.c

%build
./bootstrap

%configure \
    --disable-static \
    --with-mp4v2

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
* Sun Mar 01 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.28-0
- Initial build
