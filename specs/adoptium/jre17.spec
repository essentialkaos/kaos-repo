################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack %{nil}

################################################################################

%define jdk_major  17.0.14
%define jdk_minor  7
%define jdk_patch  %{nil}

%define install_dir  %{_prefix}/java/%{name}-%{version}
%define jdk_bin_dir  %{install_dir}/bin
%define jdk_man_dir  %{install_dir}/man/man1

%define alt_priority  1708

################################################################################

Summary:      OpenJDK Runtime Environment (JRE 17)
Name:         jre17
Epoch:        1
Version:      %{jdk_major}
Release:      %{jdk_minor}%{jdk_patch}%{?dist}
Group:        Development/Languages
License:      ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:          https://adoptium.net

Source0:      https://github.com/adoptium/temurin17-binaries/releases/download/jdk-%{jdk_major}+%{jdk_minor}/OpenJDK17U-jre_x64_linux_hotspot_%{jdk_major}_%{jdk_minor}.tar.gz
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

Provides:     jre = 1:17
Provides:     jre-lts = 1:17
Provides:     java = 1:17
Provides:     jre-%{jdk_major} = 1:%{version}-%{release}
Provides:     jre-lts-%{jdk_major} = 1:%{version}-%{release}
Provides:     java-%{jdk_major} = 1:%{version}-%{release}

Provides:     %{name} = %{version}-%{release}

################################################################################

%description
Java™ is the world's leading programming language and platform. The Adoptium
Working Group promotes and supports high-quality, TCK certified runtimes and
associated technology for use across the Java™ ecosystem.

################################################################################

%prep
%{crc_check}

%setup -qn jdk-%{jdk_major}+%{jdk_minor}-jre

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
%{install_dir}

################################################################################

%changelog
* Sat Jan 25 2025 Anton Novojilov <andy@essentialkaos.com> - 17.0.14-7
- https://github.com/adoptium/temurin17-binaries/releases/tag/jdk-17.0.14%2B7

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 17.0.12-7
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-17.0.12+7

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 17.0.10-7
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-17.0.10+7

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 17.0.9-9
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-17.0.9+9

* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 17.0.7-7
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-17.0.7+7

* Fri Dec 02 2022 Anton Novojilov <andy@essentialkaos.com> - 17.0.5-8
- Updated to the latest version

* Fri Sep 30 2022 Anton Novojilov <andy@essentialkaos.com> - 17.0.4.1-1
- Updated to the latest version

* Wed Aug 17 2022 Anton Novojilov <andy@essentialkaos.com> - 17.0.4-8
- Updated to the latest version

* Tue Jun 28 2022 Anton Novojilov <andy@essentialkaos.com> - 17.0.3-7
- Initial build for kaos repository
