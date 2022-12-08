################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _smp_mflags -j1

################################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              3.3a
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  https://github.com/tmux/tmux

Source0:              https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

Source100:            checksum.sha512

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc byacc autoconf automake
BuildRequires:        ncurses-devel libevent-devel

Provides:             %{name} = %{version}-%{release}

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
  echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README README.ja CHANGES COPYING
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

################################################################################

%changelog
* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.3a-0
- Do not crash when run-shell produces output from a config file.
- Do not unintentionally turn off all mouse mode when button mode is also
  present.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.3-0
- Add an ACL list for users connecting to the tmux socket. Users may be
  forbidden from attaching, forced to attach read-only, or allowed to attach
  read-write. A new command, server-access, configures the list. File system
  permissions must still be configured manually.
- Emit window-layout-changed on swap-pane.
- Better error reporting when applying custom layouts.
- Handle ANSI escape sequences in run-shell output.
- Add pane_start_path to match start_command.
- Set PWD so shells have a hint about the real path.
- Do not allow pipe-pane on dead panes.
- Do not report mouse positions (incorrectly) above the maximum of 223 in
  normal mouse mode.
- Add an option (default off) to control the passthrough escape sequence.
- Support more mouse buttons when the terminal sends them.
- Add a window-resized hook which is fired when the window is actually resized
  which may be later than the client resize.
- Add next_session_id format with the next session ID.
- Add formats for client and server UID and user.
- Add argument to refresh-client -l to forward clipboard to a pane.
- Add remain-on-exit-format to set text shown when pane is dead.
- With split-window -f use percentages of window size not pane size.
- Add an option (fill-character) to set the character used for unused areas of
  a client.
- Add an option (scroll-on-clear) to control if tmux scrolls into history on
  clear.
- Add a capability for OSC 7 and use it similarly to how the title is set (and
  controlled by the same set-titles option).
- Add support for systemd socket activation (where systemd creates the Unix
  domain socket for tmux rather than tmux creating it). Build with
  --enable-systemd.
- Add an option (pane-border-indicators) to select how the active pane is shown
  on the pane border (colour, arrows or both).
- Support underscore styles with capture-pane -e.
- Make pane-border-format a pane option rather than window.
- Respond to OSC 4 queries
- Fix g/G keys in modes to do the same thing as copy mode (and vi).
- Bump the time terminals have to respond to device attributes queries to three
  seconds.
- If automatic-rename is off, allow the rename escape sequence to set an empty
  name.
- Trim menu item text more intelligently.
- Add cursor-style and cursor-colour options to set the default cursor style
  and colour.
- Accept some useful and non-conflicting emacs keys in vi normal mode at the
  command prompt.
- Add a format modifier (c) to force a colour to RGB.
- Add -s and -S to display-popup to set styles, -b to set lines and -T to set
  popup title. New popup-border-lines, popup-border-style and popup-style
  options set the defaults.
- Add -e flag to set an environment variable for a popup.
- Make send-keys without arguments send the key it is bound to (if bound to a
  key).
- Try to leave terminal cursor at the right position even when tmux is drawing
  its own cursor or selection (such as at the command prompt and in choose
  mode) for people using screen readers and similar which can make use of it.
- Change so that {} is converted to tmux commands immediately when parsed. This
  means it must contain valid tmux commands. For commands which expand %% and
  %%%, this now only happens within string arguments. Use of nested aliases
  inside {} is now forbidden. Processing of commands given in quotes remains
  the same.
- Disable evports on SunOS since they are broken.
- Do not expand the file given with tmux -f so it can contain :s.
- Bump FORMAT_LOOP_LIMIT and add a log message when hit.
- Add a terminal feature for the mouse (since FreeBSD termcap does not
  have kmous).
- Forbid empty session names.
- Improve error reporting when the tmux /tmp directory cannot be created or
  used.
- Give #() commands a one second grace period where the output is empty before
  telling the user they aren't doing anything ("not ready").
