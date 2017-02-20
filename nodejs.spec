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

%define shortname         node

###############################################################################

Summary:            Platform for server side programming on JavaScript
Name:               nodejs
Version:            6.9.5
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                http://nodejs.org
Vendor:             Joyent Inc.

Source0:            http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           zlib

BuildRequires:      make gcc clang python >= 2.6 openssl-devel zlib-devel
BuildRequires:      gcc-c++ libstdc++-devel

Provides:           %{name} = %{version}-%{release} 
Provides:           %{shortname} = %{version}-%{release} 
Provides:           npm = %{version}-%{release} 

###############################################################################

%description
Node.js is a platform built on Chromes JavaScript runtime for 
easily building fast, scalable network applications. Node.js 
uses an event-driven, non-blocking I/O model that makes it 
lightweight and efficient, perfect for data-intensive 
real-time applications that run across distributed devices.

###############################################################################

%package devel

Summary:            Header files for nodejs
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

BuildArch:          noarch

%description devel
This package provides the header files for nodejs.

###############################################################################

%prep
%setup -q -n %{shortname}-v%{version}

%build
export CC=clang
export CXX=clang++

%{_configure} --prefix=%{_prefix} \
              --shared-zlib \
              --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%{_bindir}/%{shortname}
%{_bindir}/npm
%{_docdir}/%{shortname}/gdbinit
%{_mandir}/man1/%{shortname}.1.gz
%{_libdir32}/%{shortname}_modules
%{_datadir}/systemtap/tapset/%{shortname}.stp

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*

###############################################################################

%changelog
* Mon Feb 20 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 6.9.5-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 6.9.4-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 6.9.1-0
- Updated to latest stable release

* Mon Jul 11 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 4.4.7-0
- Updated to latest stable release

* Mon Jul 11 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 4.4.6-0
- Updated to latest stable release

* Mon Jul 11 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 4.4.5-0
- Updated to latest stable release

* Wed May 18 2016 Anton Novojilov <andy@essentialkaos.com> - 4.4.4-0
- Updated to latest stable release

* Thu May 05 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 4.4.3-0
- Updated to latest stable release

* Wed Sep  9 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Updated to latest stable release

* Fri Jul 10 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.7-0
- Updated to latest stable release

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.6-0
- Updated to latest stable release

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.5-0
- Updated to latest stable release

* Mon May 25 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.4-0
- Updated to latest stable release

* Fri May 15 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.3-0
- Updated to latest stable release

* Wed Apr 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.2-0
- Updated to latest stable release

* Tue Mar 24 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.1-0
- Updated to latest stable release

* Sat Feb 07 2015 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-0
- Updated to latest stable release
