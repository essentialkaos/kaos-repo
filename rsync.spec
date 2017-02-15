###############################################################################

Summary:              A program for synchronizing files over a network
Name:                 rsync
Version:              3.1.0
Release:              0%{?dist}
License:              GPLv3+
Group:                Applications/Internet
URL:                  http://rsync.samba.org

Source:               http://rsync.samba.org/ftp/%{name}/src/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc >= 3.0 libacl-devel libattr-devel

###############################################################################

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
install -dm 755 %{buildroot}%{_sysconfdir}/xinetd.d
install -pm 644 packaging/lsb/rsync.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/rsync
make DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc COPYING INSTALL OLDNEWS NEWS TODO README
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man5/%{name}d.conf.5*
%config(noreplace) /etc/xinetd.d/%{name}
%{_bindir}/%{name}

###############################################################################

%changelog
* Wed Feb 15 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.1.0-0
- Initial build
