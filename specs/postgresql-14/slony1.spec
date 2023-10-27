################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global __perl_requires  %{SOURCE2}

%define maj_ver         2.2
%define pg_maj_ver      14
%define pg_high_ver     14
%define pg_low_fullver  14.6
%define pg_dir          %{_prefix}/pgsql-%{pg_high_ver}
%define realname        slony1
%define username        postgres
%define groupname       postgres

################################################################################

Summary:        A "master to multiple slaves" replication system with cascading and failover
Name:           %{realname}-%{pg_maj_ver}
Version:        2.2.11
Release:        0%{?dist}
License:        BSD
Group:          Applications/Databases
URL:            https://www.slony.info

Source0:        https://www.slony.info/downloads/%{maj_ver}/source/%{realname}-%{version}.tar.bz2
Source2:        filter-requires-perl-Pg.sh
Source3:        %{realname}.init
Source4:        %{realname}.sysconfig
Source5:        %{realname}.service

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc byacc flex chrpath
BuildRequires:  postgresql%{pg_maj_ver}-devel = %{pg_low_fullver}
BuildRequires:  postgresql%{pg_maj_ver}-server = %{pg_low_fullver}
BuildRequires:  postgresql%{pg_maj_ver}-libs = %{pg_low_fullver}

Requires:       postgresql%{pg_maj_ver}-server perl-DBD-Pg kaosv >= 2.16
Requires:       systemd

Provides:       %{name} = %{version}-%{release}

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

install -dm 755 %{buildroot}%{_localstatedir}/log/%{realname}-%{pg_maj_ver}

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  systemctl enable %{realname}-%{pg_maj_ver}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{realname}-%{pg_maj_ver}.service &>/dev/null || :
  systemctl stop %{realname}-%{pg_maj_ver}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  systemctl daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT UPGRADING INSTALL SAMPLE RELEASE
%{pg_dir}/bin/slon*
%{pg_dir}/lib/slon*
%{pg_dir}/share/slon*
%dir %{_localstatedir}/log/%{realname}-%{pg_maj_ver}
%config(noreplace) %{_sysconfdir}/sysconfig/%{realname}-%{pg_maj_ver}
%config(noreplace) %{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon.conf
%config(noreplace) %{_sysconfdir}/%{realname}-%{pg_maj_ver}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/%{realname}-%{pg_maj_ver}
%attr(755,root,root) %{_unitdir}/%{realname}-%{pg_maj_ver}.service

################################################################################

%changelog
* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 2.2.11-0
- Add support for PG 15
- Remove unused autoconf check
- Fix typo in admin guide

* Thu Feb 18 2021 Anton Novojilov <andy@essentialkaos.com> - 2.2.10-0
- Remove unsupported warning with PG13
