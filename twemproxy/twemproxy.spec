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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig

%define alias_name        nutcracker

################################################################################

Summary:           Fast and lightweight proxy for memcached and redis protocol
Name:              twemproxy
Version:           0.4.1
Release:           1%{?dist}
License:           Apache 2.0
Group:             Applications/Internet
URL:               https://github.com/twitter/twemproxy

Source0:           https://github.com/twitter/%{name}/archive/v%{version}.tar.gz
Source1:           %{name}.init
Source2:           %{name}.sysconfig

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          libevent2 kaosv >= 2.0
BuildRequires:     make gcc autoconf m4 libtool libevent2-devel

Provides:          %{name} = %{version}-%{release}
Provides:          %{alias_name} = %{version}-%{release}

################################################################################

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and 
lightweight proxy for memcached and redis protocol. It was primarily built to 
reduce the connection count on the backend caching servers.

################################################################################

%prep
%setup -qn %{name}-%{version}
sed -i 's/2.64/2.63/g' configure.ac
autoreconf -fvi

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install} PREFIX=%{buildroot} mandir=%{_mandir}


install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 644 conf/%{alias_name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

mv %{buildroot}%{_sbindir}/%{alias_name} %{buildroot}%{_sbindir}/%{name}
mv %{buildroot}%{_mandir}/man8/%{alias_name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

ln -sf %{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{alias_name}
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_sysconfdir}/%{alias_name}
ln -sf %{_initrddir}/%{name} %{buildroot}%{_initrddir}/%{alias_name}
ln -sf %{_sysconfdir}/%{name}/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{alias_name}.yml

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]]; then
 %{__service} %{name} stop &> /dev/null
 %{__chkconfig} --del %{name}
fi

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc LICENSE NOTICE README.md
%{_sbindir}/%{name}
%{_sbindir}/%{alias_name}
%{_initrddir}/%{name}
%{_initrddir}/%{alias_name}
%{_sysconfdir}/%{alias_name}
%{_mandir}/man8/%{name}.8.gz
%{_sysconfdir}/%{name}/%{alias_name}.yml
%config(noreplace)%{_sysconfdir}/%{name}/%{name}.yml

################################################################################

%changelog
* Tue Mar 28 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.1-1
- Rebuilt with latest version of libevent

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.4.1-0
- backend server hostnames are resolved lazily
- redis_auth is only valid for a redis pool
- getaddrinfo returns non-zero +ve value on error
- fix-hang-when-command-only (charsyam)
- fix bug crash when get command without key and whitespace (charsyam)
- mark server as failed on protocol level transiet failures like -OOM, -LOADING, etc
- implemented support for parsing fine grained redis error response
- remove redundant conditional judgement in rbtree deletion (leo ma)
- fix bug mset has invalid pair (charsyam)
- fix bug mset has invalid pair (charsyam)
- temp fix a core on kqueue (idning)
- support "touch" command for memcached (panmiaocai)
- fix redis parse rsp bug (charsyam)
- SORT command can take multiple arguments. So it should be part of redis_argn() 
  and not redis_arg0()
- remove incorrect assert because client could send data after sending a quit 
  request which must be discarded
- allow file permissions to be set for UNIX domain listening socket (ori liveneh)
- return error if formatted is greater than mbuf size by using nc_vsnprintf() 
  in msg_prepend_format()
- fix req_make_reply on msg_get, mark it as response (idning)
- redis database select upon connect (arne claus)
- redis_auth (charsyam)
- allow null key(empty key) (idning)
- fix core on invalid mset like "mset a a a" (idning)

* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-0
- Init scripts migrated to kaosv
- Initial build
