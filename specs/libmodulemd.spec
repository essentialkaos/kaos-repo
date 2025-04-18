################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%if 0%{?rhel} >= 8
%global python_base  python3
%global __python3    %{_bindir}/python3
%endif

################################################################################

%global _vpath_srcdir    .
%global _vpath_builddir  %{_target_platform}

################################################################################

Summary:        C Library for manipulating module metadata files
Name:           libmodulemd
Version:        2.15.0
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://github.com/fedora-modularity/libmodulemd

Source0:        https://github.com/fedora-modularity/libmodulemd/releases/download/%{version}/modulemd-%{version}.tar.xz
Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc gcc-c++ meson glib2-doc rpm-devel rpm-libs libzstd-devel
BuildRequires:  pkgconfig(gobject-2.0) pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  %{python_base}-devel %{python_base}-gobject-base epel-rpm-macros

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
C Library for manipulating module metadata files.

################################################################################

%package devel

Summary:   Development files for libmodulemd
Group:     Development/Libraries

Requires:  pkgconfig >= 1:0.14
Requires:  pkgconfig(glib-2.0) pkgconfig(rpm) pkgconfig(yaml-0.1)

Requires:  %{name} = %{version}-%{release}

%description devel
Development files for libmodulemd.

################################################################################

%prep
%{crc_check}

%setup -qn modulemd-%{version}

%build
gob_overrides_dir=$(%{__python3} -c 'import gi; print(gi._overridesdir)')

%{meson} -Dwith_docs=false \
         -Dwith_py2=false \
         -Dwith_py3=true \
         -Daccept_overflowed_buildorder=true \
         -Dgobject_overrides_dir_py3=$gob_overrides_dir

%{meson_build}

%install
rm -rf %{buildroot}

%{meson_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING
%dir %{_libdir}/girepository-1.0
%{_bindir}/modulemd-validator
%{_libdir}/%{name}.so.*
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{python3_sitearch}/gi/overrides/Modulemd.*
%{_mandir}/man1/*
%exclude %{python3_sitearch}/gi/overrides/__pycache__

%files devel
%defattr(-,root,root,-)
%dir %{_datadir}/gir-1.0
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/modulemd-2.0.pc
%{_includedir}/modulemd-2.0/
%{_datadir}/gir-1.0/Modulemd-2.0.gir

################################################################################

%changelog
* Thu Sep 07 2023 Anton Novojilov <andy@essentialkaos.com> - 2.15.0-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.15.0

* Thu Sep 22 2022 Anton Novojilov <andy@essentialkaos.com> - 2.14.0-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.14.0

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.8.2

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.8.1

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.8.0

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.7.0-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.7.0

* Sat Jul 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.6.0

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Initial build for kaos repository
