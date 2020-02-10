## Extra macros ################################################################

%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock

%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include

################################################################################

Summary:           GeoLite2 Country and City Databases
Name:              MMGeoIP
Version:           2.0
Release:           1%{?dist}
License:           CC BY-SA 4.0
Group:             Applications/Databases
URL:               https://www.maxmind.com

Source0:           https://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip
Source1:           https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip

BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          GeoIP

Provides:          %{name} = %{version}-%{release}
Provides:          GeoLite2 = %{version}-%{release}

################################################################################

%description
GeoLite2 databases are free IP geolocation databases comparable to, but less
accurate than, MaxMind’s GeoIP2 databases.

################################################################################

%prep
%build

%install
rm -rf %{buildroot}

unzip -o %{SOURCE0}
unzip -o %{SOURCE1}

install -dm 755 %{buildroot}%{_loc_datarootdir}/GeoIP

mv GeoLite2-City-*/*.csv .
mv GeoLite2-Country-*/*.csv .
mv GeoLite2-City-*/*.txt .

find . -name '*.csv' -exec rename .csv .dat {} +

chmod 644 *.dat
chmod 644 *.txt

cp -rp *.dat %{buildroot}%{_loc_datarootdir}/GeoIP/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc COPYRIGHT.txt LICENSE.txt README.txt
%{_loc_datarootdir}/GeoIP/GeoLite2-Country-*.dat
%{_loc_datarootdir}/GeoIP/GeoLite2-City-*.dat

################################################################################

%changelog
* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0-1
- Data updated

* Thu May 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0-0
- Switched to GeoLite2 data source

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2-19
- Data updated

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2-18
- Data updated

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2-17
- Data updated

* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2-16
- Data updated

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2-15
- Data updated

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-14
- Data updated

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-13
- Data updated

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-12
- Data updated
