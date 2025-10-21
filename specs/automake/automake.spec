################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Automake::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Automake::

################################################################################

%define major_version  1.18

################################################################################

Summary:        A GNU tool for automatically creating Makefiles
Name:           automake
Version:        %{major_version}.1
Release:        0%{?dist}
License:        GPLv2+ and GFDL and Public Domain and MIT
Group:          Development/Tools
URL:            https://www.gnu.org/software/automake/

Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source2:        https://git.savannah.gnu.org/cgit/config.git/plain/config.sub
Source3:        https://git.savannah.gnu.org/cgit/config.git/plain/config.guess

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       perl(Thread::Queue)
Requires:       perl(threads)

BuildRequires:  autoconf >= 2.65 make coreutils findutils
BuildRequires:  perl-generators perl-interpreter perl(Thread::Queue)
BuildRequires:  perl(threads)

BuildArch:      noarch

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Automake is a tool for automatically generating Makefile.in files compliant with
the GNU Coding Standards.

You should install Automake if you are developing software and would like to use
its ability to automatically generate GNU standard Makefiles.

################################################################################

%prep
%{crc_check}

%setup -q

for file in %{SOURCE2} %{SOURCE3} ; do
  for dest in $(find -name "$(basename "$file")"); do
    cp "$file" "$dest"
  done
done

%build
%configure
%{__make} %{?_smp_mflags}

cp m4/acdir/README README.aclocal
cp contrib/multilib/README README.multilib

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING*
%doc AUTHORS README THANKS NEWS README.aclocal README.multilib
%doc %{_defaultdocdir}/%{name}/amhello-1.0.tar.gz
%exclude %{_datadir}/aclocal
%{_bindir}/automake
%{_bindir}/automake-%{major_version}
%{_bindir}/aclocal
%{_bindir}/aclocal-%{major_version}
%{_infodir}/*.info*
%{_datadir}/automake-%{major_version}
%{_datadir}/aclocal-%{major_version}
%{_mandir}/man1/*

################################################################################

%changelog
* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18.1-0
- Undo change to mdate-sh; once again, it does not look at
  SOURCE_DATE_EPOCH. This change was a misunderstanding that causes
  problems, not fixes, for reproducible builds.
- Improve debuggability of installcheck failures.

* Tue Oct 21 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18-0
- Default tar format is now ustar, mainly to support longer filenames;
  the tar-v7 and other explicit options to force a particular tar
  format are unchanged and still override the default.
- The mdate-sh auxiliary script generally used with Texinfo now uses
  SOURCE_DATE_EPOCH, if set, instead of the source file's mtime.
- New option dist-bzip3 for bzip3 compression of distributions.
- New option --stderr-prefix for tap-driver.sh, to prefix each line of
  stderr from a test script with a given string.
- Support for Algol 68 added, based on the GNU Algol 68 compiler.
- Do not make Perl warnings fatal, per Perl's recommendation.
- Avoid Perl 5.41.8+ precedence warning for use of !!.
- a Perl path containing whitespace now emits a warning instead of
  an error, so ./configure PERL='/usr/bin/env perl' can work.
- The py-compile script once again does nothing (successfully) if the
  PYTHON environment variable is set to ":", or anything that isn't a
  Python interpreter (according to $PYTHON -V). Exception: if PYTHON
  is set to "false", do nothing but exit unsuccessfully, also to match
  previous behavior.
- The no-dist-built-sources Automake option now operates (hopefully) as
  intended, i.e., omits the dependency on $(BUILT_SOURCES) for the
  distdir target.
- Only warn about install.sh being found, instead of it being a fatal
  error.
- The compile script is more robust to Windows configurations;
  specifically, avoids double-path translation on MSYS.
- The test infrastructure sets the CONFIG_SITE environment variable to
  /dev/null, to avoid the local system's Autoconf site defaults from
  breaking the test environment.
- AM_SILENT_RULES once again always ends with a newline.
- AM_SANITY_CHECK now outputs "no" on failure, so that a complete line
  is written to stdout before the error message is written to stderr.
- Only require the presence of an ABOUT-NLS file at the 'gnits'
  strictness level.

* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 1.17-0
- Update to the latest stable version

* Fri Sep 30 2022 Anton Novojilov <andy@essentialkaos.com> - 1.16.5-0
- PYTHON_PREFIX and PYTHON_EXEC_PREFIX are now set according to
  Python's sys.* values only if the new configure option
  --with-python-sys-prefix is specified. Otherwise, GNU default values
  are used, as in the past. (The change in 1.16.3 was too incompatible.)
- consistently depend on install-libLTLIBRARIES.
- use const for yyerror declaration in bison/yacc tests.

* Sat May 23 2020 Anton Novojilov <andy@essentialkaos.com> - 1.16.2-0
- Initial build for kaos repository
