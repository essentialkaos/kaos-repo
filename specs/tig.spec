################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

%define bashcompl         %{_sysconfdir}/bash_completion.d

################################################################################

Summary:            Tig is an ncurses-based text-mode interface for git
Name:               tig
Version:            2.5.0
Release:            0%{?dist}
License:            GPL
Group:              Development/Tools
URL:                https://github.com/jonas/tig

Source0:            https://github.com/jonas/tig/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           git ncurses glibc

BuildRequires:      make gcc autoconf asciidoc xmlto ncurses-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Tig is a git repository browser that additionally can act as a pager
for output from various git commands.

When browsing repositories, it uses the underlying git commands to
present the user with various views, such as summarized revision log
and showing the commit with the log message, diffstat, and the diff.

Using it as a pager, it will display input from stdin and colorize it.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{configure}

CFLAGS="%{optflags} -DVERSION=%{name}-%{version}-%{release}"

%{__make} prefix=%{_prefix} %{?_smp_mflags} all
%{__make} prefix=%{_prefix} doc-man doc-html

%install
rm -rf %{buildroot}

CFLAGS="%{optflags} -DVERSION=%{name}-%{version}-%{release}"

%{make_install} install-doc-man prefix=%{_prefix} \
                                bindir=%{_bindir} \
                                mandir=%{_mandir}

