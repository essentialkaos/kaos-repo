################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%ifarch %{ix86} x86_64
%global dispatch 1
%global moreflags_dispatch -DXXH_X86DISPATCH_ALLOW_AVX
%else
%global dispatch 0
%global moreflags_dispatch %{nil}
%endif

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Extremely fast hash algorithm
Name:           xxhash
Version:        0.8.2
Release:        0%{?dist}
License:        BSD-2-Clause AND GPL-2.0-or-later
Group:          System Environment/Libraries
URL:            https://www.xxhash.com

Source0:        https://github.com/Cyan4973/xxHash/archive/v%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc doxygen

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

################################################################################

%package libs
Summary:  Extremely fast hash algorithm - library
Group:    Development/Libraries

%description libs
xxHash is an Extremely fast Hash algorithm, running at RAM speed
limits. It successfully completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash
functions. Code is highly portable, and hashes are identical on all
platforms (little / big endian).

################################################################################

%package devel
Summary:  Extremely fast hash algorithm - development files
Group:    Development/Libraries

Requires: %{name}-libs = %{version}-%{release}

Provides: %{name}-static = %{version}-%{release}

%description devel
Development files for the xxhash library

################################################################################

%package doc
Summary:  Extremely fast hash algorithm - documentation files
Group:    Documentation

BuildArch:  noarch

%description doc
Documentation files for the xxhash library

################################################################################

%prep
%{crc_check}

%setup -qn xxHash-%{version}

%build
%{make_build} \
    MOREFLAGS="%{__global_cflags} %{?__global_ldflags} %{moreflags_dispatch}" \
    DISPATCH=%{dispatch}

doxygen

%install
rm -rf %{buildroot}

%{make_install} PREFIX=%{_prefix} LIBDIR=%{_libdir}

rm -f %{buildroot}%{_libdir}/libxxhash.a

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%{__make} test-xxhsum-c
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc cli/README.md cli/COPYING
%{_bindir}/xxh*sum
%{_mandir}/man1/xxh*sum.1*

%files libs
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_libdir}/libxxhash.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}.h
%{_includedir}/xxh3.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%files doc
%defattr(-,root,root,-)
%doc doxygen/html

################################################################################

%changelog
* Sat Oct 28 2023 Anton Novojilov <andy@essentialkaos.com> - 0.8.2-0
- Initial build for kaos repository
