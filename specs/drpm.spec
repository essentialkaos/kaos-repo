################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        A library for making, reading and applying deltarpm packages
Name:           drpm
Version:        0.4.1
Release:        0%{?dist}
License:        LGPLv2+ and BSD
Group:          Development/Tools
URL:            https://github.com/rpm-software-management/drpm

Source0:        https://github.com/rpm-software-management/%{name}/releases/download/%{version}/drpm-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc cmake >= 2.8.5
BuildRequires:  rpm-devel openssl-devel zlib-devel bzip2-devel xz-devel
BuildRequires:  pkgconfig doxygen libcmocka-devel >= 1.0 pkgconfig(libzstd)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
The drpm package provides a library for making, reading and applying deltarpms,
compatible with the original deltarpm packages.

################################################################################

%package devel
Summary:        C interface for the drpm library
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}

%description devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

################################################################################

%prep
%{crc_check}

%autosetup
mkdir build

%build
pushd build
  cmake .. -DWITH_ZSTD:BOOL=ON \
           -DHAVE_LZLIB_DEVEL:BOOL=OFF \
           -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
           -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}

  %{__make} %{?_smp_mflags}
  %{__make} doc
popd

%install
rm -rf %{buildroot}

pushd build
  %{make_install}
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING LICENSE.BSD
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc build/doc/html/
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.4.1-0
- Initial build
