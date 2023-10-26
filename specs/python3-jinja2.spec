################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

%define package_name  jinja2

# Fix for https://github.com/pallets/jinja/issues/653
%global _python_bytecompile_errors_terminate_build  0

################################################################################

Summary:        Sandboxed template engine
Name:           python3-jinja2
Version:        2.10.3
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://jinja.pocoo.org

Source0:        https://github.com/pallets/%{package_name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python3-devel python3-setuptools

Requires:       python3 python3-markupsafe = 2.0.1

Provides:       %{name} = %{version}-%{release}

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
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 2.10.3-0
- Updated to the latest stable release

* Sun Oct 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.10-2
- Added python36-markupsafe package to dependencies

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 2.10-1
- Updated for compatibility with Python 3.6

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 2.10-0
- Updated to latest stable release

* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.6-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.9.5-0
- Updated to latest stable release

* Wed Aug 12 2015 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Initial build
