################################################################################

# rpmbuilder:github       meduketto/iksemel

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
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

Summary:         An XML parser library designed for Jabber applications
Name:            iksemel
Version:         1.5.0
Release:         0%{?dist}
Group:           Development/Tools
License:         LGPLv2+
URL:             https://github.com/meduketto/iksemel

Source0:         %{name}-%{version}.tar.bz2

BuildRequires:   make gcc gcc-c++ bison m4 autoconf automake libtool
BuildRequires:   libgcrypt-devel gnutls-devel pkgconfig texinfo

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
An XML parser library designed for Jabber applications. It is coded in
ANSI C for POSIX compatible environments, thus highly portable.

################################################################################

%package devel

Summary:         Development package for %{name}
Group:           Development/Libraries
Requires:        %{name} = %{version}

%description devel
Use this package for building/developing applications against iksemel.

################################################################################

%prep
%setup -q

%build
autoreconf -fvi
%configure --disable-static --disable-rpath --disable-python

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la

mv %{buildroot}%{_infodir}/%{name} %{buildroot}%{_infodir}/%{name}.info

rm -f %{buildroot}%{_infodir}/dir

%check
%{__make} check

%clean
rm -rf %{buildroot}

%postun
/sbin/ldconfig

%post
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING HACKING NEWS README TODO
%{_infodir}/iksemel.info*
%{_bindir}/ikslint
%{_bindir}/iksperf
%{_bindir}/iksroster

%files devel
%defattr(-,root,root,-)
%{_includedir}/iksemel.h
%{_libdir}/libiksemel.so
%{_libdir}/libiksemel.so.3
%{_libdir}/libiksemel.so.3.1.1
%{_libdir}/pkgconfig/iksemel.pc

################################################################################

%changelog
* Thu Sep 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Initial build for kaos repository
