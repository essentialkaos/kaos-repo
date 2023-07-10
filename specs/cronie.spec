################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define service_name  crond

################################################################################

%bcond_without  selinux
%bcond_without  pam
%bcond_without  audit
%bcond_without  inotify

################################################################################

Summary:         Cron daemon for executing programs at set times
Name:            cronie
Version:         1.6.1
Release:         0%{?dist}
License:         MIT and BSD and ISC and GPLv2
Group:           System Environment/Base
URL:             https://github.com/cronie-crond/cronie

Source0:         https://github.com/cronie-crond/cronie/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        syslog bash
BuildRequires:   make gcc sed

Conflicts:       sysklogd < 1.4.1
Provides:        vixie-cron = 4.4
Obsoletes:       vixie-cron <= 4.3
Requires:        dailyjobs

%if %{with selinux}
Requires:        libselinux >= 2.0.64
BuildRequires:   libselinux-devel >= 2.0.64
%endif
%if %{with pam}
Requires:        pam >= 1.0.1
BuildRequires:   pam-devel >= 1.0.1
%endif
%if %{with audit}
BuildRequires:   audit-libs-devel >= 1.4.1
%endif

Requires(post):  coreutils sed

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

################################################################################

%package anacron
Summary:         Utility for running regular jobs
Requires:        crontabs
Group:           System Environment/Base
Provides:        dailyjobs = %{version}-%{release}
Provides:        anacron = 2.4
Obsoletes:       anacron <= 2.3
Requires(post):  coreutils
Requires:        %{name} = %{version}-%{release}

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

################################################################################

%package noanacron
Summary:   Utility for running simple regular jobs in old cron style
Group:     System Environment/Base
Provides:  dailyjobs = %{version}-%{release}
Requires:  crontabs
Requires:  %{name} = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

################################################################################

%prep
%{crc_check}

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
rm -rf %{buildroot}

%{make_install} DESTMAN=%{buildroot}%{_mandir}

install -dm 700 %{buildroot}%{_localstatedir}/spool/cron
install -dm 755 %{buildroot}%{_sysconfdir}/sysconfig/
install -dm 755 %{buildroot}%{_sysconfdir}/cron.d/

%if ! %{with pam}
  rm -f %{buildroot}%{_sysconfdir}/pam.d/%{service_name}
%endif

install -pm 644 %{service_name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{service_name}

%{__touch} %{buildroot}%{_sysconfdir}/cron.deny

install -pm 644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab
install -pm 755 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly

install -dm 755 %{buildroot}%{_sysconfdir}/cron.hourly

install -pm 755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron

install -dm 755 %{buildroot}%{_spooldir}/anacron

%{__touch} %{buildroot}%{_spooldir}/anacron/cron.daily
%{__touch} %{buildroot}%{_spooldir}/anacron/cron.weekly
%{__touch} %{buildroot}%{_spooldir}/anacron/cron.monthly

# noanacron package
install -pm 644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

# install sysvinit initscript into sub-package
install -dm 755 %{buildroot}%{_initrddir}
install -pm 755 %{name}.init %{buildroot}%{_initrddir}/%{service_name}

%clean
rm -rf %{buildroot}

%post
# always try to add service to chkconfig
%{__chkconfig} --add %{service_name}

%post anacron
[[ -e %{_spooldir}/anacron/cron.daily ]] || %{__touch} %{_spooldir}/anacron/cron.daily
[[ -e %{_spooldir}/anacron/cron.weekly ]] || %{__touch} %{_spooldir}/anacron/cron.weekly
[[ -e %{_spooldir}/anacron/cron.monthly ]] || %{__touch} %{_spooldir}/anacron/cron.monthly

%postun
if [[ $1 -ge 1 ]]; then
  %{__service} %{service_name} condrestart &>/dev/null || :
fi

if [[ $1 -eq 0 ]] ; then
  %{__service} %{service_name} stop &>/dev/null || :
  %{__chkconfig} --del %{service_name}
fi

%triggerun -- %{name} < 1.4.1
cp -a %{_sysconfdir}/crontab %{_sysconfdir}/crontab.rpmsave

# perfecto:ignore 4
sed -e '/^01 \* \* \* \* root run-parts \/etc\/cron\.hourly/d' \
  -e '/^02 4 \* \* \* root run-parts \/etc\/cron\.daily/d' \
  -e '/^22 4 \* \* 0 root run-parts \/etc\/cron\.weekly/d' \
  -e '/^42 4 1 \* \* root run-parts \/etc\/cron\.monthly/d' \
     %{_sysconfdir}/crontab.rpmsave > %{_sysconfdir}/crontab
exit 0

%triggerun -- vixie-cron
cp -a %{_lockdir}/subsys/%{service_name} %{_lockdir}/subsys/%{name} &>/dev/null || :

%triggerpostun -- vixie-cron
%{__chkconfig} --add %{service_name}
[[ -f %{_lockdir}/subsys/%{name} ]] && ( rm -f %{_lockdir}/subsys/%{name} ; %{__service} %{service_name} restart ) &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README ChangeLog
%attr(0755,root,root) %{_sbindir}/%{service_name}
%attr(4755,root,root) %{_bindir}/crontab
%attr(755,root,root) %{_bindir}/cronnext
%{_mandir}/man8/%{service_name}.*
%{_mandir}/man8/cron.*
%{_mandir}/man5/crontab.*
%{_mandir}/man1/cronnext.*
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

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.6.1

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.5

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.4

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.3

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.2

* Mon Oct 03 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-2
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.1

* Tue Jul 26 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.1

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.5.0

* Thu Oct 23 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.12-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.4.12

* Wed Jan 15 2014 Anton Novojilov <andy@essentialkaos.com> - 1.4.11-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.4.11

* Tue Oct 29 2013 Anton Novojilov <andy@essentialkaos.com> - 1.4.8-11
- Initial build
