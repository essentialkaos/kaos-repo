################################################################################

# rpmbuilder:gopack github.com/linkedin/Burrow
# rpmbuilder:tag v1.1.0

################################################################################

%define  debug_package %{nil}

################################################################################

Summary:         Kafka Consumer Lag Checking
Name:            Burrow
Version:         1.1.0
Release:         0%{?dist}
Group:           Applications/Databases
License:         ASL 2.0
URL:             https://github.com/linkedin/Burrow

Source0:         %{name}-%{version}.tar.bz2

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
mv .src src
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
* Mon Jul 23 2018 Andrey Kulikov <avk@brewkeeper.net> - 1.1.0-0
- Initial build
