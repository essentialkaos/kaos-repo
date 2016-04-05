###############################################################################

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
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

%define realname       rdkafka
%define minor_ver      1
%define rel            0

###############################################################################

Summary:             Apache Kafka C/C++ client library
Name:                librdkafka
Version:             0.9.0.99
Release:             0%{?dist}
License:             2-clause BSD
Group:               Development/Libraries
URL:                 https://github.com/edenhill/librdkafka

Source0:             https://github.com/edenhill/%{name}/archive/%{version}.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       gcc make zlib

###############################################################################

%description
C library implementation of the Apache Kafka protocol, containing both 
Producer and Consumer support. It was designed with message delivery 
reliability and high performance in mind, current figures exceed 
800000 msgs/second for the producer and 3 million msgs/second for the consumer.

###############################################################################

%package devel
Summary:             Header files and libraries for librdkafka C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel
The %{name}-devel package contains the header files and
libraries to develop applications using a Kafka databases.

###############################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc README.md LICENSE INTRODUCTION.md CONFIGURATION.md
%{_libdir}/%{name}.so
%{_libdir}/%{name}.so.%{minor_ver}
%{_libdir}/%{name}++.so
%{_libdir}/%{name}++.so.%{minor_ver}

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*
%{_libdir}/%{name}.a
%{_libdir}/%{name}++.a
%{_libdir}/%{name}.so
%{_libdir}/%{name}++.so
%{_pkgconfigdir}/%{realname}.pc
%{_pkgconfigdir}/%{realname}++.pc

###############################################################################

%changelog
* Tue Apr 05 2016 Gleb Goncharov <yum@gongled.ru> - 0.9.0.99-0 
- Initial build 

