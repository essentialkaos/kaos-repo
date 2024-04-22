################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Zstandard (zstd) compression library
Name:           zstd
Version:        1.5.6
Release:        0%{?dist}
License:        BSD and GPLv2
Group:          Development/Libraries
URL:            https://github.com/facebook/zstd

Source0:        https://github.com/facebook/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

################################################################################

%package -n lib%{name}

Summary:  Zstandard (zstd) shared library
Group:    Development/Libraries

%description -n lib%{name}
Zstandard compression shared library.

################################################################################

%package -n lib%{name}-devel

Summary:  Header files for Zstandard (zstd) library
Group:    Development/Libraries

Requires:  lib%{name} = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstandard library.

################################################################################

%package -n lib%{name}-static

Summary:  Static variant of the Zstandard (zstd) library
Group:    Development/Libraries

Requires:  lib%{name}-devel = %{version}-%{release}

%description -n lib%{name}-static
Static variant of the Zstandard library.

################################################################################

%prep
%{crc_check}

%setup -q

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"

for dir in lib programs; do
  %make_build -C "$dir" ZSTD_NO_ASM=1
done

%install
rm -rf %{buildroot}

%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING LICENSE CHANGELOG README.md
%{_bindir}/%{name}*
%{_bindir}/un%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/un%{name}.1*
%{_mandir}/man1/%{name}cat.1*
%{_mandir}/man1/%{name}grep.1*
%{_mandir}/man1/%{name}less.1*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc COPYING LICENSE
%{_libdir}/lib%{name}.so.*

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%{_includedir}/zdict.h
%{_includedir}/%{name}.h
%{_includedir}/%{name}_errors.h
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/lib%{name}.so

%files -n lib%{name}-static
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.a

################################################################################

%changelog
* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.5.6-0
- https://github.com/facebook/zstd/releases/tag/v1.5.6

* Wed Apr 19 2023 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- https://github.com/facebook/zstd/releases/tag/v1.5.5

* Sat Sep 17 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Initial build for kaos-repo
