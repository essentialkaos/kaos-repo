################################################################################

Summary:         Real-time web log analyzer and interactive viewer
Name:            goaccess
Version:         1.2
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv2+
URL:             http://goaccess.io

Source0:         http://tar.goaccess.io/goaccess-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc GeoIP-devel glib2-devel ncurses-devel

Requires:        GeoIP

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Open source real-time web log analyzer and interactive viewer that runs
in a terminal in *nix systems. It provides fast and valuable HTTP statistics
for system administrators that require a visual server report on the fly.

################################################################################

%prep
%setup -q

%build
%configure --enable-debug --enable-geoip --enable-utf8

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_docdir}/%{name}/*

################################################################################

%changelog
* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-0
- Added a Dockerfile.
- Added Amazon S3 bucket name as a VirtualHost (server block).
- Added a replacement for GNU getline() to dynamically expand line buffer
  while maintaining real-time output.
- Added --daemonize command line option to run GoAccess as daemon.
- Added several improvements to the HTML report on small-screen devices.
- Added option to the HTML report to auto-hide tables on small-screen
  devices.
- Added --process-and-exit command line option to parse log and exit.
- Added several feed readers to the list of browsers.
- Added "-" single dash per convention to read from the standard input.
- Added support for MaxMind GeoIP2.
- Added the ability to read and follow from a pipe such as
  "tail -f access.log | goaccess -"
- Added the ability to specify multiple logs as input sources, e.g.:
  "goaccess access.log access.log.1" while maintaining real-time output.
- Added time unit (seconds) to the processed time label in the HTML/terminal
  output.
- Added visitors' percent column to the terminal dashboard.
- Changed D3 charts to dim Y-axis on mouseover.
- Changed D3 charts to reflect HTML column sort.
- Changed D3 charts to render only if within the viewport. This improves the
  overall real-time HTML performance.
- Changed HTML report tables to render only if within the viewport.
- Changed percentage calculation to be based on the total within each panel.
- Ensure start/end dates are updated real-time in the HTML output.
- Ensure "window.location.hostname" is used as the default WS server host.
  In most cases, this should avoid the need for specifying "--ws-url=host".
  Simply using "--real-time-html" should suffice.
- Fixed issue on HTML report to avoid outputting scientific notation for all
  byte sizes.
- Fixed integer overflow when calculating bar graph length on terminal
  output.
- Fixed issue where global config file would override command line arguments.
- Fixed issue where it wouldn't allow loading from disk without specifying a
  file when executed from the cron.
- Fixed issue where parser couldn't read some X-Forwarded-For (XFF) formats.
  Note that this breaks compatibility with the original implementation of
  parsing XFF, but at the same time it gives much more flexibility on different
  formats.
- Fixed issue where specifying fifo-in/out wouldn't allow HTML real-time
  output.
- Fixed issue where the wrong number of parsed lines upon erroring out was
  displayed.
- Fixed issue where the WebSocket server would prevent establishing a
  connection with a client due to invalid UTF-8 sequences.
- Fixed percent issue when calculating visitors field.
- Updated the list of crawlers.

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Added data metric's "unique" count on each panel to the JSON/HTML outputs.
- Changed D3 bar charts to use .rangeBands and avoid extra outer padding.
- Fixed mouseover offset position issue on D3 bar charts.
- Fixed possible heap overflow when an invalid status code was parsed and
  processed. This also ensures that only valid HTTP status codes are parsed
  >=100 or <= 599.
- Fixed sluggish D3 chart re-rendering by changing how x-axis labels are
  displayed in the HTML report.

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1-0
- Added a new layout to the HTML report and additional settings and changes
- Added 'Amazon S3' Log Format to the list of predefined options
- Added 'Android 7.1 Nougat' to the list of OSs
- Added 'Android Marshmallow 6.0.1' to the list of OSs
- Added 'Android Nougat 7.0' to the list of OSs
- Added command line option --crawlers-only to display crawlers/bots only
- Added 'Feed Wrangler' to the list of feeds
- Added --fifo-in and --fifo-out command line options to set websocket FIF
  reader/writer
- Added 'Go-http-client' to the list of browsers
- Added 'MicroMessenger' (WeChat) to the list of browsers
- Added --no-html-last-updated command line option
- Added --num-tests command line option
- Added "Remote User" panel to capture HTTP authentication requests. Use %%
  within the log-format variable to enable this panel
- Added SemrushBot to set of crawlers
- Added tebibyte unit to the byte to string function converter
- Added the ability to parse reverse proxy logs that have multiple IPs. Thi
  adds the ability to parse the "X-Forwarded-For" field in a reverse prox
  setup
- Added the ability to set default preferences for the HTML report usin
  --html-prefs
- Added the ability to show which token didn't match log/date/time pattern
  This also ensures that in the absence of data, its output is not treated a
  error but instead it produces an empty report
- Added the ability to specify a WebSocket protocol (ws|wss) throug
  --ws-url
- Added the request query string to the W3C format
- Added TLS/SSL support to the HTML real-time report
- Changed browser classification for Google Cloud Clients
- Changed 'Darwin' OS to be in their own category
- Changed default W3C log format to use the URL path instead of full request
- Changed HTML default number of items on each table to 7
- Changed request parser to allow empty query strings
- Changed to use darkBlue theme as default HTML output theme
- Ensure every version of iOS is broken down under the OS panel
- Ensure latest JSON data is fast-forwarded when connection is opened
  GoAccess now sends the latest JSON data to the client as soon as th
  WebSocket connection is opened
- Ensure localStorage is supported and enabled in the HTML repor
- Ensure unknown coutries/continents are listed
- Fixed D3 chart width overflow issue on Edge
- Fixed integer to string key conversion for unique visitors. This fixes th
  issue where resulting keys would collide with existing keys and thus no
  keeping the right visitors count on certain panels
- Fixed memory leak when unable to URL decode %%q specifier
- Fixed memory leak when unable to URL decode %%U specifier
- Fixed month name abbreviation on app.js
- Fixed percentage integer overflow with large numbers on 32bits platforms
- Fixed percent calculation due to integer division rounding to zero
- Fixed possible code injection when outputting an HTML report
- Fixed segfault when using options -H or -M without an argument
- Removed timestamp from the HTML report title tag

* Tue Jul 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- Added minor changes to the HTML report stylesheet.
- Added the ability to specify the WebSocket port within --ws-url.
- Added the proper byte swap functions used by Sun Solaris.
- Added the proper default --http-method/protocol values on the config file.
- Changed bar transition to scale delay dynamically to the length of the
  dataset.
- Fixed build issue on platforms lacking of open_memstream() by refactoring
  the JSON module to use its own memory buffer.
- Fixed issue where the server wouldn't send cached buffer to slow clients.
- Fixed OS X build check of ncursesw.
- Implemented a throttle mechanism for slow clients to avoid caching too much
  data on the server-side.
- Removed flickering on D3 line and bar chart redraw.

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- Added Android version number along with the codename when using --real-os,
  e.g., 'Lollipop 5.1'
- Added some missing headers and function checks to configure.ac
- Fixed build issues on systems running GLIBC older than 2.9, such as RHEL <= 5
- Fixed a regression where it wouldn't allow abbreviated date and time formats
  such as %%F or %%T
- Fixed issue where it wouldn't send the whole buffer to a socket causing the
  real-time-html WebSocket server to progressively consume a lot more memory
- Fixed memory leak when using getline and follow mode enabled
- Fixed some buffer initialization issues on read_line() and
  perform_tail_follow()
- Fixed uint types in sha1 files

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- Added a complete real-time functionality to the HTML output
- Added an option to set the max number of items to show per panel
- Added command line option --enable-panel=<PANEL> to display the given module
- Added command line option --origin to match the origin WebSocket header
- Added command-line shortcuts for standard log formats, --log-format=COMBINED
- Added D3 Visualziations to the HTML dashboard
- Added metadata metrics to the each of the panels (JSON output)
- Added option to specify time distribution specificity
- Added --output=<file.[html|csv|json]> as a shortcut to --output-format
- Added the ability to download a JSON file from the HTML report
- Added the ability to output multiple formats on a single log parse
- Added the ability to output pretty json using --json-pretty-print
- Added the ability to set the date specificity in hours
- Added the ability to sort all HTML tables on all panels
- Added the ability to specify a custom CSS and JS file to the HTML report
- Added user-agents to the JSON output per each host
- Added 'Vivaldi' to the list of browsers
- Bootstrapify the HTML dashboard
- Changed configure.ac to use LDFLAGS instead of CFLAGS where applicable
- Changed default terminal color scheme to 256 Monokai if terminal supports 256
  colors
- Changed GoAccess license to The MIT License (MIT)
- Changed the visitors panel to display its dates continuously instead of top
- Change the visitors panel to display its dates continuously
- Default to 256 Monokai color scheme if terminal supports 256 colors
- Default to display HTTP method/protocol (if applicable)
- Display the children's Max. T.S. as the parent's top Max. T.S
- Ensure the parent's Avg. T.S. displays parent's Cum. T.S. over parent's Hits
- Fixed color issue when switching from the color scheme window
- Fixed cross platform build issue when ncurses is built with and without
  termlib=tinfo
- Fixed issue header curses window wouldn't clear out on small window sizes
- Fixed issue where tail mode wouldn't parse full lines using getline()
- Fixed minor background color issue when using ncurses 6
- Fixed possible division by zero when getting an entry percentage
- Fixed singly link list node removal
- Fixed still reachable memory leak on GeoIP cleanup (geoip legacy >= 1.4.7)
- Fixed Valgrind's still reachable memory leaks
- Removed -Wredundant-decls

* Wed Mar 09 2016 Gleb Goncharov <yum@gongled.ru> - 0.9.8-0
- Added a more complete list of static extensions to the config file.
- Added Android 6.0 Marshmallow to the list of OSs.
- Added the ability to scroll through panels on TAB with option to disable it
  --no-tab-scroll.
- Added the first and last log dates to the overall statistics panel.
- Ensure GoAccess links correctly against libtinfo.
- Ensure static content is case-insensitive verified.
- Fixed bandwidth overflow issue (numbers > 2GB on non-x86_64 arch).
- Fixed broken HTML layout when html-method/protocol is missing in config file.
- Refactored parsing and display of available modules/panels.

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.7-0
- Added Squid native log format to the config file
- Fixed int overflow when getting total bandwidth using the on-disk storage
- Fixed issue where a timestamp was stored as date under the visitors panel
- Fixed issue where config dialog fields were not cleared out on select
- Fixed issue where "Virtual Hosts" menu item wasn't shown in the HTML sidebar

* Tue Oct 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.6-0
- Fixed segfault when appending data to a log (follow) without virtualhosts.
- Added command line option `--dcf` to view the default config file path.
- Added 'Darwin' to the list of OSs.
- Added the ability to ignore parsing status codes using `--ignore-status`.

* Tue Oct 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.5-0
- Added major performance improvements to the default storage when parsing and
  storing data.
- Added the ability to parse virtual hosts and a new panel to display metrics
  per virtual host.
- Added the ability to parse HTTP/2 requests.
- Added the ability to use GNU getline() to parse full line requests.
- Added the ability to output debug info if a log file is specified, even
  without `--enable-debug`.
- Added OS X 'El Capitan'.
- Added WebDav HTTP methods and HTTP status from RFC 2518 and  RFC 3253.
- Fixed detection of some Googlebots.
- Fixed issue where time served metrics were not shown when loading persisted
  data.
- Fixed linker error on OSX: ld: library not found for -lrt.
- Fixed percentage on the HTML output when excluding IPs.
- Removed GLib dependency and refactored storage functionality. By removing
  this dependency, GoAccess is able to store data in a more efficient manner,
  for instance, it avoids storing integer data as void* (generic typing), thus
  greatly improving memory consumption for integers.

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.4-0
- Fixed inability to parse color due to a missing POSIX extension. ERR:
  Invalid bg/fg color pairs
- Added `%%~` specifier to move forward through a log string until a non-space
  char is found.
- Added the ability to parse static files containing a query string
  `--all-static-files`.
- Added the ability to parse native Squid access.log format.
- Added the ability to log invalid requests to a file `--invalid-requests`.
- Added additional overall metric - total valid requests.
- Fixed a few issues in the configuration script.

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Added the ability to set custom colors on the terminal output.
- Added the ability to process logs incrementally.
- Added a default color palette (Monokai) to the config file.
- Added column headers for every enabled metric on each panel.
- Added cumulative time served metric.
- Added maximum time served metric (slowest running requests).
- Added the ability to parse the query string specifier '(prc)q' from a log
  file.
- Added CloudFlare status codes.
- Added command option to disable column name metrics --no-column-names.
- Added AWS Elastic Load Balancing to the list of predefined log/date/time
  formats.
- Added DragonFly BSD to the list of OSs.
- Added Slackbot to the list of crawlers/browsers.
- Disabled REFERRERS by default.
- Ensure bandwidth metric is displayed only if the (prc)b specifier is parsed.
- Fixed issue where the '--sort-panel' option wouldn't sort certain panels.
- Fixed several compiler warnings.
- Set predefined static files when no config file is used.
- Updated Windows 10 user agent from 6.4 (wrong) to 10.0.(actual)

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- Added ability to fully parse browsers that contain spaces within a token.
- Added multiple user agents to the list of browsers.
- Added the ability to handle time served in milliseconds.
- Added the ability to parse a timestamp in microseconds.
- Added the ability to parse Google Cloud Storage access logs.
- Added the ability to set a custom title and header in the HTML report.
- Added timestamp log-format specifier.
- Ensure agents' hash table is destroyed upon exiting the program.
- Ensure 'Game Systems' are processed correctly.
- Ensure visitors panel header is updated depending if crawlers are parsed or
  not.
- Fixed issue where the date value was set as time value  in the config dialog.
- Fixed memory leak in the hits metrics when using the in-memory storage (GLib).

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- Added additional Nginx-specific status codes.
- Added Applebot to the list of web crawlers.
- Added Microsoft Edge to the list of browsers.
- Added the ability to highlight active panel through --hl-header.
- Ensure dump_struct is used only if using __GLIBC__.
- Ensure goaccess image has an alt attribute on the HTML output for valid HTML5.
- Ensure the config file path is displayed when something goes wrong (FATAL).
- Ensure there is a character indicator to see which panel is active.
- Fixed Cygwin compile issue attempting to use -rdynamic.
- Fixed issue where a single IP did not get excluded after an IP range.
- Fixed issue where requests show up in the wrong view even when
  --no-query-string is used.
- Fixed issue where some browsers were not recognized or marked as 'unknown'.
- Fixed memory leak when excluding an IP range.
- Fixed overflows on sort comparison functions.
- Fixed segfault when using on-disk storage and loading persisted data with -a.
- Removed keyphrases menu item from HTML output.
- Split iOS devices from Mac OS X.

* Thu Mar 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9-0
- Added ability to double decode an HTTP referer and agent
- Added ability to sort views through the command line on initial load
- Added additional data values to the backtrace report
- Added additional graph to represent the visitors metric on the HTML output
- Added AM_PROG_CC_C_O to configure.ac
- Added 'Android Lollipop' to the list of operating systems
- Added 'average time served' metric to all panels
- Added 'bandwidth' metric to all panels
- Added command line option to disable summary metrics on the CSV output
- Added numeric formatting to the HTML output to improve readability
- Added request method specifier to the default W3C log format
- Added support for GeoIP Country IPv6 and GeoIP City IPv6 through
  --geoip-database
- Added the ability to ignore parsing and displaying given panel(s)
- Added the ability to ignore referer sites from being counted
  A good case scenario is to ignore own domains. i.e., owndomain.tld
  This also allows ignoring hosts using wildcards
  For instance, *.mydomain.tld or www.mydomain.* or www?.mydomain.tld
- Added time/hour distribution module. e.g., 00-23
- Added 'visitors' metrics to all panels
- Added Windows 10 (v6.4) to the real windows user agents
- Changed AC_PREREQ macro version so it builds on old versions of autoconf
- Changed GEOIP database load to GEOIP_MEMORY_CACHE for faster lookups
- Changed maximum number of choices to display per panel to 366 fron 300
- Ensure config file is read from home dir if unable to open it from sysconfdir
  path
- Fixed array overflows when exceeding MAX_* limits on command line options
- Fixed a SEGFAULT where sscanf could not handle special chars within the
  referer
- Fixed character encoding on geolocation output (ISO-8859 to UTF8)
- Fixed issue on wild cards containing '?' at the end of the string
- Fixed issue where a 'Nothing valid to process' error was triggered when the
  number of invalid hits was equal to the number of valid hits
- Fixed issue where outputting to a file left a zero-byte file in pwd
- Improved parsing of operating systems
- Refactored log parser so it allows with ease the addition of new modules. This
  also attempts to decouple the core functionality from the rendering functions
  It also gives the flexibility to add children metrics to root metrics for any
  module. e.g., Request A was visited by IP1, IP2, IP3, etc
- Restyled HTML output

* Fri Feb 20 2015 Anton Novojilov <andy@essentialkaos.com> - 0.8.5-0
- Initial build
