################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define short_name    grafana-zabbix
%define plugin_name   alexanderzobnin-zabbix-app
%define plugins_dir   %{_sharedstatedir}/grafana/plugins

################################################################################

Summary:              Zabbix datasource for Grafana
Name:                 grafana-plugin-zabbix-datasource
Version:              3.10.2
Release:              0%{?dist}
License:              MIT
Group:                Applications/System
URL:                  https://github.com/alexanderzobnin/grafana-zabbix

Source0:              https://github.com/alexanderzobnin/%{short_name}/archive/v%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             grafana

BuildRequires:        nodejs

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
Zabbix datasource plugin provides a support for Zabbix as a backend
database.

################################################################################

%prep
%setup -qn %{short_name}-%{version}

%build
npm install
npm run build

rm -rf node_modules/

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{plugins_dir}/%{plugin_name}

cp -a . %{buildroot}%{plugins_dir}/%{plugin_name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,0755)
%{plugins_dir}/%{plugin_name}

################################################################################

%changelog
* Tue Jul 09 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.10.2-0
- Initial build.
