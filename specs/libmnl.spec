################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Minimalistic Netlink communication library
Name:           libmnl
Version:        1.0.5
Release:        0%{?dist}
License:        LGPL-2.1+
Group:          System Environment/Libraries
URL:            https://netfilter.org

Source0:        https://www.netfilter.org/pub/%{name}/%{name}-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc libtool

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
libmnl is a minimalistic user-space library oriented to Netlink
developers. There are a lot of common tasks in parsing, validating,
constructing of both the Netlink header and TLVs that are repetitive
and easy to get wrong. This library aims to provide simple helpers
that allows you to re-use code and to avoid re-inventing the wheel.

################################################################################

%package devel
Requires:  %{name} = %{version}
Summary:   Header files and static libraries for libmnl package
Group:     Development/Libraries

%description devel
Header files and static libraries for libmnl package.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure
%{__make} %{?_smp_mflags} KERNELDIR="ignore"

%install
rm -rf %{buildroot}

%{make_install} KERNELDIR="ignore"
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sat Dec 17 2022 Anton Novojilov <andy@essentialkaos.com> - 1.0.5-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.4-0
- Updated to the latest stable release

* Fri Oct 10 2014 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Initial build
