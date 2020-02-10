################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%define shortname         node

################################################################################

Summary:            Platform for server side programming on JavaScript
Name:               nodejs
Version:            12.15.0
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://nodejs.org

Source0:            https://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           zlib

BuildRequires:      make python openssl-devel zlib-devel
BuildRequires:      devtoolset-7-gcc-c++ devtoolset-7-libstdc++-devel

Provides:           %{name} = %{version}-%{release}
Provides:           %{shortname} = %{version}-%{release}
Provides:           %{name}(engine) = %{version}-%{release}
Provides:           npm = %{version}-%{release}

################################################################################

%description
Node.js is a platform built on Chromes JavaScript runtime for
easily building fast, scalable network applications. Node.js
uses an event-driven, non-blocking I/O model that makes it
lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

################################################################################

%package devel

Summary:            Header files for nodejs
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

BuildArch:          noarch

%description devel
This package provides the header files for nodejs.

################################################################################

%prep
%{crc_check}

%setup -qn %{shortname}-v%{version}

%build
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-7/root/usr/bin:$PATH"

%{_configure} --prefix=%{_prefix} \
              --shared-zlib \
              --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-7/root/usr/bin:$PATH"

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%{_bindir}/%{shortname}
%{_bindir}/npm
%{_bindir}/npx
%{_docdir}/%{shortname}/gdbinit
%{_docdir}/%{shortname}/lldb*
%{_mandir}/man1/%{shortname}.1.gz
%{_libdir32}/%{shortname}_modules
%{_datadir}/systemtap/tapset/%{shortname}.stp

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*

################################################################################

%changelog
* Thu Feb 06 2020 Anton Novojilov <andy@essentialkaos.com> - 12.15.0-0
- Updated to the latest stable release

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 12.14.1-0
- Updated to the latest stable release

* Sun Aug 18 2019 Anton Novojilov <andy@essentialkaos.com> - 10.16.3-0
- Updated to the latest stable release

* Fri Mar 01 2019 Anton Novojilov <andy@essentialkaos.com> - 10.15.2-0
- Updated to the latest stable release

* Fri Mar 01 2019 Anton Novojilov <andy@essentialkaos.com> - 10.15.1-0
- Updated to the latest stable release

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 10.15.0-0
- Updated to the latest stable release

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 10.13.0-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 8.12.0-0
- Updated to the latest stable release

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 8.11.3-0
- Updated to the latest stable release

* Tue Apr 03 2018 Anton Novojilov <andy@essentialkaos.com> - 8.10.0-1
- Using GCC from devtoolset-3 for build

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 8.10.0-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 8.9.4-0
- Updated to the latest stable release

* Tue Feb 06 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 8.9.1-1
- Add nodejs(engine) provides tag

* Thu Nov 16 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 8.9.1-0
- Initial build for 8.x
