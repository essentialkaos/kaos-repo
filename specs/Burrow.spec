################################################################################

%define  debug_package %{nil}

################################################################################

Summary:         Burrow - Kafka Consumer Lag Checking
Name:            Burrow
Version:         1.1.0
Release:         0%{?dist}
Group:           Applications/Databases
License:         ASL 2.0
URL:             https://github.com/linkedin/Burrow

Source0:         https://github.com/linkedin/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.9

Requires:        golang

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Burrow is a monitoring companion for Apache Kafka that provides consumer lag
checking as a service without the need for specifying thresholds. It monitors
committed offsets for all consumers and calculates the status of those consumers
on demand. An HTTP endpoint is provided to request status on demand, as well as
provide other Kafka cluster information. There are also configurable notifiers
that can send status out via email or HTTP calls to another service.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
export GOPATH=$(pwd)
go get -v github.com/linkedin/%{name}
pushd src/github.com/linkedin/%{name}
  go build
popd
cp -r src/github.com/linkedin/%{name}/CHANGELOG.md \
      src/github.com/linkedin/%{name}/LICENSE \
      src/github.com/linkedin/%{name}/NOTICE \
      src/github.com/linkedin/%{name}/README.md \
      src/github.com/linkedin/%{name}/config/burrow.toml \
      src/github.com/linkedin/%{name}/config/default-email.tmpl \
      src/github.com/linkedin/%{name}/config/default-http-delete.tmpl \
      src/github.com/linkedin/%{name}/config/default-http-post.tmpl \
      src/github.com/linkedin/%{name}/config/default-slack-delete.tmpl \
      src/github.com/linkedin/%{name}/config/default-slack-post.tmpl .

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 src/github.com/linkedin/%{name}/%{name} \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md CHANGELOG.md
%doc burrow.toml default-email.tmpl default-http-delete.tmpl
%doc default-http-post.tmpl default-slack-delete.tmpl default-slack-post.tmpl
%{_bindir}/%{name}

################################################################################

%changelog
* Mon Jul 23 2018 Andrey Kulikov <avk@brewkeeper.net> - 1.1.0-0
- Initial build
