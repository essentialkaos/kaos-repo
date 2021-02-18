################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __sysctl          %{_bindir}/systemctl

################################################################################

%define maj_ver           2.2
%define pg_maj_ver        10
%define pg_high_ver       10
%define pg_low_fullver    10.0
%define pg_dir            %{_prefix}/pgsql-%{pg_high_ver}
%define realname          slony1
%define username          postgres
%define groupname         postgres

%global __perl_requires   %{SOURCE2}

################################################################################

Summary:           A "master to multiple slaves" replication system with cascading and failover
Name:              %{realname}-%{pg_maj_ver}
Version:           2.2.10
Release:           0%{?dist}
License:           BSD
Group:             Applications/Databases
URL:               https://www.slony.info

Source0:           https://www.slony.info/downloads/%{maj_ver}/source/%{realname}-%{version}.tar.bz2
Source2:           filter-requires-perl-Pg.sh
Source3:           %{realname}.init
Source4:           %{realname}.sysconfig
Source5:           %{realname}.service

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc byacc flex chrpath
BuildRequires:     postgresql%{pg_maj_ver}-devel = %{pg_low_fullver}
BuildRequires:     postgresql%{pg_maj_ver}-server = %{pg_low_fullver}
BuildRequires:     postgresql%{pg_maj_ver}-libs = %{pg_low_fullver}

Requires:          postgresql%{pg_maj_ver}-server perl-DBD-Pg kaosv >= 2.16
Requires:          systemd

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Slony-I is a "master to multiple slaves" replication system for PostgreSQL with
cascading and failover.

The big picture for the development of Slony-I is to build a master-slave system
that includes all features and capabilities needed to replicate large databases
to a reasonably limited number of slave systems.

Slony-I is a system for data centers and backup sites, where the normal mode of
operation is that all nodes are available.

################################################################################

%prep
%{crc_check}

%setup -qn %{realname}-%{version}

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS

export LIBNAME=%{_lib}

%configure --prefix=%{pg_dir} \
           --includedir %{pg_dir}/include \
           --with-pgconfigdir=%{pg_dir}/bin \
           --libdir=%{pg_dir}/lib \
           --with-perltools=%{pg_dir}/bin \
           --sysconfdir=%{_sysconfdir}/%{realname}-%{pg_maj_ver} \
           --datadir=%{pg_dir}/share \
           --with-pglibdir=%{pg_dir}/lib

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/%{realname}-%{pg_maj_ver}
install -pm 644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon.conf
install -pm 644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon_tools.conf

# Fix the log path
sed "s:\([$]LOGDIR = '/var/log/slony1\):\1-%{pg_maj_ver}:" -i %{buildroot}%{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon_tools.conf

install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{realname}-%{pg_maj_ver}

chmod 644 COPYRIGHT UPGRADING SAMPLE RELEASE

install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{realname}-%{pg_maj_ver}

install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{realname}-%{pg_maj_ver}.service

sed -i 's/{{PG_MAJOR_VERSION}}/%{pg_maj_ver}/g' %{buildroot}%{_unitdir}/%{realname}-%{pg_maj_ver}.service
sed -i 's/{{PG_MAJOR_VERSION}}/%{pg_maj_ver}/g' %{buildroot}%{_initddir}/%{realname}-%{pg_maj_ver}
sed -i 's/{{PG_HIGH_VERSION}}/%{pg_high_ver}/g' %{buildroot}%{_initddir}/%{realname}-%{pg_maj_ver}

pushd tools
  %{make_install}

  rm -f %{buildroot}%{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon_tools.conf-sample
  rm -f %{buildroot}%{_datadir}/pgsql/*.sql
  rm -f %{buildroot}%{_libdir}/%{realname}_funcs.so

  chrpath --delete %{buildroot}%{pg_dir}/bin/slonik
  chrpath --delete %{buildroot}%{pg_dir}/bin/slon
  chrpath --delete %{buildroot}%{pg_dir}/bin/slony_logshipper
  chrpath --delete %{buildroot}%{pg_dir}/lib/slony1_funcs.%{version}.so
popd

install -dm 755 %{buildroot}%{_logdir}/%{realname}-%{pg_maj_ver}

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  %{__sysctl} enable %{realname}-%{pg_maj_ver}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable %{realname}-%{pg_maj_ver}.service &>/dev/null || :
  %{__sysctl} stop %{realname}-%{pg_maj_ver}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT UPGRADING INSTALL SAMPLE RELEASE
%{pg_dir}/bin/slon*
%{pg_dir}/lib/slon*
%{pg_dir}/share/slon*
%dir %{_logdir}/%{realname}-%{pg_maj_ver}
%config(noreplace) %{_sysconfdir}/sysconfig/%{realname}-%{pg_maj_ver}
%config(noreplace) %{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon.conf
%config(noreplace) %{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/%{realname}-%{pg_maj_ver}
%attr(755,root,root) %{_unitdir}/%{realname}-%{pg_maj_ver}.service

################################################################################

%changelog
* Thu Feb 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.10-0
- Updated to the latest stable release

* Wed May 29 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.6-2
- Improved init script
- Improved systemd unit

* Sat Jan 27 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.6-1
- Improved spec

* Thu Oct 12 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.6-0
- Initial build
