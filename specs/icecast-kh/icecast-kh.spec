################################################################################

# rpmbuilder:github       karlheyes:icecast-kh
# rpmbuilder:tag          icecast-2.4.0-kh14

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _docdir           %{_datadir}/doc
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

################################################################################

%define username          icecast
%define groupname         icecast

%define service_name      icecast
%define kh_version        14

################################################################################

Summary:           Icecast streaming media server (KH branch)
Name:              icecast
Version:           2.4.0.kh%{kh_version}
Release:           1%{?dist}
License:           GPLv2+ and GPLv2 and BSD
Group:             Applications/Multimedia
URL:               https://github.com/karlheyes/icecast-kh

Source0:           %{name}-%{version}.tar.bz2
Source1:           %{name}.service
Source2:           %{name}.logrotate
Source3:           %{name}.xml
Source4:           json.xsl

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc coreutils automake libtool
BuildRequires:     curl-devel libogg-devel libtheora-devel libvorbis-devel
BuildRequires:     libxml2-devel libxslt-devel speex-devel openssl-devel

Requires:          libogg libtheora libvorbis libxml2 libxslt speex openssl

Requires(pre):     shadow-utils

BuildRequires:     systemd
Requires:          systemd

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Icecast is a streaming media server which currently supports
Ogg Vorbis and MP3 audio streams.  It can be used to create an
Internet radio station or a privately running jukebox and many
things in between.  It is very versatile in that new formats
can be added relatively easily and supports open standards for
communication and interaction.

################################################################################

%package doc

Summary:           Documentation files for Icecast
License:           GPLv2+ and MIT and FSFULLR and FSFUL
Group:             Applications/Multimedia

BuildArch:         noarch

%description doc
This package contains the documentation files for Icecast.

################################################################################

%prep
%setup -q

find doc/ -type f | xargs chmod 0644
cp -a doc/ html/
find html/ -name 'Makefile*' | xargs rm -f

%build
autoreconf -f -i
%configure --with-curl \
           --with-ogg \
           --with-openssl \
           --with-speex \
           --with-theora \
           --with-vorbis \
           --enable-largefile \
           --enable-maintainer-mode \
           --enable-shared \
           --enable-yp \
           --disable-silent-rules \
           --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_datadir}/%{name}/doc
rm -rf %{buildroot}%{_docdir}/%{name}

install -dm 755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 755 %{buildroot}%{_localstatedir}/run/%{name}
install -dm 755 %{buildroot}%{_pkgdocdir}/examples
install -dm 755 %{buildroot}%{_pkgdocdir}/conf
install -dm 755 %{buildroot}%{_rundir}/%{name}

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

install -Dpm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -Dpm 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.xml

install -Dpm 0644 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/web/

cp -a html/ AUTHORS NEWS TODO %{buildroot}%{_pkgdocdir}
cp -a conf/*.dist %{buildroot}%{_pkgdocdir}/conf

# Remove useless templates
rm -f %{buildroot}%{_datadir}/%{name}/7.xsl
rm -f %{buildroot}%{_datadir}/%{name}/status2.xsl

%clean
rm -rf %{buildroot}

################################################################################

%pre
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{groupname} &>/dev/null || %{__groupadd} -r %{groupname}
  %{__getent} passwd %{username} &>/dev/null || %{__useradd} -r -g %{groupname} -d %{_datadir}/%{name} -s /sbin/nologin %{username}
fi

%post
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} daemon-reload %{service_name}.service &>/dev/null || :
  %{__systemctl} preset %{service_name}.service &>/dev/null || :
fi

%postun
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{service_name}.service &>/dev/null || :
  %{__systemctl} stop %{service_name}.service &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%dir %attr(-,%{username},%{groupname}) %{_localstatedir}/log/%{name}
%dir %attr(-,%{username},%{groupname}) %{_rundir}/%{name}
%config(noreplace) %attr(-,root,%{groupname}) %{_sysconfdir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_unitdir}/%{name}.service

%files doc
%defattr(-,root,root,-)
%doc %{_pkgdocdir}

################################################################################

%changelog
* Fri Jun 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh14-1
- Added xsl template for generating JSON with tracks info

* Fri May 29 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh14-0
- Fixed bug with logs rotation.
- Allow for using secs (eg 5s) in queue/min-queue/burst measures.
- Allow multiple icy sources on same port. Just embed in password a
  mountpoint:pass. The shoutcast-mount tag still creates the +1 port and sets
  a default mountpoint but source can override this.
- Fix log issue which could cause a deadlock if on-[dis]connect or auth cmd
  are used.
- Allow configure to accept ICY_CHARSET to set alternate in build. The default
  ICY metadata is assumed to be UTF8, but some sites still have issues with
  setting tags or parameters, so allow a different default if they need it.
- Regression on FLV wrapped aac metadata fixed.
- Crash/corruption fix if using stream auth and metadata updates via admin.
- Fix for glibc rwlock priority.
- Added the icy-metadata in headers allowed with CORS.
- Rework XFF to be earlier, useful in cases where banned IPs apply.
- Allow wildcards in XFF.
- Drop the BSD NOPUSH setting for now. Have seen poor performance because of
  it in certain cases.
- Openssl API cleanups. eg API differences between versions.
- Various small fixes, build and operational.

* Wed Apr 01 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh13-0
- Fix an annoying race case. memory corruption in certain cases that are hard
  to trigger normally but typically involes a listener disconnecting in certain
  conditions.
- Tightened up use-after-free cases with regard to the queue pruning.
- Leak fixes with intro via auth.
- Allow seconds to be specified in burst and queue size fields. Just specify
  the number followed by s eg 30s or 5s. Eventually we could make this the
  default so that is can apply to various bitrates.
- Small minor cleanups across the board.

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh12-0
- Fix up some incorrect or stale block cases from previous release for non-ogg
  streams. Usually cause by short write triggers or queue jumps.
- Change default charset for non-ogg streams to utf8 instead of latin1, you can
  still use latin1 either with <charset> mount setting or charset= query param
  to metadata.
- Global listeners count could get messed up with fallback to files, also make
  it a regular update stat in-line with other global stats.
- Avoid possible crash case on log re-opening, not so common.

* Sun Jan 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-10
- Initial build for kaos repository
