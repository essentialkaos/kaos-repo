################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         A search tool that combines the usability of ag with the raw speed of grep
Name:            ripgrep
Version:         0.7.1
Release:         0%{?dist}
Group:           Applications/Text
License:         MIT or Unlicense
URL:             https://github.com/BurntSushi/ripgrep

Source0:         https://github.com/BurntSushi/%{name}/archive/%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   cargo

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
ripgrep is a line oriented search tool that combines the usability of
The Silver Searcher (similar to ack) with the raw speed of GNU grep.

ripgrep works by recursively searching your current directory for a
regex pattern.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
cargo build --release

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_mandir}/man1
install -dm 755 %{buildroot}%{_datadir}/bash-completion/completions

install -pm 755 target/release/rg %{buildroot}%{_bindir}/
install -pm 644 doc/rg.1 %{buildroot}%{_mandir}/man1/

install -pm 644 target/release/build/ripgrep-*/out/rg.bash-completion \
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
%{_mandir}/man1/rg.1*
%{_datadir}/bash-completion

################################################################################

%changelog
* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.7.1-0
- Updated to latest stable release

* Mon Sep 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.6.0-0
- Updated to latest stable release

* Sun Apr 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.5.1-0
- Initial build for kaos repository
