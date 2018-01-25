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

################################################################################

%define shortname         dict

################################################################################

Summary:         ANSI C library of key-value data structures with generic interfaces
Name:            lib%{shortname}
Version:         0.2.1
Release:         0%{?dist}
License:         MIT
Group:           System Environment/Libraries
URL:             https://github.com/fmela/libdict

Source0:         https://github.com/essentialkaos/%{name}/archive/%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        pkgconfig
BuildRequires:   clang make

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
libdict is a small C library that provides access to RFC2229
dictionary servers. This is done through a series of functions, each
representing a major function of the dict server.

################################################################################

%package devel

Summary:         Header files and static libraries for libdict
Group:           System Environment/Libraries

Requires:        %{name} = %{version}-%{release}

%description devel
Header files and static libraries for libdict.

################################################################################

%prep
%setup -q

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} install INSTALL_PREFIX=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%{_libdir}/libdict.so
%{_libdir}/libdict.so.2

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*
%{_libdir}/libdict.a
%{_libdir}/libdict_p.a

################################################################################

%changelog
* Thu Mar 13 2014 Anton Novojilov <andy@essentialkaos.com> - 0.2.1-0
- Initial build
