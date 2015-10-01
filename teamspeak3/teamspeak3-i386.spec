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

%define service_user         teamspeak
%define service_group        teamspeak

###############################################################################

Summary:            VoIP communication system
Name:               teamspeak3
Version:            3.0.11.2
Release:            0%{?dist}
License:            Copyright (c) TeamSpeak Systems GmbH
Group:              Applications/Communications
URL:                http://www.teamspeak.com

Source0:            http://dl.4players.de/ts/releases/%{version}/%{name}-server_linux-x86-%{version}.tar.gz
Source1:            %{name}.init
Source2:            %{name}.sysconfig

BuildArch:          i386
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           kaosv >= 2.5.1

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
TeamSpeak is proprietary voice-over-Internet Protocol (VoIP) software that 
allows computer users to speak on a chat channel with fellow computer users, 
much like a telephone conference call.

###############################################################################

%prep
%setup -q -n %{name}-server_linux-x86

%build

%install
%{__rm} -rf %{buildroot}

install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -dm 755 %{buildroot}%{_opt}/%{name}/

cp ts3server_linux_x86 %{buildroot}%{_opt}/%{name}/ts3server
cp *.so %{buildroot}%{_opt}/%{name}/
cp -r sql redist doc %{buildroot}%{_opt}/%{name}/

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin -d %{_opt}/%{name} %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  chown %{service_user}:%{service_group} %{_opt}/%{name} -R
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%{_opt}/%{name}/*

###############################################################################

%changelog
* Sat Feb 21 2015 Anton Novojilov <andy@essentialkaos.com> - 3.0.11.2-0
- Initial build
