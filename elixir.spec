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

Summary:            A modern approach to programming for the Erlang VM
Name:               elixir
Version:            1.3.3
Release:            0%{?dist}
License:            ASL 2.0 and ERPL
Group:              Development/Tools
URL:                http://elixir-lang.org
Vendor:             Plataformatec

Source0:            https://github.com/%{name}-lang/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      erlang >= 18 git 

Requires:           erlang >= 18

Provides:           %{name} = %{version}-%{release}
Provides:           %{name}-lang = %{version}-%{release}

###############################################################################

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
LC_ALL="en_US.UTF-8" %{__make} %{?_smp_mflags}

%check
LC_ALL="en_US.UTF-8" %{__make} test

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/%{name}/%{version}
install -dm 755 %{buildroot}%{_bindir}

cp -ra bin lib %{buildroot}%{_datadir}/%{name}/%{version}/

ln -sf %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}/%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

###############################################################################

%changelog
* Sun Sep 25 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.3-0
- Updated to latest version

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- Updated to latest version

* Thu Jun 30 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.3.1-0
- Updated to latest version

* Wed Jun 22 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to latest version

* Tue Feb 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-1
- Fixed broken links to binary files

* Tue Jan 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to latest version

* Sun Oct 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Initial build
