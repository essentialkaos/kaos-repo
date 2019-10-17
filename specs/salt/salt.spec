################################################################################

%if 0%{?rhel} >= 7
%global python_base python36
%global __python3   %{_bindir}/python3.6
%else
%global python_base python34
%global __python3   %{_bindir}/python3.4
%endif

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

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
%define __sysctl          %{_bindir}/systemctl

################################################################################

Summary:          A parallel remote execution system
Name:             salt
Version:          2019.2.1
Release:          0%{?dist}
License:          ASL 2.0
Group:            System Environment/Daemons
URL:              https://github.com/saltstack/salt

Source0:          https://github.com/saltstack/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
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
Source11:         %{name}.logrotate
Source12:         salt.bash

Patch0:           %{name}-config.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    %{python_base}-devel git
BuildRequires:    %{python_base}-crypto %{python_base}-jinja2 %{python_base}-mock
BuildRequires:    %{python_base}-zmq %{python_base}-pip %{python_base}-zmq
BuildRequires:    %{python_base}-PyYAML %{python_base}-requests
BuildRequires:    %{python_base}-requests %{python_base}-six %{python_base}-backports_abc
BuildRequires:    %{python_base}-backports-ssl_match_hostname
BuildRequires:    %{python_base}-tornado < 5.0
Requires:         %{python_base}-msgpack >= 0.5

Requires:         dmidecode pciutils which yum-utils
Requires:         %{python_base} %{python_base}-crypto %{python_base}-jinja2
Requires:         %{python_base}-libcloud %{python_base}-zmq %{python_base}-PyYAML
Requires:         %{python_base}-requests %{python_base}-six
Requires:         %{python_base}-backports_abc %{python_base}-markupsafe
Requires:         %{python_base}-backports-ssl_match_hostname
Requires:         %{python_base}-tornado < 5.0
Requires:         %{python_base}-msgpack >= 0.5

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires:         kaosv >= 2.15
%else
Requires:         systemd
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

Provides:         %{name} = %{version}-%{release}

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
Requires:         %{python_base}-cherrypy

%description api
salt-api provides a REST interface to the Salt master.

################################################################################

%package cloud
Summary:          Cloud provisioner for Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name}-master = %{version}-%{release}
Requires:         %{python_base}-libcloud

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

################################################################################

%package ssh
Summary:          Agentless SSH-based version of Salt, a parallel remote execution system
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

################################################################################

%package package-manager
Summary:          Salt Package Manager
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}

%description package-manager
The Salt Package Manager, or SPM, enables Salt formulas to be packaged to
simplify distribution to Salt masters. The design of SPM was influenced by
other existing packaging systems including RPM, Yum, and Pacman.

################################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p1

%build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --root %{buildroot}

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

install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{_sysconfdir}/bash_completion.d

install -pm 644 %{SOURCE10} .

install -pm 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/salt
install -pm 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/bash_completion.d/salt.bash

%clean
rm -rf %{buildroot}

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

%preun master
if [[ $1 -eq 0 ]] ; then
  %{__service} salt-master stop &>/dev/null || :
  %{__chkconfig} --del salt-master
fi

%preun syndic
if [[ $1 -eq 0 ]] ; then
  %{__service} salt-syndic stop &>/dev/null || :
  %{__chkconfig} --del salt-syndic
fi

%preun minion
if [[ $1 -eq 0 ]] ; then
  %{__service} salt-minion stop &>/dev/null || :
  %{__chkconfig} --del salt-minion
fi

%post master
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add salt-master
fi

if [[ $1 -eq 2 ]] ; then
  %{__service} salt-master restart &>/dev/null || :
fi

%post minion
if [[ $1 -eq 1 ]] ; then
  %{__chkconfig} --add salt-minion
fi

if [[ $1 -eq 2 ]] ; then
  %{__service} salt-minion restart &>/dev/null || :
fi

%else

%preun master
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable salt-master.service &>/dev/null || :
  %{__sysctl} stop salt-master.service &>/dev/null || :
fi

%preun syndic
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable salt-syndic.service &>/dev/null || :
  %{__sysctl} stop salt-syndic.service &>/dev/null || :
fi

%preun minion
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable salt-minion.service &>/dev/null || :
  %{__sysctl} stop salt-minion.service &>/dev/null || :
fi

%post master
if [[ $1 -eq 1 ]] ; then
%{__sysctl} preset salt-master.service &>/dev/null || :
fi

if [[ $1 -eq 2 ]] ; then
%{__sysctl} daemon-reload &>/dev/null || :
%{__sysctl} restart salt-master.service &>/dev/null || :
fi

%post minion
if [[ $1 -eq 1 ]] ; then
%{__sysctl} preset salt-minion.service &>/dev/null || :
fi

if [[ $1 -eq 2 ]] ; then
%{__sysctl} daemon-reload &>/dev/null || :
%{__sysctl} restart salt-minion.service &>/dev/null || :
fi

%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc README.fedora
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/%{name}-*-py?.?.egg-info
%{_sysconfdir}/logrotate.d/salt
%{_sysconfdir}/bash_completion.d/salt.bash
%{_var}/cache/salt

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7.*
%doc %{_mandir}/man1/salt.1.*
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

%files package-manager
%defattr(-,root,root)
%{_mandir}/man1/spm.1.*
%{_bindir}/spm

################################################################################

%changelog
* Wed Oct 16 2019 Andrey Kulikov <avk@brewkeeper.net> - 2019.2.1-0
- Updated to 2019.2.1

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2018.3.3-1
- Updated for compatibility with Python 3.6

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.3.3-0
- Updated to 2018.3.3

* Wed Jul 11 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.3.2-1
- Fixed supported versions of python34-tornado

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.3.2-0
- Updated to 2018.3.2

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2018.3.1-0
- Updated to 2018.3.1

* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2017.7.3-1
- Updated to 2017.7.3
- Rebuilt for Python 3.4 usage

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.7.2-0
- Updated to 2017.7.2

* Mon Sep 25 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.7.1-2
- Improved spec

* Thu Sep 21 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.7.1-1
- Improved logging settings

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2017.7.1-0
- Updated to 2017.7.1

* Sat Jun 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2016.11.5-1
- Fixed compatibility with latest version of python-tornado

* Fri May 19 2017 Anton Novojilov <andy@essentialkaos.com> - 2016.11.5-0
- Updated to 2016.11.5
- Fixed logrotate config

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2016.11.4-0
- Updated to 2016.11.4

* Fri Mar 31 2017 Anton Novojilov <andy@essentialkaos.com> - 2016.11.3-1
- Updated to 2016.11.3
- Improved spec

* Thu Dec 01 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.11.0-0
- Updated to 2016.11.0

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.3.4-0
- Updated to 2016.3.4

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.3.3-0
- Updated to 2016.3.3

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 2016.3.1-0
- Updated to 2016.3.1

* Wed Apr 06 2016 Gleb Goncharov <yum@gongled.ru> - 2015.8.8-0
- Updated to 2015.8.8

* Mon Feb 15 2016 Gleb Goncharov <yum@gongled.ru> - 2015.8.5-0
- Updated to 2015.8.5

* Thu Oct 22 2015 Gleb Goncharov <yum@gongled.ru> - 2015.8.1-0
- Updated to 2015.8.1

* Mon Sep 21 2015 Gleb Goncharov <yum@gongled.ru> - 2015.8.0-0
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