- When building, pick default-terminal from the first of tmux-256color, tmux,
  screen-256color, screen that is available on the build system (--with-TERM
  can override).
- Do not close popups on resize, instead adjust them to fit.
- Add a client-active hook.
- Make window-linked and window-unlinked window options.
- Do not configure on macOS without the user making a choice about utf8proc
  (either --enable-utf8proc or --disable-utf8proc).
- Do not freeze output in panes when a popup is open, let them continue to
  redraw.
- Add pipe variants of the line copy commands.
- Change copy-line and copy-end-of-line not to cancel and add -and-cancel
  variants, like the other copy commands.
- Support the OSC palette-setting sequences in popups.
- Add a pane-colours array option to specify the defaults palette.
- Add support for Unicode zero-width joiner.
- Make newline a style delimiter as well so they can cross multiple lines for
  readability in configuration files.
- Change focus to be driven by events rather than scanning panes so the
  ordering of in and out is consistent.
- Add display-popup -B to open a popup without a border.
- Add a menu for popups that can be opened with button three outside the popup
  or on the left or top border. Resizing now only works on the right and bottom
  borders or when using Meta. The menu allows a popup to be closed, expanded to
  the full size of the client, centered in the client or changed into a pane.
- Make command-prompt and confirm-before block by default (like run-shell). A
  new -b flags runs them in the background as before. Also set return code for
  confirm-before.
- Change cursor style handling so tmux understands which sequences contain
  blinking and sets the flag appropriately, means that it works whether cnorm
  disables blinking or not. This now matches xterm's behaviour.
- More accurate vi(1) word navigation in copy mode and on the status line. This
  changes the meaning of the word-separators option: setting it to the empty
  string is equivalent to the previous behavior.
- Add -F for command-prompt and use it to fix "Rename" on the window menu.
- Add different command histories for different types of prompts ("command",
  "search" etc).

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2a-0
- Add an "always" value for the "extended-keys" option; if set then tmux will
  forward extended keys to applications even if they do not request them.
- Add a "mouse" terminal feature so tmux can enable the mouse on terminals
  where it is known to be supported even if terminfo(5) says otherwise.
- Do not expand the filename given to -f so it can contain colons.
- Fixes for problems with extended keys and modifiers, scroll region,
  source-file, crosscompiling, format modifiers and other minor issues.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2-0
- Add a flag to disable keys to close a message.
- Permit shortcut keys in buffer, client, tree modes to be configured with a
  format (-K flag to choose-buffer, choose-client, choose-tree).
- Add a current_file format for the config file being parsed.
- When display-message used in config file, show the message after the config
  file finishes.
- Add client-detached notification in control mode.
- Improve performance of format evaluation.
- Make jump command support UTF-8 in copy mode.
- Support X11 colour names and other colour formats for OSC 10 and 11.
- Add "pipe" variants of "copy-pipe" commands which do not copy.
- Include "focused" in client flags.
- Send Unicode directional isolate characters around horizontal pane borders if
  the terminal supports UTF-8 and an extension terminfo(5) capability "Bidi" is
  present.
- Add a -S flag to new-window to make it select the existing window if one
  with the given name already exists rather than failing with an error.
- Add a format modifier to check if a window or session name exists (N/w or
  N/s).
- Add compat clock_gettime for older macOS.
- Add a no-detached choice to detach-on-destroy which detaches only if there
  are no other detached sessions to switch to.
- Add rectangle-on and rectangle-off copy mode commands.
- Change so that window_flags escapes # automatically. A new format
  window_raw_flags contains the old unescaped version.
- Add -N flag to never start server even if command would normally do so.
- With incremental search, start empty and only repeat the previous search if
  the user tries to search again with an empty prompt.
- Add a value for remain-on-exit that only keeps the pane if the program
  failed.
- Add a -C flag to run-shell to use a tmux command rather than a shell command.
- Do not list user options with show-hooks.
- Remove current match indicator in copy mode which can't work anymore since we
  only search the visible region.
