################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_sanitizers: %define _with_sanitizers 1}

################################################################################

%global python_base  python3
%global __python3  %{_bindir}/python3

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}
%{!?python3_lib: %global python3_lib %(%{__python3} -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))" 2>/dev/null)}
%{!?python3_inc: %global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())" 2>/dev/null)}

################################################################################

Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        1.0.1
Release:        0%{?dist}
License:        GPLv2
Group:          Development/Tools
URL:            https://github.com/rpm-software-management/createrepo_c

Source0:        https://github.com/rpm-software-management/%{name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc cmake doxygen bzip2-devel file-devel xz
BuildRequires:  glib2-devel >= 2.22.0 libcurl-devel libxml2-devel
BuildRequires:  openssl-devel sqlite-devel xz-devel zlib-devel drpm-devel
BuildRequires:  rpm-devel libmodulemd-devel libyaml-devel zchunk-devel
BuildRequires:  bash-completion

%if %{?_with_sanitizers:1}%{?_without_sanitizers:0}
BuildRequires:  libasan liblsan libubsan
%endif

Requires:       rpm

Requires:       %{name}-libs = %{version}-%{release}

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

################################################################################

%package libs

Summary:  Library for repodata manipulation
Group:    Development/Libraries

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.

################################################################################

%package devel

Summary:   Library for repodata manipulation
Group:     Development/Libraries

Requires:  pkgconfig >= 1:0.14
Requires:  pkgconfig(glib-2.0) pkgconfig(rpm) pkgconfig(libcurl)
Requires:  pkgconfig(sqlite3) pkgconfig(sqlite3) pkgconfig(libxml-2.0)
Requires:  pkgconfig(openssl)
Requires:  %{name}-libs =  %{version}-%{release}

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

################################################################################

%package -n %{python_base}-%{name}

Summary:        Python bindings for the createrepo_c library
Group:          Development/Languages

BuildRequires:  %{python_base}-devel %{python_base}-libs

Requires:       %{python_base}
Requires:       %{name} = %{version}-%{release}

%description -n %{python_base}-%{name}
Python bindings for the createrepo_c library.

################################################################################

%prep
%{crc_check}

%setup -q

%build

sed -i '/unset(PYTHON_LIBRARY/d' src/python/CMakeLists.txt
sed -i '/unset(PYTHON_INCLUDE_DIR/d' src/python/CMakeLists.txt
sed -i 's/3 EXACT/3/g' src/python/CMakeLists.txt

%if 0%{?rhel} == 9
# Fix wrong check for GLib 2.70
# https://github.com/rpm-software-management/createrepo_c/pull/342#issuecomment-1621547652
sed -i 's/g_pattern_spec_match/g_pattern_match/' src/createrepo_c.c
%endif

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
      -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
      -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
      -DPYTHON_LIBRARY:PATH=%{python3_lib} \
      -DPYTHON_INCLUDE_DIR:PATH=%{python3_inc} \
      -DENABLE_DRPM:BOOL=ON \
      -DWITH_ZCHUNK:BOOL=ON \
%if %{?_with_sanitizers:1}%{?_without_sanitizers:0}
      -DWITH_SANITIZERS=ON \
%else
      -DWITH_SANITIZERS=OFF \
%endif
      -DBUILD_SHARED_LIBS:BOOL=ON .

%{__make} %{?_smp_mflags} RPM_OPT_FLAGS="%{optflags}"
%{__make} %{?_smp_mflags} doc-c

%install
rm -rf %{buildroot}

%{make_install}

ln -sf %{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sf %{_bindir}/mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sf %{_bindir}/modifyrepo_c %{buildroot}%{_bindir}/modifyrepo
ln -sf %{_bindir}/sqliterepo_c %{buildroot}%{_bindir}/sqliterepo

%post -n %{name}-libs
/sbin/ldconfig

%postun -n %{name}-libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING AUTHORS
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c
%{_bindir}/createrepo
%{_bindir}/mergerepo
%{_bindir}/modifyrepo
%{_bindir}/sqliterepo
%{_mandir}/man8/*.8.*
%{_datadir}/bash-completion/completions/*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libcreaterepo_c.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING doc/html
%{_libdir}/libcreaterepo_c.so
%{_libdir}/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*

%files -n %{python_base}-%{name}
%defattr(-,root,root,-)
%{python3_sitearch}/*.egg-info
%{python3_sitearch}/createrepo_c/

################################################################################

%changelog
* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/1.0.0...1.0.1

* Sun Oct 01 2023 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.20.1...1.0.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.20.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.20.0...0.20.1

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.20.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.19.0...0.20.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.19.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.18.0...0.19.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.18.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.7...0.18.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.7-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.6...0.17.7

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.6-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.5...0.17.6

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.5-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.4...0.17.5

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.4-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.3...0.17.4

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.3-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.2...0.17.3

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.1...0.17.2

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.17.0...0.17.1

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.17.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.16.2...0.17.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.16.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.16.1...0.16.2

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.16.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.16.0...0.16.1

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.16.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.11...0.16.0

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.11-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.10...0.15.11

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.10-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.9...0.15.10

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.9-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.8...0.15.9

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.8-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.7...0.15.8

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.7-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.6...0.15.7

* Mon Sep 19 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.6-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.5...0.15.6

* Sun Sep 18 2022 Anton Novojilov <andy@essentialkaos.com> - 0.15.5-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.4...0.15.5

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.15.4-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.3...0.15.4

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.15.3-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.2...0.15.3

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.15.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.1...0.15.2

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.15.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.15.0...0.15.1

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.15.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.14.3...0.15.0

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 0.14.3-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.14.2...0.14.3

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.14.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.14.0...0.14.2

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.14.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.13.2...0.14.0

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.13.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.13.1...0.13.2

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 0.13.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.13.0...0.13.1

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 0.13.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.12.2...0.13.0

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.2-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.12.1...0.12.2

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.12.0...0.12.1

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-1
- Updated for compatibility with Python 3.6

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.11.1...0.12.0

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 0.11.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.11.0...0.11.1

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 0.11.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.10.0...0.11.0

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.9.1...0.10.0

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.9.0...0.9.1

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.0-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.8.1...0.9.0

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- https://github.com/rpm-software-management/createrepo_c/compare/0.7.7...0.8.1

* Thu Mar 12 2015 Anton Novojilov <andy@essentialkaos.com> - 0.7.7-0
- Initial build
