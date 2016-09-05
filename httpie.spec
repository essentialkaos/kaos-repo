###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

Summary:           A Curl-like tool for humans
Name:              httpie
Version:           0.9.6
Release:           0%{?dist}
License:           BSD
Group:             Applications/Internet
URL:               https://github.com/jakubroztocil/httpie

Source0:           https://github.com/jakubroztocil/%{name}/archive/%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          python python-pygments python-argparse
Requires:          python-requests >= 2.3 python-setuptools

BuildRequires:     python python-pygments python-requests >= 2.3
BuildRequires:     python-argparse sed python-setuptools

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
HTTPie is a CLI HTTP utility built out of frustration with existing tools. The
goal is to make CLI interaction with HTTP-based services as human-friendly as
possible.

HTTPie does so by providing an http command that allows for issuing arbitrary
HTTP requests using a simple and natural syntax and displaying colorized
responses.

###############################################################################

%prep
%setup -qn %{name}-%{version}
sed -i '/#!\/usr\/bin\/env/d' %{name}/__main__.py
sed -i 's/Pygments>=1.5/Pygments>=1.1/' setup.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}*
%{_bindir}/http

###############################################################################

%changelog
* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.6-0
- Added Python 3 as a dependency for Homebrew installations to ensure some of
  the newer HTTP features work out of the box for macOS
  users (starting with HTTPie 0.9.4.).
- Added the ability to unset a request header with Header:, and send an
  empty value with Header;.
- Added --default-scheme <URL_SCHEME> to enable things like $ alias
  https='http --default-scheme=https.
- Added -I as a shortcut for --ignore-stdin.
- Added fish shell completion (located in extras/httpie-completion.fish
  in the Github repo).
- Updated requests to 2.10.0 so that SOCKS support can be added via pip
  install requests[socks].
- Changed the default JSON Accept header from application/json to
  application/json, */*.
- Changed the pre-processing of request HTTP headers so that any
  leading and trailing whitespace is removed.

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.4-0
- Added Content-Type of files uploaded in multipart/form-data requests
- Added --ssl=<PROTOCOL> to specify the desired SSL/TLS protocol version
  to use for HTTPS requests.
- Added JSON detection with --json, -j to work around incorrect Content-Type
- Added --all to show intermediate responses such as redirects (with --follow)
- Added --history-print, -P WHAT to specify formatting of intermediate responses
- Added --max-redirects=N (default 30)
- Added -A as short name for --auth-type
- Added -F as short name for --follow
- Removed the implicit_content_type config option (use
  "default_options": ["--form"] instead)
- Redirected stdout doesn't trigger an error anymore when --output FILE is set
- Changed the default --style back to solarized for better support
  of light and dark terminals
- Improved --debug output
- Fixed --session when used with --download
- Fixed --download to trim too long filenames before saving the file
- Fixed the handling of Content-Type with multiple +subtype parts
- Removed the XML formatter as the implementation suffered from multiple issues

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-1
- Fixed deps list

* Thu Mar 31 2016 Gleb Goncharov <yum@gongled.ru> - 0.9.3-0
- Changed the default color --style from solarized to monokai
- Added basic Bash autocomplete support (need to be installed manually)
- Added request details to connection error messages
- Fixed 'requests.packages.urllib3' has no attribute 'disable_warnings'
  errors that occurred in some installations
- Fixed colors and formatting on Windows
- Fixed --auth prompt on Windows

* Tue Jul 29 2014 Anton Novojilov <andy@essentialkaos.com> - 0.8.0-0
- Initial build
