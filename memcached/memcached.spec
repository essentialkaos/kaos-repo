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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

%define username          memcached
%define groupname         memcached

###############################################################################

Summary:                  High Performance, Distributed Memory Object Cache
Name:                     memcached
Version:                  1.4.33
Release:                  0%{?dist}
Group:                    System Environment/Daemons
License:                  BSD
URL:                      http://memcached.org

Source0:                  https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
Source1:                  %{name}.init
Source2:                  %{name}.sysconf

BuildRoot:                %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:            gcc automake libevent-devel

Requires:                 initscripts libevent kaosv >= 1.5.0

Requires(pre):            shadow-utils
Requires(post):           %{__chkconfig}
Requires(preun):          %{__chkconfig} %{__service}
Requires(postun):         %{__service}

###############################################################################

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

###############################################################################

%package devel
Summary:                  Files needed for development using memcached protocol
Group:                    Development/Libraries 
Requires:                 %{name} = %{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require access to the
memcached binary include files.

###############################################################################

%package debug
Summary:                  Debug version of memcached
Group:                    System Environment/Daemons
Requires:                 %{name} = %{version}-%{release}

%description debug
Version of memcached show more additional information for debugging.

###############################################################################

%prep

%setup -q
./autogen.sh

%ifarch i386
  %define optflags -O2 -g -march=i686
%endif

%configure
sed -i 's/-Werror/ /' Makefile
sed -i "s/UNKNOWN/%{version}/" version.m4

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install} INSTALL="install -p"

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -pm 755 %{name}-debug %{buildroot}%{_bindir}/%{name}-debug
install -pm 755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool

touch %{buildroot}%{_logdir}/%{name}/%{name}.log

%clean 
%{__rm} -rf %{buildroot}

###############################################################################

%pre
%{__getent} group %{groupname} >/dev/null || %{__groupadd} -r %{groupname}
%{__getent} passwd %{username} >/dev/null || %{__useradd} -r -g %{groupname} -d %{_rundir}/%{name} -s /sbin/nologin %{username}

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{name}
fi

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(755,%{username},%{groupname}) %{_rundir}/%{name}

%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_initrddir}/%{name}

%dir %attr(755,%{username},%{groupname}) %{_logdir}/%{name}
%attr(644,%{username},%{groupname}) %{_logdir}/%{name}/%{name}.log

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/*

%files debug
%defattr(-,root,root,0755)
%{_bindir}/%{name}-debug

###############################################################################

%changelog
* Wed Nov 02 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.33-0
- Updated to latest release

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.32-0
- Updated to latest release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.4.31-0
- Updated to latest release

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.25-0
- Updated to latest release

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.24-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.22-0
- Updated to latest release

* Tue Oct 28 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.20-2
- Init script migrated to kaosv2

* Wed Jun 04 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.20-1
- Some minor fixes

* Wed Jun 04 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.20-0
- Initial build
