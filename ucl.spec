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

Summary:            UCL compression library
Name:               ucl
Version:            1.03
Release:            2%{?dist}
License:            GPL
Group:              System Environment/Libraries
URL:                http://www.oberhumer.com/opensource/ucl/

Source0:            http://www.oberhumer.com/opensource/ucl/download/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++

Provides:           %{name} = %{version}-%{release} 

###############################################################################

%description
UCL is a portable lossless data compression library written in ANSI C.
UCL implements a number of compression algorithms that achieve an
excellent compression ratio while allowing *very* fast decompression.
Decompression requires no additional memory.

###############################################################################

%package devel
Summary:            Header files, libraries and development documentation for ucl
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for ucl. If you like to develop programs using ucl,
you will need to install ucl-devel.

###############################################################################

%prep
%setup -q

%build
%configure --enable-shared

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc COPYING NEWS README THANKS TODO
%{_libdir}/libucl.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ucl/
%{_libdir}/libucl.a
%exclude %{_libdir}/libucl.la
%{_libdir}/libucl.so

###############################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.03-0
- Initial build for kaos repository
