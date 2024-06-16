################################################################################

Summary:        The Container Security Platform
Name:           runsc
Version:        20240603
Release:        0%{?dist}
Group:          Development/Tools
License:        MIT
URL:            https://gvisor.dev

Source0:        https://storage.googleapis.com/gvisor/releases/release/%{version}/x86_64/runsc
Source1:        https://storage.googleapis.com/gvisor/releases/release/%{version}/x86_64/containerd-shim-runsc-v1

Source10:       https://storage.googleapis.com/gvisor/releases/release/%{version}/x86_64/runsc.sha512
Source11:       https://storage.googleapis.com/gvisor/releases/release/%{version}/x86_64/containerd-shim-runsc-v1.sha512

Requires:       docker-ce systemd kernel > 4.14.77

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       gvisor = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}

################################################################################

%description
gVisor is an open-source Linux-compatible sandbox that runs anywhere existing
container tooling does. It enables cloud-native container security and
portability. gVisor leverages years of experience isolating production workloads
at Google.

################################################################################

%prep
cp %{SOURCE0} %{SOURCE1} .
sha512sum -c %{SOURCE10} %{SOURCE11}

%build
%install
rm -rf %{buildroot}

install -pDm 755 %{SOURCE0} \
                 %{buildroot}%{_bindir}/runsc
install -pDm 755 %{SOURCE1} \
                 %{buildroot}%{_bindir}/containerd-shim-runsc-v1

%clean
rm -rf %{buildroot}

%post
if [[ $1 -eq 1 ]] ; then
  %{_bindir}/runsc install &>/dev/null || :
  systemctl reload docker &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  systemctl reload docker &>/dev/null || :
fi

%postun
if [[ $1 -ge 1 ]] ; then
  systemctl daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/runsc
%{_bindir}/containerd-shim-runsc-v1

################################################################################

%changelog
* Thu Jun 06 2024 Anton Novojilov <andy@essentialkaos.com> - 20240603-0
- Initial build for kaos-repo
