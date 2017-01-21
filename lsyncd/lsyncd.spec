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

###############################################################################

Summary:              File change monitoring and synchronization daemon
Name:                 lsyncd
Version:              2.2.1
Release:              0%{?dist}
License:              GPLv2+
Group:                Applications/Internet
URL:                  https://github.com/axkibe/lsyncd

Source0:              https://github.com/axkibe/%{name}/archive/release-%{version}.tar.gz
Source1:              %{name}.service
Source2:              %{name}.init
Source3:              %{name}.sysconfig
Source4:              %{name}.logrotate
Source5:              %{name}.conf

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make cmake gcc gcc-c++ lua-devel >= 5.1.3 asciidoc

Requires:             lua rsync

%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(preun):      systemd
Requires(postun):     systemd
%endif

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
Lsyncd watches a local directory trees event monitor interface (inotify).
It aggregates and combines events for a few seconds and then spawns one
(or more) process(es) to synchronize the changes. By default this is
rsync.

Lsyncd is thus a light-weight live mirror solution that is comparatively
easy to install not requiring new file systems or block devices and does
not hamper local file system performance.

###############################################################################

%prep
%setup -qn %{name}-release-%{version}

%build
mkdir build
pushd build
  cmake ..
  make
popd

%install
rm -rf %{buildroot}

pushd build
  %{make_install}
popd

install -dm 755 %{buildroot}%{_loc_mandir}/man1/

mv %{buildroot}%{_loc_prefix}/man/%{name}.1* %{buildroot}%{_loc_mandir}/man1/

install -pDm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pDm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/

%if 0%{?rhel} >= 7
install -pDm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
install -pDm 755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
%endif

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload %{name}.service &>/dev/null || :
  %{__systemctl} preset %{name}.service &>/dev/null || :
%else
  %{__chkconfig} --add %{name} &>/dev/null || :
%endif
fi

%preun
if [[ $1 -eq 0 ]] ; then 
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%else
  %{__service} stop %{name} &>/dev/null || :
%endif
fi 

%postun
if [[ $1 -ge 1 ]] ; then 
%if 0%{?rhel} >= 7
  %{__systemctl} try-restart %{name}.service &>/dev/null || :
%else
  %{__service} restart %{name} &>/dev/null || :
%endif
fi

###############################################################################

%files
%defattr(-, root, root, -)
%doc COPYING ChangeLog examples
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_loc_bindir}/%{name}
%{_loc_mandir}/man1/%{name}.1*
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif

###############################################################################

%changelog
* Tue Jan 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Initial build for kaos-repo
