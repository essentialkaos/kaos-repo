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

%define upstream_name Pygments
%define pypy_subpath  b8/67/ab177979be1c81bc99c8d0592ef22d547e70bb4c6815c383286ed5dec504

###############################################################################

Summary:           Syntax highlighting engine written in Python
Name:              python-pygments
Version:           2.1.3
Release:           0%{?dist}
License:           BSD
Group:             Development/Libraries
URL:               http://pygments.org

Source0:           https://pypi.python.org/packages/%{pypy_subpath}/%{upstream_name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

BuildRequires:     python python-setuptools python-nose

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!

###############################################################################

%prep
%setup -qn Pygments-%{version}

%build
%{__python} setup.py build
%{__sed} -i 's/\r//' LICENSE

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install --root %{buildroot}

install -dm 755 %{buildroot}%{_mandir}/man1
mv doc/pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE README.rst
%{python_sitelib}/*
%{_mandir}/man1/pygmentize.1.gz
%{_bindir}/pygmentize

###############################################################################

%changelog
* Fri Sep 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
- Intial build for kaos repo
