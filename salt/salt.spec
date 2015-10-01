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

Summary:          A parallel remote execution system
Name:             salt
Version:          2015.8.0
Release:          0%{?dist}
License:          ASL 2.0
Group:            System Environment/Daemons
URL:              http://saltstack.org

Source0:          https://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
Source1:          %{name}-master.init
Source2:          %{name}-syndic.init
Source3:          %{name}-minion.init
Source4:          %{name}.sysconfig
Source5:          %{name}.logrotate

Patch0:           %{name}-%{version}-config.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

Requires:         kaosv pciutils yum-utils sshpass PyYAML m2crypto
Requires:         python-crypto python-zmq python-jinja2 python-msgpack python-requests

%ifarch %{ix86} x86_64
Requires:         dmidecode
%endif

BuildRequires:    m2crypto python-crypto python-devel python-jinja2
BuildRequires:    python-msgpack python-pip python-zmq PyYAML python-unittest2

Requires(post):   %{__chkconfig}
Requires(preun):  %{__chkconfig}
Requires(preun):  initscripts
Requires(postun): initscripts

Provides:         %{name} = %{version}-%{release}

########################################################################################

%description
Salt is a distributed remote execution system used to execute commands and 
query data. It was developed in order to bring the best solutions found in 
the world of remote execution together and make them better, faster and more 
malleable. Salt accomplishes this via its ability to handle larger loads of 
information, and not just dozens, but hundreds or even thousands of individual 
servers, handle them quickly and through a simple and manageable interface.

########################################################################################

%package master
Summary:          Management component for salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description master 
The Salt master is the central server to which all minions connect.

########################################################################################

%package minion
Summary:          Client component for salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description minion
Salt minion is queried and controlled from the master.

########################################################################################

%prep
%setup -q
%patch0 -p1

%build
%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --root %{buildroot}

install -dm 755 %{buildroot}%{_initrddir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_cachedir}/%{name}

install -pm 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-master
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-syndic
install -pm 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-minion

install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -pm 640 conf/minion %{buildroot}%{_sysconfdir}/%{name}/minion
install -pm 640 conf/master %{buildroot}%{_sysconfdir}/%{name}/master

%preun master
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name}-master stop >/dev/null 2>&1
  %{__service} %{name}-syndic stop >/dev/null 2>&1
  %{__chkconfig} --del %{name}-master
  %{__chkconfig} --del %{name}-syndic
fi

%preun minion
if [[ $1 -eq 0 ]] ; then
  %{__service} %{name}-minion stop >/dev/null 2>&1
  %{__chkconfig} --del %{name}-minion
fi

%post master
%{__chkconfig} --add %{name}-master
%{__chkconfig} --add %{name}-syndic

%post minion
%{__chkconfig} --add %{name}-minion

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE AUTHORS README.rst
%doc %{_mandir}/man7/%{name}.7.*
%{python_sitelib}/%{name}/*
%{python_sitelib}/%{name}-*.egg-info
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/sysconfig/%{name}
%{_cachedir}/%{name}

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-call.1.*
%doc %{_mandir}/man1/%{name}-minion.1.*
%doc %{_mandir}/man1/%{name}-proxy.1.*
%config(noreplace) %{_sysconfdir}/%{name}/minion
%{_bindir}/%{name}-call
%{_bindir}/%{name}-minion
%{_bindir}/%{name}-proxy
%{_initrddir}/%{name}-minion

%files master
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}-api.1.*
%doc %{_mandir}/man1/%{name}-cloud.1.*
%doc %{_mandir}/man1/%{name}-cp.1.*
%doc %{_mandir}/man1/%{name}-key.1.*
%doc %{_mandir}/man1/%{name}-master.1.*
%doc %{_mandir}/man1/%{name}-run.1.*
%doc %{_mandir}/man1/%{name}-ssh.1.*
%doc %{_mandir}/man1/%{name}-syndic.1.*
%doc %{_mandir}/man1/%{name}-unity.1.*
%config(noreplace) %{_sysconfdir}/%{name}/master
%{_bindir}/spm
%{_bindir}/%{name}
%{_bindir}/%{name}-api
%{_bindir}/%{name}-cloud
%{_bindir}/%{name}-cp
%{_bindir}/%{name}-key
%{_bindir}/%{name}-master
%{_bindir}/%{name}-run
%{_bindir}/%{name}-ssh
%{_bindir}/%{name}-syndic
%{_bindir}/%{name}-unity
%{_initrddir}/%{name}-master
%{_initrddir}/%{name}-syndic

########################################################################################

%changelog
* Mon Sep 21 2015 Gleb Goncharov <inbox@gongled.ru> - 2015.8.0-0
- Updated to 2015.8.0

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 2015.5.5-0
- Updated to 2015.5.5

* Wed Aug 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2015.5.3-0
- Updated to 2015.5.3

* Mon Jun 15 2015 Anton Novojilov <andy@essentialkaos.com> - 2015.5.2-0
- Updated to 2015.5.2

* Sat May 30 2015 Anton Novojilov <andy@essentialkaos.com> - 2015.5.1-0
- Updated to 2015.5.1

* Tue May 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2014.7.4-1
- Updated to 2014.7.4

* Thu Apr 30 2015 Anton Novojilov <andy@essentialkaos.com> - 2014.7.2-1
- Updated to 2014.7.2
