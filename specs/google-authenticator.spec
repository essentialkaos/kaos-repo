################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         One-time passcode support using open standards
Name:            google-authenticator
Version:         1.09
Release:         0%{?dist}
License:         ASL 2.0
Group:           Development/Tools
URL:             https://github.com/google/google-authenticator-libpam

Source0:         https://github.com/google/%{name}-libpam/archive/refs/tags/%{version}.tar.gz

Source100:       checksum.sha512

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc libtool automake pam-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The Google Authenticator package contains a pluggable authentication
module (PAM) which allows login using one-time passcodes conforming to
the open standards developed by the Initiative for Open Authentication
(OATH) (which is unrelated to OAuth).

Passcode generators are available (separately) for several mobile
platforms.

These implementations support the HMAC-Based One-time Password (HOTP)
algorithm specified in RFC 4226 and the Time-based One-time Password
(TOTP) algorithm currently in draft.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-libpam-%{version}

%build
./bootstrap.sh
%{configure}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/security/*.la

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc FILEFORMAT README.md totp.html
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_mandir}/man8/pam_google_authenticator*
%{_libdir}/security/*
%{_docdir}/%{name}/*

################################################################################

%changelog
* Wed Dec 07 2022 Anton Novojilov <andy@essentialkaos.com> - 1.09-0
- Updated to the latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.02-0
- Updated to the latest stable release

* Wed May 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.01-0
- Initial build
