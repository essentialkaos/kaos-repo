################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Compressed file format that allows easy deltas
Name:           zchunk
Version:        1.5.1
Release:        0%{?dist}
License:        BSD and MIT
Group:          Development/Libraries
URL:            https://github.com/zchunk/zchunk

Source0:        https://github.com/zchunk/%{name}/archive/refs/tags/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc meson epel-rpm-macros
BuildRequires:  libcurl-devel openssl-devel libzstd-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

################################################################################

%package libs

Summary:  Zchunk library
Group:    Development/Libraries

%description libs
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the zchunk library, libzck.

################################################################################

%package devel

Summary:  Headers for building against zchunk
Group:    Development/Libraries

Requires:  %{name}-libs = %{version}-%{release}
Requires:  pkgconfig(libzstd) pkgconfig(libcurl) pkgconfig(openssl)

%description devel
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the headers necessary for building against the zchunk
library, libzck.

################################################################################

%prep
%{crc_check}

%setup -q

# Remove all bundled SHA libs
rm -rf src/lib/hash/sha*

%build
%meson -Dwith-openssl=enabled \
       -Dwith-curl=enabled \
       -Dwith-zstd=enabled

%meson_build

%install
rm -rf %{buildroot}

%meson_install

install -dm 0755 %{buildroot}%{_libexecdir}
install -pm 0644 contrib/gen_xml_dictionary %{buildroot}%{_libexecdir}/zck_gen_xml_dictionary

%check
%if %{?_with_check:1}%{?_without_check:0}
%meson_test
%endif

%clean
rm -rf %{buildroot}

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md contrib
%{_bindir}/zck*
%{_bindir}/unzck
%{_libexecdir}/zck_gen_xml_dictionary
%{_mandir}/man1/*.gz

%files libs
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_libdir}/libzck.so.*

%files devel
%defattr(-,root,root,-)
%doc zchunk_format.txt
%{_libdir}/libzck.so
%{_libdir}/pkgconfig/zck.pc
%{_includedir}/zck.h

################################################################################

%changelog
* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- https://github.com/zchunk/zchunk/compare/1.4.0...1.5.1

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- https://github.com/zchunk/zchunk/compare/1.3.2...1.4.0

* Mon Oct 09 2023 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- https://github.com/zchunk/zchunk/compare/1.2.3...1.3.2

* Sat Sep 17 2022 Anton Novojilov <andy@essentialkaos.com> - 1.2.3-0
- Initial build for kaos-repo
