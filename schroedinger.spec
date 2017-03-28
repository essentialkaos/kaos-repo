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

Summary:            Portable libraries for the high quality Dirac video codec
Name:               schroedinger
Version:            1.0.11
Release:            2%{?dist}
Group:              System Environment/Libraries
License:            LGPL
URL:                http://www.diracvideo.org

Source0:            http://www.diracvideo.org/download/%{name}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make libtool 
BuildRequires:      orc-devel >= 0.4.10 glew-devel >= 1.5.1

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
The Schrödinger project will implement portable libraries for the high
quality Dirac video codec created by BBC Research and Development. 
Dirac is a free and open source codec producing very high image quality video.

The Schrödinger project is a project done by BBC R&D and Fluendo in
order to create a set of high quality decoder and encoder libraries
for the Dirac video codec.

###############################################################################

%package devel
Summary:            Development files for schroedinger
Group:              Development/Libraries

Requires:           orc-devel >= 0.4.10
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for schroedinger.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static

sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING* NEWS TODO
%{_libdir}/lib%{name}-*.so.*

###############################################################################

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-*
%{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/%{name}-*.pc

###############################################################################

%changelog
* Wed Jan 25 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-2
- Minor improvements

* Thu Nov 24 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-1
- Fixed dependencies for devel package

* Wed Apr 20 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.11-0
- Updated to latest stable release
