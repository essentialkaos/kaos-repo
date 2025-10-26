################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define bashcompl  %{_sysconfdir}/bash_completion.d

################################################################################

Summary:        Tig is an ncurses-based text-mode interface for git
Name:           tig
Version:        2.6.0
Release:        0%{?dist}
License:        GPL
Group:          Development/Tools
URL:            https://github.com/jonas/tig

Source0:        https://github.com/jonas/tig/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc autoconf asciidoc xmlto ncurses-devel

Requires:       git ncurses glibc

Provides:       %{name} = %{version}-%{release}

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

################################################################################

%files
%defattr(-,root,root,-)
%doc README.adoc COPYING INSTALL.adoc NEWS.adoc
%doc doc/*.html
%{_bindir}/%{name}
%{_sysconfdir}/tigrc
%{bashcompl}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*

################################################################################

%changelog
* Mon Oct 20 2025 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- https://github.com/jonas/tig/releases/tag/tig-2.6.0

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 2.5.12-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.12

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 2.5.11-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.11

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 2.5.10-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.10

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 2.5.9-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.9

* Tue Apr 25 2023 Anton Novojilov <andy@essentialkaos.com> - 2.5.8-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.8

* Fri Dec 02 2022 Anton Novojilov <andy@essentialkaos.com> - 2.5.7-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.7

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- https://github.com/jonas/tig/releases/tag/tig-2.5.0

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.1-0
- https://github.com/jonas/tig/releases/tag/tig-2.4.1

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- https://github.com/jonas/tig/releases/tag/tig-2.4.0

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.3-0
- https://github.com/jonas/tig/releases/tag/tig-2.3.3

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.2-0
- https://github.com/jonas/tig/releases/tag/tig-2.3.2

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.1-0
- https://github.com/jonas/tig/releases/tag/tig-2.3.1

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- https://github.com/jonas/tig/releases/tag/tig-2.3.0

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.2-0
- https://github.com/jonas/tig/releases/tag/tig-2.2.2

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.1-0
- https://github.com/jonas/tig/releases/tag/tig-2.2.1

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- https://github.com/jonas/tig/releases/tag/tig-2.2

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- https://github.com/jonas/tig/releases/tag/tig-2.1.1

* Thu Mar 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- https://github.com/jonas/tig/releases/tag/tig-2.1

* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- https://github.com/jonas/tig/releases/tag/tig-2.0.3

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- https://github.com/jonas/tig/releases/tag/tig-2.0.2

* Thu Dec 19 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- Initial build
