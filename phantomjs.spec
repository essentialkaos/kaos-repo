########################################################################################

# rpmbuilder:github ariya/phantomjs
# rpmbuilder:tag    2.1.1

########################################################################################

Summary:            A headless WebKit with JavaScript API
Name:               phantomjs
Version:            2.1.1
Release:            0%{?dist}
License:            BSD
Group:              Development/Tools
URL:                http://phantomjs.org

Source0:            %{name}-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      bison flex fontconfig-devel freetype-devel gcc gcc-c++ gperf
BuildRequires:      libicu-devel libjpeg-devel libpng-devel make openssl-devel
BuildRequires:      perl(Getopt::Long) python ruby sqlite-devel urw-fonts

Provides:           %{name} = %{version}-%{release}

########################################################################################

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG. PhantomJS is created by Ariya Hidayat.

########################################################################################

%prep
%setup -q

%build
./build.py --confirm --release

%install
rm -rf %{buildroot}

install -Dm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-, root, root, -)
%doc LICENSE.BSD ChangeLog README.md
%{_bindir}/%{name}

########################################################################################

%changelog
* Wed Dec 21 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Initial build for kaos-repo
