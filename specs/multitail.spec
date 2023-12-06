################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define shortname  mtl

################################################################################

Summary:        View one or multiple files like tail but with multiple windows
Name:           multitail
Version:        7.1.2
Release:        0%{?dist}
License:        Apache-2.0
Group:          Applications/Text
URL:            https://www.vanheusden.com/multitail/

Source0:        https://github.com/folkertvanheusden/multitail/archive/%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc ncurses-devel

%if 0%{?rhel} <= 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif

Requires:       ncurses

Provides:       %{name} = %{version}-%{release}
Provides:       %{shortname} = %{version}-%{release}

################################################################################

%description
MultiTail lets you view one or multiple files like the original tail
program. The difference is that it creates multiple windows on your
console (with ncurses). It can also monitor wildcards: if another file
matching the wildcard has a more recent modification date, it will
automatically switch to that file. That way you can, for example,
monitor a complete directory of files. Merging of 2 or even more
logfiles is possible.

It can also use colors while displaying the logfiles (through regular
expressions), for faster recognition of what is important and what not.
Multitail can also filter lines (again with regular expressions) and
has interactive menus for editing given regular expressions and
deleting and adding windows. One can also have windows with the output
of shell scripts and other software. When viewing the output of
external software, MultiTail can mimic the functionality of tools like
'watch' and such.

################################################################################

%prep
%{crc_check}

%setup -q

sed -i "s/6.4.3/%{version}/" CMakeLists.txt
sed -i '/multitail.conf.new/d' CMakeLists.txt
sed -i '/conversion-scripts/d' CMakeLists.txt

rm GNUmakefile

%build
%{cmake3}
%{cmake3_build}

%install
rm -rf %{buildroot}

%{cmake3_install}

rm -rf %{buildroot}%{_docdir}/

install -dm 755 %{buildroot}%{_sysconfdir}
install -pm 644 %{name}.conf %{buildroot}%{_sysconfdir}/

ln -sf %{_bindir}/%{name} %{buildroot}%{_bindir}/%{shortname}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/%{shortname}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 7.1.2-0
- https://github.com/folkertvanheusden/multitail/compare/7.0.0...7.1.2

* Tue Dec 13 2022 Anton Novojilov <andy@essentialkaos.com> - 7.0.0-0
- https://github.com/folkertvanheusden/multitail/compare/6.5...7.0.0

* Thu Feb 25 2021 Anton Novojilov <andy@essentialkaos.com> - 6.5.0-1
- Fixed path to configuration file

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 6.5.0-0
- Updated to the lastes stable release

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 6.4.2-0
- Updated to the lastes stable release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 6.4.1-0
- Updated to the lastes stable release

* Tue Apr 01 2014 Anton Novojilov <andy@essentialkaos.com> - 6.2.1-0
- Updated to the lastes stable release

* Tue Jan 14 2014 Anton Novojilov <andy@essentialkaos.com> - 6.0-0
- Updated to release 6.0

* Mon Sep 30 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.13-3
- Small improvements

* Wed Aug 21 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.13-0
- Updated to release 5.2.13

* Wed Jun 19 2013 Anton Novojilov <andy@essentialkaos.com> - 5.2.12-0
- Updated to release 5.2.12