- Make synchronize-panes a pane option and add -U flag to set-option to unset
  an option on all panes.
- Make replacement of ##s consistent when drawing formats, whether followed by
  [ or not. Add a flag (e) to the q: format modifier to double up #s.
- Add -N flag to display-panes to ignore keys.
- Change how escaping is processed for formats so that ## and # can be used in
  styles.
- Add a 'w' format modifier for string width.
- Add support for Haiku.
- Expand menu and popup -x and -y as formats.
- Add numeric comparisons for formats.
- Fire focus events even when the pane is in a mode.
- Add -O flag to display-menu to not automatically close when all mouse buttons
  are released.
- Allow fnmatch(3) wildcards in update-environment.
- Disable nested job expansion so that the result of #() is not expanded again.
- Use the setal capability as well as (tmux's) Setulc.
- Add -q flag to unbind-key to hide errors.
- Allow -N without a command to change or add a note to an existing key.
- Add a -w flag to set- and load-buffer to send to clipboard using OSC 52.
- Add -F to set-environment and source-file.
- Allow colour to be spelt as color in various places.
- Add n: modifier to get length of a format.
- Respond to OSC colour requests if a colour is available.
- Add a -d option to display-message to set delay.
- Add a way for control mode clients to subscribe to a format and be notified
  of changes rather than having to poll.
- Add some formats for search in copy mode (search_present, search_match).
- Do not wait on shutdown for commands started with run -b.
- Add -b flags to insert a window before (like the existing -a for after) to
  break-pane, move-window, new-window.
- Make paste -p the default for ].
- Add support for pausing a pane when the output buffered for a control mode
  client gets too far behind. The pause-after flag with a time is set on the
  pane with refresh-client -f and a paused pane may be resumed with
  refresh-client -A.
- Allow strings in configuration files to span multiple lines - newlines and
  any leading whitespace are removed, as well as any following comments that
  couldn't be part of a format. This allows long formats or other strings to be
  annotated and indented.
- Instead of using a custom parse function to process {} in configuration
  files, treat as a set of statements the same as outside {} and convert back
  to a string as the last step. This means the rules are consistent inside and
  outside {}, %%if and friends work at the right time, and the final result
  isn't littered with unnecessary newlines.
- Add support for extended keys - both xterm(1)'s CSI 27 ~ sequence and the
  libtickit CSI u sequence are accepted; only the latter is output. tmux will
  only attempt to use these if the extended-keys option is on and it can detect
  that the terminal outside supports them (or is told it does with the
  "extkeys" terminal feature).
- Add an option to set the pane border lines style from a choice of single
  lines (ACS or UTF-8), double or heavy (UTF-8), simple (plain ASCII) or number
  (the pane numbers). Lines that won't work on a non-UTF-8 terminal are
  translated back into ACS when they are output.
- Make focus events update the latest client (like a key press).
- Store UTF-8 characters differently to reduce memory use.
- Fix break-pane -n when only one pane in the window.
- Instead of sending all data to control mode clients as fast as possible, add
  a limit of how much data will be sent to the client and try to use it for
  panes with some degree of fairness.
- Add an active-pane client flag (set with attach-session -f, new-session -f
  or refresh-client -f). This allows a client to have an independent active
  pane for interactive use (the window client pane is still used for many
  things however).
- Add a mark to copy mode, this is set with the set-mark command (bound to X)
  and appears with the entire line shown using copy-mode-mark-style and the
  marked character in reverse. The jump-to-mark command (bound to M-x) swaps
  the mark and the cursor positions.
- Add a -D flag to make the tmux server run in the foreground and not as a
  daemon.
- Do not loop forever in copy mode when search finds an empty match.
- Fix the next-matching-bracket logic when using vi(1) keys.
- Add a customize mode where options may be browsed and changed, includes
  adding a brief description of each option. Bound to C-b C by default.
- Change message log (C-b ~) so there is one for the server rather than one per
  client and it remains after detach, and make it useful by logging every
  command.
- Add M-+ and M-- to tree mode to expand and collapse all.
- Change the existing client flags for control mode to apply for any client,
  use the same mechanism for the read-only flag and add an ignore-size flag.
  refresh-client -F has become -f (-F stays for backwards compatibility) and
  attach-session and switch-client now have -f flags also. A new format
  client_flags lists the flags and is shown by list-clients by default.
  This separates the read-only flag from "ignore size" behaviour (new
  ignore-size) flag - both behaviours are useful in different circumstances.
  attach -r and switchc -r remain and set or toggle both flags together.
- Store and restore cursor position when copy mode is resized.
- Export TERM_PROGRAM and TERM_PROGRAM_VERSION like various other terminals.
- Add formats for after hook command arguments: hook_arguments with all the
  arguments together; hook_argument_0, hook_argument_1 and so on with
  individual arguments; hook_flag_X if flag -X is present; hook_flag_X_0,
  hook_flag_X_1 and so on if -X appears multiple times.
- Try to search the entire history first for up to 200 ms so a search count can
  be shown. If it takes too long, search the visible text only.
- Use VIS_CSTYLE for paste buffers also (show \012 as \n).
- Change default formats for tree mode, client mode and buffer mode to be more
  compact and remove some clutter.
- Add a key (e) in buffer mode to open the buffer in an editor. The buffer
  contents is updated when the editor exits.
- Add -e flag for new-session to set environment variables, like the same flag
  for new-window.
- Improve search match marking in copy mode. Two new options
  copy-mode-match-style and copy-mode-current-match-style to set the style for
  matches and for the current match respectively. Also a change so that if a
  copy key is pressed with no selection, the current match (if any) is copied.
- Sanitize session names like window names instead of forbidding invalid ones.
- Check if the clear terminfo(5) capability starts with CSI and if so then
  assume the terminal is VT100-like, rather than relying on the XT capability.
- Improve command prompt tab completion and add menus both for strings and -t
  and -s (when used without a trailing space). command-prompt has additional
  flags for only completing a window (-W) and a target (-T), allowing C-b ' to
  only show windows and C-b . only targets.
- Change all the style options to string options so they can support formats.
  Change pane-active-border-style to use this to change the border colour when
  in a mode or with synchronize-panes on. This also implies a few minor changes
  to existing behaviour:
- set-option -a with a style option automatically inserts a comma between the
  old value and appended text.
- OSC 10 and 11 no longer set the window-style option, instead they store the
  colour internally in the pane data and it is used as the default when the
  option is evaluated.
- status-fg and -bg now override status-style instead of the option values
  being changed.
- Add extension terminfo(5) capabilities for margins and focus reporting.
- Try $XDG_CONFIG_HOME/tmux/tmux.conf as well as ~/.config/tmux/tmux.conf for
  configuration file (the search paths are in TMUX_CONF in Makefile.am).
- Remove the DSR 1337 iTerm2 extension and replace by the extended device
  attributes sequence (CSI > q) supported by more terminals.
- Add a -s flag to copy-mode to specify a different pane for the source
  content. This means it is possible to view two places in a pane's history at
  the same time in different panes, or view the history while still using the
  pane. Pressing r refreshes the content from the source pane.
- Add an argument to list-commands to show only a single command.
- Change copy mode to make copy of the pane history so it does not need to
  freeze the pane.
- Restore pane_current_path format from portable tmux on OpenBSD.
- Wait until the initial command sequence is done before sending a device
  attributes request and other bits that prompt a reply from the terminal. This
  means that stray replies are not left on the terminal if the command has
  attached and then immediately detached and tmux will not be around to receive
  them.
- Add a -f filter argument to the list commands like choose-tree.
- Move specific hooks for panes to pane options and windows for window options
  rather than all hooks being session options.
- Show signal names when a process exits with remain-on-exit on platforms which
  have a way to get them.
- Start menu with top item selected if no mouse and use mode-style for the
  selected item.
- Add a copy-command option and change copy-pipe and friends to pipe to it if
  used without arguments, allows all the default copy key bindings to be
  changed to pipe with one option rather than needing to change each key
  binding individually.
- Tidy up the terminal detection and feature code and add named sets of
  terminal features, each of which are defined in one place and map to a
  builtin set of terminfo(5) capabilities. Features can be specified based on
  TERM with a new terminal-features option or with the -T flag when running
  tmux. tmux will also detect a few common terminals from the DA and DSR
  responses.
  This is intended to make it easier to configure tmux's use of terminfo(5)
  even in the presence of outdated ncurses(3) or terminfo(5) databases or for
  features which do not yet have a terminfo(5) entry. Instead of having to grok
  terminfo(5) capability names and what they should be set to in the
  terminal-overrides option, the user can hopefully just give tmux a feature
  name and let it do the right thing.
  The terminal-overrides option remains both for backwards compatibility and to
  allow tweaks of individual capabilities.
- Support mintty's application escape sequence (means tmux doesn't have to
  delay to wait for Escape, so no need to reduce escape-time when using
  mintty).
