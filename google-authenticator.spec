########################################################################################

Summary:         One-time passcode support using open standards
Name:            google-authenticator
Version:         1.02
Release:         0%{?dist}
License:         ASL 2.0
Group:           Development/Tools
URL:             https://github.com/google/google-authenticator

Source0:         https://github.com/google/%{name}/archive/%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc libtool m4 pam-devel

Provides:        %{name} = %{version}-%{release}

########################################################################################

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

########################################################################################

%prep
%setup -q

%build
cd libpam
./bootstrap.sh
%{configure}
%{__make} CFLAGS="${CFLAGS:-%optflags}" LDFLAGS=-ldl %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}/%{_lib}/security

cd libpam

install -pm 755 .libs/pam_google_authenticator.so \
                %{buildroot}/%{_lib}/security/pam_google_authenticator.so

install -pm 755 %{name} %{buildroot}%{_bindir}/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

########################################################################################

%files
%defattr(-,root,root,-)
%doc libpam/FILEFORMAT libpam/README.md libpam/totp.html
/%{_lib}/security/*.so
%{_bindir}/%{name}

########################################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.02-0
- Updated to latest stable release

* Wed May 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.01-0
- Initial build
