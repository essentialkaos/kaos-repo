###############################################################################

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

###############################################################################

%define main_version 2.9
%define patch        0

###############################################################################

Summary:         A small text editor
Name:            nano
Version:         %{main_version}.%{patch}
Release:         0%{?dist}
License:         GPLv3+
Group:           Applications/Editors
URL:             http://www.nano-editor.org

Source:          https://www.nano-editor.org/dist/v%{main_version}/%{name}-%{version}.tar.gz

Patch0:          %{name}-nanorc.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc make automake groff ncurses-devel sed

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
GNU nano is a small and friendly text editor.

###############################################################################

%prep
%setup -q

%patch0 -p1

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 0755 %{buildroot}%{_sysconfdir}
install -dm 0755 %{buildroot}%{_root}

install -pm 0644 doc/sample.nanorc %{buildroot}%{_sysconfdir}/nanorc

# Create config for root with red title and status
cp %{buildroot}%{_sysconfdir}/nanorc %{buildroot}%{_root}/.nanorc

sed -i 's/^set titlecolor brightwhite,blue/set titlecolor brightwhite,red/' %{buildroot}%{_root}/.nanorc
sed -i 's/^set statuscolor brightwhite,green/set statuscolor brightwhite,red/' %{buildroot}%{_root}/.nanorc

rm -f %{buildroot}%{_infodir}/dir

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
  fi
fi

###############################################################################

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc doc/sample.nanorc
%config(noreplace) %{_sysconfdir}/nanorc
%config(noreplace) %{_root}/.nanorc
%{_bindir}/nano
%{_bindir}/rnano
%{_mandir}/man1/nano.1.*
%{_mandir}/man1/rnano.1.*
%{_mandir}/man5/nanorc.5.*
%{_infodir}/nano.info*
%{_datadir}/nano
%{_defaultdocdir}/%{name}/*.html

###############################################################################

%changelog
* Mon Nov 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.0-0
- Updated to latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.8.7-0
- Updated to latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.8.5-0
- Updated to latest stable release

* Wed Jun 14 2017 Anton Novojilov <andy@essentialkaos.com> - 2.8.4-0
- Updated to latest stable release
- Added config root with red status and title

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.5-0
- Updated to latest stable release

* Fri Jan 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.4-0
- Initial build for kaos repository
