################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define debug_package  %{nil}

################################################################################

Summary:        A highly-available key value store for shared configuration
Name:           etcd
Version:        3.5.21
Release:        0%{?dist}
Group:          Applications/Internet
License:        APLv2
URL:            https://etcd.io

Source0:        https://github.com/etcd-io/etcd/archive/refs/tags/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  git golang >= 1.23

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
etcd is a distributed, consistent key-value store for shared configuration
and service discovery, with a focus on being:

- Simple: well-defined, user-facing API (gRPC)
- Secure: optional SSL client cert authentication
- Fast: benchmarked 1000s of writes/s per instance
- Reliable: properly distributed using Raft

etcd is written in Go and uses the Raft consensus algorithm to manage a
highly-available replicated log.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
pushd server
  go build -installsuffix cgo \
           -ldflags "-X version.GitSHA=0000000" \
           -o "../etcd_bin" .
popd

pushd etcdctl
  go build -installsuffix cgo \
           -ldflags "-X version.GitSHA=0000000" \
           -o "../etcdctl_bin" .
popd

pushd etcdutl
  go build -installsuffix cgo \
           -ldflags "-X version.GitSHA=0000000" \
           -o "../etcdutl_bin" .
popd


%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 etcd_bin %{buildroot}%{_bindir}/etcd
install -pm 755 etcdctl_bin %{buildroot}%{_bindir}/etcdctl
install -pm 755 etcdutl_bin %{buildroot}%{_bindir}/etcdutl

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md ROADMAP.md GOVERNANCE.md Documentation
%{_bindir}/etcd
%{_bindir}/etcdctl
%{_bindir}/etcdutl

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5.21-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.21

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5.17-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.17

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 3.5.15-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.15

* Wed May 29 2024 Anton Novojilov <andy@essentialkaos.com> - 3.5.14-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.14

* Thu Apr 18 2024 Anton Novojilov <andy@essentialkaos.com> - 3.5.13-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.13

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 3.5.11-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.11

* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 3.5.6-0
- https://github.com/etcd-io/etcd/releases/tag/v3.5.6

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 3.3.18-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.18

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 3.3.13-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.13

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.10-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.10

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.9-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.9

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.8-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.8

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.7-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.7

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.2-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.2

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 3.3.0-0
- https://github.com/etcd-io/etcd/releases/tag/v3.3.0

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.9-0
- https://github.com/etcd-io/etcd/releases/tag/v3.2.9

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.7-0
- https://github.com/etcd-io/etcd/releases/tag/v3.2.7

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- https://github.com/etcd-io/etcd/releases/tag/v3.2.2

* Mon May 15 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.7-0
- https://github.com/etcd-io/etcd/releases/tag/v3.1.7

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.3-0
- https://github.com/etcd-io/etcd/releases/tag/v3.1.3

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- https://github.com/etcd-io/etcd/releases/tag/v3.1.1

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.0-0
- https://github.com/etcd-io/etcd/releases/tag/v3.1.0

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.14-0
- https://github.com/etcd-io/etcd/releases/tag/v3.0.14

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.12-0
- https://github.com/etcd-io/etcd/releases/tag/v3.0.12

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.7-0
- https://github.com/etcd-io/etcd/releases/tag/v3.0.7

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.6-0
- https://github.com/etcd-io/etcd/releases/tag/v2.3.6

* Thu May 26 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.5-0
- https://github.com/etcd-io/etcd/releases/tag/v2.3.5

* Tue Mar 22 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- https://github.com/etcd-io/etcd/releases/tag/v2.3.3
