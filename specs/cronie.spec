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
Version:         1.7.0
Release:         0%{?dist}
License:         MIT and BSD and ISC and GPLv2
Group:           System Environment/Base
URL:             https://github.com/cronie-crond/cronie

Source0:         https://github.com/cronie-crond/cronie/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc sed systemd

Requires:        dailyjobs systemd

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
Provides:        %{service_name} = %{version}-%{release}

################################################################################

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

################################################################################

%package anacron
Summary:   Utility for running regular jobs
Group:     System Environment/Base

Requires:        crontabs
Requires:        %{name} = %{version}-%{release}
Requires(post):  coreutils

Provides:  dailyjobs = %{version}-%{release}
Provides:  anacron = 2.4

Obsoletes:  anacron <= 2.3

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
Summary:  Utility for running simple regular jobs in old cron style
Group:    System Environment/Base

Requires:  crontabs
Requires:  %{name} = %{version}-%{release}

Provides:  dailyjobs = %{version}-%{release}

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

%{make_build} V=2

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

touch %{buildroot}%{_sysconfdir}/cron.deny

install -pm 644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab
install -pm 644 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly

install -dm 755 %{buildroot}%{_sysconfdir}/cron.hourly

install -pm 755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron

install -dm 755 %{buildroot}%{_localstatedir}/spool/anacron

touch %{buildroot}%{_localstatedir}/spool/anacron/cron.daily
touch %{buildroot}%{_localstatedir}/spool/anacron/cron.weekly
touch %{buildroot}%{_localstatedir}/spool/anacron/cron.monthly

# noanacron package
install -pm 644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

# install systemd service
install -dm 755 %{buildroot}%{_unitdir}
install -pm 644 contrib/%{name}.systemd %{buildroot}%{_unitdir}/%{service_name}.service

%clean
rm -rf %{buildroot}

%post
if [[ -f "%{_rundir}/%{service_name}.pid" ]] ; then
  rm -f %{_rundir}/%{service_name}.pid
fi

if [[ $1 -eq 1 ]] ; then
  systemctl enable %{service_name}.service &>/dev/null || :
fi

systemctl daemon-reload &>/dev/null || :

%preun
if [[ $1 -eq 0 ]]; then
  systemctl --no-reload disable %{service_name}.service &>/dev/null || :
  systemctl stop %{service_name}.service &>/dev/null || :
fi

%postun
systemctl daemon-reload &>/dev/null || :

if [[ $1 -ge 1 ]] ; then
  systemctl try-restart &>/dev/null || :
fi

%post anacron
[[ -e %{_localstatedir}/spool/anacron/cron.daily ]] || touch %{_localstatedir}/spool/anacron/cron.daily
[[ -e %{_localstatedir}/spool/anacron/cron.weekly ]] || touch %{_localstatedir}/spool/anacron/cron.weekly
[[ -e %{_localstatedir}/spool/anacron/cron.monthly ]] || touch %{_localstatedir}/spool/anacron/cron.monthly

%triggerin -- pam, glibc
# changes in pam, glibc or libselinux can make crond crash when it calls pam
systemctl try-restart %{service_name}.service &>/dev/null || :

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
%if %{with pam}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{service_name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%config(noreplace) %{_sysconfdir}/cron.deny
%{_sysconfdir}/cron.d/0hourly
%{_unitdir}/%{service_name}.service

%files anacron
%defattr(-,root,root,-)
%{_sbindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir %{_localstatedir}/spool/anacron
%ghost %verify(not md5 size mtime) %{_localstatedir}/spool/anacron/cron.daily
%ghost %verify(not md5 size mtime) %{_localstatedir}/spool/anacron/cron.weekly
%ghost %verify(not md5 size mtime) %{_localstatedir}/spool/anacron/cron.monthly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%defattr(-,root,root,-)
%attr(0644,root,root) %{_sysconfdir}/cron.d/dailyjobs

################################################################################

%changelog
* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- https://github.com/cronie-crond/cronie/releases/tag/cronie-1.7.0

* Mon Oct 09 2023 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Spec refactoring

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
