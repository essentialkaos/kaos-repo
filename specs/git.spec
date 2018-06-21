################################################################################

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

################################################################################

Summary:          Core git tools
Name:             git
Version:          2.17.1
Release:          0%{?dist}
License:          GPL
Group:            Development/Tools
URL:              https://git-scm.com

Source:           http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    gcc make gettext xmlto asciidoc > 6.0.3 lynx
BuildRequires:    libcurl-devel expat-devel openssl-devel zlib-devel >= 1.2

Requires:         perl-Git = %{version}-%{release}
Requires:         zlib >= 1.2 rsync less openssh-clients expat expat-devel

Provides:         git-core = %{version}-%{release}

Obsoletes:        git-core <= 1.5.4.2
Obsoletes:        git-p4 <= 1.5.4.2

################################################################################

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

################################################################################

%package all
Summary:           Meta-package to pull in all git tools
Group:             Development/Tools

BuildArch:         noarch

Requires:          git = %{version}-%{release}
Requires:          git-svn = %{version}-%{release}
Requires:          git-cvs = %{version}-%{release}
Requires:          git-arch = %{version}-%{release}
Requires:          git-email = %{version}-%{release}
Requires:          gitk = %{version}-%{release}
Requires:          gitweb = %{version}-%{release}
Requires:          git-gui = %{version}-%{release}
Obsoletes:         git <= 1.5.4.2

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

################################################################################

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools

Requires:       git = %{version}-%{release} subversion

%description svn
Git tools for importing Subversion repositories.

################################################################################

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} cvs cvsps

%description cvs
Git tools for importing CVS repositories.

################################################################################

%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tla

%description arch
Git tools for importing Arch repositories.

################################################################################

%package email
Summary:        Git tools for sending email
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release}

%description email
Git tools for sending email.

################################################################################

%package gui
Summary:        Git GUI tool
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tk >= 8.4

%description gui
Git GUI tool

################################################################################

%package -n gitk
Summary:        Git revision tree visualiser ('gitk')
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tk >= 8.4

%description -n gitk
Git revision tree visualiser ('gitk')

################################################################################

%package -n gitweb
Summary:        Git web interface
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release}

%description -n gitweb
Browsing git repository on the web

################################################################################

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries

BuildArch:      noarch

Requires:       git = %{version}-%{release}
Requires:       perl

BuildRequires:  perl-Error perl-ExtUtils-MakeMaker

AutoReq:        no

%description -n perl-Git
Perl interface to Git

################################################################################

%prep
%setup -q

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     %{path_settings} \
     all

%install
rm -rf %{buildroot}

%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=%{buildroot} \
     %{path_settings} \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}

