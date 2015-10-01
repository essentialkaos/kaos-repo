##########################################################################

%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

##########################################################################

Summary:         ATrpms Repo
Name:            atrpms-repo
Version:         6.5
Release:         3%{?dist}
License:         GPLv3
Vendor:          ATrpms.net
Group:           System Environment/Base
URL:             http://ATrpms.net

Source0:         %{name}-%{version}.tar.bz2

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

##########################################################################

%description
This package contains yum repo file for access to ATrpms public repository.

##########################################################################

%prep
%setup -q
%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -dm 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -pm 644 *.repo \
                %{buildroot}%{_sysconfdir}/yum.repos.d/

install -pm 644 RPM-GPG-KEY-atrpms \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg


%clean
rm -rf %{buildroot}

##########################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

##########################################################################

%changelog
* Thu Sep 17 2015 Anton Novojilov <andy@essentialkaos.com> - 6.5-3
- Removed debug_info repo

* Tue Sep 15 2015 Anton Novojilov <andy@essentialkaos.com> - 6.5-2
- Changed base url to Yandex mirror

* Sun Oct 12 2014 Anton Novojilov <andy@essentialkaos.com> - 6.5-1
- Improved spec

* Fri Sep 19 2014 Anton Novojilov <andy@essentialkaos.com> - 6.5-0
- Initial build
