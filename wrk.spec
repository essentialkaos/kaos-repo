########################################################################################

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

########################################################################################

Summary:          HTTP benchmarking tool
Name:             wrk
Version:          4.0.1
Release:          0%{?dist}
License:          Apache 2.0
Group:            Development/Tools
URL:              https://github.com/wg/wrk

Source:           https://github.com/wg/%{name}/archive/%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    make gcc openssl-devel
Requires:         openssl

Provides:         %{name} = %{version}-%{release}

########################################################################################

%description
wrk is a modern HTTP benchmarking tool capable of generating significant
load when run on a single multi-core CPU. It combines a multithreaded
design with scalable event notification systems such as epoll and kqueue.

An optional LuaJIT script can perform HTTP request generation, response
processing, and custom reporting.

########################################################################################

%prep
%setup -q

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_loc_datarootdir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}/scripts

install -pm 755 %{name} %{buildroot}%{_bindir}/

cp scripts/* %{buildroot}%{_loc_datarootdir}/%{name}/scripts/

%clean
%{__rm} -rf %{buildroot}

###########################################################################

%files
%defattr(-, root, root, 0755)
%doc LICENSE README NOTICE
%{_loc_datarootdir}/%{name}/scripts/*
%{_bindir}/%{name}

###########################################################################

%changelog
* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Updated to latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.1.2-0
- Updated to latest release

* Wed Oct 01 2014 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- Initial build
