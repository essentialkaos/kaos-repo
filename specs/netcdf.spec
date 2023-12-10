################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

%global hdf5_ver  %(rpm -q --quiet hdf5-devel && rpm -q --qf '%%{version}' hdf5-devel || echo "1.14")

################################################################################

Summary:        Libraries for the Unidata network Common Data Form
Name:           netcdf
Version:        4.9.2
Release:        1%{?dist}
License:        NetCDF
Group:          Applications/Engineering
URL:            https://www.unidata.ucar.edu/software/netcdf/

Source0:        https://downloads.unidata.ucar.edu/%{name}-c/%{version}/%{name}-c-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc chrpath doxygen gawk libxml2-devel
BuildRequires:  libcurl-devel m4 zlib-devel openssh-clients libtirpc-devel
BuildRequires:  hdf-static hdf5-devel

Requires:       hdf5 = %{hdf5_ver}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a freely-distributed collection of software libraries
for C, Fortran, C++, and perl that provides an implementation of the
interface.  The NetCDF library also defines a machine-independent
format for representing scientific data.  Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The NetCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

################################################################################

%package devel
Summary:  Development files for netcdf
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}
Requires:  hdf5-devel = %{hdf5_ver}
Requires:  pkgconfig libcurl-devel

%description devel
This package contains the netCDF C header files, shared devel libs, and
man pages.

################################################################################

%package static
Summary:  Static libs for netcdf
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description static
This package contains the netCDF C static libs.

################################################################################

%prep
%setup -qn %{name}-c-%{version}

%build
export LDFLAGS="%{__global_ldflags} -L%{_libdir}/hdf"
export CFLAGS="%{optflags} -fno-strict-aliasing"

mkdir build
pushd build
  ln -s ../configure .

  %configure --enable-shared \
             --enable-dap \
             --enable-netcdf-4 \
             --enable-hdf4 \
             --disable-dap-remote-tests \
             --enable-extra-example-tests \
             CPPFLAGS="-I%{_includedir}/hdf -DH5_USE_110_API" \
             LIBS="-ltirpc"

  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install} -C build

chrpath --delete --keepgoing %{buildroot}%{_bindir}/* || :

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} -C build check
%endif

%clean
rm -rf %{buildroot}

%post
%{_sbindir}/ldconfig

%postun
%{_sbindir}/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%{_bindir}/nc4print
%{_bindir}/nccopy
%{_bindir}/ncdump
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_bindir}/ocprint
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc examples
%{_bindir}/nc-config
%{_includedir}/*.h
%{_libdir}/libnetcdf.settings
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcdf.pc
%{_mandir}/man3/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

################################################################################

%changelog
* Sat Dec 09 2023 Anton Novojilov <andy@essentialkaos.com> - 4.9.2-1
- Rebuilt with the latest version of HDF5

* Wed Sep 27 2023 Anton Novojilov <andy@essentialkaos.com> - 4.9.2-0
- https://github.com/Unidata/netcdf-c/releases/tag/v4.9.2

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 4.7.3-0
- Updated to the latest stable release

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 4.6.1-0
- Updated to the latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 4.5.0-0
- Updated to the latest stable release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 4.4.1.1-0
- Initial build for kaos repository
