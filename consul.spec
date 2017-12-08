###############################################################################

%define  debug_package %{nil}

###############################################################################

Summary:         Tool for service discovery, monitoring and configuration
Name:            consul
Version:         1.0.0
Release:         0%{?dist}
Group:           Applications/Internet
License:         MPLv2
URL:             http://www.consul.io

Source0:         https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.9

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Consul is a tool for service discovery and configuration. Consul is 
distributed, highly available, and extremely scalable.

###############################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src/github.com/hashicorp/%{name}
mv * .src/github.com/hashicorp/%{name}/
mv .src src

%build
export GOPATH=$(pwd)
export XC_OS=$(go env GOOS)
export XC_ARCH=$(go env GOARCH)
export GO15VENDOREXPERIMENT=1
export CGO_ENABLED=0
export GIT_IMPORT="github.com/hashicorp/consul/version"
export GOLDFLAGS="-X $GIT_IMPORT.GitDescribe=%{version}"

pushd src/github.com/hashicorp/%{name}
  %{__make} tools || :
  $GOPATH/bin/gox -osarch="${XC_OS}/${XC_ARCH}" \
                  -ldflags "${GOLDFLAGS}" \
                  -tags="consul" \
                  -output "$GOPATH/%{name}" .
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 %{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

###############################################################################

%changelog
* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Updated to latest stable release

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 0.8.5-0
- Updated to latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.5-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.2-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.0-0
- Updated to latest stable release

* Tue Mar 22 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.4-0
- Updated to latest stable release

* Thu Mar 10 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.3-0
- Initial build
