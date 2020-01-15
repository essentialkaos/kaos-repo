################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

################################################################################

Summary:          Core git tools
Name:             git
Version:          2.24.1
Release:          0%{?dist}
License:          GPL
Group:            Development/Tools
URL:              https://git-scm.com

Source0:          https://github.com/git/git/archive/v%{version}.tar.gz

Source100:        checksum.sha512

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
%{crc_check}

%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}" \
     %{path_settings} \
     all

%install
rm -rf %{buildroot}

%{__make} %{?_smp_mflags} CFLAGS="%{optflags}" DESTDIR=%{buildroot} \
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
* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.24.1-0
- This release merges up the fixes that appear in v2.14.6, v2.15.4,
  v2.17.3, v2.20.2 and in v2.21.1, addressing the security issues
  CVE-2019-1348, CVE-2019-1349, CVE-2019-1350, CVE-2019-1351,
  CVE-2019-1352, CVE-2019-1353, CVE-2019-1354, CVE-2019-1387, and
  CVE-2019-19604

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.24.0-0
- "filter-branch" is showing its age and alternatives are available.
  From this release, we started to discourage its use and hint
  people about filter-repo.
- We now have an active interim maintainer for the Git-Gui part of
  the system.  Praise and thank Pratyush Yadav for volunteering.
- The command line parser learned "--end-of-options" notation; the
  standard convention for scripters to have hardcoded set of options
  first on the command line, and force the command to treat end-user
  input as non-options, has been to use "--" as the delimiter, but
  that would not work for commands that use "--" as a delimiter
  between revs and pathspec.
- A mechanism to affect the default setting for a (related) group of
  configuration variables is introduced.
- "git fetch" learned "--set-upstream" option to help those who first
  clone from their private fork they intend to push to, add the true
  upstream via "git remote add" and then "git fetch" from it.
- Device-tree files learned their own userdiff patterns.
- "git rebase --rebase-merges" learned to drive different merge
  strategies and pass strategy specific options to them.
- A new "pre-merge-commit" hook has been introduced.
- Command line completion updates for "git -c var.name=val" have been
  added.
- The lazy clone machinery has been taught that there can be more
  than one promisor remote and consult them in order when downloading
  missing objects on demand.
- The list-objects-filter API (used to create a sparse/lazy clone)
  learned to take a combined filter specification.
- The documentation and tests for "git format-patch" have been
  cleaned up.
- On Windows, the root level of UNC share is now allowed to be used
  just like any other directory.
- The command line completion support (in contrib/) learned about the
  "--skip" option of "git revert" and "git cherry-pick".
- "git rebase --keep-base <upstream>" tries to find the original base
  of the topic being rebased and rebase on top of that same base,
  which is useful when running the "git rebase -i" (and its limited
  variant "git rebase -x").
  The command also has learned to fast-forward in more cases where it
  can instead of replaying to recreate identical commits.
- A configuration variable tells "git fetch" to write the commit
  graph after finishing.
- "git add -i" has been taught to show the total number of hunks and
  the hunks that has been processed so far when showing prompts.
- "git fetch --jobs=<n>" allowed <n> parallel jobs when fetching
  submodules, but this did not apply to "git fetch --multiple" that
  fetches from multiple remote repositories.  It now does.
- The installation instruction for zsh completion script (in
  contrib/) has been a bit improved.
- The code to write commit-graph over given commit object names has
  been made a bit more robust.
- The first line of verbose output from each test piece now carries
  the test name and number to help scanning with eyeballs.
- Further clean-up of the initialization code.
- xmalloc() used to have a mechanism to ditch memory and address
  space resources as the last resort upon seeing an allocation
  failure from the underlying malloc(), which made the code complex
  and thread-unsafe with dubious benefit, as major memory resource
  users already do limit their uses with various other mechanisms.
  It has been simplified away.
- Unnecessary full-tree diff in "git log -L" machinery has been
  optimized away.
- The http transport lacked some optimization the native transports
  learned to avoid unnecessary ref advertisement, which has been
  corrected.
- Preparation for SHA-256 upgrade continues in the test department.
- The memory ownership model of the "git fast-import" got
  straightened out.
- Output from trace2 subsystem is formatted more prettily now.
- The internal code originally invented for ".gitignore" processing
  got reshuffled and renamed to make it less tied to "excluding" and
  stress more that it is about "matching", as it has been reused for
  things like sparse checkout specification that want to check if a
  path is "included".
- "git stash" learned to write refreshed index back to disk.
- Coccinelle checks are done on more source files than before now.
- The cache-tree code has been taught to be less aggressive in
  attempting to see if a tree object it computed already exists in
  the repository.
- The code to parse and use the commit-graph file has been made more
  robust against corrupted input.
- The hg-to-git script (in contrib/) has been updated to work with
  Python 3.
- Update the way build artifacts in t/helper/ directory are ignored.
- Preparation for SHA-256 upgrade continues.
- "git log --graph" for an octopus merge is sometimes colored
  incorrectly, which is demonstrated and documented but not yet
  fixed.
- The trace2 output, when sending them to files in a designated
  directory, can populate the directory with too many files; a
  mechanism is introduced to set the maximum number of files and
  discard further logs when the maximum is reached.
- We have adopted a Code-of-conduct document.
- "git grep --recurse-submodules" that looks at the working tree
  files looked at the contents in the index in submodules, instead of
  files in the working tree.
- Codepaths to walk tree objects have been audited for integer
  overflows and hardened.
- "git pack-refs" can lose refs that are created while running, which
  is getting corrected.
- "git checkout" and "git restore" to re-populate the index from a
  tree-ish (typically HEAD) did not work correctly for a path that
  was removed and then added again with the intent-to-add bit, when
  the corresponding working tree file was empty.  This has been
  corrected.
- Compilation fix.
- "git gui" learned to call the clean-up procedure before exiting.
- We promoted the "indent heuristics" that decides where to split
  diff hunks from experimental to the default a few years ago, but
  some stale documentation still marked it as experimental, which has
  been corrected.
- Fix a mismerge that happened in 2.22 timeframe.
- "git archive" recorded incorrect length in extended pax header in
  some corner cases, which has been corrected.
- On-demand object fetching in lazy clone incorrectly tried to fetch
  commits from submodule projects, while still working in the
  superproject, which has been corrected.
- Prepare get_short_oid() codepath to be thread-safe.
- "for-each-ref" and friends that show refs did not protect themselves
  against ancient tags that did not record tagger names when asked to
  show "%%(taggername)", which have been corrected.
- The "git am" based backend of "git rebase" ignored the result of
  updating ".gitattributes" done in one step when replaying
  subsequent steps.
- Tell cURL library to use the same malloc() implementation, with the
  xmalloc() wrapper, as the rest of the system, for consistency.
- Build fix to adjust .gitignore to unignore a path that we started to track.
- A few implementation fixes in the notes API.
- Fix an earlier regression to "git push --all" which should have
  been forbidden when the target remote repository is set to be a
  mirror.
- Fix an earlier regression in the test suite, which mistakenly
  stopped running HTTPD tests.
- "git rebase --autostash <upstream> <branch>", when <branch> is
  different from the current branch, incorrectly moved the tip of the
  current branch, which has been corrected.
- Update support for Asciidoctor documentation toolchain.
- Start using DocBook 5 (instead of DocBook 4.5) as Asciidoctor 2.0
  no longer works with the older one.
- The markup used in user-manual has been updated to work better with
  asciidoctor.
- Make sure the grep machinery does not abort when seeing a payload
  that is not UTF-8 even when JIT is not in use with PCRE1.
- The name of the blob object that stores the filter specification
  for sparse cloning/fetching was interpreted in a wrong place in the
  code, causing Git to abort.
- "git log --decorate-refs-exclude=<pattern>" was incorrectly
  overruled when the "--simplify-by-decoration" option is used, which
  has been corrected.
- The "upload-pack" (the counterpart of "git fetch") needs to disable
  commit-graph when responding to a shallow clone/fetch request, but
  the way this was done made Git panic, which has been corrected.
- The object traversal machinery has been optimized not to load tree
  objects when we are only interested in commit history.
- The object name parser for "Nth parent" syntax has been made more
  robust against integer overflows.
- The code used in following tags in "git fetch" has been optimized.
- Regression fix for progress output.
- A bug in merge-recursive code that triggers when a branch with a
  symbolic link is merged with a branch that replaces it with a
  directory has been fixed.
- The rename detection logic sorts a list of rename source candidates
  by similarity to pick the best candidate, which means that a tie
  between sources with the same similarity is broken by the original
  location in the original candidate list (which is sorted by path).
  Force the sorting by similarity done with a stable sort, which is
  not promised by system supplied qsort(3), to ensure consistent
  results across platforms.
- The code to skip "UTF" and "UTF-" prefix, when computing an advice
  message, did not work correctly when the prefix was "UTF", which
  has been fixed.
- The author names taken from SVN repositories may have extra leading
  or trailing whitespaces, which are now munged away.
- "git rebase -i" showed a wrong HEAD while "reword" open the editor.
- A few simplification and bugfixes to PCRE interface.
- PCRE fixes.
- "git range-diff" segfaulted when diff.noprefix configuration was
  used, as it blindly expected the patch it internally generates to
  have the standard a/ and b/ prefixes.  The command now forces the
  internal patch to be built without any prefix, not to be affected
  by any end-user configuration.
- "git stash apply" in a subdirectory of a secondary worktree failed
  to access the worktree correctly, which has been corrected.
- The merge-recursive machinery is one of the most complex parts of
  the system that accumulated cruft over time.  This large series
  cleans up the implementation quite a bit.
- Pretty-printed command line formatter (used in e.g. reporting the
  command being run by the tracing API) had a bug that lost an
  argument that is an empty string, which has been corrected.
- "git range-diff" failed to handle mode-only change, which has been
  corrected.
- Dev support update.
- "git format-patch -o <outdir>" did an equivalent of "mkdir <outdir>"
  not "mkdir -p <outdir>", which was corrected.
- "git stash save" lost local changes to submodules, which has been
  corrected.
- The atomic push over smart HTTP transport did not work, which has
  been corrected.
- Other code cleanup, docfix, build fix, etc.

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.23.0-0
- The "--base" option of "format-patch" computed the patch-ids for
  prerequisite patches in an unstable way, which has been updated to
  compute in a way that is compatible with "git patch-id --stable".
- The "git log" command by default behaves as if the --mailmap option
  was given.
- The "git fast-export/import" pair has been taught to handle commits
  with log messages in encoding other than UTF-8 better.
- In recent versions of Git, per-worktree refs are exposed in
  refs/worktrees/<wtname>/ hierarchy, which means that worktree names
  must be a valid refname component.  The code now sanitizes the names
  given to worktrees, to make sure these refs are well-formed.
- "git merge" learned "--quit" option that cleans up the in-progress
  merge while leaving the working tree and the index still in a mess.
- "git format-patch" learns a configuration to set the default for
  its --notes=<ref> option.
- The code to show args with potential typo that cannot be
  interpreted as a commit-ish has been improved.
- "git clone --recurse-submodules" learned to set up the submodules
  to ignore commit object names recorded in the superproject gitlink
  and instead use the commits that happen to be at the tip of the
  remote-tracking branches from the get-go, by passing the new
  "--remote-submodules" option.
- The pattern "git diff/grep" use to extract funcname and words
  boundary for Matlab has been extend to cover Octave, which is more
  or less equivalent.
- "git help git" was hard to discover (well, at least for some
  people).
- The pattern "git diff/grep" use to extract funcname and words
  boundary for Rust has been added.
- "git status" can be told a non-standard default value for the
  "--[no-]ahead-behind" option with a new configuration variable
  status.aheadBehind.
- "git fetch" and "git pull" reports when a fetch results in
  non-fast-forward updates to let the user notice unusual situation.
  The commands learned "--no-show-forced-updates" option to disable
  this safety feature.
