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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __usermod         %{_sbindir}/usermod
%define __groupadd        %{_sbindir}/groupadd
%define __groupmod        %{_sbindir}/groupmod
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

%define _statdpath        %{_sharedstatedir}/nfs/statd

%define rpcuser_name      rpcuser
%define rpcuser_group     rpcuser
%define rpcuser_gid       29
%define rpcuser_uid       29
%define rpcuser_home      %{_sharedstatedir}/nfs

# Using the 16-bit value of -2 for the nfsnobody uid and gid
%define nfsnobody_name    nfsnobody
%define nfsnobody_group   nfsnobody
%define nfsnobody_uid     65534
%define nfsnobody_gid     65534
%define nfsnobody_home    %{_sharedstatedir}/nfs

################################################################################

Summary:              NFS utilities and supporting clients and daemons for the kernel NFS server
Name:                 nfs-utils
Epoch:                1
Version:              1.3.4
Release:              3%{?dist}
License:              MIT and GPLv2 and GPLv2+ and BSD
Group:                System Environment/Daemons
URL:                  https://sourceforge.net/projects/nfs

Source0:              https://www.kernel.org/pub/linux/utils/%{name}/%{version}/%{name}-%{version}.tar.xz
Source1:              id_resolver.conf
Source2:              nfs.sysconfig
Source3:              nfs-utils_env.sh
Source4:              lockd.conf

Patch001:             %{name}-1.3.5-rc2.patch
Patch100:             %{name}-1.2.1-statdpath-man.patch
Patch101:             %{name}-1.2.1-exp-subtree-warn-off.patch
Patch102:             %{name}-1.2.3-sm-notify-res_init.patch
Patch103:             %{name}-1.2.5-idmap-errmsg.patch
Patch104:             %{name}-1.3.2-systemd-gssargs.patch

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        libevent-devel >= 2.0.22 libcap-devel
BuildRequires:        libnfsidmap-devel libtirpc-devel libblkid-devel
BuildRequires:        krb5-libs >= 1.4 autoconf >= 2.57 openldap-devel >= 2.2
BuildRequires:        automake libtool gcc device-mapper-devel
BuildRequires:        krb5-devel tcp_wrappers-devel libmount-devel
BuildRequires:        sqlite-devel python-devel

Requires:             rpcbind sed gawk sh-utils fileutils textutils grep
Requires:             kmod keyutils quota libnfsidmap libevent >= 2.0.22
Requires:             libtirpc >= 0.2.3-1 libblkid libcap libmount
Requires:             gssproxy => 0.3.0-0

Provides:             exportfs = %{epoch}:%{version}-%{release}
Provides:             nfsstat = %{epoch}:%{version}-%{release}
Provides:             showmount = %{epoch}:%{version}-%{release}
Provides:             rpcdebug = %{epoch}:%{version}-%{release}
Provides:             rpc.idmapd = %{epoch}:%{version}-%{release}
Provides:             rpc.mountd = %{epoch}:%{version}-%{release}
Provides:             rpc.nfsd = %{epoch}:%{version}-%{release}
Provides:             rpc.statd = %{epoch}:%{version}-%{release}
Provides:             rpc.gssd = %{epoch}:%{version}-%{release}
Provides:             mount.nfs = %{epoch}:%{version}-%{release}
Provides:             mount.nfs4 = %{epoch}:%{version}-%{release}
Provides:             umount.nfs = %{epoch}:%{version}-%{release}
Provides:             umount.nfs4 = %{epoch}:%{version}-%{release}
Provides:             sm-notify = %{epoch}:%{version}-%{release}
Provides:             start-statd = %{epoch}:%{version}-%{release}

Requires(pre):        shadow-utils >= 4.0.3-25
Requires(pre):        util-linux
Requires(post):       systemd-units
Requires(preun):      systemd-units
Requires(postun):     systemd-units

################################################################################

%description
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.

This package also contains the mount.nfs and umount.nfs program.

################################################################################

%prep
%setup -q

%patch001 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1

%build
%ifarch s390 s390x sparcv9 sparc64
PIE="-fPIE"
%else
PIE="-fpie"
%endif
export PIE

./autogen.sh

CFLAGS="`echo %{optflags} $ARCH_OPT_FLAGS $PIE -D_FILE_OFFSET_BITS=64`"

%configure \
    CFLAGS="$CFLAGS" \
    CPPFLAGS="$DEFINES" \
    LDFLAGS="-pie" \
    --enable-libmount-mount \
    --enable-mountconfig \
    --enable-ipv6 \
    --with-statdpath=%{_statdpath} \
    --with-systemd

%{__make} %{?_smp_mflags} all

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbin}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libexecdir}/%{name}
install -d %{buildroot}%{_unitdir}/../system
install -d %{buildroot}%{_unitdir}/../system-generators
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/request-key.d
install -d %{buildroot}%{_sysconfdir}/modprobe.d
install -d %{buildroot}%{_sysconfdir}/exports.d
install -d %{buildroot}/run/sysconfig
install -d %{buildroot}%{_unitdir}/../scripts
install -d %{buildroot}%{_sharedstatedir}/nfs/rpc_pipefs
install -d %{buildroot}%{_sharedstatedir}/nfs/statd/sm
install -d %{buildroot}%{_sharedstatedir}/nfs/statd/sm.bak
install -d %{buildroot}%{_sharedstatedir}/nfs/v4recovery

