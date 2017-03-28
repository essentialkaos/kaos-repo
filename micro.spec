###############################################################################

# rpmbuilder:gopack    github.com/zyedidia/micro
# rpmbuilder:tag       v1.1.4

###############################################################################

%define  debug_package %{nil}

###############################################################################

Summary:         A modern and intuitive terminal-based text editor
Name:            micro
Version:         1.1.4
Release:         0%{?dist}
Group:           Applications/Editors
License:         MIT
URL:             https://micro-editor.github.io

Source0:         %{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make golang >= 1.7

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Micro is a terminal-based text editor that aims to be easy to use and 
intuitive, while also taking advantage of the full capabilities of modern 
terminals. It comes as one single, batteries-included, static binary with no 
dependencies, and you can download and use it right now.

As the name indicates, micro aims to be somewhat of a successor to the nano 
editor by being easy to install and use in a pinch, but micro also aims to be 
enjoyable to use full time, whether you work in the terminal because you 
prefer it (like me), or because you need to (over ssh).

###############################################################################

%prep
%setup -q

mkdir bin
mkdir -p .src
mv * .src/
mv .src src

cp -r src/github.com/zyedidia/%{name}/LICENSE \
      src/github.com/zyedidia/%{name}/README.md .

build_date=`date +'%B %d, %Y'`

sed -e "s/0.0.0-unknown/%{version}/" \
    -e "s/CommitHash\ *= \"Unknown\"/CommitHash = \"00000000\"/" \
    -e "s/CompileDate\ *= \"Unknown\"/CompileDate = \"$build_date\"/" \
    -i src/github.com/zyedidia/%{name}/cmd/%{name}/%{name}.go

%build
export GOPATH=$(pwd)

pushd src/github.com/zyedidia/%{name}
  make runtime
  go build ./cmd/micro
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 src/github.com/zyedidia/%{name}/%{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}

###############################################################################

%changelog
* Sat Jan 28 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.3-0
- Initial build for kaos repository
