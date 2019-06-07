################################################################################

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

################################################################################

%define service_dir %{_opt}/%{name}

################################################################################

Summary:           SQL editor & simple business intelligence for Clickhouse
Name:              tabix
Version:           18.07.1
Release:           0%{?dist}
Group:             Applications/Databases
License:           ASL 2.0
URL:               https://tabix.io

Source0:           https://github.com/tabixio/%{name}/archive/%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Tabix - SQL Editor & Open source simple business intelligence for Clickhouse.

Advantages:
- No need to install, works from the browser
- Supports SQL syntax ClickHouse
- Draws charts, charts or maps of the world

################################################################################

%prep
%setup -qn %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{service_dir}

cp -rp build/* %{buildroot}%{service_dir}/
rm -f %{buildroot}%{service_dir}/CNAME

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.md
%{service_dir}

################################################################################

%changelog
* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 18.07.1-0
- Initial build for kaos repository
