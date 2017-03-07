###############################################################################

%define  debug_package %{nil}

###############################################################################

%global  cfssl_binaries cfssl mkbundle cfssljson cfssl-certinfo cfssl-newkey cfssl-scan

###############################################################################

Name:               cfssl
Summary:            CloudFlare PKI Toolkit
Version:            1.2.0
Release:            0%{?dist}
URL:                https://github.com/cloudflare/cfssl
Vendor:             CloudFlare
Group:              Applications/Internet
License:            MIT
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:            https://github.com/cloudflare/cfssl/archive/%{version}.tar.gz
BuildRequires:      golang >= 1.6
Provides:           %{name} = %{version}-%{release}

%description
CF-SSL is CloudFlare's SSL/TLS/X.509 swiss army knife. It is both a
command line tool and an HTTP API server for signing, verifying, and
bundling SSL/TLS X.509 certificates.

%prep
%setup -qn %{name}-%{version}
mkdir -p .src/github.com/cloudflare/cfssl
mv * .src/github.com/cloudflare/cfssl/
mv .src src

%build
export GOPATH=$(pwd)
export CGO_ENABLED=0
export GO15VENDOREXPERIMENT=1

cp -R src/github.com/cloudflare/cfssl/doc src/github.com/cloudflare/cfssl/LICENSE .

for _b in %{cfssl_binaries};
do
  go build -x -o ${_b} src/github.com/cloudflare/cfssl/cmd/${_b}/${_b}.go
done

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

rm -f cfssl_binaries.list

for _b in %{cfssl_binaries};
do
  install -spm 755 ${_b} %{buildroot}%{_bindir}
  echo "%{_bindir}/${_b}" >> cfssl_binaries.list
done

%files -f cfssl_binaries.list
%defattr(-,root,root,-)
%doc doc LICENSE

%clean
rm -rf %{buildroot}

%post

%preun

################################################################################
%changelog
* Tue Mar 06 2017 Andrey Kulikov <avk@brewkeeper.net> - 1.2.0-0
- Initial build
