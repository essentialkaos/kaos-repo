################################################################################

%if 0%{?rhel} >= 7
%global python_base python36
%global __python3   %{_bindir}/python3.6
%else
%global python_base python34
%global __python3   %{_bindir}/python3.4
%endif

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

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

################################################################################

%define pkgname     pip

################################################################################

Summary:            Tool for installing and managing Python packages
Name:               %{python_base}-%{pkgname}
Version:            18.1
Release:            2%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://github.com/pypa/pip

Source0:            https://github.com/pypa/%{pkgname}/archive/%{version}.tar.gz

BuildArch:          noarch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      %{python_base}-setuptools %{python_base}-devel

Requires:           %{python_base}-setuptools %{python_base}-devel

Provides:           pip3 = %{version}-%{release}
Provides:           python3-pip = %{version}-%{release}
Provides:           %{name} = %{version}-%{release}

################################################################################

%description
pip is a tool for installing and managing Python packages, such as those found
in the Python Package Index. It’s a replacement for easy_install.

################################################################################

%prep
%setup -qn %{pkgname}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

rm -rf %{buildroot}%{_bindir}/%{pkgname}-*

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc docs AUTHORS.txt LICENSE.txt MANIFEST.in README.rst
%attr(755, root, root) %{_bindir}/%{pkgname}*
%{python3_sitelib}/%{pkgname}*

################################################################################

%changelog
* Thu Sep 19 2019 Anton Novojilov <andy@essentialkaos.com> - 18.1-2
- Fixed compatibility with the latest version of Python 3 package

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 18.1-1
- Updated for compatibility with Python 3.6

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 18.1-0
- Allow PEP 508 URL requirements to be used as dependencies.
- As a security measure, pip will raise an exception when installing packages
  from PyPI if those packages depend on packages not also hosted on PyPI. In
  the future, PyPI will block uploading packages with such external URL
  dependencies directly.
- Upgrade pyparsing to 2.2.1.
- Allows dist options (–abi, –python-version, –platform, –implementation)
  when installing with –target
- Support passing svn+ssh URLs with a username to pip install -e.
- pip now ensures that the RECORD file is sorted when installing from a wheel
  file.
- Add support for Python 3.7.
- Checkout the correct branch when doing an editable Git install.
- Run self-version-check only on commands that may access the index, instead
  of trying on every run and failing to do so due to missing options.
- Allow a Git ref to be installed over an existing installation.
- Show a better error message when a configuration option has an invalid value.
- Always revalidate cached simple API pages instead of blindly caching
  them for up to 10 minutes.
- Avoid caching self-version-check information when cache is disabled.
- Avoid traceback printing on autocomplete after flags in the CLI.
- Fix incorrect parsing of egg names if pip needs to guess the package name.

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 18.0-0
- Remove the legacy format from pip list.
- Dropped support for Python 3.3.
- Remove support for cleaning up #egg fragment postfixes.
- Remove the shim for the old get-pip.py location.
- Introduce a new --prefer-binary flag, to prefer older wheels over newer
  source packages.
- Improve autocompletion function on file name completion after options which
  have <file>, <dir> or <path> as metavar.
- Add support for installing PEP 518 build dependencies from source.
- Improve status message when upgrade is skipped due to only-if-needed
  strategy.
- Update pip's self-check logic to not use a virtualenv specific file and honor
  cache-dir.
- Remove compiled pyo files for wheel packages.
- Speed up printing of newly installed package versions.
- Restrict install time dependency warnings to directly-dependant packages.
- Warning about the entire package set has resulted in users getting confused
  as to why pip is printing these warnings.
- Improve handling of PEP 518 build requirements: support environment markers
  and extras.
- Remove username/password from log message when using index with basic auth.
- Remove trailing os.sep from PATH directories to avoid false negatives.
- Fix "pip wheel pip" being blocked by the "don't use pip to modify itself"
  check.
- Disable pip's version check (and upgrade message) when installed by
  a different package manager.
- Check for file existence and unlink first when clobbering existing files
  during a wheel install.
- Improve error message to be more specific when no files are found as listed
  in as listed in PKG-INFO.
- Always read pyproject.toml as UTF-8. This fixes Unicode handling on Windows
  and Python 2.
- Fix a crash that occurs when PATH not set, while generating script location
  warning.
- Disallow packages with pyproject.toml files that have an empty build-system
  table.

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 10.0.1-0
- Fix a bug that made get-pip.py unusable on Windows without renaming.
- Fix a TypeError when loading the cache on older versions of Python 2.7.
- Fix and improve error message when EnvironmentError occurs during
  installation.
- A crash when reinstalling from VCS requirements has been fixed.
- Fix PEP 518 support when pip is installed in the user site.

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 10.0.0-0
- Prevent false-positive installation warnings due to incomplete name
  normalizaton.
- Fix issue where installing from Git with a short SHA would fail.
- Accept pre-release versions when checking for conflicts with pip check or pip
  install.
- ioctl(fd, termios.TIOCGWINSZ, ...) needs 8 bytes of data
- Do not warn about script location when installing to the directory containing
  sys.executable. This is the case when 'pip install'ing without activating
  a virtualenv.
- Fix PEP 518 support.
- Don't warn about script locations if --target is specified.

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 9.0.3-0
- Fix an error where the vendored requests was not correctly containing itself
  to only the internal vendored prefix.
- Restore compatibility with 2.6.

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 9.0.1-0
- Correct the deprecation message when not specifying a --format so that it
  uses the correct setting name (format) rather than the incorrect one
  (list_format).
- Fix "pip check" to check all available distributions and not just the
  local ones.
- Fix a crash on non ASCII characters from lsb_release.
- Fix an SyntaxError in an an used module of a vendored dependency.
- Fix UNC paths on Windows.

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 8.1.2-0
- Fix a regression on systems with uninitialized locale.
- Use environment markers to filter packages before determining if a
  required wheel is supported.
- Make glibc parsing for `manylinux1` support more robust for the variety of
  glibc versions found in the wild.
- Update environment marker support to fully support PEP 508 and legacy
  environment markers.
- Always use debug logging to the ``--log`` file.
- Don't attempt to wrap search results for extremely narrow terminal windows.

* Sun Mar 20 2016 Gleb Goncharov <yum@gongled.ru> - 8.1.1-0
- Fix regression with non-ascii requirement files on Python 2 and add support
  for encoding headers in requirement files.
