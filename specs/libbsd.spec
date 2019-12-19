################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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

Summary:         Library providing BSD-compatible functions for portability
Name:            libbsd
Version:         0.10.0
Release:         0%{?dist}
License:         MIT
Group:           System Environment/Libraries
URL:             https://libbsd.freedesktop.org

Source0:         https://gitlab.freedesktop.org/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc gcc-c++ automake libtool autoconf >= 2.67

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

################################################################################

%package devel
Requires:       %{name} = %{version}
Summary:        Header files for libbsd package
Group:          Development/Libraries

%description devel
Header files for libbsd package.

################################################################################

%prep
%{crc_check}

%setup -q
echo %{version} > .dist-version

%build
./autogen
%configure --disable-static
%{__make} CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
rm -rf %{buildroot}

%{make_install} libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot}

find %{buildroot}%{_libdir} -name '*.a' -delete
find %{buildroot}%{_libdir} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING TODO
%{_libdir}/%{name}.so
%{_libdir}/%{name}.so.0*

%files devel
%defattr(-,root,root)
%doc README COPYING TODO
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-*.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

################################################################################

%changelog
* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- Updated to the latest stable release

* Mon Aug 06 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.9.1-0
- Initial build
