########################################################################################

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

########################################################################################

%define pg_maj_ver        10
%define pg_low_fullver    10.0
%define pg_dir            %{_prefix}/pgsql-10

%define realname          pg_repack

########################################################################################

Summary:           Reorganize tables in PostgreSQL databases without any locks
Name:              %{realname}%{pg_maj_ver}
Version:           1.4.2
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               http://pgxn.org/dist/pg_repack/

Source0:           http://api.pgxn.org/dist/%{realname}/%{version}/%{realname}-%{version}.zip

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc openssl-devel readline-devel
BuildRequires:     postgresql%{pg_maj_ver}-devel = %{pg_low_fullver}
BuildRequires:     postgresql%{pg_maj_ver}-libs = %{pg_low_fullver}

Requires:          postgresql%{pg_maj_ver}

Provides:          %{realname} = %{version}-%{release}

########################################################################################

%description
pg_repack can re-organize tables on a postgres database without any locks so that
you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

########################################################################################

%prep
%setup -qn %{realname}-%{version}

%build
%{__make} %{?_smp_mflags} PG_CONFIG=%{pg_dir}/bin/pg_config

%install
rm -rf %{buildroot}
%{make_install} PG_CONFIG=%{pg_dir}/bin/pg_config

%post
%{__ldconfig}

%postun
%{__ldconfig}

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-,root,root)
%doc COPYRIGHT doc/pg_repack.rst
%attr (755,root,root) %{pg_dir}/bin/pg_repack
%attr (755,root,root) %{pg_dir}/lib/pg_repack.so
%{pg_dir}/share/extension/%{realname}--%{version}.sql
%{pg_dir}/share/extension/%{realname}.control

########################################################################################

%changelog
* Tue Nov 28 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Initial build for kaos repo
