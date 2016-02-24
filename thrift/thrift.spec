########################################################################################

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

########################################################################################

Summary:         Software framework for cross-language services development
Name:            thrift
Version:         0.9.3
Release:         0%{?dist}
License:         ASL 2.0 / BSD
Group:           Development/Libraries
URL:             http://thrift.apache.org

Source0:         http://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:         https://gitorious.org/pkg-scribe/%{name}-deb-pkg/raw/master:debian/manpage.1.ex

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   automake autoconf libtool gcc gcc-c++ openssl-devel bison

Provides:        %{name} = %{version}-%{release}

########################################################################################

%description

The Apache Thrift software framework for cross-language services
development combines a software stack with a code generation engine to
build services that work efficiently and seamlessly between C++, Java,
Python, %{?php_langname}and other languages.

########################################################################################

%package devel

Summary:         Development files for %{name}

Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description  devel
The thrift-devel package contains libraries and header files for
developing applications that use thrift.

########################################################################################

%package -n erlang-%{name}

Summary:         Erlang support for thrift

Requires:        %{name} = %{version}-%{release}
Requires:        erlang

BuildRequires:   erlang

%description -n erlang-%{name}
The erlang-thrift package contains Erlang bindings for thrift.

########################################################################################

%package -n erlangR15-%{name}

Summary:         ErlangR15 support for thrift

Requires:        %{name} = %{version}-%{release}
Requires:        erlangR15

BuildRequires:   erlang

%description -n erlangR15-%{name}
The erlangR15-thrift package contains ErlangR15 bindings for thrift.

########################################################################################

%package -n erlangR16-%{name}

Summary:         ErlangR16 support for thrift

Requires:        %{name} = %{version}-%{release}
Requires:        erlangR16

BuildRequires:   erlang

%description -n erlangR16-%{name}
The erlangR16-thrift package contains ErlangR16 bindings for thrift.

########################################################################################

%package -n erlang17-%{name}

Summary:         Erlang17 support for thrift

Requires:        %{name} = %{version}-%{release}
Requires:        erlang17

BuildRequires:   erlang

%description -n erlang17-%{name}
The erlang17-thrift package contains Erlang17 bindings for thrift.

########################################################################################

%package -n erlang18-%{name}

Summary:         Erlang18 support for thrift

Requires:        %{name} = %{version}-%{release}
Requires:        erlang18

BuildRequires:   erlang

%description -n erlang18-%{name}
The erlang18-thrift package contains Erlang18 bindings for thrift.

########################################################################################

%prep
%setup -q

%build

export PY_PREFIX=%{_prefix}
export GLIB_LIBS=$(pkg-config --libs glib-2.0)
export GLIB_CFLAGS=$(pkg-config --cflags glib-2.0)
export GOBJECT_LIBS=$(pkg-config --libs gobject-2.0)
export GOBJECT_CFLAGS=$(pkg-config --cflags gobject-2.0)

%configure --disable-dependency-tracking \
           --docdir=%{_docdir}/%{name}-%{version} \
           --disable-static \
           --without-c-glib \
           --without-cpp \
           --without-ruby \
           --without-java \
           --without-lua \
           --without-go

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_mandir}/man1
cp %{SOURCE1} %{buildroot}%{_mandir}/man1/%{name}.1
gzip -9v %{buildroot}%{_mandir}/man1/%{name}.1

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%files -n erlang-%{name}
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_libdir}/erlang/lib/%{name}-%{version}/

%files -n erlangR15-%{name}
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_libdir}/erlang/lib/%{name}-%{version}/

%files -n erlangR16-%{name}
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_libdir}/erlang/lib/%{name}-%{version}/

%files -n erlang17-%{name}
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_libdir}/erlang/lib/%{name}-%{version}/

%files -n erlang18-%{name}
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_libdir}/erlang/lib/%{name}-%{version}/

########################################################################################

%changelog
* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Updated to latest version

* Wed Apr 29 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- Initial build for python and erlang
