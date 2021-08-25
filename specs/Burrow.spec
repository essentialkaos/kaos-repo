################################################################################

# rpmbuilder:gopack github.com/linkedin/Burrow
# rpmbuilder:tag    v1.3.6

################################################################################

%define  debug_package %{nil}

################################################################################

Summary:         Kafka Consumer Lag Checking
Name:            Burrow
Version:         1.3.6
Release:         0%{?dist}
Group:           Applications/Databases
License:         ASL 2.0
URL:             https://github.com/linkedin/Burrow

Source0:         https://github.com/linkedin/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.9

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
mkdir -p .src
mv * .src/
mkdir -p src/github.com/linkedin
mv .src src/github.com/linkedin/%{name}
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

%build
export GOPATH=$(pwd)
pushd src/github.com/linkedin/%{name}
  go build
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -Dpm 755 src/github.com/linkedin/%{name}/%{name} \
                %{buildroot}%{_bindir}/burrow

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md CHANGELOG.md
%doc burrow.toml default-email.tmpl default-http-delete.tmpl
%doc default-http-post.tmpl default-slack-delete.tmpl default-slack-post.tmpl
%{_bindir}/burrow

################################################################################

%changelog
* Wed Aug 25 2021 Ivan Burashev <vanche93@yandex.ru> - 1.3.6-0
- Fix goreleaser github action
- Update base alpine image from 3.12 to 3.13

* Tue May 21 2019 Andrey Kulikov <avk@brewkeeper.net> - 1.2.2-0
- More fixes to binary release process

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Add support for Kafka up to version 2.1.0
- Update sarama to version 1.20.1 with support for zstd compression
- Support linux/arm64
- Add blacklist for memory store

* Mon Jul 23 2018 Andrey Kulikov <avk@brewkeeper.net> - 1.1.0-0
- Initial build for EK repository
