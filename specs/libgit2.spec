################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         C implementation of the Git core methods as a library with a solid API
Name:            libgit2
Version:         0.28.4
Release:         0%{?dist}
Group:           Development/Libraries
License:         GPLv2 with exceptions
URL:             https://libgit2.github.com

Source0:         https://github.com/libgit2/libgit2/archive/v%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

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
%{crc_check}

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
* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 0.28.4-0
- CVE-2019-1348: the fast-import stream command "feature
  export-marks=path" allows writing to arbitrary file paths. As
  libgit2 does not offer any interface for fast-import, it is not
  susceptible to this vulnerability.
- CVE-2019-1349: by using NTFS 8.3 short names, backslashes or
  alternate filesystreams, it is possible to cause submodules to
  be written into pre-existing directories during a recursive
  clone using git. As libgit2 rejects cloning into non-empty
  directories by default, it is not susceptible to this
  vulnerability.
- CVE-2019-1350: recursive clones may lead to arbitrary remote
  code executing due to improper quoting of command line
  arguments. As libgit2 uses libssh2, which does not require us
  to perform command line parsing, it is not susceptible to this
  vulnerability.
- CVE-2019-1351: Windows provides the ability to substitute
  drive letters with arbitrary letters, including multi-byte
  Unicode letters. To fix any potential issues arising from
  interpreting such paths as relative paths, we have extended
  detection of DOS drive prefixes to accomodate for such cases.
- CVE-2019-1352: by using NTFS-style alternative file streams for
  the ".git" directory, it is possible to overwrite parts of the
  repository. While this has been fixed in the past for Windows,
  the same vulnerability may also exist on other systems that
  write to NTFS filesystems. We now reject any paths starting
  with ".git:" on all systems.
- CVE-2019-1353: by using NTFS-style 8.3 short names, it was
  possible to write to the ".git" directory and thus overwrite
  parts of the repository, leading to possible remote code
  execution. While this problem was already fixed in the past for
  Windows, other systems accessing NTFS filesystems are
  vulnerable to this issue too. We now enable NTFS protecions by
  default on all systems to fix this attack vector.
- CVE-2019-1354: on Windows, backslashes are not a valid part of
  a filename but are instead interpreted as directory separators.
  As other platforms allowed to use such paths, it was possible
  to write such invalid entries into a Git repository and was
  thus an attack vector to write into the ".git" dierctory. We
  now reject any entries starting with ".git" on all systems.
- CVE-2019-1387: it is possible to let a submodule's git
  directory point into a sibling's submodule directory, which may
  result in overwriting parts of the Git repository and thus lead
  to arbitrary command execution. As libgit2 doesn't provide any
  way to do submodule clones natively, it is not susceptible to
  this vulnerability. Users of libgit2 that have implemented
  recursive submodule clones manually are encouraged to review
  their implementation for this vulnerability.

* Wed Oct 23 2019 Andrey Kulikov <avk@brewkeeper.net> - 0.28.3-0
- Initial build
