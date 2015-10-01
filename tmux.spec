###############################################################################

%define _smp_mflags -j1

###############################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              2.0
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  http://sourceforge.net/projects/tmux

Source:               http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        ncurses-devel libevent-devel >= 1.4.14b

###############################################################################

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

###############################################################################

%prep
%setup -q

%build
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
%doc CHANGES FAQ TODO examples/
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

###############################################################################

%changelog
* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0-0
- The choose-list command has been removed.
- 'terminal-overrides' is now a server option, not a session option.
- 'message-limit' is now a server option, not a session option.
- 'monitor-content' option has been removed.
- 'pane_start_path' option has been removed.
- The "info" mechanism which used to (for some commands) provide feedback
  has been removed, and like other commands, they now produce nothing on
  success.
- tmux can now write an entry to utmp if the library 'utempter' is present
  at compile time.
- set-buffer learned append mode (-a), and a corresponding
  'append-selection' command has been added to copy-mode.
- choose-mode now has the following commands which can be bound:
  - start-of-list
  - end-of-list
  - top-line
  - bottom-line
- choose-buffer now understands UTF-8.
- Pane navigation has changed:
  - The old way of always using the top or left if the choice is ambiguous.
  - The new way of remembering the last used pane is annoying if the
    layout is balanced and the leftmost is obvious to the user (because
    clearly if we go right from the top-left in a tiled set of four we want
    to end up in top-right, even if we were last using the bottom-right).

      So instead, use a combination of both: if there is only one possible
      pane alongside the current pane, move to it, otherwise choose the most
      recently used of the choice.
- 'set-buffer' can now be told to give names to buffers.
- The 'new-session', 'new-window', 'split-window', and 'respawn-pane' commands
  now understand multiple arguments and handle quoting problems correctly.
- 'capture-pane' understands '-S-' to mean the start of the pane, and '-E-' to
  mean the end of the pane.
- Support for function keys beyond F12 has changed.  The following explains:
  - F13-F24 are S-F1 to S-F12
  - F25-F36 are C-F1 to C-F12
  - F37-F48 are C-S-F1 to C-S-F12
  - F49-F60 are M-F1 to M-F12
  - F61-F63 are M-S-F1 to M-S-F3
 Therefore, F13 becomes a binding of S-F1, etc.
- Support using pane id as part of session or window specifier (so % means
  session-of-1 or window-of-1) and window id as part of session
  (so @1 means session-of-@1).
- 'copy-pipe' command now understands formats via -F
- 'if-shell'  command now understands formats via -F
- 'split-window' and 'join-window' understand -b to create the pane to the left
  or above the target pane

* Wed Mar 26 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9a-0
- Updated to version 1.9a

* Wed Mar 26 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9-0
- Updated to version 1.9

* Sun Jul 21 2013 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- Updated to version 1.8
