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
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

# Found X264_BUILD in (x264.h)
%define pkg_build            148
%define pkg_snapshot_date    20160417
%define pkg_snapshot_prefix  2245

%define pkg_snapshot_version %{pkg_snapshot_date}-%{pkg_snapshot_prefix}

###############################################################################

Summary:            H.264 (MPEG-4 AVC) encoder library
Name:               x264
Version:            0.%{pkg_build}
Release:            %{pkg_snapshot_date}_0%{?dist}
License:            GPL
Group:              System Environment/Libraries
URL:                http://www.videolan.org/developers/x264.html

Source0:            http://ftp.videolan.org/pub/videolan/%{name}/snapshots/%{name}-snapshot-%{pkg_snapshot_version}-stable.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make nasm yasm gettext

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
x264 is a free library for encoding H.264/AVC video streams.

###############################################################################

%package devel
Summary:            Development files for x264
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Header files and shared libraries for x264.

###############################################################################

%prep
%setup -qn %{name}-snapshot-%{pkg_snapshot_version}-stable

%build
%ifarch %ix86
  %define optflags -O2 -g -pipe -Wall -fexceptions -fstack-protector -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -Wp,-D_FORTIFY_SOURCE=2 --param=ssp-buffer-size=4
%endif

%configure --enable-pic --enable-debug --enable-shared

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/*.txt
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_includedir}/%{name}_config.h
%{_pkgconfigdir}/%{name}.pc

###############################################################################

%changelog
* Mon Apr 18 2016 Gleb Goncharov <yum@gongled.ru> - 0.148_20160416-0
- Update to latest stable snapshot

* Mon Apr 07 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.142-20_20140406.2245
- Update to latest stable snapshot

* Fri Nov 15 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.138-19_20130917.2245
- Update to latest stable snapshot

* Wed Sep 18 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.136-19_20130917.2245
- Update to latest stable snapshot

* Fri May 10 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.130-18_20130509.2245
- Update to latest stable snapshot

* Sat Nov 12 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.118-17_20111111.2245
- Update to latest stable snapshot

* Sat Jun 11 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.115-16_20110610.2245
- Update to latest stable snapshot

* Wed Mar  9 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.114-15_20110308.2245
- Update to latest stable snapshot

* Sat Oct  2 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.106-13_20101001.2245
- Update to latest git

* Tue Jun 22 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.98-12_20100621.2245
- Update to latest git

* Thu Apr  1 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.92-12_20100401.2245
- Update to latest git

* Fri Nov 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.79-11_20091119.2245
- Update to latest git

* Mon Jul 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.68-10_20090719.2245
- Update to latest git

* Sun Nov 16 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.65-8_20081108.2245
- x264-libs from a 3rd party repo generates conflicts

* Sun Nov  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.65-6_20081108.2245
- Update to latest git

* Fri Jun 27 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20080626_2245-5
- Update to latest git

* Tue Feb 26 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20080225_2245-5
- Update to latest svn

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070414_2245-4
- Update to latest svn

* Wed Feb  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070206_2245-3
- Update to latest svn

* Wed Jan  3 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070102_2245-2
- Update to latest svn

* Wed Sep 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20060912_2245-1
- Initial build