test ! -d %{buildroot}%{python_sitelib} || rm -fr %{buildroot}%{python_sitelib}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}%{_libexecdir}/git-core -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@) >> bin-man-doc-files
(find %{buildroot}%{_mandir} %{buildroot}/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files

rm -rf %{buildroot}%{_datadir}/locale

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d

install -m 644 -T contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

%clean
rm -rf %{buildroot}

################################################################################

%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc COPYING Documentation/*.txt
%doc Documentation/howto
%doc Documentation/technical
%{_sysconfdir}/bash_completion.d

%files svn
%defattr(-,root,root)
%{_libexecdir}/git-core/*svn*
%doc Documentation/*svn*.txt
%{_mandir}/man1/*svn*.1*

%files cvs
%defattr(-,root,root)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*

%files arch
%defattr(-,root,root)
%doc Documentation/git-archimport.txt
%{_libexecdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*

%files email
%defattr(-,root,root)
%doc Documentation/*email*.txt
%{_libexecdir}/git-core/*email*
%{_mandir}/man1/*email*.1*

%files gui
%defattr(-,root,root)
%{_libexecdir}/git-core/git-gui
%{_libexecdir}/git-core/git-citool
%{_libexecdir}/git-core/git-gui--askpass
%{_datadir}/git-gui/
%{_mandir}/man1/git-gui.1*
%{_mandir}/man1/git-citool.1*

%files -n gitk
%defattr(-,root,root)
%doc Documentation/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk/
%{_mandir}/man1/*gitk*.1*

%files -n gitweb
%defattr(-,root,root)
%doc gitweb/README gitweb/INSTALL Documentation/*gitweb*.txt
%{_datadir}/gitweb
%{_mandir}/man1/*gitweb*.1*
%{_mandir}/man5/*gitweb*.5*

%files -n perl-Git
%defattr(-,root,root)
%{_datadir}/perl5/*

%files all
%defattr(-,root,root,-)
# No files for you!

################################################################################

%changelog
* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 2.17.1-0
- This release contains the same fixes made in the v2.13.7 version of
  Git, covering CVE-2018-11233 and 11235, and forward-ported to
  v2.14.4, v2.15.2 and v2.16.4 releases.  See release notes to
  v2.13.7 for details.
- In addition to the above fixes, this release has support on the
  server side to reject pushes to repositories that attempt to create
  such problematic .gitmodules file etc. as tracked contents, to help
  hosting sites protect their customers by preventing malicious
  contents from spreading.

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 2.16.3-0
- "git status" after moving a path in the working tree (hence making
  it appear "removed") and then adding with the -N option (hence
  making that appear "added") detected it as a rename, but did not
  report the  old and new pathnames correctly.
- "git commit --fixup" did not allow "-m<message>" option to be used
  at the same time; allow it to annotate resulting commit with more
  text.
- When resetting the working tree files recursively, the working tree
  of submodules are now also reset to match.
- Fix for a commented-out code to adjust it to a rather old API change
  around object ID.
- When there are too many changed paths, "git diff" showed a warning
  message but in the middle of a line.
- The http tracing code, often used to debug connection issues,
  learned to redact potentially sensitive information from its output
  so that it can be more safely sharable.
- Crash fix for a corner case where an error codepath tried to unlock
  what it did not acquire lock on.
- The split-index mode had a few corner case bugs fixed.
- Assorted fixes to "git daemon".
- Completion of "git merge -s<strategy>" (in contrib/) did not work
  well in non-C locale.
- Workaround for segfault with more recent versions of SVN.
- Recently introduced leaks in fsck have been plugged.
- Travis CI integration now builds the executable in 'script' phase
  to follow the established practice, rather than during
  'before_script' phase.  This allows the CI categorize the failures
  better ('failed' is project's fault, 'errored' is build
  environment's).

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 2.16.2-0
- An old regression in "git describe --all $annotated_tag^0" has been
  fixed.
- "git svn dcommit" did not take into account the fact that a
  svn+ssh:// URL with a username@ (typically used for pushing) refers
  to the same SVN repository without the username@ and failed when
  svn.pushmergeinfo option is set.
- "git merge -Xours/-Xtheirs" learned to use our/their version when
  resolving a conflicting updates to a symbolic link.
- "git clone $there $here" is allowed even when here directory exists
  as long as it is an empty directory, but the command incorrectly
  removed it upon a failure of the operation.
- "git stash -- <pathspec>" incorrectly blew away untracked files in
  the directory that matched the pathspec, which has been corrected.
- "git add -p" was taught to ignore local changes to submodules as
  they do not interfere with the partial addition of regular changes
  anyway.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.16.1-0
- "git clone" segfaulted when cloning a project that happens to
  track two paths that differ only in case on a case insensitive
  filesystem.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.16.0-0
- Use of an empty string as a pathspec element that is used for
  'everything matches' is now an error.
- An empty string as a pathspec element that means "everything"
  i.e. 'git add ""', is now illegal.  We started this by first
  deprecating and warning a pathspec that has such an element in
  2.11 (Nov 2016).
- A hook script that is set unexecutable is simply ignored.  Git
  notifies when such a file is ignored, unless the message is
  squelched via advice.ignoredHook configuration.
- "git pull" has been taught to accept "--[no-]signoff" option and
  pass it down to "git merge".
- The "--push-option=<string>" option to "git push" now defaults to a
  list of strings configured via push.pushOption variable.
- "gitweb" checks if a directory is searchable with Perl's "-x"
  operator, which can be enhanced by using "filetest 'access'"
  pragma, which now we do.
- "git stash save" has been deprecated in favour of "git stash push".
- The set of paths output from "git status --ignored" was tied
  closely with its "--untracked=<mode>" option, but now it can be
  controlled more flexibly.  Most notably, a directory that is
  ignored because it is listed to be ignored in the ignore/exclude
  mechanism can be handled differently from a directory that ends up
  to be ignored only because all files in it are ignored.
- The remote-helper for talking to MediaWiki has been updated to
  truncate an overlong pagename so that ".mw" suffix can still be
  added.
- The remote-helper for talking to MediaWiki has been updated to
  work with mediawiki namespaces.
- The "--format=..." option "git for-each-ref" takes learned to show
  the name of the 'remote' repository and the ref at the remote side
  that is affected for 'upstream' and 'push' via "%%(push:remotename)"
  and friends.
- Doc and message updates to teach users "bisect view" is a synonym
  for "bisect visualize".
- "git bisect run" that did not specify any command to run used to go
  ahead and treated all commits to be tested as 'good'.  This has
  been corrected by making the command error out.
- The SubmittingPatches document has been converted to produce an
  HTML version via AsciiDoc/Asciidoctor.
- We learned to optionally talk to a file system monitor via new
  fsmonitor extension to speed up "git status" and other operations
  that need to see which paths have been modified.  Currently we only
  support "watchman".  See File System Monitor section of
  git-update-index(1) for more detail.
- The "diff" family of commands learned to ignore differences in
  carriage return at the end of line.
- Places that know about "sendemail.to", like documentation and shell
  completion (in contrib/) have been taught about "sendemail.tocmd",
  too.
- "git add --renormalize ." is a new and safer way to record the fact
  that you are correcting the end-of-line convention and other
  "convert_to_git()" glitches in the in-repository data.
- "git branch" and "git checkout -b" are now forbidden from creating
  a branch whose name is "HEAD".
- "git branch --list" learned to show its output through the pager by
  default when the output is going to a terminal, which is controlled
  by the pager.branch configuration variable.  This is similar to a
  recent change to "git tag --list".
- "git grep -W", "git diff -W" and their friends learned a heuristic
  to extend a pre-context beyond the line that matches the "function
  pattern" (aka "diff.*.xfuncname") to include a comment block, if
  exists, that immediately precedes it.
- "git config --expiry-date gc.reflogexpire" can read "2.weeks" from
  the configuration and report it as a timestamp, just like "--int"
  would read "1k" and report 1024, to help consumption by scripts.
- The shell completion (in contrib/) learned that "git pull" can take
  the "--autostash" option.
- The tagnames "git log --decorate" uses to annotate the commits can
  now be limited to subset of available refs with the two additional
  options, --decorate-refs[-exclude]=<pattern>.
- "git grep" compiled with libpcre2 sometimes triggered a segfault,
  which is being fixed.
- "git send-email" tries to see if the sendmail program is available
  in /usr/lib and /usr/sbin; extend the list of locations to be
  checked to also include directories on $PATH.
- "git diff" learned, "--anchored", a variant of the "--patience"
  algorithm, to which the user can specify which 'unique' line to be
  used as anchoring points.
- The way "git worktree add" determines what branch to create from
  where and checkout in the new worktree has been updated a bit.
- Ancient part of codebase still shows dots after an abbreviated
  object name just to show that it is not a full object name, but
  these ellipses are confusing to people who newly discovered Git
  who are used to seeing abbreviated object names and find them
  confusing with the range syntax.
- With a configuration variable rebase.abbreviateCommands set,
  "git rebase -i" produces the todo list with a single-letter
  command names.
- "git worktree add" learned to run the post-checkout hook, just like
  "git checkout" does, after the initial checkout.
- "git svn" has been updated to strip CRs in the commit messages, as
  recent versions of Subversion rejects them.
- "git imap-send" did not correctly quote the folder name when
  making a request to the server, which has been corrected.
- Error messages from "git rebase" have been somewhat cleaned up.
- Git has been taught to support an https:// URL used for http.proxy
  when using recent versions of libcurl.
- "git merge" learned to pay attention to merge.verifySignatures
  configuration variable and pretend as if '--verify-signatures'
  option was given from the command line.
- "git describe" was taught to dig trees deeper to find a
  <commit-ish>:<path> that refers to a given blob object.
- An earlier update made it possible to use an on-stack in-core
  lockfile structure (as opposed to having to deliberately leak an
  on-heap one).  Many codepaths have been updated to take advantage
  of this new facility.
- Calling cmd_foo() as if it is a general purpose helper function is
  a no-no.  Correct two instances of such to set an example.
- We try to see if somebody runs our test suite with a shell that
  does not support "local" like bash/dash does.
- An early part of piece-by-piece rewrite of "git bisect" in C.
- GSoC to piece-by-piece rewrite "git submodule" in C.
- Optimize the code to find shortest unique prefix of object names.
- Pathspec-limited revision traversal was taught not to keep finding
  unneeded differences once it knows two trees are different inside
  given pathspec.
- Conversion from uchar[20] to struct object_id continues.
- Code cleanup.
- A single-word "unsigned flags" in the diff options is being split
  into a structure with many bitfields.
- TravisCI build updates.
- Parts of a test to drive the long-running content filter interface
  has been split into its own module, hopefully to eventually become
  reusable.
- Drop (perhaps overly cautious) sanity check before using the index
  read from the filesystem at runtime.
- The build procedure has been taught to avoid some unnecessary
  instability in the build products.
- A new mechanism to upgrade the wire protocol in place is proposed
  and demonstrated that it works with the older versions of Git
  without harming them.
- An infrastructure to define what hash function is used in Git is
  introduced, and an effort to plumb that throughout various
  codepaths has been started.
- The code to iterate over loose object files got optimized.
- An internal function that was left for backward compatibility has
  been removed, as there is no remaining callers.
- Historically, the diff machinery for rename detection had a
  hardcoded limit of 32k paths; this is being lifted to allow users
  trade cycles with a (possibly) easier to read result.
- The tracing infrastructure has been optimized for cases where no
  tracing is requested.
- In preparation for implementing narrow/partial clone, the object
  walking machinery has been taught a way to tell it to "filter" some
  objects from enumeration.
- A few structures and variables that are implementation details of
  the decorate API have been renamed and then the API got documented
  better.
- Assorted updates for TravisCI integration.
- Introduce a helper to simplify code to parse a common pattern that
  expects either "--key" or "--key=<something>".
- "git version --build-options" learned to report the host CPU and
  the exact commit object name the binary was built from.
- "auto" as a value for the columnar output configuration ought to
  judge "is the output consumed by humans?" with the same criteria as
  "auto" for coloured output configuration, i.e. either the standard
  output stream is going to tty, or a pager is in use.  We forgot the
  latter, which has been fixed.
- The experimental "color moved lines differently in diff output"
  feature was buggy around "ignore whitespace changes" edges, which
  has been corrected.
- Instead of using custom line comparison and hashing functions to
  implement "moved lines" coloring in the diff output, use the pair
  of these functions from lower-layer xdiff/ code.
- Some codepaths did not check for errors when asking what branch the
  HEAD points at, which have been fixed.
- "git commit", after making a commit, did not check for errors when
  asking on what branch it made the commit, which has been corrected.
- "git status --ignored -u" did not stop at a working tree of a
  separate project that is embedded in an ignored directory and
  listed files in that other project, instead of just showing the
  directory itself as ignored.
- A broken access to object databases in recent update to "git grep
  --recurse-submodules" has been fixed.
- A recent regression in "git rebase -i" that broke execution of git
  commands from subdirectories via "exec" instruction has been fixed.
- A (possibly flakey) test fix.
- "git check-ref-format --branch @{-1}" bit a "BUG()" when run
  outside a repository for obvious reasons; clarify the documentation
  and make sure we do not even try to expand the at-mark magic in
  such a case, but still call the validation logic for branch names.
- "git fetch --recurse-submodules" now knows that submodules can be
  moved around in the superproject in addition to getting updated,
  and finds the ones that need to be fetched accordingly.
- Command line completion (in contrib/) update.
- Description of blame.{showroot,blankboundary,showemail,date}
  configuration variables have been added to "git config --help".
- After an error from lstat(), diff_populate_filespec() function
  sometimes still went ahead and used invalid data in struct stat,
  which has been fixed.
- UNC paths are also relevant in Cygwin builds and they are now
  tested just like Mingw builds.
- Correct start-up sequence so that a repository could be placed
  immediately under the root directory again (which was broken at
  around Git 2.13).
- The credential helper for libsecret (in contrib/) has been improved
  to allow possibly prompting the end user to unlock secrets that are
  currently locked (otherwise the secrets may not be loaded).
- MinGW updates.
- Error checking in "git imap-send" for empty response has been
  improved.
- Recent update to the refs infrastructure implementation started
  rewriting packed-refs file more often than before; this has been
  optimized again for most trivial cases.
- Some error messages did not quote filenames shown in it, which have
  been fixed.
- "git rebase -i" recently started misbehaving when a submodule that
  is configured with 'submodule.<name>.ignore' is dirty; this has
  been corrected.
- Building with NO_LIBPCRE1_JIT did not disable it, which has been fixed.
- We used to add an empty alternate object database to the system
  that does not help anything; it has been corrected.
- Doc update around use of "format-patch --subject-prefix" etc.
- A fix for an ancient bug in "git apply --ignore-space-change" codepath.
- Clarify and enhance documentation for "merge-base --fork-point", as
  it was clear what it computed but not why/what for.
- A few scripts (both in production and tests) incorrectly redirected
  their error output.  These have been corrected.
- "git notes" sent its error message to its standard output stream,
  which was corrected.
- The three-way merge performed by "git cherry-pick" was confused
  when a new submodule was added in the meantime, which has been
  fixed (or "papered over").
- The sequencer machinery (used by "git cherry-pick A..B", and "git
  rebase -i", among other things) would have lost a commit if stopped
  due to an unlockable index file, which has been fixed.
- "git apply --inaccurate-eof" when used with "--ignore-space-change"
  triggered an internal sanity check, which has been fixed.
- Command line completion (in contrib/) has been taught about the
  "--copy" option of "git branch".
- When "git rebase" prepared a mailbox of changes and fed it to "git
  am" to replay them, it was confused when a stray "From " happened
  to be in the log message of one of the replayed changes.  This has
  been corrected.
- There was a recent semantic mismerge in the codepath to write out a
  section of a configuration section, which has been corrected.
- Mentions of "git-rebase" and "git-am" (dashed form) still remained
  in end-user visible strings emitted by the "git rebase" command;
  they have been corrected.
- Contrary to the documentation, "git pull -4/-6 other-args" did not
  ask the underlying "git fetch" to go over IPv4/IPv6, which has been
  corrected.
- "git checkout --recursive" may overwrite and rewind the history of
  the branch that happens to be checked out in submodule
  repositories, which might not be desirable.  Detach the HEAD but
  still allow the recursive checkout to succeed in such a case.
- "git branch --set-upstream" has been deprecated and (sort of)
  removed, as "--set-upstream-to" is the preferred one these days.
  The documentation still had "--set-upstream" listed on its
  synopsis section, which has been corrected.
- Internally we use 0{40} as a placeholder object name to signal the
  codepath that there is no such object (e.g. the fast-forward check
  while "git fetch" stores a new remote-tracking ref says "we know
  there is no 'old' thing pointed at by the ref, as we are creating
  it anew" by passing 0{40} for the 'old' side), and expect that a
  codepath to locate an in-core object to return NULL as a sign that
  the object does not exist.  A look-up for an object that does not
  exist however is quite costly with a repository with large number
  of packfiles.  This access pattern has been optimized.
- In addition to "git stash -m message", the command learned to
  accept "git stash -mmessage" form.
- @{-N} in "git checkout @{-N}" may refer to a detached HEAD state,
  but the documentation was not clear about it, which has been fixed.
- A regression in the progress eye-candy was fixed.
- The code internal to the recursive merge strategy was not fully
  prepared to see a path that is renamed to try overwriting another
  path that is only different in case on case insensitive systems.
  This does not matter in the current code, but will start to matter
  once the rename detection logic starts taking hints from nearby
  paths moving to some directory and moves a new path along with them.
- An v2.12-era regression in pathspec match logic, which made it look
  into submodule tree even when it is not desired, has been fixed.
- Amending commits in git-gui broke the author name that is non-ascii
  due to incorrect enconding conversion.
- Recent update to the submodule configuration code broke "diff-tree"
  by accidentally stopping to read from the index upfront.
- Git shows a message to tell the user that it is waiting for the
  user to finish editing when spawning an editor, in case the editor
  opens to a hidden window or somewhere obscure and the user gets
  lost.
- The "safe crlf" check incorrectly triggered for contents that does
  not use CRLF as line endings, which has been corrected.
- "git clone --shared" to borrow from a (secondary) worktree did not
  work, even though "git clone --local" did.  Both are now accepted.
- The build procedure now allows not just the repositories but also
  the refs to be used to take pre-formatted manpages and html
  documents to install.
- Update the shell prompt script (in contrib/) to strip trailing CR
  from strings read from various "state" files.
- "git merge -s recursive" did not correctly abort when the index is
  dirty, if the merged tree happened to be the same as the current
  HEAD, which has been fixed.
- Bytes with high-bit set were encoded incorrectly and made
  credential helper fail.
- "git rebase -p -X<option>" did not propagate the option properly
  down to underlying merge strategy backend.
- "git merge -s recursive" did not correctly abort when the index is
  dirty, if the merged tree happened to be the same as the current
  HEAD, which has been fixed.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.15.2-0
- Recent update to the refs infrastructure implementation started
  rewriting packed-refs file more often than before; this has been
  optimized again for most trivial cases.
- The SubmittingPatches document has been converted to produce an
  HTML version via AsciiDoc/Asciidoctor.
- Contrary to the documentation, "git pull -4/-6 other-args" did not
  ask the underlying "git fetch" to go over IPv4/IPv6, which has been
  corrected.
- When "git rebase" prepared an mailbox of changes and fed it to "git
  am" to replay them, it was confused when a stray "From " happened
  to be in the log message of one of the replayed changes.  This has
  been corrected.
- Command line completion (in contrib/) has been taught about the
  "--copy" option of "git branch".
- "git apply --inaccurate-eof" when used with "--ignore-space-change"
  triggered an internal sanity check, which has been fixed.
- The sequencer machinery (used by "git cherry-pick A..B", and "git
  rebase -i", among other things) would have lost a commit if stopped
  due to an unlockable index file, which has been fixed.
- The three-way merge performed by "git cherry-pick" was confused
  when a new submodule was added in the meantime, which has been
  fixed (or "papered over").
- "git notes" sent its error message to its standard output stream,
  which was corrected.
- A few scripts (both in production and tests) incorrectly redirected
  their error output.  These have been corrected.
- Clarify and enhance documentation for "merge-base --fork-point", as
  it was clear what it computed but not why/what for.

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.15.1-0
- TravisCI build updates.
- "auto" as a value for the columnar output configuration ought to
  judge "is the output consumed by humans?" with the same criteria as
  "auto" for coloured output configuration, i.e. either the standard
  output stream is going to tty, or a pager is in use.  We forgot the
  latter, which has been fixed.
- The experimental "color moved lines differently in diff output"
  feature was buggy around "ignore whitespace changes" edges, which
  has been corrected.
- Instead of using custom line comparison and hashing functions to
  implement "moved lines" coloring in the diff output, use the pair
  of these functions from lower-layer xdiff/ code.
- Some codepaths did not check for errors when asking what branch the
  HEAD points at, which have been fixed.
- "git commit", after making a commit, did not check for errors when
  asking on what branch it made the commit, which has been corrected.
- "git status --ignored -u" did not stop at a working tree of a
  separate project that is embedded in an ignored directory and
  listed files in that other project, instead of just showing the
  directory itself as ignored.
- A broken access to object databases in recent update to "git grep
  --recurse-submodules" has been fixed.
- A recent regression in "git rebase -i" that broke execution of git
  commands from subdirectories via "exec" instruction has been fixed.
- "git check-ref-format --branch @{-1}" bit a "BUG()" when run
  outside a repository for obvious reasons; clarify the documentation
  and make sure we do not even try to expand the at-mark magic in
  such a case, but still call the validation logic for branch names.
- Command line completion (in contrib/) update.
- Description of blame.{showroot,blankboundary,showemail,date}
  configuration variables have been added to "git config --help".
- After an error from lstat(), diff_populate_filespec() function
  sometimes still went ahead and used invalid data in struct stat,
  which has been fixed.
- UNC paths are also relevant in Cygwin builds and they are now
  tested just like Mingw builds.
- Correct start-up sequence so that a repository could be placed
  immediately under the root directory again (which was broken at
  around Git 2.13).
- The credential helper for libsecret (in contrib/) has been improved
  to allow possibly prompting the end user to unlock secrets that are
  currently locked (otherwise the secrets may not be loaded).
- Updates from GfW project.
- "git rebase -i" recently started misbehaving when a submodule that
  is configured with 'submodule.<name>.ignore' is dirty; this has
  been corrected.
- Some error messages did not quote filenames shown in it, which have
  been fixed.
- Building with NO_LIBPCRE1_JIT did not disable it, which has been fixed.
- We used to add an empty alternate object database to the system
  that does not help anything; it has been corrected.
- Error checking in "git imap-send" for empty response has been
  improved.
- An ancient bug in "git apply --ignore-space-change" codepath has
  been fixed.
- There was a recent semantic mismerge in the codepath to write out a
  section of a configuration section, which has been corrected.

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.15.0-0
- Use of an empty string as a pathspec element that is used for
  'everything matches' is still warned and Git asks users to use a
  more explicit '.' for that instead.  The hope is that existing
  users will not mind this change, and eventually the warning can be
  turned into a hard error, upgrading the deprecation into removal of
  this (mis)feature.  That is now scheduled to happen in Git v2.16,
  the next major release after this one.
- Git now avoids blindly falling back to ".git" when the setup
  sequence said we are _not_ in Git repository.  A corner case that
  happens to work right now may be broken by a call to BUG().
  We've tried hard to locate such cases and fixed them, but there
  might still be cases that need to be addressed--bug reports are
  greatly appreciated.
- "branch --set-upstream" that has been deprecated in Git 1.8 has
  finally been retired.
- An example that is now obsolete has been removed from a sample hook,
  and an old example in it that added a sign-off manually has been
  improved to use the interpret-trailers command.
- The advice message given when "git rebase" stops for conflicting
  changes has been improved.
- The "rerere-train" script (in contrib/) learned the "--overwrite"
  option to allow overwriting existing recorded resolutions.
- "git contacts" (in contrib/) now lists the address on the
  "Reported-by:" trailer to its output, in addition to those on
  S-o-b: and other trailers, to make it easier to notify (and thank)
  the original bug reporter.
- "git rebase", especially when it is run by mistake and ends up
  trying to replay many changes, spent long time in silence.  The
  command has been taught to show progress report when it spends
  long time preparing these many changes to replay (which would give
  the user a chance to abort with ^C).
- "git merge" learned a "--signoff" option to add the Signed-off-by:
  trailer with the committer's name.
- "git diff" learned to optionally paint new lines that are the same
  as deleted lines elsewhere differently from genuinely new lines.
- "git interpret-trailers" learned to take the trailer specifications
  from the command line that overrides the configured values.
- "git interpret-trailers" has been taught a "--parse" and a few
  other options to make it easier for scripts to grab existing
  trailer lines from a commit log message.
- The "--format=%%(trailers)" option "git log" and its friends take
  learned to take the 'unfold' and 'only' modifiers to normalize its
  output, e.g. "git log --format=%%(trailers:only,unfold)".
- "gitweb" shows a link to visit the 'raw' contents of blobs in the
  history overview page.
- "[gc] rerereResolved = 5.days" used to be invalid, as the variable
  is defined to take an integer counting the number of days.  It now
  is allowed.
- The code to acquire a lock on a reference (e.g. while accepting a
  push from a client) used to immediately fail when the reference is
  already locked---now it waits for a very short while and retries,
  which can make it succeed if the lock holder was holding it during
  a read-only operation.
- "branch --set-upstream" that has been deprecated in Git 1.8 has
  finally been retired.
- The codepath to call external process filter for smudge/clean
  operation learned to show the progress meter.
- "git rev-parse" learned "--is-shallow-repository", that is to be
  used in a way similar to existing "--is-bare-repository" and
  friends.
- "git describe --match <pattern>" has been taught to play well with
  the "--all" option.
- "git branch" learned "-c/-C" to create a new branch by copying an
  existing one.
- Some commands (most notably "git status") makes an opportunistic
  update when performing a read-only operation to help optimize later
  operations in the same repository.  The new "--no-optional-locks"
  option can be passed to Git to disable them.
- "git for-each-ref --format=..." learned a new format element,
  %%(trailers), to show only the commit log trailer part of the log
  message.
- Conversion from uchar[20] to struct object_id continues.
- Start using selected c99 constructs in small, stable and
  essential part of the system to catch people who care about
  older compilers that do not grok them.
- The filter-process interface learned to allow a process with long
  latency give a "delayed" response.
- Many uses of comparison callback function the hashmap API uses
  cast the callback function type when registering it to
  hashmap_init(), which defeats the compile time type checking when
  the callback interface changes (e.g. gaining more parameters).
  The callback implementations have been updated to take "void *"
  pointers and cast them to the type they expect instead.
- Because recent Git for Windows do come with a real msgfmt, the
  build procedure for git-gui has been updated to use it instead of a
  hand-rolled substitute.
- "git grep --recurse-submodules" has been reworked to give a more
  consistent output across submodule boundary (and do its thing
  without having to fork a separate process).
- A helper function to read a single whole line into strbuf
  mistakenly triggered OOM error at EOF under certain conditions,
  which has been fixed.
- The "ref-store" code reorganization continues.
- "git commit" used to discard the index and re-read from the filesystem
  just in case the pre-commit hook has updated it in the middle; this
  has been optimized out when we know we do not run the pre-commit hook.
- Updates to the HTTP layer we made recently unconditionally used
  features of libCurl without checking the existence of them, causing
  compilation errors, which has been fixed.  Also migrate the code to
  check feature macros, not version numbers, to cope better with
  libCurl that vendor ships with backported features.
- The API to start showing progress meter after a short delay has
  been simplified.
- Code clean-up to avoid mixing values read from the .gitmodules file
  and values read from the .git/config file.
- We used to spend more than necessary cycles allocating and freeing
  piece of memory while writing each index entry out.  This has been
  optimized.
- Platforms that ship with a separate sha1 with collision detection
  library can link to it instead of using the copy we ship as part of
  our source tree.
- Code around "notes" have been cleaned up.
- The long-standing rule that an in-core lockfile instance, once it
  is used, must not be freed, has been lifted and the lockfile and
  tempfile APIs have been updated to reduce the chance of programming
  errors.
- Our hashmap implementation in hashmap.[ch] is not thread-safe when
  adding a new item needs to expand the hashtable by rehashing; add
  an API to disable the automatic rehashing to work it around.
- Many of our programs consider that it is OK to release dynamic
  storage that is used throughout the life of the program by simply
  exiting, but this makes it harder to leak detection tools to avoid
  reporting false positives.  Plug many existing leaks and introduce
  a mechanism for developers to mark that the region of memory
  pointed by a pointer is not lost/leaking to help these tools.
- As "git commit" to conclude a conflicted "git merge" honors the
  commit-msg hook, "git merge" that records a merge commit that
  cleanly auto-merges should, but it didn't.
- The codepath for "git merge-recursive" has been cleaned up.
- Many leaks of strbuf have been fixed.
- "git imap-send" has our own implementation of the protocol and also
  can use more recent libCurl with the imap protocol support.  Update
  the latter so that it can use the credential subsystem, and then
  make it the default option to use, so that we can eventually
  deprecate and remove the former.
- "make style" runs git-clang-format to help developers by pointing
  out coding style issues.
- A test to demonstrate "git mv" failing to adjust nested submodules
  has been added.
- On Cygwin, "ulimit -s" does not report failure but it does not work
  at all, which causes an unexpected success of some tests that
  expect failures under a limited stack situation.  This has been
  fixed.
- Many codepaths have been updated to squelch -Wimplicit-fallthrough
  warnings from Gcc 7 (which is a good code hygiene).
- Add a helper for DLL loading in anticipation for its need in a
  future topic RSN.
- "git status --ignored", when noticing that a directory without any
  tracked path is ignored, still enumerated all the ignored paths in
  the directory, which is unnecessary.  The codepath has been
  optimized to avoid this overhead.
- The final batch to "git rebase -i" updates to move more code from
  the shell script to C has been merged.
- Operations that do not touch (majority of) packed refs have been
  optimized by making accesses to packed-refs file lazy; we no longer
  pre-parse everything, and an access to a single ref in the
  packed-refs does not touch majority of irrelevant refs, either.
- Add comment to clarify that the style file is meant to be used with
  clang-5 and the rules are still work in progress.
- Many variables that points at a region of memory that will live
  throughout the life of the program have been marked with UNLEAK
  marker to help the leak checkers concentrate on real leaks..
- Plans for weaning us off of SHA-1 has been documented.
- A new "oidmap" API has been introduced and oidset API has been
  rewritten to use it.
- "%%C(color name)" in the pretty print format always produced ANSI
  color escape codes, which was an early design mistake.  They now
  honor the configuration (e.g. "color.ui = never") and also tty-ness
  of the output medium.
- The http.{sslkey,sslCert} configuration variables are to be
  interpreted as a pathname that honors "~[username]/" prefix, but
  weren't, which has been fixed.
- Numerous bugs in walking of reflogs via "log -g" and friends have
  been fixed.
- "git commit" when seeing an totally empty message said "you did not
  edit the message", which is clearly wrong.  The message has been
  corrected.
- When a directory is not readable, "gitweb" fails to build the
  project list.  Work this around by skipping such a directory.
- Some versions of GnuPG fails to kill gpg-agent it auto-spawned
  and such a left-over agent can interfere with a test.  Work it
  around by attempting to kill one before starting a new test.
- A recently added test for the "credential-cache" helper revealed
  that EOF detection done around the time the connection to the cache
  daemon is torn down were flaky.  This was fixed by reacting to
  ECONNRESET and behaving as if we got an EOF.
- "git log --tag=no-such-tag" showed log starting from HEAD, which
  has been fixed---it now shows nothing.
- The "tag.pager" configuration variable was useless for those who
  actually create tag objects, as it interfered with the use of an
  editor.  A new mechanism has been introduced for commands to enable
  pager depending on what operation is being carried out to fix this,
  and then "git tag -l" is made to run pager by default.
- "git push --recurse-submodules $there HEAD:$target" was not
  propagated down to the submodules, but now it is.
- Commands like "git rebase" accepted the --rerere-autoupdate option
  from the command line, but did not always use it.  This has been
  fixed.
- "git clone --recurse-submodules --quiet" did not pass the quiet
  option down to submodules.
- Test portability fix for OBSD.
- Portability fix for OBSD.
- "git am -s" has been taught that some input may end with a trailer
  block that is not Signed-off-by: and it should refrain from adding
  an extra blank line before adding a new sign-off in such a case.
- "git svn" used with "--localtime" option did not compute the tz
  offset for the timestamp in question and instead always used the
  current time, which has been corrected.
- Memory leak in an error codepath has been plugged.
- "git stash -u" used the contents of the committed version of the
  ".gitignore" file to decide which paths are ignored, even when the
  file has local changes.  The command has been taught to instead use
  the locally modified contents.
- bash 4.4 or newer gave a warning on NUL byte in command
  substitution done in "git stash"; this has been squelched.
- "git grep -L" and "git grep --quiet -L" reported different exit
  codes; this has been corrected.
- When handshake with a subprocess filter notices that the process
  asked for an unknown capability, Git did not report what program
  the offending subprocess was running.  This has been corrected.
- "git apply" that is used as a better "patch -p1" failed to apply a
  taken from a file with CRLF line endings to a file with CRLF line
  endings.  The root cause was because it misused convert_to_git()
  that tried to do "safe-crlf" processing by looking at the index
  entry at the same path, which is a nonsense---in that mode, "apply"
  is not working on the data in (or derived from) the index at all.
  This has been fixed.
- Killing "git merge --edit" before the editor returns control left
  the repository in a state with MERGE_MSG but without MERGE_HEAD,
  which incorrectly tells the subsequent "git commit" that there was
  a squash merge in progress.  This has been fixed.
- "git archive" did not work well with pathspecs and the
  export-ignore attribute.
- In addition to "cc: <a@dd.re.ss> # cruft", "cc: a@dd.re.ss # cruft"
  was taught to "git send-email" as a valid way to tell it that it
  needs to also send a carbon copy to <a@dd.re.ss> in the trailer
  section.
- "git branch -M a b" while on a branch that is completely unrelated
  to either branch a or branch b misbehaved when multiple worktree
  was in use.  This has been fixed.
- "git gc" and friends when multiple worktrees are used off of a
  single repository did not consider the index and per-worktree refs
  of other worktrees as the root for reachability traversal, making
  objects that are in use only in other worktrees to be subject to
  garbage collection.
- A regression to "gitk --bisect" by a recent update has been fixed.
- "git -c submodule.recurse=yes pull" did not work as if the
  "--recurse-submodules" option was given from the command line.
  This has been corrected.
- Unlike "git commit-tree < file", "git commit-tree -F file" did not
  pass the contents of the file verbatim and instead completed an
  incomplete line at the end, if exists.  The latter has been updated
  to match the behaviour of the former.
- Many codepaths did not diagnose write failures correctly when disks
  go full, due to their misuse of write_in_full() helper function,
  which have been corrected.
- "git help co" now says "co is aliased to ...", not "git co is".
- "git archive", especially when used with pathspec, stored an empty
  directory in its output, even though Git itself never does so.
  This has been fixed.
- API error-proofing which happens to also squelch warnings from GCC.
- The explanation of the cut-line in the commit log editor has been
  slightly tweaked.
- "git gc" tries to avoid running two instances at the same time by
  reading and writing pid/host from and to a lock file; it used to
  use an incorrect fscanf() format when reading, which has been
  corrected.
- The scripts to drive TravisCI has been reorganized and then an
  optimization to avoid spending cycles on a branch whose tip is
  tagged has been implemented.
- The test linter has been taught that we do not like "echo -e".
- Code cmp.std.c nitpick.
- A regression fix for 2.11 that made the code to read the list of
  alternate object stores overrun the end of the string.
- "git describe --match" learned to take multiple patterns in v2.13
  series, but the feature ignored the patterns after the first one
  and did not work at all.  This has been fixed.
- "git filter-branch" cannot reproduce a history with a tag without
  the tagger field, which only ancient versions of Git allowed to be
  created.  This has been corrected.
- "git cat-file --textconv" started segfaulting recently, which
  has been corrected.
- The built-in pattern to detect the "function header" for HTML did
  not match <H1>..<H6> elements without any attributes, which has
  been fixed.
- "git mailinfo" was loose in decoding quoted printable and produced
  garbage when the two letters after the equal sign are not
  hexadecimal.  This has been fixed.
- The machinery to create xdelta used in pack files received the
  sizes of the data in size_t, but lost the higher bits of them by
  storing them in "unsigned int" during the computation, which is
  fixed.
- The delta format used in the packfile cannot reference data at
  offset larger than what can be expressed in 4-byte, but the
  generator for the data failed to make sure the offset does not
  overflow.  This has been corrected.
- The documentation for '-X<option>' for merges was misleadingly
  written to suggest that "-s theirs" exists, which is not the case.
- "git fast-export" with -M/-C option issued "copy" instruction on a
  path that is simultaneously modified, which was incorrect.
- Many codepaths have been updated to squelch -Wsign-compare
  warnings.
- Memory leaks in various codepaths have been plugged.
- Recent versions of "git rev-parse --parseopt" did not parse the
  option specification that does not have the optional flags (*=?!)
  correctly, which has been corrected.
- The checkpoint command "git fast-import" did not flush updates to
  refs and marks unless at least one object was created since the
  last checkpoint, which has been corrected, as these things can
  happen without any new object getting created.
- Spell the name of our system as "Git" in the output from
  request-pull script.
- Fixes for a handful memory access issues identified by valgrind.
- Backports a moral equivalent of 2015 fix to the poll() emulation
  from the upstream gnulib to fix occasional breakages on HPE NonStop.
- Users with "color.ui = always" in their configuration were broken
  by a recent change that made plumbing commands to pay attention to
  them as the patch created internally by "git add -p" were colored
  (heh) and made unusable.  This has been fixed by reverting the
  offending change.
- In the "--format=..." option of the "git for-each-ref" command (and
  its friends, i.e. the listing mode of "git branch/tag"), "%%(atom:)"
  (e.g. "%%(refname:)", "%%(body:)" used to error out.  Instead, treat
  them as if the colon and an empty string that follows it were not
  there.
- An ancient bug that made Git misbehave with creation/renaming of
  refs has been fixed.
- "git fetch <there> <src>:<dst>" allows an object name on the <src>
  side when the other side accepts such a request since Git v2.5, but
  the documentation was left stale.
- Update the documentation for "git filter-branch" so that the filter
  options are listed in the same order as they are applied, as
  described in an earlier part of the doc.
- A possible oom error is now caught as a fatal error, instead of
  continuing and dereferencing NULL.


* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.14.1-0
- This release forward-ports the fix for "ssh://..." URL from Git v2.7.6

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.14.0-0
- Use of an empty string as a pathspec element that is used for
  'everything matches' is still warned and Git asks users to use a
  more explicit '.' for that instead.  The hope is that existing
  users will not mind this change, and eventually the warning can be
  turned into a hard error, upgrading the deprecation into removal of
  this (mis)feature.  That is not scheduled to happen in the upcoming
  release (yet).
- Git now avoids blindly falling back to ".git" when the setup
  sequence said we are _not_ in Git repository.  A corner case that
  happens to work right now may be broken by a call to die("BUG").
  We've tried hard to locate such cases and fixed them, but there
  might still be cases that need to be addressed--bug reports are
  greatly appreciated.
- The experiment to improve the hunk-boundary selection of textual
  diff output has finished, and the "indent heuristics" has now
  become the default.
- Git can now be built with PCRE v2 instead of v1 of the PCRE
  library. Replace USE_LIBPCRE=YesPlease with USE_LIBPCRE2=YesPlease
  in existing build scripts to build against the new version.  As the
  upstream PCRE maintainer has abandoned v1 maintenance for all but
  the most critical bug fixes, use of v2 is recommended.
- The colors in which "git status --short --branch" showed the names
  of the current branch and its remote-tracking branch are now
  configurable.
- "git clone" learned the "--no-tags" option not to fetch all tags
  initially, and also set up the tagopt not to follow any tags in
  subsequent fetches.
- "git archive --format=zip" learned to use zip64 extension when
  necessary to go beyond the 4GB limit.
- "git reset" learned "--recurse-submodules" option.
- "git diff --submodule=diff" now recurses into nested submodules.
- "git repack" learned to accept the --threads=<n> option and pass it
  to pack-objects.
- "git send-email" learned to run sendemail-validate hook to inspect
  and reject a message before sending it out.
- There is no good reason why "git fetch $there $sha1" should fail
  when the $sha1 names an object at the tip of an advertised ref,
  even when the other side hasn't enabled allowTipSHA1InWant.
- The "[includeIf "gitdir:$dir"] path=..." mechanism introduced in
  2.13.0 would canonicalize the path of the gitdir being matched,
  and did not match e.g. "gitdir:~/work/*" against a repo in
  "~/work/main" if "~/work" was a symlink to "/mnt/storage/work".
  Now we match both the resolved canonical path and what "pwd" would
  show. The include will happen if either one matches.
- The "indent" heuristics is now the default in "diff". The
  diff.indentHeuristic configuration variable can be set to "false"
  for those who do not want it.
- Many commands learned to pay attention to submodule.recurse
  configuration.
- The convention for a command line is to follow "git cmdname
  --options" with revisions followed by an optional "--"
  disambiguator and then finally pathspecs.  When "--" is not there,
  we make sure early ones are all interpretable as revs (and do not
  look like paths) and later ones are the other way around.  A
  pathspec with "magic" (e.g. ":/p/a/t/h" that matches p/a/t/h from
  the top-level of the working tree, no matter what subdirectory you
  are working from) are conservatively judged as "not a path", which
  required disambiguation more often.  The command line parser
  learned to say "it's a pathspec" a bit more often when the syntax
  looks like so.
- Update "perl-compatible regular expression" support to enable JIT
  and also allow linking with the newer PCRE v2 library.
- "filter-branch" learned a pseudo filter "--setup" that can be used
  to define common functions/variables that can be used by other
  filters.
- Using "git add d/i/r" when d/i/r is the top of the working tree of
  a separate repository would create a gitlink in the index, which
  would appear as a not-quite-initialized submodule to others.  We
  learned to give warnings when this happens.
- "git status" learned to optionally give how many stash entries there
  are in its output.
- "git status" has long shown essentially the same message as "git
  commit"; the message it gives while preparing for the root commit,
  i.e. "Initial commit", was hard to understand for some new users.
  Now it says "No commits yet" to stress more on the current status
  (rather than the commit the user is preparing for, which is more in
  line with the focus of "git commit").
- "git send-email" now has --batch-size and --relogin-delay options
   which can be used to overcome limitations on SMTP servers that
   restrict on how many of e-mails can be sent in a single session.
- An old message shown in the commit log template was removed, as it
  has outlived its usefulness.
- "git pull --rebase --recurse-submodules" learns to rebase the
  branch in the submodules to an updated base.
- "git log" learned -P as a synonym for --perl-regexp, "git grep"
  already had such a synonym.
- "git log" didn't understand --regexp-ignore-case when combined with
  --perl-regexp. This has been fixed.
Performance, Internal Implementation, Development Support etc.
- The default packed-git limit value has been raised on larger
  platforms to save "git fetch" from a (recoverable) failure while
  "gc" is running in parallel.
- Code to update the cache-tree has been tightened so that we won't
  accidentally write out any 0{40} entry in the tree object.
- Attempt to allow us notice "fishy" situation where we fail to
  remove the temporary directory used during the test.
- Travis CI gained a task to format the documentation with both
  AsciiDoc and AsciiDoctor.
- Some platforms have ulong that is smaller than time_t, and our
  historical use of ulong for timestamp would mean they cannot
  represent some timestamp that the platform allows.  Invent a
  separate and dedicated timestamp_t (so that we can distingiuish
  timestamps and a vanilla ulongs, which along is already a good
  move), and then declare uintmax_t is the type to be used as the
  timestamp_t.
- We can trigger Windows auto-build tester (credits: Dscho &
  Microsoft) from our existing Travis CI tester now.
- Conversion from uchar[20] to struct object_id continues.
- Simplify parse_pathspec() codepath and stop it from looking at the
  default in-core index.
- Add perf-test for wildmatch.
- Code from "conversion using external process" codepath has been
  extracted to a separate sub-process.[ch] module.
- When "git checkout", "git merge", etc. manipulates the in-core
  index, various pieces of information in the index extensions are
  discarded from the original state, as it is usually not the case
  that they are kept up-to-date and in-sync with the operation on the
  main index.  The untracked cache extension is copied across these
  operations now, which would speed up "git status" (as long as the
  cache is properly invalidated).
- The internal implementation of "git grep" has seen some clean-up.
- Update the C style recommendation for notes for translators, as
  recent versions of gettext tools can work with our style of
  multi-line comments.
- The implementation of "ref" API around the "packed refs" have been
  cleaned up, in preparation for further changes.
- The internal logic used in "git blame" has been libified to make it
  easier to use by cgit.
- Our code often opens a path to an optional file, to work on its
  contents when we can successfully open it.  We can ignore a failure
  to open if such an optional file does not exist, but we do want to
  report a failure in opening for other reasons (e.g. we got an I/O
  error, or the file is there, but we lack the permission to open).
  The exact errors we need to ignore are ENOENT (obviously) and
  ENOTDIR (less obvious).  Instead of repeating comparison of errno
  with these two constants, introduce a helper function to do so.
- We often try to open a file for reading whose existence is
  optional, and silently ignore errors from open/fopen; report such
  errors if they are not due to missing files.
- When an existing repository is used for t/perf testing, we first
  create bit-for-bit copy of it, which may grab a transient state of
  the repository and freeze it into the repository used for testing,
  which then may cause Git operations to fail.  Single out "the index
  being locked" case and forcibly drop the lock from the copy.
- Three instances of the same helper function have been consolidated
  to one.
- "fast-import" uses a default pack chain depth that is consistent
  with other parts of the system.
- A new test to show the interaction between the pattern [^a-z]
  (which matches '/') and a slash in a path has been added.  The
  pattern should not match the slash with "pathmatch", but should
  with "wildmatch".
- The 'diff-highlight' program (in contrib/) has been restructured
  for easier reuse by an external project 'diff-so-fancy'.
- A common pattern to free a piece of memory and assign NULL to the
  pointer that used to point at it has been replaced with a new
  FREE_AND_NULL() macro.
- Traditionally, the default die() routine had a code to prevent it
  from getting called multiple times, which interacted badly when a
  threaded program used it (one downside is that the real error may
  be hidden and instead the only error message given to the user may
  end up being "die recursion detected", which is not very useful).
- Introduce a "repository" object to eventually make it easier to
  work in multiple repositories (the primary focus is to work with
  the superproject and its submodules) in a single process.
- Optimize "what are the object names already taken in an alternate
  object database?" query that is used to derive the length of prefix
  an object name is uniquely abbreviated to.
- The hashmap API has been updated so that data to customize the
  behaviour of the comparison function can be specified at the time a
  hashmap is initialized.
- The "collision detecting" SHA-1 implementation shipped with 2.13 is
  now integrated into git.git as a submodule (the first submodule to
  ship with git.git). Clone git.git with --recurse-submodules to get
  it. For now a non-submodule copy of the same code is also shipped
  as part of the tree.
- A recent update made it easier to use "-fsanitize=" option while
  compiling but supported only one sanitize option.  Allow more than
  one to be combined, joined with a comma, like "make SANITIZE=foo,bar".
- Use "p4 -G" to make "p4 changes" output more Python-friendly
  to parse.
- We started using "%%" PRItime, imitating "%%" PRIuMAX and friends, as
  a way to format the internal timestamp value, but this does not
  play well with gettext(1) i18n framework, and causes "make pot"
  that is run by the l10n coordinator to create a broken po/git.pot
  file.  This is a possible workaround for that problem.
- It turns out that Cygwin also needs the fopen() wrapper that
  returns failure when a directory is opened for reading.
- "git gc" did not interact well with "git worktree"-managed
  per-worktree refs.
- "git cherry-pick" and other uses of the sequencer machinery
  mishandled a trailer block whose last line is an incomplete line.
  This has been fixed so that an additional sign-off etc. are added
  after completing the existing incomplete line.
- The codepath in "git am" that is used when running "git rebase"
  leaked memory held for the log message of the commits being rebased.
- "git clone --config var=val" is a way to populate the
  per-repository configuration file of the new repository, but it did
  not work well when val is an empty string.  This has been fixed.
- Setting "log.decorate=false" in the configuration file did not take
  effect in v2.13, which has been corrected.
- A few codepaths in "checkout" and "am" working on an unborn branch
  tried to access an uninitialized piece of memory.
- The Web interface to gmane news archive is long gone, even though
  the articles are still accessible via NTTP.  Replace the links with
  ones to public-inbox.org.  Because their message identification is
  based on the actual message-id, it is likely that it will be easier
  to migrate away from it if/when necessary.
- The receive-pack program now makes sure that the push certificate
  records the same set of push options used for pushing.
- Tests have been updated to pass under GETTEXT_POISON (a mechanism
  to ensure that output strings that should not be translated are
  not translated by mistake), and TravisCI is told to run them.
- "git checkout --recurse-submodules" did not quite work with a
  submodule that itself has submodules.
- "pack-objects" can stream a slice of an existing packfile out when
  the pack bitmap can tell that the reachable objects are all needed
  in the output, without inspecting individual objects.  This
  strategy however would not work well when "--local" and other
  options are in use, and need to be disabled.
- Fix memory leaks pointed out by Coverity (and people).
- "git read-tree -m" (no tree-ish) gave a nonsense suggestion "use
  --empty if you want to clear the index".  With "-m", such a request
  will still fail anyway, as you'd need to name at least one tree-ish
  to be merged.
- Make sure our tests would pass when the sources are checked out
  with "platform native" line ending convention by default on
  Windows.  Some "text" files out tests use and the test scripts
  themselves that are meant to be run with /bin/sh, ought to be
  checked out with eol=LF even on Windows.
- Introduce the BUG() macro to improve die("BUG: ...").
- Clarify documentation for include.path and includeIf.<condition>.path
  configuration variables.
- Git sometimes gives an advice in a rhetorical question that does
  not require an answer, which can confuse new users and non native
  speakers.  Attempt to rephrase them.
- A few http:// links that are redirected to https:// in the
  documentation have been updated to https:// links.
- "git for-each-ref --format=..." with %%(HEAD) in the format used to
  resolve the HEAD symref as many times as it had processed refs,
  which was wasteful, and "git branch" shared the same problem.
- Regression fix to topic recently merged to 'master'.
- The shell completion script (in contrib/) learned "git stash" has
  a new "push" subcommand.
- "git interpret-trailers", when used as GIT_EDITOR for "git commit
  -v", looked for and appended to a trailer block at the very end,
  i.e. at the end of the "diff" output.  The command has been
  corrected to pay attention to the cut-mark line "commit -v" adds to
  the buffer---the real trailer block should appear just before it.
- A test allowed both "git push" and "git receive-pack" on the other
  end write their traces into the same file.  This is OK on platforms
  that allows atomically appending to a file opened with O_APPEND,
  but on other platforms led to a mangled output, causing
  intermittent test failures.  This has been fixed by disabling
  traces from "receive-pack" in the test.
- Tag objects, which are not reachable from any ref, that point at
  missing objects were mishandled by "git gc" and friends (they
  should silently be ignored instead)
- "git describe --contains" penalized light-weight tags so much that
  they were almost never considered.  Instead, give them about the
  same chance to be considered as an annotated tag that is the same
  age as the underlying commit would.
- The "run-command" API implementation has been made more robust
  against dead-locking in a threaded environment.
- A recent update to t5545-push-options.sh started skipping all the
  tests in the script when a web server testing is disabled or
  unavailable, not just the ones that require a web server.  Non HTTP
  tests have been salvaged to always run in this script.
- "git send-email" now uses Net::SMTP::SSL, which is obsolete, only
  when needed.  Recent versions of Net::SMTP can do TLS natively.
- "foo\bar\baz" in "git fetch foo\bar\baz", even though there is no
  slashes in it, cannot be a nickname for a remote on Windows, as
  that is likely to be a pathname on a local filesystem.
- "git clean -d" used to clean directories that has ignored files,
  even though the command should not lose ignored ones without "-x".
  "git status --ignored"  did not list ignored and untracked files
  without "-uall".  These have been corrected.
- The result from "git diff" that compares two blobs, e.g. "git diff
  $commit1:$path $commit2:$path", used to be shown with the full
  object name as given on the command line, but it is more natural to
  use the $path in the output and use it to look up .gitattributes.
- The "collision detecting" SHA-1 implementation shipped with 2.13
  was quite broken on some big-endian platforms and/or platforms that
  do not like unaligned fetches.  Update to the upstream code which
  has already fixed these issues.
- "git am -h" triggered a BUG().
- The interaction of "url.*.insteadOf" and custom URL scheme's
  whitelisting is now documented better.
- The timestamp of the index file is now taken after the file is
  closed, to help Windows, on which a stale timestamp is reported by
  fstat() on a file that is opened for writing and data was written
  but not yet closed.
- "git pull --rebase --autostash" didn't auto-stash when the local history
  fast-forwards to the upstream.
- A flaky test has been corrected.
- "git $cmd -h" for builtin commands calls the implementation of the
  command (i.e. cmd_$cmd() function) without doing any repository
  set-up, and the commands that expect RUN_SETUP is done by the Git
  potty needs to be prepared to show the help text without barfing.
  (merge d691551192 jk/consistent-h later to maint).
- Help contributors that visit us at GitHub.
- "git stash push <pathspec>" did not work from a subdirectory at all.
  Bugfix for a topic in v2.13
- As there is no portable way to pass timezone information to
  strftime, some output format from "git log" and friends are
  impossible to produce.  Teach our own strbuf_addftime to replace %%z
  and %%Z with caller-supplied values to help working around this.
  (merge 6eced3ec5e rs/strbuf-addftime-zZ later to maint).
- "git mergetool" learned to work around a wrapper MacOS X adds
  around underlying meld.
- An example in documentation that does not work in multi worktree
  configuration has been corrected.
- The pretty-format specifiers like '%%h', '%%t', etc. had an
  optimization that no longer works correctly.  In preparation/hope
  of getting it correctly implemented, first discard the optimization
  that is broken.
- The code to pick up and execute command alias definition from the
  configuration used to switch to the top of the working tree and
  then come back when the expanded alias was executed, which was
  unnecessarilyl complex.  Attempt to simplify the logic by using the
  early-config mechanism that does not chdir around.
- Fix configuration codepath to pay proper attention to commondir
  that is used in multi-worktree situation, and isolate config API
  into its own header file.
  (merge dc8441fdb4 bw/config-h later to maint).
- "git add -p" were updated in 2.12 timeframe to cope with custom
  core.commentchar but the implementation was buggy and a
  metacharacter like $ and * did not work.
- A recent regression in "git rebase -i" has been fixed and tests
  that would have caught it and others have been added.
- An unaligned 32-bit access in pack-bitmap code has been corrected.
- Tighten error checks for invalid "git apply" input.
- The split index code did not honor core.sharedRepository setting
  correctly.
- The Makefile rule in contrib/subtree for building documentation
  learned to honour USE_ASCIIDOCTOR just like the main documentation
  set does.
- Code clean-up to fix possible buffer over-reading.
- A few tests that tried to verify the contents of push certificates
  did not use 'git rev-parse' to formulate the line to look for in
  the certificate correctly.
- Update the character width tables.
- After "git branch --move" of the currently checked out branch, the
  code to walk the reflog of HEAD via "log -g" and friends
  incorrectly stopped at the reflog entry that records the renaming
  of the branch.
- The rewrite of "git branch --list" using for-each-ref's internals
  that happened in v2.13 regressed its handling of color.branch.local;
  this has been fixed.
- The build procedure has been improved to allow building and testing
  Git with address sanitizer more easily.
  (merge 425ca6710b jk/build-with-asan later to maint).
- On Cygwin, similar to Windows, "git push //server/share/repository"
  ought to mean a repository on a network share that can be accessed
  locally, but this did not work correctly due to stripping the double
  slashes at the beginning.
- The progress meter did not give a useful output when we haven't had
  0.5 seconds to measure the throughput during the interval.  Instead
  show the overall throughput rate at the end, which is a much more
  useful number.
- Code clean-up, that makes us in sync with Debian by one patch.
- We run an early part of "git gc" that deals with refs before
  daemonising (and not under lock) even when running a background
  auto-gc, which caused multiple gc processes attempting to run the
  early part at the same time.  This is now prevented by running the
  early part also under the GC lock.
- A recent update broke an alias that contained an uppercase letter.

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 2.13.2-0
- The "collision detecting" SHA-1 implementation shipped with 2.13.1
  was still broken on some platforms.  Update to the upstream code
  again to take their fix.
- "git checkout --recurse-submodules" did not quite work with a
  submodule that itself has submodules.
- Introduce the BUG() macro to improve die("BUG: ...").
- The "run-command" API implementation has been made more robust
  against dead-locking in a threaded environment.
- A recent update to t5545-push-options.sh started skipping all the
  tests in the script when a web server testing is disabled or
  unavailable, not just the ones that require a web server.  Non HTTP
  tests have been salvaged to always run in this script.
- "git clean -d" used to clean directories that has ignored files,
  even though the command should not lose ignored ones without "-x".
  "git status --ignored"  did not list ignored and untracked files
  without "-uall".  These have been corrected.
- The timestamp of the index file is now taken after the file is
  closed, to help Windows, on which a stale timestamp is reported by
  fstat() on a file that is opened for writing and data was written
  but not yet closed.
- "git pull --rebase --autostash" didn't auto-stash when the local history
  fast-forwards to the upstream.
- "git describe --contains" penalized light-weight tags so much that
  they were almost never considered.  Instead, give them about the
  same chance to be considered as an annotated tag that is the same
  age as the underlying commit would.
- The result from "git diff" that compares two blobs, e.g. "git diff
  $commit1:$path $commit2:$path", used to be shown with the full
  object name as given on the command line, but it is more natural to
  use the $path in the output and use it to look up .gitattributes.
- A flaky test has been corrected.
- Help contributors that visit us at GitHub.
- "git stash push <pathspec>" did not work from a subdirectory at all.
  Bugfix for a topic in v2.13

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 2.13.1-0
- The Web interface to gmane news archive is long gone, even though
  the articles are still accessible via NTTP.  Replace the links with
  ones to public-inbox.org.  Because their message identification is
  based on the actual message-id, it is likely that it will be easier
  to migrate away from it if/when necessary.
- Update tests to pass under GETTEXT_POISON (a mechanism to ensure
  that output strings that should not be translated are not
  translated by mistake), and tell TravisCI to run them.
- Setting "log.decorate=false" in the configuration file did not take
  effect in v2.13, which has been corrected.
- An earlier update to test 7400 needed to be skipped on CYGWIN.
- Git sometimes gives an advice in a rhetorical question that does
  not require an answer, which can confuse new users and non native
  speakers.  Attempt to rephrase them.
- "git read-tree -m" (no tree-ish) gave a nonsense suggestion "use
  --empty if you want to clear the index".  With "-m", such a request
  will still fail anyway, as you'd need to name at least one tree-ish
  to be merged.
- The codepath in "git am" that is used when running "git rebase"
  leaked memory held for the log message of the commits being rebased.
- "pack-objects" can stream a slice of an existing packfile out when
  the pack bitmap can tell that the reachable objects are all needed
  in the output, without inspecting individual objects.  This
  strategy however would not work well when "--local" and other
  options are in use, and need to be disabled.
- Clarify documentation for include.path and includeIf.<condition>.path
  configuration variables.
- Tag objects, which are not reachable from any ref, that point at
  missing objects were mishandled by "git gc" and friends (they
  should silently be ignored instead)
- A few http:// links that are redirected to https:// in the
  documentation have been updated to https:// links.
- Make sure our tests would pass when the sources are checked out
  with "platform native" line ending convention by default on
  Windows.  Some "text" files out tests use and the test scripts
  themselves that are meant to be run with /bin/sh, ought to be
  checked out with eol=LF even on Windows.
- Fix memory leaks pointed out by Coverity (and people).
- The receive-pack program now makes sure that the push certificate
  records the same set of push options used for pushing.
- "git cherry-pick" and other uses of the sequencer machinery
  mishandled a trailer block whose last line is an incomplete line.
  This has been fixed so that an additional sign-off etc. are added
  after completing the existing incomplete line.
- The shell completion script (in contrib/) learned "git stash" has
  a new "push" subcommand.
- Travis CI gained a task to format the documentation with both
  AsciiDoc and AsciiDoctor.
- Update the C style recommendation for notes for translators, as
  recent versions of gettext tools can work with our style of
  multi-line comments.
- "git clone --config var=val" is a way to populate the
  per-repository configuration file of the new repository, but it did
  not work well when val is an empty string.  This has been fixed.
- A few codepaths in "checkout" and "am" working on an unborn branch
  tried to access an uninitialized piece of memory.
- "git for-each-ref --format=..." with (HEAD) in the format used to
  resolve the HEAD symref as many times as it had processed refs,
  which was wasteful, and "git branch" shared the same problem.
- "git interpret-trailers", when used as GIT_EDITOR for "git commit
  -v", looked for and appended to a trailer block at the very end,
  i.e. at the end of the "diff" output.  The command has been
  corrected to pay attention to the cut-mark line "commit -v" adds to
  the buffer---the real trailer block should appear just before it.
- A test allowed both "git push" and "git receive-pack" on the other
  end write their traces into the same file.  This is OK on platforms
  that allows atomically appending to a file opened with O_APPEND,
  but on other platforms led to a mangled output, causing
  intermittent test failures.  This has been fixed by disabling
  traces from "receive-pack" in the test.
- "foo\bar\baz" in "git fetch foo\bar\baz", even though there is no
  slashes in it, cannot be a nickname for a remote on Windows, as
  that is likely to be a pathname on a local filesystem.
- The "collision detecting" SHA-1 implementation shipped with 2.13
  was quite broken on some big-endian platforms and/or platforms that
  do not like unaligned fetches.  Update to the upstream code which
  has already fixed these issues.
- "git am -h" triggered a BUG().
- The interaction of "url.*.insteadOf" and custom URL scheme's
  whitelisting is now documented better.

* Wed May 10 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.13.0-0
- Use of an empty string as a pathspec element that is used for
  'everything matches' is still warned and Git asks users to use a
  more explicit '.' for that instead.  The hope is that existing
  users will not mind this change, and eventually the warning can be
  turned into a hard error, upgrading the deprecation into removal of
  this (mis)feature.  That is not scheduled to happen in the upcoming
  release (yet).
- The historical argument order "git merge <msg> HEAD <commit>..."
  has been deprecated for quite some time, and is now removed.
- The default location "~/.git-credential-cache/socket" for the
  socket used to communicate with the credential-cache daemon has
  been moved to "~/.cache/git/credential/socket".
- Git now avoids blindly falling back to ".git" when the setup
  sequence said we are _not_ in Git repository.  A corner case that
  happens to work right now may be broken by a call to die("BUG").
  We've tried hard to locate such cases and fixed them, but there
  might still be cases that need to be addressed--bug reports are
  greatly appreciated.

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.12.2-0
- "git status --porcelain" is supposed to give a stable output, but a
  few strings were left as translatable by mistake.
- "Dumb http" transport used to misparse a nonsense http-alternates
  response, which has been fixed.
- "git diff --quiet" relies on the size field in diff_filespec to be
  correctly populated, but diff_populate_filespec() helper function
  made an incorrect short-cut when asked only to populate the size
  field for paths that need to go through convert_to_git() (e.g. CRLF
  conversion).
- There is no need for Python only to give a few messages to the
  standard error stream, but we somehow did.
- A leak in a codepath to read from a packed object in (rare) cases
  has been plugged.
- "git upload-pack", which is a counter-part of "git fetch", did not
  report a request for a ref that was not advertised as invalid.
  This is generally not a problem (because "git fetch" will stop
  before making such a request), but is the right thing to do.
- A "gc.log" file left by a backgrounded "gc --auto" disables further
  automatic gc; it has been taught to run at least once a day (by
  default) by ignoring a stale "gc.log" file that is too old.
- "git remote rm X", when a branch has remote X configured as the
  value of its branch.*.remote, tried to remove branch.*.remote and
  branch.*.merge and failed if either is unset.
- A caller of tempfile API that uses stdio interface to write to
  files may ignore errors while writing, which is detected when
  tempfile is closed (with a call to ferror()).  By that time, the
  original errno that may have told us what went wrong is likely to
  be long gone and was overwritten by an irrelevant value.
  close_tempfile() now resets errno to EIO to make errno at least
  predictable.
- "git show-branch" expected there were only very short branch names
  in the repository and used a fixed-length buffer to hold them
  without checking for overflow.
- The code that parses header fields in the commit object has been
  updated for (micro)performance and code hygiene.
- A test that creates a confusing branch whose name is HEAD has been
  corrected not to do so.
- "Cc:" on the trailer part does not have to conform to RFC strictly,
  unlike in the e-mail header.  "git send-email" has been updated to
  ignore anything after '>' when picking addresses, to allow non-address
  cruft like " # stable 4.4" after the address.
- "git push" had a handful of codepaths that could lead to a deadlock
  when unexpected error happened, which has been fixed.
- Code to read submodule.<name>.ignore config did not state the
  variable name correctly when giving an error message diagnosing
  misconfiguration.
- "git ls-remote" and "git archive --remote" are designed to work
  without being in a directory under Git's control.  However, recent
  updates revealed that we randomly look into a directory called
  .git/ without actually doing necessary set-up when working in a
  repository.  Stop doing so.
- The code to parse the command line "git grep <patterns>... <rev>
  [[--] <pathspec>...]" has been cleaned up, and a handful of bugs
  have been fixed (e.g. we used to check "--" if it is a rev).
- The code to parse "git -c VAR=VAL cmd" and set configuration
  variable for the duration of cmd had two small bugs, which have
  been fixed.
  This supersedes jc/config-case-cmdline topic that has been discarded.

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.12.1-0
- Reduce authentication round-trip over HTTP when the server supports
  just a single authentication method.  This also improves the
  behaviour when Git is misconfigured to enable http.emptyAuth
  against a server that does not authenticate without a username
  (i.e. not using Kerberos etc., which makes http.emptyAuth
  pointless).
- Windows port wants to use OpenSSL's implementation of SHA-1
  routines, so let them.
- Add 32-bit Linux variant to the set of platforms to be tested with
  Travis CI.
- When a redirected http transport gets an error during the
  redirected request, we ignored the error we got from the server,
  and ended up giving a not-so-useful error message.
- The patch subcommand of "git add -i" was meant to have paths
  selection prompt just like other subcommand, unlike "git add -p"
  directly jumps to hunk selection.  Recently, this was broken and
  "add -i" lost the paths selection dialog, but it now has been
  fixed.
- Git v2.12 was shipped with an embarrassing breakage where various
  operations that verify paths given from the user stopped dying when
  seeing an issue, and instead later triggering segfault.
- The code to parse "git log -L..." command line was buggy when there
  are many ranges specified with -L; overrun of the allocated buffer
  has been fixed.
- The command-line parsing of "git log -L" copied internal data
  structures using incorrect size on ILP32 systems.

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 2.12.0-0
- Use of an empty string that is used for 'everything matches' is
  still warned and Git asks users to use a more explicit '.' for that
  instead.  The hope is that existing users will not mind this
  change, and eventually the warning can be turned into a hard error,
  upgrading the deprecation into removal of this (mis)feature.  That
  is not scheduled to happen in the upcoming release (yet).
- The historical argument order "git merge <msg> HEAD <commit>..."
  has been deprecated for quite some time, and will be removed in a
  future release.
- An ancient script "git relink" has been removed.
- Various updates to "git p4".
- "git p4" didn't interact with the internal of .git directory
  correctly in the modern "git-worktree"-enabled world.
- "git branch --list" and friends learned "--ignore-case" option to
  optionally sort branches and tags case insensitively.
- In addition to (subject), (body), "log --pretty=format:..."
  learned a new placeholder (trailers).
- "git rebase" learned "--quit" option, which allows a user to
  remove the metadata left by an earlier "git rebase" that was
  manually aborted without using "git rebase --abort".
- "git clone --reference $there --recurse-submodules $super" has been
  taught to guess repositories usable as references for submodules of
  $super that are embedded in $there while making a clone of the
  superproject borrow objects from $there; extend the mechanism to
  also allow submodules of these submodules to borrow repositories
  embedded in these clones of the submodules embedded in the clone of
  the superproject.
- Porcelain scripts written in Perl are getting internationalized.
- "git merge --continue" has been added as a synonym to "git commit"
  to conclude a merge that has stopped due to conflicts.
- Finer-grained control of what protocols are allowed for transports
  during clone/fetch/push have been enabled via a new configuration
  mechanism.
- "git shortlog" learned "--committer" option to group commits by
  committer, instead of author.
- GitLFS integration with "git p4" has been updated.
- The isatty() emulation for Windows has been updated to eradicate
  the previous hack that depended on internals of (older) MSVC
  runtime.
- Some platforms no longer understand "latin-1" that is still seen in
  the wild in e-mail headers; replace them with "iso-8859-1" that is
  more widely known when conversion fails from/to it.
- "git grep" has been taught to optionally recurse into submodules.
- "git rm" used to refuse to remove a submodule when it has its own
  git repository embedded in its working tree.  It learned to move
  the repository away to $GIT_DIR/modules/ of the superproject
  instead, and allow the submodule to be deleted (as long as there
  will be no loss of local modifications, that is).
- A recent updates to "git p4" was not usable for older p4 but it
  could be made to work with minimum changes.  Do so.
- "git diff" learned diff.interHunkContext configuration variable
  that gives the default value for its --inter-hunk-context option.
- The prereleaseSuffix feature of version comparison that is used in
  "git tag -l" did not correctly when two or more prereleases for the
  same release were present (e.g. when 2.0, 2.0-beta1, and 2.0-beta2
  are there and the code needs to compare 2.0-beta1 and 2.0-beta2).
- "git submodule push" learned "--recurse-submodules=only option to
  push submodules out without pushing the top-level superproject.
- "git tag" and "git verify-tag" learned to put GPG verification
  status in their "--format=<placeholders>" output format.
- An ancient repository conversion tool left in contrib/ has been
  removed.
- "git show-ref HEAD" used with "--verify" because the user is not
  interested in seeing refs/remotes/origin/HEAD, and used with
  "--head" because the user does not want HEAD to be filtered out,
  i.e. "git show-ref --head --verify HEAD", did not work as expected.
- "git submodule add" used to be confused and refused to add a
  locally created repository; users can now use "--force" option
  to add them.
  (merge 619acfc78c sb/submodule-add-force later to maint).
- Some people feel the default set of colors used by "git log --graph"
  rather limiting.  A mechanism to customize the set of colors has
  been introduced.
- "git read-tree" and its underlying unpack_trees() machinery learned
  to report problematic paths prefixed with the --super-prefix option.
- When a submodule "A", which has another submodule "B" nested within
  it, is "absorbed" into the top-level superproject, the inner
  submodule "B" used to be left in a strange state.  The logic to
  adjust the .git pointers in these submodules has been corrected.
- The user can specify a custom update method that is run when
  "submodule update" updates an already checked out submodule.  This
  was ignored when checking the submodule out for the first time and
  we instead always just checked out the commit that is bound to the
  path in the superproject's index.
- The command line completion (in contrib/) learned that
  "git diff --submodule=" can take "diff" as a recently added option.
- The "core.logAllRefUpdates" that used to be boolean has been
  enhanced to take 'always' as well, to record ref updates to refs
  other than the ones that are expected to be updated (i.e. branches,
  remote-tracking branches and notes).
- Comes with more command line completion (in contrib/) for recently
  introduced options.
  - Commands that operate on a log message and add lines to the trailer
  blocks, such as "format-patch -s", "cherry-pick (-x|-s)", and
  "commit -s", have been taught to use the logic of and share the
  code with "git interpret-trailer".
- The default Travis-CI configuration specifies newer P4 and GitLFS.
- The "fast hash" that had disastrous performance issues in some
  corner cases has been retired from the internal diff.
- The character width table has been updated to match Unicode 9.0
- Update the procedure to generate "tags" for developer support.
- The codeflow of setting NOATIME and CLOEXEC on file descriptors Git
  opens has been simplified.
- "git diff" and its family had two experimental heuristics to shift
  the contents of a hunk to make the patch easier to read.  One of
  them turns out to be better than the other, so leave only the
  "--indent-heuristic" option and remove the other one.
- A new submodule helper "git submodule embedgitdirs" to make it
  easier to move embedded .git/ directory for submodules in a
  superproject to .git/modules/ (and point the latter with the former
  that is turned into a "gitdir:" file) has been added.
- "git push \\server\share\dir" has recently regressed and then
  fixed.  A test has retroactively been added for this breakage.
- Build updates for Cygwin.
- The implementation of "real_path()" was to go there with chdir(2)
  and call getcwd(3), but this obviously wouldn't be usable in a
  threaded environment.  Rewrite it to manually resolve relative
  paths including symbolic links in path components.
- Adjust documentation to help AsciiDoctor render better while not
  breaking the rendering done by AsciiDoc.
- The sequencer machinery has been further enhanced so that a later
  set of patches can start using it to reimplement "rebase -i".
- Update the definition of the MacOSX test environment used by
  TravisCI.
- Rewrite a scripted porcelain "git difftool" in C.
- "make -C t failed" will now run only the tests that failed in the
  previous run.  This is usable only when prove is not use, and gives
  a useless error message when run after "make clean", but otherwise
  is serviceable.
- "uchar [40]" to "struct object_id" conversion continues.
