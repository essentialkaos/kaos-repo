################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Interactive process viewer
Name:           htop
Version:        3.3.0
Release:        0%{?dist}
License:        GPLv2
Group:          Applications/System
URL:            https://htop.dev

Source0:        https://github.com/htop-dev/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc ncurses-devel lm_sensors-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
htop is an interactive process viewer for Linux.

htop allows scrolling the list of processes vertically and horizontally to see
their full command lines and related information like memory and CPU
consumption. Also system wide information, like load average or swap usage,
is shown.

The information displayed is configurable through a graphical setup and can
be sorted and filtered interactively.

################################################################################

%prep
%setup -q

%build
%configure --enable-sensors

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_datadir}/applications
rm -rf %{buildroot}%{_datadir}/pixmaps
rm -rf %{buildroot}%{_datadir}/icons

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%doc %{_mandir}/man1/htop.1*
%{_bindir}/htop

################################################################################

%changelog
* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 3.3.0-0
- Multiple refactorings and code improvements
- Shorten docker container IDs to 12 characters
- Settings: preserve empty header
- Fix execlp() argument without pointer cast
- OpenFilesScreen: Make column sizing dynamic for file size, offset and inode
- Add support for "truss" (FreeBSD equivalent of "strace")
- Darwin: add NetworkIOMeter support
- HeaderLayout: add "3 columns - 40/30/30", "... 30/40/30" & "... 30/30/40"
- Meter: use correct unicode characters for digit '9'
- Note in manual re default memory units of KiB
- Add column for process container name
- Add logic to filter the container name (+type) from the CGroup name
- Change NetworkIOMeter value unit from KiB/s to bytes/second
- Cap DiskIOMeter "utilisation" percentage at 100%
- PCP platform implementation of frontswap and zswap accounting
- Shorten podman/libpod container IDs to 12 characters
- Write configuration to temporary file first
- Incorporate shared memory in bar text
- Move shared memory next to used memory
- Correct order of memory meter in help
- Add recalculate to Ctrl-L refresh
- Update process list on thread visibility toggling
- Support dynamic screens with 'top-most' entities beyond processes
- Introduce Row and Table classes for screens beyond top-processes
- Rework ZramMeter and remove MeterClass.comprisedValues
- More robust logic for CPU process percentages (Linux & PCP)
- Show year as start time for processes older than a year
- Short-term fix for docker container detection
- default color preset: use bold blue for better visibility
- Document 'O' keyboard shortcut
- Implement logic for '--max-iterations'
- Update F5 key label on tab switch (Tree <-> List)
- Force re-sorting of the process list view after switching between
  list/treeview mode
- Linux: (hack) work around the fact that Zswapped pages may be SwapCached
- Linux: implement zswap support
- {Memory,Swap}Meter: add "compressed memory" metrics
- Darwin: add DiskIOMeter support
- Fix scroll relative to followed process
- ZramMeter: update bar mode
- Use shared real memory on FreeBSD
- Increase Search and Filter max string length to 128
- Improve CPU computation code
- Remove LXC special handling for the CPU count
- Create new File Descriptor meter
- PCP: add IRQ PSI meter
- Linux: add IRQ PSI meter
- Linux: highlight username if process has elevated privileges
- Add support for scheduling policies
- Add a systemd user meter to monitor user units.
- FreeBSD: remove duplicate zfs ARC size subtraction