%{make_install}

# rpc.svcgssd is no longer supported.
rm -rf %{buildroot}%{_unitdir}/rpc-svcgssd.service

install -pm 755 tools/rpcdebug/rpcdebug %{buildroot}%{_sbindir}
install -pm 644 utils/mount/nfsmount.conf %{buildroot}%{_sysconfdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/request-key.d
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/nfs
install -pm 755 %{SOURCE3} %{buildroot}%{_libexecdir}/nfs-utils/nfs-utils_env.sh
install -pm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/modprobe.d/lockd.conf

# create symlinks for backward compatibility with an older versions nfs-utils
pushd %{buildroot}%{_unitdir}
  ln -s nfs-server.service nfs.service
  ln -s rpc-gssd.service nfs-secure.service
  ln -s nfs-idmapd.service  nfs-idmap.service
  ln -s rpc-statd.service nfs-lock.service
popd

touch %{buildroot}%{_sharedstatedir}/nfs/rmtab

mv %{buildroot}%{_sbindir}/rpc.statd %{buildroot}/sbin

################################################################################

%clean
rm -rf %{buildroot}

%pre
# move files so the running service will have this applied as well
for x in gssd idmapd ; do
  if [[ -f %{_lockdir}/rpc.$x ]] ; then
    mv %{_lockdir}/rpc.$x %{_lockdir}/rpc$x
  fi
done

getent group %{rpcuser_group} &> /dev/null || groupadd -g %{rpcuser_gid} %{rpcuser_group} &>/dev/null || :
getent group %{nfsnobody_group} &> /dev/null || groupadd -g %{nfsnobody_gid} %{nfsnobody_group} &>/dev/null || :
getent passwd %{rpcuser_name} &> /dev/null || \
  useradd -l -c "RPC Service User" -r -g %{rpcuser_uid} \
    -s /sbin/nologin -u %{rpcuser_uid} \
    -d %{rpcuser_home} %{rpcuser_name} &>/dev/null || :
getent passwd %{nfsnobody_name} &> /dev/null || \
  useradd -l -c "Anonymous NFS User" -r -g %{nfsnobody_uid} \
    -s /sbin/nologin -u %{nfsnobody_uid} \
    -d %{nfsnobody_home} %{nfsnobody_name} &>/dev/null || :

%post
if [[ $1 -eq 1 ]] ; then
  %{__systemctl} enable nfs-client.target &>/dev/null || :
  %{__systemctl} start nfs-client.target &>/dev/null || :
fi

%systemd_post nfs-config
%systemd_post nfs-server

# Make sure statd used the correct uid/gid.
chown -R rpcuser:rpcuser %{rpcuser_home}/statd

%preun
if [[ $1 -eq 0 ]] ; then
  %systemd_preun nfs-client.target
  %systemd_preun nfs-server.server
fi

%postun
%systemd_postun_with_restart nfs-client.target
%systemd_postun_with_restart nfs-server

%{__systemctl} --system daemon-reload &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/sysconfig/nfs
%config(noreplace) %{_sysconfdir}/nfsmount.conf
%dir %{_sysconfdir}/exports.d
%dir %{_sharedstatedir}/nfs/v4recovery
%dir %{_sharedstatedir}/nfs/rpc_pipefs
%dir %{_sharedstatedir}/nfs
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm.bak
%ghost %attr(644,rpcuser,rpcuser) %{_statdpath}/state
%config(noreplace) %{_sharedstatedir}/nfs/xtab
%config(noreplace) %{_sharedstatedir}/nfs/etab
%config(noreplace) %{_sharedstatedir}/nfs/rmtab
%config(noreplace) %{_sysconfdir}/request-key.d/id_resolver.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/lockd.conf
%doc linux-nfs/ChangeLog linux-nfs/KNOWNBUGS linux-nfs/NEW linux-nfs/README
%doc linux-nfs/THANKS linux-nfs/TODO
%{_sbin}/rpc.statd
%{_sbin}/osd_login
%{_sbin}/nfsdcltrack
%{_sbindir}/exportfs
%{_sbindir}/nfsstat
%{_sbindir}/rpcdebug
%{_sbindir}/rpc.mountd
%{_sbindir}/rpc.nfsd
%{_sbindir}/showmount
%{_sbindir}/rpc.idmapd
%{_sbindir}/rpc.gssd
%{_sbindir}/sm-notify
%{_sbindir}/start-statd
%{_sbindir}/mountstats
%{_sbindir}/nfsiostat
%{_sbindir}/nfsidmap
%{_sbindir}/blkmapd
%{_mandir}/*/*
%{_unitdir}/../*/*
%attr(755,root,root) %{_libexecdir}/nfs-utils/nfs-utils_env.sh
%attr(4755,root,root) /sbin/mount.nfs
%{_sbin}/mount.nfs4
%{_sbin}/umount.nfs
%{_sbin}/umount.nfs4

################################################################################

%changelog
* Wed Feb 12 2020 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-3
- Rebuilt with the latest version of libevent

* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-2
- Rebuilt with the latest version of libevent

* Tue Aug 01 2017 Gleb Goncharov <ggoncharov@fun-box.ru> - 1.3.4-1
- Initial build for kaos repository
