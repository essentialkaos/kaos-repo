################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        Real-time web log analyzer and interactive viewer
Name:           goaccess
Version:        1.9.4
Release:        0%{?dist}
Group:          Development/Tools
License:        GPLv2+
URL:            https://goaccess.io

Source0:        https://tar.goaccess.io/goaccess-%{version}.tar.gz
Source1:        extra-browsers.list
Source100:      checksum.sha512

Patch1:         webkaos-formats.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc libmaxminddb-devel glib2-devel ncurses-devel
BuildRequires:  openssl-devel gettext-devel gettext-devel

Requires:       openssl libmaxminddb

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Open source real-time web log analyzer and interactive viewer that runs
in a terminal in *nix systems. It provides fast and valuable HTTP statistics
for system administrators that require a visual server report on the fly.

################################################################################

%prep
%crc_check
%autosetup -p1

%build
%configure --enable-utf8 \
           --with-openssl \
           --with-getline \
           --enable-geoip=mmdb

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install}

cat %{SOURCE1} >> %{buildroot}%{_sysconfdir}/%{name}/browsers.list

%clean
rm -rf %{buildroot}

############################################################# ###################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md TODO
%config(noreplace) %{_sysconfdir}/%{name}/browsers.list
%config(noreplace) %{_sysconfdir}/%{name}/podcast.list
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/locale/*/LC_MESSAGES/goaccess.mo
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Tue Apr 15 2025 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- https://goaccess.io/release-notes#release-1.9.4

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- https://goaccess.io/release-notes#release-1.9.3

* Wed May 08 2024 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- Added extra user-agents for package managers and status check services

* Thu Apr 18 2024 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- https://goaccess.io/release-notes#release-1.9.2

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- https://goaccess.io/release-notes#release-1.8.1

* Wed Oct 04 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- https://goaccess.io/release-notes#release-1.8

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- https://goaccess.io/release-notes#release-1.7.2

* Wed Feb 22 2023 Anton Novojilov <andy@essentialkaos.com> - 1.7-0
- https://goaccess.io/release-notes#release-1.7

* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6.5-0
- https://goaccess.io/release-notes#release-1.6.5

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6.2-0
- https://goaccess.io/release-notes#release-1.6.2

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://goaccess.io/release-notes#release-1.6.1

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.6-0
- https://goaccess.io/release-notes#release-1.6

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.7-0
- https://goaccess.io/release-notes#release-1.5.7

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.6-0
- https://goaccess.io/release-notes#release-1.5.6

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.5-0
- https://goaccess.io/release-notes#release-1.5.5

* Mon Aug 22 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.4-0
- https://goaccess.io/release-notes#release-1.5.4

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- https://goaccess.io/release-notes#release-1.5.3

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- https://goaccess.io/release-notes#release-1.5.2

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- https://goaccess.io/release-notes#release-1.5.1

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- https://goaccess.io/release-notes#release-1.5

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.6-0
- https://goaccess.io/release-notes#release-1.4.6

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- https://goaccess.io/release-notes#release-1.4.5

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- https://goaccess.io/release-notes#release-1.4.4

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- https://goaccess.io/release-notes#release-1.4.3

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- https://goaccess.io/release-notes#release-1.4.2

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4.1-0
- https://goaccess.io/release-notes#release-1.4.1

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.4-0
- https://goaccess.io/release-notes#release-1.4

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3-0
- https://goaccess.io/release-notes#release-1.3

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.2-0
- https://goaccess.io/release-notes#release-1.2

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- https://goaccess.io/release-notes#release-1.1.1

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.1-0
- https://goaccess.io/release-notes#release-1.1

* Tue Jul 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-0
- https://goaccess.io/release-notes#release-1.0.2

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- https://goaccess.io/release-notes#release-1.0.1

* Fri Jun 17 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0-0
- https://goaccess.io/release-notes#release-1.0

* Wed Mar 09 2016 Gleb Goncharov <yum@gongled.ru> - 0.9.8-0
- https://goaccess.io/release-notes#release-0.9.8

* Tue Dec 29 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.7-0
- https://goaccess.io/release-notes#release-0.9.7

* Tue Oct 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.6-0
- https://goaccess.io/release-notes#release-0.9.6

* Tue Oct 27 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.5-0
- https://goaccess.io/release-notes#release-0.9.5

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.4-0
- https://goaccess.io/release-notes#release-0.9.4

* Fri Sep 04 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- https://goaccess.io/release-notes#release-0.9.3

* Mon Jul 06 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- https://goaccess.io/release-notes#release-0.9.2

* Wed Jul 01 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- https://goaccess.io/release-notes#release-0.9.1

* Thu Mar 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.9-0
- https://goaccess.io/release-notes#release-0.9

* Fri Feb 20 2015 Anton Novojilov <andy@essentialkaos.com> - 0.8.5-0
- Initial build
