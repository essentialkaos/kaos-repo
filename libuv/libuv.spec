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

Summary:              Cross-platform asychronous I/O 
Name:                 libuv
Version:              1.9.1
Release:              0%{?dist}
License:              MIT, BSD and ISC
Group:                Development/Tools
URL:                  http://http://libuv.org

Source0:              https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:              %{name}.pc.in

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        autoconf >= 2.59 automake >= 1.9.6
BuildRequires:        gcc libtool >= 1.5.22

Requires(post):       %{__ldconfig}
Requires(postun):     %{__ldconfig}

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
A multi-platform support library with a focus on asynchronous I/O. 
It was primarily developed for use by Node.js, but it’s also used by Luvit, 
Julia, pyuv, and others.

###############################################################################

%package devel
Summary:              Development libraries for libuv
Group:                Development/Tools

Requires:             %{name} = %{version}-%{release}
Requires:             pkgconfig

Requires(post):       %{__ldconfig}
Requires(postun):     %{__ldconfig}

%description devel
Development libraries for libuv.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'

./autogen.sh

%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_pkgconfigdir}

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}%{_pkgconfigdir}/libuv.pc

%clean
rm -rf %{buildroot}

###############################################################################

%post
%{__ldconfig}

%postun
%{__ldconfig}

###############################################################################

%files
%defattr(-,root,root)
%doc README.md AUTHORS LICENSE
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md AUTHORS LICENSE
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.1-0
- Initial build
