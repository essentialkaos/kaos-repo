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

Summary:              Generic non-JVM producer and consumer for Apache Kafka 
Name:                 kafkacat
Version:              1.3.1
Release:              0%{?dist}
License:              2-clause BSD
Group:                Development/Libraries
URL:                  https://github.com/edenhill/kafkacat

Source0:              https://github.com/edenhill/%{name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc make librdkafka-devel

Requires:             librdkafka

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
kafkacat is fast and lightweight client for Apache Kafka. 

In producer mode kafkacat reads messages from stdin, delimited with a 
configurable delimeter, and produces them to the provided Kafka cluster, 
topic and partition.

In consumer mode kafkacat reads messages from a topic and partition and prints
them to stdout using the configured message delimiter. 

kafkacat also features a Metadata list mode to display the current state of 
the Kafka cluster and its topics and partitions.

###############################################################################

%prep
%setup -qn %{name}-%{version}

# Fix version number output
sed -i "s/KAFKACAT_VERSION,/\"%{version}\",/" kafkacat.c

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc LICENSE README.md
%{_bindir}/%{name}

###############################################################################

%changelog
* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- Added support for formatter T - message timestamp
- Introduce -E argument (don't exit on error)
- Added offsets_for_times() support (KIP-79): query offset by timestamp with
  -Q -t ..
- Now builds on win32 (VS)
- Use default fallback version if built outside of git repo
- Fix -X dump
- Allow brokers to be specified through -X ..
- Ensure metadata is destroyed in consumer_run
- Temporary QUEUE_FULL should not be consider permanent errors
- Readme Change regarding -X parameter

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Fixed project url
- Added fix for version number output
- Updated to latest version

* Tue Apr 05 2016 Gleb Goncharov <yum@gongled.ru> - 1.2.0-0
- Initial build 
