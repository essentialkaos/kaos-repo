###############################################################################

# rpmbuilder:relative-pack true

###############################################################################

%define  debug_package %{nil}

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

Summary:         VULnerability Scanner
Name:            vuls
Version:         0.1.7
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv3
URL:             https://github.com/future-architect/vuls

Source0:         %{name}-%{version}.tar.bz2
Source1:         go-cve-dictionary.tar.bz2

BuildRequires:   golang >= 1.6

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        sqlite

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Vulnerability scanner for Linux/FreeBSD, agentless, written in golang

###############################################################################

%prep
%setup -q

%{__tar} xjfv %{SOURCE1}

%build
mkdir -p .src
mv go-cve-dictionary/* .src/
rm -rf go-cve-dictionary
cp -r * .src/
rm -rf *
mv .src src

export GOPATH=$(pwd)

go build -o %{name} src/github.com/future-architect/vuls/main.go
go build -o go-cve-dictionary src/github.com/kotakanbe/go-cve-dictionary/main.go

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_logdir}/%{name}

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 755 go-cve-dictionary %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%dir %{_logdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/go-cve-dictionary

###############################################################################

%changelog
* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.1.7-0
- Updated to latest stable release

* Thu Oct 06 2016 Anton Novojilov <andy@essentialkaos.com> - 0.1.6-0
- Initial build for kaos repository
