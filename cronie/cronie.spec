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
%define _spooldir         %{_localstatedir}/spool
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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig

%define service_name      crond

###############################################################################

%bcond_without selinux
%bcond_without pam
%bcond_without audit
%bcond_without inotify

###############################################################################

Summary:           Cron daemon for executing programs at set times
Name:              cronie
Version:           1.5.1
Release:           0%{?dist}
License:           MIT and BSD and ISC and GPLv2
Group:             System Environment/Base
URL:               https://fedorahosted.org/cronie

Source:            https://fedorahosted.org/releases/c/r/%{name}/%{name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          syslog bash >= 2.0
BuildRequires:     make gcc sed

Conflicts:         sysklogd < 1.4.1
Provides:          vixie-cron = 4.4
Obsoletes:         vixie-cron <= 4.3
Requires:          dailyjobs

%if %{with selinux}
Requires:          libselinux >= 2.0.64
BuildRequires:     libselinux-devel >= 2.0.64
%endif
%if %{with pam}
Requires:          pam >= 1.0.1
BuildRequires:     pam-devel >= 1.0.1
%endif
%if %{with audit}
BuildRequires:     audit-libs-devel >= 1.4.1
%endif

Requires(post):    coreutils sed

###############################################################################

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

###############################################################################

%package anacron
Summary:           Utility for running regular jobs
Requires:          crontabs
Group:             System Environment/Base
Provides:          dailyjobs = %{version}-%{release}
Provides:          anacron = 2.4
Obsoletes:         anacron <= 2.3
Requires(post):    coreutils
Requires:          %{name} = %{version}-%{release}

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

###############################################################################

%package noanacron
Summary:           Utility for running simple regular jobs in old cron style
Group:             System Environment/Base
Provides:          dailyjobs = %{version}-%{release}
Requires:          crontabs
Requires:          %{name} = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

###############################################################################

%prep
%setup -q

%build
%configure \
%if %{with pam}
--with-pam \
%endif
%if %{with selinux}
--with-selinux \
%endif
%if %{with audit}
--with-audit \
%endif
%if %{with inotify}
--with-inotify \
%endif
--enable-anacron \
--enable-pie \
--enable-relro

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install} DESTMAN=%{buildroot}%{_mandir}

%{__install} -dm 700 %{buildroot}%{_localstatedir}/spool/cron
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/sysconfig/
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/cron.d/

%if ! %{with pam}
  %{__rm} -f %{buildroot}%{_sysconfdir}/pam.d/%{service_name}
%endif

%{__install} -pm 644 %{service_name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{service_name}

%{__touch} %{buildroot}%{_sysconfdir}/cron.deny

%{__install} -pm 644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab
%{__install} -cm 755 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly

%{__mkdir_p} -m 755 %{buildroot}%{_sysconfdir}/cron.hourly

%{__install} -cm 755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron

%{__mkdir_p} %{buildroot}%{_spooldir}/anacron

%{__touch} %{buildroot}%{_spooldir}/anacron/cron.daily
%{__touch} %{buildroot}%{_spooldir}/anacron/cron.weekly
%{__touch} %{buildroot}%{_spooldir}/anacron/cron.monthly

# noanacron package
%{__install} -pm 644 contrib/dailyjobs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/dailyjobs

# install sysvinit initscript into sub-package
%{__mkdir_p} -m 755 %{buildroot}%{_initrddir}
%{__install} -pm 755 %{name}.init %{buildroot}%{_initrddir}/%{service_name}

%clean
%{__rm} -rf %{buildroot}

%post
%{__chkconfig} --add %{service_name}

%post anacron
[[ -e %{_spooldir}/anacron/cron.daily ]] || %{__touch} %{_spooldir}/anacron/cron.daily
[[ -e %{_spooldir}/anacron/cron.weekly ]] || %{__touch} %{_spooldir}/anacron/cron.weekly
[[ -e %{_spooldir}/anacron/cron.monthly ]] || %{__touch} %{_spooldir}/anacron/cron.monthly


%postun
if [[ $1 -ge 1 ]]; then
  %{__service} %{service_name} condrestart >/dev/null 2>&1 || :
fi

if [[ $1 -eq 1 ]] ; then
  %{__service} %{service_name} stop >/dev/null 2>&1 || :
  %{__chkconfig} --del %{service_name}
fi

%triggerun -- %{name} < 1.4.1
%{__cp} -a %{_sysconfdir}/crontab %{_sysconfdir}/crontab.rpmsave
%{__sed} -e '/^01 \* \* \* \* root run-parts \/etc\/cron\.hourly/d'\
  -e '/^02 4 \* \* \* root run-parts \/etc\/cron\.daily/d'\
  -e '/^22 4 \* \* 0 root run-parts \/etc\/cron\.weekly/d'\
  -e '/^42 4 1 \* \* root run-parts \/etc\/cron\.monthly/d' %{_sysconfdir}/crontab.rpmsave > %{_sysconfdir}/crontab
exit 0

%triggerun -- vixie-cron
%{__cp} -a %{_lockdir}/subsys/%{service_name} %{_lockdir}/subsys/%{name} > /dev/null 2>&1 || :

%triggerpostun -- vixie-cron
%{__chkconfig} --add %{service_name}
[[ -f %{_lockdir}/subsys/%{name} ]] && ( rm -f %{_lockdir}/subsys/%{name} ; %{__service} %{service_name} restart ) > /dev/null 2>&1 || :

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README ChangeLog
%attr(755,root,root) %{_sbindir}/%{service_name}
%attr(4755,root,root) %{_bindir}/crontab
%{_mandir}/man8/%{service_name}.*
%{_mandir}/man8/cron.*
%{_mandir}/man5/crontab.*
%{_mandir}/man1/crontab.*
%dir %{_localstatedir}/spool/cron
%dir %{_sysconfdir}/cron.d
%{_initrddir}/%{service_name}
%if %{with pam}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{service_name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%config(noreplace) %{_sysconfdir}/cron.deny
%attr(0644,root,root) %{_sysconfdir}/cron.d/0hourly

%files anacron
%defattr(-,root,root,-)
%{_sbindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir %{_spooldir}/anacron
%ghost %verify(not md5 size mtime) %{_spooldir}/anacron/cron.daily
%ghost %verify(not md5 size mtime) %{_spooldir}/anacron/cron.weekly
%ghost %verify(not md5 size mtime) %{_spooldir}/anacron/cron.monthly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%defattr(-,root,root,-)
%attr(0644,root,root) %{_sysconfdir}/cron.d/dailyjobs

###############################################################################

%changelog
* Tue Jul 26 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- crontab: Use temporary file name that is ignored by crond.
- crond: Inherit PATH from the crond environment if -P option is used.
- crond: Remove hardcoded "system_u" SELinux user, use the SELinux user of
  the running crond.
- anacron: Small cleanups and fixes.
- crond: Fix longstanding race condition on repeated crontab modification.

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- crond: Job environment variables are set also when executing sendmail.
- crond: Adding duplicate orphans on reload is now prevented.
- crond: The regular crond shutdown is now logged.
- crontab: PAM is not called in crontab command if the caller's uid is 0.
- crond: PAM is not called from crond for system cron jobs
  (/etc/crontab, /etc/cron.d) which are run for uid 0.
- crond: The existence of an user is checked at time when job is run
  and not when the crontab is parsed on database reload.

* Thu Oct 23 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.12-0
- Updated to latest stable release

* Wed Jan 15 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.11-0
- Updated to latest stable release

* Tue Oct 29 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-11
- Rewrited spec from Fedora package
