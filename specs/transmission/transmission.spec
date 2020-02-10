################################################################################

%define _hardened_build   1

%{!?_without_check: %define _with_check 1}

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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define service_user      transmission
%define service_group     transmission
%define service_name      %{name}
%define service_home      %{_sharedstatedir}/%{name}

################################################################################

Summary:            A lightweight GTK+ BitTorrent client
Name:               transmission
Version:            2.94
Release:            1%{?dist}
License:            MIT and GPLv2
Group:              Applications/Internet
URL:                http://www.transmissionbt.com

Source0:            https://github.com/%{name}/%{name}-releases/raw/master/%{name}-%{version}.tar.xz
Source1:            %{name}-gtk.appdata.xml

Patch0:             %{name}-libsystemd.patch
Patch1:             %{name}-fdlimits.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc-c++ openssl-devel >= 1.1.0 glib2-devel >= 2.32.0
BuildRequires:      gtk3-devel >= 3.2.0 libnotify-devel >= 0.4.3
BuildRequires:      libcanberra-devel libcurl-devel >= 7.16.3
BuildRequires:      dbus-glib-devel >= 0.70 libevent-devel >= 2.0.10
BuildRequires:      desktop-file-utils gettext intltool qt5-qtbase-devel
BuildRequires:      systemd-devel libnatpmp-devel >= 20150609-1

Requires:           transmission-gtk

################################################################################

%description
Transmission is a free, lightweight BitTorrent client. It features a
simple, intuitive interface on top on an efficient, cross-platform
back-end.

################################################################################

%package common
Summary:            Transmission common files
Group:              Applications/Internet

Conflicts:          %{name} < 1.80-0.3.b4

%description common
Common files for Transmission BitTorrent client sub-packages. It includes
the web user interface, icons and transmission-remote, transmission-create,
transmission-edit, transmission-show utilities.

################################################################################

%package cli
Summary:            Transmission command line implementation
Group:              Applications/Internet
Requires:           transmission-common

%description cli
Command line version of Transmission BitTorrent client.

################################################################################

%package daemon
Summary:            Transmission daemon
Group:              Applications/Internet
Requires:           transmission-common

BuildRequires:      systemd

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description daemon
Transmission BitTorrent client daemon.

################################################################################

%package gtk
Summary:            Transmission GTK interface
Group:              Applications/Internet
Requires:           transmission-common

%description gtk
GTK graphical interface of Transmission BitTorrent client.

################################################################################

%package qt
Summary:            Transmission Qt interface
Group:              Applications/Internet
Requires:           transmission-common

%description qt
Qt graphical interface of Transmission BitTorrent client.

################################################################################

%prep
%setup -q

%patch0 -p0
%patch1 -p0

# fix icon location for Transmission Qt
sed -i 's|Icon=%{name}-qt|Icon=%{name}|g' qt/%{name}-qt.desktop

# convert to UTF encoding
iconv --from=ISO-8859-1 --to=UTF-8 AUTHORS > AUTHORS.new
mv AUTHORS.new AUTHORS

iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
CXXFLAGS="%{optflags} -fPIC"

%configure --disable-static --enable-utp --enable-daemon --with-systemd-daemon \
           --enable-nls --enable-cli --enable-daemon \
           --enable-external-natpmp

%{__make} %{?_smp_mflags}

pushd qt
  %{qmake_qt5} qtr.pro
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

%{make_install}
%{make_install} INSTALL_ROOT=%{buildroot}%{_prefix} -C qt

%find_lang %{name}-gtk

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gtk.desktop
desktop-file-install \
                --dir=%{buildroot}%{_datadir}/applications/  \
                  qt/%{name}-qt.desktop

install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_sharedstatedir}/%{name}
install -dm 0755 %{buildroot}%{_datadir}/appdata

install -pm 0644 daemon/%{name}-daemon.service  %{buildroot}%{_unitdir}/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/%{name}-gtk.appdata.xml

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

################################################################################

%pre daemon
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{service_group} >/dev/null || %{__groupadd} -o -r %{service_group}
  %{__getent} passwd %{service_user} >/dev/null || \
    %{__useradd} -M -n -o -r -d %{service_home} \
        -s /sbin/nologin -c "transmission daemon-account" %{service_user}
fi

%post daemon
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} daemon-reload %{name}-daemon.service &>/dev/null || :
  %{__systemctl} preset %{name}-daemon.service &>/dev/null || :
fi

%preun daemon
if [[ $1 -eq 0 ]] ; then
  %{__systemctl} --no-reload disable %{name}-daemon.service &>/dev/null || :
  %{__systemctl} stop %{name}-daemon.service &>/dev/null || :
fi

%postun daemon
%systemd_postun_with_restart %{name}-daemon.service

################################################################################

%files
%defattr(-,root,root,-)

%files common
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-create
%{_bindir}/%{name}-edit
%{_bindir}/%{name}-show
%{_datadir}/%{name}/
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%doc %{_mandir}/man1/%{name}-remote*
%doc %{_mandir}/man1/%{name}-create*
%doc %{_mandir}/man1/%{name}-edit*
%doc %{_mandir}/man1/%{name}-show*

%files cli
%defattr(-,root,root,-)
%{_bindir}/%{name}-cli
%doc %{_mandir}/man1/%{name}-cli*

%files daemon
%defattr(-,root,root,-)
%{_bindir}/%{name}-daemon
%{_unitdir}/%{name}-daemon.service
%attr(-,%{service_user},%{service_group})%{service_home}
%doc %{_mandir}/man1/%{name}-daemon*

%files gtk -f %{name}-gtk.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}-gtk
%{_datadir}/appdata/%{name}-gtk.appdata.xml
%{_datadir}/applications/%{name}-gtk.desktop
%doc %{_mandir}/man1/%{name}-gtk.*

%files qt
%defattr(-,root,root,-)
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%doc %{_mandir}/man1/%{name}-qt.*

################################################################################

%changelog
* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 2.94-1
- Rebuilt with the latest version of libevent

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 2.94-0
- Fix building against LibreSSL
- Fix building against mbedTLS
- Fix torrents ETA calculation
- Fix cross-compilation issues caused by miniupnpc configuration test
- Fix bad downloaded percentage in DetailsDialog
- Fix tracker error XSS in inspector
- Fix torrent name HTML-escaping in trackers inspector tab

* Sun Feb 11 2018 Gleb Goncharov <inbox@gongled.ru> - 2.93-0
- Initial build
