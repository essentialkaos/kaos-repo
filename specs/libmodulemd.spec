################################################################################

%global _vpath_srcdir   .
%global _vpath_builddir %{_target_platform}

################################################################################

Summary:            C Library for manipulating module metadata files
Name:               libmodulemd
Version:            2.6.0
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://github.com/fedora-modularity/libmodulemd

Source0:            https://github.com/fedora-modularity/libmodulemd/releases/download/%{name}-%{version}/modulemd-%{version}.tar.xz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ meson
BuildRequires:      pkgconfig(gobject-2.0) pkgconfig(gobject-introspection-1.0)
BuildRequires:      pkgconfig(yaml-0.1) pkgconfig(gtk-doc)
BuildRequires:      valgrind clang

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
C Library for manipulating module metadata files.

################################################################################

%package devel

Summary:            Development files for libmodulemd
Group:              Development/Libraries

Requires:           pkgconfig >= 1:0.14
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for libmodulemd.

################################################################################

%prep
%setup -qn modulemd-%{version}

%build
%meson -Ddeveloper_build=false \
       -Dbuild_api_v1=false \
       -Dbuild_api_v2=true \
       -Dwith_py3_overrides=false

%meson_build

%install
rm -rf %{buildroot}

%meson_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING
%dir %{_libdir}/girepository-1.0
%{_bindir}/modulemd-validator
%{_libdir}/%{name}.so.*
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib

%files devel
%defattr(-,root,root,-)
%dir %{_datadir}/gir-1.0
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/modulemd-2.0.pc
%{_includedir}/modulemd-2.0/
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{_datadir}/gtk-doc/html/modulemd-2.0/

################################################################################

%changelog
* Sat Jul 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Initial build for kaos repository
