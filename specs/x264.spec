################################################################################

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

################################################################################

%ifarch %ix86
  %define optflags -O2 -g -pipe -Wall -fexceptions -fstack-protector -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -Wp,-D_FORTIFY_SOURCE=2 --param=ssp-buffer-size=4
%endif

################################################################################

# Found X264_BUILD in (x264.h)
%define pkg_build            155
%define pkg_snapshot_date    20180911
%define pkg_snapshot_suffix  2245

%define pkg_snapshot_version %{pkg_snapshot_date}-%{pkg_snapshot_suffix}

################################################################################

Summary:            H.264 (MPEG-4 AVC) encoder library
Name:               x264
Version:            0.%{pkg_build}
Release:            %{pkg_snapshot_date}_0%{?dist}
License:            GPL
Group:              System Environment/Libraries
URL:                http://www.videolan.org/developers/x264.html

Source0:            http://ftp.videolan.org/pub/videolan/%{name}/snapshots/%{name}-snapshot-%{pkg_snapshot_version}-stable.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make nasm >= 2.13 yasm gettext

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
x264 is a free library for encoding H.264/AVC video streams.

################################################################################

%package devel
Summary:            Development files for x264
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Header files and shared libraries for x264.

################################################################################

%prep
%setup -qn %{name}-snapshot-%{pkg_snapshot_version}-stable

%build

# Fail build if header file contains different build version
if [[ $(grep '#define X264_BUILD' x264.h | cut -f3 -d" ") != "%{pkg_build}" ]] ; then
  echo "Header file contains different build version!"
  exit 1
fi

%configure --enable-pic --enable-debug --enable-shared

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

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

################################################################################

%changelog
* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 0.152_20180620-0
- Updated to latest stable snapshot

* Tue Feb 20 2018 Anton Novojilov <andy@essentialkaos.com> - 0.152_20180219-0
- Updated to latest stable snapshot

* Tue Sep 19 2017 Anton Novojilov <andy@essentialkaos.com> - 0.152_20170918-0
- Updated to latest stable snapshot

* Wed Jul 12 2017 Anton Novojilov <andy@essentialkaos.com> - 0.151_20170711-0
- Updated to latest stable snapshot

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 0.150_20170709-0
- Updated to latest stable snapshot

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 0.149_20170321-0
- Updated to latest stable snapshot

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 0.148_20160905-0
- Updated to latest stable snapshot

* Mon Apr 18 2016 Gleb Goncharov <yum@gongled.ru> - 0.148_20160416-0
- Updated to latest stable snapshot
