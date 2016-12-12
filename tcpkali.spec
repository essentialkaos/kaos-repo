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

Summary:            High performance TCP and WebSocket load generator and sink
Name:               tcpkali
Version:            1.0
Release:            0%{?dist}
License:            BSD 2-Clause
Group:              Development/Tools
URL:                https://github.com/machinezone/tcpkali

Source0:            https://github.com/machinezone/%{name}/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ m4 autoconf automake libtool
BuildRequires:      bison flex ncurses-devel

Provides:           %{name} = %{version}-%{release} 

###############################################################################

%description
High performance TCP and WebSocket load generator and sink

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
autoreconf -iv

%{_configure} --prefix=%{_prefix}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md TODO.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

###############################################################################

%changelog
* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Export --latency-connect and --latency-first-bytes to statsd.
- --latency-percentiles now affect --statsd reporting as well.
- Added -H, --header to add HTTP headers to WebSocket handshake.
- Added --message-stop to quickly die if a given message is seen.

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9-0
- Added -r@<Latency> form to measure message rate at a given latency.
- Websocket frame types in expressions: \{ws.ping}, \{ws.pong}, etc.
- Websocket frames accept files: \{ws.binary <image.png>}.
- Websocket frames can be non-final: \{ws.binary ...}.
- Regular expressions as data generators: \{re <regex>}.
- Display last received bytes with --verbose 2.

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 0.8-0
- Added --latency-connect to measure connect latency.
- Added --latency-first-byte to measure latency to first byte.
- Added --latency-percentiles to control percentile reporting.
- Mean/max latencies for messages are not reported, for UI
  consistency. Use --latency-percentiles 50,100 to display.
- Added --dump-{one,all}{,-in,-out} to dump all or one
  connections' input/output.
- Added --write-combine=off to emit high packet rates.

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 0.7-0
- Added a manual page. man tcpkali after installation.
- Exceed 64k connections limit by using all available IP aliases on network interfaces.
- --latency-marker-skip <N> to ignore the first occurrences of a marker.
- --listen-mode=active to send data for connections received through -l.
- --source-ip <IP> option to restrict or change source IPs.
- "Bandwidth per channel:" output changed to ⇅ to reflect bi-direction.

* Thu May 14 2015 Anton Novojilov <andy@essentialkaos.com> - 0.6-0
- Parse \{connection.uid} type expressions in --first-message, --message, 
  --latency-marker parameters, allowing constructing payloads unique per 
  connection.
- Added "k" multiplier to --connections; allowing for a -c10k 
  option (inside joke ;)

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 0.5-0
- --enable-asan and --enable-tsan flags to enable address/thread sanitizer
- Do not account latencies for --first-message
- Maximum storable latency increased from 10s to 100s
- -e (--unescape-message-args) now affect --latency-marker string as well
- --websocket now awaits response after sending HTTP upgrade headers
- Add WebSocket masking on client->server communication (mandated by RFC)
- Use Boyer-Moore-Horspool to search --latency-marker in the stream
- Add --sndbuf and --rcvbuf command line options to adjust kernel buffers via setsockopt(SO_*BUF)
- Record latencies even if only a portion of a message has been sent

* Wed Mar 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.4.2-0
- Initial build
