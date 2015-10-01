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

Summary:         Userspace library for packets that have been queued by the kernel packet filter
Name:            libnetfilter_queue
Version:         1.0.2
Release:         0%{?dist}
License:         GPLv2
Group:           System Environment/Libraries
URL:             http://netfilter.org

Source0:         http://ftp.netfilter.org/pub/%{name}/%{name}-%{version}.tar.bz2

Patch1:          rhel6-iptos.diff

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc libmnl-devel >= 1.0.3 libnfnetlink-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
libnetfilter_queue is a userspace library providing an API to packets
that have been queued by the kernel packet filter. It is is part of a
system that deprecates the old ip_queue / libipq mechanism.

libnetfilter_queue has been previously known as libnfnetlink_queue.

################################################################################

%package devel
Requires:       %{name} = %{version}
Requires:       libnfnetlink-devel
Summary:        Header files and static libraries for libnetfilter_queue package
Group:          Development/Libraries

%description devel
Header files and static libraries for libnetfilter_queue package.

################################################################################

%prep
%setup -q
%patch1 -p1

# Update headers for compatibility with libnfnetlink 1.0
sed -i 's/linux_nfnetlink.h/libnfnetlink.h/' include/libnetfilter_queue/linux_nfnetlink_queue.h
sed -i 's/linux_nfnetlink.h/libnfnetlink.h/' include/linux/netfilter/nfnetlink_queue.h

%build
%configure --disable-static
%{__make} %{?_smp_mflags} KERNELDIR="ignore"

%install
rm -rf %{buildroot}

%{make_install} KERNELDIR="ignore"
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.1*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Fri Oct 10 2014 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Initial build
