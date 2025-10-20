################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        A modern approach to programming for the Erlang VM
Name:           elixir
Version:        1.19.0
Release:        0%{?dist}
License:        ASL 2.0 and ERPL
Group:          Development/Tools
URL:            https://elixir-lang.org

Source0:        https://github.com/elixir-lang/elixir/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  erlang26 git

Requires:       erlang >= 26

Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-lang = %{version}-%{release}

################################################################################

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
LC_ALL="en_US.UTF-8" %{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/%{name}/%{version}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man1

install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/

cp -ra bin lib %{buildroot}%{_datadir}/%{name}/%{version}/

rm -f %{buildroot}%{_datadir}/%{name}/%{version}/bin/*.ps1

chmod 0600 %{buildroot}%{_datadir}/%{name}/%{version}/lib/elixir/scripts/*.exs

ln -sf %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}%{_bindir}/

%check
%if %{?_with_check:1}%{?_without_check:0}
LC_ALL="en_US.UTF-8" %{__make} %{?_smp_mflags} test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}
%{_mandir}/man1

################################################################################

%changelog
* Mon Oct 20 2025 Anton Novojilov <andy@essentialkaos.com> - 1.19.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.19.0

* Tue Jun 17 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.18.4

* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.18.3

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.18.2

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 1.18.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.18.1

* Mon Dec 23 2024 Anton Novojilov <andy@essentialkaos.com> - 1.18.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.18.0

* Fri Sep 20 2024 Anton Novojilov <andy@essentialkaos.com> - 1.17.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.17.3

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.17.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.17.2

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.17.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.17.1

* Fri Jun 14 2024 Anton Novojilov <andy@essentialkaos.com> - 1.17.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.17.0

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 1.16.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.16.2

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 1.16.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.16.1

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.16.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.16.0

* Wed Nov 08 2023 Anton Novojilov <andy@essentialkaos.com> - 1.15.7-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.15.7

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.15.6-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.15.6

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.15.5-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.15.5

* Wed Jun 21 2023 Anton Novojilov <andy@essentialkaos.com> - 1.14.5-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.14.5

* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 1.14.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.14.2

* Thu Nov 03 2022 Anton Novojilov <andy@essentialkaos.com> - 1.14.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.14.1

* Thu Nov 03 2022 Anton Novojilov <andy@essentialkaos.com> - 1.14.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.14.0

* Thu Nov 03 2022 Anton Novojilov <andy@essentialkaos.com> - 1.13.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.13.4

* Thu Nov 03 2022 Anton Novojilov <andy@essentialkaos.com> - 1.13.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.13.3

* Thu Nov 03 2022 Anton Novojilov <andy@essentialkaos.com> - 1.13.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.13.2

* Wed Dec 22 2021 Anton Novojilov <andy@essentialkaos.com> - 1.13.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.13.1

* Wed Dec 22 2021 Anton Novojilov <andy@essentialkaos.com> - 1.13.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.13.0

* Thu Sep 30 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.12.3

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.12.2

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.12.1

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.12.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.12.0

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.11.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.11.4

* Wed Jul 21 2021 Anton Novojilov <andy@essentialkaos.com> - 1.11.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.11.3

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.11.2

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.11.1

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.11.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.11.0

* Thu Aug 13 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.10.4

* Thu Aug 13 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.10.3

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.10.2

* Tue Mar 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.10.1

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 1.10.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.10.0

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.9.4

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.9.3

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.9.2

* Thu Aug 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.9.1
- Added CRC check for sources

* Fri Jun 28 2019 Anton Novojilov <andy@essentialkaos.com> - 1.9.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.9.0

* Mon Jun 03 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.8.2

* Wed Feb 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.8.1

* Sat Jan 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.8.0

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.7.4

* Mon Aug 27 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.7.3

* Wed Aug 22 2018 Gleb Goncharov <ggoncharov@fun-box.ru> - 1.7.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.7.2

* Wed Aug 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.7.1

* Wed Aug 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.7.0

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.6-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.6.6

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.5-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.6.5

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.6.4

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.6.1

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.6.0

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.5.3

* Wed Oct 25 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.5.2-1
- Fixed Erlang OTP version dependency

* Thu Oct 05 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.5.2

* Wed Aug 23 2017 Gleb Goncharov <ggoncharov@fun-box.ru> - 1.5.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.5.1

* Wed Aug 23 2017 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.5.0

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.4.5

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.4.4

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.4.3

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.4.2

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.4.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.4.0

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.3.4

* Sun Sep 25 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.3-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.3.3

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.2-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.3.2

* Thu Jun 30 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.3.1-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.3.1

* Wed Jun 22 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.3.0

* Tue Feb 09 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-1
- Fixed broken links to binary files

* Tue Jan 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- https://github.com/elixir-lang/elixir/releases/tag/v1.2.0

* Sun Oct 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.1.1-0
- Initial build
