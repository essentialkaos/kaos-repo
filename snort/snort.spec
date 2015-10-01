###############################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0002

########################################################################################

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

########################################################################################

%define rules_dir         %{_sysconfdir}/%{name}/rules
%define daemon_name       snortd
%define usershell         /bin/false

########################################################################################

Summary:         An open source Network Intrusion Detection System (NIDS)
Name:            snort
Version:         2.9.7.6
Release:         0%{?dist}
License:         GPL
Group:           Applications/Internet
URL:             http://www.snort.org

Source0:         https://www.snort.org/downloads/%{name}/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        libdnet libpcap pcre daq

BuildRequires:   autoconf automake make gcc libtool
BuildRequires:   pcre-devel libpcap-devel libdnet-devel daq-devel

Provides:        %{name} = %{version}-%{release}

########################################################################################

%description
Snort is an open source network intrusion detection system, capable of
performing real-time traffic analysis and packet logging on IP networks.
It can perform protocol analysis, content searching/matching and can be
used to detect a variety of attacks and probes, such as buffer overflows,
stealth port scans, CGI attacks, SMB probes, OS fingerprinting attempts,
and much more.

########################################################################################

%prep
%setup -q

%build

export AM_CFLAGS="%{optflags}"

./configure --prefix=%{_prefix} \
            --bindir=%{_sbindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir}/%{name} \
            --with-libpcap-includes=%{_includedir} \
            --enable-targetbased \
            --enable-control-socket

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

find . -type 'd' -name "CVS" -print | xargs rm -rf

sed -i 's;var RULE_PATH ../rules;var RULE_PATH %{rules_dir};' etc/%{name}.conf
sed -i 's;dynamicpreprocessor directory \/usr\/local/lib\/snort_dynamicpreprocessor;dynamicpreprocessor directory %{_libdir}\/%{name}-%{version}_dynamicpreprocessor;' etc/%{name}.conf
sed -i 's;dynamicengine \/usr\/local/lib\/snort_dynamicengine;dynamicengine %{_libdir}\/%{name}-%{version}_dynamicengine;' etc/%{name}.conf

install -dm 755 %{buildroot}%{_sbindir}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{rules_dir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_var}/log/%{name}
install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_mandir}/man8
install -dm 755 %{buildroot}%{_docdir}/%{name}-%{version}
install -dm 755 %{buildroot}%{_libdir}/%{name}-%{version}_dynamicengine
install -dm 755 %{buildroot}%{_libdir}/%{name}-%{version}_dynamicpreprocessor

install -pm 755 src/%{name} %{buildroot}%{_sbindir}/%{name}-plain
install -pm 755 tools/control/%{name}_control %{buildroot}%{_bindir}/%{name}_control
install -pm 755 tools/u2spewfoo/u2spewfoo %{buildroot}%{_bindir}/u2spewfoo
install -pm 755 tools/u2boat/u2boat %{buildroot}%{_bindir}/u2boat

install -pm 755 src/dynamic-plugins/sf_engine/.libs/libsf_engine.so \
                %{buildroot}%{_libdir}/%{name}-%{version}_dynamicengine

ln -sf %{_libdir}/%{name}-%{version}_dynamicengine/libsf_engine.so \
       %{buildroot}%{_libdir}/%{name}-%{version}_dynamicengine/libsf_engine.so.0

install -pm 755 src/dynamic-preprocessors/build%{_libdir}/snort_dynamicpreprocessor/*.so* \
                %{buildroot}%{_libdir}/%{name}-%{version}_dynamicpreprocessor

for file in %{buildroot}%{_libdir}/%{name}-%{version}_dynamicpreprocessor/*.so ; do  
  preprocessor=`basename $file`
  ln -sf %{_libdir}/%{name}-%{version}_dynamicpreprocessor/$preprocessor.0 $file     
done  

install -pm 644 %{name}.8 %{buildroot}%{_mandir}/man8/
install -pm 755 rpm/%{daemon_name} %{buildroot}%{_initrddir}

install -pm 644 rpm/%{name}.sysconfig \
                %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 rpm/%{name}.logrotate \
                %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -pm 644 etc/reference.config \
                etc/classification.config \
                etc/unicode.map \
                etc/gen-msg.map \
                etc/threshold.conf \
                etc/%{name}.conf \
                %{buildroot}%{_sysconfdir}/%{name}/

ln -sf %{_sbindir}/%{name}-plain %{buildroot}%{_sbindir}/%{name}

find doc -maxdepth 1 -type f -not -name 'Makefile*' -exec install -pm 0644 {} %{buildroot}%{_docdir}/%{name}-%{version} \;

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || %{__groupadd} %{name} 2> /dev/null || true
getent passwd %{name} >/dev/null || %{__useradd} -M -d %{_var}/log/%{name} -s %{usershell} -g %{name} %{name} 2>/dev/null || true
exit 0

%post
if [[ $1 -eq 1 ]] ; then
  chown -R %{name}:%{name} %{_var}/log/%{name}
  %{__chkconfig} --add %{daemon_name}
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__service} %{daemon_name} stop 2>/dev/null 1>/dev/null
  %{__chkconfig} --del %{daemon_name}
fi

########################################################################################

%files
%defattr(-,root,root)
%{_sbindir}/%{name}-plain
%{_sbindir}/%{name}
%{_bindir}/%{name}_control
%{_bindir}/u2spewfoo
%{_bindir}/u2boat
%{_mandir}/man8/%{name}.8.*
%dir %{rules_dir}
%config(noreplace) %{_sysconfdir}/%{name}/classification.config
%config(noreplace) %{_sysconfdir}/%{name}/reference.config
%config(noreplace) %{_sysconfdir}/%{name}/threshold.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.map
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_initrddir}/%{daemon_name}
%dir %{_sysconfdir}/%{name}
%{_docdir}/%{name}-%{version}/*
%dir %{_libdir}/%{name}-%{version}_dynamicengine
%{_libdir}/%{name}-%{version}_dynamicengine/libsf_engine.*
%dir %{_libdir}/%{name}-%{version}_dynamicpreprocessor
%{_libdir}/%{name}-%{version}_dynamicpreprocessor/libsf_*_preproc.*
%dir %{_docdir}/%{name}-%{version}

%attr(0755,%{name},%{name}) %dir %{_var}/log/%{name}

########################################################################################

%changelog
* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.9.7.6-0
- Updated to latest version

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.9.7.5-0
- Updated to latest version

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.9.7.3-0
- Updated to latest version

* Wed Dec 17 2014 Anton Novojilov <andy@essentialkaos.com> - 2.9.7.0-0
- Updated to latest version

* Fri Oct 03 2014 Anton Novojilov <andy@essentialkaos.com> - 2.9.6.2-0
- Initial build
