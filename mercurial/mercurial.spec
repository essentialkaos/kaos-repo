###############################################################################

%define shortname      hg
%define emacs_version  22.1

###############################################################################

%define _emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile

###############################################################################

Summary:           Distributed source control management tool
Name:              mercurial
Version:           3.5
Release:           0%{?dist}
License:           GPLv2+
Group:             Development/Tools
URL:               https://mercurial.selenic.com/

Source0:           http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
Source1:           %{name}-site-start.el
Source2:           hgk.rc
Source3:           certs.rc

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     python python-devel python-docutils
BuildRequires:     emacs-nox emacs-el pkgconfig gettext

Requires:          python

Provides:          %{shortname} = %{version}-%{release}
Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
Mercurial is a free, distributed source control management tool. It 
efficiently handles projects of any size and offers an easy and intuitive 
interface.

###############################################################################

%package -n emacs-mercurial
Summary:           Mercurial version control system support for Emacs
Group:             Applications/Editors
Requires:          %{shortname} = %{version}-%{release} emacs-common
Requires:          emacs(bin) >= %{emacs_version}
Obsoletes:         mercurial-emacs = %{version}

BuildArch:         noarch

%description -n emacs-mercurial
Contains byte compiled elisp packages for mercurial.
To get started: start emacs, load hg-mode with M-x hg-mode, and show 
help with C-c h h

###############################################################################

%package -n emacs-mercurial-el
Summary:           Elisp source files for mercurial under GNU Emacs
Group:             Applications/Editors
Requires:          emacs-mercurial = %{version}-%{release}

%description -n emacs-mercurial-el
This package contains the elisp source files for mercurial under GNU Emacs.

###############################################################################

%package hgk
Summary:           Hgk interface for mercurial
Group:             Development/Tools
Requires:          %{shortname} = %{version}-%{release} tk

%description hgk
A Mercurial extension for displaying the change history graphically using 
Tcl/Tk. Displays branches and merges in an easily understandable way and 
shows diffs for each revision. Based on gitk for the git SCM.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
make %{?_smp_mflags} all

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --root %{buildroot} --prefix %{_prefix} --record=%{name}.files

make install-doc DESTDIR=%{buildroot} MANDIR=%{_mandir}

install -dm 755 %{buildroot}%{_libexecdir}/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -dm 755 %{buildroot}%{_datadir}/zsh/site-functions
install -dm 755 %{buildroot}%{_datadir}/emacs/site-lisp
install -dm 755 %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}/hgrc.d

grep -v -e 'hgk.py*' -e %{python_sitearch}/%{name}/ -e %{python_sitearch}/hgext/ < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

pushd contrib
for file in %{name}.el mq.el ; do
  %{_emacs_bytecompile} $file
  install -pm 644 $file ${file}c %{buildroot}%{_datadir}/emacs/site-lisp
  rm -f ${file}c
done
popd

install -Dm 755 contrib/hgk %{buildroot}%{_libexecdir}/%{name}/hgk
install -pm 755 contrib/%{shortname}-ssh %{buildroot}%{_bindir}/

install -m 644 contrib/bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}.sh
install -m 644 contrib/zsh_completion %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d/

install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/hgrc.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/hgrc.d

mv %{buildroot}%{python_sitearch}/%{name}/locale %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{python_sitearch}/%{name}/locale

%find_lang %{shortname}

grep -v locale %{name}-base.files > %{name}-base-filtered.files

%clean
rm -rf %{buildroot}

###############################################################################

%files -f %{name}-base-filtered.files -f %{shortname}.lang
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/%{shortname}*.txt doc/%{shortname}*.html *.cgi contrib/*.fcgi contrib/*.wsgi
%doc %attr(644,root,root) %{_mandir}/man?/%{shortname}*.gz
%doc %attr(644,root,root) contrib/*.svg
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}.sh
%{_bindir}/%{shortname}-ssh
%dir %{_sysconfdir}/bash_completion.d/
%dir %{_datadir}/zsh/
%{_datadir}/zsh/site-functions/
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/hgrc.d
%{python_sitearch}/%{name}
%{python_sitearch}/hgext
%config(noreplace) %{_sysconfdir}/%{name}/hgrc.d/certs.rc

%files -n emacs-mercurial
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/*.elc
%{_datadir}/emacs/site-lisp/site-start.d/*.el

%files -n emacs-mercurial-el
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/*.el

%files hgk -f %{name}-hgk.files
%defattr(-,root,root,-)
%{_libexecdir}/%{name}/
%{_sysconfdir}/%{name}/hgrc.d/hgk.rc

###############################################################################

%changelog
* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 3.5-0
- Updated to latest stable release

* Tue May 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.4-0
- Updated to latest stable release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 3.3.3-0
- Updated to latest stable release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.3.2-0
- Updated to latest stable release

* Sat Jan 17 2015 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- Updated to latest stable release

* Sat Dec 20 2014 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- Updated to latest stable release

* Wed Dec 10 2014 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Initial build
