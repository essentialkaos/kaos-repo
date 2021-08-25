################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

Summary:            GMerlin Audio Video Library
Name:               gavl
Version:            1.4.0
Release:            1%{?dist}
License:            GPLv2+
Group:              System Environment/Libraries
URL:                http://gmerlin.sourceforge.net/gavl_frame.html

Source0:            https://downloads.sourceforge.net/gmerlin/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      automake make gcc libtool doxygen
BuildRequires:      autoconf >= 2.50 libpng-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
GMerlin Audio Video Library.

################################################################################

%package devel
Summary:            Header files for gavl library
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
This is the package containing the header files for gavl library.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%if 0%{?rhel} >= 7
  sed -i 's/INCLUDES/AM_CPPFLAGS/g' configure.ac
%endif

%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake} --add-missing

%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -Rf %{buildroot}%{_libdir}/*.la
rm -Rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.1

%files devel
%defattr(644,root,root,755)
%{?with_apidocs:%doc doc/apiref}
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

################################################################################

%changelog
* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-1
- Fixed problems with executing ldconfig

* Wed Apr 13 2016 Gleb Goncharov <yum@gongled.me> - 1.4.0-0
- Initial build
