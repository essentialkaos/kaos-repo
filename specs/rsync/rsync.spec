################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        A program for synchronizing files over a network
Name:           rsync
Version:        3.3.0
Release:        0%{?dist}
License:        GPLv3+
Group:          Applications/Internet
URL:            https://rsync.samba.org

Source0:        https://download.samba.org/pub/%{name}/src/%{name}-%{version}.tar.gz
Source1:        %{name}d.conf

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc autoconf
BuildRequires:  libacl-devel libattr-devel popt-devel libzstd-devel
BuildRequires:  openssl-devel lz4-devel xxhash-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

################################################################################

%package daemon
Summary:  Service for anonymous access to rsync
Group:    Applications/Internet

BuildArch:  noarch

Requires:  %{name} = %{version}-%{release}

%description daemon
Rsync can be used to offer read only access to anonymous clients. This
package provides the anonymous rsync service.

################################################################################

%prep
%{crc_check}

%setup -q

chmod -x support/*

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALLCMD='install -p' INSTALLMAN='install -p'

install -dDm 755 %{buildroot}%{_unitdir}

install -pDm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rsyncd.conf
install -pDm 644 packaging/systemd/* %{buildroot}%{_unitdir}/

%clean
rm -rf %{buildroot}

%post daemon
if [[ $1 -eq 1 ]] ; then
  systemctl preset rsyncd.service &>/dev/null || :
fi

%preun daemon
if [[ $1 -eq 0 ]] ; then
  systemctl --no-reload disable rsyncd.service &>/dev/null || :
  systemctl stop rsyncd.service &>/dev/null || :
fi

%postun daemon
systemctl daemon-reload rsyncd.service &>/dev/null || :

if [[ $1 -ge 1 ]] ; then
  systemctl try-restart rsyncd.service &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING README.md SECURITY.md NEWS.md support/ tech_report.tex
%{_bindir}/%{name}
%{_bindir}/%{name}-ssl
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-ssl.1*

%files daemon
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rsyncd.conf
%{_mandir}/man5/rsyncd.conf.5*
%{_unitdir}/rsync.socket
%{_unitdir}/rsync.service
%{_unitdir}/rsync@.service

################################################################################

%changelog
* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 3.3.0-0
- https://github.com/RsyncProject/rsync/blob/v3.3.0/NEWS.md

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 3.2.7-0
- https://github.com/RsyncProject/rsync/blob/v3.2.7/NEWS.md

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 3.1.3-0
- Updated to latest stable release

* Wed Feb 15 2017 Anton Novojilov <andy@essentialkaos.com> - 3.1.2-0
- Initial build for kaos repository
