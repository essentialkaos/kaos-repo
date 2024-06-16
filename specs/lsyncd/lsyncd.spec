################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __systemctl  %{_bindir}/systemctl

################################################################################

Summary:        File change monitoring and synchronization daemon
Name:           lsyncd
Version:        2.3.1
Release:        1%{?dist}
License:        GPL-2.0-or-later AND CC-BY-3.0
Group:          Applications/Internet
URL:            https://github.com/axkibe/lsyncd

Source0:        https://github.com/lsyncd/lsyncd/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.sysconfig
Source3:        %{name}.logrotate
Source4:        %{name}.conf
Source5:        %{name}.sysctl

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ asciidoc

%if 0%{?rhel} <= 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif

%if 0%{?rhel} >= 9
BuildRequires:  lua-devel <= 5.4.2
%else
BuildRequires:  lua-devel
%endif

Requires:       lua rsync >= 3.1.0 systemd

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Lsyncd watches a local directory trees event monitor interface (inotify).
It aggregates and combines events for a few seconds and then spawns one
(or more) process(es) to synchronize the changes. By default this is
rsync.

Lsyncd is thus a light-weight live mirror solution that is comparatively
easy to install not requiring new file systems or block devices and does
not hamper local file system performance.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
mkdir build
pushd build
  cmake3 .. -DCMAKE_INSTALL_PREFIX:PATH=%{_usr}
  %{make_build}
popd

%install
rm -rf %{buildroot}

pushd build
  %{make_install}
popd

install -dm 755 %{buildroot}%{_mandir}/man1/
install -pm 644 docs/manpage/%{name}.1 %{buildroot}%{_mandir}/man1/

install -pDm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pDm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/
install -pDm 644 %{SOURCE5} %{buildroot}%{_sysctldir}/50-lsyncd.conf

install -pDm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

rm -rf %{buildroot}/man1
rm -rf %{buildroot}%{_prefix}/doc/examples

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} daemon-reload %{name}.service &>/dev/null || :
  %{__systemctl} preset %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  %{__systemctl} try-restart %{name}.service &>/dev/null || :
fi

################################################################################

%files
%defattr(-, root, root, -)
%doc COPYING ChangeLog examples
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysctldir}/50-lsyncd.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_unitdir}/%{name}.service

################################################################################

%changelog
* Wed May 08 2024 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-1
- Fixed path to binary in service file
- Added sysctl configuration
- Updated sysconfig

* Wed Dec 14 2022 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- https://github.com/lsyncd/lsyncd/releases/tag/v2.3.1

* Wed Dec 14 2022 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- https://github.com/lsyncd/lsyncd/releases/tag/v2.3.0

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-2
- Improved init script
- Added CRC check for all sources

* Mon Aug 28 2017 Gleb Goncharov <inbox@gongled.ru> - 2.2.2-1
- Fixed invalid path to binary in systemd unit file

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-0
- Updated to latest stable release

* Wed Feb 15 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-1
- Fixed rsync version in dependencies
- Init script migrated to kaosv

* Tue Jan 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Initial build for kaos-repo
