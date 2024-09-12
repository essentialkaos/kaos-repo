################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?llvm:%global llvm 1}

################################################################################

%define pg_ver      %{?_pg}%{!?_pg:99}
%define pg_dir      %{_prefix}/pgsql-%{pg_ver}
%define realname    pg_repack

################################################################################

Summary:         Reorganize tables in PostgreSQL %{pg_ver} databases without any locks
Name:            %{realname}%{pg_ver}
Version:         1.5.0
Release:         0%{?dist}
License:         BSD
Group:           Applications/Databases
URL:             https://pgxn.org/dist/pg_repack/

Source0:         https://api.pgxn.org/dist/%{realname}/%{version}/%{realname}-%{version}.zip

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc openssl-devel readline-devel zlib-devel libzstd-devel
BuildRequires:   postgresql%{pg_ver}-devel postgresql%{pg_ver}-libs

%if %llvm
BuildRequires:   llvm-devel >= 13.0 clang-devel >= 13.0
%endif

Requires:        postgresql%{pg_ver}

Requires(post):  chkconfig

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
pg_repack can re-organize tables on a postgres database without any locks so
that you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

################################################################################

%prep
%crc_check
%autosetup -n %{realname}-%{version}

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

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT doc/pg_repack.rst
%attr(755,root,root) %{pg_dir}/bin/pg_repack
%attr(755,root,root) %{pg_dir}/lib/pg_repack.so
%{pg_dir}/share/extension/%{realname}--%{version}.sql
%{pg_dir}/share/extension/%{realname}.control
%if %llvm
%{pg_dir}/lib/bitcode/*
%endif

################################################################################

%changelog
* Tue Sep 10 2024 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- https://github.com/reorg/pg_repack/releases/tag/ver_1.5.0

* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-0
- Added support for PostgreSQL 15
- Fixed --parent-table on declarative partitioned tables
- Removed connection info from error log
