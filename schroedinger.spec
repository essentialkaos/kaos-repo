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

Summary:            Portable libraries for the high quality Dirac video codec
Name:               schroedinger
Version:            1.0.11
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            LGPL
URL:                http://www.diracvideo.org

Source0:            http://www.diracvideo.org/download/%{name}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool 
BuildRequires:      orc-devel >= 0.4.10 glew-devel >= 1.5.1

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
The Schrödinger project will implement portable libraries for the high
quality Dirac video codec created by BBC Research and Development. 
Dirac is a free and open source codec producing very high image quality video.

The Schrödinger project is a project done by BBC R&D and Fluendo in
order to create a set of high quality decoder and encoder libraries
for the Dirac video codec.

###############################################################################

%package devel
Summary:            Development files for schroedinger
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Development files for schroedinger.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static

sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

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
%doc COPYING* NEWS TODO
%{_libdir}/lib%{name}-*.so.*

###############################################################################

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-*
%{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/%{name}-*.pc

###############################################################################

%changelog
* Wed Apr 20 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-0
- Updated to latest stable release

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.10-0
- Updated to latest version

* Tue Apr 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-2
- Added dependency on gtk-doc

* Fri Mar 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9
- Dropped dependency on liboil
- Added dependency on orc

* Mon Feb  1 2010 Nicolas CHauvet <kwizart@fedoraproject.org> - 1.0.8-4
- Remove gstreamer-plugins-schroedinger 
  Obsoleted by gst-plugins-bad-free introduction in Fedora.

* Sun Oct 25 2009 kwizart < kwizart at gmail.com > - 1.0.8-3
- Re-introduce gstreamer sub-package until seen in -good

* Tue Oct 20 2009 kwizart < kwizart at gmail.com > - 1.0.8-2
- Update to 1.0.8
- gstreamer-plugins-schroedinger is now in bad.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.7-1
- Update to 1.0.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-4
- Fix some typos [BZ#469133]

* Fri Sep 12 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-3
- Bump release and rebuild against latest gstreamer-* packages to pick
- up special gstreamer codec provides.

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.5-2
- fix license tag

* Wed Aug 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-1
- Update to 1.0.5

* Fri Jul  2 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-2
- Devel subpackage needs to require liboil-devel.

* Fri Jun 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-1
- Update to 1.0.3.
- Update URLs.

* Fri Feb 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.0-1
- Update to 1.0.0

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-2
- Rebuild for GCC 4.3

* Mon Nov 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-1
- Update to 0.9.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.6.1-3
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-2
- Fix license field
- Add pkgconfig as a requirement for the devel subpackage

* Sun Jun 10 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-1
- First version for Fedora
