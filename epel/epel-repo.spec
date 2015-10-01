##########################################################################

Summary:         Extra Packages for Enterprise Linux repository
Name:            epel-repo
Version:         6.8
Release:         0%{?dist}
License:         GPLv2
Vendor:          ATrpms.net
Group:           System Environment/Base
URL:             http://dl.fedoraproject.org/pub/epel/

Source0:         http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-6
Source1:         GPL
Source2:         epel.repo
Source3:         epel-testing.repo
Source4:         macros.ghc-srpm

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

##########################################################################

%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum and up2date.

##########################################################################

%prep
%setup -qcT
install -pm 644 %{SOURCE1} .

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -dm 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -dm 755 %{buildroot}%{_sysconfdir}/rpm

install -pm 644 %{SOURCE0} \
                %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

install -pm 644 %{SOURCE2} %{SOURCE3} \
                %{buildroot}%{_sysconfdir}/yum.repos.d

install -pm 644 %{SOURCE4} \
                %{buildroot}%{_sysconfdir}/rpm/macros.ghc-srpm

%clean
rm -rf %{buildroot}

##########################################################################

%files
%defattr(-,root,root,-)
%doc GPL
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*
%{_sysconfdir}/rpm/macros.ghc-srpm

##########################################################################

%changelog
* Sun Oct 12 2014 Anton Novojilov <andy@essentialkaos.com> - 6.8-0
- Rebuilt for kaos-repo
