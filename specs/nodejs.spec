################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot  /
%define _lib32      %{_posixroot}lib
%define _libdir32   %{_prefix}%{_lib32}

################################################################################

%define shortname  node

################################################################################

Summary:        Platform for server side programming on JavaScript
Name:           nodejs
Version:        20.14.0
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://nodejs.org

Source0:        https://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make python3 openssl-devel zlib-devel
BuildRequires:  gcc-c++ libstdc++-devel

Requires:       zlib

Provides:       %{name} = %{version}-%{release}
Provides:       %{shortname} = %{version}-%{release}
Provides:       %{name}(engine) = %{version}-%{release}
Provides:       npm = %{version}-%{release}

################################################################################

%description
Node.js is a platform built on Chromes JavaScript runtime for
easily building fast, scalable network applications. Node.js
uses an event-driven, non-blocking I/O model that makes it
lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

################################################################################

%package devel

Summary:    Header files for nodejs
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

BuildArch:  noarch

%description devel
This package provides the header files for nodejs.

################################################################################

%prep
%{crc_check}

%setup -qn %{shortname}-v%{version}

%build
%{_configure} --prefix=%{_prefix} \
              --shared-zlib \
              --shared-zlib-includes=%{_includedir}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot}%{_libdir32}/%{shortname}_modules -name "*.cmd" -type f -delete
find %{buildroot}%{_libdir32}/%{shortname}_modules -name "*.ps1" -type f -delete

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md GOVERNANCE.md README.md SECURITY.md
%{_bindir}/%{shortname}
%{_bindir}/npm
%{_bindir}/npx
%{_bindir}/corepack
%{_libdir32}/%{shortname}_modules
%{_docdir}/%{shortname}/gdbinit
%{_docdir}/%{shortname}/lldb*
%{_mandir}/man1/%{shortname}.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/*

################################################################################

%changelog
* Thu May 30 2024 Anton Novojilov <andy@essentialkaos.com> - 20.14.0-0
- https://nodejs.org/en/blog/release/v20.14.0

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 20.12.2-0
- https://nodejs.org/en/blog/release/v20.12.2

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 20.11.1-0
- https://nodejs.org/en/blog/release/v20.11.1

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 20.11.0-0
- https://nodejs.org/en/blog/release/v20.11.0

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 20.10.0-0
- https://nodejs.org/en/blog/release/v20.10.0

* Sat Oct 14 2023 Anton Novojilov <andy@essentialkaos.com> - 18.18.2-0
- https://nodejs.org/en/blog/release/v18.18.2

* Fri Oct 13 2023 Anton Novojilov <andy@essentialkaos.com> - 18.18.1-0
- https://nodejs.org/en/blog/release/v18.18.1

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 18.18.0-0
- https://nodejs.org/en/blog/release/v18.18.0

* Thu Dec 15 2022 Anton Novojilov <andy@essentialkaos.com> - 18.12.1-0
- https://nodejs.org/en/blog/release/v18.12.1
