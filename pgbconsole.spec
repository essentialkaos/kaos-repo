###############################################################################

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

###############################################################################

Summary:            Top-like console for Pgbouncer
Name:               pgbconsole
Version:            0.1.1
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/lesovsky/pgbconsole

Source0:            https://github.com/lesovsky/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc postgresql94-devel ncurses-devel

Provides:           %{name} = %{version}-%{release} 

###############################################################################

%description
pgbConsole is the top-like console for Pgbouncer - PostgreSQL connection 
pooler. 

Features:
- top-like interface
- show information about client/servers connections, pools/databases info 
  and statistics.
- ability to perform admin commands, such as pause, resume, reload 
  and others.
- ability to show log files or edit configuration in local pgbouncers.
- see details in doc directory.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags} PGCONFIG=%{_prefix}/pgsql-9.4/bin/pg_config

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

%{make_install}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md
%{_bindir}/%{name}

###############################################################################

%changelog
* Thu Jun 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.1-0
- Initial build
