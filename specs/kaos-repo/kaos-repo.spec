################################################################################

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

%define fm_config         %{_sysconfdir}/yum/pluginconf.d/fastestmirror.conf
%define pr_config         %{_sysconfdir}/yum/pluginconf.d/priorities.conf

################################################################################

Summary:         ESSENTIAL KAOS Public Repo
Name:            kaos-repo
Version:         9.2
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

################################################################################

%description
This package contains yum configuration files for access to ESSENTIAL KAOS
repository.

################################################################################

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
if [[ -f %{fm_config} ]] ; then
  if ! grep -q 'kaos' %{fm_config} ; then
    sed -i 's/^exclude.*/\0, kaos/g' %{fm_config}
    sed -i 's/^#exclude.*/exclude=kaos/g' %{fm_config}
  fi
fi

if [[ -f %{pr_config} ]] ; then
  if ! grep -q 'check_obsoletes=1' ; then
    echo 'check_obsoletes=1' >> %{pr_config}
  fi
fi

if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
  if [[ ! $(grep 'ESSENTIALKAOS' %{_sysconfdir}/abrt/gpg_keys) ]] ; then
    echo "%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ESSENTIALKAOS" >> %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%postun
if [[ $1 -eq 0 ]] ; then
  if [[ -e %{_sysconfdir}/abrt/gpg_keys ]] ; then
    sed -i '/ESSENTIALKAOS/d' %{_sysconfdir}/abrt/gpg_keys
  fi
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

################################################################################

%changelog
* Wed May 29 2019 Anton Novojilov <andy@essentialkaos.com> - 9.2-0
- Added obsoletes check in priorities plugin

* Fri Feb 16 2018 Anton Novojilov <andy@essentialkaos.com> - 9.1-0
- Added bugtracker URL

* Thu Feb 01 2018 Anton Novojilov <andy@essentialkaos.com> - 9.0-0
- Migrated from kaos.io to kaos.st

* Thu Mar 23 2017 Anton Novojilov <andy@essentialkaos.com> - 8.0-0
- Dropped support of x32 arch

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
