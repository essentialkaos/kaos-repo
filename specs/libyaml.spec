################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         A C library for parsing and emitting YAML
Name:            libyaml
Version:         0.2.5
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             https://pyyaml.org/wiki/LibYAML

Source0:         https://pyyaml.org/download/%{name}/yaml-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.

################################################################################

%package devel
Summary:         Development files for LibYAML applications
Group:           Development/Libraries

Requires:        libyaml = %{version}-%{release} pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use LibYAML.

################################################################################

%prep
%{crc_check}

%setup -qn yaml-%{version}

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

rm -f %{buildroot}%{_libdir}/*.{la,a}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc License ReadMe.md
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/yaml.h

################################################################################

%changelog
* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 0.2.5-0
- https://github.com/yaml/libyaml/releases/tag/0.2.5

* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.2.2-0
- Updated to the latest release

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 0.2.1-0
- Updated to the latest release

* Tue Nov 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.1.7-0
- Initial build for kaos repo
