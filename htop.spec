################################################################################

Summary:              Interactive process viewer
Name:                 htop
Version:              2.0.2
Release:              0%{?dist}
License:              GPL
Group:                Applications/System
URL:                  http://hisham.hm/htop

Source:               http://hisham.hm/htop/releases/%{version}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:        gcc >= 3.0 ncurses-devel

################################################################################

%description
htop is an interactive process viewer for Linux.

################################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{make_install}

%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%doc %{_mandir}/man1/htop.1*
%{_bindir}/htop
%{_datadir}/applications/htop.desktop
%{_datadir}/pixmaps/htop.png

################################################################################

%changelog
* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Mac OS X: stop trying when task_for_pid fails for a process, stops spamming
  logs with errors
- Add Ctrl+A and Ctrl+E to go to beginning and end of line
- FreeBSD: fixes for CPU calculation
- Usability: auto-follow process after a search
- Use Linux backend on GNU Hurd
- Improvement for reproducible builds
- BUGFIX: Fix behavior of Alt-key combinations
- Various code tweaks and cleanups

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- OpenBSD: Various fixes and improvements
- FreeBSD: fix CPU and memory readings
- FreeBSD: add battery support
- Linux: Retain last-obtained name of a zombie process
- Mac OS X: Improve portability for OS X versions
- Mac OS X: Fix reading command-line arguments and basename
- Mac OS X: Fix process state information
- Mac OS X: Fix tree view collapsing/expanding
- Mac OS X: Fix tree organization
- Mac OS X: Fix memory accounting
- Fix crash when emptying a column of meters
- Make Esc key more responsive

* Thu Feb 11 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.0-0
- Platform abstraction layer
- Initial FreeBSD support
- Initial Mac OS X support
- Swap meter for Mac OSX
- OpenBSD port
- FreeBSD support improvements
- Support for NCurses 6 ABI, including mouse wheel support
- Much improved mouse responsiveness
- Process environment variables screen
- Higher-resolution UTF-8 based Graph mode
- Show program path settings
- BUGFIX: Fix crash when scrolling an empty filtered list.
- Use dynamic units for text display, and several fixes
- BUGFIX: fix error caused by overflow in usertime calculation
- Catch all memory allocation errors
- Several tweaks and bugfixes

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.0.3-0
- Updated to version 1.0.3

* Fri Feb  1 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Updated to version 1.0.2

* Sat Apr 21 2012 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-3
- Updated to release 1.0.1 and rewrited spec by David Hrbáč
