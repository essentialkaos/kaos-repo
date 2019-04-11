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

################################################################################

%define upstream_name Pygments
%define pypi_subpath  71/2a/2e4e77803a8bd6408a2903340ac498cb0a2181811af7c9ec92cb70b0308a

################################################################################

Summary:           Syntax highlighting engine written in Python
Name:              %{python_base}-pygments
Version:           2.2.0
Release:           1%{?dist}
License:           BSD
Group:             Development/Libraries
URL:               http://pygments.org

Source0:           https://pypi.python.org/packages/%{pypi_subpath}/%{upstream_name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

BuildRequires:     %{python_base}-setuptools %{python_base}-devel %{python_base}-nose

Requires:          %{python_base}

Provides:          %{name} = %{version}-%{release}

################################################################################

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

################################################################################

%prep
%setup -qn Pygments-%{version}

%build
%{__python3} setup.py build
sed -i 's/\r//' LICENSE

%install
rm -rf %{buildroot}

%{__python3} setup.py install --root %{buildroot}

install -dm 755 %{buildroot}%{_mandir}/man1

mv doc/pygmentize.1 %{buildroot}%{_mandir}/man1/pygmentize3.1
mv %{buildroot}%{_bindir}/pygmentize %{buildroot}%{_bindir}/pygmentize3

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE README.rst
%{python3_sitelib}/*
%{_mandir}/man1/pygmentize3.1.gz
%{_bindir}/pygmentize3

################################################################################

%changelog
* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-1
- Updated for compatibility with Python 3.6

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest version

* Fri Sep 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
- Initial build for kaos repo
