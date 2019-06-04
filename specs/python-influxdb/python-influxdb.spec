################################################################################

%define package_name      influxdb
%define package_altname   influxdb-python

################################################################################

Summary:        InfluxDB-Python is a client for interacting with InfluxDB
Name:           python-influxdb
Version:        5.2.0
Release:        0%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            https://github.com/influxdata/influxdb-python

Source:         https://github.com/influxdata/%{package_altname}/archive/v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools

Requires:       python-dateutil pytz python-requests python-six

Provides:       %{name} = %{verion}-%{release}
Provides:       python2-influxdb = %{verion}-%{release}

################################################################################

%description
%{name} is a client for interacting with InfluxDB - an open-source distributed
time series database.

################################################################################

%prep
%setup -qn %{package_altname}-%{version}

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
* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 5.2.0-0
- Updated to latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 5.0.0-0
- Updated to latest stable release

* Fri Nov 17 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 4.4.1-0
- Initial build

