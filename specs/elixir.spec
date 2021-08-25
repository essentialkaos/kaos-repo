################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

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

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            A modern approach to programming for the Erlang VM
Name:               elixir
Version:            1.12.2
Release:            0%{?dist}
License:            ASL 2.0 and ERPL
Group:              Development/Tools
URL:                https://elixir-lang.org

Source0:            https://github.com/%{name}-lang/%{name}/archive/v%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      erlang22 git

Requires:           erlang >= 22

Provides:           %{name} = %{version}-%{release}
Provides:           %{name}-lang = %{version}-%{release}

################################################################################

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
LC_ALL="en_US.UTF-8" %{__make} %{?_smp_mflags}

%check
%if %{?_with_check:1}%{?_without_check:0}
LC_ALL="en_US.UTF-8" %{__make} %{?_smp_mflags} test
%endif

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/%{name}/%{version}
install -dm 755 %{buildroot}%{_bindir}

cp -ra bin lib %{buildroot}%{_datadir}/%{name}/%{version}/

ln -sf %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

################################################################################

%changelog
* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.2-0
- Updated to the latest release

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.1-0
- Updated to the latest release

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.0-0
- Updated to the latest release

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.11.4-0
- Updated to the latest release

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.11.3-0
- Updated to the latest release

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.2-0
- Updated to the latest release

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.1-0
- Updated to the latest release

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-0
- Updated to the latest release

* Thu Aug 13 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.4-0
- Updated to the latest release

* Thu Aug 13 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.3-0
- Updated to the latest release

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- Updated to the latest release

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.1-0
- Updated to the latest release

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- Updated to the latest release

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- Updated to the latest release

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- Updated to the latest release

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- Updated to the latest release

* Thu Aug 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- Updated to the latest release
- Added CRC check for sources

* Fri Jun 28 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- Updated to the latest version

* Mon Jun 03 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.2-0
- Updated to the latest version

* Wed Feb 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- Updated to the latest version

* Sat Jan 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- Updated to the latest version

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- Updated to the latest version

* Mon Aug 27 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- Updated to the latest version

* Wed Aug 22 2018 Gleb Goncharov <ggoncharov@fun-box.ru> - 1.7.2-0
- Updated to the latest version

* Wed Aug 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- Updated to the latest version

* Wed Aug 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to the latest version

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.6-0
- Updated to the latest version

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.5-0
- Updated to the latest version

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.4-0
- Updated to the latest version

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- Updated to the latest version

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to the latest version

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- Updated to the latest version

* Wed Oct 25 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.5.2-1
- Fixed Erlang OTP version dependency

* Thu Oct 05 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Updated to the latest version

* Wed Aug 23 2017 Gleb Goncharov <ggoncharov@fun-box.ru> - 1.5.1-0
- Updated to the latest version

* Wed Aug 23 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to the latest version

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- Updated to the latest version

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- Updated to the latest version

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- Updated to the latest version

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Updated to the latest version

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- Updated to the latest version

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-0
- Updated to the latest version

* Sun Sep 25 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.3-0
- Updated to the latest version

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- Updated to the latest version

* Thu Jun 30 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.3.1-0
- Updated to the latest version

* Wed Jun 22 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to the latest version

* Tue Feb 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-1
- Fixed broken links to binary files

* Tue Jan 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to the latest version

* Sun Oct 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Initial build
