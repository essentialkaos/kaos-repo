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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent

###############################################################################

%define service_user         %{name}
%define service_group        %{name}
%define service_name         %{name}

###############################################################################

Summary:              Very fast HTTP server written in C
Name:                 h2o
Version:              1.4.4
Release:              0%{?dist}
License:              Copyright (c) 2014 DeNA Co., Ltd.
Group:                System Environment/Daemons
Vendor:               DeNA Co., Ltd. / ESSENTIALKAOS
URL:                  https://github.com/h2o/h2o

Source0:              https://github.com/h2o/%{name}/archive/v%{version}.tar.gz
Source1:              %{name}.logrotate
Source2:              %{name}.init
Source3:              %{name}.sysconfig
Source4:              %{name}.conf

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             libyaml kaosv >= 2.6

BuildRequires:        make gcc gcc-c++ cmake openssl-devel libyaml-devel

Requires(pre):        shadow-utils
Requires(post):       chkconfig

###############################################################################

%description
H2O is a very fast HTTP server written in C. It can also be used as a library.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%build
cmake -DWITH_BUNDLED_SSL=on -DCMAKE_INSTALL_PREFIX=%{_prefix} .

%{__make} %{?_smp_mflags}

%{make_install}

%install
%{__rm} -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}

install -pm 755 %{name} \
                %{buildroot}%{_bindir}/%{name}

install -pm 644 examples/doc_root/index.html \
                %{buildroot}%{_loc_datarootdir}/%{name}/

install -pm 644 %{SOURCE1} \
                %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -pm 755 %{SOURCE2} \
                %{buildroot}%{_initrddir}/%{service_name}

install -pm 644 %{SOURCE3} \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -pm 644 %{SOURCE4} \
                %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

###############################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || useradd -r -g %{service_group} -s /sbin/nologin %{service_user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add %{name}

  if [[ -d %{_logdir}/%{name} ]] ; then
    if [[ ! -e %{_logdir}/%{name}/access.log ]]; then
      touch %{_logdir}/%{name}/access.log
      %{__chmod} 640 %{_logdir}/%{name}/access.log
      %{__chown} %{service_user}: %{_logdir}/%{name}/access.log
    fi

    if [[ ! -e %{_logdir}/%{name}/error.log ]] ; then
      touch %{_logdir}/%{name}/error.log
      %{__chmod} 640 %{_logdir}/%{name}/error.log
      %{__chown} %{service_user}: %{_logdir}/%{name}/error.log
    fi
  fi
fi

###############################################################################

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop > /dev/null 2>&1
  %{__chkconfig} --del %{service_name}
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc Changes LICENSE README.md

%dir %{_logdir}/%{name}

%{_bindir}/%{name}

%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%{_initrddir}/%{service_name}

