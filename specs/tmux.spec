################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        A terminal multiplexer
Name:           tmux
Version:        3.5a
Release:        0%{?dist}
License:        ISC and BSD
Group:          Applications/System
URL:            https://github.com/tmux/tmux

Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc byacc autoconf automake
BuildRequires:  ncurses-devel libevent-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
./autogen.sh

%configure

%{__make} %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
rm -rf %{buildroot}

%{make_install} INSTALLBIN="install -pm 755" INSTALLMAN="install -pm 644"

%post
if [[ ! -f %{_sysconfdir}/shells ]] ; then
  echo "%{_bindir}/%{name}" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README README.ja CHANGES COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5a-0
- https://raw.githubusercontent.com/tmux/tmux/3.5a/CHANGES

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 3.5-0
- https://raw.githubusercontent.com/tmux/tmux/3.5/CHANGES

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 3.4-0
- https://raw.githubusercontent.com/tmux/tmux/3.4/CHANGES

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.3a-0
- https://raw.githubusercontent.com/tmux/tmux/3.3a/CHANGES

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.3-0
- https://raw.githubusercontent.com/tmux/tmux/3.3/CHANGES

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2a-0
- https://raw.githubusercontent.com/tmux/tmux/3.2a/CHANGES

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2-0
- https://raw.githubusercontent.com/tmux/tmux/3.2/CHANGES

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.1c-0
- https://raw.githubusercontent.com/tmux/tmux/3.1c/CHANGES

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1b-0
- https://raw.githubusercontent.com/tmux/tmux/3.1b/CHANGES

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1a-0
- https://raw.githubusercontent.com/tmux/tmux/3.1a/CHANGES

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- https://raw.githubusercontent.com/tmux/tmux/3.1/CHANGES

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0a-0
- https://raw.githubusercontent.com/tmux/tmux/3.0a/CHANGES

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- https://raw.githubusercontent.com/tmux/tmux/3.0/CHANGES
