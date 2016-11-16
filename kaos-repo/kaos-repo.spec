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

%define fmconfig          %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf

##########################################################################

Summary:         ESSENTIAL KAOS Public Repo
Name:            kaos-repo
Version:         7.2
Release:         0%{?dist}
License:         EKOL
Vendor:          ESSENTIALKAOS
Group:           Development/Tools
URL:             https://github.com/essentialkaos/kaos-repo

Source0:         %{name}-%{version}.tar.bz2

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        yum-plugin-priorities

Provides:        %{name} = %{version}-%{release}

##########################################################################

%description
This package contains yum repo file for access to ESSENTIAL KAOS 
repository.

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

install -pm 644 RPM-GPG-KEY-ESSENTIALKAOS \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg

%post
if [[ -f %{fmconfig} ]] ; then
  if [[ -z `grep 'kaos' %{fmconfig}` ]] ; then
    sed -i 's/^exclude.*/\0, kaos/g' %{fmconfig}
    sed -i 's/^#exclude.*/exclude=kaos/g' %{fmconfig}
  fi
fi

if [[ -e /etc/abrt/gpg_keys ]] ; then
  if [[ ! $(grep 'ESSENTIALKAOS' /etc/abrt/gpg_keys) ]] ; then
    echo "%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ESSENTIALKAOS" >> /etc/abrt/gpg_keys
  fi
fi

%postun
if [[ $1 -eq 0 ]] ; then
  if [[ -e /etc/abrt/gpg_keys ]] ; then
    sed -i '/ESSENTIALKAOS/d' /etc/abrt/gpg_keys
  fi
fi

%clean
rm -rf %{buildroot}

##########################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

##########################################################################

%changelog
* Thu Nov 17 2016 Anton Novojilov <andy@essentialkaos.com> - 7.2-0
- Removed mirrors

* Thu Jun 16 2016 Anton Novojilov <andy@essentialkaos.com> - 7.1-0
- Added abrt configuration

* Thu May 05 2016 Anton Novojilov <andy@essentialkaos.com> - 7.0-0
- Added multiver configuration

* Sat Apr 02 2016 Anton Novojilov <andy@essentialkaos.com> - 6.8-1
- Fixed wrong urls of x64 repo

* Sun Oct 12 2014 Anton Novojilov <andy@essentialkaos.com> - 6.8-0
- Changed versioning scheme
