###############################################################################

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

###############################################################################

%define install_dir       %{_loc_prefix}/%{name}
%define profile_dir       %{_sysconfdir}/profile.d
%define profile           %{profile_dir}/%{name}.sh

###############################################################################

Summary:         Simple Ruby version management utility
Name:            rbenv
Version:         1.0.0
Release:         0%{?dist}
License:         MIT
Group:           Development/Tools
URL:             https://github.com/sstephenson/rbenv

Source0:         https://github.com/rbenv/%{name}/archive/v%{version}.tar.gz
Source1:         %{name}.profile

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:       noarch

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
rbenv lets you easily switch between multiple versions 
of Ruby. Its simple, unobtrusive, and follows the UNIX 
tradition of single-purpose tools that do one thing well.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}

install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}
install -dm 0755 %{buildroot}%{profile_dir}
install -dm 0755 %{buildroot}%{_bindir}

cp -r bin libexec completions LICENSE %{buildroot}%{_loc_prefix}/%{name}/

install -pm 644 %{SOURCE1} %{buildroot}%{profile}

ln -sf %{_loc_prefix}/%{name}/libexec/rbenv %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{install_dir}
%{profile}
%{_bindir}/%{name}

###############################################################################

%changelog
* Thu May 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to latest stable release

* Wed Sep 17 2014 Anton Novojilov <andy@essentialkaos.com> - 0.4.1-0
- Small fixes in spec

* Wed Jul 02 2014 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-3
- Updated source to latest version

* Wed Jul 02 2014 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-2
- Improved install system

* Tue Aug 13 2013 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-1
- Fixed bug with profile export

* Mon May 13 2013 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-0
- rbenv now prefers .ruby-version files to .rbenv-version files for specifying 
  local application-specific versions. The .ruby-version file has the same 
  format as .rbenv-version but is compatible with other Ruby version managers.
- Deprecated ruby-local-exec and moved its functionality into the standard 
  ruby shim. See the ruby-local-exec wiki page for upgrade instructions.
- Modified shims to include the full path to rbenv so that they can be invoked 
  without having rbenvs bin directory in the $PATH.
- Sped up rbenv init by avoiding rbenv reinitialization and by using a simpler 
  indexing approach. (Users of chef-rbenv should upgrade to the latest version 
  to fix a compatibility issue.)
- Reworked rbenv help so that usage and documentation is stored as a comment 
  in each subcommand, enabling plugin commands to hook into the help system.
- Added support for full completion of the command line, not just the first 
  argument.
- Updated installation instructions for Zsh and Ubuntu users.
- Fixed rbenv which and rbenv prefix with system Ruby versions.
- Changed rbenv exec to avoid prepending the system Ruby location to $PATH to 
  fix issues running system Ruby commands that invoke other commands.
- Changed rbenv rehash to ensure it exits with a 0 status code under normal 
  operation, and to ensure outdated shims are removed first when rehashing.
- Modified rbenv rehash to run hash -r afterwards, when shell integration is 
  enabled, to ensure the shells command cache is cleared.
- Removed use of the += operator to support older versions of Bash.
- Adjusted non-bare rbenv versions output to include system, if present.
- Improved documentation for installing and uninstalling Ruby versions.
- Fixed rbenv versions not to display a warning if the currently specified 
  version doesnt exist.
- Fixed an instance of local variable leakage in the rbenv shell function wrapper.
- Changed rbenv shell to ensure it exits with a non-zero status on failure.
- Added rbenv --version for printing the current version of rbenv.
- Added /usr/lib/rbenv/hooks to the plugin hook search path.
- Fixed rbenv which to account for path entries with spaces.
- Changed rbenv init to accept option arguments in any order.

* Mon Feb 6 2011 Anton Novojilov <andy@essentialkaos.com> - 0.3.0-0
- Added an rbenv root command which prints the value of $RBENV_ROOT, or 
the default root directory if its unset.
- Clarified Zsh installation instructions in the readme.
- Removed some redundant code in rbenv rehash.
- Fixed an issue with calling readlink for paths with spaces.
- Changed Zsh initialization code to install completion hooks only 
for interactive shells.
- Added preliminary support for ksh.
- rbenv rehash creates or removes shims only when necessary instead of 
removing and re-creating all shims on each invocation.
- Fixed that RBENV_DIR, when specified, would be incorrectly expanded 
to its parent directory.
- Removed the deprecated set-default and set-local commands.
- Added a --no-rehash option to rbenv init for skipping the automatic 
rehash when opening a new shell.


