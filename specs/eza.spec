################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        A modern alternative to ls
Name:           eza
Version:        0.23.0
Release:        0%{?dist}
Group:          Development/Tools
License:        MIT
URL:            https://eza.rocks

Source0:        https://github.com/eza-community/eza/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/eza-community/eza/releases/download/v%{version}/completions-%{version}.tar.gz
Source2:        https://github.com/eza-community/eza/releases/download/v%{version}/man-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cargo

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
eza is a modern, maintained replacement for the venerable file-listing
command-line program ls that ships with Unix and Linux operating systems, giving
it more features and better defaults. It uses colours to distinguish file types
and metadata. It knows about symlinks, extended attributes, and Git. And it’s
small, fast, and just one single binary.

By deliberately making some decisions differently, eza attempts to be a more
featureful, more user-friendly version of ls.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

tar xzf %{SOURCE1}
tar xzf %{SOURCE2}

%build
cargo build --release --verbose

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 target/release/%{name} %{buildroot}%{_bindir}/

install -pDm 644 target/completions-%{version}/%{name} \
                 %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -pDm 644 target/completions-%{version}/%{name}.fish \
                 %{buildroot}%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
install -pDm 644 target/completions-%{version}/_%{name} \
                 %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

install -pDm 644 target/man-%{version}/%{name}.1 \
                 %{buildroot}%{_mandir}/man1/%{name}.1
install -pDm 644 target/man-%{version}/%{name}_colors-explanation.5 \
                 %{buildroot}%{_mandir}/man5/%{name}_colors-explanation.5
install -pDm 644 target/man-%{version}/%{name}_colors.5 \
                 %{buildroot}%{_mandir}/man5/%{name}_colors.5

ln -s %{name} %{buildroot}%{_bindir}/exa

%check
%if %{?_with_check:1}%{?_without_check:0}
cargo test
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/exa
%{_datadir}/bash-completion/completions/%{name}
%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/eza.*
%{_mandir}/man5/eza_*

################################################################################

%changelog
* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 0.23.0-0
- https://github.com/eza-community/eza/releases/tag/v0.23.0

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 0.20.18-0
- https://github.com/eza-community/eza/releases/tag/v0.20.18

* Wed Sep 11 2024 Anton Novojilov <andy@essentialkaos.com> - 0.19.2-0
- Initial build for kaos repository
