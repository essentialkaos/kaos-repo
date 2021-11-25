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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define pg_ver            14
%define pg_maj_ver        14
%define pg_low_fullver    14.0
%define pg_dir            %{_prefix}/pgsql-14
%define realname          pg_comparator

################################################################################


Summary:           Efficient table content comparison and synchronization for PostgreSQL %{pg_ver}
Name:              %{realname}%{pg_maj_ver}
Version:           2.3.2
Release:           0%{?dist}
License:           BSD
Group:             Development/Tools
URL:               https://www.cri.ensmp.fr/people/coelho/pg_comparator

Source:            https://www.cri.ensmp.fr/people/coelho/pg_comparator/%{realname}-%{version}.tgz

Patch0:            %{realname}-Makefile.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc
BuildRequires:     postgresql%{pg_maj_ver}-devel = %{pg_low_fullver}
BuildRequires:     postgresql%{pg_maj_ver}-libs = %{pg_low_fullver}

%if 0%{?rhel} == 8
BuildRequires:     llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?rhel} == 7
BuildRequires:     llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 4.0.1
%endif

Requires:          perl(Getopt::Long), perl(Time::HiRes)
Requires:          postgresql%{pg_maj_ver}

Requires(post):    %{_sbindir}/update-alternatives

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

################################################################################

%prep
%setup -qn %{realname}-%{version}

%patch0 -p1

%build
%{__make} %{?_smp_mflags} PG_CONFIG=%{pg_dir}/bin/pg_config

%install
rm -rf %{buildroot}
%{make_install} PG_CONFIG=%{pg_dir}/bin/pg_config

%post
%{_sbindir}/update-alternatives --install %{_bindir}/pg_comparator pgcomparator %{pg_dir}/bin/pg_comparator %{pg_maj_ver}0

%postun
if [[ $1 -eq 0 ]] ; then
  %{_sbindir}/update-alternatives --remove pgcomparator %{pg_dir}/bin/pg_comparator
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc %{pg_dir}/doc/extension/README.pg_comparator
%{pg_dir}/bin/pg_comparator
%{pg_dir}/lib/pgcmp.so
%{pg_dir}/share/extension/*.sql
%{pg_dir}/share/extension/pgcmp.control
%{pg_dir}/lib/bitcode/*

################################################################################

%changelog
* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- Initial build for kaos-repo