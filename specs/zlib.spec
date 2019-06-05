################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            The compression and decompression library
Name:               zlib
Version:            1.2.11
Release:            0%{?dist}
License:            zlib and Boost
Group:              System Environment/Libraries
URL:                https://www.zlib.net

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source:             https://www.zlib.net/%{name}-%{version}.tar.xz

BuildRequires:      make automake autoconf libtool

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

################################################################################

%package devel

Summary:            Header files and libraries for Zlib development
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

################################################################################

%package static

Summary:            Static libraries for Zlib development
Group:              Development/Libraries
Requires:           %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

################################################################################

%package -n minizip

Summary:            Library for manipulation with .zip archives
Group:              System Environment/Libraries
Requires:           %{name} = %{version}-%{release}

%description -n minizip
Minizip is a library for manipulation with files from .zip archives.

################################################################################

%package -n minizip-devel

Summary:            Development files for the minizip library
Group:              Development/Libraries
Requires:           minizip = %{version}-%{release}
Requires:           %{name}-devel = %{version}-%{release}

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

################################################################################

%prep
%setup -q

iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog.tmp
mv ChangeLog.tmp ChangeLog

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"

./configure --libdir=%{_libdir} \
            --includedir=%{_includedir} \
            --prefix=%{_prefix}

%{__make} %{?_smp_mflags}

pushd contrib/minizip
  autoreconf --install
  %configure --enable-static=no
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install}

pushd contrib/minizip
  %{make_install}
popd

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_includedir}/minizip/crypt.h

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post -n minizip
/sbin/ldconfig

%postun -n minizip
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/algorithm.txt test/example.c
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

################################################################################

%changelog
* Wed Jun 05 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.11-0
- Initial build for kaos repository
