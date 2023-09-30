################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define pg_ver      10
%define pg_fullver  %{pg_ver}.23
%define pg_dir      %{_prefix}/pgsql-%{pg_ver}
%define realname    pg_comparator

################################################################################

Summary:         Efficient table content comparison and synchronization for PostgreSQL %{pg_ver}
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
%setup -qn %{realname}-%{version}

%patch0 -p1

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

################################################################################

%changelog
* Thu Sep 21 2023 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- Updated to the latest stable release

* Thu Oct 12 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Initial build
