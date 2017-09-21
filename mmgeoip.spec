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

########################################################################################

Summary:           MaxMinds data for GeoIP
Name:              MMGeoIP
Version:           1.2
Release:           13%{?dist}
License:           Copyright © 2010 Achillefs Charmpilas
Group:             Applications/Databases
URL:               http://www.maxmind.com/

Source0:           http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip
Source1:           http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
Source2:           http://geolite.maxmind.com/download/geoip/database/GeoIPv6.csv.gz
Source3:           http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.csv.gz

BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:          GeoIP

Provides:          %{name} = %{version}-%{release}

########################################################################################

%description
MaxMinds data for GeoIP

########################################################################################

%package IPV6

Summary:           MaxMinds data for GeoIP (IPV6)
Requires:          GeoIP

%description IPV6
MaxMinds IPV6 data for GeoIP

########################################################################################

%prep
%build

%install
rm -rf %{buildroot}

unzip -o %{SOURCE0}
unzip -o %{SOURCE1}
gzip -dc %{SOURCE2} > GeoIPV6.dat
gzip -dc %{SOURCE3} > GeoLiteCityV6.dat

mv GeoIPCountryWhois.csv GeoIP.dat
mv GeoLiteCity_*/GeoLiteCity-Blocks.csv GeoLiteCity-Blocks.dat
mv GeoLiteCity_*/GeoLiteCity-Location.csv GeoLiteCity-Location.dat

install -dm 755 %{buildroot}%{_loc_datarootdir}/GeoIP

install -pm 755 GeoLiteCity-Blocks.dat %{buildroot}%{_loc_datarootdir}/GeoIP/
install -pm 755 GeoLiteCity-Location.dat %{buildroot}%{_loc_datarootdir}/GeoIP/
install -pm 755 GeoIP.dat %{buildroot}%{_loc_datarootdir}/GeoIP/
install -pm 755 GeoLiteCityV6.dat %{buildroot}%{_loc_datarootdir}/GeoIP/
install -pm 755 GeoIPV6.dat %{buildroot}%{_loc_datarootdir}/GeoIP/

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-, root, root, -)
%{_loc_datarootdir}/GeoIP/GeoLiteCity-Blocks.dat
%{_loc_datarootdir}/GeoIP/GeoLiteCity-Location.dat
%{_loc_datarootdir}/GeoIP/GeoIP.dat

%files IPV6
%defattr(-, root, root, -)
%{_loc_datarootdir}/GeoIP/GeoLiteCityV6.dat
%{_loc_datarootdir}/GeoIP/GeoIPV6.dat

########################################################################################

%changelog
* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-13
- Data updated

* Sun Jul 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-12
- Data updated

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-11
- Data updated

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-10
- Data updated

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-9
- Data updated

* Mon Oct 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2-8
- Data updated

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2-7
- Data updated

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2-6
- Data updated

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2-5
- Data updated

* Wed Feb 24 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2-4
- Data updated

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2-3
- Data updated

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2-2
- Data updated

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 1.2-1
- Data updated

* Sat Dec 27 2014 Anton Novojilov <andy@essentialkaos.com> - 1.2-0
- Data updated
- New versioning scheme
