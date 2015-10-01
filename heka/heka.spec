########################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _share            /share
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

########################################################################################

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

########################################################################################

%define user_name         heka
%define group_name        heka

########################################################################################

Summary:        Tool for collecting and collating data from a number of different sources
Name:           heka
Version:        0.9.2
Release:        0%{?dist}
License:        MPL2.0
Group:          System Environment/Daemons
URL:            https://github.com/mozilla-services/heka

Source0:        https://github.com/mozilla-services/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}-man.tar.gz

Patch0:         %{name}-cmake-no-submodules.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc golang >= 1.4 git mercurial


Requires(post): %{__chkconfig} initscripts
Requires(pre):  %{__chkconfig} initscripts

Provides:       %{name} = %{version}-%{release}

########################################################################################

%description
Heka is a tool for collecting and collating data from a number of different
sources, performing "in-flight" processing of collected data, and delivering
the results to any number of destinations for further analysis.

########################################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p1

%build
%{__tar} xzvf %{SOURCE1}

./build.sh

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_libdir}
install -dm 755 %{buildroot}%{_includedir}
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_mandir}/man5

cp -r build/heka/bin/*       %{buildroot}%{_bindir}/
cp -r build/heka/lib/*       %{buildroot}%{_libdir}/
cp -r build/heka/include/*   %{buildroot}%{_includedir}/

cp -r man/*.1 %{buildroot}%{_mandir}/man1/
cp -r man/*.5 %{buildroot}%{_mandir}/man5/

install -dm 755 %{buildroot}%{_datadir}/%{name}/lua_decoders
install -dm 755 %{buildroot}%{_datadir}/%{name}/lua_encoders
install -dm 755 %{buildroot}%{_datadir}/%{name}/lua_filters
install -dm 755 %{buildroot}%{_datadir}/%{name}/lua_modules
install -dm 755 %{buildroot}%{_datadir}/%{name}/dasher

cp -r sandbox/lua/decoders/* %{buildroot}%{_datadir}/%{name}/lua_decoders/
cp -r sandbox/lua/encoders/* %{buildroot}%{_datadir}/%{name}/lua_encoders/
cp -r sandbox/lua/filters/*  %{buildroot}%{_datadir}/%{name}/lua_filters/
cp -r sandbox/lua/modules/*  %{buildroot}%{_datadir}/%{name}/lua_modules/

cp -r dasher/* %{buildroot}%{_datadir}/%{name}/dasher/

%clean
rm -rf %{buildroot}

%pre
getent group %{group_name} >/dev/null || %{__groupadd} -r %{group_name}
getent passwd %{user_name} >/dev/null || %{__useradd} -s /sbin/nologin -M -r -g %{group_name} %{user_name}

########################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.md CHANGES.txt
%{_bindir}/%{name}-cat
%{_bindir}/%{name}-flood
%{_bindir}/%{name}-inject
%{_bindir}/%{name}-logstreamer
%{_bindir}/%{name}-sbmgr
%{_bindir}/%{name}-sbmgrload
%{_bindir}/hekad
%{_bindir}/mockgen
%{_bindir}/protoc-gen-gogo
%{_libdir}/*
%{_includedir}/*
%{_datadir}/%{name}/*
%{_mandir}/*

########################################################################################

%changelog
* Fri Jun 26 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- Initial build
