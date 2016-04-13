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

Summary:         Let's Encrypt client
Name:            lego
Version:         0.3.0
Release:         0%{?dist}
Group:           Development/Tools
License:         MIT
URL:             https://github.com/xenolf/%{name}

Source0:         %{name}.tar.bz2

BuildRequires:   golang >= 1.4

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Let's Encrypt client written in Go.

###############################################################################

%prep
%setup -qn %{name}

%build
export GOPATH=$(pwd)

mkdir -p src

mv github.com src
mv golang.org src
mv google.golang.org src
mv gopkg.in src

pushd src/github.com/xenolf/%{name}
go build
popd

mv src/github.com/xenolf/%{name}/%{name} %{name}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}

install -pm 755 %{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/%{name}

###############################################################################

%changelog
* Wed Mar 23 2016 Gleb Goncharov <yum@gongled.me> - 0.3.0-0
- Updated to latest release.

* Sun Jan 31 2016 Gleb Goncharov <yum@gongled.me> - 0.2.0-1
- Added certificates path 

* Fri Jan 22 2016 Gleb Goncharov <yum@gongled.me> - 0.2.0-0
- Initial build 
