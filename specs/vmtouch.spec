################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Portable file system cache diagnostics and control
Name:           vmtouch
Version:        1.3.1
Release:        0%{?dist}
License:        BSD 3-Clause
Group:          Development/Tools
URL:            https://github.com/hoytech/vmtouch

Source0:        https://github.com/hoytech/%{name}/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc

Provides:       %{name} = %{version}-%{release}

################################################################################

%description

vmtouch is a tool for learning about and controlling the file system cache
of unix and unix-like systems. It is BSD licensed so you can basically
do whatever you want with it.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} \
        PREFIX="%{buildroot}" \
        BINDIR="%{_sbindir}" \
        MANDIR="%{_mandir}/man8"

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc CHANGES README.md TODO
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*

################################################################################

%changelog
* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.3.1-0
- New switch: "-P <pidfile>". When combined with -l or -L, the
  PID of the daemon process will be written to this file.
- In Makefile, support staged installs using DESTDIR
- Create snapcraft.yaml to enable snap creation
- Fix compilation for pre-C99 compilers
- Documentation improvements

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- New switch: "-b <file>". This enables "batch mode" where the
  list of files to crawl is read from the specified file
- New switch: "-0". When this is enabled, the files in
  "batch mode" are separated by NUL bytes instead of newlines
- New switch: "-F". Prevents vmtouch from traversing separate
  filesystems
- Lots of updates to the debian packaging
- Use standard path for manpages
- On linux, if an open fails due to EPERM then try again
  without O_NOATIME

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- -i feature which lets you ignore entire files and directories
  (Thanks Etienne Bruines)
- -I feature which lets you only process filenames matching
  certain patterns.
- Both -i and -I support wildcards
- Specify C99 standard during compile (Thanks ecebuzz)

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Better error checking for extremely large values to command
  line parameters (Thanks Matthew Fernandez)
- Fix some boundary conditions in the range support added
  in 1.0.1 (Thanks Justas Lavišius)
- On Linux, support touching/evicting/displaying block devices
  directly. This displays the underlying buffer cache, not the
  filesystem cache (Thanks to maq123 for the suggestion)
- On Linux, open files with O_NOATIME so that we don't cause
  unnecessary disk activity recording access times
  (Thanks Mat R.)
- Replaces a stat() call with an fstat() call which is slightly
  more efficient.
- Skipped symlinks are no longer included in total file count
- Closes file descriptors after locking memory since there is
  no need to keep them open. This makes it less likely you will
  hit the RLIMIT_NOFILE when using -l or -L.
- TUNING.md file (Thanks to Artem Sheremet for the idea and
  to Vladimir Kotal for Solaris tuning info)

* Sat Feb 06 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Initial build