* Thu Mar 09 2023 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- CPUMeter now can show frequency in text mode
- Add option to render distribution path prefixes shadowed
- DiskIOMeter converts to bytes per second (not per interval)
- DiskIOMeter uses complete units, including missing "iB/s"
- DiskIOMeter indicates read and write in meter mode
- NetworkIOMeter converts to packets per second, shows packet rate
- Allow continued process following when changing display settings
- Update the panel header when changing to another tab
- Drop margin around the header if there are no meters
- Use Unicode replacement character for non-printable characters
- Default color preset uses bold blue for better visibility
- Update the Panel header on sort order inversions ('I')
- Toggle the header meters with pound key
- Fix ScreenPanel to handle quitting the panel while renaming
- Add fallback for HOME environment variable using passwd database
- Replace meaningless ID column with FD column in lock screen
- Use device format in the lock screen matching the files screen
- On Linux, improvements to file-descriptor lock detection
- On Linux, further distinguish systemd states in the SystemdMeter
- On Linux, improvements to cgroup and container identification
- On Linux, support openat(2) without readlinkat(2) platforms
- On Darwin, fix current process buffer handling for busy systems
- On DragonFly BSD, fix incorrect processor time of processes
- On FreeBSD, fix an issue with the memory graph not showing correctly
- On FreeBSD, add support for displaying shared memory usage
- On PCP, use pmLookupDescs(3) if available for efficiency
- On PCP, normalize generic columns values for consistent display
- On PCP, changes preparing for configurable, dynamic screens
- Handle invalid process columns from the configuration file
- Avoid undefined behaviour with deeply nested processes
- Fix crash when removing the currently active screen
- Prevent possible crash on a very early error path
- Include automake for Debian/Ubuntu
- Restore non-mouse support
- Reject unsupported command line arguments
- Document idle process state
- Clarify M_TRS/M_DRS columns

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Fix setting to show all branches collapsed by default
- Restore functionality of stripExeFromCmdline setting
- Fix some command line display settings not being honored without restart
- Display single digit precision for CPU% greater than 99.9%
- On Linux, FreeBSD and PCP consider only shrinkable ZFS ARC as cache
- On Linux, increase field width of CPUD% and SWAPD% columns
- Colorize process state characters in help screen
- Use mousemask(3X) to enable and disable mouse control
- Fix heap buffer overflow in Vector_compact
- On Solaris, fix a process time scaling error
- On Solaris, fix the build
- On NetBSD, OpenBSD and Solaris ensure env buffer size is sufficient
- On Linux, resolve processes exiting interfering with sampling
- Fix ProcessList quadratic removal when scanning processes
- Under LXC, limit CPU count to that given by /proc/cpuinfo
- Improve container detection for LXC
- Some minor documentation fixes

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- Support for displaying multiple tabs in the user interface
- Allow multiple filter and search terms (logical OR, separate by "|")
- Set correct default sorting direction (defaultSortDesc)
- Improve performance for process lookup and update
- Rework the IOMeters initial display
- Removed duplicate sections on COMM and EXE
- Highlight process UNINTERRUPTIBLE_WAIT state (D)
- Show only integer value when CPU% more than 99.9%
- Handle rounding ambiguity between 99.9 and 100.0%
- No longer leaves empty the last column in header
- Fix header layout and meters reset if a header column is empty
- Fix PID and UID column widths off-by-one error
- On Linux, read generic sysfs batteries
- On Linux, do not collect LRS per thread (it is process-wide)
- On Linux, dynamically adjust the SECATTR and CGROUP column widths
- On Linux, fix a crash in LXD
- On FreeBSD, add support for showing process emulation
- On Darwin, lazily set process TTY name
- Always set SIGCHLD to default handling
- Avoid zombie processes on signal races
- Ensure last line is cleared when SIGINT is received
- Instead of SIGTERM, pre-select the last sent signal
- Internal Hashtable performance and sizing improvements
- Add heuristics for guessing LXC or Docker from /proc/1/mounts
- Force elapsed time display to zero if process started in the future
- Avoid extremely large year values when printing time
- Fix division by zero when calculating IO rates
- Fix out of boundary writes in XUtils
- Fix custom thread name display issue
- Use AC_CANONICAL_HOST, not AC_CANONICAL_TARGET in configure.ac
- Support libunwind of LLVM

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.1.2-0
- Bugfix for crash when storing modified settings at exit
- Generate xz-compressed source tarball (with configure) using github actions
- Allow -u UID with numerical value as argument
- Added documentation for obsolete/state libraries/program files highlighting
- Some obsolete/stale library highlighting refinements
- Column width issues resolved
- Dynamic UID column sizing improved
- Discard stale information from Disk and Network I/O meters
- Refined Linux kernel thread detection
- Reworked process state handling
- New CCGROUP column showing abbreviated cgroup name
- New OFFSET column in the list of open files screen

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- Update license headers to explicitly say GPLv2+
- Document minimum version for libcap
- Fix mouse wheel collision with autogroups nice adjustment
- Adjust Makefile.am macro definitions for older automake versions
- Ensure consistent reporting of MemoryMeter 'used' memory
- Report hugepage memory as real and used memory (as before)
- Handle procExeDeleted, usesDeletedLib without mergedCommandline mode
- Validate meter configuration before proceeding beyond htoprc parsing
- Properly release memory on partially read configuration
- Handle interrupted sampling from within libpcp PDU transfers
- On Linux, provide O_PATH value if not defined
- On Linux, always compute procExeDeleted if already set
- Workaround for Rosetta 2 on Darwin
- Fix FreeBSD cmdline memory leak in Process_updateCmdline, and
- Plug a Disk I/O meter memory leak on FreeBSD

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.1.0-0
- Updated COPYING file to remove the PLPA exemption (appendix 2)
  With this change the license is now GPLv2 without any additional wording.
