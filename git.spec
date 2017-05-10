###############################################################################

Summary:          Core git tools
Name:             git
Version:          2.12.2
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

###############################################################################

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

###############################################################################

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

###############################################################################

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools

Requires:       git = %{version}-%{release} subversion

%description svn
Git tools for importing Subversion repositories.

###############################################################################

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} cvs cvsps

%description cvs
Git tools for importing CVS repositories.

###############################################################################

%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tla

%description arch
Git tools for importing Arch repositories.

###############################################################################

%package email
Summary:        Git tools for sending email
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release}

%description email
Git tools for sending email.

###############################################################################

%package gui
Summary:        Git GUI tool
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tk >= 8.4

%description gui
Git GUI tool

###############################################################################

%package -n gitk
Summary:        Git revision tree visualiser ('gitk')
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release} tk >= 8.4

%description -n gitk
Git revision tree visualiser ('gitk')

###############################################################################

%package -n gitweb
Summary:        Git web interface
Group:          Development/Tools

BuildArch:      noarch

Requires:       git = %{version}-%{release}

%description -n gitweb
Browsing git repository on the web

###############################################################################

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

###############################################################################

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%prep
%setup -q

%build
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     %{path_settings} \
     all

%install
rm -rf %{buildroot}

make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=%{buildroot} \
     %{path_settings} \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}

test ! -d %{buildroot}%{python_sitelib} || rm -fr %{buildroot}%{python_sitelib}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}%{_libexecdir}/git-core -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@) >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) >> perl-files
(find %{buildroot}%{_mandir} %{buildroot}/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files

rm -rf %{buildroot}%{_datadir}/locale

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d

install -m 644 -T contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

%clean
rm -rf %{buildroot}

###############################################################################

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

%files -n perl-Git -f perl-files
%defattr(-,root,root)

%files all
# No files for you!

###############################################################################

%changelog
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
