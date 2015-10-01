###############################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0002

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

Summary:         A software platform for processing vast amounts of data
Name:            hadoop
Version:         2.5.2
Release:         0%{?dist}
License:         ASL 2.0 and BSD
Group:           Development/Tools
URL:             http://hadoop.apache.org

Source0:         %{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        jre8

AutoReq:         no

###############################################################################

%description
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

###############################################################################

%prep
%setup -q

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_opt}/%{name}-%{version}

rm -rf share/doc/

cp -r bin %{buildroot}%{_opt}/%{name}-%{version}/
cp -r etc %{buildroot}%{_opt}/%{name}-%{version}/
cp -r include %{buildroot}%{_opt}/%{name}-%{version}/
cp -r lib %{buildroot}%{_opt}/%{name}-%{version}/
cp -r libexec %{buildroot}%{_opt}/%{name}-%{version}/
cp -r sbin %{buildroot}%{_opt}/%{name}-%{version}/
cp -r share %{buildroot}%{_opt}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.txt
%{_opt}/%{name}-%{version}

###############################################################################

%changelog
* Tue Dec 09 2014 Anton Novojilov <andy@essentialkaos.com> - 2.5.2-0
- Initial build
