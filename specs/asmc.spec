################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define commit_sha  916f1e580966e76f25c85e35c24592ae7838dc65

################################################################################

Summary:    Masm compatible assembler
Name:       asmc
Version:    2.36.12
Release:    0%{?dist}
Group:      Development/Tools
License:    GPL
URL:        https://github.com/nidud/asmc

Source0:    https://github.com/nidud/asmc/raw/%{commit_sha}/bin/asmc
Source1:    https://github.com/nidud/asmc/raw/%{commit_sha}/bin/asmc64

Source100:  checksum.sha512

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   %{name} = %{version}-%{release}

################################################################################

%description
Asmc Macro Assembler.

################################################################################

%prep
%{crc_check}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 %{SOURCE0} %{buildroot}%{_bindir}/
install -pm 755 %{SOURCE1} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}64

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 2.36.12-0
- Initial build for kaos repository
