################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Friendly interactive shell (FISh)
Name:           fish
Version:        4.1.2
Release:        0%{?dist}
License:        GPL2
Group:          System Environment/Shells
URL:            https://fishshell.com

Source0:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake gcc-c++ cargo rust ninja-build
BuildRequires:  python3-devel pcre2-devel ncurses-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
fish is a shell geared towards interactive use. Its features are
focused on user friendliness and discoverability. The language syntax
is simple but incompatible with other shell languages.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%cmake3 -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -Dextra_completionsdir=%{_datadir}/%{name}/vendor_completions.d \
    -Dextra_functionsdir=%{_datadir}/%{name}/vendor_functions.d \
    -Dextra_confdir=%{_datadir}/%{name}/vendor_conf.d

%cmake3_build

%install
rm -rf %{buildroot}

%cmake3_install

rm -f %{buildroot}%{_datadir}/applications/fish.desktop
rm -f %{buildroot}%{_datadir}/pixmaps/fish.png

%clean
rm -rf %{buildroot}

%post
if ! grep -q "%{_bindir}/%{name}" %{_sysconfdir}/shells ; then
  echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
fi

%postun
if [[ $1 -eq 0 && -f %{_sysconfdir}/shells ]] ; then
  sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
fi

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config.fish
%{_bindir}/fish
%{_bindir}/fish_indent
%{_bindir}/fish_key_reader
%{_datadir}/%{name}/
%{_datadir}/doc/%{name}/
%{_mandir}/man1/*
%{_datadir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Mon Oct 20 2025 Anton Novojilov <andy@essentialkaos.com> - 4.1.2-0
- https://github.com/fish-shell/fish-shell/releases/tag/4.1.2

* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 4.0.2-0
- https://github.com/fish-shell/fish-shell/releases/tag/4.0.2

* Tue Mar 18 2025 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/4.0.1

* Tue Mar 18 2025 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/4.0.0

* Mon Mar 25 2024 Anton Novojilov <andy@essentialkaos.com> - 3.7.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.7.1

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.7.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.7.0

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 3.6.4-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.6.4

* Thu Oct 05 2023 Anton Novojilov <andy@essentialkaos.com> - 3.6.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.6.1

* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 3.5.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.5.1

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.0.2

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/3.0.0

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.7.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.7.1

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.6.0

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.5.0

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.4.0

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.3.1

* Mon May 23 2016 Gleb Goncharov <inbox@gongled.ru> - 2.3.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.3.0

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.2.0

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.2-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.1.2

* Fri Oct 10 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- https://github.com/fish-shell/fish-shell/releases/tag/2.1.1

* Fri Dec 27 2013 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- Initial build
