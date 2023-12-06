################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack  %{nil}

################################################################################

%define pkg_name       apache-maven
%define pkg_major_ver  3
%define pkg_homedir    %{_datadir}/%{name}
%define pkg_confdir    %{_sysconfdir}/%{name}

################################################################################

Summary:    Java project management and project comprehension tool
Name:       maven
Version:    3.9.6
Release:    0%{?dist}
Group:      Development/Tools
License:    ASL 2.0 and MIT
URL:        https://maven.apache.org

Source0:    https://mirror.linux-ia64.org/apache/%{name}/%{name}-%{pkg_major_ver}/%{version}/binaries/apache-%{name}-%{version}-bin.tar.gz
Source1:    %{name}-bash-completion

Source100:  checksum.sha512

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   jdk >= 1.8.0
Requires:   %{name}-lib = %{version}-%{release}

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

################################################################################

%package lib
Summary:  Core part of Maven
Group:    Development/Tools

%description lib
Core part of Apache Maven that can be used as a library.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkg_name}-%{version}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/java/%{name}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_datadir}/bash-completion/completions/
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{pkg_homedir}

install -pm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/mvn

cp -rp * %{buildroot}%{pkg_homedir}/

rm -rf %{buildroot}%{pkg_homedir}/lib/jansi-native

# Remove docs from installation dir
rm -f %{buildroot}%{pkg_homedir}/LICENSE
rm -f %{buildroot}%{pkg_homedir}/NOTICE
rm -f %{buildroot}%{pkg_homedir}/README.txt

# Remove Win scripts
rm -f %{buildroot}%{pkg_homedir}/bin/*.cmd

for jarfile in %{buildroot}%{pkg_homedir}/lib/%{name}-*.jar ; do
  jarname=$(basename "$jarfile" .jar)
  ln -sfv %{pkg_homedir}/lib/${jarname}.jar %{buildroot}%{_datadir}/java/%{name}/${jarname}.jar
done

for binfile in %{buildroot}%{pkg_homedir}/bin/* ; do
  binname=$(basename "$binfile")
  ln -sfv %{pkg_homedir}/bin/${binname} %{buildroot}%{_bindir}/${binname}
done

mv %{buildroot}%{pkg_homedir}/bin/m2.conf %{buildroot}%{_sysconfdir}/m2.conf
ln -sf %{_sysconfdir}/m2.conf %{buildroot}%{pkg_homedir}/bin/m2.conf

mv %{buildroot}%{pkg_homedir}/conf/settings.xml %{buildroot}%{_sysconfdir}/%{name}/settings.xml
ln -sf %{_sysconfdir}/%{name}/settings.xml %{buildroot}%{pkg_homedir}/conf/settings.xml

mv %{buildroot}%{pkg_homedir}/conf/logging %{buildroot}%{_sysconfdir}/%{name}/
ln -sf %{_sysconfdir}/%{name}/logging %{buildroot}%{pkg_homedir}/conf/logging

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.txt
%{_bindir}/*
%{_datadir}/bash-completion

%files lib
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/m2.conf
%config(noreplace) %{_sysconfdir}/%{name}/settings.xml
%{_sysconfdir}/%{name}/logging/*
%{_datadir}/java/%{name}/*.jar
%{_sysconfdir}/%{name}
%{pkg_homedir}

################################################################################

%changelog
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 3.9.6-0
- https://maven.apache.org/docs/3.9.6/release-notes.html

* Sun Oct 15 2023 Anton Novojilov <andy@essentialkaos.com> - 3.9.5-0
- https://maven.apache.org/docs/3.9.5/release-notes.html

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 3.6.3-0
- Initial build for kaos-repo