- Change so main-pane-width and height can be given as a percentage.
- Support for the iTerm2 synchronized updates feature (allows the terminal to
  avoid unnecessary drawing while output is still in progress).
- Make the mouse_word and mouse_line formats work in copy mode and enable the
  default pane menu in copy mode.
- Add a -T flag to resize-pane to trim lines below the cursor, moving lines out
  of the history.
- Add a way to mark environment variables as "hidden" so they can be used by
  tmux (for example in formats) but are not set in the environment for new
  panes. set-environment and show-environment have a new -h flag and there is a
  new %%hidden statement for the configuration file.
- Change default position for display-menu -x and -y to centre rather than top
  left.
- Add support for per-client transient popups, similar to menus but which are
  connected to an external command (like a pane). These are created with new
  command display-popup.
- Change double and triple click bindings so that only one is fired (previously
  double click was fired on the way to triple click). Also add default double
  and triple click bindings to copy the word or line under the cursor and
  change the existing bindings in copy mode to do the same.
- Add a default binding for button 2 to paste.
- Add -d flag to run-shell to delay before running the command and allow it to
  be used without a command so it just delays.
- Add C-g to cancel command prompt with vi keys as well as emacs, and q in
  command mode.
- When the server socket is given with -S, create it with umask 177 instead of
  117 (because it may not be in a safe directory like the default directory in
  /tmp).
