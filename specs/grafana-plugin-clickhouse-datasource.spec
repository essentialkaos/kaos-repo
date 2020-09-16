################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%define short_name    clickhouse-grafana
%define plugin_name   vertamedia-clickhouse-datasource
%define plugins_dir   %{_sharedstatedir}/grafana/plugins

################################################################################

Summary:              Clickhouse datasource for Grafana
Name:                 grafana-plugin-clickhouse-datasource
Version:              2.1.0
Release:              1%{?dist}
License:              MIT
Group:                Applications/System
URL:                  https://github.com/Vertamedia/clickhouse-grafana

Source0:              https://github.com/Vertamedia/%{short_name}/archive/%{version}.tar.gz

Source100:            checksum.sha512

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             grafana

BuildRequires:        git nodejs golang >= 1.14 zlib >= 1.2.11

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
ClickHouse datasource plugin provides a support for ClickHouse as a backend
database.

################################################################################

%prep
%{crc_check}

%setup -qn %{short_name}-%{version}

%build
npm install
npm run build:prod

GOOS=linux GOARCH=amd64 go build -o dist/vertamedia-clickhouse-plugin_linux_amd64 .

rm -rf node_modules/
rm -f dist/vertamedia-clickhouse-plugin_windows_amd64.exe
rm -f dist/vertamedia-clickhouse-plugin_darwin_amd64

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
* Wed Sep 16 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.1.0-1
- Updated to the latest release

* Wed Sep 09 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.1.0-0
- Updated to the latest release

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- Ad Hoc Filters small adjustments for numeric values
- UI optimizations within Metric builder

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- Ad Hoc Filters improvments

* Sun Oct 20 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.2-0
- Compatibility fix to support grafana 6.4.x
- Ad Hoc Filters fix
- $conditionalTest ALL value option fix

* Mon Sep 23 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.0-0
- Updated to the latest release

* Wed Apr 17 2019 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.8.1-0
- Initial build