- Improved default sort ordering
  Note for users: This may lead to an inverted sort order on startup of
  htop 3.1.0 compared to previous versions.
  This is due to what is stored in your htoprc file. Solution: Press I
  (to invert sort order).
  This changed setting will be saved by htop on exit as long as it can
  write to your htoprc file.
- The compile-time option to cater specifically for running htop as
  setuid has been removed
- Add read-only option
  This allows htop to be run in an non-intrusive fashion where it acts only
  as a process viewer disabling all functions to manipulate system state.
  Note: This is not a security feature!
- Move the code for handling the command line formatting related tasks
  to be shared across all platforms
  This means important features like stale binary/library highlighting
  can now be available on all supported platforms.
- Make the EXE and COMM columns available on all platforms
  All supported platforms have the name of the executable (EXE) and a
  self-chosen thread/command name (COMM) available one way or the other.
  Moving this column to be handled as a platform-independently available
  information simplifies the markup of the command line.
- Introduce configuration file versioning and config_reader_min_version
  Starting with this version the configuration file contains a version
  identifying the minimum version of the configuration parser needed to
  fully understand the configuration file format.
  Old configuration file formats are automatically upgraded when
  saving the config file (htoprc).
- Make the configuration parser friendlier to users
  With this change only settings that cannot be parsed properly are
  reset to their defaults.
- Improve default display for systems with many CPUs
- Add the process ELAPSED time column
- Improve the process STATE column sorting
- Reworked handling resize and redrawing of the UI
- Fixed an issue where the LED meter mode could overflow allotted space
- Allow text mode Meters to span empty neighbors to the right
- Rescale graph meters when value of total changes
- Update generic process field display
  Usually "uninteresting" values in columns like 1 thread, nice value
  of 0, CPU and memory of 0%, idle/sleeping state, etc. are shown with
  reduced intensity (dark grey)
- Option and key ("*") to collapse / expand all branches under PID 1
  (and PID 2 if kernel threads are shown)
- Keep following a process when inverting the sort order, displaying
  the help screen or hiding/unhiding userland threads.
  If a thread is currently selected the selection is updated to point
  to the thread's parent process.
- Reorder process scanning to be performed before updating the display
  of the meters in the header
- Always check the user for a process for any changes.
  This affects multiple platforms that previously didn't correctly handle
  the user field for a process to change at runtime (e.g. due to seteuid
  or similar syscalls).
- Disable mouse option when support is unavailable
- Support curses libraries without ncurses mouse support
- Support offline and hot-swapping of CPUs on all platforms
- Fix the CPU Meter for machines with more than 256 CPUs
- Supplemented the "show updated/deleted executables" feature (red basename)
  to indicate when linked libraries were updated (yellow basename)
