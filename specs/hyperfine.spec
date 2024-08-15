################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Command-line benchmarking tool
Name:           hyperfine
Version:        1.18.0
Release:        0%{?dist}
Group:          Applications/Text
License:        MIT or Unlicense
URL:            https://github.com/sharkdp/hyperfine

Source0:        https://github.com/sharkdp/%{name}/archive/refs/tags/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cargo

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
A command-line benchmarking tool.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
cargo build --release --verbose

%install
rm -rf %{buildroot}

install -pDm 644 -t %{buildroot}%{_mandir}/man1 doc/%{name}.1

pushd target/release
  install -pDm 755 %{name} %{buildroot}%{_bindir}/%{name}

  install -pDm 644 -t %{buildroot}%{_datadir}/bash-completion/completions \
                      build/%{name}-*/out/%{name}.bash

  install -pDm 644 -t %{buildroot}%{_datadir}/fish/vendor_completions.d \
                      build/%{name}-*/out/%{name}.fish

  install -pDm 644 -t %{buildroot}%{_datadir}/zsh/site-functions \
                      build/%{name}-*/out/_%{name}
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
%doc README.md CHANGELOG.md LICENSE-APACHE LICENSE-MIT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/bash-completion/completions/hyperfine.bash
%{_datadir}/fish/vendor_completions.d/hyperfine.fish
%{_datadir}/zsh/site-functions/_hyperfine

################################################################################

%changelog
* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.18.0-0
- Initial build for kaos repository
