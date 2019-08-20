################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

%define ek_theme_version  1.2.0

################################################################################

Summary:             A small text editor
Name:                nano
Version:             4.3
Release:             0%{?dist}
License:             GPLv3+
Group:               Applications/Editors
URL:                 http://www.nano-editor.org

Source0:             https://www.nano-editor.org/dist/v4/%{name}-%{version}.tar.xz
Source1:             https://github.com/essentialkaos/blackhole-theme-nano/archive/v%{ek_theme_version}.tar.gz

Source100:           checksum.sha512

Patch0:              %{name}-nanorc.patch

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       gcc make automake groff ncurses-devel sed

Requires(post):      /sbin/install-info
Requires(preun):     /sbin/install-info

Provides:            %{name} = %{version}-%{release}

################################################################################

%description
GNU nano is a small and friendly text editor.

################################################################################

%prep
%{crc_check}

%setup -q

tar xzvf %{SOURCE1}

%patch0 -p1

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 0755 %{buildroot}%{_sysconfdir}
install -dm 0755 %{buildroot}%{_root}

install -pm 0644 doc/sample.nanorc %{buildroot}%{_sysconfdir}/nanorc

# Create config for root with red title and status
cp %{buildroot}%{_sysconfdir}/nanorc %{buildroot}%{_root}/.nanorc

sed -i 's/^set titlecolor brightwhite,blue/set titlecolor brightwhite,red/' %{buildroot}%{_root}/.nanorc
sed -i 's/^set statuscolor brightwhite,green/set statuscolor brightwhite,red/' %{buildroot}%{_root}/.nanorc

