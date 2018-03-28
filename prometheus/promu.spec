################################################################################

%define debug_package  %{nil}

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

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

Summary:          Prometheus Utility Tool
Name:             promu
Version:          0.1.0
Release:          0%{?dist}
Group:            Development/Tools
License:          ASL 2.0
URL:              https://prometheus.io

Source0:          https://github.com/prometheus/%{name}/archive/v%{version}.tar.gz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    golang >= 1.10

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Promu is the utility tool for Prometheus projects. This tool is part of
reflexion about Prometheus Component Builds.

################################################################################

%prep
%setup -q -n %{name}-%{version}

mkdir -p .src/github.com/prometheus/%{name}
mv * .src/github.com/prometheus/%{name}/
mv .promu.yml .src/github.com/prometheus/%{name}/
mv .src src

%build
export GOPATH=$(pwd)

pushd src/github.com/prometheus/%{name}
    %{__make} %{?_smp_mflags} build
popd

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bin}

install -pm 0755 src/github.com/prometheus/%{name}/%{name} \
        %{buildroot}%{_bin}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bin}/%{name}

################################################################################

%changelog
* Wed Mar 28 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.1.0-0
- Initial build

