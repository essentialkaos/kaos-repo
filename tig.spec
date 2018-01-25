################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

%define bashcompl         %{_sysconfdir}/bash_completion.d

################################################################################

Summary:            Tig is an ncurses-based text-mode interface for git
Name:               tig
Version:            2.2
Release:            0%{?dist}
License:            GPL
Group:              Development/Tools
URL:                http://jonas.nitro.dk/tig/
Vendor:             Jonas Fonseca <fonseca@diku.dk>

Source0:            http://jonas.nitro.dk/tig/releases/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           git ncurses glibc

BuildRequires:      make autoconf asciidoc xmlto ncurses-devel

Provides:           %{name} = %{version}-%{release}

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
%setup -q

%build
%{configure}

CFLAGS="$RPM_OPT_FLAGS -DVERSION=%{name}-%{version}-%{release}"

%{__make} prefix=%{_prefix} %{?_smp_mflags} all doc-man doc-html

%install
%{__rm} -rf %{buildroot}

CFLAGS="$RPM_OPT_FLAGS -DVERSION=%{name}-%{version}-%{release}"

%{make_install} install-doc-man prefix=%{_prefix} \
                                bindir=%{_bindir} \
                                mandir=%{_mandir}

install -dm 755 %{buildroot}%{bashcompl}
install -pm 644 contrib/tig-completion.bash %{buildroot}%{bashcompl}/%{name}

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.adoc COPYING INSTALL.adoc NEWS.adoc
%doc doc/*.html
%{_bindir}/*
%{_sysconfdir}/tigrc
%{bashcompl}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*

################################################################################

%changelog
* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.2-0
- Updated to latest stable release

* Wed Sep  9 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-1
- Improved spec file

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1.1-0
- Updated to latest stable release

* Thu Mar 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.1-0
- Updated to latest stable release

* Sat Oct 18 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.3-0
- Updated to latest stable release

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Updated to latest stable release

* Thu Dec 19 2013 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- Initial build
