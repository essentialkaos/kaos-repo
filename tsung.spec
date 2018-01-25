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
%define __chkconfig       %{_sbin}/chkconfig

################################################################################

Name:              tsung
Summary:           A distributed multi-protocol load testing tool
Version:           1.7.0
Release:           0%{?dist}
Group:             Development/Tools
License:           GPLv2
URL:               http://tsung.erlang-projects.org

Source:            http://tsung.erlang-projects.org/dist/%{name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     erlang make

Requires:          erlang perl(Template)

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
tsung is a distributed load testing tool. It is protocol-independent and can 
currently be used to stress and benchmark HTTP, Jabber/XMPP, PostgreSQL, 
MySQL and LDAP servers.
It simulates user behaviour using an XML description file, reports many 
measurements in real time (statistics can be customized with transactions, 
and graphics generated using gnuplot).
For HTTP, it supports 1.0 and 1.1, has a proxy mode to record sessions, 
supports GET and POST methods, Cookies, and Basic WWW-authentication. 
It also has support for SSL.

################################################################################

%prep
%setup -q
iconv -f ISO-8859-1 -t UTF-8 CONTRIBUTORS > CONTRIBUTORS.new && \
touch -r CONTRIBUTORS CONTRIBUTORS.new && \
mv CONTRIBUTORS.new CONTRIBUTORS
sed -i 's/\r$//' examples/*

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_defaultdocdir}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING TODO
%{_bindir}/%{name}*
%{_bindir}/tsplot
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/tsplot.1*

################################################################################

%changelog
* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to latest stable release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to latest stable release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-1
- Updated group in spec

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Updated to latest stable release

* Wed Oct 30 2013 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-5
- Initial build
