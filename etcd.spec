###############################################################################

# rpmbuilder:gopack    github.com/coreos/etcd
# rpmbuilder:tag       v3.1.7

###############################################################################

%define  debug_package %{nil}

###############################################################################

Summary:         Distributed reliable key-value store for the most critical data of a distributed system
Name:            etcd
Version:         3.1.7
Release:         0%{?dist}
Group:           Applications/Internet
License:         APLv2
URL:             https://coreos.com/etcd

Source0:         %{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.8

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
etcd is a distributed, consistent key-value store for shared configuration 
and service discovery, with a focus on being:

- Simple: well-defined, user-facing API (gRPC)
- Secure: optional SSL client cert authentication
- Fast: benchmarked 1000s of writes/s per instance
- Reliable: properly distributed using Raft

etcd is written in Go and uses the Raft consensus algorithm to manage a 
highly-available replicated log.

###############################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src
mv * .src/
mv .src src

cp -r src/github.com/coreos/%{name}/LICENSE \
      src/github.com/coreos/%{name}/README.md \
      src/github.com/coreos/%{name}/NOTICE \
      src/github.com/coreos/%{name}/MAINTAINERS \
      src/github.com/coreos/%{name}/Documentation .

%build
export GOPATH=$(pwd)
export GO15VENDOREXPERIMENT=1
export CGO_ENABLED=0

pushd src/github.com/coreos/%{name}
  ./build
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 src/github.com/coreos/%{name}/bin/%{name} \
                %{buildroot}%{_bindir}/
install -pm 755 src/github.com/coreos/%{name}/bin/%{name}ctl \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md NOTICE MAINTAINERS Documentation
%{_bindir}/%{name}
%{_bindir}/%{name}ctl

###############################################################################

%changelog
* Mon May 15 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.7-0
- Updated to latest stable release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.3-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.0-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.14-0
- Updated to latest stable release

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.12-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0.7-0
- Updated to latest stable release

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.6-0
- Updated to latest stable release

* Thu May 26 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.5-0
- Updated to latest stable release

* Tue Mar 22 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- Updated to latest stable release
