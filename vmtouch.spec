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

Summary:            Portable file system cache diagnostics and control
Name:               vmtouch
Version:            1.0.2
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/hoytech/vmtouch

Source0:            https://github.com/hoytech/%{name}/archive/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description

vmtouch is a tool for learning about and controlling the file system cache 
of unix and unix-like systems. It is BSD licensed so you can basically 
do whatever you want with it.

###############################################################################

%prep
%setup -qn %{name}-%{name}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} \
        PREFIX="%{buildroot}" \
        BINDIR="%{buildroot}%{_sbindir}" \
        MANDIR="%{buildroot}%{_mandir}/man8"

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, -)
%doc CHANGES README.md TODO
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*

###############################################################################

%changelog
* Sat Feb 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Initial build
