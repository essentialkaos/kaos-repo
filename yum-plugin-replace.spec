################################################################################

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

################################################################################

Summary:           Package replacement plugin for Yum
Name:              yum-plugin-replace
Version:           0.2.7
Release:           0%{?dist}
License:           GPL
Group:             System Environment/Base
URL:               https://github.com/iuscommunity/yum-plugin-replace

Source0:           https://github.com/iuscommunity/%{name}/archive/%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch
Requires:          yum

################################################################################

%description
This plugin enables the ability to replace an installed package, with another
package that provides the same thing.  It was developed specifically for the
IUS Community Project whose packages have alternative names as to not
automatically upgrade stock packages.  They also do not Obsolete the packages
they provide, therefore making upgrading a little bit more tedious.  For
example upgrading 'mysql' to 'mysql50' or 'mysql51' requires first
uninstalling 'mysql' and then installing the alternate package name. 

################################################################################

%prep
%setup -qn %{name}-%{version}
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/yum/pluginconf.d/ \
         %{buildroot}%{_libdir32}/yum-plugins/


install -pm 0644 etc/yum/pluginconf.d/replace.conf \
    %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -pm 0644 lib/yum-plugins/replace.py \
    %{buildroot}%{_libdir32}/yum-plugins/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README LICENSE ChangeLog
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/replace.conf
%{_libdir32}/yum-plugins/replace.py*

################################################################################

%changelog
* Wed Sep 03 2014 Anton Novojilov <andy@essentialkaos.com> - 2.7.0-0
- Initial build
