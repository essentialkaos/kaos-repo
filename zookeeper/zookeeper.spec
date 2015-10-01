###############################################################################

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

###############################################################################

Summary:         A high-performance coordination service for distributed applications
Name:            zookeeper
Version:         3.4.6
Release:         0%{?dist}
License:         ASL 2.0 and BSD
Group:           Development/Tools
URL:             http://zookeeper.apache.org

Source0:         %{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch

Requires:        jre8

AutoReq:         no

###############################################################################


%description
ZooKeeper is a centralized service for maintaining configuration information, 
naming, providing distributed synchronization, and providing group services. 
All of these kinds of services are used in some form or another by distributed 
applications. Each time they are implemented there is a lot of work that goes 
into fixing the bugs and race conditions that are inevitable. Because of the 
difficulty of implementing these kinds of services, applications initially 
usually skimp on them ,which make them brittle in the presence of change and 
difficult to manage. Even when done correctly, different implementations of 
these services lead to management complexity when the applications are 
deployed.

###############################################################################

%prep
%setup -q

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_opt}/%{name}-%{version}

rm -rf doc

cp -r bin %{buildroot}%{_opt}/%{name}-%{version}/
cp -r conf %{buildroot}%{_opt}/%{name}-%{version}/
cp -r contrib %{buildroot}%{_opt}/%{name}-%{version}/
cp -r dist-maven %{buildroot}%{_opt}/%{name}-%{version}/
cp -r recipes %{buildroot}%{_opt}/%{name}-%{version}/
cp -r src %{buildroot}%{_opt}/%{name}-%{version}/
cp -r %{name}-%{version}.* %{buildroot}%{_opt}/%{name}-%{version}/
cp -r ivy.xml ivysettings.xml %{buildroot}%{_opt}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt NOTICE.txt README.txt
%{_opt}/%{name}-%{version}

###############################################################################

%changelog
* Tue Dec 09 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.6-0
- Initial build
