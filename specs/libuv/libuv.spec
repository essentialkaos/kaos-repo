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

################################################################################

Summary:              Cross-platform asychronous I/O
Name:                 libuv
Version:              1.30.1
Release:              0%{?dist}
License:              MIT, BSD and ISC
Group:                Development/Tools
URL:                  http://libuv.org

Source0:              https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:              %{name}.pc.in

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        autoconf >= 2.59 automake >= 1.9.6
BuildRequires:        gcc libtool >= 1.5.22

Requires(post):       %{__ldconfig}
Requires(postun):     %{__ldconfig}

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
A multi-platform support library with a focus on asynchronous I/O.
It was primarily developed for use by Node.js, but it’s also used by Luvit,
Julia, pyuv, and others.

################################################################################

%package devel
Summary:              Development libraries for libuv
Group:                Development/Tools

Requires:             %{name} = %{version}-%{release}
Requires:             pkgconfig

Requires(post):       %{__ldconfig}
Requires(postun):     %{__ldconfig}

%description devel
Development libraries for libuv.

################################################################################

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

################################################################################

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

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
%{_includedir}/uv/*.h
%{_libdir}/pkgconfig/*.pc

################################################################################

%changelog
* Sun Aug 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.30.1-0
- Updated to the latest stable release

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 1.25.0-0
- Updated to the latest stable release

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.24.0-0
- Updated to the latest stable release

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.23.1-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.23.0-0
- Updated to the latest stable release

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.21.0-0
- Updated to the latest stable release

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.20.3-0
- Updated to the latest stable release

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 1.19.2-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.19.1-0
- Updated to the latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.16.1-0
- Updated to the latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.14.1-0
- Updated to the latest stable release

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.13.1-0
- Updated to the latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-1
- Minor spec improvement

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-0
- Updated to the latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- Updated to the latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- Updated to the latest stable release

* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.1-0
- Initial build
