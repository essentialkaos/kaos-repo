###############################################################################

# rpmbuilder:svn          http://svn.code.sf.net/p/xavs/code/trunk
# rpmbuilder:revision     r46

###############################################################################

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

###############################################################################

Summary:            Audio Video Standard of China
Name:               xavs
Version:            0.1.51
Release:            0%{?dist}
License:            GPL
Group:              System Environment/Libraries
URL:                http://xavs.sourceforge.net/

Source0:            %{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc-c++ make

###############################################################################

%description
AVS is the Audio Video Standard of China. This project aims to
implement high quality AVS encoder and decoder.

###############################################################################

%package devel
Summary:            Header files and static libraries for xavs
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
These are the header files and static libraries from xavs that are needed
to build programs that use it.

###############################################################################

%prep
%setup -q

%build
export CFLAGS="%{optflags} -fPIC"
%configure \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --enable-pic \
  --enable-shared

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

###############################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/xavs
%{_libdir}/lib%{name}.so.*
%{_pkgconfigdir}/%{name}.pc

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so

###############################################################################

%changelog
* Sun Apr 24 2016 Gleb Goncharov <yum@gongled.ru> - 0.1.51-0
- Initial build.

