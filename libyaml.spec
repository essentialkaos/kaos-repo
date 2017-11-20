################################################################################

Summary:         A C library for parsing and emitting YAML
Name:            libyaml
Version:         0.1.7
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             http://pyyaml.org/wiki/LibYAML

Source0:         http://pyyaml.org/download/%{name}/yaml-%{version}.tar.gz

Patch0:          https://github.com/yaml/libyaml/commit/abaf719330e742d80c7295c6943fe14c31ec83bd.diff

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
%setup -qn yaml-%{version}

%patch0 -p1

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/*.{la,a}

%check
%{__make} check

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/yaml-0.1.pc
%{_includedir}/yaml.h

################################################################################

%changelog
* Tue Nov 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.1.7-0
- Initial build for kaos repo
