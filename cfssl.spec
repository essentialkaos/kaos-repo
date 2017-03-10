###############################################################################

%define  debug_package %{nil}

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

go build -x -o cfssl src/github.com/cloudflare/cfssl/cmd/cfssl/cfssl.go
go build -x -o cfssljson src/github.com/cloudflare/cfssl/cmd/cfssljson/cfssljson.go
go build -x -o cfssl-certinfo src/github.com/cloudflare/cfssl/cmd/cfssl-certinfo/cfssl-certinfo.go
go build -x -o cfssl-mkbundle src/github.com/cloudflare/cfssl/cmd/mkbundle/mkbundle.go

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -spm 755 cfssl %{buildroot}%{_bindir}
install -spm 755 cfssljson %{buildroot}%{_bindir}
install -spm 755 cfssl-certinfo %{buildroot}%{_bindir}
install -spm 755 cfssl-mkbundle %{buildroot}%{_bindir}

%files
%defattr(-,root,root,-)
%{_bindir}/cfssl
%{_bindir}/cfssljson
%{_bindir}/cfssl-certinfo
%{_bindir}/cfssl-mkbundle
%doc doc LICENSE

%clean
rm -rf %{buildroot}

%post

%preun

################################################################################
%changelog
* Tue Mar 06 2017 Andrey Kulikov <avk@brewkeeper.net> - 1.2.0-0
- Initial build
