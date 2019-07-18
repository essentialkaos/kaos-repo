################################################################################

%define __os_install_post %{nil}

################################################################################

%define jdk_major   8u212
%define jdk_minor   b04

%define install_dir %{_prefix}/java/%{name}-%{version}
%define jdk_bin_dir %{install_dir}/bin
%define jdk_man_dir %{install_dir}/man/man1

%define alt_priority 800

################################################################################

Summary:            OpenJDK Runtime Environment (JRE 8)
Name:               jre8
Version:            1.8.0.212.b04
Release:            0%{?dist}
Group:              Development/Languages
License:            ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:                https://adoptopenjdk.net

Source0:            https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk%{jdk_major}-%{jdk_minor}/OpenJDK8U-jre_x64_linux_hotspot_%{jdk_major}%{jdk_minor}.tar.gz
Source1:            java.sh

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Conflicts:          java-1.6.0-openjdk-headless
Conflicts:          java-1.7.0-openjdk-headless
Conflicts:          java-1.8.0-openjdk-headless
Conflicts:          java-11-openjdk-headless

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Java™ is the world's leading programming language and platform. AdoptOpenJDK
uses infrastructure, build and test scripts to produce prebuilt binaries from
OpenJDK™ class libraries and a choice of either the OpenJDK HotSpot or Eclipse
OpenJ9 VM.

All AdoptOpenJDK binaries and scripts are open source licensed and available
for free.

################################################################################

%prep
%setup -qn jdk%{jdk_major}-%{jdk_minor}-jre

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

deps="$deps --slave %{_sysconfdir}/profile.d/java.sh java.sh %{install_dir}/java.sh"

%{_sbindir}/update-alternatives --install $deps

%postun
if [[ $1 -eq 0 ]] ; then
  %{_sbindir}/update-alternatives --remove java %{jdk_bin_dir}/java
fi

################################################################################

%files
%defattr(-, root, root, -)
%doc ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README
%{install_dir}

################################################################################

%changelog
* Sun Jul 14 2019 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.212.b04-0
- Initial build for kaos repository
