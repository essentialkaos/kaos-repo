################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        A cat(1) clone with wings
Name:           bat
Version:        0.24.0
Release:        0%{?dist}
Group:          Applications/Text
License:        MIT and Apache 2.0
URL:            https://github.com/sharkdp/bat

Source0:        https://github.com/sharkdp/%{name}/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cargo

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
A cat(1) clone with wings.

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

install -pm 755 target/release/%{name} %{buildroot}%{_bindir}/

install -pm 644 $(find target/release -name "%{name}.1" | head -1) \
                %{buildroot}%{_mandir}/man1/

install -pm 644 $(find target/release -name "%{name}.bash" | head -1) \
                %{buildroot}%{_datadir}/bash-completion/completions/%{name}

install -pm 644 $(find target/release -name "%{name}.fish" | head -1) \
                %{buildroot}%{_datarootdir}/fish/vendor_completions.d/%{name}.fish

install -pm 644 $(find target/release -name "%{name}.zsh" | head -1) \
                %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%check
%if %{?_with_check:1}%{?_without_check:0}
cargo test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md CONTRIBUTING.md CHANGELOG.md NOTICE LICENSE-APACHE LICENSE-MIT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/bash-completion/completions/%{name}
%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

################################################################################

%changelog
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 0.24.0-0
- https://github.com/sharkdp/bat/releases/tag/v0.24.0

* Sat Oct 01 2022 Anton Novojilov <andy@essentialkaos.com> - 0.22.1-0
- Initial build for kaos repository
