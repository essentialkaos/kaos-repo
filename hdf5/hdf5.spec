################################################################################

%global _configure ../configure

%global configure_opts \\\
  --disable-silent-rules \\\
  --enable-fortran \\\
  --enable-fortran2003 \\\
  --enable-hl \\\
  --enable-shared \\\
%{nil}

################################################################################

Summary:              A general purpose library and file format for storing scientific data
Name:                 hdf5
Version:              1.8.20
Release:              0%{?dist}
License:              BSD
Group:                System Environment/Libraries
URL:                  http://www.hdfgroup.org/HDF5/

Source:               http://support.hdfgroup.org/ftp/HDF5/current18/src/%{name}-%{version}.tar.bz2
Source1:              h5comp

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc gcc-c++ automake libtool openssh-clients
BuildRequires:        krb5-devel openssl-devel zlib-devel gcc-gfortran time
BuildRequires:        chrpath

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.

################################################################################

%package devel
Summary:            HDF5 development files
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           zlib-devel

%description devel
HDF5 development headers and libraries.

################################################################################

%package static
Summary:            HDF5 static libraries
Group:              Development/Libraries

Requires:           %{name}-devel = %{version}-%{release}

%description static
HDF5 static libraries.

################################################################################

%prep
%setup -q

%build

export CC=gcc
export CXX=g++
export F9X=gfortran
export CFLAGS="${RPM_OPT_FLAGS/O2/O0}"

mkdir build
pushd build
  ln -s ../configure .
  %configure %{configure_opts} --enable-cxx
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install} -C build

rm %{buildroot}%{_libdir}/*.la

mkdir -p %{buildroot}%{_fmoddir}
mv %{buildroot}%{_includedir}/*.mod %{buildroot}%{_fmoddir}
find %{buildroot}%{_datadir} \( -name '*.[ch]*' -o -name '*.f90' \) -exec chmod -x {} +

%ifarch x86_64
sed -i -e s/H5pubconf.h/H5pubconf-64.h/ %{buildroot}%{_includedir}/H5public.h
mv %{buildroot}%{_includedir}/H5pubconf.h \
   %{buildroot}%{_includedir}/H5pubconf-64.h
for x in h5c++ h5cc h5fc ; do
  mv %{buildroot}%{_bindir}/${x} \
     %{buildroot}%{_bindir}/${x}-64
  install -m 0755 %SOURCE1 %{buildroot}%{_bindir}/${x}
done
%else
sed -i -e s/H5pubconf.h/H5pubconf-32.h/ %{buildroot}%{_includedir}/H5public.h
mv %{buildroot}%{_includedir}/H5pubconf.h \
   %{buildroot}%{_includedir}/H5pubconf-32.h
for x in h5c++ h5cc h5fc ; do
  mv %{buildroot}%{_bindir}/${x} \
     %{buildroot}%{_bindir}/${x}-32
  install -m 0755 %SOURCE1 %{buildroot}%{_bindir}/${x}
done
%endif

chrpath --delete %{buildroot}%{_bindir}/gif2h5
chrpath --delete %{buildroot}%{_bindir}/h52gif
chrpath --delete %{buildroot}%{_bindir}/h5copy
chrpath --delete %{buildroot}%{_bindir}/h5debug
chrpath --delete %{buildroot}%{_bindir}/h5diff
chrpath --delete %{buildroot}%{_bindir}/h5dump
chrpath --delete %{buildroot}%{_bindir}/h5import
chrpath --delete %{buildroot}%{_bindir}/h5jam
chrpath --delete %{buildroot}%{_bindir}/h5ls
chrpath --delete %{buildroot}%{_bindir}/h5mkgrp
chrpath --delete %{buildroot}%{_bindir}/h5perf_serial
chrpath --delete %{buildroot}%{_bindir}/h5repack
chrpath --delete %{buildroot}%{_bindir}/h5repart
chrpath --delete %{buildroot}%{_bindir}/h5stat
chrpath --delete %{buildroot}%{_bindir}/h5unjam
chrpath --delete %{buildroot}%{_libdir}/*.so.*

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY*.txt
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5copy
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5mkgrp
%{_bindir}/h5perf_serial
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5stat
%{_bindir}/h5unjam
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/h5c++*
%{_bindir}/h5cc*
%{_bindir}/h5fc*
%{_bindir}/h5redeploy
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.settings
%{_fmoddir}/*.mod
%{_datadir}/hdf5_examples/

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

################################################################################

%changelog
* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.8.20-0
- Updated to latest stable release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.19-0
- Updated to latest stable release

* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.18-0
- Initial build for kaos repository
