################################################################################

%define _smp_mflags -j1

################################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              2.9a
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  https://github.com/tmux/tmux

Source:               https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make automake gcc ncurses-devel libevent2-devel

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

################################################################################

%prep
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
  echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README README.ja CHANGES TODO
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

################################################################################

%changelog
* Fri Jul 19 2019 Anton Novojilov <andy@essentialkaos.com> - 2.9a-0
- Fix bugs in select-pane and the main-horizontal and main-vertical layouts.
- Attempt to preserve horizontal cursor position as well as vertical with
  reflow.
- Rewrite main-vertical and horizontal and change layouts to better handle the
  case where all panes won't fit into the window size, reduce problems with
  pane border status lines and fix other bugs mostly found by Thomas Sattler.
- Add format variables for the default formats in the various modes
  (tree_mode_format and so on) and add a -a flag to display-message to list
  variables with values.
- Add a -v flag to display-message to show verbose messages as the format is
  parsed, this allows formats to be debugged
- Add support for HPA (\033[`).
- Add support for origin mode (\033[?6h).
- No longer clear history on RIS.
- Extend the #[] style syntax and use that together with previous format
  changes to allow the status line to be entirely configured with a single
  option.
- Add E: and T: format modifiers to expand a format twice (useful to expand the
  value of an option).
- The individual -fg, -bg and -attr options have been removed; they
  were superseded by -style options in tmux 1.9.
- Allow more than one mode to be opened in a pane. Modes are kept on a stack
  and retrieved if the same mode is entered again. Exiting the active mode goes
  back to the previous one.
- When showing command output in copy mode, call it view mode instead (affects
  pane_mode format).
- Add -b to display-panes like run-shell.
- Handle UTF-8 in word-separators option.
- New "terminal" colour allowing options to use the terminal default colour
  rather than inheriting the default from a parent option.
- Do not move the cursor in copy mode when the mouse wheel is used.
- Use the same working directory rules for jobs as new windows rather than
  always starting in the user's home.
- Allow panes to be one line or column in size.
- Go to last line when goto-line number is out of range in copy mode.
- Yank previously cut text if any with C-y in the command prompt, only use the
  buffer if no text has been cut.
- Add q: format modifier to quote shell special characters.
- Add StatusLeft and StatusRight mouse locations (keys such as
  MouseDown1StatusLeft) for the status-left and status-right areas of the
  status line.
- Add -Z to find-window.
- Support for windows larger than the client.

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Make display-panes block the client until a pane is chosen or it
  times out.
- Clear history on RIS like most other terminals do.
- Add an "Any" key to run a command if a key is pressed that is not
  bound in the current key table.
- Expand formats in load-buffer and save-buffer.
- Add a rectangle_toggle format.
- Add set-hook -R to run a hook immediately.
- Add README.ja.
- Add pane focus hooks.
- Allow any punctuation as separator for s/x/y not only /.
- Improve resizing with the mouse (fix resizing the wrong pane in some
  layouts, and allow resizing multiple panes at the same time).
- Allow , and } to be escaped in formats as #, and #}.
- Add KRB5CCNAME to update-environment.
- Change meaning of -c to display-message so the client is used if it
  matches the session given to -t.
- Fixes to : form of SGR.
- Add x and X to choose-tree to kill sessions, windows or panes.

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.7-0
- Remove EVENT_- variables from environment on platforms where tmux uses them
  so they do not pass on to panes.
- Fixes for hooks at server exit.
- Remove SGR 10 (was equivalent to SGR 0 but no other terminal seems to do
  this).
- Expand formats in window and session names.
- Add -Z flag to choose-tree, choose-client, choose-buffer to automatically
  zoom the pane when the mode is entered and unzoom when it exits, assuming the
  pane is not already zoomed. This is now part of the default key bindings.
- Add C-g to exit modes with emacs keys.
- Add exit-empty option to exit server if no sessions (defaults to on).
- Show if a filter is present in choose modes.
- Add pipe-pane -I to to connect stdin of the child process.
- Performance improvements for reflow.
- Use RGB terminfo(5) capability to detect RGB colour terminals (the existing
  Tc extension remains unchanged).
- Support for ISO colon-separated SGR sequences.
- Add select-layout -E to spread panes out evenly (bound to E key).
- Support wide characters properly when reflowing.
- Pass PWD to new panes as a hint to shells, as well as calling chdir().
- Performance improvements for the various choose modes.
- Only show first member of session groups in tree mode (-G flag to choose-tree
  to show all).
- Support %%else in config files to match %%if.
- Fix "kind" terminfo(5) capability to be S-Down not S-Up.
- Add a box around the preview label in tree mode.
- Show exit status and time in the remain-on-exit pane text.
- Correctly use pane-base-index in tree mode.
- Change the allow-rename option default to off.
- Support for xterm(1) title stack escape sequences.
- Correctly remove padding cells to fix a UTF-8 display problem

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.6-0
- Add select-pane -T to set pane title.
- Fix memory leak when lines with BCE are removed from history.
- Fix (again) the "prefer unattached" behaviour of attach-session.
- Reorder how keys are checked to allow keys to be specified that have a
  leading escape.
- Support REP escape sequence (\033[b).
- Run alert hooks based on options rather than always, and allow further bells
  even if there is an existing bell.
- Add -d flag to display-panes to override display-panes-time.
- Add selection_present format when in copy mode (allows key bindings that do
  something different if there is a selection).
- Add pane_at_left, pane_at_right, pane_at_top and pane_at_bottom formats.
- Make bell, activity and silence alerting more consistent by: removing the
  bell-on-alert option; adding activity-action and silence-action options with
  the same possible values as the existing bell-action; adding a "both" value
  for the visual-bell, visual-activity and visual-silence options to trigger
  both a bell and a message.
- Add a pane_pipe format to show if pipe-pane is active.
- Block signals between forking and resetting signal handlers so that the
  libevent signal handler doesn't get called in the child and incorrectly write
  into the signal pipe that it still shares with the parent.
- Allow punctuation in pane_current_command.
- Add -c for respawn-pane and respawn-window.
- Wait for any remaining data to flush when a pane is closed while pipe-pane is
  in use.
- Fix working out current client with no target.
- Try to fallback to C.UTF-8 as well as en_US.UTF-8 when looking for a UTF-8
  locale.
- Add user-keys option for user-defined key escape sequences (mapped to User0
  to User999 keys).
- Add pane-set-clipboard hook.
- FAQ file has moved out of repository to online.
- Fix problem with high CPU usage when a client dies unexpectedly.
  941.
- Do a dance on OS X 10.10 and above to return tmux to the user namespace,
  allowing access to the clipboard.
- Do not allow escape sequences which expect a specific terminator (APC, DSC,
  OSC) to wait for forever - use a small timeout. This reduces the chance of
  the pane locking up completely when sent garbage (cat /dev/random or
  similar).
- Support SIGUSR2 to toggle logging on a running server, also generate the
  "out" log file with -vv not -vvvv.
- Make set-clipboard a three state option: on (tmux both sends to outside
  terminal and accepts from applications inside); external (tmux sends outside
  but does not accept inside); and off.
- Fix OSC 4 palette setting for bright foreground colours.
- Use setrgbf and setrgbb terminfo(5) capabilities to set RGB colours, if they
  are available. (Tc is still supported as well.)
- Fix redrawing panes when they are resized several times but end up with the
  size unchanged (for example, splitw/resizep -Z/breakp).
- Major rewrite of choose mode. Now includes preview, sorting, searching and
  tagging; commands that can be executed directly from the mode (for example,
  to delete one or more buffers); and filtering in tree mode.
- choose-window and choose-session are now aliases of choose-tree (in the
  command-alias option).
- Support OSC 10 and OSC 11 to set foreground and background colours.
- Check the U8 capability to determine whether to use UTF-8 line drawing
  characters for ACS.
- Some missing notifications for layout changes.
- Control mode clients now do not affect session sizes until they issue
  refresh-client -C. new-session -x and -y works with control clients even if
  the session is not detached.
- All new sessions that are unattached (whether with -d or started with no
  terminal) are now created with size 80 x 24. Whether the status line is on or
  off does not affect the size of new sessions until they are attached.
- Expand formats in option names and add -F flag to expand them in option
  values.
- Remember the search string for a pane even if copy mode is exited and entered
  again.
- Some further BCE fixes (scroll up, reverse index).
- Improvements to how terminals are cleared (entirely or partially).

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 2.5-0
- Reset updated flag when restarting #() command so that new output is properly
  recognised
- Fix ECH with a background colour.
- Do not rely on the terminal not moving the cursor after DL or EL.
- Fix send-keys and send-prefix in copy-mode (so C-b C-b works). GitHub issue
  905.
- Set the current pane for rotate-window so it works in command sequences.
- Add pane_mode format.
- Differentiate M-Up from Escape+Up when possible (that is, in terminals with
  xterm(1) style function keys)
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
