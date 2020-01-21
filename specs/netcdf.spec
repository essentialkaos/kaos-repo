################################################################################

%{!?_without_check: %define _with_check 1}

# Do out of tree builds
%global _configure ../configure

# Common configure options
%global configure_opts \\\
           --enable-shared \\\
           --enable-netcdf-4 \\\
           --enable-dap \\\
           --enable-extra-example-tests \\\
           CPPFLAGS=-I%{_includedir}/hdf \\\
           LIBS="-ldf -ljpeg" \\\
           --enable-hdf4 \\\
           --disable-dap-remote-tests \\\
%{nil}

################################################################################

Summary:            Libraries for the Unidata network Common Data Form
Name:               netcdf
Version:            4.7.3
Release:            0%{?dist}
License:            NetCDF
Group:              Applications/Engineering
URL:                https://www.unidata.ucar.edu/downloads/netcdf/

Source0:            https://www.unidata.ucar.edu/downloads/%{name}/ftp/%{name}-c-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc chrpath doxygen hdf-static gawk
BuildRequires:      libcurl-devel m4 zlib-devel openssh-clients
BuildRequires:      hdf5-devel >= 1.10

Requires:           hdf5 >= 1.10

Provides:           %{name} = %{version}-%{release}

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
Summary:            Development files for netcdf
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig hdf5-devel libcurl-devel

%description devel
This package contains the netCDF C header files, shared devel libs, and
man pages.

################################################################################

%package static
Summary:            Static libs for netcdf
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description static
This package contains the netCDF C static libs.

################################################################################

%prep
%setup -qn %{name}-c-%{version}

%build
export LDFLAGS="-Wl,-z,relro -L%{_libdir}/hdf"

# Serial build
mkdir build
pushd build
  ln -s ../configure .
  %configure %{configure_opts}
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install} -C build

chrpath --delete %{buildroot}%{_bindir}/nc{copy,dump,gen,gen3}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} -C build check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%{_bindir}/nccopy
%{_bindir}/ncdump
%{_bindir}/ncgen
%{_bindir}/ncgen3
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
* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 4.7.3-0
- Updated to the latest stable release

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 4.6.1-0
- Updated to the latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 4.5.0-0
- Updated to the latest stable release

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 4.4.1.1-0
- Initial build for kaos repository
