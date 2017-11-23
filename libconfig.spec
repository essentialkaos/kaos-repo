###############################################################################

Name:               libconfig
Summary:            C/C++ configuration file library
Version:            1.7
Release:            0%{?dist}
License:            LGPLv2+
Group:              Development/Libraries
URL:                https://hyperrealm.github.io/libconfig

Source0:            https://hyperrealm.github.io/%{name}/dist/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make texinfo-tex bison byacc flex gcc gcc-c++

###############################################################################

%description
Libconfig is a simple library for manipulating structured configuration 
files. This file format is more compact and more readable than XML. And 
unlike XML, it is type-aware, so it is not necessary to do string parsing 
in application code.

###############################################################################

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

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%postun -p /sbin/ldconfig

###############################################################################

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

###############################################################################

%changelog
* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7-0
- Updated to version 1.7

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- Updated to version 1.5

* Thu Apr 11 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.9-0
- Updated to version 1.4.8

* Thu Apr 12 2012 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-1
- Updated to version 1.4.8

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.2-1.1
- Rebuilt for RHEL 6

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.2-1
- update to 1.3.2