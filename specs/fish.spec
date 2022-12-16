################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Friendly interactive shell (FISh)
Name:           fish
Version:        3.5.1
Release:        0%{?dist}
License:        GPL2
Group:          System Environment/Shells
URL:            https://fishshell.com

Source0:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel gettext autoconf

%if 0%{?rhel} <= 7
BuildRequires:  cmake3 devtoolset-9-gcc-c++ devtoolset-9-binutils
%else
BuildRequires:  cmake gcc-c++
%endif

Requires:       bc which man

%if 0%{?rhel} <= 8
Requires:       python2
%else
Requires:       python3
%endif

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
%if 0%{?rhel} <= 7
# Use gcc and gcc-c++ from DevToolSet 9
export PATH="/opt/rh/devtoolset-9/root/usr/bin:$PATH"
%endif

mkdir build
pushd build
  cmake3 .. -DCMAKE_INSTALL_PREFIX="/"
  cmake3 --build .
popd

%install
rm -rf %{buildroot}

pushd build
  %{make_install}
popd

rm -f %{buildroot}%{_datadir}/applications/fish.desktop
rm -f %{buildroot}%{_datadir}/pixmaps/fish.png

%clean
rm -rf %{buildroot}

%post
if ! grep -q "%{_bindir}/%{name}" %{_sysconfdir}/shells ; then
  echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
fi

%postun
if [[ $1 -eq 0 ]] ; then
  grep -v "%{_bindir}/%{name}" %{_sysconfdir}/shells > %{_sysconfdir}/%{name}.tmp
  mv %{_sysconfdir}/%{name}.tmp %{_sysconfdir}/shells
fi

################################################################################

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config.fish
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/doc/%{name}/
%{_datadir}/locale/*
%{_mandir}/man1/*
%{_datadir}/pkgconfig/%{name}.pc

################################################################################

%changelog
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
