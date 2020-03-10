################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __sysctl          %{_bindir}/systemctl

%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __userdel         %{_sbindir}/userdel
%define __getent          %{_bindir}/getent

################################################################################

Summary:            HAProxy Data Plane API
Name:               dataplaneapi
Version:            1.2.4
Release:            0%{?dist}
License:            ASL 2.0
Group:              System Environment/Daemons
URL:                https://github.com/haproxytech/dataplaneapi

Source0:            https://github.com/haproxytech/%{name}/archive/v%{version}.tar.gz
Source1:            %{name}.service
Source2:            %{name}.logrotate
Source3:            %{name}.sysconfig

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      golang >= 1.13

Requires:           haproxy >= 1.9
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Data Plane API is a sidecar process that runs next to HAProxy and provides API
endpoints for managing HAProxy. It requires HAProxy version 1.9.0 or higher.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

mkdir -p .src/github.com/haproxytech/%{name}
mv * .src/github.com/haproxytech/%{name}/
mv .src src

mv src/github.com/haproxytech/%{name}/LICENSE \
   src/github.com/haproxytech/%{name}/README.md \
   .

%build
export GOPATH=$(pwd)
export GO111MODULE=on

pushd src/github.com/haproxytech/%{name}
go build -gcflags "-N -l" -ldflags "-X main.COMMIT=000000 -X main.BRANCH=master" \
         -o "$GOPATH/%{name}" ./cmd/%{name}
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sbindir}

install -pDm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -pDm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 0755 %{name} %{buildroot}%{_sbindir}/

%clean
find pkg -type d -exec chmod 0755 {} \;
find pkg -type f -exec chmod 0644 {} \;
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  %{__sysctl} enable %{name}.service &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]]; then
  %{__sysctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__sysctl} stop %{name}.service &>/dev/null || :
fi

%postun
%{__sysctl} daemon-reload &>/dev/null || :

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service

################################################################################

%changelog
* Thu Mar 05 2020 Andrey Kulikov <a.kulikov@fun-box.ru> - 1.2.4-0
- Initial build
