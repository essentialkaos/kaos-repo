################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            VisualOn AMR-WB encoder library
Name:               vo-amrwbenc
Version:            0.1.3
Release:            2%{?dist}
Group:              System Environment/Libraries
License:            ASL 2.0
URL:                https://sourceforge.net/projects/opencore-amr/

Source0:            https://downloads.sourceforge.net/opencore-amr/%{name}/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
This library contains an encoder implementation of the Adaptive
Multi Rate Wideband (AMR-WB) audio codec. The library is based
on a codec implementation by VisualOn as part of the Stagefright
framework from the Google Android project.

################################################################################

%package devel
Summary:            Development files for vo-amrwbenc
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
The vo-amrwbenc devel package contains libraries and header files for
developing applications that use vo-amrwbenc.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/lib%{name}.la

%clean
rm -rf %{buildroot}

%post
/bin/ldconfig

%postun
/bin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README NOTICE
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Thu Jan 25 2018 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-2
- Initial build for kaos repo
