###############################################################################

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

###############################################################################

Summary:         Jansson JSON Library
Name:            jansson
Version:         2.10
Release:         0%{?dist}
License:         MIT
Group:           System Environment/Libraries
URL:             http://www.digip.org/jansson/

Source0:         http://www.digip.org/jansson/releases/%{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc make

Requires:        pkgconfig

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Jansson is a C library for encoding, decoding and manipulating JSON data.

###############################################################################

%package devel

Summary:         Header files for Jansson JSON Library
Requires:        %{name} = %{version}
Group:           Development/Libraries

%description devel
Header files for Jansson JSON Library

###############################################################################

%prep
%setup -q

%build
%{_configure} --libdir=%{_libdir} --includedir=%{_includedir} --disable-static
%{__make} %{?_smp_mflags}

%check
%{__make} check

%install
rm -rf %{buildroot}

%{__make} install INSTALL="install -p" DESTDIR="%{buildroot}"
rm -f %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

###############################################################################

%changelog
* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 2.10-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.9-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Updated to latest stable release

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 2.7-0
- Updated to latest stable release

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 2.6-2
- Initial build
