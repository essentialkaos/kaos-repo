################################################################################

%if ! (0%{?rhel} >= 6 || 0%{?fedora} > 12)
%global with_python26 1
%define pybasever 2.6
%define __python_ver 26
%define __python %{_bindir}/python%{?pybasever}
%endif

%global include_tests 1

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

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

################################################################################

Summary:          A parallel remote execution system
Name:             salt
Version:          2015.8.1
Release:          0%{?dist}
License:          ASL 2.0
Group:            System Environment/Daemons
URL:              http://saltstack.org

Source0:          http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
Source1:          %{name}.sysconfig
Source2:          %{name}-master.init
Source3:          %{name}-syndic.init
Source4:          %{name}-minion.init
Source5:          %{name}-api.init
Source6:          %{name}-master.service
Source7:          %{name}-syndic.service
Source8:          %{name}-minion.service
Source9:          %{name}-api.service
Source10:         README.fedora
Source11:         %{name}-common.logrotate
Source12:         salt.bash

Patch0:           %{name}-%{version}-config.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

%ifarch %{ix86} x86_64
Requires:         dmidecode
%endif

Requires:         pciutils which yum-utils

%if 0%{?with_python26}

BuildRequires:    python26-devel python26-tornado >= 4.2.1 python26-six
Requires:         python26-crypto >= 2.6.1 python26-jinja2 python26-msgpack > 0.3
Requires:         python26-PyYAML python26-requests >= 1.0.0 python26-tornado >= 4.2.1
Requires:         python26-zmq python26-six

%else

%if ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})
BuildRequires:    python-crypto >= 2.6.1 python-jinja2 python-msgpack > 0.3
BuildRequires:    python-pip python-zmq PyYAML python-requests python-unittest2
BuildRequires:    python-mock git python-libcloud python-six

%if ((0%{?rhel} == 6) && 0%{?include_tests})
BuildRequires:    python-argparse
Requires:         kaosv
%endif

%endif

BuildRequires:    python-devel python-tornado >= 4.2.1 python-futures >= 2.0
Requires:         python-crypto >= 2.6.1 python-jinja2 python-msgpack > 0.3
Requires:         PyYAML python-requests >= 1.0.0 python-zmq python-markupsafe
Requires:         python-tornado >= 4.2.1 python-futures >= 2.0 python-six

%endif

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

%else

%if 0%{?systemd_preun:1}

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%endif

BuildRequires:    systemd-units
Requires:         systemd-python

%endif

################################################################################

%description
Salt is a distributed remote execution system used to execute commands and 
query data. It was developed in order to bring the best solutions found in 
the world of remote execution together and make them better, faster and more 
malleable. Salt accomplishes this via its ability to handle larger loads of 
information, and not just dozens, but hundreds or even thousands of individual 
servers, handle them quickly and through a simple and manageable interface.

################################################################################

%package master
Summary:          Management component for salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}
%if (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires:         systemd-python
%endif

%description master
The Salt master is the central server to which all minions connect.

################################################################################

%package minion
Summary:          Client component for Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions 
from the master, runs jobs, and returns results back to the master.

################################################################################

%package syndic
Summary:          Master-of-master component for Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a 
higher-level master, allowing for tiered organization of your Salt
infrastructure.

################################################################################

%package api
Summary:          REST API for Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name}-master = %{version}-%{release}
Requires:         python-cherrypy

%description api
salt-api provides a REST interface to the Salt master.

################################################################################

%package cloud
Summary:          Cloud provisioner for Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name}-master = %{version}-%{release}
Requires:         python-libcloud

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and 
adds them to the master's collection of controllable minions.

################################################################################

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use 
of an agent (salt-minion) service.

################################################################################

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1

%build

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --root %{buildroot}

# Add some directories
install -dm 755 %{buildroot}%{_var}/cache/salt
install -dm 755 %{buildroot}%{_sysconfdir}/salt
install -dm 755 %{buildroot}%{_sysconfdir}/salt/cloud.conf.d
install -dm 755 %{buildroot}%{_sysconfdir}/salt/cloud.deploy.d
install -dm 755 %{buildroot}%{_sysconfdir}/salt/cloud.maps.d
install -dm 755 %{buildroot}%{_sysconfdir}/salt/cloud.profiles.d
install -dm 755 %{buildroot}%{_sysconfdir}/salt/cloud.providers.d

