################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        A general purpose library and file format for storing scientific data
Name:           hdf
Version:        4.2.16
Release:        0%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            https://portal.hdfgroup.org/display/HDF4/HDF4

Source0:        https://support.hdfgroup.org/ftp/HDF/releases/HDF%{version}/src/%{name}-%{version}.tar.bz2

Source100:      checksum.sha512

Patch0:         %{name}-maxavailfiles.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ gcc-gfortran automake libtool chrpath
BuildRequires:  flex byacc libjpeg-turbo-devel zlib-devel libtirpc-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
HDF is a general purpose library and file format for storing scientific data.
HDF can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF files according to your needs.

################################################################################

%package devel
Summary:  HDF4 development files
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}
Requires:  libjpeg-turbo-devel zlib-devel

Provides:  %{name}-static = %{version}-%{release}

%description devel
HDF4 development headers and libraries.

################################################################################

%package libs
Summary:  HDF4 shared libraries
Group:    Development/Libraries

%description libs
HDF4 shared libraries.

################################################################################

%package static
Summary:  HDF4 static libraries
Group:    Development/Libraries

Requires:  %{name}-devel = %{version}-%{release}

%description static
HDF4 static libraries.

################################################################################

%prep
%crc_check
%autosetup -p1

# perfecto:ignore
chmod a-x *hdf/*/*.c hdf/*/*.h

%build
rm config/*linux-gnu

export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export CPPFLAGS="%{optflags} -fPIC"
export LIBS="-ltirpc"

mkdir build-static
pushd build-static
  ln -s ../configure .
  %configure --disable-production \
             --disable-netcdf \
             --enable-shared=no \
             --enable-static=yes \
             --includedir=%{_includedir}/%{name}

  %{__make} %{?_smp_mflags}
popd

mkdir build-shared
pushd build-shared
  ln -s ../configure .
  %configure --disable-production \
             --disable-netcdf \
             --enable-shared=yes \
             --enable-static=no \
             --includedir=%{_includedir}/%{name}

  %{__make} %{?_smp_mflags}
popd

touch -c -r hdf/src/hdf.inc hdf/src/hdf.f90
touch -c -r hdf/src/dffunc.inc hdf/src/dffunc.f90
touch -c -r mfhdf/fortran/mffunc.inc mfhdf/fortran/mffunc.f90

%install
rm -rf %{buildroot}

%make_install -C build-static
%make_install -C build-shared

rm -f %{buildroot}%{_libdir}/*.la

chrpath --delete \
        --keepgoing \
        %{buildroot}%{_bindir}/* \
        %{buildroot}%{_libdir}/%{name}/*.so.* \
        %{buildroot}%{_libdir}/*.so.* || :

for file in ncdump ncgen ; do
  mv %{buildroot}%{_bindir}/$file %{buildroot}%{_bindir}/h$file
  rm %{buildroot}%{_mandir}/man1/${file}.1
done

# Remove an autoconf conditional from the API that is unused and cause
# the API to be different on x86 and x86_64
pushd %{buildroot}%{_includedir}/hdf
  grep -v 'H4_SIZEOF_INTP' h4config.h > h4config.h.tmp
  touch -c -r h4config.h h4config.h.tmp
  mv h4config.h.tmp h4config.h
popd

install -dm 755 %{buildroot}%{_defaultdocdir}/%{name}

mv %{buildroot}%{_datadir}/hdf4_examples \
   %{buildroot}%{_defaultdocdir}/%{name}/examples

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} -C build-shared check
%{__make} -C build-static check
%endif

%clean
rm -rf %{buildroot}

%post
%{_sbindir}/ldconfig

%postun
%{_sbindir}/ldconfig

%post libs
%{_sbindir}/ldconfig

%postun libs
%{_sbindir}/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README.md release_notes/*.txt
%exclude %{_defaultdocdir}/%{name}/examples
%{_bindir}/*
%exclude %{_bindir}/h4?c*
%{_libdir}/*.so.0*
%{_mandir}/man1/*.gz

%files devel
%defattr(-,root,root,-)
%{_bindir}/h4?c*
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/*.settings
%{_defaultdocdir}/%{name}/examples

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.0*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

################################################################################

%changelog
* Wed Sep 27 2023 Anton Novojilov <andy@essentialkaos.com> - 4.2.16-0
- https://support.hdfgroup.org/ftp/HDF/releases/HDF4.2.16/src/hdf-4.2.16-RELEASE.txt

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 4.2.14-0
- Updated to latest stable release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 4.2.13-0
- Updated to latest stable release

* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 4.2.12-0
- Initial build for kaos repository
