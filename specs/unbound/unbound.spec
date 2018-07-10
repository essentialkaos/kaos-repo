################################################################################

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

%define __sysctl          %{_bindir}/systemctl
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

################################################################################

%{?!with_python: %global with_python 1}
%{?!with_munin: %global with_munin 1}

%if 0%{with_python} == 1
%if 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%endif

################################################################################

Summary:            Validating, recursive, and caching DNS(SEC) resolver
Name:               unbound
Version:            1.7.2
Release:            0%{?dist}
License:            BSD
Group:              System Environment/Daemons
URL:                https://www.unbound.net

Source0:            https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
Source1:            %{name}.service
Source2:            %{name}.conf
Source3:            %{name}.munin
Source4:            %{name}_munin_
Source5:            root.key
Source7:            %{name}-keygen.service
Source8:            tmpfiles-unbound.conf
Source9:            example.com.key
Source10:           example.com.conf
Source11:           block-example.com.conf
Source12:           https://data.iana.org/root-anchors/icannbundle.pem
Source13:           root.anchor
Source14:           %{name}.sysconfig
Source15:           %{name}-anchor.timer
Source16:           %{name}-munin.README
Source17:           %{name}-anchor.service

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc flex openssl-devel expat-devel
BuildRequires:      libevent-devel systemd pkgconfig

%if 0%{with_python}
BuildRequires:      python2-devel swig
%endif

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

Requires:           %{name}-libs = %{version}-%{release}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Unbound is a validating, recursive, and caching DNS(SEC) resolver.

The C implementation of Unbound is developed and maintained by NLnet
Labs. It is based on ideas and algorithms taken from a java prototype
developed by Verisign labs, Nominet, Kirei and ep.net.

Unbound is designed as a set of modular components, so that also
DNSSEC (secure DNS) validation and stub-resolvers (that do not run
as a server, but are linked into an application) are easily possible.

################################################################################

%if %{with_munin}
%package munin
Summary:            Plugin for the munin / munin-node monitoring package
Group:              System Environment/Daemons

Requires:           munin-node
Requires:           %{name} = %{version}-%{release} bc

BuildArch:          noarch

%description munin
Plugin for the munin / munin-node monitoring package
%endif

################################################################################

%package devel
Summary:            Development package that includes the unbound header files
Group:              Development/Libraries

Requires:           %{name}-libs = %{version}-%{release}
Requires:           pkgconfig openssl-devel

%description devel
The devel package contains the unbound library and the include files

################################################################################

%package libs
Summary:            Libraries used by the unbound server and client applications
Group:              Applications/System

Requires(post):     %{__ldconfig} systemd
Requires(postun):   %{__ldconfig} systemd
Requires(preun):    systemd
Requires(pre):      shadow-utils

%description libs
Contains libraries used by the unbound server and client applications

################################################################################

%if 0%{with_python}
%package -n python2-unbound
%{?python_provide:%python_provide python2-unbound}
Summary:            Python 2 modules and extensions for unbound
Group:              Applications/System

Requires:           %{name}-libs = %{version}-%{release}
Provides:           unbound-python = %{version}-%{release}
Obsoletes:          unbound-python < %{version}-%{release}

%description -n python2-unbound
Python 2 modules and extensions for unbound
%endif

################################################################################

%prep
%setup -qcn %{name}-%{version}

%if 0%{with_python}
mv %{name}-%{version} %{name}-%{version}_python2
pushd %{name}-%{version}_python2
%else
pushd %{name}-%{version}
%endif
cp -pr doc pythonmod libunbound ../
popd

%build
# This is needed to rebuild the configure script to support Python 3.x
# autoreconf -iv
export LDFLAGS="-Wl,-z,relro,-z,now -pie -specs=/usr/lib/rpm/redhat/redhat-hardened-ld"
export CFLAGS="$RPM_OPT_FLAGS -fPIE -pie"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIE -pie"

