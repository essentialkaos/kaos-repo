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

Summary:           Timezone Updater Tool
Name:              tzupdater
Version:           2.0.3
Release:           2015b%{?dist}
License:           http://www.oracle.com/technetwork/java/javasebusiness/downloads/tzupdater-lic-354297.txt
Group:             Applications/Databases
URL:               http://www.oracle.com

Source0:           %{name}.jar
Source1:           %{name}

BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:          %{name} = %{version}-%{release}

########################################################################################

%description
The TZUpdater tool is provided to allow you to update installed Java Development Kit 
(JDK) and Java Runtime Environment (JRE) software with more recent timezone data, 
to accommodate daylight saving time (DST) changes in different countries.

########################################################################################

%prep
%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sbindir}
install -dm 755 %{buildroot}%{_loc_datarootdir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}

install -pm 644 %{SOURCE0} %{buildroot}%{_loc_datarootdir}/%{name}/
install -pm 755 %{SOURCE1} %{buildroot}%{_sbindir}/

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-, root, root, -)
%{_loc_datarootdir}/%{name}/%{name}.jar
%{_sbindir}/%{name}

########################################################################################

%changelog
* Mon Mar 21 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-2015b
- Updated to latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-2015a
- Updated to latest release

* Sat Oct 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-2014h
- Initial build
