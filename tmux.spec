###############################################################################

%define _smp_mflags -j1

###############################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              2.4
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  https://github.com/tmux/tmux

Source:               https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make automake gcc ncurses-devel libevent2-devel

Provides:             %{name} = %{version}-%{release}

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
* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4-0
- Fix send-keys and send-prefix in copy-mode (so C-b C-b works).
- Set the current pane for rotate-window so it works in command sequences.
- Add pane_mode format.
- Differentiate M-Up from Escape+Up when possible (that is, in terminals with
  xterm(1) style function keys).
- Add session_stack and window_stack_index formats.
- Some new control mode notifications and corresponding hooks:
  pane-mode-changed, window-pane-changed, client-session-changed,
  session-window-changed.
- Format pane_search_string for last search term while in copy mode (useful
  with command-prompt -I).
- Fix a problem with high CPU usage and multiple clients with #().
- Fix UTF-8 combining characters in column 0.
- Fix reference counting so that panes are properly destroyed and their
  processes killed.
- Clamp SU (CSI S) parameter to work around a bug in Konsole.
- Tweak line wrapping in full width panes to play more nicely with terminal
  copy and paste.
- Fix when we emit SGR 0 in capture-pane -e.
- Do not change TERM until after config file parsing has finished, so that
  commands run inside the config file can use it to make decisions (typically
  about default-terminal).
- Make the initial client wait until config file parsing has finished to avoid
  racing with commands.
- Fix core when if-shell fails.
- Only use ED to clear screen if the pane is at the bottom.
- Fix multibyte UTF-8 output.
- Code improvements around target (-t) resolution.
- Change how the default target (for commands without -t) is managed across
  command sequences: now it is set up at the start and commands are required
  to update it if needed. Fixes binding command sequences to mouse keys.
- Make if-shell from the config file work correctly.
- Change to always check the root key table if no binding is found in the
  current table (prefix table or copy-mode table or whatever). This means that
  root key bindings will take effect even in copy mode, if not overridden by a
  copy mode key binding.
- Fix so that the history file works again.
- Run config file without a client rather than using the first client, restores
  previous behaviour.
- If a #() command doesn't exit, continue to read from it and use its last full
  line of output.
- Handle slow terminals and fast output better: when the amount of data
  outstanding gets too large, discard output until it is drained and we are
  able to do a full redraw. Prevents tmux sitting on a huge buffer that the
  terminal will take forever to consume.
- Do not redraw a client unless we realistically think it can accept the data -
  defer redraws until the client has nothing else waiting to write.

* Tue Mar 28 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3-1
- Rebuilt with latest version of libevent

* Tue Oct 18 2016 Anton Novojilov <andy@essentialkaos.com> - 2.3-0
- New option 'pane-border-status' to add text in the pane borders.
- Support for hooks on commands: 'after' and 'before' hooks.
- 'source-file' understands '-q' to suppress errors for nonexistent files.
- Lots of UTF8 improvements, especially on MacOS.
- 'window-status-separator' understands #[] expansions.
- 'split-window' understands '-f' for performing a full-width split.
- Allow report count to be specified when using 'bind-key -R'.
- 'set -a' for appending to user options (@foo) is now supported.
- 'display-panes' can now accept a command to run, rather than always
  selecting the pane.

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
