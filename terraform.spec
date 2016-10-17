###############################################################################

%define  debug_package %{nil}

###############################################################################

Summary:         Tool for building, changing, and combining infrastructure 
Name:            terraform
Version:         0.7.6
Release:         0%{?dist}
Group:           Applications/Internet
License:         MPLv2
URL:             http://www.terraform.io

Source0:         https://github.com/hashicorp/%{name}/archive/v%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   zip golang >= 1.7

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Terraform is a tool for building, changing, and combining infrastructure 
safely and efficiently.

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
  %{__make} bin
popd

cp src/github.com/hashicorp/%{name}/README.md .
cp src/github.com/hashicorp/%{name}/LICENSE .
cp src/github.com/hashicorp/%{name}/CHANGELOG.md .

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

cp src/github.com/hashicorp/%{name}/pkg/*/%{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc README.md CHANGELOG.md LICENSE
%{_bindir}/%{name}

###############################################################################

%changelog
* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.6-0
- Updated to latest stable release

* Fri Sep 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.3-0
- Updated to latest stable release

* Fri Sep 02 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.2-0
- Updated to latest stable release

* Fri Sep 02 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.1-0
- Updated to latest stable release

* Fri Aug 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.7.0-0
- Updated to latest stable release

* Tue Jun 07 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.16-0
- Updated to latest stable release

* Thu May 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.15-0
- Updated to latest stable release

* Thu Mar 10 2016 Anton Novojilov <andy@essentialkaos.com> - 0.6.14-0
- Initial build
