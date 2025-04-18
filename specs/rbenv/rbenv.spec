################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define profile_dir  %{_sysconfdir}/profile.d
%define profile      %{profile_dir}/%{name}.sh

################################################################################

Summary:        Version manager tool for the Ruby programming language
Name:           rbenv
Version:        1.3.2
Release:        0%{?dist}
License:        MIT
Group:          Development/Tools
URL:            https://github.com/rbenv/rbenv

Source0:        https://github.com/rbenv/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.profile

Source100:      checksum.sha512

Patch0:         %{name}-default-root.patch
Patch1:         %{name}-hit-prefix-arrow.patch

BuildRequires:  make gcc

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
rbenv is a version manager tool for the Ruby programming language on Unix-like
systems. It is useful for switching between multiple Ruby versions on the same
machine and for ensuring that each project you are working on always runs on the
correct Ruby version.

################################################################################

%prep
%crc_check
%autosetup -p1 -n %{name}-%{version}

%build
pushd src
%configure
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_prefix}/local/%{name}
install -dm 0755 %{buildroot}%{profile_dir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 0755 %{buildroot}%{_prefix}/local/%{name}/versions
install -dm 0755 %{buildroot}%{_prefix}/local/%{name}/shims

cp -r bin libexec completions LICENSE %{buildroot}%{_prefix}/local/%{name}/

install -pm 755 %{SOURCE1} %{buildroot}%{profile}

ln -sf %{_prefix}/local/%{name}/libexec/rbenv %{buildroot}%{_bindir}/%{name}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{profile}
%{_prefix}/local/%{name}
%{_bindir}/%{name}

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- https://github.com/rbenv/rbenv/releases/tag/v1.3.2

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- https://github.com/rbenv/rbenv/releases/tag/v1.3.1

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- https://github.com/rbenv/rbenv/releases/tag/v1.3.0

* Fri Aug 19 2022 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- https://github.com/rbenv/rbenv/releases/tag/v1.2.0

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.1.2-0
- https://github.com/rbenv/rbenv/releases/tag/v1.1.2

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
- Fixed an instance of local variable leakage in the rbenv shell function
  wrapper.
- Changed rbenv shell to ensure it exits with a non-zero status on failure.
- Added rbenv --version for printing the current version of rbenv.
- Added /usr/lib/rbenv/hooks to the plugin hook search path.
- Fixed rbenv which to account for path entries with spaces.
- Changed rbenv init to accept option arguments in any order.