- Add a copy-mode -H flag to hide the position marker in the top right.
- Add number operators for formats (+, -, *, / and m).

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 3.1c-0
- Do not write after the end of the array and overwrite the stack when
  colon-separated SGR sequences contain empty arguments.

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1b-0
- Fix build on systems without sys/queue.h.
- Fix crash when allow-rename is on and an empty name is set.

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1a-0
- Do not close stdout prematurely in control mode since it is needed to print
  exit messages. Prevents hanging when detaching with iTerm2.

* Sat Jun 27 2020 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- Only search the visible part of the history when marking (highlighting)
  search terms. This is much faster than searching the whole history and solves
  problems with large histories. The count of matches shown is now the visible
  matches rather than all matches.
- Search using regular expressions in copy mode. search-forward and
  search-backward use regular expressions by default; the incremental versions
  do not.
- Turn off mouse mode 1003 as well as the rest when exiting.
- Add selection_active format for when the selection is present but not moving
  with the cursor.
- Fix dragging with modifier keys, so binding keys such as C-MouseDrag1Pane and
  C-MouseDragEnd1Pane now work.
- Add -a to list-keys to also list keys without notes with -N.
- Do not jump to next word end if already on a word end when selecting a word;
  fixes select-word with single character words and vi(1) keys.
- Fix top and bottom pane calculation with pane border status enabled.
- Add support for adding a note to a key binding (with bind-key -N) and use
  this to add descriptions to the default key bindings. A new -N flag to
  list-keys shows key bindings with notes. Change the default ? binding to use
  this to show a readable summary of keys. Also extend command-prompt to return
  the name of the key pressed and add a default binding (/) to show the note
  for the next key pressed.
