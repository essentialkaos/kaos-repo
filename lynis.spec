###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
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

###############################################################################

Summary:            Security auditing and hardening tool
Name:               lynis
Version:            2.5.1
Release:            0%{?dist}
License:            GPLv3
Group:              Development/Tools
URL:                https://cisofy.com/lynis/

Source0:            https://github.com/CISOfy/%{name}/archive/%{version}.tar.gz

BuildArch:          noarch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           bash >= 4

Provides:           %{name} = %{version}-%{release} 

###############################################################################

%description
Lynis is a security auditing for Unix derivatives like Linux, BSD, and 
Solaris. It performs an in-depth security scan on the system to detect 
software and security issues. Besides information related to security, 
it will also scan for general system information, vulnerable software 
packages, and possible configuration issues.

We believe software should be simple, updated on a regular basis and open. 
You should be able to trust, understand, and even alter the software. 
Many agree with us, as the software is being used by thousands every 
day to protect their systems.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man8/
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}

install -pm 755 %{name}     %{buildroot}%{_bindir}/%{name}
install -pm 444 %{name}.8   %{buildroot}%{_mandir}/man8/
install -pm 644 default.prf %{buildroot}%{_sysconfdir}/%{name}

cp -r db extras include plugins %{buildroot}%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md CONTRIBUTORS.md FAQ LICENSE README.md
%{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.*
%{_datadir}/%{name}

###############################################################################

%changelog
* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.1-0
- Updated to latest stable release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4.6-0
- Updated to latest stable release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4.2-0
- Updated to latest stable release

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Updated to latest stable release

* Thu Oct 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.4-0
- Updated to latest stable release

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- Updated to latest stable release

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest stable release

* Wed Oct 07 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Initial build
