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
%define __ldconfig        %{_sbin}/ldconfig
%define __chkconfig       %{_sbin}/chkconfig

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            General-purpose scalable concurrent malloc implementation
Name:               jemalloc
Version:            5.1.0
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            BSD
URL:                http://jemalloc.net

Source0:            https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make libxslt

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of jemalloc.

################################################################################

%package devel

Summary:        Development files for jemalloc
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}

%description devel
The jemalloc-devel package contains libraries and header files for
developing applications that use jemalloc.

################################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

%clean
rm -rf %{buildroot}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%doc COPYING README VERSION
%doc doc/jemalloc.html
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%{_bindir}/%{name}.sh
%{_bindir}/jeprof

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

################################################################################

%changelog
* Sat Mar 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.1.0-0
- Initial build for kaos repository
