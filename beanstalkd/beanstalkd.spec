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

###############################################################################

%define __chkconfig       %{_sbin}/chkconfig
%define __service         %{_sbin}/service
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd
%define __sysctl          %{_bindir}/systemctl

%define __user            %{name}
%define __group           %{__user}
%define __home            %{_localstatedir}/lib/%{name}
%define __logdir          %{_logdir}/%{name}
%define __binlogdir       %{__home}/binlog

###############################################################################

Summary:            A simple, fast work-queue service
Name:               beanstalkd
Version:            1.10
Release:            5%{?dist}
Group:              System Environment/Daemons
License:            GPLv3+
URL:                http://xph.us/software/beanstalkd/

Source0:            https://github.com/kr/%{name}/archive/v%{version}.tar.gz
Source1:            %{name}.init
Source2:            %{name}.sysconfig
Source3:            %{name}.service

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make libevent-devel

Requires:           kaosv >= 2.10

Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig initscripts
Requires(postun):   initscripts

###############################################################################

%description
beanstalkd is a simple, fast work-queue service. Its interface is generic,
but was originally designed for reducing the latency of page views in
high-volume web applications by running most time-consuming tasks
asynchronously.

%prep
%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} install PREFIX=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{__home}
install -dm 755 %{buildroot}%{__binlogdir}
install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%if 0%{?rhel} >= 7
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/
%endif

install -pm 644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/
install -pm 644 doc/protocol.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%pre
getent group %{__group} >/dev/null || %{__groupadd} -r %{__group}
getent passwd %{__user} >/dev/null || %{__useradd} -r -g %{__group} -d %{__home} -s /sbin/nologin \
                                                   -c "beanstalkd user" %{__user}
exit 0

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} enable %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

if [[ -d %{__home} ]] ; then
  install -d %{__binlogdir} -m 0755 -o %{__user} -g %{__group} %{__binlogdir}
fi

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} >= 7
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} %{name} stop &> /dev/null
  %{__chkconfig} --del %{name} &> /dev/null || :
%endif
fi

%postun
%if 0%{?rhel} >= 7
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

###############################################################################

%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}-%{version}/protocol.txt
%doc README LICENSE doc/protocol.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%endif
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

###############################################################################

%changelog
* Wed Nov 18 2015 Anton Novojilov <andy@essentialkaos.com> - 1.10-6
- Improved init script

* Fri Nov 07 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10-5
- Fixed typo

* Tue Oct 21 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10-4
- Init script migrated to kaosv version 2

* Fri Oct 17 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10-3
- Improved init script

* Wed Oct 15 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10-2
- Small fixes in spec

* Sat Aug 09 2014 Anton Novojilov <andy@essentialkaos.com> - 1.10-0
- Updated to latest stable release
- Improvements in init script

* Mon May 05 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9-6
- Fixed some minor bugs in spec
