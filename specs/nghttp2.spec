################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:         Meta-package that only requires libnghttp2
Name:            nghttp2
Version:         1.40.0
Release:         0%{?dist}
Group:           Applications/Internet
License:         MIT
URL:             https://nghttp2.org

Source0:         https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.bz2

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc openssl-devel zlib-devel

Requires:        libnghttp2%{?_isa} = %{version}-%{release}

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
This package installs no files. It only requires the libnghttp2 package.

################################################################################

%package -n libnghttp2

Summary:         A library implementing the HTTP/2 protocol
Group:           Development/Libraries

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.

################################################################################

%package -n libnghttp2-devel

Summary:         Files needed for building applications with libnghttp2
Group:           Development/Libraries

Requires:        libnghttp2%{?_isa} = %{version}-%{release}
Requires:        pkgconfig

%description -n libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure \
  --disable-python-bindings \
  --disable-static \
  --without-libxml2 \
  --without-spdylay

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install}

# not needed on Fedora/RHEL
rm -f %{buildroot}%{_libdir}/libnghttp2.la

# will be installed via %%doc
rm -f %{buildroot}%{_datadir}/doc/nghttp2/README.rst

# do not install man pages and helper scripts for tools that are not available
rm -fr %{buildroot}%{_datadir}/nghttp2
rm -fr %{buildroot}%{_mandir}/man1

%post -n libnghttp2
/sbin/ldconfig

%postun -n libnghttp2
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
# No files for you!

%files -n libnghttp2
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_libdir}/libnghttp2.so.*

%files -n libnghttp2-devel
%defattr(-,root,root,-)
%doc README.rst
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/libnghttp2.pc
%{_libdir}/libnghttp2.so

################################################################################

%changelog
* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.40.0-0
- Updated to the latest stable release

* Sun Aug 18 2019 Anton Novojilov <andy@essentialkaos.com> - 1.39.1-0
- Updated to the latest stable release

* Sat Nov 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.34.0-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.33.0-0
- Updated to the latest stable release

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.32.0-0
- Updated to the latest stable release

* Fri Apr 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.31.1-0
- Updated to the latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.27.0-0
- Updated to the latest stable release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.25.0-0
- Updated to the latest stable release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.24.0-0
- Updated to the latest stable release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.22.0-0
- Updated to the latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.20.0-0
- Updated to the latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.19.0-0
- Updated to the latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.18.1-0
- Updated to the latest stable release

* Tue Nov 01 2016 Anton Novojilov <andy@essentialkaos.com> - 1.16.0-0
- Initial build for kaos repository
