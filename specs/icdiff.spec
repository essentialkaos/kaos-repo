################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%if 0%{?rhel} == 7
%global python_base  python36
%global __python3    %{_bindir}/python3.6
%endif

%if 0%{?rhel} == 8
%global python_base  python38
%global __python3    %{_bindir}/python3.8
%endif

%if 0%{?rhel} == 9
%global python_base  python3
%global __python3    %{_bindir}/python3
%endif

%global python_ver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(plat_specific=True)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

Summary:           Improved colored diff
Name:              icdiff
Version:           2.0.5
Release:           0%{?dist}
License:           Python 2.6.2
Group:             Development/Tools
URL:               https://www.jefftk.com/icdiff

Source0:           https://github.com/jeffkaufman/%{name}/archive/release-%{version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          %{python_base}-setuptools

BuildRequires:     %{python_base}-devel %{python_base}-setuptools

Provides:          %{name} = %{version}-%{release}

################################################################################

%description

Improved colored diff.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-release-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc LICENSE ChangeLog README.md
%exclude %{python3_sitelib}/__pycache__
%{python3_sitelib}/%{name}*
%{_bindir}/git-%{name}
%{_bindir}/%{name}

################################################################################

%changelog
* Sat Dec 10 2022 Anton Novojilov <andy@essentialkaos.com> - 2.0.5-0
- Set process exit code to indicate differences
- Support -P/--permissions option

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.5-0
- Error handling: unknown encoding
- pipes: stop printing an error when pipes close
- git-icdiff: start search for pager in icdiff.pager
- fix: fix the unknown option 'default' error when call git config
- feat: show the real file name when displaying git diff result
- fix FIRST_TIME_CHECK_GIT_DIFF
- options parsing: fall back to 80 columns on errors, and clean things up

* Sun Jan 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- Allow {path} and {basename} in --label
- Properly implement git difftool protocol

* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- Add --exclude-lines (-E) which can exclude comments
- Add --color-map so you can choose which colors to use for what
- Allow highlighted characters to be bold
- Support configuring git-icdiff with gitconfig
- Don't choke on bad terminal sizes
- Print proper error messages instead of raising exceptions
- Allow the line numbers to be colorized
- Add a LICENSE file

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- Handle files with CR characters better and add --strip-trailing-cr

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- Fix setup.py by symlinking icdiff to icdiff.py

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- Updated remaining copy of unicode test file (b/1)

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- Updated unicode test file (input-3)
- Allow testing installed version
- Allow importing as a module
- Minor deduplication tweak to git-icdiff
- Add pip instructions to readme
- Allow using --tabsize
- Allow non-recursive directory diffing

* Fri Sep 25 2015 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- Initial release
