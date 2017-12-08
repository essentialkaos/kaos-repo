###############################################################################

Summary:           Improved colored diff
Name:              icdiff
Version:           1.9.1
Release:           0%{?dist}
License:           Python 2.6.2
Group:             Development/Tools
URL:               http://www.jefftk.com/icdiff

Source0:           https://github.com/jeffkaufman/%{name}/archive/release-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch
Requires:          python-setuptools

BuildRequires:     python2-devel python-setuptools

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description

Improved colored diff.

###############################################################################

%prep
%setup -qn %{name}-release-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc ChangeLog README.md
%{python_sitelib}/%{name}*
%{_bindir}/git-%{name}
%{_bindir}/%{name}

###############################################################################

%changelog
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
