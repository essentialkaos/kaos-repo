###############################################################################

%define _smp_mflags -j1

###############################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              2.2
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  https://github.com/tmux/tmux

Source:               https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        ncurses-devel libevent2-devel

###############################################################################

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
./autogen.sh
%configure

%{__make}  %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{make_install} INSTALLBIN="install -pm 755" INSTALLMAN="install -pm 644"

%post
if [[ ! -f %{_sysconfdir}/shells ]] ; then
  echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ TODO
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

###############################################################################

%changelog
* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- The format strings which referenced time have been removed.  Instead:
  #{t:window_activity} can be used.
- Support for TMPDIR has been removed.  Use TMUX_TMPDIR instead.
- UTF8 detection how happens automatically if the client supports it,
  hence the:
  mouse-utf8
  utf8
  options has been removed.
- The: mouse_utf8_flag format string has been removed.
- The -I option to show-messages has been removed.  See: #{t:start_time}
  format option instead.
- Panes are unzoomed with selectp -LRUD
- New formats added:
  #{scroll_position}
  #{socket_path}
  #{=10:...} -- limit to N characters (from the start)
  #{=-10:...} -- limit to N characters (from the end)
  #{t:...} -- used to format time-based formats
  #{b:...} -- used to ascertain basename from string
  #{d:...} -- used to ascertain dirname from string
  #{s:...} -- used to perform substitutions on a string
- Job output is run via the format system, so formats work again
- If display-time is set to 0, then the indicators wait for a key to be
  pressed.
- list-keys and list-commands can be run without starting the tmux server.
- kill-session learns -C to clear all alerts in all windows of the session.
- Support for hooks (internal for now), but hooks for the following have been
  implemented:
  alert-bell
  alert-silence
  alert-activity
  client-attached
  client-detached
  client-resized
  pane-died
  pane-exited
- RGB (24bit) colour support.  The 'Tc' flag must be set in the external TERM
  entry (using terminal-overrides or a custom terminfo entry).

* Sun Nov 22 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- Updated to 2.1

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0-0
- Updated to 2.0

* Wed Mar 26 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9a-0
- Updated to 1.9a

* Wed Mar 26 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9-0
- Updated to 1.9

* Sun Jul 21 2013 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- Updated to 1.8
