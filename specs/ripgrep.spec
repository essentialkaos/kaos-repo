################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Line-oriented search tool
Name:           ripgrep
Version:        14.1.1
Release:        0%{?dist}
Group:          Applications/Text
License:        MIT or Unlicense
URL:            https://github.com/BurntSushi/ripgrep

Source0:        https://github.com/BurntSushi/%{name}/archive/%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cargo asciidoc libxslt-devel libxml2 docbook-style-xsl

Provides:       %{name} = %{version}-%{release}

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
install -dm 755 %{buildroot}%{_datarootdir}/fish/vendor_completions.d
install -dm 755 %{buildroot}%{_datadir}/zsh/site-functions

pushd target/release
  install -pm 755 rg %{buildroot}%{_bindir}/

  ./rg --generate man > %{buildroot}%{_mandir}/man1/rg.1
  ./rg --generate complete-bash > %{buildroot}%{_datadir}/bash-completion/completions/rg
  ./rg --generate complete-fish > %{buildroot}%{_datarootdir}/fish/vendor_completions.d/rg.fish
  ./rg --generate complete-zsh > %{buildroot}%{_datadir}/zsh/site-functions/_rg
popd

%check
%if %{?_with_check:1}%{?_without_check:0}
cargo test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md CHANGELOG.md COPYING LICENSE-MIT UNLICENSE
%{_bindir}/rg
%{_mandir}/man1/rg.*
%{_datadir}/bash-completion/completions/rg
%{_datadir}/zsh/site-functions/_rg
%{_datarootdir}/fish/vendor_completions.d/rg.fish

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 14.1.1-0
- https://github.com/BurntSushi/ripgrep/releases/tag/14.1.1

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 14.1.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/14.1.0

* Thu Dec 07 2023 Anton Novojilov <andy@essentialkaos.com> - 14.0.3-0
- https://github.com/BurntSushi/ripgrep/releases/tag/14.0.3

* Sat Oct 01 2022 Anton Novojilov <andy@essentialkaos.com> - 13.0.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/13.0.0

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.1-0
- https://github.com/BurntSushi/ripgrep/releases/tag/11.0.1

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/11.0.0

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 0.10.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/0.10.0

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- https://github.com/BurntSushi/ripgrep/releases/tag/0.8.1

* Tue Feb 20 2018 Anton Novojilov <andy@essentialkaos.com> - 0.8.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/0.8.0

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.1-0
- https://github.com/BurntSushi/ripgrep/releases/tag/0.7.1

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.6.0-0
- https://github.com/BurntSushi/ripgrep/releases/tag/0.6.0

* Sun Apr 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.5.1-0
- Initial build for kaos repository
