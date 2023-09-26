################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?llvm:%global llvm 1}

################################################################################

%define pg_ver      15
%define pg_fullver  %{pg_ver}.0
%define pg_dir      %{_prefix}/pgsql-%{pg_ver}
%define realname    pg_repack

################################################################################

Summary:        Reorganize tables in PostgreSQL %{pg_ver} databases without any locks
Name:           %{realname}%{pg_ver}
Version:        1.4.8
Release:        0%{?dist}
License:        BSD
Group:          Applications/Databases
URL:            https://pgxn.org/dist/pg_repack/

Source0:        https://api.pgxn.org/dist/%{realname}/%{version}/%{realname}-%{version}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc openssl-devel readline-devel zlib-devel libzstd-devel
BuildRequires:  postgresql%{pg_ver}-devel = %{pg_fullver}
BuildRequires:  postgresql%{pg_ver}-libs = %{pg_fullver}

%if %llvm
%if 0%{?rhel} >= 8
BuildRequires:  llvm-devel >= 6.0.0 clang-devel >= 6.0.0
%endif
%if 0%{?rhel} == 7
BuildRequires:  llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 4.0.1
%endif
%endif

Requires:       postgresql%{pg_ver}

Requires(post):  %{_sbindir}/update-alternatives

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
pg_repack can re-organize tables on a postgres database without any locks so
that you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

################################################################################

%prep
%setup -qn %{realname}-%{version}

%build
%if %llvm
%if 0%{?rhel} == 7
# perfecto:ignore
export CLANG=/opt/rh/llvm-toolset-7/root/usr/bin/clang
export LLVM_CONFIG=%{_libdir}/llvm5.0/bin/llvm-config
%endif
%endif

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
%if %llvm
%{pg_dir}/lib/bitcode/*
%endif

################################################################################

%changelog
* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-0
- Added support for PostgreSQL 15
- Fixed --parent-table on declarative partitioned tables
- Removed connection info from error log
