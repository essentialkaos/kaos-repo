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

###############################################################################

%define pkg_name   faad

###############################################################################

Summary:           Library and frontend for decoding MPEG2/4 AAC
Name:              faad2
Version:           2.7
Release:           0%{?dist}
License:           GPLv2
Group:             Applications/Multimedia
URL:               http://www.audiocoding.com

Source0:           http://download.sourceforge.net/faac/%{name}-%{version}.tar.bz2

Patch0:            %{name}-%{version}-mp4ff.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     autoconf automake libtool gcc gcc-c++
BuildRequires:     libsndfile-devel >= 1.0.0 id3lib-devel zlib-devel

Obsoletes:         faad2-libs <= %{version}

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

###############################################################################

%package -n libfaad2
Summary:           Libraries for faad2
Group:             Development/Libraries

Requires:          %{name} = %{version}

%description -n libfaad2
Libraries from faad2 that are needed to build programs that use it.

###############################################################################

%package -n libfaad2-devel
Summary:           Header files for faad2
Group:             Development/Libraries

Requires:          %{name} = %{version}

%description -n libfaad2-devel
Header files from faad2 that are needed to build programs that use it.

###############################################################################

%prep
%setup -q
%patch0 -p1 -b .mp4ff

%build
autoreconf -i

%configure \
  --without-xmms \
  --with-mpeg4ip \
  --with-mp4v2

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/%{pkg_name}
%{_mandir}/manm/%{pkg_name}.man*

%files -n lib%{name}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

###############################################################################

%changelog
* Mon Sep 05 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.7-0
- Initial build. 
