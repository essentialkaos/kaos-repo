################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _opt              /opt
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

################################################################################

%define npm_name        yarn
%global nodejs_sitelib  %{_prefix}%{_lib32}/node_modules

################################################################################

Summary:            Fast, reliable, and secure dependency management.
Name:               nodejs-yarn
Version:            1.21.1
Release:            0%{?dist}
License:            BSD
Group:              Development/Tools
URL:                https://yarnpkg.com

Source0:            https://github.com/yarnpkg/yarn/releases/download/v%{version}/yarn-v%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           nodejs >= 12

Provides:           %{name} = %{version}-%{release}
Provides:           yarnpkg = %{version}-%{release}

################################################################################

%description
Fast: Yarn caches every package it has downloaded, so it never needs to download
the same package again. It also does almost everything concurrently to maximize
resource utilization. This means even faster installs.

Reliable: Using a detailed but concise lockfile format and a deterministic
algorithm for install operations, Yarn is able to guarantee that any
installation that works on one system will work exactly the same on another
system.

Secure: Yarn uses checksums to verify the integrity of every installed package
before its code is executed.

################################################################################

%prep
%{crc_check}

%setup -qn %{npm_name}-v%{version}

%build

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{nodejs_sitelib}/%{npm_name}

cp -pr package.json lib bin %{buildroot}%{nodejs_sitelib}/%{npm_name}

rm -f %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/*.cmd

ln -sf ../lib/node_modules/yarn/bin/yarn.js %{buildroot}%{_bindir}/%{name}
ln -sf ../lib/node_modules/yarn/bin/yarn.js %{buildroot}%{_bindir}/yarnpkg

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/%{name}
%{_bindir}/yarnpkg

################################################################################

%changelog
* Tue Jan 14 2020 Andrey Kulikov <a.kulikov@fun-box.ru> - 1.21.1-0
- Initial build
