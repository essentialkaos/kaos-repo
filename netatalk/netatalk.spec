################################################################################

%define _hardened_build   1

%{!?kerberos:%define kerberos 1}

%define with_acls         1
%define with_cracklib     1
%define with_docbook      1
%define with_dbus         1
%define with_dtrace       1
%define with_ldap         1
%define with_libevent     1
%define with_mysql        1
%define with_openafs      0
%define with_tcp_wrappers 1
%define with_quota        1

%define docbook_ver       $(rpm -q --qf "%%{VERSION}" docbook-style-xsl)

%if 0%{?rhel} >= 7
%define with_bdb          1
%else
%define with_bdb          0
%endif

%if 0%{?rhel} >= 7
%define with_tracker      1
%define tracker_ver       $(rpm -qls tracker-devel.%{_target_cpu} | grep sparql | grep pc | cut -d"-" -f3 | cut -d"." -f1-2 | sort -u)
%else
%define with_tracker      0
%endif

%if 0%{?rhel} >= 7
%define with_procpsng    1
%else
%define with_procpsng    0
%endif

%if 0%{?rhel} >= 7
%define with_systemd      1
%else
%define with_systemd      0
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

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

Summary:           Open Source Apple Filing Protocol(AFP) fileserver
Name:              netatalk
Version:           3.1.11
Release:           0%{?dist}
License:           GPLv2+
Group:             Applications/System
URL:               http://netatalk.sourceforge.net

Source0:           http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:           %{name}.pam-system-auth

BuildRequires:     gcc avahi-devel bison flex libattr-devel libgcrypt-devel
BuildRequires:     krb5-devel openssl-devel libtdb-devel pam-devel

%if 0%{?with_cracklib}
BuildRequires:     cracklib-devel
%endif
%if 0%{?with_dbus}
BuildRequires:     dbus-devel dbus-glib-devel
%endif
%if 0%{?with_docbook}
BuildRequires:     docbook-style-xsl
%endif
%if 0%{?with_acls}
BuildRequires:     libacl-devel
%endif
%if 0%{?with_bdb}
BuildRequires:     libdb-devel
%else
BuildRequires:     db4-devel
%endif
%if 0%{?with_libevent}
%if 0%{?rhel} >= 7
BuildRequires:     libevent-devel
%else
BuildRequires:     libevent2-devel
%endif
%endif
%if 0%{?with_docbook}
BuildRequires:     libxslt
%endif
%if 0%{?with_mysql}
BuildRequires:     mysql-devel
%endif
%if 0%{?with_openafs}
BuildRequires:     openafs-devel
%endif
%if 0%{?with_ldap}
BuildRequires:     openldap-devel
%endif
%if 0%{?with_procpsng}
BuildRequires:     procps-ng
%else
BuildRequires:     procps
%endif
%if 0%{?with_quota}
BuildRequires:     quota-devel
%endif
%if 0%{?with_systemd}
BuildRequires:     systemd
%endif
%if 0%{?with_dtrace}
BuildRequires:     systemtap-sdt-devel
%endif
%if 0%{?with_tcp_wrappers}
BuildRequires:     tcp_wrappers-devel
%endif
%if 0%{?with_tracker}
BuildRequires:     tracker-devel
%endif

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          dbus-python perl-IO-Socket-INET6

%if 0%{?with_tracker}
Requires:          dconf
%endif

%if 0%{?with_systemd}
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

################################################################################

%description
Netatalk is a freely-available Open Source AFP fileserver. A *NIX/*BSD
system running Netatalk is capable of serving many Macintosh clients
simultaneously as an AppleShare file server (AFP).

################################################################################

%package        devel
Summary:        Development files for %{name}
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for developing applications
that use %{name}.

################################################################################

%prep
%setup -q
%if 0%{?with_libevent}
rm -fr libevent/
%endif

# Avoid re-running the autotools
# touch -r aclocal.m4 configure configure.ac macros/gssapi-check.m4

# fix permissions
find include \( -name '*.h' -a -executable \) -exec chmod -x {} \;

%build
%ifarch ppc ppc64 s390 s390x
export CFLAGS="$CFLAGS -fsigned-char"
%endif

%configure \
        --localstatedir=%{_localstatedir}/lib \
%if 0%{?with_acls}
        --with-acl \
%endif
%if 0%{?with_cracklib}
        --with-cracklib \
%endif
%if 0%{?with_docbook}
        --with-docbook=%{_datadir}/sgml/docbook/xsl-stylesheets-%{docbook_ver} \
%endif
        --with-kerberos \
        --with-libgcrypt \
        --with-pam \
        --with-pkgconfdir=%{_sysconfdir}/%{name}/ \
        --with-shadow                               \
        --with-tbd=no \
        --with-uams-path=%{_libdir}/%{name} \
        --enable-pgp-uam \
        --enable-shared \
        --enable-krbV-uam \
        --enable-overwrite \
%if 0%{?with_systemd}
        --with-init-style=redhat-systemd \
%else
        --with-init-style=redhat-sysv \
%endif
%if 0%{?with_tracker}
        --with-spotlight \
        --with-tracker-pkgconfig-version=%{tracker_ver} \
        --with-dbus-daemon=%{_bindir}/dbus-daemon \
%endif
%if 0%{?with_libevent}
        --without-libevent \
        --with-libevent-header=%{_includedir} \
        --with-libevent-lib=%{_libdir} \
%endif
        --without-tdb \
        --with-bdb \
        --disable-silent-rules \
        --disable-static

%{__make} %{?_smp_mflags}
%{__make} -C doc/manual html-local

%install
rm -rf %{buildroot}
%{make_install}

mkdir -p %{buildroot}%{_var}/lock/%{name}

install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

find %{buildroot} -name '*.la' -delete -print

%check
bash test/afpd/test.sh

%clean
rm -rf %{buildroot}

################################################################################

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} <= 6
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload %{name}.service &>/dev/null || :
  %{__systemctl} preset %{name}.service &>/dev/null || :
%endif
fi
%{__ldconfig}

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} <= 6
  %{__service} %{name} stop &>/dev/null || :
  %{__chkconfig} --del %{name} &>/dev/null || :
%endif
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%endif
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS NEWS
%if 0%{?rhel} >= 7
%license COPYING COPYRIGHT
%else
%doc COPYING COPYRIGHT
%endif
%doc doc/manual/*.html
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/%{name}-dbus.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/afp.conf
%config(noreplace) %{_sysconfdir}/%{name}/dbus-session.conf
%config(noreplace) %{_sysconfdir}/%{name}/extmap.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_bindir}/*
%exclude %{_bindir}/%{name}-config
%{_libdir}/%{name}/
%{_libdir}/libatalk.so.*
%{_mandir}/man*/*
%exclude %{_mandir}/man*/%{name}-config*
%{_sbindir}/*
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%ghost %dir %{_var}/lock/%{name}
%{_localstatedir}/lib

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_datadir}/aclocal/%{name}.m4
%{_includedir}/atalk/
%{_libdir}/libatalk.so
%{_mandir}/man*/%{name}-config.1*

################################################################################

%changelog
* Sun Feb 11 2018 <inbox@gongled.ru> - 3.1.11-0
- Initial build
