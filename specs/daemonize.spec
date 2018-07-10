################################################################################

Summary:         Run a command as a Unix daemon
Name:            daemonize
Version:         1.7.8
Release:         0%{?dist}
Group:           Applications/System
License:         BSD
URL:             http://software.clapper.org/daemonize

Source0:         https://github.com/bmc/%{name}/archive/release-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc

################################################################################

%description
daemonize runs a command as a Unix daemon. As defined in W. Richard Stevens'
1990 book, Unix Network Programming (Addison-Wesley, 1990), a daemon is "a
process that executes 'in the background' (i.e., without an associated
terminal or login shell) either waiting for some event to occur, or waiting
to perform some specified task on a periodic basis." Upon startup, a typical
daemon program will:

- Close all open file descriptors (especially standard input, standard output
  and standard error)
- Change its working directory to the root filesystem, to ensure that it
  doesn’t tie up another filesystem and prevent it from being unmounted
- Reset its umask value
- Run in the background (i.e., fork)
- Disassociate from its process group (usually a shell), to insulate itself
  from signals (such as HUP) sent to the process group
- Ignore all terminal I/O signals
- Disassociate from the control terminal (and take steps not to reacquire one)
- Handle any SIGCLD signals

Most programs that are designed to be run as daemons do that work for
themselves. However, you’ll occasionally run across one that does not.
When you must run a daemon program that does not properly make itself into a
true Unix daemon, you can use daemonize to force it to run as a true daemon.

################################################################################

%prep
%setup -qn %{name}-release-%{version}

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install} INSTALL="install -p" install

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md LICENSE.md README.md
%{_sbindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

################################################################################

%changelog
* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.8-0
- Fixed various compiler and cross-linking issues

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 1.7.7-0
- CFLAGS and LDFLAGS not passed through from configure to Makefile

* Tue May 12 2015 Anton Novojilov <andy@essentialkaos.com> - 1.7.6-0
- Fixed potential memory allocation issues

* Wed Aug 20 2014 Anton Novojilov <andy@essentialkaos.com> - 1.7.5-0
- Added support for out-of-tree builds

* Tue Feb 04 2014 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- Merged acconfig.h patch that cleans up getopt references
- Moved version stamp into a header
