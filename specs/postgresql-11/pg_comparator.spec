################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?llvm:%global llvm 1}

################################################################################

%define pg_ver      11
%define pg_fullver  %{pg_ver}.18
%define pg_dir      %{_prefix}/pgsql-%{pg_ver}
%define realname    pg_comparator

################################################################################

Summary:         A tool to compare and sync tables in different locations
Name:            %{realname}%{pg_ver}
Version:         2.3.2
Release:         0%{?dist}
License:         BSD
Group:           Development/Tools
URL:             https://www.cri.ensmp.fr/people/coelho/pg_comparator

Source:          https://www.cri.ensmp.fr/people/coelho/pg_comparator/%{realname}-%{version}.tgz

Patch0:          %{realname}-Makefile.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc
BuildRequires:   postgresql%{pg_ver}-devel = %{pg_fullver}
BuildRequires:   postgresql%{pg_ver}-libs = %{pg_fullver}

%if %llvm
BuildRequires:   llvm-devel >= 6.0.0 clang-devel >= 6.0.0
%endif

Requires:        perl(Getopt::Long), perl(Time::HiRes)
Requires:        postgresql%{pg_ver}

Requires(post):  chkconfig

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

################################################################################

%prep
%crc_check
%autosetup -p1 -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags} PG_CONFIG=%{pg_dir}/bin/pg_config

%install
rm -rf %{buildroot}

%{make_install} PG_CONFIG=%{pg_dir}/bin/pg_config

%post
update-alternatives --install %{_bindir}/pg_comparator pgcomparator %{pg_dir}/bin/pg_comparator %{pg_ver}0

%postun
if [[ $1 -eq 0 ]] ; then
  update-alternatives --remove pgcomparator %{pg_dir}/bin/pg_comparator
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc %{pg_dir}/doc/extension/README.pg_comparator
%{pg_dir}/bin/pg_comparator
%{pg_dir}/lib/pgcmp.so
%{pg_dir}/share/extension/*.sql
%{pg_dir}/share/extension/pgcmp.control
%if %llvm
%{pg_dir}/lib/bitcode/*
%endif

################################################################################

%changelog
* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- Updated to the latest stable release

* Thu Oct 12 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Initial build