rm -f %{buildroot}%{_datadir}/%{name}/*.nanorc
cp blackhole-theme-nano-%{ek_theme_version}/*.nanorc \
   %{buildroot}%{_datadir}/%{name}/

rm -f %{buildroot}%{_infodir}/dir

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
  fi
fi

################################################################################

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc doc/sample.nanorc
%config(noreplace) %{_sysconfdir}/nanorc
%config(noreplace) %{_root}/.nanorc
%{_bindir}/nano
%{_bindir}/rnano
%{_mandir}/man1/nano.1.*
%{_mandir}/man1/rnano.1.*
%{_mandir}/man5/nanorc.5.*
%{_infodir}/nano.info*
%{_datadir}/nano
%{_defaultdocdir}/%{name}/*.html

################################################################################

%changelog
* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 4.3-0
- The ability to read from and write to a FIFO has been regained.
- Startup time is reduced by fully parsing a syntax only when needed.
- Asking for help (^G) when using --operatingdir does not crash.
- The reading of a huge or slow file can be stopped with ^C.
- Cut, zap, and copy operations are undone separately when intermixed.
- M-D reports the correct number of lines (zero for an empty buffer).

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 4.2-0
- The integrated spell checker does not crash when 'spell' is missing.
- Option --breaklonglines works also when --ignorercfiles is used.
- Automatic hard-wrapping is more persistent in pushing words to the
  same overflow line.

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 4.1-0
- By default, a newline character is again automatically added at the
  end of a buffer, to produce valid POSIX text files by default, but
  also to get back the easy adding of text at the bottom.
- The now unneeded option --finalnewline (-f) has been removed.
- Syntax files are read in alphabetical order when globbing, so that
  the precedence of syntaxes becomes predictable.
- In the C syntax, preprocessor directives are highlighted differently.
- M-S now toggles soft wrapping, and M-N toggles line numbers.
- The jumpy-scrolling toggle has been removed.
- The legacy keystrokes ^W^Y and ^W^V are recognized again.
- Executing an external command is disallowed when in view mode.
- Problems with resizing during external or speller commands were fixed.

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 4.0-0
- An overlong line is no longer automatically hard-wrapped.
- Smooth scrolling (one line at a time) has become the default.
- A newline character is no longer automatically added at end of buffer.
- The line below the title bar is by default part of the editing space.
- Option --breaklonglines (-b) turns automatic hard-wrapping back on.
- Option --jumpyscrolling (-j) gives the chunky, half-screen scrolling.
- Option --finalnewline (-f) brings back the automatic newline at EOF.
- Option --emptyline (-e) leaves the line below the title bar unused.
- <Alt+Up> and <Alt+Down> now do a linewise scroll instead of a findnext.
- Any number of justifications can be undone (like all other operations).
- When marked text is justified, it becomes a single, separate paragraph.
- Option --guidestripe=<number> draws a vertical bar at the given column.
- Option --fill=<number> no longer turns on automatic hard-wrapping.
- When a line continues offscreen, it now ends with a highlighted ">".
- The halves of a split two-column character are shown as "[" and "]".
- A line now scrolls horizontally one column earlier.
- The bindable functions 'cutwordleft' and 'cutwordright' were renamed
- to 'chopwordleft' and 'chopwordright' as they don't use the cutbuffer.
- The paragraph-jumping functions were moved from Search to Go-to-Line.
- Option --rebinddelete is able to compensate for more misbindings.
- Options --morespace and --smooth are obsolete and thus ignored.
- The --disable-wrapping-as-root configure option was removed.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 3.2-0
- syntax: python: do not highlight 'print' and 'exec' in Python 3
- bindings: allow using <Enter> to exit from the linter
- bindings: allow using ^X to exit from the linter
- bindings: drop M-| as a keystroke for 'cutwordleft' -- set it free again
- bindings: in tiny version with help, don't show unfunctional M-◀ and M-▶
- bindings: make <Alt+Up> and <Alt+Down> work also on a Linux console
- bindings: make the linter separately accessible, through M-B by default
- bindings: make the Shift+arrow keys work by default on more terminals
- bindings: no longer bind F13 and F14 and F15
- bindings: recognize ASCII DEL as backspace also in viewer and browser
- bindings: recognize <Ctrl+Shift+Delete> also on a Linux console
- bindings: rename 'prevhistory' to 'older' and 'nexthistory' to 'newer'
- bindings: stop binding <Bsp> to do_backspace() in the browser menu
- bindings: when implanting a string, make sure to use positive values
- build: exclude scrolling functions only from tiny version without help
- build: fix compilation again when configured with --enable-tiny
- build: fix compilation when configured with --disable-multibuffer
- build: verify that --enable-tiny compiles before allowing a release
- bump version numbers and add a news item for the 3.1 release
- debug: report for which modified editing keys ncurses has no keycode
- display: correct a mistaken label in the help lines of the browser
- display: ensure that the help lines are shown when in linting mode
- display: let the title bar show when nano is in linting mode
- display: show the cursor also in a help text (when --showcursor is used)
- display: use a different color when showing a linting message
- docs: document the slightly changed workings of the --view option
- docs: give suggestions for alternative key bindings in the sample nanorc
- docs: remove a no-longer-needed suggestion from the sample nanorc
- docs: update the description of -R/--restricted, as it now reads nanorc
- docs, usage: mention that --showcursor now covers help texts too
- feedback: give proper message for ^R when combining --view & --restricted
- gnulib: update to its current upstream state
- help: add a relevant explanatory text for the linter
- help: move the linter to the end, to restore pairing in the help lines
- help: pull "Older" and "Newer" into view on an 80-column terminal
- help: restore the blank line between manipulation and position stuff
- help: show <PgUp> and <PgDn> instead of F7 and F8 for pagewise scrolling
- help: show the keystroke <Ctrl+Shift+Delete> as "Sh-^Del"
- linter: allow using <Ctrl+Up> and <Ctrl+Down> to jump to other message
- linter: do not pause when there are no messages for unopened files
- linter: for "first"/"last", reshow actual message after a short pause
- options: --ignorercfiles is now available in restricted mode
- options: let view mode activate "multibuffer" to allow viewing more files
- speller: remove a pointless message -- it is never seen
- startup: allow reading nanorc in restricted mode, to permit customization
- syntaxes: remove several redundant end-of-line anchors from regexes
- tweaks: add a comment, and correct an indentation
- tweaks: add two more translator hints
- tweaks: capitalize the word "nano" when at the start of a sentence
- tweaks: change a bunch of URLs to use 'https' instead of 'http'
- tweaks: condense a handful of comments, and drop an assert
- tweaks: condense another bit of code
- tweaks: define a symbol to make the code itself a little simpler
- tweaks: don't bother asking ncurses for keycodes for shifted Left/Right
- tweaks: drop a check for the needle (the search string) being empty
- tweaks: drop the checking of two flags that can no longer be toggled
- tweaks: elide a function that is used just once and is a oneliner
- tweaks: elide a wrapper function that is no longer useful
- tweaks: exclude word-deletion keystrokes from the tiny version
- tweaks: fold a few pairs of regexes into each other
- tweaks: group a series of related variables together
- tweaks: improve two comments, and reshuffle a line for consistency
- tweaks: include an extra function call only where it is needed
- tweaks: move all the function keys to the end of the shortcuts list
- tweaks: move some calls of edit_redraw() to where they are needed
- tweaks: redefine MMOST to exclude MBROWSER, to simplify the bindings
- tweaks: reduce some repetitious and superfluous comments to just one
- tweaks: remove a check that was made redundant by the previous commit
- tweaks: remove a now-unused parameter from four functions
- tweaks: remove an unneeded check for NULL, and rename a parameter
- tweaks: remove a stray file that was accidentally comitted
- tweaks: remove some old debugging code
- tweaks: rename a bunch of variables, to make it clearer what they contain
- tweaks: rename a flag, to match the name of the option
- tweaks: rename a variable, to be a bit more fitting
- tweaks: renumber a couple of symbols, and reshuffle a bit of code
- tweaks: reorder some code to put backward motion before the forward one
- tweaks: reshuffle a couple of conditions, to group things better
- tweaks: reshuffle some conditions, putting the least likely one first
- tweaks: reshuffle some lines to get standard order (first up, then down)
- tweaks: reshuffle some lines, to put things in order of option name
- tweaks: snip trailing whitespace that ended with a non-breaking space
- tweaks: stop setting and requiring the Meta flag for special keycodes
- tweaks: swap and reword two bullet points in the rnano manpage
- tweaks: there is no reason to block SIGWINCHes while waiting for speller
- undo: move another piece of checking to the two places that need it
- undo: move some special checking code to the one place that needs it
- wrapping: make the --fill option override 'set fill' again
- bindings: hard-bind the zap function to M-Del (Alt+Delete)
- display: make all dying messages end in a newline
- linter: throttle "first"/"last" message on repeated key presses
- new feature: a bindable 'zap', to erase text without changing cutbuffer
- options: add --zap, that makes <Bsp> and <Del> erase a marked region
- display: do spotlighting as part of drawing the screen
- docs: update rnano manpage, as -R/--restricted now reads nanorc
- input: don't detect <Ctrl+Shift+Delete> on Linux console in tiny version
- input: properly consume a modified Delete key also in the tiny version
- input: properly recognize Alt+Delete when using -K/--rebindkeypad
- input: recognize some escape sequences for <Shift+Delete>
- speller: restore the mark coordinates slightly later
- syntax: nanohelp: properly color the keystroke "Sh-^Del"
- tweaks: don't define controldelete or controlshiftdelete in tiny version
- tweaks: join two lines, and add a clarifying comment
- tweaks: move the justifying of a single paragraph into its own function
- tweaks: normalize the indentation of the shuffled code
- tweaks: reshuffle some code to avoid several checks for having justified
- tweaks: simplify by using a 'do/while' loop instead of 'while (TRUE)'
- weeding: remove the 'active' parameter from spotlight()
- wrapping: make relative fill values work again also for screen resizes

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- bindings: bind ASCII DEL during startup instead of repeatedly at runtime
- bindings: make ^H rebindable also on NetBSD, FreeBSD and macOS
- bindings: when Ctrl+Shift+Delete has no keycode, don't use KEY_BSP
- bump version numbers and add a news item for the 3.1 release
- input: keep the cursor in edit window after message, also on NetBSD
- input: recognize the sequences for Ctrl+Shift+Delete on xterm and urxvt
- main: allow toggling all editor features when in view mode
- suspension: don't try to show the cursor position when going to sleep
- syntax: sh: let the header regex match also busybox shell scripts
- tweaks: condense a bit of code
- tweaks: remove a superfluous comment and a redundant assignment
- tweaks: rename a variable to be special and distinct
- tweaks: sharpen an optimization, to allow DEL to be a shortcut
- search: disallow switching to the Replace prompt when in view mode

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- bindings: bind M-Q to 'findprevious' by default, and M-W to 'findnext'
- bindings: hard-bind <Ctrl+Shift+Delete> to 'cutwordleft'
- bindings: make ^Q and M-Q available also in the help viewer
- bindings: move the noconvert toggle from the main to the insert menu
- bindings: reassign the M-| keystroke to 'cutwordleft' by default
- bindings: remove backup and new-buffer toggles (M-B, M-F) from main menu
- bindings: remove the More-Space toggle entirely
- bindings: remove the 'searchagain' function entirely
- bindings: rename two bindable functions: copytext to copy, uncut to paste
- bindings: unassign the M-? keystroke, to free it up for future use
- build: add the release script to the repository
- build: fix compilation again when configured with --enable-tiny
- build: fix compilation when configured with --enable-tiny
- build: verify that 'msgfmt' is available when building from git
- bump version numbers and add a news item for the 3.0 release
- chars: make the UTF-8 case ever so slightly faster by eliding an 'if'
- chars: speed up the counting of string length for the plain ASCII case
- chars: speed up the parsing of a character for the plain ASCII case
- completion: when the cursor is not after a word fragment, say so
- cut: concentrate the logic for clearing the cutbuffer mostly in one place
- cutting: when deleting whole words, don't join lines unexpectedly
- debug: add some code to time the performance of get_totsize()
- docs: improve a comment about rebinding <Backspace>
- docs: mention that also Ctrl increases the stride when selecting text
- docs: mention that "normal" can be used to give things the default color
- docs: mention that the 'formatter' command has been superseded
- docs: reshuffle a bindable function to a slightly better position
- docs: say that 'cutwordright' is now bound to <Ctrl+Delete> by default
- docs: slightly reword the description of four bindable functions
- docs: the 'noconvert' bindable function was renamed to 'flipconvert'
- dropping a feature: remove the ability to use the 'formatter' command
- easter: show the crawl only when there is room enough for the lines
- files: add the file format on the status bar when switching buffers
- filtering: wait for the data-sending process to terminate too
- gnulib: update to its current upstream state
- help: for ^R^X, mention that the buffer can be piped to the command
- help: move "Search Again" away from "Find Next" and "Find Previous"
- input: consume the whole escape sequence for modified PgUp and PgDn keys
- input: fully consume modified PgUp and PgDn keys also in the tiny version
- input: ignore any <Escape>s before a valid command keystroke
- input: stop <Alt+Insert> from entering "3~" into the buffer
- input: stop a modified Delete key from entering stuff into the buffer
- mouse: put the row/column arguments in the proper order  [coverity scan]
- prompt: concentrate manipulations of 'statusbar_x' into a single file
- prompt: remove redundant redrawings of the prompt bar
- rcfile: allow to rebind the Cancel function in the yesno menu
- rcfile, docs: no longer recognize nor mention 'set backwards'
- rcfile: do not accept rebinding F0 nor function keys above F16
- rcfile: ensure that in the yesno menu Cancel is bound to some keystroke
- rcfile: explicitly check for disallowed keywords in included files
- rcfile: reject things like "M-Del" and "^{" as invalid key names
- rcfile: when a vital function is not mapped, mention in which menu
- search: include 'findprevious' and 'findnext' in the tiny version
- signals: don't call a print routine in a signal handler
- speller: do not replace the text when the temporary file did not change
- startup: don't overwrite rcfile error messages on a Linux console
- startup: show the correct number of lines when opening multiple files
- syntax: awk: recognize any {g,m,n,}awk script also by its shebang line
- syntax: default: colorize also two-digit and capitalized nano versions
- syntaxes: remove all traces of the 'formatter' command
- syntax: nanorc: recognize 'yesno' as a valid menu to bind/unbind keys in
- syntax: nanorc: show ^@ as validly rebindable, but not any ^digit
- syntax: python: avoid coloring the three special values inside strings
- text: add auto-whitespace to the file size after creating the undo item
- tweaks: adjust indentation after the previous change
- tweaks: adjust one more translator hint, for removed toggles
- tweaks: adjust some translator hints for past changes, and add two more
- tweaks: adjust two comments, to be more accurate and general
- tweaks: avoid dereferencing a pointer when it is NULL  [coverity scan]
- tweaks: close a temp file only when descriptor is valid  [coverity scan]
- tweaks: correct a comment, rewrap a line, and drop some debugging stuff
- tweaks: delete some old debugging code that no longer seems useful
- tweaks: don't bother having debug code that deallocates all memory
- tweaks: don't call va_start() without calling va_end()  [coverity scan]
- tweaks: drop a condition that has been made redundant two commits ago
- tweaks: drop some old debugging code
- tweaks: elide a bunch of unneeded constant strings
- tweaks: elide a function that is used just once
- tweaks: elide another function that is used just once
- tweaks: elide an unneeded/duplicate variable
- tweaks: elide a one-line function -- no, a half-line function
- tweaks: elide a subfunction that is used just once
- tweaks: exclude a global flagging variable when it is not needed
- tweaks: exclude the file-prepending code from the tiny version
- tweaks: fix a pasting error from a month ago
- tweaks: implement the name-to-menu function in another manner
- tweaks: improve a couple of comments in the sample nanorc
- tweaks: improve a translator hint and some other comments
- tweaks: move a call to where it will be executed  [coverity scan]
- tweaks: normalize the indentation after the previous change
- tweaks: properly escape "\" in a man page and "@" in a texi document
- tweaks: recognize escape sequences of modified Ins/Del more precisely
- tweaks: reduce the counting of characters to just the needed function
- tweaks: remove a redundant "struct" word, and replace it in comments
- tweaks: remove a superfluous condition and a redundant refresh
- tweaks: remove redundant braces and conditions after the previous change
- tweaks: remove some braces that are now superfluous
- tweaks: remove some ineffectual parts from header-line regexes
- tweaks: remove the superfluous calls that reset the mbtowc() state
- tweaks: remove two needless words, and split up a changed text further
- tweaks: remove two superfluous assignments
- tweaks: rename a constant, to match what it actually means
- tweaks: rename a function and place its call better
- tweaks: rename a function to better match its counterpart
- tweaks: rename a function, to better state what it does
- tweaks: rename a variable and a function, for more clarity
- tweaks: rename a variable, to better match its task
- tweaks: reshuffle some lines, in order to elide one
- tweaks: reshuffle the order of the bindings, for help-line esthetics
- tweaks: show "Space" and "Bsp" in the help text of the browser
- tweaks: slightly improve error message when vital function is unmapped
- tweaks: use a shorter message, because when the screen is small...
- undo: differentiate between general filtering and spell checking
- input: give feedback for all unbound keys also in the help viewer
- statusbar: elevate three messages to an ALERT, to make them more visible
- tweaks: correct four spaces of indentation to a tab, in two places
- tweaks: remove the 'bright' field from the colortype struct
- bindings: make "n" work again in file browser and help viewer
- bindings: make ^Q start a backward search also in the file browser
- docs: mention that "Ins" and "Del" are valid rebindable keys
- justify: verify being in a paragraph before trying to find its beginning
- speller: hook up a full alternative spellcheck to the undo system
- speller: hook up a marked-text alternative spellcheck to the undo system
- speller: make replace_buffer() use the cutting functions directly
- speller: make replace_marked_buffer() use the cutting functions directly
- undo: actually enable undoing/redoing an alternative spellcheck
- undo: always initialize the 'newsize' element in the undo struct
- undo: position the cursor properly when undoing/redoing magicline cuts
- undo: restore the cursor position when a cut and paste are paired
- undo: store the correct cursor position after a paired cut+insert
- files: speed up reading by using getc_unlocked() instead of getc()
- syntax: sh: recognize more file extensions and header lines
- input: erase the next word when Ctrl is held while pressing Delete
- build: fix compilation when CC=tcc
- syntax: lua: do not color strings inside comments, and add a linter

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 2.9.8-0
- build: fix compilation failure when configured with --enable-tiny
- build: fix compilation when configured with --disable-justify
- build: fix compilation when configured with --disable-multibuffer
- build: fix compilation with --enable-{tiny,help,multibuffer}
- bump version numbers and add a news item for the 2.9.8 release
- copyright: update the years for significantly changed files
- credits: sort the names roughly according to amount of influence
- docs: add a missing double quote in the default brackets string
- docs: describe what constitutes a paragraph
- docs: improve description of 'speller' and related bindable functions
- docs: improve the description of --nonewlines, and properly sort it
- docs: improve the description of the --autoindent option
- docs: make quotes around regexes bold, as they are part of the command
- docs: mark the filtering of text through an external command as done
- docs: register Marco as the author of the filtering feature
- docs: remove mention of the quotestr for when regex support is lacking
- docs: remove quotes around the name of a syntax -- they are not needed
- docs: thank Kamil for his bug fixes, and update an email address
- docs, usage: make it clear that the argument of --quotestr is a regex
- files: give feedback during writeout also when prepending or appending
- filtering: pair the cut and the insert, so they can be undone together
- gnulib: update to its current upstream state
- justification: find the beginning of a paragraph in a better way
- justification: limit the amount of recursion to prevent a stack overflow
- justification: recognize indented paragraphs also without --autoindent
- justification: when leading whitespace exceeds fill width, wrap anyway
- linter: don't try to access absent stat info, as that gives a crash
- linter: make sure that the margin is updated before displaying a buffer
- linter: make sure the shortcuts bar will redrawn when exiting early
- main: add "/" to the quoting regex, to allow justifying //-comments
- main: interpret only a double slash (//) as quoting, not a single one
- rcfile: don't crash when a bind to a string lacks the closing quote
- startup: provide a hint for people unfamiliar with the ^char convention
- syntaxes: condense and/or correct some extension regexes
- syntax: makefile: color all keywords that GNU make recognizes
- tweaks: adjust a translator hint
- tweaks: avoid an unused-variable warning with --enable-tiny
- tweaks: avoid a warning with --enable-{tiny,help,multibuffer}
- tweaks: condense a comment, and elide an unneeded 'if'
- tweaks: condense some repetitious comments, and check before assigning
- tweaks: condense two statements into one, and elide a 'break'
- tweaks: elide a function that is called just once
- tweaks: elide another function that is called just once
- tweaks: exclude an unneeded 'if' from the single-buffer version
- tweaks: frob a couple of comments
- tweaks: frob some comments, and rename two parameters to make sense
- tweaks: give some continuation lines a more obvious indentation
- tweaks: improve a couple of comments, and reshuffle a group of lines
- tweaks: make better use of an existing variable
- tweaks: make better use of an intermediate variable
- tweaks: reduce the abundance of the word 'toggle' in the Info manual
- tweaks: remove a superfluous assignment -- the lead length never changes
- tweaks: remove two superfluous checks, after making one of them so
- tweaks: rename a function, for more aptness and extra contrast
- tweaks: rename a variable, for contrast, and improve two comments
- tweaks: rename a variable, to give it some meaning
- tweaks: rename two variables, to better fit their tasks
- tweaks: reshuffle a condition, and adjust a comment and some indentation
- tweaks: reshuffle a couple of assignments
- tweaks: simplify the determining of the prefix for justified lines
- tweaks: stop decreasing both the iterator and the limit of a loop
- tweaks: use a more meaningful variable name, and avoid a distant 'else'
- wrapping: use "smart" autoindenting only when hard-wrapping is enabled
- wrapping: when autoindenting, use indentation of next line as example
- tweaks: avoid two unused variable warnings when NLS is disabled
- syntax: makefile: recognize also an all-lowercase makefile name
- bindings: add the "flippipe" bindable function
- tweaks: avoid an unused variable warning with --enable-tiny
- tweaks: fix some grammar plus a typo in the comments
- linter: check all open buffers, instead of just the next one
- new feature: allow piping (selected) text to an external command
