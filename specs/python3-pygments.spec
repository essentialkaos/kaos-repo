################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define upstream_name  Pygments
%define pypi_subpath   da/6a/c427c06913204e24de28de5300d3f0e809933f376e0b7df95194b2bb3f71

################################################################################

Summary:        Syntax highlighting engine written in Python
Name:           python3-pygments
Version:        2.14.0
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            https://pygments.org

Source0:        https://pypi.python.org/packages/%{pypi_subpath}/%{upstream_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python3-setuptools python3-devel

Requires:       python3 python3-libs

Provides:       %{name} = %{version}-%{release}

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
%{crc_check}

%setup -qn Pygments-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

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
* Thu Feb 09 2023 Anton Novojilov <andy@essentialkaos.com> - 2.14.0-0
- https://github.com/pygments/pygments/releases/tag/2.14.0

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-1
- Updated for compatibility with Python 3.6

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- Updated to latest version

* Fri Sep 09 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.3-0
- Initial build for kaos repo
