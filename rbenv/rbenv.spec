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

%define profile_dir       %{_sysconfdir}/profile.d
%define profile           %{profile_dir}/%{name}.sh

###############################################################################

Summary:         Simple Ruby version management utility
Name:            rbenv
Version:         1.1.1
Release:         1%{?dist}
License:         MIT
Group:           Development/Tools
URL:             https://github.com/sstephenson/rbenv

Source0:         https://github.com/rbenv/%{name}/archive/v%{version}.tar.gz
Source1:         %{name}.profile

Patch0:          %{name}-init-fix.patch
Patch1:          %{name}-default-root.patch
Patch2:          %{name}-configure-sed.patch

BuildRequires:   make gcc

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
rbenv lets you easily switch between multiple versions 
of Ruby. Its simple, unobtrusive, and follows the UNIX 
tradition of single-purpose tools that do one thing well.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

pushd src
%configure
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}
install -dm 0755 %{buildroot}%{profile_dir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}/versions
install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}/shims

cp -r bin libexec completions LICENSE %{buildroot}%{_loc_prefix}/%{name}/

install -pm 755 %{SOURCE1} %{buildroot}%{profile}

ln -sf %{_loc_prefix}/%{name}/libexec/rbenv %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_loc_prefix}/%{name}
%{profile}
%{_bindir}/%{name}

###############################################################################

%changelog
* Mon Aug 07 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-1
- Improvements

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Fix setting environment variable in fish shell
- Rename OLD_RBENV_VERSION to RBENV_* convention

* Thu Apr 20 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-1
- Added patch with rbenv-init fix

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Remove deprecated ruby-local-exec executable
- Remove support for .rbenv-version legacy version file
- Remove support for default, global legacy global version files
- Add support for rbenv shell - style of invocation that restores previous
  version
- Adopt Contributor Covenant 1.4
- Replace . with source for fish shell
- Unset CDPATH if it's set by the user
- Fix rbenv <cmd> --help for sh-* commands
- Expand literal tilde in PATH

* Tue May 24 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-1
- Improved spec

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
