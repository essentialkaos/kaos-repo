################################################################################

# rpmbuilder:github       karlheyes:icecast-kh
# rpmbuilder:tag          icecast-2.4.0-kh13

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
Release:           0%{?dist}
License:           GPLv2+ and GPLv2 and BSD
Group:             Applications/Multimedia
URL:               https://github.com/karlheyes/icecast-kh

Source0:           %{name}-%{version}.tar.bz2
Source1:           %{name}.service
Source2:           %{name}.logrotate
Source3:           %{name}.xml

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

cp -a html/ AUTHORS NEWS TODO %{buildroot}%{_pkgdocdir}
cp -a conf/*.dist %{buildroot}%{_pkgdocdir}/conf

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
* Fri May 29 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh14-0
- Updated to the latest stable release
- Fixed bug with logs rotation

* Wed Apr 01 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh13-0
- Updated to the latest stable release

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh12-0
- Updated to the latest stable release

* Sun Jan 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-10
- Initial build for kaos repository
