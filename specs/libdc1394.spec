################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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

################################################################################

Summary:             1394-based digital camera control library
Name:                libdc1394
Version:             2.2.6
Release:             0%{?dist}
License:             LGPLv2+
Group:               System Environment/Libraries
URL:                 https://sourceforge.net/projects/libdc1394/

Source0:             https://downloads.sourceforge.net/project/%{name}/%{name}-2/%{version}/%{name}-%{version}.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       make gcc doxygen libX11-devel libXv-devel
BuildRequires:       kernel-headers libraw1394-devel libusb1-devel

Provides:            %{name} = %{version}-%{release}

################################################################################

%description
Libdc1394 is a library that is intended to provide a high level programming
interface for application developers who wish to control IEEE 1394 based
cameras that conform to the 1394-based Digital Camera Specification.

################################################################################

%package devel
Summary:             Header files and libraries for libdc1394
Group:               Development/Libraries

Requires:            %{name} = %{version}-%{release}
Requires:            libraw1394-devel pkgconfig

%description devel
This package contains the header files and libraries
for libdc1394. If you like to develop programs using libdc1394,
you will need to install libdc1394-devel.

################################################################################

%package docs
Summary:             Development documentation for libdc1394
Group:               Documentation

%description docs
This package contains the development documentation for libdc1394.

################################################################################

%package tools
Summary:             Tools for use with libdc1394
Group:               Applications/System

Requires:            %{name} = %{version}-%{release}

%description tools
This package contains tools that are useful when working and
developing with libdc1394.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static --enable-doxygen-html --enable-doxygen-dot

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}
%{__make} doc

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

for p in grab_color_image grab_gray_image grab_partial_image ladybug grab_partial_pvn ; do
  install -pm 0644 -s examples/.libs/$p %{buildroot}%{_bindir}/dc1394_$p
done

install -pm 0644 examples/dc1394_multiview %{buildroot}%{_bindir}/dc1394_multiview

for f in grab_color_image grab_gray_image grab_partial_image ; do
  mv %{buildroot}%{_mandir}/man1/$f.1 %{buildroot}%{_mandir}/man1/dc1394_$f.1
done

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

################################################################################

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libdc1394*.so.*

%files devel
%defattr(-, root, root, -)
%doc examples/*.h examples/*.c
%{_includedir}/dc1394/
%{_libdir}/libdc1394*.so
%{_libdir}/pkgconfig/%{name}-2.pc
%exclude %{_libdir}/*.la

%files docs
%defattr(-, root, root, -)
%doc doc/html/*

%files tools
%defattr(-, root, root, -)
%{_bindir}/dc1394_*
%{_mandir}/man1/dc1394_*.1.gz

################################################################################

%changelog
* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.6-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.5-0
- Updated to the latest stable release

* Sat Nov 26 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2.4-0
- Initial build for kaos repo