- Add support for the iTerm2 DSR 1337 sequence to get the terminal version.
- Treat plausible but invalid keys (like C-BSpace) as literal like any other
  unrecognised string passed to send-keys.
- Detect iTerm2 and enable use of DECSLRM (much faster with horizontally split
  windows).
- Add -Z to default switch-client command in tree mode.
- Add ~ to quoted characters for %%%.
- Document client exit messages in the manual page.
- Do not let read-only clients limit the size, unless all clients are
  read-only.
- Add a number of new formats to inspect what sessions and clients a window is
  present or active in.
- Change file reading and writing to go through the client if necessary. This
  fixes commands like "tmux loadb /dev/fd/X". Also modify source-file to
  support "-" for standard input, like load-buffer and save-buffer.
- Add ~/.config/tmux/tmux.conf to the default search path for configuration
  files.
- Bump the escape sequence timeout to five seconds to allow for longer
  legitimate sequences.
- Make a best effort to set xpixel and ypixel for each pane and add formats for
  them.
- Add push-default to status-left and status-right in status-format[0].
- Do not clear search marks on cursor movement with vi(1) keys.
- Add p format modifier for padding to width and allow multiple substitutions
  in a single format.
- Add -f for full size to join-pane (like split-window).
- Do not use bright when emulating 256 colours on an 8 colour terminal because
  it is also bold on some terminals.
- Make select-pane -P set window-active-style also to match previous behaviour.
- Do not truncate list-keys output.
- Turn automatic-rename back on if the \033k rename escape sequence is used
  with an empty name.
- Add support for percentage sizes for resize-pane ("-x 10%"). Also change
  split-window and join-pane -l to accept similar percentages and deprecate the
  -p flag.
- Add -F flag to send-keys to expand formats in search-backward and forward
  copy mode commands and copy_cursor_word and copy_cursor_line formats for word
  and line at cursor in copy mode. Use for default # and - binding with vi(1)
  keys.
- Add formats for word and line at cursor position in copy mode.
- Add formats for cursor and selection position in copy mode.
- Support all the forms of RGB colour strings in OSC sequences rather than
  requiring two digits.
- Limit lazy resize to panes in attached sessions only.
- Add an option to set the key sent by backspace for those whose system uses ^H
  rather than ^?.
- Change new-session -A without a session name (that is, no -s option also) to
  attach to the best existing session like attach-session rather than a new
  one.
- Add a "latest" window-size option which tries to size windows based on the
  most recently used client. This is now the default.
- Add simple support for OSC 7 (result is available in the pane_path format).
- Add push-default and pop-default for styles which change the colours and
  attributes used for #[default]. These are used in status-format to restore
  the behaviour of window-status-style being the default for
  window-status-format.
- Add window_marked_flag.
- Add cursor-down-and-cancel in copy mode.
- Default to previous search string for search-forward and search-backward.
- Add -Z flag to rotate-window, select-pane, swap-pane, switch-client to
  preserve zoomed state.
- Add -N to capture-pane to preserve trailing spaces.
- Add reverse sorting in tree, client and buffer modes.

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0a-0
- Do not require REG_STARTEND.
- Respawn panes or windows correctly if default-command is set.
- Add missing option for after-kill-pane hook.
- Fix for crash with a format variable that doesn't exist.
- Do not truncate list-keys output on some platforms.
- Do not crash when restoring a layout with only one pane.

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- xterm 348 now disables margins when resized, so send DECLRMM again after
  resize.
- Add support for the SD (scroll down) escape sequence.
- Expand arguments to C and s format modifiers to match the m modifier.
- Add support for underscore colours (Setulc capability must be added with
  terminal-overrides as described in tmux(1)).
- Add a "fill" style attribute for the fill colour of the drawing area (where
  appropriate).
- New -H flag to send-keys to send literal keys.
- Format variables for pane mouse modes (mouse_utf8_flag and mouse_sgr_flag)
  and for origin mode (origin_flag).