- Apply the stale binary highlighting for the EXE column in addition to
  the command line field
- Add new combined Memory and Swap meter
- Implement bar and graph mode for NetworkIO Meter
- Rework TTY column to be more consistent across platforms
- Make the CWD column generally available on all platforms
- Add Performance Co-Pilot (PCP) platform support
  This is added via a separate pcp-htop(1) binary which provides remote host
  analysis, new Meters for any PCP metric and new Columns for any PCP process
  metric - see the pcp-htop(5) man page for further details.
- Add Linux columns and key bindings for process autogroup identifier
  and nice value
- Change available and used memory reporting on Linux to be based on
  MemAvailable (Kernel 3.14+)
- Add a new SysArchMeter showing kernel and platform information
- Linux memory usage explicitly treats tmpfs memory usage as shared memory
  This is to make memory used by tmpfs visible as this cannot be freed
  unlike normal filesystem cache data.
- Exclude zram devices when calculating DiskIO on Linux
- Use PATH lookup for systemctl in systemd meter
- Add native platform support for NetBSD
  This allows htop to run on NetBSD without the need for active Linux
  emulation of the procfs filesystem.
- Add NetworkIO, DiskIO, CPU frequency, and battery meter support on NetBSD
- Fix NetBSD display of in-use and cached memory
- Rework NetBSD CPU and memory accounting
- Fix NetBSD accounting of user and kernel threads
- Initial work to allow building with default libcurses on NetBSD
- FreeBSD updates - implement process majflt and processor column values
- Add FreeBSD support for CPU frequency and temperature
- Fixes and cleanups for ZFS Meters and metrics
- Correctly color the ZFS ARC ratio
- Bugfixes related to CPU time display/calculations for darwin on M1 systems
- Harmonize the handling of multiple batteries across different platforms.
  The system is now considered to run on AC if at least one power supply
  marked as AC is found in the system.
  Battery capacity is summed up over all batteries found.
  This also changes the old behavior that batteries reported by the
  system after the first AC adapter where sometimes ignored.
- Correctly handle multiple batteries on Darwin.
  Resolves a possible memory leak on systems with multiple batteries.
- Handle Linux Shmem being part of Cached in the MemoryMeter
- Add SwapCached to the Linux swap meter
- Convert process time to days if applicable
- Always show the number of threads in the TaskMeter, even when threads
  are not shown in the process list
- Fix Linux --drop-capabilities option handling
- Correctly detect failure to initialize Linux boottime
- Overhaul the Linux memory fields to partition them like free(1) now does
- Improve the Linux process I/O column values
- Rework the libsensors parsing on Linux
- Update the MemoryMeter to display shared memory
- Update OpenBSD platform - implement additional columns, scan LWP,
  proper markup for STATE, show CPU frequency
- Fix the tree view on OpenBSD when hiding kernel threads
- Remove old InfoScreen lines before re-scanning
- Document historic naming of Light-Weight Processes column aka threads
- Improve user interaction when the last process entry is selected
- Draw the panel header on the TraceScreen
- Add mouse wheel scroll and fix mouse selection on the InfoScreen
- Add a HugepageMeter and subtract hugepages from normal memory
- Display wide characters in LED meters and restore non-wide ncurses support
- Add command line option to drop Linux capabilities
- Support scheduler affinity on platforms beyond Linux
- Report on any failure to write the configuration file
- Cache stderr to be able to print assert messages.
  These messages are shown in case htop terminates unexpectedly.
- Print current settings on crash
- Reset signal handlers on program exit
- Add configure script option to create a static htop binary
- Resolved longer-standing compilation issues on Solaris/Illumos
- Check for availability of set_escdelay in configure
- Build system updates for autotools 2.70

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- BUGFIX / SECURITY: InfoScreen: fix uncontrolled format string
- BUGFIX: Improve white text in the Light Terminal colour scheme
  (both of the above thanks to V)
- Enable the function bar on the main screen to be hidden (see Setup ->
  Display options)
