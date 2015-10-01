###############################################################################

# rpmbuilder:github       moovweb:gvm
# rpmbuilder:revision     bba42f81f917bcfb5947951a861c3e22b7e7783a

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

Summary:           Go Version Manager
Name:              gvm
Version:           1.0.22.1
Release:           0%{?dist}
License:           MIT
Group:             Applications/System
URL:               https://github.com/moovweb/gvm

Source0:           https://github.com/moovweb/%{name}/archive/%{version}.tar.gz
Source1:           %{name}.profile
Source2:           %{name}.script

BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          make gcc bison glibc-devel git curl mercurial

Provides:          %{name} = %{version}-%{release}

Conflicts:         golang

###############################################################################

%description
GVM provides an interface to manage Go versions.

###############################################################################

%prep
%setup -qn %{version}

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_opt}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/profile.d

cp -r bin config scripts VERSION %{buildroot}%{_opt}/%{name}

install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -pm 755 %{SOURCE2} %{buildroot}%{_opt}/%{name}/scripts/%{name}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{_sysconfdir}/profile.d/%{name}.sh
%{_opt}/%{name}

###############################################################################

%changelog
* Fri Jun 12 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.22.1-0
- Used last revision of code from github

* Sat Mar 28 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.22-0
- Initial build
