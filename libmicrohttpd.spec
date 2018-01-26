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

################################################################################

Summary:         Lightweight library for embedding a webserver in applications
Name:            libmicrohttpd
Version:         0.9.55
Release:         0%{?dist}
License:         GNU LGPL
Group:           Development/Libraries
URL:             http://www.gnu.org/software/libmicrohttpd/

Source0:         http://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   autoconf automake libtool gnutls-devel libgcrypt-devel
BuildRequires:   libcurl-devel graphviz doxygen

Requires(post):  info
Requires(preun): info

################################################################################

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.
Key features that distinguish libmicrohttpd from other projects are:

* C library: fast and small
* API is simple, expressive and fully reentrant
* Implementation is http 1.1 compliant
* HTTP server can listen on multiple ports
* Support for IPv6
* Support for incremental processing of POST data
* Creates binary of only 25k (for now)
* Three different threading models

################################################################################

%package devel
Summary:         Development files for libmicrohttpd
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

%description devel
Development files for libmicrohttpd

################################################################################

%package doc
Summary:         Documentation for libmicrohttpd
Group:           Documentation
Requires:        %{name} = %{version}-%{release}

%description doc
Doxygen documentation for libmicrohttpd and some example source code

################################################################################

%prep
%setup -q

%build
# Required because patches modify .am files
# autoreconf --force
%configure --disable-static --with-gnutls

%{__make} %{?_smp_mflags}

pushd doc/doxygen/
doxygen %{name}.doxy
popd

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_bindir}

# Install some examples in /usr/share/doc/libmicrohttpd-${version}/examples
mkdir -p examples
install -m 644 src/examples/*.c examples

# Install the doxygen documentation in /usr/share/doc/libmicrohttpd-${version}/html
cp -R doc/doxygen/html html

%clean
rm -rf %{buildroot}

%post doc
%{_sbin}/install-info %{_infodir}/microhttpd.info.gz %{_infodir}/dir || :
%{_sbin}/install-info %{_infodir}/microhttpd-tutorial.info.gz %{_infodir}/dir || :

%preun doc
if [[ $1 -eq 0 ]] ; then
  %{_sbin}/install-info --delete %{_infodir}/microhttpd.info.gz %{_infodir}/dir || :
  %{_sbin}/install-info --delete %{_infodir}/microhttpd-tutorial.info.gz %{_infodir}/dir || :
fi

%post
%{_sbin}/ldconfig

%postun
%{_sbin}/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/microhttpd.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man3/%{name}.3.gz
%{_infodir}/%{name}.info.gz
%{_infodir}/%{name}-tutorial.info.gz
%doc AUTHORS README ChangeLog
%doc examples
%doc html

################################################################################

%changelog
* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.55-0
- Updated to latest release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.54-0
- Updated to latest release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.52-0
- Updated to latest release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.51-0
- Updated to latest release

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.49-0
- Updated to latest release

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.48-0
- Updated to latest release

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.46-0
- Updated to latest release

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.43-0
- Updated to latest release

* Thu Jul 02 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.42-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.40-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.39-0
- Updated to latest release

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.38-0
- Updated to latest release

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.37-0
- Updated to latest release

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.36-0
- Updated to latest release

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.35-0
- Updated to latest release

* Thu Mar 06 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.34-0
- Updated to latest release

* Wed Nov 20 2013 Anton Novojilov <andy@essentialkaos.com> - 0.9.31-0
- Updated to latest release

* Sun Jul 28 2013 Anton Novojilov <andy@essentialkaos.com> - 0.9.28-0
- Updated to latest release

* Thu Apr 11 2013 Anton Novojilov <andy@essentialkaos.com> - 0.9.26-0
- Updated to latest release

* Fri Jun 8 2012 Anton Novojilov <andy@essentialkaos.com> - 0.9.20-0
- Updated to latest release

* Thu Apr 12 2012 Anton Novojilov <andy@essentialkaos.com> - 0.9.19-0
- Updated to latest release
