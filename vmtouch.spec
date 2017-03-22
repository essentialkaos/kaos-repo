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

Summary:            Portable file system cache diagnostics and control
Name:               vmtouch
Version:            1.3.0
Release:            0%{?dist}
License:            BSD 3-Clause
Group:              Development/Tools
URL:                https://github.com/hoytech/vmtouch

Source0:            https://github.com/hoytech/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description

vmtouch is a tool for learning about and controlling the file system cache 
of unix and unix-like systems. It is BSD licensed so you can basically 
do whatever you want with it.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} \
        PREFIX="%{buildroot}" \
        BINDIR="%{buildroot}%{_sbindir}" \
        MANDIR="%{buildroot}%{_mandir}/man8"

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, -)
%doc CHANGES README.md TODO
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*

###############################################################################

%changelog
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
