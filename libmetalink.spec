###############################################################################

Summary:         Metalink library written in C
Name:            libmetalink
Version:         0.1.3
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         MIT
URL:             https://launchpad.net/libmetalink

Source0:         https://launchpad.net/libmetalink/trunk/%{name}-%{version}/+download/%{name}-%{version}.tar.bz2

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc expat-devel

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
libmetalink is a Metalink C library. It adds Metalink functionality such as
parsing Metalink XML files to programs written in C.

###############################################################################

%package  devel

Summary:         Files needed for developing with %{name}
Group:           Development/Libraries
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description  devel
Files needed for building applications with libmetalink.

###############################################################################

%prep
%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

find %{buildroot} -name *.la -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, -)
%doc COPYING README 
%{_libdir}/libmetalink.so.*

%files devel
%defattr(-, root, root, -)
%dir %{_includedir}/metalink/
%{_includedir}/metalink/metalink_error.h
%{_includedir}/metalink/metalink.h
%{_includedir}/metalink/metalink_parser.h
%{_includedir}/metalink/metalink_types.h
%{_includedir}/metalink/metalinkver.h
%{_libdir}/libmetalink.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*

###############################################################################

%changelog
* Tue Nov 01 2016 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- Initial build for kaos repository
