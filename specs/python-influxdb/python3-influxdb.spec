################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%define package_name      influxdb
%define package_altname   influxdb-python

################################################################################

Summary:        InfluxDB-Python is a client for interacting with InfluxDB
Name:           %{python_base}-influxdb
Version:        5.2.3
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/influxdata/influxdb-python

Source0:        https://github.com/influxdata/%{package_altname}/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  %{python_base}-devel %{python_base}-setuptools

Requires:       %{python_base}-requests %{python_base}-six
Requires:       %{python_base} %{python_base}-dateutil pytz

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
%{name} is a client for interacting with InfluxDB - an open-source distributed
time series database.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_altname}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 5.2.3-0
- Updated to the latest stable release

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-1
- Updated for compatibility with Python 3.6

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-0
- Updated to latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- Updated to latest stable release

* Fri Nov 17 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 4.4.1-0
- Initial build
