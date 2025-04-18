################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Tool for monitoring the progress of data through a pipeline
Name:           pv
Version:        1.9.31
Release:        0%{?dist}
License:        GPLv3+
Group:          Applications/System
URL:            https://www.ivarch.com/programs/pv.shtml

Source0:        https://www.ivarch.com/programs/sources/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make gettext

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Pipe Viewer is a terminal-based tool for monitoring the progress of
data through a pipeline. It can be inserted into any normal pipeline
between two processes to give a visual indication of how quickly data
is passing through, how long it has taken, how near to completion it
is, and an estimate of how long it will be until completion.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_datarootdir}/locale

%{make_install} DESTDIR="%{buildroot}"

rm -rf %{buildroot}%{_docdir}/%{name}

%find_lang %{name}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datarootdir}/locale/*

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.9.31-0
- https://codeberg.org/a-j-wood/pv/releases/tag/v1.9.31

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.9.27-0
- https://codeberg.org/a-j-wood/pv/releases/tag/v1.9.27

* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 1.8.12-0
- https://codeberg.org/a-j-wood/pv/releases/tag/v1.8.12

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8.5-0
- https://codeberg.org/a-j-wood/pv/releases/tag/v1.8.5

* Sat Dec 10 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6.20-0
- https://github.com/a-j-wood/pv/releases/tag/v1.6.20

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6.6-0
- https://github.com/a-j-wood/pv/releases/tag/v1.6.6

* Thu May 04 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.6.0-0
- Initial build
