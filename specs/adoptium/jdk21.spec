################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack %{nil}

################################################################################

%define jdk_major  21.0.5
%define jdk_minor  11
%define jdk_patch  %{nil}

%define install_dir  %{_prefix}/java/%{name}-%{version}
%define jdk_bin_dir  %{install_dir}/bin
%define jdk_man_dir  %{install_dir}/man/man1

%define alt_priority  2153

################################################################################

Summary:      OpenJDK Runtime Environment (JDK 21)
Name:         jdk21
Epoch:        1
Version:      %{jdk_major}
Release:      %{jdk_minor}%{jdk_patch}%{?dist}
Group:        Development/Languages
License:      ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:          https://adoptium.net

Source0:      https://github.com/adoptium/temurin21-binaries/releases/download/jdk-%{jdk_major}+%{jdk_minor}/OpenJDK21U-jdk_x64_linux_hotspot_%{jdk_major}_%{jdk_minor}.tar.gz
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

Provides:     jdk = 1:21
Provides:     jdk-lts = 1:21
Provides:     java = 1:21
Provides:     jdk-%{jdk_major} = 1:%{version}-%{release}
Provides:     jdk-lts-%{jdk_major} = 1:%{version}-%{release}
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

%setup -qn jdk-%{jdk_major}+%{jdk_minor}

%build

%install
rm -rf %{buildroot}

rm -rf demo release

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
* Sat Nov 02 2024 Anton Novojilov <andy@essentialkaos.com> - 21.0.5-11
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-21.0.5+11

* Sat Aug 17 2024 Anton Novojilov <andy@essentialkaos.com> - 21.0.4-7
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-21.0.4+7

* Fri Mar 22 2024 Anton Novojilov <andy@essentialkaos.com> - 21.0.2-13
- https://adoptium.net/en-GB/temurin/release-notes/?version=jdk-21.0.2+13

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 21.0.1-12
- Initial build for kaos repository
