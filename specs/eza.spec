################################################################################

%define checksum  2198529bf8fbabf069dc232f106c2c474e29b9d7571611f64e04299e0899b33b

################################################################################

Summary:    A modern alternative to ls
Name:       eza
Version:    0.19.2
Release:    0%{?dist}
Group:      Development/Tools
License:    MIT
URL:        https://eza.rocks

Source0:    https://github.com/eza-community/eza/releases/download/v%{version}/eza_x86_64-unknown-linux-gnu.tar.gz
Source1:    https://github.com/eza-community/eza/releases/download/v%{version}/completions-%{version}.tar.gz
Source2:    https://github.com/eza-community/eza/releases/download/v%{version}/man-%{version}.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   %{name} = %{version}-%{release}

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
if [[ $(sha256sum -b %{SOURCE0} | cut -f1 -d' ') != "%{checksum}" ]] ; then
  echo "Invalid source checksum"
  exit 1
fi

%autosetup -c

tar xzf %{SOURCE1}
tar xzf %{SOURCE2}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 %{name} %{buildroot}%{_bindir}/

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

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/exa
%{_datadir}/bash-completion/completions/%{name}
%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/*

################################################################################

%changelog
* Wed Sep 11 2024 Anton Novojilov <andy@essentialkaos.com> - 0.19.2-0
- Initial build for kaos repository
