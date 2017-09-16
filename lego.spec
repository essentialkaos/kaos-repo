###############################################################################

# rpmbuilder:gopack    github.com/xenolf/lego

###############################################################################

%define  debug_package %{nil}

###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

###############################################################################

Summary:         Let's Encrypt client
Name:            lego
Version:         0.4.0
Release:         0%{?dist}
Group:           Development/Tools
License:         MIT
URL:             https://github.com/xenolf/lego

Source0:         %{name}-%{version}.tar.bz2

BuildRequires:   golang >= 1.8

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
Let's Encrypt client written in Go

###############################################################################

%prep
%setup -q

%build
export GOPATH=$(pwd)

# Move all sources to src directory
mkdir -p .src ; mv * .src ; mv .src src

pushd src/github.com/xenolf/%{name}
  go build
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}

install -pm 755 src/github.com/xenolf/%{name}/%{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/%{name}

###############################################################################

%changelog
* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.0-0
- CLI: The --http-timeout switch. This allows for an override of the default
  client HTTP timeout.
- lib: The HTTPClient field. This allows for an override of the default HTTP
  timeout for library HTTP requests.
- CLI: The --dns-timeout switch. This allows for an override of the default DNS
  timeout for library DNS requests.
- lib: The DNSTimeout switch. This allows for an override of the default client
  DNS timeout.
- lib: The QueryRegistration function on acme.Client. This performs a POST on
  the client registration's URI and gets the updated registration info.
- lib: The DeleteRegistration function on acme.Client. This deletes the
  registration as currently configured in the client.
- lib: The ObtainCertificateForCSR function on acme.Client. The function allows
  to request a certificate for an already existing CSR.
- CLI: The --csr switch. Allows to use already existing CSRs for certificate
  requests on the command line.
- CLI: The --pem flag. This will change the certificate output so it outputs
  a .pem file concatanating the .key and .crt files together.
- CLI: The --dns-resolvers flag. Allows for users to override the default DNS
  servers used for recursive lookup.
- lib: Added a memcached provider for the HTTP challenge.
- CLI: The --memcached-host flag. This allows to use memcached for challenge
  storage.
- CLI: The --must-staple flag. This enables OCSP must staple in the generated
  CSR.
- lib: The library will now honor entries in your resolv.conf.
- lib: Added a field IssuerCertificate to the CertificateResource struct.
- lib: A new DNS provider for OVH.
- lib: A new DNS provider for DNSMadeEasy.
- lib: A new DNS provider for Linode.
- lib: A new DNS provider for AuroraDNS.
- lib: A new DNS provider for NS1.
- lib: A new DNS provider for Azure DNS.
- lib: A new DNS provider for Rackspace DNS.
- lib: A new DNS provider for Exoscale DNS.
- lib: A new DNS provider for DNSPod.
- lib: Exported the PreCheckDNS field so library users can manage the DNS check
  in tests.
- lib: The library will now skip challenge solving if a valid Authz already
  exists.
- lib: The library will no longer check for auto renewed certificates. This
  has been removed from the spec and is not supported in Boulder.
- lib: Fix a problem with the Route53 provider where it was possible the
  verification was published to a private zone.
- lib: Loading an account from file should fail if a integral part is nil
- lib: Fix a potential issue where the Dyn provider could resolve to an
  incorrect zone.
- lib: If a registration encounteres a conflict, the old registration is
  now recovered.
- CLI: The account.json file no longer has the executable flag set.
- lib: Made the client registration more robust in case of a 403 HTTP response.
- lib: Fixed an issue with zone lookups when they have a CNAME in another zone.
- lib: Fixed the lookup for the authoritative zone for Google Cloud.
- lib: Fixed a race condition in the nonce store.
- lib: The Google Cloud provider now removes old entries before trying to add
  new ones.
- lib: Fixed a condition where we could stall due to an early error condition.
- lib: Fixed an issue where Authz object could end up in an active state after
  an error condition.

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 0.3.1-0
- lib: A new DNS provider for Vultr.
- lib: DNS Provider for DigitalOcean could not handle subdomains properly.
- lib: handleHTTPError should only try to JSON decode error messages with the
  right content type.
- lib: The propagation checker for the DNS challenge would not retry on
  send errors.

* Wed Mar 23 2016 Gleb Goncharov <yum@gongled.me> - 0.3.0-0
- Updated to latest release.

* Sun Jan 31 2016 Gleb Goncharov <yum@gongled.me> - 0.2.0-1
- Added certificates path 

* Fri Jan 22 2016 Gleb Goncharov <yum@gongled.me> - 0.2.0-0
- Initial build 