- BUGFIX: Reduce layout issues esp. around printing wide characters (not
  complete yet)
- BUGFIX: Make the follow function exit cleanly after followed process died
- Solaris: make Process callbacks static
- Update help and man page for improved -t / -s options
- Drop usage of formatted error messages from <err.h>
- Show arrow indicating order of sorted process column
- Lots of plumbing around the internal Hashtable, hardening and code cleanups
- LibSensors: add support for Ryzen CPUs
- BUGFIX: Fix CPU percentage on M1 silicon Macs
- LoadMeter: dynamically adjust color and total of bar
- Find libsensors.so.4 for Fedora and friends
- Add support to display CPU frequencies on Solarish platforms
- Enable going back to previous search matches (Shift-F3)
- Added keybind 'N' for sorting by PID (drops 'n'/'N' as not used before much)


* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.4-0
- Separate tree and list sort orders
- Invert Process_compare so that superclass matches run first
- Unhardcode Mac OS tick-to-milliseconds conversion
- Check if clock_gettime needs linking of librt
- Define O_PATH if not already defined
- Add column on Mac for processes running under translation
- Configure check for additional linker flags for keypad(3)
- PSI Meter: constant width and only print ten-duration as bar
- Sort in paused mode after inverting sort order
- Handle absence of package CPU temperature
- Meter: restore non-wide-character build
- LibSensors: restore temperature for Raspberry Pi
- MainPanel: do not reset hideProcessSelection on KEY_SHUFFLE
- BarMeter: rework text padding
- Panel: rework drawing of FunctionBar
- Meter: fix artifacts with very tiny width
- DragonFlyBSD updates
- BUGFIX: Fix dlopen issue for libsensors5 for some platforms
- BUGFIX: Fix broken tree display on inverted sort order
- BUGFIX: Fix pause mode ("Z") in tree view
- BUGFIX: Correct timebase for non-x86 CPUs on Darwin
- BUGFIX: Avoid NULL dereference on zombie processes
- Document dynamic bindings and assumed external configuration
- Update key mapping documentation for sorting

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.3-0
- Improved command display/sort functionality
- Add screen for active file locks
- Calculate library size (M_LRS column) from maps file
- Add a Zram meter
- Add Linux cwd process column
- Dynamically load libsensors at runtime
- Improve PressureStall Meter display strings
- Hide process selection on ESC
- Fully support non-ascii characters in Meter-Bar
- Add support to change numeric options in settings screen
- Rename virtual memory column from M_SIZE to M_VIRT
- Add process column for normalized CPU usage
- Show CPU temperature in CPU meter
- Drop hideThreads Setting
- Add a systemd meter
- Add a network IO meter
- Add a SELinux meter
- Compress size of default FunctionBar
- Updates to the OpenFiles screen
- Continue updating header data in paused mode
- BUGFIX: Handle data wraparounds in IO meters
- BUGFIX: Update InfoScreen content on resize
- Add security attribute process column
- Add DiskIOMeter for IO read/write usage
- Read CPU frequency from sysfs by default
- Add Linux process column for context switches
- Several FreeBSD and Mac OS X platform updates
- Add process environment for FreeBSD
- Parse POWER_SUPPLY_CAPACITY for Linux Battery meter
- Add octuple-column CPU meters.
- BUGFIX: On Linux consider ZFS ARC to be cache
- BUGFIX: Limit screen title length to window width
- Show selected command wrapped in a separate window
- Allow to pass '/' for item search
- Document implicit incremental search
- Handle 'q' as quit if first character
- Avoid expensive build of process tree when not using it
- Include documentation for COMM and EXE
- Distinguish display of no permissions for reading M_LRS
- Only calculate M_LRS size every 2 seconds
- Improvements to comm / cmdline display functionality
- Merged view for COMM, EXE and cmdline
- Consistent kernel thread display for COMM/EXE columns
- Central fault handling for all platforms
- Handle parsing envID & VPid from process status file
- Use threshold for display of guest/steal/irq meters
- Enhance highlighting of semi-large and large numbers
- Documentation on the repository style guide
- Align processor identifier to the right
- Document M_PSS, M_PSSWP, M_SWAP in man page
- Add Date and DateTime meters
- BUGFIX: Fix Solaris 11.4 due to missing ZFS ARC kstats
- Code hardening, speedups, fd and memory leak fixes
- Number CPUs from zero by default
- Remove residual python checks during the build process

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- BUGFIX: Drop 'vim_mode' - several issues, needs rethink
- BUGFIX: fix regression in -u optional-argument handling
- Build system rework to remove python, header generation
- BUGFIX: report nice level correctly on Solaris
- CI, code quality improvements

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.1-0
- Coverity fixes, CI improvements, documentation updates
- BUGFIX: Fix early exit with longer sysfs battery paths
- BUGFIX: Improve OOM output, fix sorting
- Rework check buttons and tree open/closed
- Add -U/--no-unicode option to disable unicode
- Improvements to the affinity panel

