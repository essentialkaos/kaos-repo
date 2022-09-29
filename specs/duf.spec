################################################################################

# rpmbuilder:gopack    github.com/muesli/duf
# rpmbuilder:tag       v0.8.1

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define  debug_package %{nil}

################################################################################

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

################################################################################

Summary:         Disk usage utility
Name:            duf
Version:         0.8.1
Release:         0%{?dist}
Group:           Development/Tools
License:         MIT
URL:             https://github.com/muesli/duf

Source0:         %{name}-%{version}.tar.bz2

Source100:       checksum.sha512

BuildRequires:   golang >= 1.15

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Disk Usage/Free Utility with a variety of features:

- User-friendly, colorful output
- Adjusts to your terminal's width
- Sort the results according to your needs
- Groups & filters devices
- Can conveniently output JSON

################################################################################

%prep
%{crc_check}

%setup -q

%build
export GOPATH=$(pwd)

# Move all sources to src directory
mkdir -p .src ; mv * .src ; mv .src src

pushd src/github.com/muesli/%{name}
  go build -ldflags="-X 'main.Version=%{version}' -X main.CommitSHA=HEAD"
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 src/github.com/muesli/%{name}/%{name} \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

################################################################################

%changelog
* Fri Sep 30 2022 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to the latest stable release

* Fri Oct 23 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.4.0-0
- Initial build for kaos-repo
