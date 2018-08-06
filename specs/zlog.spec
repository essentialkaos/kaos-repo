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

Summary:         A high-performance, thread safe, pure C logging library
Name:            zlog
Version:         1.2.12
Release:         0%{?dist}
License:         LGPL-2.1
Group:           Development/Libraries
URL:             https://github.com/HardySimpson/zlog

Source0:         https://github.com/HardySimpson/%{name}/archive/%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   autoconf automake libtool make gcc

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
zlog is a reliable, high-performance, thread safe, flexible, clear-model, pure
C logging library. Actually, in the C world there is NO good logging library
for application like logback in java or log4cxx in c++. printf can work, but
can not be easily redirected or reformat. syslog is slow and is designed for
system use.

################################################################################

%package devel
Requires:       %{name} = %{version}
Summary:        Header files and static libraries for zlog package
Group:          Development/Libraries

%description devel
Header files and static libraries for zlog package.

################################################################################

%prep
%setup -q

%build
REF_DATE=$(LANG=C date -r src/version.h +"%%b %%d %%Y")
REF_TIME=$(LANG=C date -r src/version.h +"%%H:%%M:%%S")

find -name "*.c" -exec \
     sed -i -e "s/__DATE__/\"${REF_DATE}\"/g" -e "s/__TIME__/\"${REF_TIME}\"/g" {} \;

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} PREFIX=%{buildroot}%{_prefix} \
                LIBRARY_PATH=%{_lib64}
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
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root)
%doc README COPYING TODO
%{_includedir}/*
%{_libdir}/lib%{name}.a

################################################################################

%changelog
* Mon Aug 06 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.2.12-0
- Initial build

