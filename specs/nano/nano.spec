################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _root  /root

################################################################################

%define ek_theme_version  1.5.0

################################################################################

Summary:          A small text editor
Name:             nano
Version:          8.4
Release:          0%{?dist}
License:          GPLv3+
Group:            Applications/Editors
URL:              https://www.nano-editor.org

Source0:          https://www.nano-editor.org/dist/v8/%{name}-%{version}.tar.xz
Source1:          https://kaos.sh/blackhole-theme-nano/%{ek_theme_version}.tar.gz

Source100:        checksum.sha512

Patch0:           %{name}-nanorc.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    gcc make automake ncurses-devel sed

Requires(post):   /sbin/install-info
Requires(preun):  /sbin/install-info

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
GNU nano is a small and friendly text editor.

################################################################################

%prep
%crc_check
%autosetup -p1

tar xzvf %{SOURCE1}

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

sed -i 's/^set titlecolor normal,blue/set titlecolor normal,red/' %{buildroot}%{_root}/.nanorc
sed -i 's/^set statuscolor normal,green/set statuscolor normal,red/' %{buildroot}%{_root}/.nanorc

rm -f %{buildroot}%{_datadir}/%{name}/*.nanorc
cp blackhole-theme-nano-%{ek_theme_version}/*.nanorc \
   %{buildroot}%{_datadir}/%{name}/

rm -f %{buildroot}%{_infodir}/dir

%find_lang %{name}

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
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 8.4-0
- Bracketed pastes over a slow connection are more reliable.
- Tabs in an external paste at a prompt are not dropped.
- Feedback occurs when the cursor sits on a Byte Order Mark.
- The Execute prompt is more forgiving of a typo.

* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 8.3-0
- A build failure with gcc-15 is fixed.
- Several translations were updated.

* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 8.2-0
- At a Yes-No prompt, beside Y and the localized initial for "Yes",
  also ^Y is accepted. Similarly, ^N for "No", and ^A for "All".
- A text-highlighting bug with Alt+Home/Alt+End is fixed.

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 8.1-0
- The idiom nano filename:linenumber is understood only when
  the option --colonparsing (or 'set colonparsing') is used.
- Modern bindings are not activated when nano's invocation name
  starts with "e", as it jars with Debian's alternatives system.
- New bindable function 'cycle' first centers the current row,
  then moves it to the top of the viewport, then to the bottom.
  It is bound by default to ^L.
- Option --listsyntaxes/-z lists the names of available syntaxes.


* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 8.0-0
- By default ^F is bound to starting a forward search, and ^B to
  starting a backward search, while M-F and M-B repeat the search
  in the corresponding direction. (See the documentation if you
  want the old bindings back.)
- Command-line option --modernbindings (-/) makes ^Q quit, ^X cut,
  ^C copy, ^V paste, ^Z undo, ^Y redo, ^O open a file, ^W write a file,
  ^R replace, ^G find again, ^D find again backwards, ^A set the mark,
  ^T jump to a line, ^P show the position, and ^E execute.
- Above modern bindings are activated also when the name of
  nano's executable (or a symlink to it) starts with the letter "e".
- To open a file at a certain line number, one can now use also
  nano filename:number, besides nano +number filename.
- <Alt+Home> and <Alt+End> put the cursor on the first and last
  row in the viewport, while retaining the horizontal position.
- When the three digits in an #RGB color code are all the same,
  the code is mapped to the xterm grey scale, giving access to
  fourteen levels of grey instead of just four.
- For easier access, M-" is bound to placing/removing an anchor,
  and M-' to jumping to the next anchor.
- Whenever an error occurs, the keystroke buffer is cleared, thus
  stopping the execution of a macro or a string bind.
- The mousewheel scrolls the viewport instead of moving the cursor.


* Sat Feb 18 2023 Anton Novojilov <andy@essentialkaos.com> - 7.2-0
- <Shift+Insert> is prevented from pasting in view mode.

* Sun Dec 25 2022 Anton Novojilov <andy@essentialkaos.com> - 7.1-0
- When --autoindent and --breaklonglines are combined, pressing
  <Enter> at a specific position no longer eats characters.

* Thu Dec 01 2022 Anton Novojilov <andy@essentialkaos.com> - 7.0-0
- String binds may contain bindable function names between braces.
  For example, to move the current line down to after the next one:
  bind ^D "{cut}{down}{paste}{up}" main. Of course, braced function
  names may be mixed with literal text. If an existing string bind
  contains a literal {, replace it with {{}.
- Unicode codes can be entered (via M-V) without leading zeroes,
  by finishing short codes with <Space> or <Enter>.
- Word completion (^]) looks for candidates in all open buffers.
- No regular expression matches the final empty line any more.

* Sun Oct 09 2022 Anton Novojilov <andy@essentialkaos.com> - 6.4-1
- Improved color theme

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 6.4-0
- The file browser does not crash when moving up to the root folder.
- Softwrapping very long lines is done more efficiently.
- Invoking the formatter does not blink the screen.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 6.3-0
- For multiline regexes, text is now colored as soon as a start match
  is found, also when there is no end match at all.
- The colorizing of any line is stopped after two thousand bytes,
  to avoid frustrating delays.
- When environment variable NO_COLOR is set, the two default colors
  (yellow for the spotlight, red for error messages) are suppressed
  when no interface colors are specified in a nanorc file.
- Full justification and piping the whole buffer through a command
  now keep the cursor at the same line number.
- Utility xsel can be used to copy a marked region to the system's
  clipboard.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 6.2-0
- The file browser clears the prompt bar also when using --minibar.
- Linting now works also with a newer 'pyflakes'.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 6.1-0
- The behavior of ^K at a prompt has been enhanced: when there
  is text after the cursor, just this text is erased. (In the usual
  situation, however, when the cursor is at the end of the answer,
  the behavior is as before: the whole answer is erased.)
- At a prompt, M-6 copies the current answer into the cutbuffer.
- Large external pastes into nano are handled more quickly.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 6.0-0
- Option --zero hides the title bar, status bar and help lines, and
  uses all rows of the terminal as editing area. The title bar and
  status bar can be toggled with M-Z.
- Colors can now be specified also as three-digit hexadecimal numbers,
  in the format #rgb. This picks from the 216 index colors (that most
  terminals know) the color that is nearest to the given values.
- For users who dislike numbers, there are fourteen new color names:
  rosy, beet, plum, sea, sky, slate, teal, sage, brown, ocher, sand,
  tawny, brick, and crimson.
- Suspension is enabled by default, invokable with ^T^Z. The options
  -z, --suspendable, and 'set suspendable' are obsolete and ignored.
  (In case you want to be able to suspend nano with a single keystroke,
  you can put 'bind ^Z suspend main' in your nanorc.)
- When automatic hard-wrapping is in effect, pasting just a few words
  (without a line break) will now hard-wrap the line when needed.
- Toggling Append or Prepend clears the current filename.
- The word count as shown by M-D is now affected by option --wordbounds;
  with it, nano counts words as 'wc' does; without it (the new default),
  words are counted in a more human way: seeing punctuation as space.
- The YAML syntax file is now actually included in the tarball.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.9-0
- The extension of a filename is added to the name of a corresponding
  temporary file, so that spell checking a C file, for example, will check
  only the comments and strings (when using 'aspell').
- The process number is added to the name of an emergency save file,
  so that when multiple nanos die they will not fight over a filename.
- Undoing a cutting operation will restore an anchor that was located
  in the cut area to its original line.
- When using --locking, saving a new buffer will create a lock file.
- Syntax highlighting for YAML files has been added.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.8-0
- After a search, the spotlighting is dropped after 1.5 seconds (0.8
  seconds with --quick) to avoid the idea that the text is selected.
- A + and a space before a filename on the command line will put
  the cursor at the end of the corresponding buffer.
- Linter messages no longer include filename and line/column numbers.
- Color name "grey" or "gray" can be used instead of "lightblack".
- The color of the minibar can be chosen with 'set minicolor'.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.7-0
- The output of --constantshow (without --minibar) is more stable.
- When opening multiple buffers and there is an error message, this
  message is shown again upon first switch to the relevant buffer.
- The position and size of the indicator now follow actual lines,
  instead of visual lines when in softwrap mode, meaning that the
  size of the indicator can change when scrolling in softwrap mode.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.6.1-0
- Search matches are properly colorized in softwrap mode too.
- Option 'highlightcolor' has been renamed to 'spotlightcolor'.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.6-0
- A search match gets highlighted (in black on yellow by default),
  in addition to placing the cursor at the start of the match.
- The color combination can be changed with 'set highlightcolor'.
- By default the cursor is hidden until the next keystroke, but
  it can be forced on with --showcursor / 'set showcursor'.
- Option --markmatch / 'set markmatch' has been removed.
- Cursor position and character code are displayed in the minibar
  only when option --constantshow / 'set constantshow' is used,
  and their display can be toggled with M-C.
- The state flags are displayed in the minibar only when option
  --stateflags / 'set stateflags' is used.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.5-0
- Option 'set minibar' makes nano suppress the title bar and instead
  show a bar with basic editing information at the bottom: file name
  (plus an asterisk when the buffer is modified), the cursor position
  (line,column), the character under the cursor (U+xxxx), the flags
  that --stateflags normally shows, plus the percentage of the buffer
  that is above the cursor.
- With 'set promptcolor' the color combination of the prompt bar can
  be changed, to allow contrasting it with the mini bar (which always
  has the same color as the title bar).
- Option 'set markmatch' highlights the result of a successful search
  by putting the mark at the end of the match, making the match more
  visible. It also suppresses the cursor until the next keystroke.
  (If you dislike the hiding of the cursor, use 'set showcursor'.)
- The bindable toggle 'nowrap' has been renamed to 'breaklonglines',
  to match the corresponding option, like for all other toggles.
- Support for Slang has been removed.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.4-0
- Moving the cursor now skips over combining characters (and
  other zero-width characters). Deleting a character deletes
  also any succeeding zero-width characters, but backspacing
  deletes just one character at a time.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.3-0
- Option 'set stateflags' makes nano show the state of auto-indenting,
  the mark, hard-wrapping, macro recording, and soft-wrapping in the
  title bar. The flags take the place of "Modified", and a modified
  buffer is instead indicated by an asterisk (*) after its name.
- Nano no longer by default tries using libmagic to determine the type
  of a file (when neither filename nor first line gave a clue), because
  in most cases it is a waste of time. It requires using the option
  --magic or -! or 'set magic' to make nano try libmagic.
- The color of the indicator can be changed with 'set scrollercolor'.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.2-0
- Making certain replacements after a large paste does not crash.
- Hitting a toggle at the Search prompt does not clear the answer.
- Using --positionlog does not complain at the first start.
- A macro containing a Search command will not sometimes fail.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.1-0
- M-Bsp (Alt+Backspace) deletes a word backwards, like in Bash.
- M-[ has become bindable. (Be careful, though: as it is the
  starting combination of many escape sequences, avoid gluing
  it together with other keystrokes, like in a macro.)
- With --indicator and --softwrap, the first keystroke in an
  empty buffer does not crash.
- Invoking the formatter while text is marked does not crash.
- In UTF-8 locales, an anchor is shown as a diamond.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 5.0-0
- With --indicator (or -q or 'set indicator') nano will show a kind
  of scrollbar on the righthand side of the screen to indicate where
  in the buffer the viewport is located and how much it covers.
- With <Alt+Insert> any line can be "tagged" with an anchor, and
  <Alt+PageUp> and <Alt+PageDown> will jump to the nearest anchor.
- When using line numbers, an anchor is shown as "+" in the margin.
- The Execute Command prompt is now directly accessible from the
  main menu (with ^T, replacing the Spell Checker). The Linter,
- Formatter, Spell Checker, Full Justification, Suspension, and
  Cut-Till-End functions are available in this menu too.
- On terminals that support at least 256 colors, nine new color
  names are available: pink, purple, mauve, lagoon, mint, lime,
  peach, orange, and latte. These do not have lighter versions.
- For the color names red, green, blue, yellow, cyan, magenta,
  white, and black, the prefix 'light' gives a brighter color.
- Prefix 'bright' is deprecated, as it means both bold AND light.
- All color names can be preceded with "bold," and/or "italic,"
  (in that order) to get a bold and/or italic typeface.
- With --bookstyle (or -O or 'set bookstyle') nano considers any
  line that begins with whitespace as the start of a paragraph.
- Refreshing the screen with ^L now works in every menu.
- In the main menu, ^L also centers the line with the cursor.
- Toggling the help lines with M-X now works in all menus except
  in the help viewer and the linter.
- At a filename prompt, the first <Tab> lists the possibilities,
  and these are listed near the bottom instead of near the top.
- Bindable function 'curpos' has been renamed to 'location'.
- Long option --tempfile has been renamed to --saveonexit.
- Short option -S is now a synonym of --softwrap.
- The New Buffer toggle (M-F) has become non-persistent. Options
  -multibuffer and 'set multibuffer' still make it default to on.
- Backup files will retain their group ownership (when possible).
- Data is synced to disk before "... lines written" is shown.
- The raw escape sequences for F13 to F16 are no longer recognized.
- Distro-specific syntaxes, and syntaxes of less common languages,
  have been moved down to subdirectory syntax/extra/. The affected
  distros and others may wish to move wanted syntaxes one level up.
- Syntaxes for Markdown, Haskell, and Ada were added.

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 4.9.3-0
- When justifying a selection, the new paragraph and the
  succeeding one get the appropriate first-line indent.
- Trying to justify an empty selection does not crash.
- Redoing the insertion of an empty file does not crash.
- On the BSDs and macOS, ^H has become rebindable again
  (in most terminal emulators, not on the console).
- DOS line endings in nanorc files are accepted.
- Option --suspend / 'set suspend' has been renamed to
  the more logical --suspendable / 'set suspendable'.

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 4.8-0
- When something is pasted into nano, auto-indentation is suppressed,
  and the paste can be undone as a whole with a single M-U.
- When a lock file is encountered during startup, pressing ^C/Cancel
  quits nano. (Pressing 'No' just skips the file and continues.)
- Shift+Meta+letter key combos can be bound with 'bind Sh-M-letter'.
- Making any such binding dismisses the default behavior of ignoring
- Shift for all Meta+letter keystrokes.
- The configuration option --with-slang (to be avoided when possible)
  can now be used only together with --enable-tiny.
- A custom nanorc file can be specified on the command line, with
  -f filename or --rcfile=filename.

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 4.7-0
- build: add the uploading of PDF and cheatsheet to the release script
- build: avoid three compiler warnings when using gcc-9.2 or newer
- build: fix compilation for --enable-tiny --enable-wrapping
- build: fix compilation on macOS, where 'st_mtim' is unknown
- build: fix compilation when configured with --disable-justify
- bump version numbers and add a news item for the 4.7 release
- display: don't color the space that separates line numbers from text
- docs: add or improve the 'description' meta tag in the two HTML pages
- docs: add the 'lang' attribute in the right place to the two HTML pages
- docs: mention that all keywords in a nanorc file should be in lowercase
- docs: mention that a negative number after "+" counts from the end
- gnulib: update to its current upstream state
- input: make <Tab> indent only when mark and cursor are on different lines
- justify: distinguish between tabs and spaces when comparing indentation
- justify: treat consecutive indentations that look the same as the same
- linter: beep when trying to go beyond first or last message
- rcfile: accept also function names and menu names only in lowercase
- rcfile: accept only keywords in all lowercase, for speed of comparison
- rcfile: demand that function 'exit' is bound in the file browser
- syntax: nanohelp: colorize also ^/ as a possible keystroke
- syntax: sh: recognize shell rc files also in dedicated directories
- tweaks: avoid using strlen() where it is not needed
- tweaks: drop M-Space and ^Space from the browser's key list
- tweaks: improve two comments and the ordering of some operands
- tweaks: move three functions to the file where they are used
- tweaks: optimize the trimming of trailing whitespace
- tweaks: remove a stray space
- tweaks: rename a function, to get out of the way for another rename
- tweaks: rename a function, to get rid of a useless suffix
- tweaks: reshuffle a few lines, for brevity or speed or consistency
- tweaks: reshuffle a few lines, for symmetry with the preceding function
- tweaks: reshuffle a fragment of code, for efficiency
- tweaks: reshuffle and rename a few things, to elide duplication
- tweaks: reshuffle an item, to avoid a lone 'else'
- tweaks: reshuffle two declarations, for compactness
- tweaks: slightly streamline the search for a possible wrapping point
- tweaks: trim or adjust some whitespace in HTML, and add two keywords
- tweaks: unwrap a few lines, and move some strings to among their peers
- wrapping: never break in the quoting part nor in the indentation part

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 4.6-0
- bindings: allow to rebind ^/, even though it is synonymous with ^_
- bindings: don't hard-bind ^H in the help viewer or the file browser
- bindings: the 'all' keyword should encompass the browser menu too
- bindings: the 'all' keyword should include the browser menu always
- build: fix compilation for --enable-tiny --enable-histories
- build: fix compilation when configured with --disable-color
- build: slightly speed up the compilation of the tiny version
- bump version numbers and add a news item for the 4.6 release
- chars: add a faster version of the character-parsing function
- commands: rename 'fixer' to 'formatter', to be less misleading
- cutting: do nothing when trying to chop a word leftward at start of file
- display: do refresh the edit window when exiting from the help viewer
- docs: add a note saying that rebinding ^M or ^I is not advisable
- docs: add the M-F and M-N keystrokes to the cheatsheet
- docs: adjust the compilation instructions to two-digit version numbers
- docs: correct the description of the 'spell' menu
- docs: document the 'fixer' command, a per-syntax content arranger
- docs: mention that color rules are applied in the order they are listed
- docs: mention that 'hunspell' is now the first default spelling program
- docs: mention that the 'nopauses' option is obsolete
- docs: remove some excessive detail from the sample nanorc file
- docs: remove the note about the formatter having been removed
- feedback: say it when spell check or manipulation did not change anything
- files: distinguish between read error and write error when prepending
- files: don't mention the name of the temp file when reading goes wrong
- files: when opening a file for copying, it should NOT be created
- formatter: accept the formatted result also upon a nonzero exit status
- formatter: don't let output from the program pollute the screen
- gnulib: update to its current upstream state
- history: don't wait when there is something wrong with the history files
- linter: report it as an error when running the linting program fails
- rcfile: allow binding also F17...F24
- rcfile: process extensions to file-matching commands straightaway
- restored feature: a per-syntax 'fixer' command that processes the buffer
- softwrap: when switching to another buffer, re-align the starting column
- speller: prefer 'hunspell' over 'spell', because it can handle UTF-8
- speller: when 'spell' is not found, try running 'hunspell -l' instead
- statusbar: show only the first error message, with dots to indicate more
- syntax: c: recognize some C++ header files by their Emacs modeline
- syntax: default: don't colorize stuff between two pairs of brackets
- syntax: html: add a formatter command, making use of 'tidy'
- syntax: html: colorize only full attributes, and colorize strings later
- syntax: javascript: colorize also special values 'null' and 'undefined'
- syntax: javascript: colorize the boolean values 'true' and 'false' too
- syntax: nanorc: colorize all arguments of 'fixer' and 'linter' as valid
- syntax: nanorc: colorize in bright red everything that is invalid
- syntax: nanorc: colorize only lowercase keywords as valid
- syntax: nanorc: colorize the 'fixer' command as valid
- syntax: ruby: colorize also lowercase global/instance variables
- syntaxes: put the 'linter' and 'formatter' commands on a separate line
- tweaks: add a helper function without the ubiquitous NULL argument
- tweaks: add a local variable, for clarity, to not preuse another one
- tweaks: add some "fall-through" comments, and reshuffle some breaks
- tweaks: add two translator hints
- tweaks: adjust the indentation after the previous change
- tweaks: adjust the indentation after the previous change
- tweaks: adjust the indentation after the previous change, and another
- tweaks: adjust two comments, to better fit the actual functions
- tweaks: avoid setting and resetting a variable when there is no need
- tweaks: avoid three unneeded calls of umask() in the normal case
- tweaks: be explicit about which program complained
- tweaks: check the return value of copy_file() also after its other uses
- tweaks: close the unused reading ends of two more output pipes
- tweaks: condense a fragment of code by making use of a helper function
- tweaks: condense or improve some comments
- tweaks: condense two comments, and rename two parameters
- tweaks: condense two comments, and rewrap a line
- tweaks: correct a comment, and retype a variable
- tweaks: die on an impossible condition -- to be removed later
- tweaks: don't do in the parent something that only the child needs
- tweaks: don't wrap calls of statusline() that slightly overshoot 80 cols
- tweaks: drop the unneeded closing of descriptors when exiting anyway
- tweaks: elide a duplicate opening of the existing file when prepending
- tweaks: elide a function call for the plain ASCII case
- tweaks: elide another two calls of umask(), and rename two variables
- tweaks: elide an unneeded and leaky function
- tweaks: elide an unneeded check when making a backup
- tweaks: elide a variable, and add a condition to elide an assignment
- tweaks: elide a variable that is the same as another
- tweaks: exclude two fragments of code from the tiny version
- tweaks: fuse two regexes into one
- tweaks: group the closing of descriptors together, for compactness
- tweaks: group the closing of two descriptors, and reword two comments
- tweaks: harmonize a message with another
- tweaks: improve some comments, and trim some repetitive ones
- tweaks: make a function do a check so its calls don't need to
- tweaks: mark two strings for translation
- tweaks: move a call of umask() closer to where it is relevant
- tweaks: move two functions to after the one that they make use of
- tweaks: normalize the indentation after the previous change
- tweaks: order two functions more sensibly
- tweaks: pass an empty string as an answer instead of a NULL pointer
- tweaks: pass an empty string for copying instead of a non-existent one
- tweaks: pass any special undo/redo messages to the add_undo() function
- tweaks: remove a pointless updating of the title bar
- tweaks: remove a redundant check for an existing emergency file
- tweaks: remove the superfluous closing of a file descriptor
- tweaks: remove two pointless re-inclusion guards
- tweaks: remove two superfluous conditions when prepending
- tweaks: rename a function and add a parameter, so it becomes more general
- tweaks: rename a function, and elide a parameter that is always NULL
- tweaks: rename a function and elide its first parameter
- tweaks: rename a local variable, to not shadow another
- tweaks: rename a variable, to be a bit more fitting
- tweaks: rename a variable, to be distinct and visible
- tweaks: rename three variables, and reshuffle some lines
- tweaks: rename three variables, to be consistent with other linestructs
- tweaks: rename three variables, to be more descriptive
- tweaks: rename three variables, to match others elsewhere
- tweaks: rename two parameters, for contrast and to match others
- tweaks: rename two parameters plus a variable, to match others
- tweaks: rename two variables, and add a third, for more contrast
- tweaks: reshuffle a few declarations, and reduce the scope of one
- tweaks: reshuffle a fragment of code into two alternatives
- tweaks: reshuffle an 'if' to avoid a negation, and improve a comment
- tweaks: reshuffle some declarations, and rename a variable
- tweaks: reword an undo/redo string that was overlooked during the rename
- tweaks: silence a warning when configured with --enable-tiny
- tweaks: simplify the opening of files when prepending
- tweaks: slightly reword some fragments in the manual's rebinding section
- tweaks: use a better variable name for the argument of an option
- tweaks: use a literal NULL instead of a variable that is NULL
- tweaks: use a simpler positive/negative check for after copy_file()
- tweaks: use a string-copy function that checks for out-of-memory
- tweaks: use the given string instead of the found match, for clarity
- undo: don't try to copy a string that doesn't exist
- undo: put the cursor back on the original row for a full-buffer operation
- utils: don't accept NULL for the string to be copied
- syntax: gentoo: highlight the BDEPEND variable as well

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 4.5-0
- bindings: add a dedicated keycode for <Tab> for when a region is marked
- bump version numbers and add a news item for the 4.5 release
- color: don't concatenate an absolute path with the working directory
- docs: add two examples of the 'tabgives' command to the sample nanorc
- docs: describe the new syntax-specific 'tabgives' command
- docs: mark the undoing of justifications as done in the TODO list
- docs: mention that gcc must be at least version 5.0
- gnulib: update to its current upstream state
- mouse: make the clickable width of menu items more consistent
- new feature: a 'tabgives' command to define what the Tab key produces
- search: after search-at-startup, store the column (for vertical movement)
- tweaks: add a translator hint, and correct two others
- tweaks: add some translator hints, be more precise on permissible length
- tweaks: add two hints for translators, to try and help avoid mistakes
- tweaks: adjust indentation after previous change, reshuffle declarations
- tweaks: avoid a comparison between signed and unsigned  [coverity]
- tweaks: avoid leaking memory when finding an invalid string  [coverity]
- tweaks: avoid recomputing a maximum value every time round the loop
- tweaks: don't burden all menus with something meant for the WriteOut menu
- tweaks: elide a function from a non-UTF8 build
- tweaks: elide two multiplications with something that is always 1
- tweaks: frob a few comments
- tweaks: improve a bunch of comments, and reshuffle some declarations
- tweaks: improve a handful of comments, and reduce the needed padding
- tweaks: mark as 'const' a parameter that takes fixed strings  [coverity]
- tweaks: meld two calls of free() into a single one, to elide an 'else'
- tweaks: move a fragment of common code into the appropriate function
- tweaks: move a function to a better file, to be amongst its kind
- tweaks: move a function to before its callers and next to its kind
- tweaks: move two functions to after the ones that they call
- tweaks: remove some timing code that has served its purpose
- tweaks: remove two superfluous macros, as sizeof(char) is always 1
- tweaks: rename a function, to be a bit more fitting
- tweaks: rename another type, again to better fit the general pattern
- tweaks: rename another type, to also better fit the general pattern
- tweaks: rename another variable, for a better fit
- tweaks: rename a type, to better fit the general pattern
- tweaks: rename a variable, normalize a comment, and reshuffle a free()
- tweaks: rename a variable, to be more compact
- tweaks: rename three variables, for contrast and more sense
- tweaks: rename three variables, for more contrast
- tweaks: rename three variables, to better indicate what they hold
- tweaks: rename two variables, away from single letters
- tweaks: rename two variables, to better describe what they contain
- tweaks: reshuffle a fragment, to group some toggles together
- tweaks: reshuffle a line, to group things better
- tweaks: reshuffle some lines, to elide an unneeded assignment
- tweaks: reshuffle some lines, to have the same order as elsewhere
- tweaks: reshuffle two fragments, to group things better
- tweaks: rewrap a line, reshuffle a declaration, and improve some comments
- tweaks: simplify a calculation, as done elsewhere
- tweaks: simplify the determination of a canonical path
- tweaks: sort two keywords strictly alphabetically
- tweaks: speed up determining the width of plain ASCII characters
- tweaks: speed up the counting of the menu entries to be shown
- tweaks: use a more effecient way to skip storing an empty file name
- tweaks: use an early return when there is no tilde
- tweaks: use 'void' in prototypes of parameterless functions  [coverity]
- usage: mark the -J/--guidestripe option plus argument as translatable
- usage: properly align --help output also when it has accented characters
- search: accept a match at start of file when searching from command line
- syntax: rust: add the words reserved in 2018, and remove unreserved ones

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 4.4-0
- browser: draw a bar of spaces only where needed -- for the selected item
- build: exclude the search-at-startup feature from the tiny version
- bump version numbers and add a news item for the 4.4 release
- copying: do not prevent M-6 from copying emptiness into the cutbuffer
- display: blank the status bar on a successful cut or paste
- display: clear the remainder of a row only when there actually is some
- display: don't clear a row beforehand -- just clear the remainder
- display: use a somewhat faster method to clear a row
- display: when linenumbering, correctly spotlight text that spans two rows
- display: where needed, use slow blanking, but elsewhere do it much faster
- docs: change a few URLs over to https, and rewrap a couple of NEWS items
- docs: document the search-at-startup feature (+/string or +?string)
- docs: make the synopsis of --speller and 'set speller' more accurate
- docs: mention the M-N toggle instead of the obsolete M-# one
- docs: slightly reword some of the descriptions around syntax highlighting
- docs: slightly reword the descriptions of most configure options
- docs: stop mentioning the 'unjustify' function, as it no longer exists
- gnulib: update to its current upstream state
- new document: a condensed overview of nano's shortcut keystrokes
- new feature: allow specifying a search string to "jump to" at startup
- rcfile: properly handle an empty syntax before an 'include' statement
- scrolling: don't overscroll when the edit window has just one row
- search: don't wipe the status bar at startup when there was an error
- search: wipe the status bar before searching again (M-W / M-Q)
- syntax: c: allow an underscore in lowercase type names
- syntax: default: colorize bracketed section headers in some config files
- syntaxes: change some unneeded 'icolor' commands to 'color' commands
- syntaxes: recognize .ctp extension as a PHP file, and .cu as a C/C++ file
- syntax: perl: avoid recognizing embedded hash signs as a comment starter
- syntax: perl: avoid upsetting older glibcs with crafty range expression
- syntax: perl: don't color the character after a variable name
- syntax: po: colorize numbers only when they form a self-contained word
- text: copy leading quote characters when automatic hard-wrapping occurs
- tweaks: add a translator hint, to clarify four short words
- tweaks: call the correct lighting function directly when softwrapping
- tweaks: condense some comments, and drop two unneeded initializations
- tweaks: drop two parameters that are no longer needed
- tweaks: improve a comment, and drop a superfluous one
- tweaks: improve a handful of comments
- tweaks: make a function name unique, to not overlap with others
- tweaks: move a call from two different places to a single place
- tweaks: move a function to before the first one that calls it
- tweaks: move a general function to a better place
- tweaks: remove a saving and restoring that has become superfluous
- tweaks: rename a function, to suit better, and reshuffle its parameters
- tweaks: rename a parameter in three functions, to say what it points to
- tweaks: reshuffle an assignment, and trim some excessive blank lines
- tweaks: reshuffle an 'if' out of a function, and rename the function
- tweaks: reword and condense two comments, and correct another
- tweaks: rewrap two lines, and reshuffle some logic to make more sense
- tweaks: shorten two messages that translators tend to make too long
- tweaks: try the allocation of a multidata cache just once per line
- tweaks: when precalculating, allocate all the cache space upfront
- rcfile: for an empty syntax, show the line number of the 'syntax' command
- rcfile: report the correct command location for an invalid 'include'
- search: accept toggles for case and regex when searching at startup

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
