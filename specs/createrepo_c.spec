################################################################################

%if 0%{?rhel} >= 7
%global python_base python36
%global __python3   %{_bindir}/python3.6
%else
%global python_base python34
%global __python3   %{_bindir}/python3.4
%endif

%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}
%{!?python3_lib: %global python3_lib %(%{__python3} -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))" 2>/dev/null)}
%{!?python3_inc: %global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())" 2>/dev/null)}

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

################################################################################

Summary:            Creates a common metadata repository
Name:               createrepo_c
Version:            0.12.0
Release:            1%{?dist}
License:            GPLv2
Group:              Development/Tools
URL:                https://github.com/rpm-software-management/createrepo_c

Source0:            https://github.com/rpm-software-management/%{name}/archive/%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc cmake doxygen bzip2-devel expat-devel file-devel
BuildRequires:      glib2-devel >= 2.22.0 libcurl-devel libxml2-devel
BuildRequires:      openssl-devel sqlite-devel xz-devel zlib-devel
BuildRequires:      rpm-devel >= 4.8.0-28

%if 0%{?rhel} == 6
Requires:           rpm >= 4.8.0-28
%else
BuildRequires:      bash-completion zchunk pkgconfig(zck) >= 0.9.11
Requires:           rpm >= 4.9.0
%endif

Requires:           %{name}-libs = %{version}-%{release}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

################################################################################

%package libs

Summary:            Library for repodata manipulation
Group:              Development/Libraries

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.

################################################################################

%package devel

Summary:            Library for repodata manipulation
Group:              Development/Libraries

Requires:           pkgconfig >= 1:0.14
Requires:           %{name}-libs =  %{version}-%{release}

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

################################################################################

%package -n %{python_base}-%{name}

Summary:            Python bindings for the createrepo_c library
Group:              Development/Languages

BuildRequires:      %{python_base}-devel %{python_base}-libs %{python_base}-nose

Requires:           %{python_base}

Requires:           %{name} = %{version}-%{release}

%description -n %{python_base}-%{name}
Python bindings for the createrepo_c library.

################################################################################

%prep
%setup -q

%build

sed -i '/unset(PYTHON_LIBRARY/d' src/python/CMakeLists.txt
sed -i '/unset(PYTHON_INCLUDE_DIR/d' src/python/CMakeLists.txt

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
      -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
      -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
      -DPYTHON_LIBRARY:PATH=%{python3_lib} \
      -DPYTHON_INCLUDE_DIR:PATH=%{python3_inc} \
%if 0%{?rhel} >= 7
      -DWITH_ZCHUNK:BOOL=ON \
%else
      -DWITH_ZCHUNK:BOOL=OFF \
%endif
      -DBUILD_SHARED_LIBS:BOOL=ON .

%{__make} %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
%{__make} %{?_smp_mflags} doc-c

%install
rm -rf %{buildroot}

%{make_install}

%post -n %{name}-libs
%{__ldconfig}

%postun -n %{name}-libs
%{__ldconfig}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING AUTHORS
%{_mandir}/man8/*.8.*
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c
%if 0%{?rhel} >= 7
%{_datadir}/bash-completion/completions/*
%endif

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
%{python3_sitearch}/createrepo_c/

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-1
- Updated for compatibility with Python 3.6

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 0.12.0-0
- Updated to 0.12.0

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 0.11.1-0
- Updated to 0.11.1

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 0.11.0-0
- Updated to 0.11.0

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- Updated to 0.10.0

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- Updated to 0.9.1

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.0-0
- Updated to 0.9.0

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to 0.8.1

* Thu Mar 12 2015 Anton Novojilov <andy@essentialkaos.com> - 0.7.7-0
- Initial build
