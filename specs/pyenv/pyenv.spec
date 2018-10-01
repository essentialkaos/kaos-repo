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

%define profile_dir       %{_sysconfdir}/profile.d
%define profile           %{profile_dir}/%{name}.sh

################################################################################

Summary:         Simple Python version management utility
Name:            pyenv
Version:         1.2.7
Release:         0%{?dist}
License:         MIT
Group:           Development/Tools
URL:             https://github.com/pyenv/pyenv

Source0:         https://github.com/pyenv/%{name}/archive/v%{version}.tar.gz
Source1:         %{name}.profile

Patch0:          %{name}-default-root.patch
Patch1:          %{name}-hit-prefix-arrow.patch

BuildRequires:   make gcc

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
pyenv lets you easily switch between multiple versions
of Python. Its simple, unobtrusive, and follows the UNIX
tradition of single-purpose tools that do one thing well.

################################################################################

%package plugin-python-build
Summary:         pyenv plugin for installing Python versions
Group:           Development/Tools

Requires:        pyenv

Provides:        %{name} = %{version}-%{release}

%description plugin-python-build
pyenv plugin which provides installation Python to shims directory
from the source codes.

################################################################################

%prep
%setup -qn %{name}-%{version}

%patch0 -p1
%patch1 -p1

%build

pushd src
%configure
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}
install -dm 0755 %{buildroot}%{profile_dir}
install -dm 0755 %{buildroot}%{_bindir}

install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}/versions
install -dm 0755 %{buildroot}%{_loc_prefix}/%{name}/shims

cp -r bin libexec completions LICENSE %{buildroot}%{_loc_prefix}/%{name}/

install -pm 755 %{SOURCE1} %{buildroot}%{profile}

ln -sf %{_loc_prefix}/%{name}/libexec/%{name} %{buildroot}%{_bindir}/%{name}

pushd plugins/python-build
  PREFIX=%{buildroot}%{_prefix} ./install.sh
popd

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_loc_prefix}/%{name}
%{profile}
%{_bindir}/%{name}

%files plugin-python-build
%defattr(-,root,root,-)
%{_datarootdir}/python-build/
%{_bindir}/%{name}-install
%{_bindir}/%{name}-uninstall
%{_bindir}/python-build

################################################################################

%changelog
* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.7-0
- python-build: Add CPython 3.5.6
- python-build: Add CPython 3.4.9

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.6-0
- python-build: Added CPython 3.6.6
- python-build: Check wget version iff wget is going to be used

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.5-0
- python-build: Add CPython 3.7.0
- python-build: Add micropython 1.9.4
- python-build: Add anaconda[23]-5.2.0
- pyenv: Fix seq(1) is not available on OpenBSD

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.4-0
- python-build: Add CPython 2.7.15
- python-build: Add PyPy 6.0.0
- python-build: Allow overriding HTTP client type based on environment variable
  PYTHON_BUILD_HTTP_CLIENT
- python-build: Use version-specific get-pip.py when installing 2.6 and 3.2
- pyenv: Merge rbenv master
- pyenv: Make pyenv-rehash safer for multiple processes

* Wed Apr 04 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.3-0
- python-build: Add CPython 3.6.5
- python-build: Set openssl PKG_CONFIG_PATH for python 3.7
- python-build: Add ActivePython versions 2.7.14, 3.5.4, 3.6.0
- python-build: Unset PIP_VERSION before invoking get-pip.py as a workaround for
  invalid truth value error

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.2-0
- python-build: Add PyPy3 5.10.1
- python-build: Add CPython 3.5.5
- python-build: Add Anaconda[23]-5.1.0
- python-build: Fix checksum issue for CPython 3.4.8
- python-build: Prevent Anaconda from installing a clear shim
- Fixed python-build plugin installation

* Tue Jan 23 2018 Gleb Goncharov <inbox@gongled.ru> - 1.2.1-0
- Initial build