- Add -F to refresh-client for flags for control mode clients, only one flag
  (no-output) supported at the moment.
- Add a few vi(1) keys for menus.
- Add pane options, set with set-option -p and displayed with show-options -p.
  Pane options inherit from window options (so every pane option is also
  a window option). The pane style is now configured by setting window-style
  and window-active-style in the pane options; select-pane -P and -g now change
  the option but are no longer documented.
- Do not document set-window-option and show-window-options. set-option -w and
  show-options -w should be used instead.
- Add a -A flag to show-options to show parent options as well (they are marked
  with a *).
- Resize panes lazily - do not resize unless they are in an attached, active
  window.
- Add regular expression support for the format search, match and substitute
  modifiers and make them able to ignore case. find-window now accepts -r to
  use regular expressions.
- Do not use $TMUX to find the session because for windows in multiple sessions
  it is wrong as often as it is right, and for windows in one session it is
  pointless. Instead use TMUX_PANE if it is present.
- Do not always resize the window back to its original size after applying a
  layout, keep it at the layout size until it must be resized (for example when
  attached and window-size is not manual).
- Add new-session -X and attach-session -x to send SIGHUP to parent when
  detaching (like detach-client -P).
- Support for octal escapes in strings (such as \007) and improve list-keys
  output so it parses correctly if copied into a configuration file.
- INCOMPATIBLE: Add a new {} syntax to the configuration file. This is a string
  similar to single quotes but also includes newlines and allows commands that
  take other commands as string arguments to be expressed more clearly and
  without additional escaping.
  A literal { and } or a string containing { or } must now be escaped or
  quoted, for example '{' and '}' instead of { or }, or 'X#{foo}' instead of
  X#{foo}.
- New <, >, <= and >= comparison operators for formats.
- Improve escaping of special characters in list-keys output.
- INCOMPATIBLE: tmux's configuration parsing has changed to use yacc(1). There
  is one incompatible change: a \ on its own must be escaped or quoted as
  either \\ or '\' (the latter works on older tmux versions).
  Entirely the same parser is now used for parsing the configuration file
  and for string commands. This means that constructs previously only
  available in .tmux.conf, such as %%if, can now be used in string commands
  (for example, those given to if-shell - not commands invoked from the
  shell, they are still parsed by the shell itself).
- Add support for the overline attribute (SGR 53). The Smol capability is
  needed in terminal-overrides.
- Add the ability to create simple menus. Introduces new command
  display-menu. Default menus are bound to MouseDown3 on the status line;
  MouseDown3 or M-MouseDown3 on panes; MouseDown3 in tree, client and
  buffer modes; and C-b C-m and C-b M-m.
- Allow panes to be empty (no command). They can be created either by piping to
  split-window -I, or by passing an empty command ('') to split-window. Output
  can be sent to an existing empty window with display-message -I.
- Add keys to jump between matching brackets (emacs C-M-f and C-M-b, vi %%).
- Add a -e flag to new-window, split-window, respawn-window, respawn-pane to
  pass environment variables into the newly created process.
- Hooks are now stored in the options tree as array options, allowing them to
  have multiple separate commands. set-hook and show-hooks remain but
  set-option and show-options can now also be used (show-options will only show
  hooks if given the -H flag). Hooks with multiple commands are run in index
  order.
- Automatically scroll if dragging to create a selection with the mouse and the
  cursor reaches the top or bottom line.
- Add -no-clear variants of copy-selection and copy-pipe which do not clear the
  selection after copying. Make copy-pipe clear the selection by default to be
  consistent with copy-selection.
- Add an argument to copy commands to set the prefix for the buffer name, this
  (for example) allows buffers for different sessions to be named separately.
- Update session activity on focus event.
- Pass target from source-file into the config file parser so formats in %%if
  and %%endif have access to more useful variables.
- Add the ability to infer an option type (server, session, window) from its
  name to show-options (it was already present in set-option).

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