- Two new commands "git switch" and "git restore" are introduced to
  split "checking out a branch to work on advancing its history" and
  "checking out paths out of the index and/or a tree-ish to work on
  advancing the current history" out of the single "git checkout"
  command.
- "git branch --list" learned to always output the detached HEAD as
  the first item (when the HEAD is detached, of course), regardless
  of the locale.
- The conditional inclusion mechanism learned to base the choice on
  the branch the HEAD currently is on.
- "git rev-list --objects" learned the "--no-object-names" option to
  squelch the path to the object that is used as a grouping hint for
  pack-objects.
- A new tag.gpgSign configuration variable turns "git tag -a" into
  "git tag -s".
- "git multi-pack-index" learned expire and repack subcommands.
- "git blame" learned to "ignore" commits in the history, whose
  effects (as well as their presence) get ignored.
- "git cherry-pick/revert" learned a new "--skip" action.
- The tips of refs from the alternate object store can be used as
  starting point for reachability computation now.
- Extra blank lines in "git status" output have been reduced.
- The commits in a repository can be described by multiple
  commit-graph files now, which allows the commit-graph files to be
  updated incrementally.
- "git range-diff" output has been tweaked for easier identification
  of which part of what file the patch shown is about.
- Update supporting parts of "git rebase" to remove code that should
  no longer be used.
- Developer support to emulate unsatisfied prerequisites in tests to
  ensure that the remainder of the tests still succeeds when tests
  with prerequisites are skipped.
- "git update-server-info" learned not to rewrite the file with the
  same contents.
- The way of specifying the path to find dynamic libraries at runtime
  has been simplified.  The old default to pass -R/path/to/dir has been
  replaced with the new default to pass -Wl,-rpath,/path/to/dir,
  which is the more recent GCC uses.  Those who need to build with an
  old GCC can still use "CC_LD_DYNPATH=-R"
- Prepare use of reachability index in topological walker that works
  on a range (A..B).
- A new tutorial targeting specifically aspiring git-core
  developers has been added.
- Auto-detect how to tell HP-UX aCC where to use dynamically linked
  libraries from at runtime.
- "git mergetool" and its tests now spawn fewer subprocesses.
- Dev support update to help tracing out tests.
- Support to build with MSVC has been updated.
- "git fetch" that grabs from a group of remotes learned to run the
  auto-gc only once at the very end.
- A handful of Windows build patches have been upstreamed.
- The code to read state files used by the sequencer machinery for
  "git status" has been made more robust against a corrupt or stale
  state files.
- "git for-each-ref" with multiple patterns have been optimized.
- The tree-walk API learned to pass an in-core repository
  instance throughout more codepaths.
- When one step in multi step cherry-pick or revert is reset or
  committed, the command line prompt script failed to notice the
  current status, which has been improved.
- Many GIT_TEST_* environment variables control various aspects of
  how our tests are run, but a few followed "non-empty is true, empty
  or unset is false" while others followed the usual "there are a few
  ways to spell true, like yes, on, etc., and also ways to spell
  false, like no, off, etc." convention.
- Adjust the dir-iterator API and apply it to the local clone
  optimization codepath.
- We have been trying out a few language features outside c89; the
  coding guidelines document did not talk about them and instead had
  a blanket ban against them.
- A test helper has been introduced to optimize preparation of test
  repositories with many simple commits, and a handful of test
  scripts have been updated to use it.

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 2.22.1-0
- A relative pathname given to "git init --template=<path> <repo>"
  ought to be relative to the directory "git init" gets invoked in,
  but it instead was made relative to the repository, which has been
  corrected.
- "git worktree add" used to fail when another worktree connected to
  the same repository was corrupt, which has been corrected.
- The ownership rule for the file descriptor to fast-import remote
  backend was mixed up, leading to unrelated file descriptor getting
  closed, which has been fixed.
- "git update-server-info" used to leave stale packfiles in its
  output, which has been corrected.
- The server side support for "git fetch" used to show incorrect
  value for the HEAD symbolic ref when the namespace feature is in
  use, which has been corrected.
- "git am -i --resolved" segfaulted after trying to see a commit as
  if it were a tree, which has been corrected.
- "git bundle verify" needs to see if prerequisite objects exist in
  the receiving repository, but the command did not check if we are
  in a repository upfront, which has been corrected.
- "git merge --squash" is designed to update the working tree and the
  index without creating the commit, and this cannot be countermanded
  by adding the "--commit" option; the command now refuses to work
  when both options are given.
- The data collected by fsmonitor was not properly written back to
  the on-disk index file, breaking t7519 tests occasionally, which
  has been corrected.
- Update to Unicode 12.1 width table.
- The command line to invoke a "git cat-file" command from inside
  "git p4" was not properly quoted to protect a caret and running a
  broken command on Windows, which has been corrected.
- "git request-pull" learned to warn when the ref we ask them to pull
  from in the local repository and in the published repository are
  different.
- When creating a partial clone, the object filtering criteria is
  recorded for the origin of the clone, but this incorrectly used a
  hardcoded name "origin" to name that remote; it has been corrected
  to honor the "--origin <name>" option.
- "git fetch" into a lazy clone forgot to fetch base objects that are
  necessary to complete delta in a thin packfile, which has been
  corrected.
- The filter_data used in the list-objects-filter (which manages a
  lazily sparse clone repository) did not use the dynamic array API
  correctly---'nr' is supposed to point at one past the last element
  of the array in use.  This has been corrected.
