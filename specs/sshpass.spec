################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Non-interactive SSH authentication utility
Name:           sshpass
Version:        1.10
Release:        0%{?dist}
License:        GPLv2
Group:          Development/Tools
URL:            https://sshpass.sourceforge.net

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Tool for non-interactively performing password authentication with so called
"interactive keyboard password authentication" of SSH. Most users should use
more secure public key authentication of SSH instead.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS
%{_bindir}/%{name}
%{_datadir}/man/man1/%{name}.1*

################################################################################

%changelog
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.10-0
- Remove sig unsafe functions from signal handler.
- Allow -e to explicitly specify the environment variable to use
- Unset the variable specified with -e before calling subprogram
- Change the logic for setting a controlling TTY. Fixes compatibility
  issues with OpenSolaris and MSYS/Cygwin.

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 1.09-0
- Explicitly set the controlling TTY

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 1.08-0
- Report when IP key has changed
- Scrub the environment variable for -e

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 1.07-0
- Pass signals that should terminate to ssh
- Fix race around signal handling
- Report IPC errors to stderr
- Report if can't open -f password file

* Tue Oct 04 2016 Anton Novojilov <andy@essentialkaos.com> - 1.06-0
- Initial build for kaos repo
