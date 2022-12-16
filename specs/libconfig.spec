################################################################################

Name:               libconfig
Summary:            C/C++ configuration file library
Version:            1.7.3
Release:            0%{?dist}
License:            LGPLv2+
Group:              Development/Libraries
URL:                https://hyperrealm.github.io/libconfig

Source0:            https://hyperrealm.github.io/%{name}/dist/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make texinfo-tex bison byacc flex gcc gcc-c++

################################################################################

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.

################################################################################

%package devel
Summary:             Development files for libconfig
Group:               Development/Libraries

Requires:            %{name} = %{version}-%{release}
Requires:            pkgconfig

Requires(post):      /sbin/install-info
Requires(preun):     /sbin/install-info

%description devel
Development libraries and headers for developing software against
libconfig.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%{_infodir}/libconfig.info*
%{_libdir}/cmake/%{name}++/*.cmake
%{_libdir}/cmake/%{name}/*.cmake

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- https://github.com/hyperrealm/libconfig/releases/tag/v1.7.3

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- https://github.com/hyperrealm/libconfig/releases/tag/v1.7.2

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- https://github.com/hyperrealm/libconfig/releases/tag/v1.7.1

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7-0
- https://github.com/hyperrealm/libconfig/releases/tag/v1.7

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6-0
- https://github.com/hyperrealm/libconfig/releases/tag/v1.6

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- Updated to version 1.5
