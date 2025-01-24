################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Cross-platform asychronous I/O
Name:           libuv
Version:        1.50.0
Release:        0%{?dist}
License:        MIT, BSD and ISC
Group:          Development/Tools
URL:            https://libuv.org

Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.pc.in

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc libtool autoconf automake

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
A multi-platform support library with a focus on asynchronous I/O.
It was primarily developed for use by Node.js, but it’s also used by Luvit,
Julia, pyuv, and others.

################################################################################

%package devel
Summary:  Development libraries for libuv
Group:    Development/Tools

Requires:  pkgconfig
Requires:  %{name} = %{version}-%{release}

%description devel
Development libraries for libuv.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'

./autogen.sh

%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_libdir}/pkgconfig

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}%{_libdir}/pkgconfig/libuv.pc

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc README.md AUTHORS LICENSE
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md AUTHORS LICENSE
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/uv/*.h
%{_libdir}/pkgconfig/*.pc

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.50.0-0
- https://github.com/libuv/libuv/releases/tag/v1.50.0

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.49.2-0
- https://github.com/libuv/libuv/releases/tag/v1.49.2

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.49.1-0
- https://github.com/libuv/libuv/releases/tag/v1.49.1

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.49.0-0
- https://github.com/libuv/libuv/releases/tag/v1.49.0

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.48.0-0
- https://github.com/libuv/libuv/releases/tag/v1.48.0

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.47.0-0
- https://github.com/libuv/libuv/releases/tag/v1.47.0

* Sun Jul 09 2023 Anton Novojilov <andy@essentialkaos.com> - 1.46.0-0
- https://github.com/libuv/libuv/releases/tag/v1.46.0

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 1.34.0-0
- https://github.com/libuv/libuv/releases/tag/v1.34.0

* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.30.1-0
- https://github.com/libuv/libuv/releases/tag/v1.30.1

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.25.0-0
- https://github.com/libuv/libuv/releases/tag/v1.25.0

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.24.0-0
- https://github.com/libuv/libuv/releases/tag/v1.24.0

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.23.1-0
- https://github.com/libuv/libuv/releases/tag/v1.23.1

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.23.0-0
- https://github.com/libuv/libuv/releases/tag/v1.23.0

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.21.0-0
- https://github.com/libuv/libuv/releases/tag/v1.21.0

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.20.3-0
- https://github.com/libuv/libuv/releases/tag/v1.20.3

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 1.19.2-0
- https://github.com/libuv/libuv/releases/tag/v1.19.2

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.19.1-0
- https://github.com/libuv/libuv/releases/tag/v1.19.1

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.16.1-0
- https://github.com/libuv/libuv/releases/tag/v1.16.1

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.14.1-0
- https://github.com/libuv/libuv/releases/tag/v1.14.1

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.13.1-0
- https://github.com/libuv/libuv/releases/tag/v1.13.1

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-1
- Minor spec improvement

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-0
- https://github.com/libuv/libuv/releases/tag/v1.11.0

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- https://github.com/libuv/libuv/releases/tag/v1.10.2

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- https://github.com/libuv/libuv/releases/tag/v1.10.0

* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.1-0
- Initial build
