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
Version:              1.6.1
Release:              0%{?dist}
License:              Copyright (c) 2014 DeNA Co., Ltd.
Group:                System Environment/Daemons
Vendor:               DeNA Co., Ltd.
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
* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to 1.6.1

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- Updated to 1.5.4

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to 1.5.0

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- Updated to 1.4.4

* Tue Aug 11 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-1
- Some fixes in spec and init script

* Mon Aug 10 2015 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Updated to 1.4.2

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- Updated to 1.3.1

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to 1.2.0

* Tue Mar 03 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- Updated to 1.0.1

* Tue Mar 03 2015 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to 1.0.0

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- Updated to 0.9.1

* Mon Dec 29 2014 Anton Novojilov <andy@essentialkaos.com> - 0.9.0-0
- Initial build
