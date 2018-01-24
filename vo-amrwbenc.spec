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
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __ldconfig        %{_sbin}/ldconfig
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

Summary:            VisualOn AMR-WB encoder library
Name:               vo-amrwbenc
Version:            0.1.3
Release:            2%{?dist}
Group:              System Environment/Libraries
License:            ASL 2.0
URL:                http://opencore-amr.sourceforge.net

Source0:            http://downloads.sourceforge.net/opencore-amr/%{name}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
This library contains an encoder implementation of the Adaptive
Multi Rate Wideband (AMR-WB) audio codec. The library is based
on a codec implementation by VisualOn as part of the Stagefright
framework from the Google Android project.

###############################################################################

%package devel
Summary:            Development files for vo-amrwbenc
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
The vo-amrwbenc devel package contains libraries and header files for
developing applications that use vo-amrwbenc.

###############################################################################

%prep
%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/lib%{name}.la

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README NOTICE
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

###############################################################################

%changelog
* Thu Jan 25 2018 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-2
- Initial build for kaos repo