%if 0%{with_python}
pushd %{name}-%{version}_python2
%else
pushd %{name}-%{version}
%endif

%configure --with-libevent \
           --with-pthreads \
           --with-ssl \
           --disable-rpath \
           --disable-static \
           --enable-sha2 \
           --disable-gost \
           --enable-ecdsa \
%if %{with_python}
           --with-pythonmodule \
           --with-pyunbound PYTHON=%{__python2} \
%endif
           --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
           --with-pidfile=%{_localstatedir}/run/%{name}/%{name}.pid \
           --with-rootkey-file=%{_sharedstatedir}/unbound/root.key

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} streamtcp

%if 0%{with_python}
popd
%endif

%install
rm -rf %{buildroot}

install -pm 0644 %{SOURCE16} .

%if 0%{with_python}
pushd %{name}-%{version}_python2
%else
pushd %{name}-%{version}
%endif

%{make_install} unbound-event-install
install -m 0755 streamtcp %{buildroot}%{_sbindir}/unbound-streamtcp

%if 0%{with_python}
popd
%endif

install -dm 0755 %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig

install -pm 0644 %{SOURCE1}  %{buildroot}%{_unitdir}/unbound.service
install -pm 0644 %{SOURCE7}  %{buildroot}%{_unitdir}/unbound-keygen.service
install -pm 0644 %{SOURCE15} %{buildroot}%{_unitdir}/unbound-anchor.timer
install -pm 0644 %{SOURCE17} %{buildroot}%{_unitdir}/unbound-anchor.service
install -pm 0755 %{SOURCE2}  %{buildroot}%{_sysconfdir}/unbound
install -pm 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/unbound
install -pm 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/sysconfig/unbound

%if %{with_munin}
install -dm 0755 %{buildroot}%{_sysconfdir}/munin/plugin-conf.d
install -dm 0755 %{buildroot}%{_datadir}/munin/plugins/

install -pm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/munin/plugin-conf.d/unbound
install -pm 0755 %{SOURCE4} %{buildroot}%{_datadir}/munin/plugins/unbound

for plugin in unbound_munin_hits unbound_munin_queue unbound_munin_memory unbound_munin_by_type unbound_munin_by_class unbound_munin_by_opcode unbound_munin_by_rcode unbound_munin_by_flags unbound_munin_histogram ; do
  ln -s unbound %{buildroot}%{_datadir}/munin/plugins/$plugin
done
%endif

%if 0%{with_python}
pushd %{name}-%{version}_python2
%endif

install -Dm 0644 contrib/libunbound.pc \
                 %{buildroot}%{_libdir}/pkgconfig/libunbound.pc

%if 0%{with_python}
popd
%endif

# Install tmpfiles.d config
install -dm 0755 %{buildroot}%{_tmpfilesdir} %{buildroot}%{_sharedstatedir}/unbound
install -m 0644 %{SOURCE8} %{buildroot}%{_tmpfilesdir}/unbound.conf

install -m 0644 %{SOURCE5}  %{buildroot}%{_sysconfdir}/unbound/
install -m 0644 %{SOURCE13} %{buildroot}%{_sharedstatedir}/unbound/root.key

