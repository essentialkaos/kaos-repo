################################################################################

# perfecto:target el8 el9

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global nodejs_sitelib  %{_prefix}/lib/node_modules

################################################################################

Summary:    Fast, reliable, and secure dependency management
Name:       yarn
Version:    1.22.21
Release:    0%{?dist}
License:    BSD
Group:      Development/Tools
URL:        https://yarnpkg.com

Source0:    https://github.com/yarnpkg/yarn/releases/download/v%{version}/yarn-v%{version}.tar.gz

Source100:  checksum.sha512

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   nodejs

Provides:   %{name} = %{version}-%{release}
Provides:   yarnpkg = %{version}-%{release}

################################################################################

%description
Fast: Yarn caches every package it has downloaded, so it never needs to download
the same package again. It also does almost everything concurrently to maximize
resource utilization. This means even faster installs.

Reliable: Using a detailed but concise lockfile format and a deterministic
algorithm for install operations, Yarn is able to guarantee that any
installation that works on one system will work exactly the same on another
system.

Secure: Yarn uses checksums to verify the integrity of every installed package
before its code is executed.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-v%{version}

%build
%install
rm -rf %{buildroot}

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{nodejs_sitelib}/%{name}

cp -pr package.json lib bin %{buildroot}%{nodejs_sitelib}/%{name}

rm -f %{buildroot}%{nodejs_sitelib}/%{name}/bin/*.cmd

ln -sf %{_prefix}/lib/node_modules/%{name}/bin/%{name}.js %{buildroot}%{_bindir}/%{name}
ln -sf %{_prefix}/lib/node_modules/%{name}/bin/%{name}.js %{buildroot}%{_bindir}/yarnpkg

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{nodejs_sitelib}/%{name}
%{_bindir}/%{name}
%{_bindir}/yarnpkg

################################################################################

%changelog
* Thu Feb 22 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.21-0
- https://github.com/yarnpkg/yarn/releases/tag/v1.22.21

* Tue Jan 14 2020 Andrey Kulikov <a.kulikov@fun-box.ru> - 1.21.1-0
- Initial build
