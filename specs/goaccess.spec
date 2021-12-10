################################################################################

Summary:         Real-time web log analyzer and interactive viewer
Name:            goaccess
Version:         1.5.3
Release:         0%{?dist}
Group:           Development/Tools
License:         GPLv2+
URL:             https://goaccess.io

Source0:         https://tar.goaccess.io/goaccess-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc GeoIP-devel glib2-devel ncurses-devel openssl-devel

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
%configure --enable-utf8 --with-openssl --enable-geoip=legacy

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
%config(noreplace) %{_sysconfdir}/%{name}/browsers.list
%config(noreplace) %{_sysconfdir}/%{name}/podcast.list
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/locale/*/LC_MESSAGES/goaccess.mo
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- Added additional crawlers to the default list.
- Added Italian translation (i18n).
- Added 'macOS 12' to the list of OS.
- Fixed buffer overflow caused by an excessive number of invalid requests with
  multiple logs.
- Fixed visualization issue on the HTML report for panels with disabled chart.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Added .avi to the list of static requests/extensions.
- Changed label from 'Init. Proc. Time' to 'Log Parsing Time'.
- Fixed issue where lengthy static-file extension wouldn't account certain valid
  requests.
- Fixed possible buffer underflow when checking static-file extension.
- Fixed segfault when attempting to parse an invalid JSON log while using a JSON
  log format.
- Fixed segfault when ignoring a status code and processing a line > '4096'
  chars.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Changed official deb repo so it now builds '--with-getline' in order to
  support request lines longer than 4096.
- Ensure there's no tail delay if the log file hasn't changed.
- Fixed data race when writing to a self-pipe and attempting to stop the WS
  server.
- Fixed inability to close expanded panel when pressing 'q' on TUI.
- Fixed possible data race during parsing spinner label assignment.
- Increased the maximum number of files to monitor from '512' to '3072'.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- Added a Docker container based isolated build environment (Debian).
- Added Dark Mode detection to the HTML report.
- Added the ability for the WebSocket server to bind to a Unix-domain socket.
- Added the ability to parse IPs enclosed within brackets (e.g., IPv6).
- Changed categorization of requests containing 'CFNetwork' to 'iOS' when
  applicable.
- Changed command line option from '--hide-referer' to '--hide-referrer'.
- Changed command line option from '--ignore-referer' to '--ignore-referrer'.
- Fixed a potential division by zero.
- Fixed inablity to parse IPv6 when using a 'CADDY' log format.
- Fixed issue where a 'BSD' OS could be displayed as Linux with certain
  user-agents.
- Fixed memory leak when a JSON value contained an empty string(e.g., JSON/CADDY
  format).
- Fixed possible buffer overflow on a WS packet coming from the browser.
- Refactored a substancial part of the storage codebase for upcoming
  filtering/search capabilities (issue #117).
- Refactored DB storage to minimize memory consumption up to '35%'.
- Updated default 'AWS Elastic Load Balancing' log format.
- Updated German translation.
- Updated page size to 24 on the HTML report.
- Updated UNIX OS catergories.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.6-0
- Added additional feed reader clients.
- Added additional browsers and bots to the main list.
- Added command line option '--unknowns-log' to log unknown browsers and OSs.
- Added 'Referer' to the pre-defined 'Caddy JSON' log format.
- Added support for real-time piping as non-root user.
- Added the ability to Handle case when IPv4 is encoded as IPv6 in
  GeoIP1/legacy.
- Ensure we capture linux (lowercase) when extracting an OS.
- Fixed a regression in parsing Google Cloud Storage or possibly other non-JSON
  formats.
- Fixed inability to parse escaped formats.
- Fixed issue when using '%%s' with 'strptime(3)' under musl libc. This
  addresses mostly the Docker image.
- Fixed possible buffer over-read for certain log-format patterns.
- Fixed segfault when attempting to process a malformed JSON string.
- Fixed segfault when setting an empty log-format from the TUI dialog.
- Fixed sorting on hits and visitors when larger than INT_MAX.
- Updated CloudFront pre-defined log-format to reflect the latest fields.
- Updated 'Dockerfile' image to use 'alpine:3.13' instead of edge due to
  compatibility issue with the GNU coreutils.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- Fixed build issue due to initial declarations only allowed in C99 mode
  (e.g., CentOS7).

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- Added 'Caddy' to the list of pre-defined log formats.
- Added command line option '--no-strict-status' to disable status validation.
- Added native support to parse JSON logs.
- Added the ability to process timestamps in milliseconds using '%%*'.
- Ensure TUI/CSV/HTML reports are able to output 'uint64_t' data.
- Ensure we allow UI render if the rate at which data is being read is greater
  than '8192' req/s.
- Ensure we don't re-render Term/HTML output if no data was read/piped.
- Fixed build configure to work on NetBSD.
- Fixed issue where it would send data via socket each second when managed by
  systemd.
- Fixed issue where parser was unable to parse syslog date with padding.
- Fixed issue where some items under browsers.list were not tab separated.
- Fixed issue where the format parser was unable to properly parse logs
  delimited by a pipe.
- Fixed issue where T.X. Amount metrics were not shown when data was piped.
- Fixed issue where XFF parser could swallow an additional field.
- Fixed memory leak when using '%x' as date/time specifier.
- Replaced select(2) with poll(2) as it is more efficient and a lot faster than
  select(2).
- Updated Swedish i18n.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- Added the ability to set how often goaccess will parse data and output to the
  HTML report via '--html-refresh=<secs>'.
- Changed how TLS is parsed so the Cypher uses a separate specifier. It now
  uses '%K' for the TLS version and '%k' for the Cypher.
- Fixed issue where real-time output would double count a rotated log. This was
  due to the change of inode upon rotating the log.
- Updated man page to reflect proper way of 'tail -f' a remote access log.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- Added the ability to show 'Encryption Settings' such as 'TLSv1.2' and Cipher
  Suites on its own panel.
- Added the ability to show 'MIME Types' such as 'application/javascript' on its
  own panel.
- Changed Debian build to use mmdb instead of libgeoip (legacy).
- Ensure the HTML report defaults to widescreen if viewport is larger
  than '2560px'.
- Fixed inability to properly process multiple logs in real-time.
- Fixed issue where named PIPEs were not properly seed upon generating
  filename.
- Fixed issue where served time metrics were not shown when data was piped.
- Removed unnecessary padding from SVG charts. Improves readability on mobile.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- Added addtional browsers and bots to the main list.
- Added 'Android 11' to the list of OSs.
- Added 'macOS 11.0 Big Sur' to the list of OSs.
- Added 'average' to each panel overall metrics.
- Added '.dmg', '.xz', and '.zst' to the static list.
- Added extra check to ensure restoring from disk verifies the content of the
  log against previous runs.
- Added Russian translation (i18n).
- Added Ukrainian translation (i18n).
- Added support for HTTP status code '308'.
- Added the ability for 'get_home ()' to return NULL on error, instead of
  terminating the process. Great if using through systemd.
- Added the ability to read lowercase predefined log formats. For
  instance, '--log-format=COMBINED' or '--log-format=combined'.
- Changed how FIFOs are created and avoid using predictable filenames
  under '/tmp'.
- Changed '--ignore-referer' to use whole referrer instead of referring site.
- Ensure Cache Status can be parsed without sensitivity to case.
- Ensure restored data enforces '--keep-last' if used by truncating
  accordingly.
- Fixed a few memory leaks when restoring from disk.
- Fixed blank time distribution panel when using timestamps.
- Fixed build issue due to lack of 'mmap' on 'Win'/'Cygwin'/'MinGW'.
- Fixed crash in mouse enabled mode.
- Fixed double free on data restore.
- Fixed inability to keep processing a log when using '--keep-last'.
- Fixed inability to properly parse truncated logs.
- Fixed inability to properly count certain requests when restoring from disk.
- Fixed issue where it would not parse subsequent requests coming from stdin
  (tail).
- Fixed issue where log truncation could prevent accurate number counting.
- Fixed issue where parsed date range was not rendered with '--date-spec'.
- Fixed issue where parser would stop regardless of a valid '--num-test' value.
- Fixed issue where restoring from disk would increment 'MAX.TS'.
- Fixed possible incremental issue when log rotation occurs.
- Fixed possible XSS when getting real-time data into the HTML report.
- Fixed potential memory leak when failing to get root node.
- Fixed real-time hits count issue for certain scenarios.
- Fixed segfault in 'Docker' due to a bad allocation when generating FIFOs.
- Fixed 'Unknown' Operating Systems with 'W3C' format.
- Removed unnecessary include from parser.c so it builds in macOS.
- Updated each panel overall UI to be more streamlined.
- Updated French translation.
- Updated German translation.
- Updated Spanish translation.
- Updated sigsegv handler.

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4-0
- Added a caching storage mechanism to improve parsing raw data and data
  rendering.
- Added a mechanism to avoid counting duplicate data when restoring persisted
  data from disk.
- Added additional option to the HTML report to set a maximum number of items
  per page to 3.
- Added a list of podcast-related user agents under '%%sysconfdir%%'.
- Added 'Android 10' to the list of Android codenames.
- Added a 'widescreen' layout to the HTML report (e.g., 4K TV/KPI Dashboard).
- Added 'Beaker', 'Brave', and 'Firefox Focus' to the list of browsers
- Added command line option --user-name=username to avoid running GoAccess as
  root when outputting a real-time report.
- Added 'DuckDuckGo' and 'MSNBot' browsers to the browsers.list.
- Added 'facebookexternalhit' to the default crawler list.
- Added German translation (DE).
- Added Kubernetes Nginx Ingress Log Format to the default config file.
- Added 'macOS Catalina' to the list of OSX codenames.
- Added minor CSS updates to HTML report.
- Added missing header '<sys/socket.h>' to fix FreeBSD build
- Added new 'Edg' token to the list of browsers.
- Added '--no-ip-validation' command line to disable client IP validation
- Added '--persist' and '--restore' options to persist to disk and restore a
  dump from disk.
- Added Portuguese translation (pt-BR)
- Added Swedish translation (SV)
- Added the ability to parse server cache status and a new panel to display
  those metrics.
- Changed accumulated time to work by default on '--persist' and '--restore'.
- Changed back how the hits and visitors percentage is calculated to be more
  intuitive.
- Changed Geo Location panel display default to show only if database file is
  provided ('LIBMAXMINDDB').
- Changed initial processing time from secs to HH:MM:SS in HTML output.
- Changed '--max-items' for the static HTML report to allow no limit on output
  entries.
- Changed required 'gettext' version to 0.19
- Changed to ignore 'SIGPIPE' with 'SIG_IGN'
- Changed version to 10.15 for 'macOS Catalina'.
- Ensure proper escaping on default AWSELB log format.
- Ensure valid requests counter is not affected on duplicate entries when
  restoring data.
- Fixed issue preventing Ctrl-C (SIGINT) for the curses interface to stop the
  program.
- Fixed issue where HTML report wouldn't update the tables when changing per
  page option.
- Fixed issue where it wouldn't find either the user's or global config file.
- Fixed issue where changing the number of items per page in the HTML report
  would not automatically refresh the tables.
- Fixed issue where last updated label was not updated in real-time.
- Fixed issue where overall date range wasn't showing the right start/end parse
  dates.
- Fixed issue where tailing a file could potentially re-parse part of the log.
- Fixed memory leak when fetching country/continent while using 'LIBMAXMINDDB'.
- Fixed several '-Wcast-qual' warnings.
- Fixed unwanted added characters to the HTML output.
- Fixed websocket issue returning a 400 due to request header size.
- Increased 'MAX_LINE_CONF' so a JSON string can be properly parsed from the
  config file.
- Removed deprecated option '--geoip-city-data' from config file.
- Removed unnecessary dependency from snapcraft.yaml.
- Removed Vagrantfile per #1410
- Removed some old browsers from the default curated list.
- Replaced TokyoCabinet storage for a non-dependency in-memory persistent
  storage.
- Updated Dockerfile.

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3-0
- Added ability to store accumulated processing time into DB_GEN_STATS tcb file
  via '--accumulated-time' command line option.
- Added additional Apache status codes to the list.
- Added a few feed readers to the list.
- Added 'Android 8 Oreo' to the list of OSs.
- Added 'Android Pie 9' to the list of OSs.
- Added --anonymize-ip command line option to anonymize ip addresses.
- Added --browsers-file command line option to load a list of crawlers from a
  text file.
- Added byte unit (PiB) to C formatter and refactored code.
- Added byte unit (PiB) to JS formatter.
- Added Chinese translation (i18n).
- Added French translation (i18n).
- Added '%h' date specifier to the allowed date character specifiers.
- Added "HeadlessChrome" to the list of browsers.
- Added --hide-referer command line option to hide referers from report.
- Added HTTP status code 429 (TOO MANY REQUESTS).
- Added IGNORE_LEVEL_PANEL and IGNORE_LEVEL_REQ definitions.
- Added --ignore-referer-report command line option to hide referers from
  output.
- Added Japanese translation (i18n).
- Added macOS 10.14 Mojave to the list of OSs.
- Added "Mastodon" user-agent to the list of crawlers/unix-like.
- Added new fontawesome icons and use angle arrows in HTML paging.
- Added new purple theme to HTML report and default to it.
- Added --no-parsing-spinner command line option to switch off parsing spinner.
- Added .ogv and ogg static file extension (ogg video, Ogg Vorbis audio).
- Added OS X version numbers when outputting with --real-os.
- Added parsing mechanism in an attempt capture more bots and to include
  unspecified bots/crawlers.
- Added --pidfile command line option to the default config file.
- Added Spanish translation (i18n).
- Added SSL support for Docker goaccess build.
- Added support to the WebSocket server for openssl-1.1*.
- Added the ability to show/hide a chart per panel in the HTML report.
- Added transparency to the navigation bar of the HTML report.
- Added "WhatsApp" user-agent to the list of crawlers.
- Changed default db folder so it adds the process id (PID). --db-path is
  required now when using --load-from-disk.
- Changed Dockerfile to build from the current source.
- Changed 'hits' to be right-aligned on TUI.
- Changed to use faster slide animations on HTML report.
- Changed wording from 'Bandwidth' to the proper term 'Tx. Amount'.
- Ensure database filenames used by btree are less predictable.
- Ensure HTML templates, CSS and JS files are minified when outputting report.
- Ensure key phrases from Google are added even when https is used.
- Ensure live report updates data & charts if tab/document has focus.
- Ensure multiple 'Yandex' crawlers are properly parsed.
- Ensure Safari has priority over most crawlers except the ones that are
  known to have it.
- Ensure the request protocol on its own is properly parsed.
- Ensure the right number of tests are performed against the given log.
- Ensure user configuration is parsed first when available.
- Ensure wss:// is used when connecting via HTTPS.
- Ensure XFF parser takes into account escaped braces.
- Fixed a regression where fifo-in/out would fail with ENXIO.
- Fixed a regression where it would return EXIT_FAILURE on an empty log.
- Fixed a (ssh) pipeline problem with fgetline()/fgets() when there is a race
  for data on stdin.
- Fixed broken X-Forwarded-For (XFF) %%~ specifier in certain parsing cases.
- Fixed conf.filenames duplication problem if logs are via pipe.
- Fixed float percent value on JSON/HTML output for locales using decimal comma.
- Fixed issue where it was not possible to establish a Web Socket connection
  when attempting to parse and extract HTTP method.
- Fixed issue where log formats with pipe delimiter were not propely parsed.
- Fixed memory leak after config file path has been set (housekeeping).
- Fixed memory leak when adding host to holder introduced in c052d1ea.
- Fixed possible memory leak when hiding specific referrers.
- Fixed several JS jshint warnings.
- Fixed sudo installs on TravisCI.
- Fixed UNDEFINED time range in HTML report when VISITORS panel was ignored.
- Fixed unnecessary closing span tags from template.
- Fixed use-after-free when two color items were found on color_list.

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
