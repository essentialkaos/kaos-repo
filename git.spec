###############################################################################

Summary:          Core git tools
Name:             git
Version:          2.6.3
Release:          0%{?dist}
License:          GPL
Group:            Development/Tools
URL:              http://kernel.org/pub/software/scm/git/

Source:           http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    zlib-devel >= 1.2 openssl-devel libcurl-devel expat-devel gettext xmlto asciidoc > 6.0.3 lynx

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
%doc README COPYING Documentation/*.txt
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
* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.3-0
- Updated to latest release

* Thu Oct 08 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.1-0
- Updated to latest release

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- Updated to latest release

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.1-0
- Updated to latest release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Updated to latest release

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 2.4.5-0
- Updated to latest release

* Tue May 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Updated to latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 2.3.5-0
- Updated to latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- Updated to latest release

* Fri Feb 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-0
- Updated to latest release

* Fri Dec 19 2014 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- Updated to latest release

* Mon Dec 01 2014 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest release

* Sat Nov 08 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
- Updated to latest release

* Mon Sep 29 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Updated to latest release

* Wed Aug 20 2014 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- Updated to latest release

* Tue Jul 01 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- Updated to latest release

* Thu Jun 05 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Updated to latest release

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- Updated to latest release

* Wed Mar 19 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- Updated to latest release

* Fri Mar 07 2014 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- Updated to latest release

* Tue Feb 04 2014 Anton Novojilov <andy@essentialkaos.com> - 1.8.5.3-0
- Updated to latest release

* Fri Dec 20 2013 Anton Novojilov <andy@essentialkaos.com> - 1.8.5.2-0
- Updated to latest release

* Wed Nov 20 2013 Anton Novojilov <andy@essentialkaos.com> - 1.8.4-3
- Updated to latest release

* Tue Aug 13 2013 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-4
- Rewrited and improved spec
