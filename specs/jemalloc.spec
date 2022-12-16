################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            General-purpose scalable concurrent malloc implementation
Name:               jemalloc
Version:            5.3.0
Release:            0%{?dist}
Group:              System Environment/Libraries
License:            BSD
URL:                https://jemalloc.net

Source0:            https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make libxslt

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of jemalloc.

################################################################################

%package devel

Summary:        Development files for jemalloc
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}

%description devel
The jemalloc-devel package contains libraries and header files for
developing applications that use jemalloc.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

%clean
rm -rf %{buildroot}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%doc COPYING README VERSION
%doc doc/jemalloc.html
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*
%{_bindir}/%{name}.sh
%{_bindir}/jeprof

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 5.3.0-0
- https://github.com/jemalloc/jemalloc/releases/tag/5.3.0

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 5.2.1-0
- https://github.com/jemalloc/jemalloc/releases/tag/5.2.1

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-0
- https://github.com/jemalloc/jemalloc/releases/tag/5.2.0

* Sat Mar 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.1.0-0
- Initial build for kaos repository
