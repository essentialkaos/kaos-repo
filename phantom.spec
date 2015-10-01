###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
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

###############################################################################

%define __mainver         0.14.0
%define __mainrel         0

###############################################################################

Summary:            I/O engine with some modules
Name:               phantom
Version:            %{__mainver}
Release:            %{__mainrel}%{?dist}
License:            GPLv2
Group:              Applications/Internet
URL:                https://github.com/mamchits/phantom/
Vendor:             Yandex

Source0:            %{name}-%{version}.tar.bz2

BuildArch:          i386 x86_64
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           perl glibc openssl binutils

BuildRequires:      glibc-devel gcc-c++ perl openssl-devel binutils-devel

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description
I/O engine with some modules

###############################################################################

%package devel
Summary:            Phantom development library
Requires:           glibc-devel gcc-c++ 
Requires:           %{name} => %{version}-%{release}

%description devel
Phantom development library

###############################################################################

%package ssl
Summary:            OpenSSL dependent modules for phantom
Requires:           openssl-devel
Requires:           %{name} => %{version}-%{release}

%description ssl
OpenSSL dependent modules for phantom

###############################################################################

%package debug
Summary:            libbfd dependent modules for phantom
Requires:           %{name} => %{version}-%{release}

%description debug
libbfd dependent modules for phantom

###############################################################################

%package ssl-devel
Summary:            Phantom development library (ssl part)
Requires:           openssl-devel
Requires:           %{name} => %{version}-%{release}
Requires:           %{name}-ssl => %{version}-%{release}

%description ssl-devel
Phantom development library (ssl part)

###############################################################################

%package debug-devel
Summary:            libbfd dependent modules for phantom
Requires:           %{name} => %{version}-%{release}

%description debug-devel
Phantom development library (debug part)

###############################################################################

%prep
%setup -q

%build

%{__make} -R %{?_smp_mflags}

%install
rm -rf %{buildroot}

# Main package

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_libdir}
install -dm 755 %{buildroot}%{_docdir}
install -dm 755 %{buildroot}%{_libdir}/%{name}

