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

%define short_name    cpp-driver

###############################################################################

Summary:              DataStax C/C++ Driver for Apache Cassandra
Name:                 cassandra-%{short_name}
Version:              2.5.0
Release:              0%{?dist}
License:              APLv2.0
Group:                Development/Libraries
URL:                  http://datastax.github.io/cpp-driver

Source0:              https://github.com/datastax/%{short_name}/archive/%{version}.tar.gz
Source1:              cassandra.pc.in
Source2:              cassandra_static.pc.in

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        cmake >= 2.6.4 libuv-devel >= 1.9.1
BuildRequires:        automake gcc-c++ openssl-devel

Requires(post):       %{__ldconfig}
Requires(postun):     %{__ldconfig}

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra using exclusively Cassandra's native protocol and Cassandra Query
Language.

###############################################################################

%package devel
Summary:              Development libraries for ${name}
Group:                Development/Tools

Requires:             %{name} = %{version}-%{release}
Requires:             libuv >= 1.9.1
Requires:             pkgconfig

%description devel
Development libraries for %{name}.

###############################################################################

%prep
%setup -qn %{short_name}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'

cmake -DCMAKE_BUILD_TYPE=RELEASE \
      -DCASS_BUILD_STATIC=ON \
      -DCASS_INSTALL_PKG_CONFIG=OFF \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} .

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
    %SOURCE1 > %{buildroot}%{_pkgconfigdir}/cassandra.pc

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}%{_pkgconfigdir}/cassandra_static.pc

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
%doc README.md LICENSE.txt
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest stable release

* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.4.3-0
- Initial build
