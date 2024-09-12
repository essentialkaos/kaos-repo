################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack  %{nil}

################################################################################

%define jdk_major  422
%define jdk_minor  b05
%define jdk_patch  %{nil}

%define install_dir  %{_prefix}/java/%{name}-%{version}
%define jdk_bin_dir  %{install_dir}/bin
%define jdk_man_dir  %{install_dir}/man/man1

%define alt_priority  817

################################################################################

Summary:      OpenJDK Runtime Environment (JRE 8)
Name:         jre8
Epoch:        1
Version:      1.8.0.%{jdk_major}
Release:      %{jdk_minor}%{jdk_patch}%{?dist}
Group:        Development/Languages
License:      ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:          https://adoptium.net

Source0:      https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u%{jdk_major}-%{jdk_minor}/OpenJDK8U-jre_x64_linux_hotspot_8u%{jdk_major}%{jdk_minor}.tar.gz
Source1:      java.sh

Source100:    checksum.sha512

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Conflicts:    java-1.6.0-openjdk-headless
Conflicts:    java-1.7.0-openjdk-headless
Conflicts:    java-1.8.0-openjdk-headless
Conflicts:    java-11-openjdk-headless
Conflicts:    java-17-openjdk-headless
Conflicts:    java-21-openjdk-headless

AutoProv:     no
AutoReqProv:  no

Provides:     jre = 1:1.8.0
Provides:     jre-lts = 1:1.8.0
Provides:     java = 1:1.8.0
Provides:     jre-1.8.0 = 1:%{version}-%{release}
Provides:     jre-lts-1.8.0 = 1:%{version}-%{release}
Provides:     java-1.8.0 = 1:%{version}-%{release}

Provides:     %{name} = %{version}-%{release}

################################################################################

%description
Java™ is the world's leading programming language and platform. The Adoptium
Working Group promotes and supports high-quality, TCK certified runtimes and
associated technology for use across the Java™ ecosystem.

################################################################################

%prep
%{crc_check}

%setup -qn jdk8u%{jdk_major}-%{jdk_minor}-jre

%build

%install
rm -rf %{buildroot}

rm -rf release

mkdir -p %{buildroot}%{install_dir}
cp -a * %{buildroot}%{install_dir}/

install -pm 644 %{SOURCE1} %{buildroot}%{install_dir}/

%clean
rm -rf %{buildroot}

%post
deps="%{_bindir}/java java %{jdk_bin_dir}/java %{alt_priority}"

for bin in $(ls -1 %{jdk_bin_dir}) ; do
  deps="$deps --slave %{_bindir}/$bin $bin %{jdk_bin_dir}/$bin"
done

for doc in $(ls -1 %{jdk_man_dir}) ; do
  deps="$deps --slave %{_mandir}/man1/$doc $doc %{jdk_man_dir}/$doc"
done

deps="$deps --slave %{_sysconfdir}/profile.d/java.sh java-profile %{install_dir}/java.sh"

%{_sbindir}/update-alternatives --install $deps

%preun
%{_sbindir}/update-alternatives --remove java %{jdk_bin_dir}/java

################################################################################

%files
%defattr(-, root, root, -)
%doc ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README
%{install_dir}

################################################################################

%changelog
* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.422-b05
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk8u422-b05

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.402-b06
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk8u402-b06

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.392-b08
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk8u392-b08

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.372-b07
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk8u372-b07

* Fri Dec 02 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.352-b08
- Updated to the latest version

* Wed Aug 17 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.345-b01
- Updated to the latest version

* Tue Jun 28 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.332-b09
- Updated to the latest version

* Tue Feb 15 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.322-b06
- Updated to the latest version

* Wed Nov 10 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.312-b07
- Updated to the latest version

* Fri Sep 03 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.302-b08.1
- Updated to the latest version

* Wed Jul 14 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.292-b10
- Updated to the latest version

* Fri Jan 29 2021 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.282-b08
- Updated to the latest version

* Sat Dec 12 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.275-b01
- Updated to the latest version

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.272-b10
- Updated to the latest version

* Mon Aug 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.265.b01-0
- Updated to the latest version

* Sun May 24 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.252.b09-0
- Updated to the latest version

* Sat Feb 22 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.242.b08-0
- Updated to the latest version

* Sat Feb 22 2020 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.232.b09-1
- Fixed bug with removing previous version from alternatives

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.232.b09-0
- Updated to the latest version

* Thu Aug 08 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.222.b10-0
- Updated to the latest version

* Sun Jul 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.212.b04-0
- Initial build for kaos repository
