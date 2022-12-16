################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            Portable libraries for the high quality Dirac video codec
Name:               schroedinger
Version:            1.0.11
Release:            3%{?dist}
Group:              System Environment/Libraries
License:            LGPL
URL:                https://sourceforge.net/projects/schrodinger/

Source0:            %{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool
BuildRequires:      orc-devel >= 0.4.10 glew-devel >= 1.5.1

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
The Schrödinger project will implement portable libraries for the high
quality Dirac video codec created by BBC Research and Development.
Dirac is a free and open source codec producing very high image quality video.

The Schrödinger project is a project done by BBC R&D and Fluendo in
order to create a set of high quality decoder and encoder libraries
for the Dirac video codec.

################################################################################

%package devel
Summary:            Development files for schroedinger
Group:              Development/Libraries

Requires:           orc-devel >= 0.4.10
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for schroedinger.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
%configure --disable-static

sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING* NEWS TODO
%{_libdir}/lib%{name}-*.so.*

################################################################################

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/%{name}-*.pc

################################################################################

%changelog
* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-3
- Minor improvements

* Wed Jan 25 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-2
- Minor improvements

* Thu Nov 24 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-1
- Fixed dependencies for devel package

* Wed Apr 20 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-0
- Updated to latest stable release
