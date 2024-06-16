################################################################################

# rpmbuilder:gopack  github.com/benbjohnson/litestream
# rpmbuilder:tag     v0.3.13

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define  debug_package %{nil}

################################################################################

Summary:        Tool for real-time replication of SQLite databases
Name:           litestream
Version:        0.3.13
Release:        0%{?dist}
Group:          Development/Tools
License:        Apache-2.0
URL:            https://litestream.io

Source0:        %{name}-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRequires:  golang >= 1.21

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Litestream is a standalone disaster recovery tool for SQLite. It runs as a
background process and safely replicates changes incrementally to another file
or S3. Litestream only communicates with SQLite through the SQLite API so it
will not corrupt your database.

################################################################################

%prep
%{crc_check}

%setup -q

%build
pushd github.com/benbjohnson/%{name}/cmd/%{name}
  go build -ldflags="-X 'main.Version=%{version}'" -o ../../%{name}
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_unitdir}

install -pm 755 github.com/benbjohnson/%{name}/%{name} \
                %{buildroot}%{_bindir}/
# perfecto:ignore
install -pm 640 github.com/benbjohnson/%{name}/etc/%{name}.yml \
                %{buildroot}%{_sysconfdir}/
# perfecto:ignore
install -pm 644 github.com/benbjohnson/%{name}/etc/%{name}.service \
                %{buildroot}%{_unitdir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}.yml
%config(noreplace) %{_unitdir}/%{name}.service
%{_bindir}/%{name}

################################################################################

%changelog
* Mon May 27 2024 Anton Novojilov <andy@essentialkaos.com> - 0.3.13-0
- Initial build for kaos-repo
