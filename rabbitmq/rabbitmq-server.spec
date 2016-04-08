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
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig

###############################################################################

%define _basename           rabbitmq
%define _user               %{_basename}
%define _group              %{_basename}
%global _rabbit_libdir      %{_exec_prefix}/lib/%{_basename}
%global _rabbit_erllibdir   %{_rabbit_libdir}/lib/%{_basename}_server-%{version}
%global _plugins_state_dir  %{_localstatedir}/lib/%{_basename}/plugins

###############################################################################

Summary:           The RabbitMQ server
Name:              %{_basename}-server
Version:           3.6.1
Release:           0%{?dist}
License:           MPLv1.1
Group:             Applications/Internet
URL:               http://www.rabbitmq.com

Source0:           http://www.rabbitmq.com/releases/%{name}/v%{version}/%{name}-%{version}.tar.xz
Source1:           %{name}.init
Source2:           %{_basename}-script-wrapper
Source3:           %{name}.logrotate
Source4:           %{name}.ocf

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          erlang >= 16 logrotate
BuildRequires:     erlang >= 16 python-simplejson xmlto libxslt python zip nc

Requires(pre):     shadow-utils initscripts
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts

###############################################################################

%description
RabbitMQ is an implementation of AMQP, the emerging standard for high
performance enterprise messaging. The RabbitMQ server is a robust and
scalable implementation of an AMQP broker.

###############################################################################

%prep
%setup -q

%build 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} install-bin install-man DESTDIR=%{buildroot} \
                                  PREFIX=%{_exec_prefix} \
                                  RMQ_ROOTDIR=%{_rabbit_libdir} \
                                  MANDIR=%{_mandir}

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{_basename}/mnesia
%{__mkdir_p} %{buildroot}%{_logdir}/%{_basename}

install -pDm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pDm 0755 %{SOURCE2} %{buildroot}%{_sbindir}/%{_basename}ctl
install -pDm 0755 %{SOURCE2} %{buildroot}%{_sbindir}/%{name}
install -pDm 0755 %{SOURCE4} %{buildroot}%{_exec_prefix}/lib/ocf/resource.d/%{_basename}/%{name}

install -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{_basename}

%{__rm} -f %{_maindir}/LICENSE %{_maindir}/LICENSE-MPL-RabbitMQ %{_maindir}/INSTALL

install -d %{buildroot}%{_rundir}/%{_basename}

%{__rm} -rf %{buildroot}%{_rabbit_erllibdir}/LICENSE-*

%pre
if [[ $1 -gt 1 ]] ; then
  %{__service} %{name} stop &> /dev/null || :
fi

getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -g %{_group} -d %{_localstatedir}/lib/%{_basename} \
    -c "RabbitMQ messaging server" %{_user}

%post
%{__chkconfig} --add %{name}

%preun
if [[ $1 -eq 0 ]]; then
  %{__service} %{name} stop &> /dev/null || :
  %{__chkconfig} --del %{name}
fi

%{__rm} -rf %{_plugins_state_dir}
for ext in rel script boot ; do
  %{__rm} -f %{_rabbit_erllibdir}/ebin/rabbit.$ext
done

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, -)
%doc LICENSE LICENSE-*
%attr(0750, %{_user}, %{_group}) %dir %{_localstatedir}/lib/%{_basename}
%attr(0750, %{_user}, %{_group}) %dir %{_logdir}/%{_basename}
%attr(0755, %{_user}, %{_group}) %dir %{_rundir}/%{_basename}
%{_sysconfdir}/%{_basename}
%{_rabbit_erllibdir}
%{_rabbit_libdir}/bin
%{_initrddir}/%{name}
%{_mandir}/*
%{_sbindir}/*
%{_exec_prefix}/lib/ocf/resource.d/%{_basename}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

###############################################################################

%changelog
* Sat Apr 09 2016 Anton Novojilov <andy@essentialkaos.com> - 3.6.1-0
- Updated to latest release

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 3.6.0-0
- Updated to latest release

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.6-0
- Updated to latest release

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.5-0
- Updated to latest release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.4-0
- Updated to latest release

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.3-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.1-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5.0-0
- Updated to latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.4.4-0
- Updated to latest release

* Wed Jan 07 2015 Anton Novojilov <andy@essentialkaos.com> - 3.4.3-0
- Updated to latest release

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.2-0
- Updated to latest release

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.1-0
- Updated to latest release

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.0-0
- Updated to latest release

* Wed Aug 20 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.5-0
- Updated to latest release

* Thu Jul 03 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.4-0
- Updated to latest release

* Thu Jul 03 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.3-0
- Updated to latest release

* Thu Jul 03 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.2-0
- Updated to latest release

* Mon May 12 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.1-0
- Updated to latest release

* Mon May 12 2014 Anton Novojilov <andy@essentialkaos.com> - 3.3.0-0
- Updated to latest release

* Tue Mar 25 2014 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- Updated to latest release

* Thu Jan 23 2014 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- Updated to latest release

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Updated to latest release

* Mon Nov 18 2013 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Updated to latest release

* Thu Oct 03 2013 Anton Novojilov <andy@essentialkaos.com> - 3.1.5-2
- Rewrited spec from epel repo