# Add the config files
install -pm 640 conf/minion %{buildroot}%{_sysconfdir}/salt/minion
install -pm 640 conf/master %{buildroot}%{_sysconfdir}/salt/master
install -pm 640 conf/cloud %{buildroot}%{_sysconfdir}/salt/cloud
install -pm 640 conf/roster %{buildroot}%{_sysconfdir}/salt/roster

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{SOURCE2} %{buildroot}%{_initrddir}/salt-master
install -pm 755 %{SOURCE3} %{buildroot}%{_initrddir}/salt-syndic
install -pm 755 %{SOURCE4} %{buildroot}%{_initrddir}/salt-minion
install -pm 755 %{SOURCE5} %{buildroot}%{_initrddir}/salt-api
%else
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE6} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -pm 644 %{SOURCE9} %{buildroot}%{_unitdir}/
%endif

%if 0%{?rhel} == 6
sed -i 's#/usr/bin/python#/usr/bin/python2.6#g' %{buildroot}%{_bindir}/salt*
sed -i 's#/usr/bin/python#/usr/bin/python2.6#g' %{buildroot}%{_initrddir}/salt*
%endif

install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/bash_completion.d

install -pm 644 %{SOURCE10} .

install -pm 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/salt
install -pm 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/bash_completion.d/salt.bash

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

%preun master
if [[ $1 -eq 0 ]] ; then
  /sbin/service salt-master stop >/dev/null 2>&1
  /sbin/chkconfig --del salt-master
fi

%preun syndic
if [[ $1 -eq 0 ]] ; then
  /sbin/service salt-syndic stop >/dev/null 2>&1
  /sbin/chkconfig --del salt-syndic
fi

%preun minion
if [[ $1 -eq 0 ]] ; then
  /sbin/service salt-minion stop >/dev/null 2>&1
  /sbin/chkconfig --del salt-minion
fi

%post master
if [[ $1 -eq 1 ]] ; then
  /sbin/chkconfig --add salt-master
fi

%post minion
if [[ $1 -eq 1 ]] ; then
  /sbin/chkconfig --add salt-minion
fi

%else

%preun master
%if 0%{?systemd_preun:1}
  %systemd_preun salt-master.service
%else
if [[ $1 -eq 0 ]] ; then
  /bin/systemctl --no-reload disable salt-master.service > /dev/null 2>&1 || :
  /bin/systemctl stop salt-master.service > /dev/null 2>&1 || :
fi
%endif

%preun syndic
%if 0%{?systemd_preun:1}
  %systemd_preun salt-syndic.service
%else
if [[ $1 -eq 0 ]] ; then
  /bin/systemctl --no-reload disable salt-syndic.service > /dev/null 2>&1 || :
  /bin/systemctl stop salt-syndic.service > /dev/null 2>&1 || :
fi
%endif

%preun minion
%if 0%{?systemd_preun:1}
  %systemd_preun salt-minion.service
%else
if [[ $1 -eq 0 ]] ; then
  /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
  /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
fi
%endif

%post master
%if 0%{?systemd_post:1}
  %systemd_post salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post minion
%if 0%{?systemd_post:1}
  %systemd_post salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc README.fedora
%{python_sitelib}/%{name}/*
%{python_sitelib}/%{name}-*-py?.?.egg-info
%{_sysconfdir}/logrotate.d/salt
%{_sysconfdir}/bash_completion.d/salt.bash
%{_var}/cache/salt
%{_bindir}/spm

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7.*
%doc %{_mandir}/man1/salt-cp.1.*
%doc %{_mandir}/man1/salt-key.1.*
%doc %{_mandir}/man1/salt-master.1.*
%doc %{_mandir}/man1/salt-run.1.*
%doc %{_mandir}/man1/salt-unity.1.*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_bindir}/salt-unity
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-master
%else
%{_unitdir}/salt-master.service
%endif
%config(noreplace) %{_sysconfdir}/salt/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1.*
%doc %{_mandir}/man1/salt-minion.1.*
%doc %{_mandir}/man1/salt-proxy.1.*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%{_bindir}/salt-proxy
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-minion
%else
%{_unitdir}/salt-minion.service
%endif
%config(noreplace) %{_sysconfdir}/salt/minion

%files syndic
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-syndic.1.*
%{_bindir}/salt-syndic
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-syndic
%else
%{_unitdir}/salt-syndic.service
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1.*
%{_bindir}/salt-api
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-api
%else
%{_unitdir}/salt-api.service
%endif

%files cloud
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-cloud.1.*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-ssh.1.*
%{_bindir}/salt-ssh
%config(noreplace) %{_sysconfdir}/salt/roster

################################################################################

%changelog
* Mon Oct 22 2015 Gleb Goncharov <inbox@gongled.ru> - 2015.8.1-0
- Updated to 2015.8.1

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
