################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        GMerlin Audio Video Library
Name:           gavl
Version:        1.4.0
Release:        1%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
URL:            https://gmerlin.sourceforge.net/gavl_frame.html

Source0:        https://downloads.sourceforge.net/gmerlin/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake make gcc libtool doxygen
BuildRequires:  autoconf >= 2.50 libpng-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
GMerlin Audio Video Library.

################################################################################

%package devel
Summary:   Header files for gavl library
Group:     Development/Libraries

Requires:  %{name} = %{version}-%{release}

%description devel
This is the package containing the header files for gavl library.

################################################################################

%prep
%{crc_check}

%setup -q

%build
libtoolize
aclocal -I m4
autoconf
autoheader
automake --add-missing

%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -Rf %{buildroot}%{_libdir}/*.la
rm -Rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.1

%files devel
%defattr(644,root,root,755)
%{?with_apidocs:%doc doc/apiref}
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-1
- Fixed problems with executing ldconfig

* Wed Apr 13 2016 Gleb Goncharov <yum@gongled.me> - 1.4.0-0
- Initial build
