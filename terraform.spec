###############################################################################

%define  debug_package %{nil}

###############################################################################

Summary:         Tool for building, changing, and combining infrastructure 
Name:            terraform
Version:         0.6.15
Release:         0%{?dist}
Group:           Applications/Internet
License:         MPLv2
URL:             http://www.terraform.io

Source0:         https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   zip golang >= 1.6

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Terraform is a tool for building, changing, and combining infrastructure 
safely and efficiently.

###############################################################################

%package all

Summary:         Meta-package with all Terraform tools

Requires:        %{name}-provider-atlas
Requires:        %{name}-provider-aws
Requires:        %{name}-provider-azure
Requires:        %{name}-provider-azurerm
Requires:        %{name}-provider-chef
Requires:        %{name}-provider-clc
Requires:        %{name}-provider-cloudflare
Requires:        %{name}-provider-cloudstack
Requires:        %{name}-provider-cobbler
Requires:        %{name}-provider-consul
Requires:        %{name}-provider-datadog
Requires:        %{name}-provider-digitalocean
Requires:        %{name}-provider-dme
Requires:        %{name}-provider-dnsimple
Requires:        %{name}-provider-docker
Requires:        %{name}-provider-dyn
Requires:        %{name}-provider-fastly
Requires:        %{name}-provider-github
Requires:        %{name}-provider-google
Requires:        %{name}-provider-heroku
Requires:        %{name}-provider-influxdb
Requires:        %{name}-provider-mailgun
Requires:        %{name}-provider-mysql
Requires:        %{name}-provider-null
Requires:        %{name}-provider-openstack
Requires:        %{name}-provider-packet
Requires:        %{name}-provider-postgresql
Requires:        %{name}-provider-powerdns
Requires:        %{name}-provider-rundeck
Requires:        %{name}-provider-statuscake
Requires:        %{name}-provider-template
Requires:        %{name}-provider-terraform
Requires:        %{name}-provider-tls
Requires:        %{name}-provider-triton
Requires:        %{name}-provider-ultradns
Requires:        %{name}-provider-vcd
Requires:        %{name}-provider-vsphere
Requires:        %{name}-provisioner-chef
Requires:        %{name}-provisioner-file
Requires:        %{name}-provisioner-local-exec
Requires:        %{name}-provisioner-remote-exec

%description all
Meta-package with all Terraform tools.

###############################################################################

%package provider-atlas

Summary:         Atlas provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-atlas
Atlas provider for Terraform.

###############################################################################

%package provider-aws

Summary:         AWS provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-aws
AWS provider for Terraform.

###############################################################################

%package provider-azure

Summary:         Azure provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-azure
Azure provider for Terraform.

###############################################################################

%package provider-azurerm

Summary:         Azurerm provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-azurerm
Azurerm provider for Terraform.

###############################################################################

%package provider-chef

Summary:         Chef provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-chef
Chef provider for Terraform.

###############################################################################

%package provider-clc

Summary:         CLC provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-clc
CLC provider for Terraform.

###############################################################################

%package provider-cloudflare

Summary:         CloudFlare provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-cloudflare
CloudFlare provider for Terraform.

###############################################################################

%package provider-cloudstack

Summary:         CloudStack provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-cloudstack
CloudStack provider for Terraform.

###############################################################################

%package provider-cobbler

Summary:         Cobbler provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-cobbler
Cobbler provider for Terraform.

###############################################################################

%package provider-consul

Summary:         Consul provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-consul
Consul provider for Terraform.

###############################################################################

%package provider-datadog

Summary:         Datadog provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-datadog
Datadog provider for Terraform.

###############################################################################

%package provider-digitalocean

Summary:         DigitalOcean provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-digitalocean
DigitalOcean provider for Terraform.

###############################################################################

%package provider-dme

Summary:         DME provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-dme
DME provider for Terraform.

###############################################################################

%package provider-dnsimple

Summary:         DNSimple provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-dnsimple
DNSimple provider for Terraform.

###############################################################################

%package provider-docker

Summary:         Docker provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-docker
Docker provider for Terraform.

###############################################################################

%package provider-dyn

Summary:         Dyn provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-dyn
Dyn provider for Terraform.

###############################################################################

%package provider-fastly

Summary:         Fastly provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-fastly
Fastly provider for Terraform.

###############################################################################

%package provider-github

Summary:         GitHub provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-github
GitHub provider for Terraform.

###############################################################################

%package provider-google

Summary:         Google provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-google
Google provider for Terraform.

###############################################################################

%package provider-heroku

Summary:         Heroku provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-heroku
Heroku provider for Terraform.

###############################################################################

%package provider-influxdb

Summary:         InfluxDB provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-influxdb
InfluxDB provider for Terraform.

###############################################################################

%package provider-mailgun

Summary:         Mailgun provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-mailgun
Mailgun provider for Terraform.

###############################################################################

%package provider-mysql

Summary:         MySQL provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-mysql
MySQL provider for Terraform.

###############################################################################

%package provider-null

Summary:         Null provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-null
Null provider for Terraform.

###############################################################################

%package provider-openstack

Summary:         OpenStack provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-openstack
OpenStack provider for Terraform.

###############################################################################

