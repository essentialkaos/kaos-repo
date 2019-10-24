################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         C implementation of the Git core methods as a library with a solid API
Name:            libgit2
Version:         0.28.3
Release:         0%{?dist}
Group:           Development/Libraries
License:         GPLv2 with exceptions
URL:             https://libgit2.github.com

Source0:         https://github.com/libgit2/libgit2/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc cmake python http-parser-devel libcurl-devel libssh2-devel
BuildRequires:   openssl-devel zlib-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
libgit2 is a portable, pure C implementation of the Git core methods
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.

################################################################################

%package devel
Summary:         Development files for %{name}
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

################################################################################

%prep
%setup -qn %{name}-%{version}

# Remove VCS files from examples
find examples -name ".gitignore" -delete -print

# Don't test network
sed -i 's/sonline/xonline/' tests/CMakeLists.txt

# Remove bundled libraries
rm -frv deps

%build
mkdir %{_target_platform}

pushd %{_target_platform}
  %cmake -DTHREADSAFE=ON ..
popd

%{__make} %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}

%{make_install} -C %{_target_platform}

%check
%if %{?_with_check:1}%{?_without_check:0}
pushd %{_target_platform}
  ctest -VV
popd
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc COPYING
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%doc AUTHORS docs examples README.md
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

################################################################################

%changelog
* Wed Oct 23 2019 Andrey Kulikov <avk@brewkeeper.net> - 0.28.3-0
- Initial build
