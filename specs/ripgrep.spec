################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         A search tool that combines the usability of ag with the raw speed of grep
Name:            ripgrep
Version:         11.0.1
Release:         0%{?dist}
Group:           Applications/Text
License:         MIT or Unlicense
URL:             https://github.com/BurntSushi/ripgrep

Source0:         https://github.com/BurntSushi/%{name}/archive/%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   cargo asciidoc libxslt-devel libxml2 docbook-style-xsl

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
ripgrep is a line oriented search tool that combines the usability of
The Silver Searcher (similar to ack) with the raw speed of GNU grep.

ripgrep works by recursively searching your current directory for a
regex pattern.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
cargo build --release --verbose

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_datadir}/bash-completion/completions

install -pm 755 target/release/rg %{buildroot}%{_bindir}/
install -pm 644 $(find target -name "rg.1" | head -1) \
                %{buildroot}%{_mandir}/man1/

install -pm 644 $(find target -name "rg.bash" | head -1) \
                %{buildroot}%{_datadir}/bash-completion/completions/rg

%clean
rm -rf %{buildroot}

%check
%if %{?_with_check:1}%{?_without_check:0}
cargo test
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md CHANGELOG.md COPYING LICENSE-MIT UNLICENSE
%{_bindir}/rg
%{_mandir}/man1/rg.*
%{_datadir}/bash-completion

################################################################################

%changelog
* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.1-0
- Updated to the latest stable release

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.0-0
- Updated to the latest stable release

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- Updated to the latest stable release

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to the latest stable release

* Tue Feb 20 2018 Anton Novojilov <andy@essentialkaos.com> - 0.8.0-0
- Updated to the latest stable release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.1-0
- Updated to the latest stable release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.6.0-0
- Updated to the latest stable release

* Sun Apr 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.5.1-0
- Initial build for kaos repository
