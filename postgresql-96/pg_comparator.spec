###############################################################################

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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

###############################################################################

%define pg_maj_ver        96
%define pg_dir            %{_prefix}/pgsql-9.6
%define realname          pg_comparator

###############################################################################


Summary:           Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:              %{realname}%{pg_maj_ver}
Version:           2.2.5
Release:           0%{?dist}
License:           BSD
Group:             Development/Tools
URL:               http://pgfoundry.org/projects/pg-comparator

Source:            http://pgfoundry.org/frs/download.php/3661/%{realname}-%{version}.tgz

Patch0:            %{realname}-Makefile.diff

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc
BuildRequires:     postgresql%{pg_maj_ver}-devel

Requires:          perl(Getopt::Long), perl(Time::HiRes)
Requires:          postgresql%{pg_maj_ver}

Requires(post):    %{_sbindir}/update-alternatives

Provides:          %{realname} = %{version}-%{release}

###############################################################################

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

###############################################################################

%prep
%setup -qn %{realname}-%{version}

%patch0 -p0

%build
%{__make} PG_CONFIG=%{pg_dir}/bin/pg_config

%install
rm -rf %{buildroot}
%{make_install} PG_CONFIG=%{pg_dir}/bin/pg_config

%post
%{_sbindir}/update-alternatives --install /usr/bin/pg_comparator pgcomparator %{pg_dir}/bin/pg_comparator %{pg_maj_ver}0

%postun
if [[ $1 -eq 0 ]] ; then
  %{_sbindir}/update-alternatives --remove pgcomparator %{pg_dir}/bin/pg_comparator
fi

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc %{pg_dir}/doc/contrib/README.%{realname}
%doc %{pg_dir}/doc/contrib/README.pgc_casts
%doc %{pg_dir}/doc/contrib/README.pgc_checksum
%doc %{pg_dir}/doc/contrib/README.xor_aggregate
%{pg_dir}/bin/%{realname}
%{pg_dir}/lib/pgc_casts.so
%{pg_dir}/lib/pgc_checksum.so
%{pg_dir}/share/contrib/*.sql

###############################################################################

%changelog
* Wed May 10 2017 Andrey Kulikov <avk@brewkeeper.net> - 2.2.5-0
- Initial build