* Thu Aug 18 2022 Anton Novojilov <andy@essentialkaos.com> - 3.0.0-0
- Support ZFS ARC statistics
- Support more than 2 smaller CPU meter columns
- Support Linux proportional set size metrics
- Support Linux pressure stall information metrics
- New display option to show CPU frequency in CPU meters
- Update Linux sysfs battery discovery for recent kernels
- Add hardware topology information in the affinity panel
- Add timestamp reporting to the strace screen
- Add simple, optional vim key mapping mode
- Added an option to disable the mouse
- Add Solaris11 compatibility
- Without an argument -u uses $USER value automatically
- Support less(1) search navigation shortcuts
- Update the FreeBSD maximum PID to match FreeBSD change
- Report values larger than 100 terabytes
- Widen ST_UID (UID) column to allow for UIDs > 9999
- BUGFIX: fix makefiles for building with clang
- BUGFIX: fix <sys/sysmacros.h> major() usage
- BUGFIX: fix the STARTTIME column on FreeBSD
- BUGFIX: truncate overwide jail names on FreeBSD
- BUGFIX: fix reported memory values on FreeBSD
- BUGFIX: fix reported CPU meter values on OpenBSD
- BUGFIX: correctly identify other types of zombie process
- BUGFIX: improve follow-process handling in some situations
- BUGFIX: fix custom meters reverting to unexpected setting
- BUGFIX: close pipe after running lsof(1)
- BUGFIX: meters honour setting of counting CPUs from 0/1

* Sat Jun 16 2018 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Solaris/Illumos/OpenIndiana support
- -t/--tree flag for starting in tree-view mode
- macOS: detects High Sierra version to avoid OS bug
- OpenBSD: read battery data
- Various automake and build improvements
- Check for pkg-config when building with --enable-delayacct
- Avoid some bashisms in configure script
- Use CFLAGS from ncurses*-config if present
- Header generator supports non-UTF-8 environments
- Linux: changed detection of kernel threads
- Collapse current subtree pressing Backspace
- BUGFIX: fix behavior of SYSCR column
- BUGFIX: obtain exit code of lsof correctly
- BUGFIX: fix crash with particular keycodes
- BUGFIX: fix issue with small terminals
- BUGFIX: fix terminal color issues
- BUGFIX: preserve LDFLAGS when building
- BUGFIX: fixed overflow for systems with >= 100 signals

* Wed Feb 07 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.1.0-0
- Linux: Delay accounting metrics
- DragonFly BSD support
- Support for real-time signals
- 'c' key now works with threads as well
- Session column renamed from SESN to SID
- Improved UI for meter style selection
- Improved code for constructing process tree
- Compile-time option to disable setuid
- Error checking of various standard library operations
- Replacement of sprintf with snprintf
- Linux: performance improvements in battery meter
- Linux: update process TTY device
- Linux: add support for sorting TASK_IDLE
- Linux: add upper-bound to running process counter
- BUGFIX: avoid crash when battery is removed
- BUGFIX: macOS: fix infinite loop in tree view

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
