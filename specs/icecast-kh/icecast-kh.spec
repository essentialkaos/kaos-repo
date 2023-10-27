################################################################################

# rpmbuilder:github       karlheyes:icecast-kh
# rpmbuilder:tag          icecast-2.4.0-kh22

################################################################################

%define username   icecast
%define groupname  icecast

%define service_name  icecast
%define kh_version    22

################################################################################

Summary:        Icecast streaming media server (KH branch)
Name:           icecast
Version:        2.4.0.kh%{kh_version}
Release:        0%{?dist}
License:        GPLv2+ and GPLv2 and BSD
Group:          Applications/Multimedia
URL:            https://github.com/karlheyes/icecast-kh

Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.service
Source2:        %{name}.logrotate
Source3:        %{name}.xml
Source4:        json.xsl

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc coreutils autoconf >= 2.71 automake libtool
BuildRequires:  curl-devel libogg-devel libtheora-devel libvorbis-devel
BuildRequires:  libxml2-devel libxslt-devel speex-devel openssl-devel

Requires:       libogg libtheora libvorbis libxml2 libxslt speex openssl

Requires(pre):  shadow-utils

BuildRequires:  systemd
Requires:       systemd

Provides:       %{name} = %{version}-%{release}

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

Summary:  Documentation files for Icecast
License:  GPLv2+ and MIT and FSFULLR and FSFUL
Group:    Applications/Multimedia

BuildArch:  noarch

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
  getent group %{groupname} &>/dev/null || groupadd -r %{groupname}
  getent passwd %{username} &>/dev/null || useradd -r -g %{groupname} -d %{_datadir}/%{name} -s /sbin/nologin %{username}
fi

%post
if [[ $1 -eq 1 ]] ; then
  systemctl daemon-reload %{service_name}.service &>/dev/null || :
  systemctl preset %{service_name}.service &>/dev/null || :
fi

%postun
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable %{service_name}.service &>/dev/null || :
  systemctl stop %{service_name}.service &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%dir %attr(-,%{username},%{groupname}) %{_localstatedir}/log/%{name}
%dir %attr(-,%{username},%{groupname}) %{_localstatedir}/run/%{name}
%config(noreplace) %attr(-,root,%{groupname}) %{_sysconfdir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%{_datadir}/%{name}

%files doc
%defattr(-,root,root,-)
%doc %{_pkgdocdir}

################################################################################

%changelog
* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh22-0
- https://github.com/karlheyes/icecast-kh/releases/tag/icecast-2.4.0-kh22

* Fri Jun 05 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh14-1
- Added xsl template for generating JSON with tracks info

* Fri May 29 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh14-0
- https://github.com/karlheyes/icecast-kh/releases/tag/icecast-2.4.0-kh14

* Wed Apr 01 2020 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh13-0
- https://github.com/karlheyes/icecast-kh/releases/tag/icecast-2.4.0-kh13

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0.kh12-0
- https://github.com/karlheyes/icecast-kh/releases/tag/icecast-2.4.0-kh12

* Sun Jan 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-10
- Initial build for kaos repository
