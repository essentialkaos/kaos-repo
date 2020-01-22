################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define package_name      jinja2

# Fix for https://github.com/pallets/jinja/issues/653
%global _python_bytecompile_errors_terminate_build 0

################################################################################

Summary:        Sandboxed template engine
Name:           python-jinja2
Version:        2.10.3
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://jinja.pocoo.org

Source0:        https://github.com/pallets/%{package_name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python-devel >= 2.7 python-setuptools

Requires:       python >= 2.7 python-markupsafe

Provides:       %{name} = %{verion}-%{release}
Provides:       python2-jinja2 = %{verion}-%{release}

################################################################################

%description
Jinja is a sandboxed template engine written in pure Python. It
provides a Django-like non-XML syntax and compiles templates into
executable python code. It's basically a combination of Django
templates and python code.

################################################################################

%prep
%{crc_check}

%setup -qn jinja-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 2.10.3-0
- Updated to the latest stable release

* Sun Oct 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.10-1
- Added python-markupsafe package to dependencies

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.10-0
- Updated to the latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.6-0
- Updated to the latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.5-0
- Updated to the latest stable release

* Wed Aug 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Initial build