rm -f %{buildroot}%{_libdir}/*.la

%if 0%{with_python}
rm -f %{buildroot}%{python2_sitearch}/*.la
%endif

for mpage in ub_ctx ub_result ub_ctx_create ub_ctx_delete ub_ctx_set_option ub_ctx_get_option ub_ctx_config ub_ctx_set_fwd ub_ctx_resolvconf ub_ctx_hosts ub_ctx_add_ta ub_ctx_add_ta_file ub_ctx_trustedkeys ub_ctx_debugout ub_ctx_debuglevel ub_ctx_async ub_poll ub_wait ub_fd ub_process ub_resolve ub_resolve_async ub_cancel ub_resolve_free ub_strerror ub_ctx_print_local_zones ub_ctx_zone_add ub_ctx_zone_remove ub_ctx_data_add ub_ctx_data_remove ; do
  echo ".so man3/libunbound.3" > %{buildroot}%{_mandir}/man3/$mpage ;
done

mkdir -p %{buildroot}%{_localstatedir}/run/unbound

mkdir -p %{buildroot}%{_sysconfdir}/unbound/{keys.d,conf.d,local.d}
install -p %{SOURCE9}  %{buildroot}%{_sysconfdir}/unbound/keys.d/
install -p %{SOURCE10} %{buildroot}%{_sysconfdir}/unbound/conf.d/
install -p %{SOURCE11} %{buildroot}%{_sysconfdir}/unbound/local.d/

echo ".so man8/unbound-control.8" > %{buildroot}%{_mandir}/man8/unbound-control-setup.8

%clean
rm -rf %{buildroot}

%pre libs
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin -c "Unbound DNS resolver" unbound

%post
%systemd_post unbound.service
%systemd_post unbound-keygen.service

%post libs
%{__ldconfig}
%systemd_post unbound-anchor.timer

if [[ "$1" -eq 1 ]] ; then
  %{__sysctl} start unbound-anchor.timer &>/dev/null || :
fi

%preun
%systemd_preun unbound.service
%systemd_preun unbound-keygen.service

%preun libs
%systemd_preun unbound-anchor.timer

%postun
%systemd_postun_with_restart unbound.service
%systemd_postun unbound-keygen.service

%postun libs
%{__ldconfig}
%systemd_postun_with_restart unbound-anchor.timer

%triggerun -- unbound < 1.4.12-4
%{_bindir}/systemd-sysv-convert --save unbound &>/dev/null || :

%{__chkconfig} --del unbound &>/dev/null || :

%{__sysctl} try-restart unbound.service &>/dev/null || :
%{__sysctl} try-restart unbound-keygen.service &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%doc doc/CREDITS doc/FEATURES
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-keygen.service
%attr(0755,unbound,unbound) %dir %{_localstatedir}/run/%{name}
%attr(0644,root,root) %{_tmpfilesdir}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/keys.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/keys.d/*.key
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/conf.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.conf
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/local.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/local.d/*.conf
%{_sbindir}/unbound
%{_sbindir}/unbound-checkconf
%{_sbindir}/unbound-control
%{_sbindir}/unbound-control-setup
%{_sbindir}/unbound-host
%{_sbindir}/unbound-streamtcp
%{_mandir}/man1/*
%{_mandir}/man5/*
%exclude %{_mandir}/man8/unbound-anchor*
%{_mandir}/man8/*

%if 0%{with_python}
%files -n python2-unbound
%defattr(-,root,root,-)
%{python2_sitearch}/*
%doc pythonmod/LICENSE
%doc libunbound/python/examples/*
%doc pythonmod/examples/*
%endif

%if 0%{with_munin}
%files munin
%defattr(-,root,root,-)
%doc unbound-munin.README
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/unbound
%{_datadir}/munin/plugins/unbound*
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/libunbound.so
%{_includedir}/unbound.h
%{_includedir}/unbound-event.h
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc

%files libs
%defattr(-,root,root,-)
%doc doc/README
%doc doc/LICENSE
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%{_sbindir}/unbound-anchor
%{_libdir}/libunbound.so.*
%{_mandir}/man8/unbound-anchor*
%{_sysconfdir}/%{name}/icannbundle.pem
%{_unitdir}/unbound-anchor.timer
%{_unitdir}/unbound-anchor.service
%dir %attr(0755,unbound,unbound) %{_sharedstatedir}/%{name}
%attr(0644,unbound,unbound) %config %{_sharedstatedir}/%{name}/root.key
%attr(0644,root,root) %config %{_sysconfdir}/%{name}/root.key

################################################################################

%changelog
* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- Updated to latest stable release

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to latest stable release

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.8-0
- Initial build for kaos-repo