install -pm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -pm 755 lib/%{name}/*.so %{buildroot}%{_libdir}/%{name}/

# Devel package

install -dm 755 %{buildroot}%{_includedir}
install -dm 755 %{buildroot}%{_includedir}/pd
install -dm 755 %{buildroot}%{_includedir}/pd/base
install -dm 755 %{buildroot}%{_includedir}/pd/bq
install -dm 755 %{buildroot}%{_includedir}/pd/fixinclude
install -dm 755 %{buildroot}%{_includedir}/pd/http
install -dm 755 %{buildroot}%{_includedir}/%{name}
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_benchmark
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_benchmark/method_stream
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_client
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_client/proto_fcgi
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_client/proto_none
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_stream
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_stream/proto_http
install -dm 755 %{buildroot}%{_includedir}/%{name}/io_stream/proto_http/handler_static
install -dm 755 %{buildroot}%{_datarootdir}/%{name}

install -pm 644 lib/*.a %{buildroot}%{_libdir}/
install -pm 644 pd/base/*.H %{buildroot}%{_includedir}/pd/base/
install -pm 644 pd/bq/*.H %{buildroot}%{_includedir}/pd/bq/
install -pm 644 pd/fixinclude/*.h %{buildroot}%{_includedir}/pd/fixinclude/
install -pm 644 pd/http/*.H %{buildroot}%{_includedir}/pd/http/
install -pm 644 pd/http/*.H %{buildroot}%{_includedir}/pd/http/
install -pm 644 %{name}/*.H %{buildroot}%{_includedir}/%{name}/
install -pm 644 %{name}/io_benchmark/*.H %{buildroot}%{_includedir}/%{name}/io_benchmark/
install -pm 644 %{name}/io_benchmark/method_stream/*.H %{buildroot}%{_includedir}/%{name}/io_benchmark/method_stream/
install -pm 644 %{name}/io_client/*.H %{buildroot}%{_includedir}/%{name}/io_client/
install -pm 644 %{name}/io_client/proto_fcgi/*.H %{buildroot}%{_includedir}/%{name}/io_client/proto_fcgi/
install -pm 644 %{name}/io_client/proto_none/*.H %{buildroot}%{_includedir}/%{name}/io_client/proto_none/
install -pm 644 %{name}/io_stream/*.H %{buildroot}%{_includedir}/%{name}/io_stream/
install -pm 644 %{name}/io_stream/proto_http/*.H %{buildroot}%{_includedir}/%{name}/io_stream/proto_http/
install -pm 644 %{name}/io_stream/proto_http/handler_static/*.H %{buildroot}%{_includedir}/%{name}/io_stream/proto_http/handler_static/

install -pm 644 %{name}/module.mk %{buildroot}%{_datarootdir}/%{name}/
install -pm 644 opts.mk %{buildroot}%{_datarootdir}/%{name}/
install -pm 644 test/test.mk %{buildroot}%{_datarootdir}/%{name}/
install -pm 644 pd/library.mk %{buildroot}%{_datarootdir}/%{name}/
install -pm 644 debian/package.mk %{buildroot}%{_datarootdir}/%{name}/

install -dm 755 %{buildroot}%{_includedir}/pd/debug
install -pm 644 pd/debug/*.H %{buildroot}%{_includedir}/pd/debug/

install -dm 755 %{buildroot}%{_includedir}/pd/ssl
install -dm 755 %{buildroot}%{_includedir}/%{name}/ssl
install -pm 644 pd/ssl/*.H %{buildroot}%{_includedir}/pd/ssl/
install -pm 644 %{name}/ssl/*.H %{buildroot}%{_includedir}/%{name}/ssl/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post ssl -p /sbin/ldconfig

%postun ssl -p /sbin/ldconfig

%post debug -p /sbin/ldconfig

%postun debug -p /sbin/ldconfig

## Files #######################################################################

%files
%defattr(-, root, root, -)
%doc COPYING AUTHORS README.ru
%{_bindir}/%{name}
%{_libdir}/%{name}/mod_io_client.so
%{_libdir}/%{name}/mod_io_client_ipv4.so
%{_libdir}/%{name}/mod_io_client_ipv6.so
%{_libdir}/%{name}/mod_io_client_local.so
%{_libdir}/%{name}/mod_io_client_proto_none.so
%{_libdir}/%{name}/mod_io_client_proto_fcgi.so
%{_libdir}/%{name}/mod_io_stream.so
%{_libdir}/%{name}/mod_io_stream_ipv4.so
%{_libdir}/%{name}/mod_io_stream_ipv6.so
%{_libdir}/%{name}/mod_io_stream_proto_monitor.so
%{_libdir}/%{name}/mod_io_stream_proto_echo.so
%{_libdir}/%{name}/mod_io_stream_proto_http.so
%{_libdir}/%{name}/mod_io_stream_proto_http_handler_null.so
%{_libdir}/%{name}/mod_io_stream_proto_http_handler_static.so
%{_libdir}/%{name}/mod_io_stream_proto_http_handler_proxy.so
%{_libdir}/%{name}/mod_io_stream_proto_http_handler_fcgi.so
%{_libdir}/%{name}/mod_io_benchmark.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_ipv4.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_ipv6.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_local.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_proto_none.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_proto_http.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_source_random.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_source_log.so

%files devel
%defattr(-, root, root, -)
%{_libdir}/libpd-base.a
%{_libdir}/libpd-base.s.a
%{_libdir}/libpd-bq.a
%{_libdir}/libpd-bq.s.a
%{_libdir}/libpd-http.a
%{_libdir}/libpd-http.s.a
%{_includedir}/pd/base/*
%{_includedir}/pd/bq/*
%{_includedir}/pd/http/*
%{_includedir}/pd/fixinclude/*
%{_includedir}/%{name}/*
%{_datarootdir}/%{name}/*

%files ssl
%defattr(-, root, root, -)
%{_libdir}/%{name}/mod_ssl.so
%{_libdir}/%{name}/mod_io_stream_transport_ssl.so
%{_libdir}/%{name}/mod_io_benchmark_method_stream_transport_ssl.so

%files ssl-devel
%defattr(-, root, root, -)
%{_libdir}/libpd-ssl.a
%{_libdir}/libpd-ssl.s.a
%{_includedir}/pd/ssl/*
%{_includedir}/%{name}/ssl/*

%files debug
%defattr(-, root, root, -)
%{_libdir}/%{name}/mod_debug.so

%files debug-devel
%defattr(-, root, root, -)
%{_libdir}/libpd-debug.a
%{_libdir}/libpd-debug.s.a
%{_includedir}/pd/debug/*

###############################################################################

%changelog
* Thu Jun 27 2013 Anton Novojilov <andy@essentialkaos.com> - 0.14.0-0
- Created spec based on debian scripts from github repo