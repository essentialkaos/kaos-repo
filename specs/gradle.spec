################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack  %{nil}

################################################################################

%define _opt  /opt

################################################################################

Summary:    A powerful build system for the JVM
Name:       gradle
Version:    8.10
Release:    0%{?dist}
License:    ASL 2.0
Group:      Development/Tools
URL:        https://gradle.org

Source0:    https://services.gradle.org/distributions/%{name}-%{version}-bin.zip

Source100:  checksum.sha512

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   java

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
Gradle is a build tool with a focus on build automation and support for
multi-language development. If you are building, testing, publishing, and
deploying software on any platform, Gradle offers a flexible model that can
support the entire development lifecycle from compiling and packaging code
to publishing web sites.

Gradle has been designed to support build automation across multiple languages
and platforms including Java, Scala, Android, C/C++, and Groovy, and is
closely integrated with development tools and continuous integration servers
including Eclipse, IntelliJ, and Jenkins.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_opt}/%{name}/%{version}

cp -rp * %{buildroot}%{_opt}/%{name}/%{version}/
rm -f %{buildroot}%{_opt}/%{name}/bin/*.bat

ln -sf %{_opt}/%{name}/%{version} %{buildroot}%{_opt}/%{name}/current
ln -sf %{_opt}/%{name}/%{version}/bin/%{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_opt}/%{name}

################################################################################

%changelog
* Fri Aug 16 2024 Anton Novojilov <andy@essentialkaos.com> - 8.10-0
- https://docs.gradle.org/8.10/release-notes.html

* Thu Apr 18 2024 Anton Novojilov <andy@essentialkaos.com> - 8.7-0
- https://docs.gradle.org/8.7/release-notes.html

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 8.5-0
- https://docs.gradle.org/8.5/release-notes.html

* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 7.6-0
- https://docs.gradle.org/7.6/release-notes.html

* Sat Jul 11 2020 Anton Novojilov <andy@essentialkaos.com> - 6.5.1-0
- https://docs.gradle.org/6.5.1/release-notes.html

* Mon Dec 16 2019 Anton Novojilov <andy@essentialkaos.com> - 5.6.4-0
- https://docs.gradle.org/5.6.4/release-notes.html

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- https://docs.gradle.org/4.0.1/release-notes.html

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 3.5-0
- https://docs.gradle.org/3.5/release-notes.html

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.4.1-0
- https://docs.gradle.org/3.4.1/release-notes.html

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- https://docs.gradle.org/3.1/release-notes.html

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 3.0-0
- https://docs.gradle.org/3.0/release-notes.html

* Tue Mar 29 2016 Gleb Goncharov <yum@gongled.me> - 2.12-0
- Initial build
