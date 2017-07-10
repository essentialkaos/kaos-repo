###############################################################################

%define _posixroot        /
%define _root             /root
%define _opt              /opt
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

Summary:              A powerful build system for the JVM
Name:                 gradle
Version:              4.0.1
Release:              0%{?dist}
License:              ASL 2.0 
Group:                Development/Tools
URL:                  http://gradle.org

Source0:              https://services.gradle.org/distributions/%{name}-%{version}-src.zip

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        jdk8

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
Gradle is a build tool with a focus on build automation and support for 
multi-language development. If you are building, testing, publishing, and 
deploying software on any platform, Gradle offers a flexible model that can 
support the entire development lifecycle from compiling and packaging code 
to publishing web sites. 

Gradle has been designed to support build automation across multiple languages 
and platforms including Java, Scala, Android, C/C++, and Groovy, and is 
closely integrated with development tools and continuous integration servers 
including Eclipse, IntelliJ, and Jenkins.

###############################################################################

%prep
%setup -q

%build
./gradlew core:build -x integTest --continue --stacktrace

%install
rm -rf %{buildroot}

./gradlew install -Pgradle_installPath=%{buildroot}%{_opt}/%{name}/%{version}

ln -sf %{_opt}/%{name}/%{version} %{buildroot}%{_opt}/%{name}/current

###############################################################################

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_opt}/%{name}/*

###############################################################################

%changelog
* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Updated to latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 3.5-0
- Updated to latest stable release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.1-0
- Updated to latest stable release

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- Updated to latest stable release

* Tue Mar 29 2016 Gleb Goncharov <yum@gongled.me> - 2.12-0
- Initial build
