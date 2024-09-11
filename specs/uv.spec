################################################################################

%define checksum  c7c0a6804538e083bcfbc49c2cecf07c5aaf9fc31fdcfb4449c787d3a40c980b

################################################################################

Summary:    An extremely fast Python package installer and resolver
Name:       uv
Version:    0.4.4
Release:    0%{?dist}
Group:      Development/Tools
License:    MIT AND Apache 2.0
URL:        https://github.com/astral-sh/uv

Source0:    https://github.com/astral-sh/uv/releases/download/%{version}/%{name}-x86_64-unknown-linux-gnu.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
An extremely fast Python package installer and resolver, written in Rust.
Designed as a drop-in replacement for common pip and pip-tools workflows.
Highlights:
• Drop-in replacement for common pip, pip-tools, and virtualenv commands.
• 10-100x faster than pip and pip-tools (pip-compile and pip-sync).
• Disk-space efficient, with a global cache for dependency deduplication.
• Installable via curl, pip, pipx, etc. uv is a static binary that can be
installed without Rust or Python.
• Tested at-scale against the top 10,000 PyPI packages.
• Support for macOS, Linux, and Windows.
• Advanced features such as dependency version overrides and alternative
resolution strategies.
• Best-in-class error messages with a conflict-tracking resolver.
• Support for a wide range of advanced pip features, including editable
installs, Git dependencies, direct URL dependencies, local dependencies,
constraints, source distributions, HTML and JSON indexes, and more.

################################################################################

%prep
if [[ $(sha256sum -b %{SOURCE0} | cut -f1 -d' ') != "%{checksum}" ]] ; then
  echo "Invalid source checksum"
  exit 1
fi

%autosetup -n %{name}-x86_64-unknown-linux-gnu

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_datadir}/bash-completion/completions
install -dm 755 %{buildroot}%{_datarootdir}/fish/vendor_completions.d
install -dm 755 %{buildroot}%{_datadir}/zsh/site-functions

install -pm 755 %{name} %{buildroot}%{_bindir}/
install -pm 755 %{name}x %{buildroot}%{_bindir}/

./%{name} --generate-shell-completion bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name}
./%{name} --generate-shell-completion fish > %{buildroot}%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
./%{name} --generate-shell-completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}x
%{_datadir}/bash-completion/completions/%{name}
%{_datarootdir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

################################################################################

%changelog
* Wed Sep 04 2024 Anton Novojilov <andy@essentialkaos.com> - 0.4.4-0
- https://github.com/astral-sh/uv/releases/tag/0.4.4

* Tue Sep 03 2024 Anton Novojilov <andy@essentialkaos.com> - 0.4.3-0
- Initial build for kaos repository