install -dm 755 %{buildroot}%{bashcompl}
install -pm 644 contrib/tig-completion.bash %{buildroot}%{bashcompl}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.adoc COPYING INSTALL.adoc NEWS.adoc
%doc doc/*.html
%{_bindir}/*
%{_sysconfdir}/tigrc
%{bashcompl}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*

################################################################################

%changelog
* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Single file view enters blame mode on "b"
- Show untracked files in the default view
- Disable graph if log.follow is enabled and there is only one pathspec
- Disable graph for author searches
- git_colors: interpret 'ul' as 'underline'
- Add refname variable
- Add -C option to specify the working directory
- Improve behaviour of auto and periodic refresh modes
- Add support for repos created with git --work-tree
- Add diff-highlight to pager mode
- Show annotated commits in main view
- Introduce reflog view
- Add option to start with cursor on HEAD commit
- Support combined diffs with more than 2 parents
- Improve how a toggle option value is shown on the status line
- Add options to filter refs output
- Update utf8proc to v2.4.0
- Fix garbled cursor line with older ncurses versions
- Fix diff highlighting of removed lines starting with -- and added line
  starting with ++
- Fix loop when displaying search result if regex matches an empty string
- Add synchronous command description in tigrc
- Fix parsing of git rev-parse output
- Propagate --first-parent to diff arguments
- Use proper type for hash table size
- Fix incorrect cppcheck warning about realloc() use
- Don't shift signed int by 31 bits
- Fix Vim going background after running Tig outside of a git repository
- make-builtin-config: use "read -r"
- Fix segfaults with readline 8.0
- Reset state before closing stage view automatically
- Don't use a child view as previous view
- Force reload of VIEW_FLEX_WIDTH views only when needed
- Combined diff uses @@@ as hunk marker
- Fix memory leak induced by 'tig grep'
- Fix memory leak in main view
- Exit gracefully if refs view was defined without ref column
- Fix pager view not moving up when child view is open
- make-builtin-config: Fix unportable sed usage in read_tigrc()
- Properly detect combined diffs

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.1-0
- Add CURSES_CFLAGS to CPPFLAGS.

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Add 'send-child-enter' option to control interaction with child views.
- Update make config defaults for Cygwin to ncurses6.
- Build against netbsd-curses.
- Change the blame view to render more like git-blame(1).
- Improve worktree and submodule support.
- Support running Tig via a Git alias.
- Use ISO-8601 letters for short relative dates.
- Change date formatting to show time zones by default.
- Use utf8proc to handle Unicode characters.
- Fix file(1) argument on Linux used for resolving encodings.
- Fix underflow in the file search.
- Fix line numbers in grep view when scrolled.
- Pass command line args through to the stage view.
- Fix resource leak.
- Fix various compiler warnings and pointer arithmetic.
- Workaround potential null pointer dereferences.
- Bind to single and double quotes by using the and key mappings.
- Make Tig the process-group leader and clean child processes.
- Fix sh compatibility in contrib/tig-pick.
- Fix incorrect behaviour of up and down keys in diff view when opened from diff
  preview.
- Open the stage view when maximizing a split diff view of (un)staged changes.
- Use fully qualified reference name for tags when conflicting with branch name.
- Fix resize not working after entering command.
- Use stack allocated memory to handle TIG_LS_REMOTE.
- Fix deleted file mode line remains highlighted after hovering in diff or stage
  view.
- Fix TIG_LS_REMOTE not working with git-ls-remote(1).

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- Revert "Handle \n like \r (#758)".
- Fix by catching SIGHUP.
- Change refs_tags type to size_t.

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- Fix busy loop detection to handle large repos.

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Restore TTY attributes.
- Handle \n like \r.
- Add workaround that detects busy loops when Tig loses the TTY. This may
  happen if Tig does not receive the HUP signal (e.g. when started with
  nohup).
- Fix compatibility with ncurses-5.4 which caused copy-pasting to not work
  in the prompt.
- tig(1): document correct environment variable.

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- The width setting on the status, text and commit-title columns was
  never applied and has been removed.
- Improve load performance by throttling screen updates.
- Speed up graph rendering.
- Enable scroll optimizations for Terminal.app and iTerm2.
- Improve the test suite portability to not depend on GNU sed.
- Make build reproducible. (https://reproducible-builds.org/)
- Enable binding to more symbolic keys and keys with control modifier:
- F13-F19, ShiftLeft, ShiftRight, ShiftDel, ShiftHome, ShiftEnd,
- ShiftTab, Ctrl-C, Ctrl-V, Ctrl-S, and Ctrl-@.
- Persist readline history to ~/.tig_history or $XDG_DATA_HOME/tig/history.
- Use history-size to control the number of entries to save.
- Preload last search from persistent history.
- Add view-close-no-quit action, unbound by default.
- Add mouse-wheel-cursor option (off by default) when set to true causes
  wheel actions to prefer moving the cursor instead of scrolling.
- Add truncation-delimiter option, set to ~ by default.
- Add -q parameter to source for "source-if-present".
- Add :echo prompt command to display text in the status bar.
- Make diff-highlight colors configurable.
- Let Ctrl-C exit Y/N dialog, menu prompts and the file finder.
- Hide cursor unless at textual prompt.
- Expand tilde ('~') in :script paths.
- Show single-line output of external command in status bar.
- Disable the graph when --no-merges is passed.
- Print backtraces on segfault in debug mode.
- Ignore script lines starting with # (comment).
- Complete repo:* variables when readline is enabled.
- Incorporate XTerm's wcwidth.c to find Unicode widths.
- Fix graph display issues.
- Fix and improve rendering of Unicode characters.
- Handle hyphenated directory names when listing content.
- Do not jump to next match when cancelling the search prompt.
- Fix clearing of the status line after Ctrl-C.
- Fix handling of width on line-number and trimmed width of 1.
- Set cursor position when not updating prompt contents.
- Erase status line at exit time for users without altscreen-capable terminals.
- Fix unexpected keys when restoring from suspend (Ctrl-Z).
  contrib/vim.tigrc: Also bind G in the main as a workaround for limitations of
  the none action.
- Only override blame-options when commands are given and fix parsing of -C.
- Fix diff name discovery to better handle prefixes.
- Interpret button5 as wheel-down.
- Fix back / parent in tree view.
- Fix memory corruption in concat_argv and file finder.
- Fix reading from stdin for tig show.
- Document problem of outdated system-wide tigrc files in Homebrew.
- Repaint the display when toggling line-graphics.
- Fix custom date formatting support longer strings.
- Don't segfault on ":exec" irregular args.
- Fix segfault when calling htab_empty.

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-0
- Use diff-options when preparing the diff in the stage view to make the diff
  state configurable.
- Add 'status-show-untracked-files' option mirroring Git's
- 'status.showUntrackedFiles' to toggle display of untracked files. in the
  status view. On by default.
- Update ax_with_curses.m4 and use pkg-config to detect.
- Add tig-pick script for using Tig as a commit picker.
- Add "smart case" option ('set ignore-case = smart-case') to ignore case when
  the search string is lower-case only.
- Fix author ident cache being keyed by email only.
- Fix periodic refresh mode to properly detect ref changes.
- Add workaround for detecting failure to start the diff-highlight process.
- Show diffs in the stash view when set mailmap = true.
- Fix parsing of git-log revision arguments, such as --exclude=... in
  conjunction with --all.
- Fix diff stat parsing for binary copies.
- Fix crash when resizing terminal while search is in progress.
- Fix argument filtering to pass more arguments through to Git.
- Check for termcap support in split tinfo libs.

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Support Git's 'diff-highlight' program when diff-highlight is set to either
- true or the path of the script to use for post-processing.
- Add navigation between merge commits. (GH #525)
- Add 'A' as a binding to apply a stash without dropping it.
- Bind 'Ctrl-D' and 'Ctrl-U' to half-page movements by default.
- manual: Mention how to change default Up/Down behavior in diff view.
- Reorganize checking of libraries for termcap functions.
- Fix :goto <id> error message.

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- Updated to latest stable release

* Wed Sep  9 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-1
- Improved spec file

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Updated to latest stable release

* Thu Mar 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- Updated to latest stable release

* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- Updated to latest stable release

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Updated to latest stable release

* Thu Dec 19 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- Initial build
