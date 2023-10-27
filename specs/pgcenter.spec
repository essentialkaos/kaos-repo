################################################################################

# rpmbuilder:gopack    github.com/lesovsky/pgcenter
# rpmbuilder:tag       v0.9.2

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Top-like PostgreSQL statistics viewer
Name:           pgcenter
Version:        0.9.2
Release:        0%{?dist}
License:        BSD 3-Clause
Group:          Development/Tools
URL:            https://github.com/lesovsky/pgcenter

Source0:        %{name}-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make golang >= 1.18

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
PostgreSQL provides various statistics which includes information about
tables, indexes, functions and other database objects and their usage.
Moreover, statistics has detailed information about connections, current
queries and database operations (INSERT/DELETE/UPDATE). But most of this
statistics are provided as permanently incremented counters. The pgcenter
provides convenient interface to this statistics and allow viewing statistics
changes in time interval, eg. per second. The pgcenter provides fast access
for database management task, such as editing configuration files, reloading
services, viewing log files and canceling or terminating database backends
(by pid or using state mask). However if need execute some specific
operations, pgcenter can start psql session for this purposes.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
export TOP_DIR=$(pwd)

pushd github.com/lesovsky/pgcenter
CGO_ENABLED=0 go build -o "%{name}" ./cmd
cp COPYRIGHT README.md $TOP_DIR/
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 github.com/lesovsky/pgcenter/%{name} \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md
%{_bindir}/%{name}

################################################################################

%changelog
* Thu Dec 15 2022 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.9.2

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.4-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.6.4

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.3-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.6.3

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.2-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.6.2

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.1-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.6.1

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 0.6.0-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.6.0

* Wed Oct 03 2018 Anton Novojilov <andy@essentialkaos.com> - 0.5.0-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.5.0

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.4.0

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.3.0

* Sat Dec 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.2.0-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.2.0

* Wed Oct 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- https://github.com/lesovsky/pgcenter/releases/tag/v0.1.3

* Wed Sep 09 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.2-0
- Initial build
