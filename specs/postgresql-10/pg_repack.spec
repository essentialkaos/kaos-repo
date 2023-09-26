################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define pg_ver      10
%define pg_fullver  %{pg_ver}.23
%define pg_dir      %{_prefix}/pgsql-%{pg_ver}
%define realname    pg_repack

################################################################################

Summary:         Reorganize tables in PostgreSQL %{pg_ver} databases without any locks
Name:            %{realname}%{pg_ver}
Version:         1.4.8
Release:         0%{?dist}
License:         BSD
Group:           Applications/Databases
URL:             https://pgxn.org/dist/pg_repack/

Source0:         https://api.pgxn.org/dist/%{realname}/%{version}/%{realname}-%{version}.zip

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc openssl-devel readline-devel zlib-devel
BuildRequires:   postgresql%{pg_ver}-devel = %{pg_fullver}
BuildRequires:   postgresql%{pg_ver}-libs = %{pg_fullver}

Requires:        postgresql%{pg_ver}

Requires(post):  %{_sbindir}/update-alternatives

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
pg_repack can re-organize tables on a postgres database without any locks so
that you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

################################################################################

%prep
%setup -qn %{realname}-%{version}

%build
%{__make} %{?_smp_mflags} PG_CONFIG=%{pg_dir}/bin/pg_config

%install
rm -rf %{buildroot}

%{make_install} PG_CONFIG=%{pg_dir}/bin/pg_config

%post
update-alternatives --install %{_bindir}/pg_repack pgrepack %{pg_dir}/bin/pg_repack %{pg_ver}0

%postun
if [[ $1 -eq 0 ]] ; then
  update-alternatives --remove pgrepack %{pg_dir}/bin/pg_repack
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT doc/pg_repack.rst
%attr(755,root,root) %{pg_dir}/bin/pg_repack
%attr(755,root,root) %{pg_dir}/lib/pg_repack.so
%{pg_dir}/share/extension/%{realname}--%{version}.sql
%{pg_dir}/share/extension/%{realname}.control

################################################################################

%changelog
* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-0
- Added support for PostgreSQL 15
- Fixed --parent-table on declarative partitioned tables
- Removed connection info from error log

* Thu Nov 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.7-0
- Added support for PostgreSQL 14

* Thu Feb 18 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.6-0
- Added support for PostgreSQL 13
- Dropped support for PostgreSQL before 9.4

* Tue Jan 21 2020 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- Added support for PostgreSQL 12
- Fixed parallel processing for indexes with operators from public schema

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- Added support for PostgreSQL 11
- Remove duplicate password prompt

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- Fixed possible CVE-2018-1058 attack paths
- Fixed "unexpected index definition" after CVE-2018-1058 changes in PostgreSQL
- Fixed build with recent Ubuntu packages

* Tue Nov 28 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Initial build for kaos repo
