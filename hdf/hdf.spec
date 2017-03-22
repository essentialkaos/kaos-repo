###############################################################################

Summary:            A general purpose library and file format for storing scientific data
Name:               hdf
Version:            4.2.12
Release:            0%{?dist}
License:            BSD
Group:              System Environment/Libraries
URL:                http://hdfgroup.org/products/hdf4/index.html

Source:             http://www.hdfgroup.org/ftp/HDF/releases/HDF%{version}/src/%{name}-%{version}.tar.bz2

Patch0:             %{name}-4.2.5-maxavailfiles.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ gcc-gfortran automake libtool
BuildRequires:      flex byacc libjpeg-devel zlib-devel

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
HDF is a general purpose library and file format for storing scientific data.
HDF can store two primary objects: datasets and groups. A dataset is 
essentially a multidimensional array of data elements, and a group is a 
structure for organizing objects in an HDF file. Using these two basic 
objects, one can create and store almost any kind of scientific data 
structure, such as images, arrays of vectors, and structured and unstructured 
grids. You can also mix and match them in HDF files according to your needs.

###############################################################################

%package devel
Summary:            HDF development files
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           libjpeg-devel zlib-devel

Provides:           %{name}-static = %{version}-%{release}

%description devel
HDF development headers and libraries.

###############################################################################

%prep
%setup -q

%patch0 -p1 -b .maxavailfiles

chmod a-x *hdf/*/*.c hdf/*/*.h

%build
rm config/*linux-gnu

export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export FFLAGS="$RPM_OPT_FLAGS -fPIC -ffixed-line-length-none"

%configure --disable-production \
           --disable-netcdf \
           --includedir=%{_includedir}/%{name} \
           --libdir=%{_libdir}/%{name}

%{__make} %{?_smp_mflags}

touch -c -r hdf/src/hdf.inc hdf/src/hdf.f90
touch -c -r hdf/src/dffunc.inc hdf/src/dffunc.f90
touch -c -r mfhdf/fortran/mffunc.inc mfhdf/fortran/mffunc.f90

%install
rm -rf %{buildroot}

%{make_install} INSTALL='install -p'

for file in ncdump ncgen ; do
  mv %{buildroot}%{_bindir}/$file %{buildroot}%{_bindir}/h$file
  rm %{buildroot}%{_mandir}/man1/${file}.1
done

touch -c -r README.txt %{buildroot}%{_includedir}/%{name}/h4config.h

# Remove an autoconf conditional from the API that is unused and cause
# the API to be different on x86 and x86_64
pushd %{buildroot}%{_includedir}/hdf
  grep -v 'H4_SIZEOF_INTP' h4config.h > h4config.h.tmp
  touch -c -r h4config.h h4config.h.tmp
  mv h4config.h.tmp h4config.h
popd

install -dm 755 %{buildroot}%{_defaultdocdir}/%{name}

mv %{buildroot}%{_prefix}/examples %{buildroot}%{_defaultdocdir}/%{name}/

%check
make check

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_notes/*.txt
%exclude %{_defaultdocdir}/%{name}/examples
%{_bindir}/*
%{_mandir}/man1/*.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/%{name}/
%{_defaultdocdir}/%{name}/examples

###############################################################################

%changelog
* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 4.2.12-0
- Initial build for kaos repository
