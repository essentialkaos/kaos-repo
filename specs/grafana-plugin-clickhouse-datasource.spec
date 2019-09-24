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

%define short_name    clickhouse-grafana
%define plugin_name   vertamedia-clickhouse-datasource
%define plugins_dir   %{_sharedstatedir}/grafana/plugins

################################################################################

Summary:              Clickhouse datasource for Grafana
Name:                 grafana-plugin-clickhouse-datasource
Version:              1.9.0
Release:              0%{?dist}
License:              MIT
Group:                Applications/System
URL:                  https://github.com/Vertamedia/clickhouse-grafana

Source0:              https://github.com/Vertamedia/%{short_name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             grafana

BuildRequires:        git nodejs zlib >= 1.2.11

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
ClickHouse datasource plugin provides a support for ClickHouse as a backend
database.

################################################################################

%prep
%setup -qn %{short_name}-%{version}

# Enable alerting support
sed -i 's/\"alerting\": false/\"alerting\": true/g' src/plugin.json

%build
npm install
npm run build:prod

rm -rf node_modules/

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{plugins_dir}/%{plugin_name}

cp -a . %{buildroot}%{plugins_dir}/%{plugin_name}
rm -f %{buildroot}%{plugins_dir}/%{plugin_name}/.gitignore

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,0755)
%{plugins_dir}/%{plugin_name}

################################################################################

%changelog
* Mon Sep 23 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.0-0
- Updated to the latest release

* Wed Apr 17 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.8.1-0
- Initial build