%package provider-packet

Summary:         Packet provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-packet
Packet provider for Terraform.

###############################################################################

%package provider-postgresql

Summary:         PostgreSQL provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-postgresql
PostgreSQL provider for Terraform.

###############################################################################

%package provider-powerdns

Summary:         PowerDNS provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-powerdns
PowerDNS provider for Terraform.

###############################################################################

%package provider-rundeck

Summary:         Rundeck provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-rundeck
Rundeck provider for Terraform.

###############################################################################

%package provider-statuscake

Summary:         StatusCake provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-statuscake
StatusCake provider for Terraform.

###############################################################################

%package provider-template

Summary:         Template provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-template
Template provider for Terraform.

###############################################################################

%package provider-terraform

Summary:         Terraform provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-terraform
Terraform provider for Terraform.

###############################################################################

%package provider-tls

Summary:         TLS provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-tls
TLS provider for Terraform.

###############################################################################

%package provider-triton

Summary:         Triton provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-triton
Triton provider for Terraform.

###############################################################################

%package provider-ultradns

Summary:         UltraDNS provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-ultradns
UltraDNS provider for Terraform.

###############################################################################

%package provider-vcd

Summary:         VCD provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-vcd
VCD provider for Terraform.

###############################################################################

%package provider-vsphere

Summary:         VSphere provider for Terraform

Requires:        %{name} = %{version}-%{release}

%description provider-vsphere
VSphere provider for Terraform.

###############################################################################

%package provisioner-chef

Summary:         Chef provisioner for Terraform

Requires:        %{name} = %{version}-%{release}

%description provisioner-chef
Chef provisioner for Terraform.

###############################################################################

%package provisioner-file

Summary:         File provisioner for Terraform

Requires:        %{name} = %{version}-%{release}

%description provisioner-file
File provisioner for Terraform.

###############################################################################

%package provisioner-local-exec

Summary:         local-exec provisioner for Terraform

Requires:        %{name} = %{version}-%{release}

%description provisioner-local-exec
local-exec provisioner for Terraform.

###############################################################################

%package provisioner-remote-exec

Summary:         remote-exec provisioner for Terraform

Requires:        %{name} = %{version}-%{release}

%description provisioner-remote-exec
remote-exec provisioner for Terraform.

###############################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src/github.com/hashicorp/%{name}
mv * .src/github.com/hashicorp/%{name}/
mv .src src

%build
export GOPATH=$(pwd)
export PATH="$GOPATH/bin:$PATH"
export XC_OS=$(go env GOOS)
export XC_ARCH=$(go env GOARCH)

# Download and install stringer
go get -v golang.org/x/tools/cmd/stringer

pushd src/github.com/hashicorp/%{name}
  %{__make} %{?_smp_mflags} bin
popd

cp src/github.com/hashicorp/%{name}/README.md .
cp src/github.com/hashicorp/%{name}/LICENSE .
cp src/github.com/hashicorp/%{name}/CHANGELOG.md .

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

cp src/github.com/hashicorp/%{name}/pkg/*/%{name}* %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc README.md CHANGELOG.md LICENSE
%{_bindir}/%{name}

%files all
# No files for you

%files provider-atlas
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-atlas

%files provider-aws
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-aws

%files provider-azure
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-azure

%files provider-azurerm
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-azurerm

%files provider-chef
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-chef

%files provider-clc
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-clc

%files provider-cloudflare
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-cloudflare

%files provider-cloudstack
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-cloudstack

%files provider-cobbler
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-cobbler

%files provider-consul
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-consul

%files provider-datadog
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-datadog

%files provider-digitalocean
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-digitalocean

%files provider-dme
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-dme

%files provider-dnsimple
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-dnsimple

%files provider-docker
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-docker

%files provider-dyn
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-dyn

%files provider-fastly
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-fastly

%files provider-github
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-github

%files provider-google
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-google

%files provider-heroku
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-heroku

%files provider-influxdb
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-influxdb

%files provider-mailgun
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-mailgun

%files provider-mysql
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-mysql

%files provider-null
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-null

%files provider-openstack
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-openstack

%files provider-packet
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-packet

%files provider-postgresql
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-postgresql

%files provider-powerdns
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-powerdns

%files provider-rundeck
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-rundeck

%files provider-statuscake
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-statuscake

%files provider-template
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-template

%files provider-terraform
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-terraform

%files provider-tls
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-tls

%files provider-triton
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-triton

%files provider-ultradns
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-ultradns

%files provider-vcd
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-vcd

%files provider-vsphere
%defattr(-,root,root,-)
%{_bindir}/%{name}-provider-vsphere

%files provisioner-chef
%defattr(-,root,root,-)
%{_bindir}/%{name}-provisioner-chef

%files provisioner-file
%defattr(-,root,root,-)
%{_bindir}/%{name}-provisioner-file

%files provisioner-local-exec
%defattr(-,root,root,-)
%{_bindir}/%{name}-provisioner-local-exec

%files provisioner-remote-exec
%defattr(-,root,root,-)
%{_bindir}/%{name}-provisioner-remote-exec

###############################################################################

%changelog
* Thu May 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.15-0
- Updated to latest stable release

* Thu Mar 10 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.14-0
- Initial build
