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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         Intrusion Detection System
Name:            suricata
Version:         4.1.0
Release:         0%{?dist}
License:         GPLv2
Group:           Applications/Internet
URL:             http://suricata-ids.org

Source0:         http://www.openinfosecfoundation.org/download/%{name}-%{version}.tar.gz
Source1:         %{name}.initd
Source2:         %{name}.sysconfig
Source3:         %{name}.logrotate

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc gcc-c++ autoconf automake libtool lz4-devel
BuildRequires:   libyaml-devel libnfnetlink-devel libnetfilter_queue-devel
BuildRequires:   libnet-devel zlib-devel libpcap-devel pcre-devel
BuildRequires:   libcap-ng-devel nspr-devel nss-devel nss-softokn-devel
BuildRequires:   file-devel jansson-devel GeoIP-devel python-devel
BuildRequires:   lua-devel libluajit-devel

%if 0%{?rhel} >= 7
BuildRequires:   cargo
%endif

%if 0%{?rhel} <= 6
Requires:        initscripts kaosv >= 2.15
%endif

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine. This engine is not intended to
just replace or emulate the existing tools in the industry, but
will bring new ideas and technologies to the field. This new Engine
supports Multi-threading, Automatic Protocol Detection (IP, TCP,
UDP, ICMP, HTTP, TLS, FTP and SMB! ), Gzip Decompression, Fast IP
Matching, and GeoIP identification.

################################################################################

%prep
%setup -q

autoreconf -fv --install

%build
%configure --with-libnspr-includes=%{_includedir}/nspr4 \
           --with-libnss-includes=%{_includedir}/nss3 \
           --disable-gccmarch-native \
           --disable-coccinelle \
           --enable-nfqueue \
           --enable-af-packet \
           --enable-gccprotect \
           --enable-jansson \
           --enable-geoip \
           --enable-luajit

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} "bindir=%{_sbindir}"

install -dm 755 %{buildroot}%{_initddir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/rules
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_rundir}/%{name}
install -dm 755 %{buildroot}%{_logdir}/%{name}

install -pm 600 rules/*.rules %{buildroot}%{_sysconfdir}/%{name}/rules
install -pm 600 *.config %{buildroot}%{_sysconfdir}/%{name}
install -pm 600 %{name}.yaml %{buildroot}%{_sysconfdir}/%{name}
install -pm 755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

rm -rf %{buildroot}%{_includedir}
rm -f  %{buildroot}%{_libdir}/libhtp.la
rm -f  %{buildroot}%{_libdir}/libhtp.a
rm -f  %{buildroot}%{_libdir}/libhtp.so
rm -rf %{buildroot}%{_libdir}/pkgconfig

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%clean
rm -rf %{buildroot}

%post
%{__ldconfig}

%postun
%{__ldconfig}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING doc/Basic_Setup.txt
%doc doc/Setting_up_IPSinline_for_Linux.txt
%{_sbindir}/%{name}
%{_bindir}/%{name}sc
%{_bindir}/%{name}ctl
%{_bindir}/%{name}-update
%{_libdir}/libhtp*
%{_datadir}/%{name}/rules/*.rules
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}sc
%{python_sitelib}/suricata*.egg-info
%{_defaultdocdir}/%{name}/*
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yaml
%config(noreplace) %{_sysconfdir}/%{name}/*.config
%config(noreplace) %{_sysconfdir}/%{name}/rules/*.rules
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(755,root,root) %{_initddir}/%{name}
%attr(750,root,root) %dir %{_logdir}/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%dir %{_rundir}/%{name}

################################################################################

%changelog
* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.1.0-0
- Updated to the latest stable release

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.4-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 4.0.3-0
- Updated to the latest stable release

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Updated to the latest stable release

* Thu Sep 21 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Initial build
