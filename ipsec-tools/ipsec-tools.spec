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

################################################################################

Summary:           User-space IPsec tools for various IPsec implementations
Name:              ipsec-tools
Version:           0.8.2
Release:           0%{?dist}
License:           BSD
Group:             Development/System
URL:               http://ipsec-tools.sourceforge.net/

Source0:           http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:           racoon.init
Source2:           setkey.conf

Patch0:            support-iphone-os-main-mode-with-psk.patch
Patch1:            make-peer_certfile-dnssec-validate-dnssec.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:          racoon

BuildRequires:     flex kernel-headers libselinux-devel
BuildRequires:     openssl-devel readline-devel pam-devel krb5-devel openldap-devel

################################################################################

%description
User-space IPsec tools for various IPsec implementations. A port of KAME's
libipsec, setkey, and racoon to the Linux OS. Also works on various BSD systems.

################################################################################

%package devel
Summary:           Development files for %{name}
Group:             Development/Tools

%description devel
Development files for %{name}

################################################################################

%prep
%setup -q

%patch0 -p1
%patch1 -p1

sed -ri '/LIBS.+ -R/ d' configure

%build
sed -ri 's|-Werror||' configure
sed -ri 's|@/cert|@/racoon/cert|' src/racoon/samples/racoon.conf.in

%configure \
 --sysconfdir=%{_sysconfdir}/racoon \
 --localstatedir=%{_localstatedir}/run \
 --disable-static \
 --enable-adminport \
 --enable-rc5 \
 --enable-idea \
 --enable-hybrid \
 --enable-frag \
 --enable-gssapi \
 --enable-stats \
 --enable-dpd \
 --enable-natt \
 --enable-broken-natt \
 --enable-security-context=no \
 --with-kernel-headers=%{_includedir} \
 --with-readline \
 --with-libpam \
 --with-libldap \
 --without-libiconv \
 CFLAGS="%{optflags}" \
 LDFLAGS="-Wl,--strip-all"

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 755 %{buildroot}%{_sysconfdir}/racoon/
install -dm 755 %{buildroot}%{_sysconfdir}/racoon/cert
install -m 644 src/racoon/samples/psk.txt %{buildroot}%{_sysconfdir}/racoon/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/racoon/setkey.conf

sed -r 's|@sysconfdir_x@|%{_sysconfdir}|' src/racoon/samples/racoon.conf.in > %{buildroot}%{_sysconfdir}/racoon/racoon.conf

install -Dm 644 rpm/suse/sysconfig.racoon %{buildroot}%{_sysconfdir}/sysconfig/racoon
install -Dm 755 %{SOURCE1} %{buildroot}%{_initrddir}/racoon

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc NEWS README src/racoon/doc/* src/racoon/samples src/setkey/*.cf
%config(noreplace) %{_sysconfdir}/racoon/psk.txt
%config(noreplace) %{_sysconfdir}/racoon/racoon.conf
%config(noreplace) %{_sysconfdir}/racoon/setkey.conf
%config(noreplace) %{_sysconfdir}/sysconfig/racoon
%dir %{_sysconfdir}/racoon
%dir %{_sysconfdir}/racoon/cert
%{_sbindir}/*
%{_initrddir}/racoon
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*
%dir %{_rundir}/racoon

%files devel
%defattr(-,root,root)
%dir %{_includedir}/libipsec
%dir %{_includedir}/racoon
%{_includedir}/libipsec/*.h
%{_includedir}/racoon/*.h
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%doc %{_mandir}/man3/*

################################################################################

%changelog
* Fri Apr 11 2014 Anton Novojilov <andy@essentialkaos.com> - 0.8.2-0
- Initial build
