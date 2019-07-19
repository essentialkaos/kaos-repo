################################################################################

%ifarch i386
  %define optflags -O2 -g -march=i686
%endif

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
%define __sysctl          %{_bindir}/systemctl

################################################################################

Summary:                  Client library and command line tools for memcached server
Name:                     libmemcached
Version:                  1.0.18
Release:                  1%{?dist}
Group:                    System Environment/Libraries
License:                  BSD
URL:                      http://libmemcached.org

BuildRoot:                %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:                  https://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz

BuildRequires:            make gcc gcc-c++
BuildRequires:            cyrus-sasl-devel flex bison python-sphinx
BuildRequires:            systemtap-sdt-devel

%if 0%{?rhel} >= 7
BuildRequires:            libevent-devel
Requires:                 libevent
%else
BuildRequires:            libevent2-devel
Requires:                 libevent2
%endif

Provides:                 %{name} = %{version}-%{release}

################################################################################

%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key

################################################################################

%package devel

Summary:                  Header files and development libraries for libmemcached
Group:                    Development/Libraries

Requires:                 pkgconfig cyrus-sasl-devel

Requires:                 %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for libmemcached. If you like to develop programs using libmemcached,
you will need to install libmemcached-devel.

################################################################################

%prep
%setup -q

mkdir examples
cp -p tests/*.{cc,h} examples/

%build

%configure \
  --with-memcached=false \
  --enable-sasl \
  --enable-libmemcachedprotocol \
  --enable-memaslap \
  --enable-dtrace \
  --disable-static

%if 0%{?fedora} < 14 && 0%{?rhel} < 7
# for warning: unknown option after '#pragma GCC diagnostic' kind
sed -e 's/-Werror//' -i Makefile
%endif

%install
rm -rf %{buildroot}

%{make_install} AM_INSTALL_PROGRAM_FLAGS=""

if [[ ! -d "%{buildroot}%{_mandir}/man1" ]] ; then
  install -d %{buildroot}%{_mandir}/man1
  install -p -m 644 man/*1 %{buildroot}%{_mandir}/man1
  install -d %{buildroot}%{_mandir}/man3
  install -p -m 644 man/*3 %{buildroot}%{_mandir}/man3
fi

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr (-,root,root,-)
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*
%{_mandir}/man1/mem*

%files devel
%defattr (-,root,root,-)
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*

################################################################################

%changelog
* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.0.18-1
- Rebuilt with the latest version of libevent

* Sat Sep 29 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.18-0
- Initial build for kaos repository
