## Extra macros ################################################################

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

%define __sname           skytools
%define __pgver           90
%define __pgdir           /usr/pgsql-9.0

%define __fullver         3.1.1
%define __pyver           2.6

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

## Info ########################################################################

Summary:            PostgreSQL database management tools from Skype
Name:               %{__sname}-90
Version:            3.1
Release:            1%{?dist}
License:            BSD
Group:              Applications/Databases
URL:                http://postgresql.org/
Vendor:             PostgreSQL Foundation

Source0:            http://ftp.postgresql.org/pub/projects/pgFoundry/%{__sname}/%{__sname}/%{__fullver}/%{__sname}-%{__fullver}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           python-psycopg2 postgresql90
BuildRequires:      postgresql90-devel, python-devel

Provides:           %{name} = %{version}-%{release}

%description
Database management tools from Skype:WAL shipping, queueing, replication. 
The tools are named walmgr, PgQ and Londiste, respectively.

################################################################################

%package modules
Summary:            PostgreSQL modules of Skytools
Group:              Applications/Databases
Requires:           %{__sname}-90 = %{version}-%{release}

%description modules
This package has PostgreSQL modules of skytools.

## Build & Install #############################################################

%prep
%setup -q -n %{__sname}-%{__fullver}

%build
%configure --with-pgconfig=%{__pgdir}/bin/pg_config

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} python-install modules-install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

## Files #######################################################################

%files
%defattr(644, root, root, 755)
%attr(755,root,root) %{_bindir}/londiste3
%attr(755,root,root) %{_bindir}/pgqd
%attr(755,root,root) %{_bindir}/qadmin
%attr(755,root,root) %{_bindir}/queue_mover3
%attr(755,root,root) %{_bindir}/queue_splitter3
%attr(755,root,root) %{_bindir}/scriptmgr3
%attr(755,root,root) %{_bindir}/simple_consumer3
%attr(755,root,root) %{_bindir}/simple_local_consumer3
%attr(755,root,root) %{_bindir}/skytools_upgrade3
%attr(755,root,root) %{_bindir}/walmgr3
/usr/lib/python2.6/site-packages/pkgloader-1.0-py2.6.egg-info
/usr/lib/python2.6/site-packages/pkgloader.py*
%dir %{_libdir}/python2.6/site-packages/londiste
%{_libdir}/python2.6/site-packages/londiste/*.py*
%{_libdir}/python2.6/site-packages/londiste/handlers/*.py*
%{_libdir}/python2.6/site-packages/pgq/*.py*
%{_libdir}/python2.6/site-packages/skytools/*.py*
%{_libdir}/python2.6/site-packages/skytools/*.so
%{_libdir}/python2.6/site-packages/pgq/cascade/*.py*
%{_libdir}/python2.6/site-packages/%{__sname}-%{__fullver}-py2.6.egg-info
%{__pgdir}/share/contrib/londiste.sql
%{__pgdir}/share/contrib/londiste.upgrade.sql
%{__pgdir}/share/contrib/newgrants_londiste.sql
%{__pgdir}/share/contrib/newgrants_pgq.sql
%{__pgdir}/share/contrib/newgrants_pgq_coop.sql
%{__pgdir}/share/contrib/newgrants_pgq_ext.sql
%{__pgdir}/share/contrib/newgrants_pgq_node.sql
%{__pgdir}/share/contrib/oldgrants_londiste.sql
%{__pgdir}/share/contrib/oldgrants_pgq.sql
%{__pgdir}/share/contrib/oldgrants_pgq_coop.sql
%{__pgdir}/share/contrib/oldgrants_pgq_ext.sql
%{__pgdir}/share/contrib/oldgrants_pgq_node.sql
%{__pgdir}/share/contrib/pgq.sql
%{__pgdir}/share/contrib/pgq.upgrade.sql
%{__pgdir}/share/contrib/pgq_coop.sql
%{__pgdir}/share/contrib/pgq_coop.upgrade.sql
%{__pgdir}/share/contrib/pgq_ext.sql
%{__pgdir}/share/contrib/pgq_ext.upgrade.sql
%{__pgdir}/share/contrib/pgq_node.sql
%{__pgdir}/share/contrib/pgq_node.upgrade.sql
%{__pgdir}/share/contrib/txid.sql
%{__pgdir}/share/contrib/uninstall_pgq.sql
%{_docdir}/pgsql/contrib/README.pgq
%{_docdir}/pgsql/contrib/README.pgq_ext
%{_docdir}/skytools3/conf/pgqd.ini.templ
%{_docdir}/skytools3/conf/wal-master.ini
%{_docdir}/skytools3/conf/wal-slave.ini
%{_mandir}/man1/londiste3.1.gz
%{_mandir}/man1/pgqd.1.gz
%{_mandir}/man1/qadmin.1.gz
%{_mandir}/man1/queue_mover3.1.gz
%{_mandir}/man1/queue_splitter3.1.gz
%{_mandir}/man1/scriptmgr3.1.gz
%{_mandir}/man1/simple_consumer3.1.gz
%{_mandir}/man1/simple_local_consumer3.1.gz
%{_mandir}/man1/skytools_upgrade3.1.gz
%{_mandir}/man1/walmgr3.1.gz
%{_datadir}/skytools3/extra/v3.0_pgq_core.sql
%{_datadir}/skytools3/londiste.sql
%{_datadir}/skytools3/londiste.upgrade.sql
%{_datadir}/skytools3/pgq.sql
%{_datadir}/skytools3/pgq.upgrade.sql
%{_datadir}/skytools3/pgq_coop.sql
%{_datadir}/skytools3/pgq_coop.upgrade.sql
%{_datadir}/skytools3/pgq_ext.sql
%{_datadir}/skytools3/pgq_ext.upgrade.sql
%{_datadir}/skytools3/pgq_node.sql
%{_datadir}/skytools3/pgq_node.upgrade.sql

%files modules
%{__pgdir}/lib/pgq_lowlevel.so
%{__pgdir}/share/contrib/pgq_lowlevel.sql
%{__pgdir}/lib/pgq_triggers.so
%{__pgdir}/share/contrib/pgq_triggers.sql

## Changelog ###################################################################

%changelog
* Wed Dec 19 2012 Anton Novojilov <andy@essentialkaos.com> - 3.1-1
- Rebuilded for PostgreSQL 9.0