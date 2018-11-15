################################################################################

%define  debug_package %{nil}

################################################################################

Summary:         Vendor Package Management for Golang
Name:            glide
Version:         0.13.2
Release:         0%{?dist}
Group:           Applications/Internet
License:         MIT
URL:             https://github.com/Masterminds/glide/

Source0:         https://github.com/Masterminds/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   golang >= 1.9

Requires:        golang

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Are you used to tools such as Cargo, npm, Composer, Nuget, Pip, Maven,
Bundler, or other modern package managers? If so, Glide is the comparable
Go tool.

Manage your vendor and vendored packages with ease. Glide is a tool for
managing the vendor directory within a Go package. This feature, first
introduced in Go 1.5, allows each package to have a vendor directory
containing dependent packages for the project. These vendor packages can
be installed by a tool (e.g. glide), similar to go get or they can be
vendored and distributed with the package.

################################################################################

%prep
%setup -qn %{name}-%{version}

mkdir -p .src
mv * .src/
mkdir -p src/github.com/Masterminds
mv .src src/github.com/Masterminds/%{name}

cp -r src/github.com/Masterminds/%{name}/CHANGELOG.md \
      src/github.com/Masterminds/%{name}/LICENSE \
      src/github.com/Masterminds/%{name}/README.md .

%build
export GOPATH=$(pwd)
export GO15VENDOREXPERIMENT=1

pushd src/github.com/Masterminds/%{name}
  go build -o %{name} -ldflags "-X main.version=%{version}" %{name}.go
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 src/github.com/Masterminds/%{name}/%{name} \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md CHANGELOG.md
%{_bindir}/%{name}

################################################################################

%changelog
* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 0.13.2-0
- Updated to the latest release

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.13.1-0
- Updated to the latest release

* Sat Nov 26 2016 Anton Novojilov <andy@essentialkaos.com> - 0.12.3-0
- Initial build for kaos repo
