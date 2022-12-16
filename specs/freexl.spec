################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            Library to extract data from within an Excel spreadsheet
Name:               freexl
Version:            1.0.6
Release:            0%{?dist}
License:            MIT
Group:              System Environment/Libraries
URL:                https://www.gaia-gis.it/FreeXL

Source0:            https://www.gaia-gis.it/gaia-sins/freexl-sources/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc doxygen

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
FreeXL is a library to extract valid data
from within an Excel spreadsheet (.xls)

Design goals:
- simple and lightweight
- stable, robust and efficient
- easily and universally portable
- completely ignore any GUI-related oddity

################################################################################

%package devel
Summary:            Development Libraries for FreeXL
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure --enable-gcov=no \
           --disable-static

%{__make} %{?_smp_mflags}

# Mailed the author on Dec 5th 2011
# Preserve date of header file
sed -i 's/^INSTALL_HEADER = \$(INSTALL_DATA)/& -p/' headers/Makefile.in

# Generate HTML documentation and clean unused installdox script
doxygen

rm -f html/installdox

%install
rm -rf %{buildroot}

%{make_install}

# Delete undesired libtool archives
rm -f %{buildroot}%{_libdir}/lib%{name}.la

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

# Clean up
pushd examples
  %{__make} clean
popd

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc examples html
%{_includedir}/freexl.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/freexl.pc

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.0.6-0
- Updated to the latest stable release

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.5-0
- Updated to the latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.4-0
- Updated to the latest stable release

* Mon Mar 20 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Initial build for kaos repository
