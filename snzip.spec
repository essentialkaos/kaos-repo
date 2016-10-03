###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _docdir           %{_datadir}/doc
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

###############################################################################

Summary:              A fast data comprssion utility using google snappy
Name:                 snzip
Version:              1.0.3
Release:              0%{?dist}
License:              2-clause BSD-style license 
Group:                Applications/System
URL:                  https://github.com/kubo/snzip

Source0:              https://github.com/kubo/%{name}/archive/%{version}.tar.gz

Patch0:               %{name}-%{version}-autoconf.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc make snappy-devel autoconf268

Requires:             snappy

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
Snzip is a compress/decompress command line utility using snappy.
This supports five type of file formats; framing-format, old framing-format,
snzip format, snappy-java format and snappy-in-java format.
The default format is framing-format.

###############################################################################

%prep
%setup -q

%build
./autogen.sh
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{make_install} DESTDIR=%{buildroot} INSTALLDIRS=vendor

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/INSTALL
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README.md

###############################################################################

%changelog
* Mon Oct 03 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.0.3-0
- Initial build.