- The description about slashes in gitignore patterns (used to
  indicate things like "anchored to this level only" and "only
  matches directories") has been revamped.
- The URL decoding code has been updated to avoid going past the end
  of the string while parsing %%-<hex>-<hex> sequence.
- The list of for-each like macros used by clang-format has been
  updated.
- "git push --atomic" that goes over the transport-helper (namely,
  the smart http transport) failed to prevent refs to be pushed when
  it can locally tell that one of the ref update will fail without
  having to consult the other end, which has been corrected.
- "git clean" silently skipped a path when it cannot lstat() it; now
  it gives a warning.
- A codepath that reads from GPG for signed object verification read
  past the end of allocated buffer, which has been fixed.
- "git rm" to resolve a conflicted path leaked an internal message
  "needs merge" before actually removing the path, which was
  confusing.  This has been corrected.
- The "git clone" documentation refers to command line options in its
  description in the short form; they have been replaced with long
  forms to make them more recognisable.
- The configuration variable rebase.rescheduleFailedExec should be
  effective only while running an interactive rebase and should not
  affect anything when running a non-interactive one, which was not
  the case.  This has been corrected.
- "git submodule foreach" did not protect command line options passed
  to the command to be run in each submodule correctly, when the
  "--recursive" option was in use.
- Use "Erase in Line" CSI sequence that is already used in the editor
  support to clear cruft in the progress output.
- The codepath to compute delta islands used to spew progress output
  without giving the callers any way to squelch it, which has been
  fixed.
- The code to parse scaled numbers out of configuration files has
  been made more robust and also easier to follow.
- An incorrect list of options was cached after command line
  completion failed (e.g. trying to complete a command that requires
  a repository outside one), which has been corrected.
- "git rebase --abort" used to leave refs/rewritten/ when concluding
  "git rebase -r", which has been corrected.
- "git stash show 23" used to work, but no more after getting
  rewritten in C; this regression has been corrected.
- "git interpret-trailers" always treated '#' as the comment
  character, regardless of core.commentChar setting, which has been
  corrected.
- Code clean-up to avoid signed integer overlaps during binary search.
- "git checkout -p" needs to selectively apply a patch in reverse,
  which did not work well.
- The commit-graph file is now part of the "files that the runtime
  may keep open file descriptors on, all of which would need to be
  closed when done with the object store", and the file descriptor to
  an existing commit-graph file now is closed before "gc" finalizes a
  new instance to replace it.
- Code restructuring during 2.20 period broke fetching tags via
  "import" based transports.
- We have been trying out a few language features outside c89; the
  coding guidelines document did not talk about them and instead had
  a blanket ban against them.
- The internal diff machinery can be made to read out of bounds while
  looking for --funcion-context line in a corner case, which has been
  corrected.

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 2.22.0-0
- The filter specification "--filter=sparse:path=<path>" used to
  create a lazy/partial clone has been removed.  Using a blob that is
  part of the project as sparse specification is still supported with
  the "--filter=sparse:oid=<blob>" option.
- "git checkout --no-overlay" can be used to trigger a new mode of
  checking out paths out of the tree-ish, that allows paths that
  match the pathspec that are in the current index and working tree
  and are not in the tree-ish.
- The %%(trailers) formatter in "git log --format=..."  now allows to
  optionally pick trailers selectively by keyword, show only values,
  etc.
- Four new configuration variables {author,committer}.{name,email}
  have been introduced to override user.{name,email} in more specific
  cases.
- Command-line completion (in contrib/) learned to tab-complete the
  "git submodule absorbgitdirs" subcommand.
- "git branch" learned a new subcommand "--show-current".
- Output from "diff --cc" did not show the original paths when the
  merge involved renames.  A new option adds the paths in the
  original trees to the output.
- The command line completion (in contrib/) has been taught to
  complete more subcommand parameters.
- The final report from "git bisect" used to show the suspected
  culprit using a raw "diff-tree", with which there is no output for
  a merge commit.  This has been updated to use a more modern and
  human readable output that still is concise enough.
- "git rebase --rebase-merges" replaces its old "--preserve-merges"
  option; the latter is now marked as deprecated.
- Error message given while cloning with --recurse-submodules has
  been updated.
- The completion helper code now pays attention to repository-local
  configuration (when available), which allows --list-cmds to honour
  a repository specific setting of completion.commands, for example.
- "git mergetool" learned to offer Sublime Merge (smerge) as one of
  its backends.
- A new hook "post-index-change" is called when the on-disk index
  file changes, which can help e.g. a virtualized working tree
  implementation.
- "git difftool" can now run outside a repository.
- "git checkout -m <other>" was about carrying the differences
  between HEAD and the working-tree files forward while checking out
  another branch, and ignored the differences between HEAD and the
  index.  The command has been taught to abort when the index and the
  HEAD are different.
- A progress indicator has been added to the "index-pack" step, which
  often makes users wait for completion during "git clone".
- "git submodule" learns "set-branch" subcommand that allows the
  submodule.*.branch settings to be modified.
- "git merge-recursive" backend recently learned a new heuristics to
  infer file movement based on how other files in the same directory
  moved.  As this is inherently less robust heuristics than the one
  based on the content similarity of the file itself (rather than
  based on what its neighbours are doing), it sometimes gives an
  outcome unexpected by the end users.  This has been toned down to
  leave the renamed paths in higher/conflicted stages in the index so
  that the user can examine and confirm the result.
- "git tag" learned to give an advice suggesting it might be a
  mistake when creating an annotated or signed tag that points at
  another tag.
- The "git pack-objects" command learned to report the number of
  objects it packed via the trace2 mechanism.
- The list of conflicted paths shown in the editor while concluding a
  conflicted merge was shown above the scissors line when the
  clean-up mode is set to "scissors", even though it was commented
  out just like the list of updated paths and other information to
  help the user explain the merge better.
- The trace2 tracing facility learned to auto-generate a filename
  when told to log to a directory.
- "git clone" learned a new --server-option option when talking over
  the protocol version 2.
- The connectivity bitmaps are created by default in bare
  repositories now; also the pathname hash-cache is created by
  default to avoid making crappy deltas when repacking.
- "git branch new A...B" and "git checkout -b new A...B" have been
  taught that in their contexts, the notation A...B means "the merge
  base between these two commits", just like "git checkout A...B"
  detaches HEAD at that commit.
- Update "git difftool" and "git mergetool" so that the combinations
  of {diff,merge}.{tool,guitool} configuration variables serve as
  fallback settings of each other in a sensible order.
- The "--dir-diff" mode of "git difftool" is not useful in "--no-index"
  mode; they are now explicitly marked as mutually incompatible.
- The diff machinery, one of the oldest parts of the system, which
  long predates the parse-options API, uses fairly long and complex
  handcrafted option parser.  This is being rewritten to use the
  parse-options API.
- The implementation of pack-redundant has been updated for
  performance in a repository with many packfiles.
- A more structured way to obtain execution trace has been added.
- "git prune" has been taught to take advantage of reachability
  bitmap when able.
- The command line parser of "git commit-tree" has been rewritten to
  use the parse-options API.
- Suggest GitGitGadget instead of submitGit as a way to submit
  patches based on GitHub PR to us.
- The test framework has been updated to help developers by making it
  easier to run most of the tests under different versions of
  over-the-wire protocols.
- Dev support update to make it easier to compare two formatted
  results from our documentation.
- The scripted "git rebase" implementation has been retired.
- "git multi-pack-index verify" did not scale well with the number of
  packfiles, which is being improved.
- "git stash" has been rewritten in C.
- The "check-docs" Makefile target to support developers has been
  updated.
- The tests have been updated not to rely on the abbreviated option
  names the parse-options API offers, to protect us from an
  abbreviated form of an option that used to be unique within the
  command getting non-unique when a new option that share the same
  prefix is added.
- The scripted version of "git rebase -i" wrote and rewrote the todo
  list many times during a single step of its operation, and the
  recent C-rewrite made a faithful conversion of the logic to C.  The
  implementation has been updated to carry necessary information
  around in-core to avoid rewriting the same file over and over
  unnecessarily.
- Test framework update to more robustly clean up leftover files and
  processes after tests are done.
- Conversion from unsigned char[20] to struct object_id continues.
- While running "git diff" in a lazy clone, we can upfront know which
  missing blobs we will need, instead of waiting for the on-demand
  machinery to discover them one by one.  The code learned to aim to
  achieve better performance by batching the request for these
  promised blobs.
- During an initial "git clone --depth=..." partial clone, it is
  pointless to spend cycles for a large portion of the connectivity
  check that enumerates and skips promisor objects (which by
  definition is all objects fetched from the other side).  This has
  been optimized out.
- Mechanically and systematically drop "extern" from function
  declaration.
- The script to aggregate perf result unconditionally depended on
  libjson-perl even though it did not have to, which has been
  corrected.
- The internal implementation of "git rebase -i" has been updated to
  avoid forking a separate "rebase--interactive" process.
- Allow DEP and ASLR for Windows build to for security hardening.
- Performance test framework has been broken and measured the version
  of Git that happens to be on $PATH, not the specified one to
  measure, for a while, which has been corrected.
- Optionally "make coccicheck" can feed multiple source files to
  spatch, gaining performance while spending more memory.
- Attempt to use an abbreviated option in "git clone --recurs" is
  responded by a request to disambiguate between --recursive and
  --recurse-submodules, which is bad because these two are synonyms.
  The parse-options API has been extended to define such synonyms
  more easily and not produce an unnecessary failure.
- A pair of private functions in http.c that had names similar to
  fread/fwrite did not return the number of elements, which was found
  to be confusing.
- Update collision-detecting SHA-1 code to build properly on HP-UX.
- "git prune-packed" did not notice and complain against excess
  arguments given from the command line, which now it does.
- Split-index fix.
- "git diff --no-index" may still want to access Git goodies like
  --ext-diff and --textconv, but so far these have been ignored,
  which has been corrected.
- Unify RPC code for smart http in protocol v0/v1 and v2, which fixes
  a bug in the latter (lack of authentication retry) and generally
  improves the code base.
- The include file compat/bswap.h has been updated so that it is safe
  to (accidentally) include it more than once.
- The set of header files used by "make hdr-check" unconditionally
  included sha256/gcrypt.h, even when it is not used, causing the
  make target to fail.  We now skip it when GCRYPT_SHA256 is not in
  use.
- The Makefile uses 'find' utility to enumerate all the *.h header
  files, which is expensive on platforms with slow filesystems; it
  now optionally uses "ls-files" if working within a repository,
  which is a trick similar to how all sources are enumerated to run
  ETAGS on.
- "git rebase" that was reimplemented in C did not set ORIG_HEAD
  correctly, which has been corrected.
- Dev support.
- CFLAGS now can be tweaked when invoking Make while using
  DEVELOPER=YesPlease; this did not work well before.
- "git fsck --connectivity-only" omits computation necessary to sift
  the objects that are not reachable from any of the refs into
  unreachable and dangling.  This is now enabled when dangling
  objects are requested (which is done by default, but can be
  overridden with the "--no-dangling" option).
- On platforms where "git fetch" is killed with SIGPIPE (e.g. OSX),
  the upload-pack that runs on the other end that hangs up after
  detecting an error could cause "git fetch" to die with a signal,
  which led to a flaky test.  "git fetch" now ignores SIGPIPE during
  the network portion of its operation (this is not a problem as we
  check the return status from our write(2)s).
- A recent update broke "is this object available to us?" check for
  well-known objects like an empty tree (which should yield "yes",
  even when there is no on-disk object for an empty tree), which has
  been corrected.
- The setup code has been cleaned up to avoid leaks around the
  repository_format structure.
- "git config --type=color ..." is meant to replace "git config --get-color"
  but there is a slight difference that wasn't documented, which is
  now fixed.
- When the "clean" filter can reduce the size of a huge file in the
  working tree down to a small "token" (a la Git LFS), there is no
  point in allocating a huge scratch area upfront, but the buffer is
  sized based on the original file size.  The convert mechanism now
  allocates very minimum and reallocates as it receives the output
  from the clean filter process.
- "git rebase" uses the refs/rewritten/ hierarchy to store its
  intermediate states, which inherently makes the hierarchy per
  worktree, but it didn't quite work well.
- "git log -L<from>,<to>:<path>" with "-s" did not suppress the patch
  output as it should.  This has been corrected.
- "git worktree add" used to do a "find an available name with stat
  and then mkdir", which is race-prone.  This has been fixed by using
  mkdir and reacting to EEXIST in a loop.
- Build update for SHA-1 with collision detection.
- Build procedure has been fixed around use of asciidoctor instead of
  asciidoc.
- remote-http transport did not anonymize URLs reported in its error
  messages at places.
- Error messages given from the http transport have been updated so
  that they can be localized.
- "git init" forgot to read platform-specific repository
  configuration, which made Windows port to ignore settings of
  core.hidedotfiles, for example.
- A corner-case object name ambiguity while the sequencer machinery
  is working (e.g. "rebase -i -x") has been fixed.
- "git format-patch" did not diagnose an error while opening the
  output file for the cover-letter, which has been corrected.
- "git checkout -f <branch>" while the index has an unmerged path
  incorrectly left some paths in an unmerged state, which has been
  corrected.
- A corner case bug in the refs API has been corrected.
- Unicode update.
- dumb-http walker has been updated to share more error recovery
  strategy with the normal codepath.
- A buglet in configuration parser has been fixed.
- The documentation for "git read-tree --reset -u" has been updated.
- Code clean-up around a much-less-important-than-it-used-to-be
  update_server_info() function.
- The message given when "git commit -a <paths>" errors out has been
  updated.
- "git cherry-pick --options A..B", after giving control back to the
  user to ask help resolving a conflicted step, did not honor the
  options it originally received, which has been corrected.
- Various glitches in "git gc" around reflog handling have been fixed.
- The code to read from commit-graph file has been cleanup with more
  careful error checking before using data read from it.
- Performance fix around "git fetch" that grabs many refs.
- Protocol v2 support in "git fetch-pack" of shallow clones has been
  corrected.
- Performance fix around "git blame", especially in a linear history
  (which is the norm we should optimize for).
- Performance fix for "rev-list --parents -- pathspec".
- Updating the display with progress message has been cleaned up to
  deal better with overlong messages.
- "git blame -- path" in a non-bare repository starts blaming from
  the working tree, and the same command in a bare repository errors
  out because there is no working tree by definition.  The command
  has been taught to instead start blaming from the commit at HEAD,
  which is more useful.
- An underallocation in the code to read the untracked cache
  extension has been corrected.
- The code is updated to check the result of memory allocation before
  it is used in more places, by using xmalloc and/or xcalloc calls.
- The GETTEXT_POISON test option has been quite broken ever since it
  was made runtime-tunable, which has been fixed.
- Test fix on APFS that is incapable of store paths in Latin-1.
- "git submodule foreach <command> --quiet" did not pass the option
  down correctly, which has been corrected.
- "git send-email" has been taught to use quoted-printable when the
  payload contains carriage-return.  The use of the mechanism is in
  line with the design originally added the codepath that chooses QP
  when the payload has overly long lines.
- The recently added feature to add addresses that are on
  anything-by: trailers in 'git send-email' was found to be way too
  eager and considered nonsense strings as if they can be legitimate
  beginning of *-by: trailer.  This has been tightened.
- Builds with gettext broke on recent macOS w/ Homebrew, which
  seems to have stopped including from /usr/local/include; this
  has been corrected.
- Running "git add" on a repository created inside the current
  repository is an explicit indication that the user wants to add it
  as a submodule, but when the HEAD of the inner repository is on an
  unborn branch, it cannot be added as a submodule.  Worse, the files
  in its working tree can be added as if they are a part of the outer
  repository, which is not what the user wants.  These problems are
  being addressed.
- "git cherry-pick" run with the "-x" or the "--signoff" option used
  to (and more importantly, ought to) clean up the commit log message
  with the --cleanup=space option by default, but this has been
  broken since late 2017.  This has been fixed.
- When given a tag that points at a commit-ish, "git replace --graft"
  failed to peel the tag before writing a replace ref, which did not
  make sense because the old graft mechanism the feature wants to
  mimic only allowed to replace one commit object with another.
  This has been fixed.
- Code tightening against a "wrong" object appearing where an object
  of a different type is expected, instead of blindly assuming that
  the connection between objects are correctly made.
- An earlier update for MinGW and Cygwin accidentally broke MSVC build,
  which has been fixed.
- %%(push:track) token used in the --format option to "git
  for-each-ref" and friends was not showing the right branch, which
  has been fixed.
- "make check-docs", "git help -a", etc. did not account for cases
  where a particular build may deliberately omit some subcommands,
  which has been corrected.
- The logic to tell if a Git repository has a working tree protects
  "git branch -D" from removing the branch that is currently checked
  out by mistake.  The implementation of this logic was broken for
  repositories with unusual name, which unfortunately is the norm for
  submodules these days.  This has been fixed.
- AIX shared the same build issues with other BSDs around fileno(fp),
  which has been corrected.
- The autoconf generated configure script failed to use the right
  gettext() implementations from -libintl by ignoring useless stub
  implementations shipped in some C library, which has been
  corrected.
- Fix index-pack perf test so that the repeated invocations always
  run in an empty repository, which emulates the initial clone
  situation better.
- A "ls-files" that emulates "find" to enumerate files in the working
  tree resulted in duplicated Makefile rules that caused the build to
  issue an unnecessary warning during a trial build after merge
  conflicts are resolved in working tree *.h files but before the
  resolved results are added to the index.  This has been corrected.
- "git cherry-pick" (and "revert" that shares the same runtime engine)
  that deals with multiple commits got confused when the final step
  gets stopped with a conflict and the user concluded the sequence
  with "git commit".  Attempt to fix it by cleaning up the state
  files used by these commands in such a situation.
- On a filesystem like HFS+, the names of the refs stored as filesystem
  entities may become different from what the end-user expects, just
  like files in the working tree get "renamed".  Work around the
  mismatch by paying attention to the core.precomposeUnicode
  configuration.
- The code to generate the multi-pack idx file was not prepared to
  see too many packfiles and ran out of open file descriptor, which
  has been corrected.
- To run tests for Git SVN, our scripts for CI used to install the
  git-svn package (in the hope that it would bring in the right
  dependencies).  This has been updated to install the more direct
  dependency, namely, libsvn-perl.
- "git cvsexportcommit" running on msys did not expect cvsnt showed
  "cvs status" output with CRLF line endings.
- The fsmonitor interface got out of sync after the in-core index
  file gets discarded, which has been corrected.
- "git status" did not know that the "label" instruction in the
  todo-list "rebase -i -r" uses should not be shown as a hex object
  name.
- A prerequisite check in the test suite to see if a working jgit is
  available was made more robust.
- The codepath to parse :<path> that obtains the object name for an
  indexed object has been made more robust.

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.20.1-0
- A few newly added tests were not portable and caused minority
  platforms to report false breakages, which have been fixed.
- Portability fix for a recent update to parse-options API.
- "git help -a" did not work well when an overly long alias is
  defined, which has been corrected.
- A recent update accidentally squelched an error message when the
  run_command API failed to run a missing command, which has been
  corrected.

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 2.20.0-0
- "git branch -l <foo>" used to be a way to ask a reflog to be
  created while creating a new branch, but that is no longer the
  case.  It is a short-hand for "git branch --list <foo>" now.
- "git push" into refs/tags/* hierarchy is rejected without getting
  forced, but "git fetch" (misguidedly) used the "fast forwarding"
  rule used for the refs/heads/* hierarchy; this has been corrected,
  which means some fetches of tags that did not fail with older
  version of Git will fail without "--force" with this version.
- "git help -a" now gives verbose output (same as "git help -av").
  Those who want the old output may say "git help --no-verbose -a"..
- "git cpn --help", when "cpn" is an alias to, say, "cherry-pick -n",
  reported only the alias expansion of "cpn" in earlier versions of
  Git.  It now runs "git cherry-pick --help" to show the manual page
  of the command, while sending the alias expansion to the standard
  error stream.
- "git send-email" learned to grab address-looking string on any
  trailer whose name ends with "-by". This is a backward-incompatible
  change.  Adding "--suppress-cc=misc-by" on the command line, or
  setting sendemail.suppresscc configuration variable to "misc-by",
  can be used to disable this behaviour.
- Running "git clone" against a project that contain two files with
  pathnames that differ only in cases on a case insensitive
  filesystem would result in one of the files lost because the
  underlying filesystem is incapable of holding both at the same
  time.  An attempt is made to detect such a case and warn.
- "git checkout -b newbranch [HEAD]" should not have to do as much as
  checking out a commit different from HEAD.  An attempt is made to
  optimize this special case.
- "git rev-list --stdin </dev/null" used to be an error; it now shows
  no output without an error.  "git rev-list --stdin --default HEAD"
  still falls back to the given default when nothing is given on the
  standard input.
- Lift code from GitHub to restrict delta computation so that an
  object that exists in one fork is not made into a delta against
  another object that does not appear in the same forked repository.
- "git format-patch" learned new "--interdiff" and "--range-diff"
  options to explain the difference between this version and the
  previous attempt in the cover letter (or after the three-dashes as
  a comment).
- "git mailinfo" used in "git am" learned to make a best-effort
  recovery of a patch corrupted by MUA that sends text/plain with
  format=flawed option.
- The rules used by "git push" and "git fetch" to determine if a ref
  can or cannot be updated were inconsistent; specifically, fetching
  to update existing tags were allowed even though tags are supposed
  to be unmoving anchoring points.  "git fetch" was taught to forbid
  updates to existing tags without the "--force" option.
- "git multi-pack-index" learned to detect corruption in the .midx
  file it uses, and this feature has been integrated into "git fsck".
- Generation of (experimental) commit-graph files have so far been
  fairly silent, even though it takes noticeable amount of time in a
  meaningfully large repository.  The users will now see progress
  output.
- The minimum version of Windows supported by Windows port of Git is
  now set to Vista.
- The completion script (in contrib/) learned to complete a handful of
  options "git stash list" command takes.
- The completion script (in contrib/) learned that "git fetch
  --multiple" only takes remote names as arguments and no refspecs.
- "git status" learns to show progress bar when refreshing the index
  takes a long time.
- "git help -a" and "git help -av" give different pieces of
  information, and generally the "verbose" version is more friendly
  to the new users.  "git help -a" by default now uses the more
  verbose output (with "--no-verbose", you can go back to the
  original).  Also "git help -av" now lists aliases and external
  commands, which it did not used to.
- Unlike "grep", "git grep" by default recurses to the whole tree.
  The command learned "git grep --recursive" option, so that "git
  grep --no-recursive" can serve as a synonym to setting the
  max-depth to 0.
- When pushing into a repository that borrows its objects from an
  alternate object store, "git receive-pack" that responds to the
  push request on the other side lists the tips of refs in the
  alternate to reduce the amount of objects transferred.  This
  sometimes is detrimental when the number of refs in the alternate
  is absurdly large, in which case the bandwidth saved in potentially
  fewer objects transferred is wasted in excessively large ref
  advertisement.  The alternate refs that are advertised are now
  configurable with a pair of configuration variables.
- "git cmd --help" when "cmd" is aliased used to only say "cmd is
  aliased to ...".  Now it shows that to the standard error stream
  and runs "git $cmd --help" where $cmd is the first word of the
  alias expansion.
- The documentation of "git gc" has been updated to mention that it
  is no longer limited to "pruning away crufts" but also updates
  ancillary files like commit-graph as a part of repository
  optimization.
- "git p4 unshelve" improvements.
- The logic to select the default user name and e-mail on Windows has
  been improved.
- The "rev-list --filter" feature learned to exclude all trees via
  "tree:0" filter.
- "git send-email" learned to grab address-looking string on any
  trailer whose name ends with "-by"; --suppress-cc=misc-by on the
  command line, or setting sendemail.suppresscc configuration
  variable to "misc-by", can be used to disable this behaviour.
- "git mergetool" learned to take the "--[no-]gui" option, just like
  "git difftool" does.
- "git rebase -i" learned a new insn, 'break', that the user can
  insert in the to-do list.  Upon hitting it, the command returns
  control back to the user.
- New "--pretty=format:" placeholders %%GF and %%GP that show the GPG
  key fingerprints have been invented.
- On platforms with recent cURL library, http.sslBackend configuration
  variable can be used to choose a different SSL backend at runtime.
  The Windows port uses this mechanism to switch between OpenSSL and
  Secure Channel while talking over the HTTPS protocol.
- "git send-email" learned to disable SMTP authentication via the
  "--smtp-auth=none" option, even when the smtp username is given
  (which turns the authentication on by default).
- A fourth class of configuration files (in addition to the
  traditional "system wide", "per user in the $HOME directory" and
  "per repository in the $GIT_DIR/config") has been introduced so
  that different worktrees that share the same repository (hence the
  same $GIT_DIR/config file) can use different customization.
- A pattern with '**' that does not have a slash on either side used
  to be an invalid one, but the code now treats such double-asterisks
  the same way as two normal asterisks that happen to be adjacent to
  each other.
- The "--no-patch" option, which can be used to get a high-level
  overview without the actual line-by-line patch difference shown, of
  the "range-diff" command was earlier broken, which has been
  corrected.
- The recently merged "rebase in C" has an escape hatch to use the
  scripted version when necessary, but it hasn't been documented,
  which has been corrected.
- Developer builds now use -Wunused-function compilation option.
- One of our CI tests to run with "unusual/experimental/random"
  settings now also uses commit-graph and midx.
- When there are too many packfiles in a repository (which is not
  recommended), looking up an object in these would require
  consulting many pack .idx files; a new mechanism to have a single
  file that consolidates all of these .idx files is introduced.
- "git submodule update" is getting rewritten piece-by-piece into C.
- The code for computing history reachability has been shuffled,
  obtained a bunch of new tests to cover them, and then being
  improved.
- The unpack_trees() API used in checking out a branch and merging
  walks one or more trees along with the index.  When the cache-tree
  in the index tells us that we are walking a tree whose flattened
  contents is known (i.e. matches a span in the index), as linearly
  scanning a span in the index is much more efficient than having to
  open tree objects recursively and listing their entries, the walk
  can be optimized, which has been done.
- When creating a thin pack, which allows objects to be made into a
  delta against another object that is not in the resulting pack but
  is known to be present on the receiving end, the code learned to
  take advantage of the reachability bitmap; this allows the server
  to send a delta against a base beyond the "boundary" commit.
- spatch transformation to replace boolean uses of !hashcmp() to
  newly introduced oideq() is added, and applied, to regain
  performance lost due to support of multiple hash algorithms.
- Fix a bug in which the same path could be registered under multiple
  worktree entries if the path was missing (for instance, was removed
  manually).  Also, as a convenience, expand the number of cases in
  which --force is applicable.
- Split Documentation/config.txt for easier maintenance.
- Test helper binaries clean-up.
- Various tests have been updated to make it easier to swap the
  hash function used for object identification.
- Update fsck.skipList implementation and documentation.
- An alias that expands to another alias has so far been forbidden,
  but now it is allowed to create such an alias.
- Various test scripts have been updated for style and also correct
  handling of exit status of various commands.
- "gc --auto" ended up calling exit(-1) upon error, which has been
  corrected to use exit(1).  Also the error reporting behaviour when
  daemonized has been updated to exit with zero status when stopping
  due to a previously discovered error (which implies there is no
  point running gc to improve the situation); we used to exit with
  failure in such a case.
- Various codepaths in the core-ish part learned to work on an
  arbitrary in-core index structure, not necessarily the default
  instance "the_index".
- Code clean-up in the internal machinery used by "git status" and
  "git commit --dry-run".
- Some environment variables that control the runtime options of Git
  used during tests are getting renamed for consistency.
- A pair of new extensions to the index file have been introduced.
  They allow the index file to be read in parallel for performance.
- The oidset API was built on top of the oidmap API which in turn is
  on the hashmap API.  Replace the implementation to build on top of
  the khash API and gain performance.
- Over some transports, fetching objects with an exact commit object
  name can be done without first seeing the ref advertisements.  The
  code has been optimized to exploit this.
- In a partial clone that will lazily be hydrated from the
  originating repository, we generally want to avoid "does this
  object exist (locally)?" on objects that we deliberately omitted
  when we created the clone.  The cache-tree codepath (which is used
  to write a tree object out of the index) however insisted that the
  object exists, even for paths that are outside of the partial
  checkout area.  The code has been updated to avoid such a check.
- To help developers, an EditorConfig file that attempts to follow
  the project convention has been added.
- The result of coverage test can be combined with "git blame" to
  check the test coverage of code introduced recently with a new
  'coverage-diff' tool (in contrib/).
- An experiment to fuzz test a few areas, hopefully we can gain more
  coverage to various areas.
- More codepaths are moving away from hardcoded hash sizes.
- The way the Windows port figures out the current directory has been
  improved.
- The way DLLs are loaded on the Windows port has been improved.
- Some tests have been reorganized and renamed; "ls t/" now gives a
  better overview of what is tested for these scripts than before.
- "git rebase" and "git rebase -i" have been reimplemented in C.
- Windows port learned to use nano-second resolution file timestamps.
- The overly large Documentation/config.txt file have been split into
  million little pieces.  This potentially allows each individual piece
  to be included into the manual page of the command it affects more easily.
- Replace three string-list instances used as look-up tables in "git
  fetch" with hashmaps.
- Unify code to read the author-script used in "git am" and the
  commands that use the sequencer machinery, e.g. "git rebase -i".
- In preparation to the day when we can deprecate and remove the
  "rebase -p", make sure we can skip and later remove tests for
  it.
- The history traversal used to implement the tag-following has been
  optimized by introducing a new helper.
- The helper function to refresh the cached stat information in the
  in-core index has learned to perform the lstat() part of the
  operation in parallel on multi-core platforms.
- The code to traverse objects for reachability, used to decide what
  objects are unreferenced and expendable, have been taught to also
  consider per-worktree refs of other worktrees as starting points to
  prevent data loss.
- "git add" needs to internally run "diff-files" equivalent, and the
  codepath learned the same optimization as "diff-files" has to run
  lstat(2) in parallel to find which paths have been updated in the
  working tree.
- The procedure to install dependencies before testing at Travis CI
  is getting revamped for both simplicity and flexibility, taking
  advantage of the recent move to the vm-based environment.
- The support for format-patch (and send-email) by the command-line
  completion script (in contrib/) has been simplified a bit.
- The revision walker machinery learned to take advantage of the
  commit generation numbers stored in the commit-graph file.
- The codebase has been cleaned up to reduce "#ifndef NO_PTHREADS".
- The way -lcurl library gets linked has been simplified by taking
  advantage of the fact that we can just ask curl-config command how.
- Various functions have been audited for "-Wunused-parameter" warnings
  and bugs in them got fixed.
- A sanity check for start-up sequence has been added in the config
  API codepath.
- The build procedure to link for fuzzing test has been made
  customizable with a new Makefile variable.
- The way "git rebase" parses and forwards the command line options
  meant for underlying "git am" has been revamped, which fixed for
  options with parameters that were not passed correctly.
- Our testing framework uses a special i18n "poisoned localization"
  feature to find messages that ought to stay constant but are
  incorrectly marked to be translated.  This feature has been made
  into a runtime option (it used to be a compile-time option).
- "git push" used to check ambiguities between object-names and
  refnames while processing the list of refs' old and new values,
  which was unnecessary (as it knew that it is feeding raw object
  names).  This has been optimized out.
- The xcurl_off_t() helper function is used to cast size_t to
  curl_off_t, but some compilers gave warnings against the code to
  ensure the casting is done without wraparound, when size_t is
  narrower than curl_off_t.  This warning has been squelched.
- Code preparation to replace ulong vars with size_t vars where
  appropriate continues.
- The "test installed Git" mode of our test suite has been updated to
  work better.
- A coding convention around the Coccinelle semantic patches to have
  two classes to ease code migration process has been proposed and
  its support has been added to the Makefile.
- The "container" mode of TravisCI is going away.  Our .travis.yml
  file is getting prepared for the transition.
- Our test scripts can now take the '-V' option as a synonym for the
  '--verbose-log' option.
- "git interpret-trailers" and its underlying machinery had a buggy
  code that attempted to ignore patch text after commit log message,
  which triggered in various codepaths that will always get the log
  message alone and never get such an input.
- Malformed or crafted data in packstream can make our code attempt
  to read or write past the allocated buffer and abort, instead of
  reporting an error, which has been fixed.
- "git rebase -i" did not clear the state files correctly when a run
  of "squash/fixup" is aborted and then the user manually amended the
  commit instead, which has been corrected.
- When fsmonitor is in use, after operation on submodules updates
  .gitmodules, we lost track of the fact that we did so and relied on
  stale fsmonitor data.
- Fix for a long-standing bug that leaves the index file corrupt when
  it shrinks during a partial commit.
- Further fix for O_APPEND emulation on Windows
- A corner case bugfix in "git rerere" code.
- "git add ':(attr:foo)'" is not supported and is supposed to be
  rejected while the command line arguments are parsed, but we fail
  to reject such a command line upfront.
- Recent update broke the reachability algorithm when refs (e.g.
  tags) that point at objects that are not commit were involved,
  which has been fixed.
- "git rebase" etc. in Git 2.19 fails to abort when given an empty
  commit log message as result of editing, which has been corrected.
- The code to backfill objects in lazily cloned repository did not
  work correctly, which has been corrected.
- Update error messages given by "git remote" and make them consistent.
- "git update-ref" learned to make both "--no-deref" and "--stdin"
  work at the same time.
- Recently added "range-diff" had a corner-case bug to cause it
  segfault, which has been corrected.
- The recently introduced commit-graph auxiliary data is incompatible
  with mechanisms such as replace & grafts that "breaks" immutable
  nature of the object reference relationship.  Disable optimizations
  based on its use (and updating existing commit-graph) when these
  incompatible features are in use in the repository.
- The mailmap file update.
- The code in "git status" sometimes hit an assertion failure.  This
  was caused by a structure that was reused without cleaning the data
  used for the first run, which has been corrected.
- "git fetch $repo $object" in a partial clone did not correctly
  fetch the asked-for object that is referenced by an object in
  promisor packfile, which has been fixed.
- A corner-case bugfix.
- Various fixes to "diff --color-moved-ws".
- A partial clone that is configured to lazily fetch missing objects
  will on-demand issue a "git fetch" request to the originating
  repository to fill not-yet-obtained objects.  The request has been
  optimized for requesting a tree object (and not the leaf blob
  objects contained in it) by telling the originating repository that
  no blobs are needed.
- The codepath to support the experimental split-index mode had
  remaining "racily clean" issues fixed.
- "git log --graph" showing an octopus merge sometimes miscounted the
  number of display columns it is consuming to show the merge and its
  parent commits, which has been corrected.
- "git range-diff" did not work well when the compared ranges had
  changes in submodules and the "--submodule=log" was used.
- The implementation of run_command() API on the UNIX platforms had a
  bug that caused a command not on $PATH to be found in the current
  directory.
- A mutex used in "git pack-objects" were not correctly initialized
  and this caused "git repack" to dump core on Windows.
- Under certain circumstances, "git diff D:/a/b/c D:/a/b/d" on
  Windows would strip initial parts from the paths because they
  were not recognized as absolute, which has been corrected.
- The receive.denyCurrentBranch=updateInstead codepath kicked in even
  when the push should have been rejected due to other reasons, such
  as it does not fast-forward or the update-hook rejects it, which
  has been corrected.
- The logic to determine the archive type "git archive" uses did not
  correctly kick in for "git archive --remote", which has been
  corrected.
- "git repack" in a shallow clone did not correctly update the
  shallow points in the repository, leading to a repository that
  does not pass fsck.
- Some codepaths failed to form a proper URL when .gitmodules record
  the URL to a submodule repository as relative to the repository of
  superproject, which has been corrected.
- "git fetch" over protocol v2 into a shallow repository failed to
  fetch full history behind a new tip of history that was diverged
  before the cut-off point of the history that was previously fetched
  shallowly.
- The command line completion machinery (in contrib/) has been
  updated to allow the completion script to tweak the list of options
  that are reported by the parse-options machinery correctly.
- Operations on promisor objects make sense in the context of only a
  small subset of the commands that internally use the revisions
  machinery, but the "--exclude-promisor-objects" option were taken
  and led to nonsense results by commands like "log", to which it
  didn't make much sense.  This has been corrected.
- A regression in Git 2.12 era made "git fsck" fall into an infinite
  loop while processing truncated loose objects.
- "git ls-remote $there foo" was broken by recent update for the
  protocol v2 and stopped showing refs that match 'foo' that are not
  refs/{heads,tags}/foo, which has been fixed.
- Additional comment on a tricky piece of code to help developers.
- A couple of tests used to leave the repository in a state that is
  deliberately corrupt, which have been corrected.
- The submodule support has been updated to read from the blob at
  HEAD:.gitmodules when the .gitmodules file is missing from the
  working tree.
- "git fetch" was a bit loose in parsing responses from the other side
  when talking over the protocol v2.
- "git rev-parse --exclude=* --branches --branches"  (i.e. first
  saying "add only things that do not match '*' out of all branches"
  and then adding all branches, without any exclusion this time)
  worked as expected, but "--exclude=* --all --all" did not work the
  same way, which has been fixed.
- "git send-email --transfer-encoding=..." in recent versions of Git
  sometimes produced an empty "Content-Transfer-Encoding:" header,
  which has been corrected.
- The interface into "xdiff" library used to discover the offset and
  size of a generated patch hunk by first formatting it into the
  textual hunk header "@@ -n,m +k,l @@" and then parsing the numbers
  out.  A new interface has been introduced to allow callers a more
  direct access to them.
- Pathspec matching against a tree object were buggy when negative
  pathspec elements were involved, which has been fixed.
- "git merge" and "git pull" that merges into an unborn branch used
  to completely ignore "--verify-signatures", which has been
  corrected.
- "git rebase --autostash" did not correctly re-attach the HEAD at times.
- "rev-parse --exclude=<pattern> --branches=<pattern>" etc. did not
  quite work, which has been corrected.
- When editing a patch in a "git add -i" session, a hunk could be
  made to no-op.  The "git apply" program used to reject a patch with
  such a no-op hunk to catch user mistakes, but it is now updated to
  explicitly allow a no-op hunk in an edited patch.
- The URL to an MSDN page in a comment has been updated.
- "git ls-remote --sort=<thing>" can feed an object that is not yet
  available into the comparison machinery and segfault, which has
  been corrected to check such a request upfront and reject it.
- When "git bundle" aborts due to an empty commit ranges
  (i.e. resulting in an empty pack), it left a file descriptor to an
  lockfile open, which resulted in leftover lockfile on Windows where
  you cannot remove a file with an open file descriptor.  This has
  been corrected.
- "git format-patch --stat=<width>" can be used to specify the width
  used by the diffstat (shown in the cover letter).
- The way .git/index and .git/sharedindex* files were initially
  created gave these files different perm bits until they were
  adjusted for shared repository settings.  This was made consistent.
- "git rebase --stat" to transplant a piece of history onto a totally
  unrelated history were not working before and silently showed wrong
  result.  With the recent reimplementation in C, it started to instead
  die with an error message, as the original logic was not prepared
  to cope with this case.  This has now been fixed.
- The advice message to tell the user to migrate an existing graft
  file to the replace system when a graft file was read was shown
  even when "git replace --convert-graft-file" command, which is the
  way the message suggests to use, was running, which made little
  sense.
- "git diff --raw" lost ellipses to adjust the output columns for
  some time now, but the documentation still showed them.

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.19.2-0
- "git interpret-trailers" and its underlying machinery had a buggy
  code that attempted to ignore patch text after commit log message,
  which triggered in various codepaths that will always get the log
  message alone and never get such an input.
- "git rebase -i" did not clear the state files correctly when a run
  of "squash/fixup" is aborted and then the user manually amended the
  commit instead, which has been corrected.
- When fsmonitor is in use, after operation on submodules updates
  .gitmodules, we lost track of the fact that we did so and relied on
  stale fsmonitor data.
- Fix for a long-standing bug that leaves the index file corrupt when
  it shrinks during a partial commit.
- Further fix for O_APPEND emulation on Windows
- A corner case bugfix in "git rerere" code.
- "git add ':(attr:foo)'" is not supported and is supposed to be
  rejected while the command line arguments are parsed, but we fail
  to reject such a command line upfront.
- "git rebase" etc. in Git 2.19 fails to abort when given an empty
  commit log message as result of editing, which has been corrected.
- The code to backfill objects in lazily cloned repository did not
  work correctly, which has been corrected.
- Update error messages given by "git remote" and make them consistent.
- "git update-ref" learned to make both "--no-deref" and "--stdin"
  work at the same time.
- Recently added "range-diff" had a corner-case bug to cause it
  segfault, which has been corrected.
- The recently introduced commit-graph auxiliary data is incompatible
  with mechanisms such as replace & grafts that "breaks" immutable
  nature of the object reference relationship.  Disable optimizations
  based on its use (and updating existing commit-graph) when these
  incompatible features are in use in the repository.
- The mailmap file update.
- The code in "git status" sometimes hit an assertion failure.  This
  was caused by a structure that was reused without cleaning the data
  used for the first run, which has been corrected.
- A corner-case bugfix.
- A partial clone that is configured to lazily fetch missing objects
  will on-demand issue a "git fetch" request to the originating
  repository to fill not-yet-obtained objects.  The request has been
  optimized for requesting a tree object (and not the leaf blob
  objects contained in it) by telling the originating repository that
  no blobs are needed.
- The codepath to support the experimental split-index mode had
  remaining "racily clean" issues fixed.
- "git log --graph" showing an octopus merge sometimes miscounted the
  number of display columns it is consuming to show the merge and its
  parent commits, which has been corrected.
- The implementation of run_command() API on the UNIX platforms had a
  bug that caused a command not on $PATH to be found in the current
  directory.
- A mutex used in "git pack-objects" were not correctly initialized
  and this caused "git repack" to dump core on Windows.
- Under certain circumstances, "git diff D:/a/b/c D:/a/b/d" on
  Windows would strip initial parts from the paths because they
  were not recognized as absolute, which has been corrected.
- The receive.denyCurrentBranch=updateInstead codepath kicked in even
  when the push should have been rejected due to other reasons, such
  as it does not fast-forward or the update-hook rejects it, which
  has been corrected.
- "git repack" in a shallow clone did not correctly update the
  shallow points in the repository, leading to a repository that
  does not pass fsck.
- Operations on promisor objects make sense in the context of only a
  small subset of the commands that internally use the revisions
  machinery, but the "--exclude-promisor-objects" option were taken
  and led to nonsense results by commands like "log", to which it
  didn't make much sense.  This has been corrected.
- The "container" mode of TravisCI is going away.  Our .travis.yml
  file is getting prepared for the transition.
- Our test scripts can now take the '-V' option as a synonym for the
  '--verbose-log' option.
- A regression in Git 2.12 era made "git fsck" fall into an infinite
  loop while processing truncated loose objects.

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 2.19.1-0
- This release merges up the fixes that appear in v2.14.5 and in
  v2.17.2 to address the recently reported CVE-2018-17456

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 2.19.0-0
- "git diff" compares the index and the working tree.  For paths
  added with intent-to-add bit, the command shows the full contents
  of them as added, but the paths themselves were not marked as new
  files.  They are now shown as new by default.
  "git apply" learned the "--intent-to-add" option so that an
  otherwise working-tree-only application of a patch will add new
  paths to the index marked with the "intent-to-add" bit.
- "git grep" learned the "--column" option that gives not just the
  line number but the column number of the hit.
- The "-l" option in "git branch -l" is an unfortunate short-hand for
  "--create-reflog", but many users, both old and new, somehow expect
  it to be something else, perhaps "--list".  This step warns when "-l"
  is used as a short-hand for "--create-reflog" and warns about the
  future repurposing of the it when it is used.
- The userdiff pattern for .php has been updated.
- The content-transfer-encoding of the message "git send-email" sends
  out by default was 8bit, which can cause trouble when there is an
  overlong line to bust RFC 5322/2822 limit.  A new option 'auto' to
  automatically switch to quoted-printable when there is such a line
  in the payload has been introduced and is made the default.
- "git checkout" and "git worktree add" learned to honor
  checkout.defaultRemote when auto-vivifying a local branch out of a
  remote tracking branch in a repository with multiple remotes that
  have tracking branches that share the same names.
- "git grep" learned the "--only-matching" option.
- "git rebase --rebase-merges" mode now handles octopus merges as
  well.
- Add a server-side knob to skip commits in exponential/fibbonacci
  stride in an attempt to cover wider swath of history with a smaller
  number of iterations, potentially accepting a larger packfile
  transfer, instead of going back one commit a time during common
  ancestor discovery during the "git fetch" transaction.
- A new configuration variable core.usereplacerefs has been added,
  primarily to help server installations that want to ignore the
  replace mechanism altogether.
- Teach "git tag -s" etc. a few configuration variables (gpg.format
  that can be set to "openpgp" or "x509", and gpg.<format>.program
  that is used to specify what program to use to deal with the format)
  to allow x.509 certs with CMS via "gpgsm" to be used instead of
  openpgp via "gnupg".
- Many more strings are prepared for l10n.
- "git p4 submit" learns to ask its own pre-submit hook if it should
  continue with submitting.
- The test performed at the receiving end of "git push" to prevent
  bad objects from entering repository can be customized via
  receive.fsck.* configuration variables; we now have gained a
  counterpart to do the same on the "git fetch" side, with
  fetch.fsck.* configuration variables.
- "git pull --rebase=interactive" learned "i" as a short-hand for
  "interactive".
- "git instaweb" has been adjusted to run better with newer Apache on
  RedHat based distros.
- "git range-diff" is a reimplementation of "git tbdiff" that lets us
  compare individual patches in two iterations of a topic.
- The sideband code learned to optionally paint selected keywords at
  the beginning of incoming lines on the receiving end.
- "git branch --list" learned to take the default sort order from the
  'branch.sort' configuration variable, just like "git tag --list"
  pays attention to 'tag.sort'.
- "git worktree" command learned "--quiet" option to make it less
  verbose.
- The bulk of "git submodule foreach" has been rewritten in C.
- The in-core "commit" object had an all-purpose "void *util" field,
  which was tricky to use especially in library-ish part of the
  code.  All of the existing uses of the field has been migrated to a
  more dedicated "commit-slab" mechanism and the field is eliminated.
- A less often used command "git show-index" has been modernized.
- The conversion to pass "the_repository" and then "a_repository"
  throughout the object access API continues.
- Continuing with the idea to programatically enumerate various
  pieces of data required for command line completion, teach the
  codebase to report the list of configuration variables
  subcommands care about to help complete them.
- Separate "rebase -p" codepath out of "rebase -i" implementation to
  slim down the latter and make it easier to manage.
- Make refspec parsing codepath more robust.
- Some flaky tests have been fixed.
- Continuing with the idea to programmatically enumerate various
  pieces of data required for command line completion, the codebase
  has been taught to enumerate options prefixed with "--no-" to
  negate them.
- Build and test procedure for netrc credential helper (in contrib/)
  has been updated.
- Remove unused function definitions and declarations from ewah
  bitmap subsystem.
- Code preparation to make "git p4" closer to be usable with Python 3.
- Tighten the API to make it harder to misuse in-tree .gitmodules
  file, even though it shares the same syntax with configuration
  files, to read random configuration items from it.
- "git fast-import" has been updated to avoid attempting to create
  delta against a zero-byte-long string, which is pointless.
- The codebase has been updated to compile cleanly with -pedantic
  option.
- The character display width table has been updated to match the
  latest Unicode standard.
- test-lint now looks for broken use of "VAR=VAL shell_func" in test
  scripts.
- Conversion from uchar[40] to struct object_id continues.
- Recent "security fix" to pay attention to contents of ".gitmodules"
  while accepting "git push" was a bit overly strict than necessary,
  which has been adjusted.
- "git fsck" learns to make sure the optional commit-graph file is in
  a sane state.
- "git diff --color-moved" feature has further been tweaked.
- Code restructuring and a small fix to transport protocol v2 during
  fetching.
- Parsing of -L[<N>][,[<M>]] parameters "git blame" and "git log"
  take has been tweaked.
- lookup_commit_reference() and friends have been updated to find
  in-core object for a specific in-core repository instance.
- Various glitches in the heuristics of merge-recursive strategy have
  been documented in new tests.
- "git fetch" learned a new option "--negotiation-tip" to limit the
  set of commits it tells the other end as "have", to reduce wasted
  bandwidth and cycles, which would be helpful when the receiving
  repository has a lot of refs that have little to do with the
  history at the remote it is fetching from.
- For a large tree, the index needs to hold many cache entries
  allocated on heap.  These cache entries are now allocated out of a
  dedicated memory pool to amortize malloc(3) overhead.
- Tests to cover various conflicting cases have been added for
  merge-recursive.
- Tests to cover conflict cases that involve submodules have been
  added for merge-recursive.
- Look for broken "&&" chains that are hidden in subshell, many of
  which have been found and corrected.
- The singleton commit-graph in-core instance is made per in-core
  repository instance.
- "make DEVELOPER=1 DEVOPTS=pedantic" allows developers to compile
  with -pedantic option, which may catch more problematic program
  constructs and potential bugs.
- Preparatory code to later add json output for telemetry data has
  been added.
- Update the way we use Coccinelle to find out-of-style code that
  need to be modernised.
- It is too easy to misuse system API functions such as strcat();
  these selected functions are now forbidden in this codebase and
  will cause a compilation failure.
- Add a script (in contrib/) to help users of VSCode work better with
  our codebase.
- The Travis CI scripts were taught to ship back the test data from
  failed tests.
- The parse-options machinery learned to refrain from enclosing
  placeholder string inside a "<bra" and "ket>" pair automatically
  without PARSE_OPT_LITERAL_ARGHELP.  Existing help text for option
  arguments that are not formatted correctly have been identified and
  fixed.
- Noiseword "extern" has been removed from function decls in the
  header files.
- A few atoms like %%(objecttype) and %%(objectsize) in the format
  specifier of "for-each-ref --format=<format>" can be filled without
  getting the full contents of the object, but just with the object
  header.  These cases have been optimized by calling
  oid_object_info() API (instead of reading and inspecting the data).
- The end result of documentation update has been made to be
  inspected more easily to help developers.
- The API to iterate over all objects learned to optionally list
  objects in the order they appear in packfiles, which helps locality
  of access if the caller accesses these objects while as objects are
  enumerated.
- Improve built-in facility to catch broken &&-chain in the tests.
- The more library-ish parts of the codebase learned to work on the
  in-core index-state instance that is passed in by their callers,
  instead of always working on the singleton "the_index" instance.
- A test prerequisite defined by various test scripts with slightly
  different semantics has been consolidated into a single copy and
  made into a lazily defined one.
- After a partial clone, repeated fetches from promisor remote would
  have accumulated many packfiles marked with .promisor bit without
  getting them coalesced into fewer packfiles, hurting performance.
  "git repack" now learned to repack them.
- Partially revert the support for multiple hash functions to regain
  hash comparison performance; we'd think of a way to do this better
  in the next cycle.
- "git help --config" (which is used in command line completion)
  missed the configuration variables not described in the main
  config.txt file but are described in another file that is included
  by it, which has been corrected.
- The test linter code has learned that the end of here-doc mark
  "EOF" can be quoted in a double-quote pair, not just in a
  single-quote pair.
- "git remote update" can take both a single remote nickname and a
  nickname for remote groups, and the completion script (in contrib/)
  has been taught about it.
- "git fetch --shallow-since=<cutoff>" that specifies the cut-off
  point that is newer than the existing history used to end up
  grabbing the entire history.  Such a request now errors out.
- Fix for 2.17-era regression around `core.safecrlf`.
- The recent addition of "partial clone" experimental feature kicked
  in when it shouldn't, namely, when there is no partial-clone filter
  defined even if extensions.partialclone is set.
- "git send-pack --signed" (hence "git push --signed" over the http
  transport) did not read user ident from the config mechanism to
  determine whom to sign the push certificate as, which has been
  corrected.
- "git fetch-pack --all" used to unnecessarily fail upon seeing an
  annotated tag that points at an object other than a commit.
- When user edits the patch in "git add -p" and the user's editor is
  set to strip trailing whitespaces indiscriminately, an empty line
  that is unchanged in the patch would become completely empty
  (instead of a line with a sole SP on it).  The code introduced in
  Git 2.17 timeframe failed to parse such a patch, but now it learned
  to notice the situation and cope with it.
- The code to try seeing if a fetch is necessary in a submodule
  during a fetch with --recurse-submodules got confused when the path
  to the submodule was changed in the range of commits in the
  superproject, sometimes showing "(null)".  This has been corrected.
- Bugfix for "rebase -i" corner case regression.
- Recently added "--base" option to "git format-patch" command did
  not correctly generate prereq patch ids.
- POSIX portability fix in Makefile to fix a glitch introduced a few
  releases ago.
- "git filter-branch" when used with the "--state-branch" option
  still attempted to rewrite the commits whose filtered result is
  known from the previous attempt (which is recorded on the state
  branch); the command has been corrected not to waste cycles doing
  so.
- Clarify that setting core.ignoreCase to deviate from reality would
  not turn a case-incapable filesystem into a case-capable one.
- "fsck.skipList" did not prevent a blob object listed there from
  being inspected for is contents (e.g. we recently started to
  inspect the contents of ".gitmodules" for certain malicious
  patterns), which has been corrected.
- "git checkout --recurse-submodules another-branch" did not report
  in which submodule it failed to update the working tree, which
  resulted in an unhelpful error message.
- "git rebase" behaved slightly differently depending on which one of
  the three backends gets used; this has been documented and an
  effort to make them more uniform has begun.
- The "--ignore-case" option of "git for-each-ref" (and its friends)
  did not work correctly, which has been fixed.
- "git fetch" failed to correctly validate the set of objects it
  received when making a shallow history deeper, which has been
  corrected.
- Partial clone support of "git clone" has been updated to correctly
  validate the objects it receives from the other side.  The server
  side has been corrected to send objects that are directly
  requested, even if they may match the filtering criteria (e.g. when
  doing a "lazy blob" partial clone).
- Handling of an empty range by "git cherry-pick" was inconsistent
  depending on how the range ended up to be empty, which has been
  corrected.
- "git reset --merge" (hence "git merge ---abort") and "git reset --hard"
  had trouble working correctly in a sparsely checked out working
  tree after a conflict, which has been corrected.
- Correct a broken use of "VAR=VAL shell_func" in a test.
- "git rev-parse ':/substring'" did not consider the history leading
  only to HEAD when looking for a commit with the given substring,
  when the HEAD is detached.  This has been fixed.
- Build doc update for Windows.
- core.commentchar is now honored when preparing the list of commits
  to replay in "rebase -i".
- "git pull --rebase" on a corrupt HEAD caused a segfault.  In
  general we substitute an empty tree object when running the in-core
  equivalent of the diff-index command, and the codepath has been
  corrected to do so as well to fix this issue.
- httpd tests saw occasional breakage due to the way its access log
  gets inspected by the tests, which has been updated to make them
  less flaky.
- Tests to cover more D/F conflict cases have been added for
  merge-recursive.
- "git gc --auto" opens file descriptors for the packfiles before
  spawning "git repack/prune", which would upset Windows that does
  not want a process to work on a file that is open by another
  process.  The issue has been worked around.
- The recursive merge strategy did not properly ensure there was no
  change between HEAD and the index before performing its operation,
  which has been corrected.
- "git rebase" started exporting GIT_DIR environment variable and
  exposing it to hook scripts when part of it got rewritten in C.
  Instead of matching the old scripted Porcelains' behaviour,
  compensate by also exporting GIT_WORK_TREE environment as well to
  lessen the damage.  This can harm existing hooks that want to
  operate on different repository, but the current behaviour is
  already broken for them anyway.
- "git send-email" when using in a batched mode that limits the
  number of messages sent in a single SMTP session lost the contents
  of the variable used to choose between tls/ssl, unable to send the
  second and later batches, which has been fixed.
- The lazy clone support had a few places where missing but promised
  objects were not correctly tolerated, which have been fixed.
- One of the "diff --color-moved" mode "dimmed_zebra" that was named
  in an unusual way has been deprecated and replaced by
  "dimmed-zebra".
- The wire-protocol v2 relies on the client to send "ref prefixes" to
  limit the bandwidth spent on the initial ref advertisement.  "git
  clone" when learned to speak v2 forgot to do so, which has been
  corrected.
- "git diff --histogram" had a bad memory usage pattern, which has
  been rearranged to reduce the peak usage.
- Code clean-up to use size_t/ssize_t when they are the right type.
- The wire-protocol v2 relies on the client to send "ref prefixes" to
  limit the bandwidth spent on the initial ref advertisement.  "git
  fetch $remote branch:branch" that asks tags that point into the
  history leading to the "branch" automatically followed sent to
  narrow prefix and broke the tag following, which has been fixed.
- When the sparse checkout feature is in use, "git cherry-pick" and
  other mergy operations lost the skip_worktree bit when a path that
  is excluded from checkout requires content level merge, which is
  resolved as the same as the HEAD version, without materializing the
  merge result in the working tree, which made the path appear as
  deleted.  This has been corrected by preserving the skip_worktree
  bit (and not materializing the file in the working tree).
- The "author-script" file "git rebase -i" creates got broken when
  we started to move the command away from shell script, which is
  getting fixed now.
- The automatic tree-matching in "git merge -s subtree" was broken 5
  years ago and nobody has noticed since then, which is now fixed.
- "git fetch $there refs/heads/s" ought to fetch the tip of the
  branch 's', but when "refs/heads/refs/heads/s", i.e. a branch whose
  name is "refs/heads/s" exists at the same time, fetched that one
  instead by mistake.  This has been corrected to honor the usual
  disambiguation rules for abbreviated refnames.
- Futureproofing a helper function that can easily be misused.
- The http-backend (used for smart-http transport) used to slurp the
  whole input until EOF, without paying attention to CONTENT_LENGTH
  that is supplied in the environment and instead expecting the Web
  server to close the input stream.  This has been fixed.
- "git merge --abort" etc. did not clean things up properly when
  there were conflicted entries in the index in certain order that
  are involved in D/F conflicts.  This has been corrected.
- "git diff --indent-heuristic" had a bad corner case performance.
- The "--exec" option to "git rebase --rebase-merges" placed the exec
  commands at wrong places, which has been corrected.
- "git verify-tag" and "git verify-commit" have been taught to use
  the exit status of underlying "gpg --verify" to signal bad or
  untrusted signature they found.
- "git mergetool" stopped and gave an extra prompt to continue after
  the last path has been handled, which did not make much sense.
- Among the three codepaths we use O_APPEND to open a file for
  appending, one used for writing GIT_TRACE output requires O_APPEND
  implementation that behaves sensibly when multiple processes are
  writing to the same file.  POSIX emulation used in the Windows port
  has been updated to improve in this area.
- "git pull --rebase -v" in a repository with a submodule barfed as
  an intermediate process did not understand what "-v(erbose)" flag
  meant, which has been fixed.
- Recent update to "git config" broke updating variable in a
  subsection, which has been corrected.
- When "git rebase -i" is told to squash two or more commits into
  one, it labeled the log message for each commit with its number.
  It correctly called the first one "1st commit", but the next one
  was "commit #1", which was off-by-one.  This has been corrected.
- "git rebase -i", when a 'merge <branch>' insn in its todo list
  fails, segfaulted, which has been (minimally) corrected.
- "git cherry-pick --quit" failed to remove CHERRY_PICK_HEAD even
  though we won't be in a cherry-pick session after it returns, which
  has been corrected.
- In a recent update in 2.18 era, "git pack-objects" started
  producing a larger than necessary packfiles by missing
  opportunities to use large deltas.  This has been corrected.
- The meaning of the possible values the "core.checkStat"
  configuration variable can take were not adequately documented,
  which has been fixed.
- Recent "git rebase -i" update started to write bogusly formatted
  author-script, with a matching broken reading code.  These are
  fixed.
- Recent addition of "directory rename" heuristics to the
  merge-recursive backend makes the command susceptible to false
  positives and false negatives.  In the context of "git am -3",
  which does not know about surrounding unmodified paths and thus
  cannot inform the merge machinery about the full trees involved,
  this risk is particularly severe.  As such, the heuristic is
  disabled for "git am -3" to keep the machinery "more stupid but
  predictable".
- "git merge-base" in 2.19-rc1 has performance regression when the
  (experimental) commit-graph feature is in use, which has been
  mitigated.

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.18.0-0
- Rename detection logic that is used in "merge" and "cherry-pick" has
  learned to guess when all of x/a, x/b and x/c have moved to z/a,
  z/b and z/c, it is likely that x/d added in the meantime would also
  want to move to z/d by taking the hint that the entire directory
  'x' moved to 'z'.  A bug causing dirty files involved in a rename
  to be overwritten during merge has also been fixed as part of this
  work.  Incidentally, this also avoids updating a file in the
  working tree after a (non-trivial) merge whose result matches what
  our side originally had.
- "git filter-branch" learned to use a different exit code to allow
  the callers to tell the case where there was no new commits to
  rewrite from other error cases.
- When built with more recent cURL, GIT_SSL_VERSION can now specify
  "tlsv1.3" as its value.
- "git gui" learned that "~/.ssh/id_ecdsa.pub" and
  "~/.ssh/id_ed25519.pub" are also possible SSH key files.
- "git gui" performs commit upon CTRL/CMD+ENTER but the
  CTRL/CMD+KP_ENTER (i.e. enter key on the numpad) did not have the
  same key binding.  It now does.
- "git gui" has been taught to work with old versions of tk (like
  8.5.7) that do not support "ttk::style theme use" as a way to query
  the current theme.
- "git rebase" has learned to honor "--signoff" option when using
  backends other than "am" (but not "--preserve-merges").
- "git branch --list" during an interrupted "rebase -i" now lets
  users distinguish the case where a detached HEAD is being rebased
  and a normal branch is being rebased.
- "git mergetools" learned talking to guiffy.
- The scripts in contrib/emacs/ have outlived their usefulness and
  have been replaced with a stub that errors out and tells the user
  there are replacements.
- The new "working-tree-encoding" attribute can ask Git to convert the
  contents to the specified encoding when checking out to the working
  tree (and the other way around when checking in).
- The "git config" command uses separate options e.g. "--int",
  "--bool", etc. to specify what type the caller wants the value to
  be interpreted as.  A new "--type=<typename>" option has been
  introduced, which would make it cleaner to define new types.
- "git config --get" learned the "--default" option, to help the
  calling script.  Building on top of the above changes, the
  "git config" learns "--type=color" type.  Taken together, you can
  do things like "git config --get foo.color --default blue" and get
  the ANSI color sequence for the color given to foo.color variable,
  or "blue" if the variable does not exist.
- "git ls-remote" learned an option to allow sorting its output based
  on the refnames being shown.
- The command line completion (in contrib/) has been taught that "git
  stash save" has been deprecated ("git stash push" is the preferred
  spelling in the new world) and does not offer it as a possible
  completion candidate when "git stash push" can be.
- "git gc --prune=nonsense" spent long time repacking and then
  silently failed when underlying "git prune --expire=nonsense"
  failed to parse its command line.  This has been corrected.
- Error messages from "git push" can be painted for more visibility.
- "git http-fetch" (deprecated) had an optional and experimental
  "feature" to fetch only commits and/or trees, which nobody used.
  This has been removed.
- The functionality of "$GIT_DIR/info/grafts" has been superseded by
  the "refs/replace/" mechanism for some time now, but the internal
  code had support for it in many places, which has been cleaned up
  in order to drop support of the "grafts" mechanism.
- "git worktree add" learned to check out an existing branch.
- "git --no-pager cmd" did not have short-and-sweet single letter
  option. Now it does as "-P".
- "git rebase" learned "--rebase-merges" to transplant the whole
  topology of commit graph elsewhere.
- "git status" learned to pay attention to UI related diff
  configuration variables such as diff.renames.
- The command line completion mechanism (in contrib/) learned to load
  custom completion file for "git $command" where $command is a
  custom "git-$command" that the end user has on the $PATH when using
  newer version of bash-completion.
- "git send-email" can sometimes offer confirmation dialog "Send this
  email?" with choices 'Yes', 'No', 'Quit', and 'All'.  A new action
  'Edit' has been added to this dialog's choice.
- With merge.renames configuration set to false, the recursive merge
  strategy can be told not to spend cycles trying to find renamed
  paths and merge them accordingly.
- "git status" learned to honor a new status.renames configuration to
  skip rename detection, which could be useful for those who want to
  do so without disabling the default rename detection done by the
  "git diff" command.
- Command line completion (in contrib/) learned to complete pathnames
  for various commands better.
- "git blame" learns to unhighlight uninteresting metadata from the
  originating commit on lines that are the same as the previous one,
  and also paint lines in different colors depending on the age of
  the commit.
- Transfer protocol v2 learned to support the partial clone.
- When a short hexadecimal string is used to name an object but there
  are multiple objects that share the string as the prefix of their
  names, the code lists these ambiguous candidates in a help message.
  These object names are now sorted according to their types for
  easier eyeballing.
- "git fetch $there $refspec" that talks over protocol v2 can take
  advantage of server-side ref filtering; the code has been extended
  so that this mechanism triggers also when fetching with configured
  refspec.
- Our HTTP client code used to advertise that we accept gzip encoding
  from the other side; instead, just let cURL library to advertise
  and negotiate the best one.
- "git p4" learned to "unshelve" shelved commit from P4.
- A "git fetch" from a repository with insane number of refs into a
  repository that is already up-to-date still wasted too many cycles
  making many lstat(2) calls to see if these objects at the tips
  exist as loose objects locally.  These lstat(2) calls are optimized
  away by enumerating all loose objects beforehand.
  It is unknown if the new strategy negatively affects existing use
  cases, fetching into a repository with many loose objects from a
  repository with small number of refs.
- Git can be built to use either v1 or v2 of the PCRE library, and so
  far, the build-time configuration USE_LIBPCRE=YesPlease instructed
  the build procedure to use v1, but now it means v2.  USE_LIBPCRE1
  and USE_LIBPCRE2 can be used to explicitly choose which version to
  use, as before.
- The build procedure learned to optionally use symbolic links
  (instead of hardlinks and copies) to install "git-foo" for built-in
  commands, whose binaries are all identical.
- Conversion from uchar[20] to struct object_id continues.
- The way "git worktree prune" worked internally has been simplified,
  by assuming how "git worktree move" moves an existing worktree to a
  different place.
- Code clean-up for the "repository" abstraction.
- Code to find the length to uniquely abbreviate object names based
  on packfile content, which is a relatively recent addtion, has been
  optimized to use the same fan-out table.
- The mechanism to use parse-options API to automate the command line
  completion continues to get extended and polished.
- Copies of old scripted Porcelain commands in contrib/examples/ have
  been removed.
- Some tests that rely on the exact hardcoded values of object names
  have been updated in preparation for hash function migration.
- Perf-test update.
- Test helper update.
- The effort continues to refactor the internal global data structure
  to make it possible to open multiple repositories, work with and
  then close them,
- Small test-helper programs have been consolidated into a single
  binary.
- API clean-up around ref-filter code.
- Shell completion (in contrib) that gives list of paths have been
  optimized somewhat.
- The index file is updated to record the fsmonitor section after a
  full scan was made, to avoid wasting the effort that has already
  spent.
- Performance measuring framework in t/perf learned to help bisecting
  performance regressions.
- Some multi-word source filenames are being renamed to separate
  words with dashes instead of underscores.
- An reusable "memory pool" implementation has been extracted from
  fast-import.c, which in turn has become the first user of the
  mem-pool API.
- A build-time option has been added to allow Git to be told to refer
  to its associated files relative to the main binary, in the same
  way that has been possible on Windows for quite some time, for
  Linux, BSDs and Darwin.
- Precompute and store information necessary for ancestry traversal
  in a separate file to optimize graph walking.
- The effort to pass the repository in-core structure throughout the
  API continues.  This round deals with the code that implements the
  refs/replace/ mechanism.
- The build procedure "make DEVELOPER=YesPlease" learned to enable a
  bit more warning options depending on the compiler used to help
  developers more.  There also is "make DEVOPTS=tokens" knob
  available now, for those who want to help fixing warnings we
  usually ignore, for example.
- A new version of the transport protocol is being worked on.
- The code to interface to GPG has been restructured somewhat to make
  it cleaner to integrate with other types of signature systems later.
- The code has been taught to use the duplicated information stored
  in the commit-graph file to learn the tree object name for a commit
  to avoid opening and parsing the commit object when it makes sense
  to do so.
- "git gc" in a large repository takes a lot of time as it considers
  to repack all objects into one pack by default.  The command has
  been taught to pretend as if the largest existing packfile is
  marked with ".keep" so that it is left untouched while objects in
  other packs and loose ones are repacked.
- The transport protocol v2 is getting updated further.
- The codepath around object-info API has been taught to take the
  repository object (which in turn tells the API which object store
  the objects are to be located).
- "git pack-objects" needs to allocate tons of "struct object_entry"
  while doing its work, and shrinking its size helps the performance
  quite a bit.
- The implementation of "git rebase -i --root" has been updated to use
  the sequencer machinery more.
- Developer support update, by using BUG() macro instead of die() to
  mark codepaths that should not happen more clearly.
- Developer support.  Use newer GCC on one of the builds done at
  TravisCI.org to get more warnings and errors diagnosed.
- Conversion from uchar[20] to struct object_id continues.
- By code restructuring of submodule merge in merge-recursive,
  informational messages from the codepath are now given using the
  same mechanism as other output, and honor the merge.verbosity
  configuration.  The code also learned to give a few new messages
  when a submodule three-way merge resolves cleanly when one side
  records a descendant of the commit chosen by the other side.
- Avoid unchecked snprintf() to make future code auditing easier.
- Many tests hardcode the raw object names, which would change once
  we migrate away from SHA-1.  While some of them must test against
  exact object names, most of them do not have to use hardcoded
  constants in the test.  The latter kind of tests have been updated
  to test the moral equivalent of the original without hardcoding the
  actual object names.
- The list of commands with their various attributes were spread
  across a few places in the build procedure, but it now is getting a
  bit more consolidated to allow more automation.
- Quite a many tests assumed that newly created refs are made as
  loose refs using the files backend, which have been updated to use
  proper plumbing like rev-parse and update-ref, to avoid breakage
  once we start using different ref backends.
- "git shortlog cruft" aborted with a BUG message when run outside a
  Git repository.  The command has been taught to complain about
  extra and unwanted arguments on its command line instead in such a
  case.
- "git stash push -u -- <pathspec>" gave an unnecessary and confusing
  error message when there was no tracked files that match the
  <pathspec>, which has been fixed.
- "git tag --contains no-such-commit" gave a full list of options
  after giving an error message.
- "diff-highlight" filter (in contrib/) learned to understand "git log
  --graph" output better.
- when refs that do not point at committish are given, "git
  filter-branch" gave a misleading error messages.  This has been
  corrected.
- "git submodule status" misbehaved on a submodule that has been
  removed from the working tree.
- When credential helper exits very quickly without reading its
  input, it used to cause Git to die with SIGPIPE, which has been
  fixed.
- "git rebase --keep-empty" still removed an empty commit if the
  other side contained an empty commit (due to the "does an
  equivalent patch exist already?" check), which has been corrected.
- Some codepaths, including the refs API, get and keep relative
  paths, that go out of sync when the process does chdir(2).  The
  chdir-notify API is introduced to let these codepaths adjust these
  cached paths to the new current directory.
- "cd sub/dir && git commit ../path" ought to record the changes to
  the file "sub/path", but this regressed long time ago.
- Recent introduction of "--log-destination" option to "git daemon"
  did not work well when the daemon was run under "--inetd" mode.
- Small fix to the autoconf build procedure.
- Fix an unexploitable (because the oversized contents are not under
  attacker's control) buffer overflow.
- Recent simplification of build procedure forgot a bit of tweak to
  the build procedure of contrib/mw-to-git/
- Moving a submodule that itself has submodule in it with "git mv"
  forgot to make necessary adjustment to the nested sub-submodules;
  now the codepath learned to recurse into the submodules.
- "git config --unset a.b", when "a.b" is the last variable in an
  otherwise empty section "a", left an empty section "a" behind, and
  worse yet, a subsequent "git config a.c value" did not reuse that
  empty shell and instead created a new one.  These have been
  (partially) corrected.
- "git worktree remove" learned that "-f" is a shorthand for
  "--force" option, just like for "git worktree add".
- The completion script (in contrib/) learned to clear cached list of
  command line options upon dot-sourcing it again in a more efficient
  way.
- "git svn" had a minor thinko/typo which has been fixed.
- During a "rebase -i" session, the code could give older timestamp
  to commits created by later "pick" than an earlier "reword", which
  has been corrected.
- "git submodule status" did not check the symbolic revision name it
  computed for the submodule HEAD is not the NULL, and threw it at
  printf routines, which has been corrected.
- When fed input that already has In-Reply-To: and/or References:
  headers and told to add the same information, "git send-email"
  added these headers separately, instead of appending to an existing
  one, which is a violation of the RFC.  This has been corrected.
- "git fast-export" had a regression in v2.15.0 era where it skipped
  some merge commits in certain cases, which has been corrected.
- The code did not propagate the terminal width to subprocesses via
  COLUMNS environment variable, which it now does.  This caused
  trouble to "git column" helper subprocess when "git tag --column=row"
  tried to list the existing tags on a display with non-default width.
- We learned that our source files with ".pl" and ".py" extensions
  are Perl and Python files respectively and changes to them are
  better viewed as such with appropriate diff drivers.
- "git rebase -i" sometimes left intermediate "# This is a
  combination of N commits" message meant for the human consumption
  inside an editor in the final result in certain corner cases, which
  has been fixed.
- A test to see if the filesystem normalizes UTF-8 filename has been
  updated to check what we need to know in a more direct way, i.e. a
  path created in NFC form can be accessed with NFD form (or vice
  versa) to cope with APFS as well as HFS.
- "git format-patch --cover --attach" created a broken MIME multipart
  message for the cover letter, which has been fixed by keeping the
  cover letter as plain text file.
- The split-index feature had a long-standing and dormant bug in
  certain use of the in-core merge machinery, which has been fixed.
- Asciidoctor gives a reasonable imitation for AsciiDoc, but does not
  render illustration in a literal block correctly when indented with
  HT by default. The problem is fixed by forcing 8-space tabs.
- Code clean-up to adjust to a more recent lockfile API convention that
  allows lockfile instances kept on the stack.
- the_repository->index is not a allocated piece of memory but
  repo_clear() indiscriminately attempted to free(3) it, which has
  been corrected.
- Code clean-up to avoid non-standard-conformant pointer arithmetic.
- Code clean-up to turn history traversal more robust in a
  semi-corrupt repository.
- "git update-ref A B" is supposed to ensure that ref A does not yet
  exist when B is a NULL OID, but this check was not done correctly
  for pseudo-refs outside refs/ hierarchy, e.g. MERGE_HEAD.
- "git submodule update" and "git submodule add" supported the
  "--reference" option to borrow objects from a neighbouring local
  repository like "git clone" does, but lacked the more recent
  invention "--dissociate".  Also "git submodule add" has been taught
  to take the "--progress" option.
- Update credential-netrc helper (in contrib/) to allow customizing
  the GPG used to decrypt the encrypted .netrc file.
- "git submodule update" attempts two different kinds of "git fetch"
  against the upstream repository to grab a commit bound at the
  submodule's path, but it incorrectly gave up if the first kind
  (i.e. a normal fetch) failed, making the second "last resort" one
  (i.e. fetching an exact commit object by object name) ineffective.
  This has been corrected.
- Error behaviour of "git grep" when it cannot read the index was
  inconsistent with other commands that uses the index, which has
  been corrected to error out early.
- We used to call regfree() after regcomp() failed in some codepaths,
  which have been corrected.
- The import-tars script (in contrib/) has been taught to handle
  tarballs with overly long paths that use PAX extended headers.
- "git rev-parse Y..." etc. misbehaved when given endpoints were
  not committishes.
- "git pull --recurse-submodules --rebase", when the submodule
  repository's history did not have anything common between ours and
  the upstream's, failed to execute.  We need to fetch from them to
  continue even in such a case.
- "git remote update" can take both a single remote nickname and a
  nickname for remote groups, but only one of them was documented.
- "index-pack --strict" has been taught to make sure that it runs the
  final object integrity checks after making the freshly indexed
  packfile available to itself.
- Make zlib inflate codepath more robust against versions of zlib
  that clobber unused portion of outbuf.
- Fix old merge glitch in Documentation during v2.13-rc0 era.
- The code to read compressed bitmap was not careful to avoid reading
  past the end of the file, which has been corrected.
- "make NO_ICONV=NoThanks" did not override NEEDS_LIBICONV
  (i.e. linkage of -lintl, -liconv, etc. that are platform-specific
  tweaks), which has been corrected.

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
- Help contributors that visit us at GitHub.
- "git stash push <pathspec>" did not work from a subdirectory at all.
  Bugfix for a topic in v2.13
- As there is no portable way to pass timezone information to
  strftime, some output format from "git log" and friends are
  impossible to produce.  Teach our own strbuf_addftime to replace %%z
  and %%Z with caller-supplied values to help working around this.
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
