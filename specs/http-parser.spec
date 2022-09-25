################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         HTTP request/response parser for C
Name:            http-parser
Version:         2.9.4
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             https://github.com/nodejs/http-parser

Source:          https://github.com/nodejs/http-parser/archive/v%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc cmake

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).

################################################################################

%package devel
Summary:         Development headers and libraries for http-parser
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

%description devel
Development headers and libraries for http-parser.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

cat > CMakeLists.txt << EOF
cmake_minimum_required (VERSION 2.8.5)
project (http-parser C)
include (GNUInstallDirs)

set (SRCS http_parser.c)
set (HDRS http_parser.h)
set (TEST_SRCS test.c)

# Non-Strict version
add_library (http_parser \${SRCS})
target_compile_definitions (http_parser
                            PUBLIC -DHTTP_PARSER_STRICT=0)
add_executable (test-nonstrict \${TEST_SRCS})
target_link_libraries (test-nonstrict http_parser)
# Strict version
add_library (http_parser_strict \${SRCS})
target_compile_definitions (http_parser_strict
                            PUBLIC -DHTTP_PARSER_STRICT=1)
add_executable (test-strict \${TEST_SRCS})
target_link_libraries (test-strict http_parser_strict)

set_target_properties (http_parser http_parser_strict
                       PROPERTIES
                           SOVERSION 2
                           VERSION %{version})

install (TARGETS http_parser http_parser_strict
         LIBRARY DESTINATION \${CMAKE_INSTALL_LIBDIR})
install (FILES \${HDRS}
         DESTINATION \${CMAKE_INSTALL_INCLUDEDIR})

enable_testing ()
add_test (NAME test-nonstrict COMMAND test-nonstrict)
add_test (NAME test-strict COMMAND test-strict)
EOF

%build
mkdir %{_target_platform}
pushd %{_target_platform}
  %cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo \
            --no-warn-unused-cli
popd

%{__make} %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}

%{make_install} -C %{_target_platform}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} test
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
%doc AUTHORS README.md LICENSE-MIT
%{_libdir}/libhttp_parser.so.*
%{_libdir}/libhttp_parser_strict.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/http_parser.h
%{_libdir}/libhttp_parser.so
%{_libdir}/libhttp_parser_strict.so

################################################################################

%changelog
* Sun Sep 25 2022 Anton Novojilov <andy@essentialkaos.com> - 2.9.4-0
- Updated to the latest stable release

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.9.2-0
- Updated to the latest stable release

* Fri Jan 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.9.0-0
- Updated to the latest stable release

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- Updated to the latest stable release

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- Updated to the latest stable release

* Thu Aug 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- Initial build
