################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

# Disable strip on EL9+
%if 0%{?rhel} >= 9
%define __os_install_post %{nil}
%endif

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}

################################################################################

Summary:        Core git tools
Name:           git
Version:        2.43.0
Release:        0%{?dist}
License:        GPL
Group:          Development/Tools
URL:            https://git-scm.com

Source0:        https://github.com/git/git/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make gettext xmlto asciidoc > 6.0.3
BuildRequires:  libcurl-devel expat-devel openssl-devel zlib-devel

Requires:       perl-Git = %{version}-%{release}
Requires:       zlib rsync less openssh-clients expat expat-devel

Provides:       git-core = %{version}-%{release}

Obsoletes:      git-core <= 1.5.4.2
Obsoletes:      git-p4 <= 1.5.4.2

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
Summary:    Meta-package to pull in all git tools
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release}
Requires:   git-svn = %{version}-%{release}
Requires:   git-cvs = %{version}-%{release}
Requires:   git-email = %{version}-%{release}
Requires:   gitk = %{version}-%{release}
Requires:   gitweb = %{version}-%{release}
Requires:   git-gui = %{version}-%{release}
Obsoletes:  git <= 1.5.4.2

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

################################################################################

%package svn
Summary:   Git tools for importing Subversion repositories
Group:     Development/Tools

Requires:  git = %{version}-%{release} subversion

%description svn
Git tools for importing Subversion repositories.

################################################################################

%package cvs
Summary:    Git tools for importing CVS repositories
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release} cvs

%description cvs
Git tools for importing CVS repositories.

################################################################################

%package email
Summary:    Git tools for sending email
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release}

%description email
Git tools for sending email.

################################################################################

%package gui
Summary:    Git GUI tool
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release} tk >= 8.4

%description gui
Git GUI tool

################################################################################

%package -n gitk
Summary:    Git revision tree visualiser ('gitk')
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release} tk >= 8.4

%description -n gitk
Git revision tree visualiser ('gitk')

################################################################################

%package -n gitweb
Summary:    Git web interface
Group:      Development/Tools

BuildArch:  noarch

Requires:   git = %{version}-%{release}

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
%if 0%{?rhel} <= 7
  export CFLAGS="%{optflags} -std=gnu99"
%else
  export CFLAGS="%{optflags}"
%endif

%{__make} %{?_smp_mflags} CFLAGS="$CFLAGS" \
     %{path_settings} \
     all

%install
rm -rf %{buildroot}

%if 0%{?rhel} <= 7
  export CFLAGS="%{optflags} -std=gnu99"
%else
  export CFLAGS="%{optflags}"
%endif

%{__make} %{?_smp_mflags} CFLAGS="$CFLAGS" DESTDIR=%{buildroot} \
     %{path_settings} \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

rm -f %{buildroot}%{_libexecdir}/git-core/git-archimport
rm -f %{buildroot}%{_libexecdir}/git-core/git-p4
rm -f %{buildroot}%{_mandir}/man1/git-archimport.*

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
%doc COPYING Documentation/*.txt
%doc Documentation/howto
%doc Documentation/technical
%{_datadir}/git-core/
%{_sysconfdir}/bash_completion.d

%files svn
%defattr(-,root,root)
%doc Documentation/*svn*.txt
%{_libexecdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*

%files cvs
%defattr(-,root,root)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*

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
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.43.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.43.0.txt

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.42.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.42.1.txt

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.42.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.42.0.txt

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.41.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.41.0.txt

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.40.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.40.1.txt

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 2.39.3-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.3.txt

* Wed Feb 15 2023 Anton Novojilov <andy@essentialkaos.com> - 2.39.2-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.2.txt

* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.39.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.1.txt

* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.39.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.0.txt

* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.38.3-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.38.3.txt

* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.38.2-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.38.2.txt

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 2.38.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.38.1.txt

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 2.37.4-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.37.4.txt

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 2.36.3-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.36.3.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.35.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.35.1.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.35.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.35.0.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.34.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.34.1.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.34.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.34.0.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.33.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.33.1.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.33.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.33.0.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.32.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.32.0.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.31.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.31.1.txt

* Thu Apr 07 2022 Anton Novojilov <andy@essentialkaos.com> - 2.31.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.31.0.txt

* Wed Mar 10 2021 Anton Novojilov <andy@essentialkaos.com> - 2.30.2-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.30.2.txt

* Wed Mar 10 2021 Anton Novojilov <andy@essentialkaos.com> - 2.30.1-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.30.1.txt

* Wed Mar 10 2021 Anton Novojilov <andy@essentialkaos.com> - 2.30.0-0
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.30.0.txt