%{_loc_datarootdir}/%{name}/*

###############################################################################

%changelog
* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- [misc] fix install error of libh2o-evloop in case development files of 
  OpenSSL cannot be found #443 (Kazuho Oku)
- [fastcgi] change ownership of domain socket when `fastcgi.spawn` command 
  is used #433 (Masaki TAGAWA)
- [fastcgi] kill fastcgi processes spawned by `fastcgi.spawn` command when 
  standalone server receives SIGINT #444 (Kazuho Oku)
- [file] fix file descriptor leak on multi-range request #434 (Justin Zhu)
- [ssl] update libressl to 2.2.2 #440 (Kazuho Oku)
- [misc] fix build error in case development files of OpenSSL cannot 
  be found #433 (Kazuho Oku)

* Tue Aug 11 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-1
- Some fixes in spec and init script

* Mon Aug 10 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- [fastcgi] do not concatenate the headers (ex. Set-Cookie) sent by a 
  FastCGI app #427 (Kazuho Oku)
- [ssl] for guarding session ticket secret use writer-preferred locks on 
  Linux as well #423 (Kazuho Oku)
- [misc] suppress compiler warnings #415 (Syohei YOSHIDA)

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- [core] do not refuse to start-up when failing to enable TCP Fast Open 
  #368 (Kazuho Oku)
- [fastcgi] fix server start-up issues when using fastcgi.spawn #367 
  (Kazuho Oku)
- [SSL] support OCSP stapling using openssl ocsp command built from 
  LibreSSL in addition to OpenSSL #366 (Tatsuhiro Tsujikawa)
- [core] enable TCP fast-open #356 (Tatsuhiko Kubo)
- [core] improve virtual-host lookup logic #293 #296 (Kazuho Oku)
- [core] fix content being mis-sent for HEAD requests #300 #302 (Kazuho Oku)
- [doc] bundle documents #292 (Kazuho Oku)
- [fastcgi] add FastCGI support #346 #359 #360 #364 (Kazuho Oku)
- [file] support for If-Range requests #345 (Justin Zhu)
- [file] send 503 (not 403) in case if too many files are open #304 (Kazuho Oku)
- [http2] add http2-reprioritize-blocking-assets directive to optimize 
  first-paint time on Chrome #349 (Kazuho Oku)
- [http2] fix incompliant behavior when the number of stream exceeds the 
  negotiated maximum #341 #352 (Kazuho Oku)
- [proxy] fix potential use-after-free issue in case upstream name is resolved 
  using getaddrinfo #307 (Kazuho Oku)
- [proxy] increase default I/O timeout from 5 to 30 seconds fb5c016 (Kazuho Oku)
- [redirect] support internal redirect #364 (Kazuho Oku)
- [SSL] fix assertion failure during handshake #316 (Kazuho Oku)
- [SSL] fix assertion failure when receiving a corrupt TLS record 
  (http2 only) #297 (Kazuho Oku)
- [SSL] fix build error on OpenSUSE using libressl #337 (Kazuho Oku)
- [SSL] select ALPN protocol based on server-side preference #335 (Justin Zhu)
- [libh2o] build shared libraries as well #324 (pyos)
- [libh2o] build libh2o-evloop #327 (Laurentiu Nicola)
- [misc] emit stacktrace in case of fatal error (Linux only) #331 (Kazuho Oku)
- [misc] improve NetBSD compatibility #289 (Kazuho Oku)
- [misc] fix file descriptor leaks #336 (Kazuho Oku)

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- [core] bundle libyaml #248 (Kazuho Oku)
- [core] implement master-worker process mode and daemon mode 
  (bundles Server::Starter) #258 #270 (Kazuho Oku)
- [file] more mime-types by default #250 #254 #280 (Tatsuhiko Kubo, 
    George Liu, Kazuho Oku)
- [file][http1] fix connection being closed if the length of content 
  is zero #276 (Kazuho Oku)
- [headers] fix heap overrun during configuration #251 (Kazuho Oku)
- [http2] do not delay sending PUSH_PROMISE #221 (Kazuho Oku)
- [http2] reduce memory footprint under high load #271 (Kazuho Oku)
- [http2] fix incorrect error sent when number of streams exceed the 
  limit #268 (Kazuho Oku)
- [proxy] fix heap overrun when building request sent to upstream 
  #266 #269 (Moto Ishizawa, Kazuho Oku)
- [proxy] fix laggy response in case the length of content is zero 
  #274 #276 (Kazuho Oku)
- [SSL] fix potential stall while reading data from client #268 (Kazuho Oku)
- [SSL] bundle LibreSSL #236 #272 (Kazuho Oku)
- [SSL] obtain source-level compatibility with BoringSSL #228 (Kazuho Oku)
- [SSL] add directive listen.ssl.cipher-preference for controlling 
  the selection logic of cipher-suites #233 (Kazuho Oku)
- [SSL] disable TLS compression #252 (bisho)
- [libh2o] fix C++ compatibility (do not use empty struct) #225 (Kazuho Oku)
- [libh2o] search external dependencies using pkg-config #227 (Kazuho Oku)
- [misc] fix GCC version detection bug used for controlling compiler 
  warnings #224 (Kazuho Oku)
- [misc] check merory allocation failures in socket pool #265 (Tatsuhiko Kubo)

* Tue Mar 03 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- [core] change backlog size from 65,536 to 65,535 #183 (Tatsuhiko Kubo)
- [http2] fix assertion failure in HPACK encoder #186 (Kazuho Oku)
- [http2] add extern to some global variables that were not marked as 
  such #178 (Kazuho Oku)
- [proxy] close persistent upstream connection if client abruptly closes 
  the stream #188 (Kazuho Oku)
- [proxy] fix internal state corruption in case upstream sends response 
  headers divided into multiple packets #189 (Kazuho Oku)
- [SSL] add host header to OCSP request #176 (Masaaki Hirose)
- [libh2o] do not require header files under deps/ when using 
  libh2o #173 (Kazuho Oku)
- [libh2o] fix compile error in examples when compiled with 
  H2O_USE_LIBUV=0 #177 (Kazuho Oku)
- [libh2o] in example, add missing / after the reference 
  path #180 (Matthieu Garrigues)
- [misc] fix invalid HTML in sample page #175 (Deepak Prakash)

* Tue Mar 03 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- [core] add redirect handler #150 (Kazuho Oku)
- [core] add pid-file directive for specifying the pid file #164 (Kazuho Oku)
- [core] connections accepted by host-specific listeners should not be handled 
  by handlers of other hosts #163 (Kazuho Oku)
- [core] (FreeBSD) fix a bug that prevented the standalone server from booting 
  when run as root #160 (Kazuho Oku)
- [core] switch to pipe-based interthread messaging #154 (Kazuho Oku)
- [core] use kqueue on all BSDs #156 (Kazuho Oku)
- [access-log] more logging directives #158 (Kazuho Oku)
- [access-log] bugfix: header values were not logged when specified using 
  uppercase letters #157 (Kazuho Oku)
- [file] add application/json to defalt MIME-types #159 (Tatsuhiko Kubo)
- [http2] add support for the finalized version of HTTP/2 #166 (Kazuho Oku)
- [http2] fix issues reported by h2spec v0.0.6 #165 (Kazuho Oku)
- [proxy] merge the cookie headers before sending to upstream #161 (Kazuho Oku)
- [proxy] simplify the configuration directives (and make persistent upstream 
  connections as default) #162 (Kazuho Oku)
- [SSL] add configuration directive to preload DH params #148 (Jeff Marrison)
- [libh2o] separate versioning scheme using H2O_LIBRARY_VERSION_* #167 (Kazuho Oku)

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- added configuration directives: ssl/cipher-suite, ssl/ocsp-update-interval, 
  ssl/ocsp-max-failures, expires, file.send-gzip
- [http2] added support for draft-16 (draft-14 is also supported)
- [http2] dependency-based prioritization
- [http2] improved conformance to the specification
- [SSL] OCSP stapling (automatically enabled by default)
- [SSL] fix compile error with OpenSSL below version 1.0.1
- [file] content negotiation (serving .gz files)
- [expires] added support for Cache-Control: max-age
- [libh2o] libh2o and the header files installed by make install
- [libh2o] fix compile error when used from C++
- automatically setuids to nobody when run as root and if user directive is not set
- automatically raises RLIMIT_NOFILE
- uses all CPU cores by default
- now compiles on NetBSD and other BSD-based systems

* Mon Dec 29 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.0-0
- Initial build
