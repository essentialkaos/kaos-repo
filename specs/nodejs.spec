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

Summary:        Platform for server side programming on JavaScript
Name:           nodejs
Version:        18.12.1
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://nodejs.org

Source0:        https://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       zlib

BuildRequires:  make python3 openssl-devel zlib-devel

%if 0%{?rhel} <= 7
BuildRequires:  devtoolset-11-gcc-c++ devtoolset-11-libstdc++-devel
%else
BuildRequires:  gcc-c++ libstdc++-devel
%endif

Provides:       %{name} = %{version}-%{release}
Provides:       %{shortname} = %{version}-%{release}
Provides:       %{name}(engine) = %{version}-%{release}
Provides:       npm = %{version}-%{release}

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
%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-11/root/usr/bin:$PATH"
%endif

%{_configure} --prefix=%{_prefix} \
              --shared-zlib \
              --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-11/root/usr/bin:$PATH"
%endif

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
%{_bindir}/corepack
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
* Thu Dec 15 2022 Anton Novojilov <andy@essentialkaos.com> - 18.12.1-0
- https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V18.md#18.12.1
