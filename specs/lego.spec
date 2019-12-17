################################################################################

# rpmbuilder:gopack    github.com/go-acme/lego
# rpmbuilder:tag       v3.2.0

################################################################################

%define  debug_package %{nil}

################################################################################

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

################################################################################

Summary:         Let's Encrypt client
Name:            lego
Version:         3.2.0
Release:         0%{?dist}
Group:           Development/Tools
License:         MIT
URL:             https://github.com/go-acme/lego

Source0:         %{name}-%{version}.tar.bz2

BuildRequires:   golang >= 1.13

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Let's Encrypt client written in Go.

################################################################################

%prep
%setup -q

%build
export GOPATH=$(pwd)

# Move all sources to src directory
mkdir -p .src ; mv * .src ; mv .src src

export PATH="$GOPATH/bin:$PATH"

pushd src/github.com/go-acme/%{name}
  go build -v -ldflags '-X "main.version=%{version}"' -o dist/lego ./cmd/lego/
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}

install -pm 755 src/github.com/go-acme/%{name}/dist/%{name} \
                %{buildroot}%{_bindir}/

%clean
# Fix permissions for files and directories in modules dir
find pkg -type d -exec chmod 0755 {} \;
find pkg -type f -exec chmod 0644 {} \;

rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/%{name}

################################################################################

%changelog
* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 3.2.0-0
- [dnsprovider] Add support for autodns
- [dnsprovider] httpreq: Allow use environment vars from a _FILE file
- [lib] Don't deactivate valid authorizations
- [lib] Expose more SOA fields found by dns01.FindZoneByFqdn
- [dnsprovider] use token as unique ID

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 3.1.0-0
- [dnsprovider] Add DNS provider for Liquid Web
- [dnsprovider] cloudflare: add support for API tokens
- [cli] feat: ease operation behind proxy servers
- [dnsprovider] cloudflare: update client
- [dnsprovider] linodev4: propagation timeout configuration
- [dnsprovider] ovh: fix int overflow
- [dnsprovider] bindman: fix client version

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 3.0.2-0
- migrate to go module
- update DNS clients

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- [dnsprovider] Add support for Joker.com DMAPI
- [dnsprovider] Add support for Bindman DNS provider
- [dnsprovider] Add support for EasyDNS
- [lib] Get an existing certificate by URL
- [dnsprovider] digitalocean: LEGO_EXPERIMENTAL_CNAME_SUPPORT support
- [dnsprovider] gcloud: Use fqdn to get zone Present/CleanUp
- [dnsprovider] exec: serial behavior
- [dnsprovider] manual: serial behavior.
- [dnsprovider] Strip newlines when reading environment variables from _FILE
  suffixed files.
- [cli] fix: cli disable-cp option.
- [dnsprovider] gcloud: fix zone visibility.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- [cli] Adds renew hook
- [dnsprovider] Adds 'Since' to DNS providers documentation
- [dnsprovider] gcloud: use public DNS zones
- [dnsprovider] route53: enhance documentation.
- [dnsprovider] cloudns: fix TTL and status validation
- [dnsprovider] sakuracloud: supports concurrent update
- [dnsprovider] Disable authz when solve fail.
- Add tzdata to the Docker image.

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.4.0-0
- Migrate from xenolf/lego to go-acme/lego.
- [dnsprovider] Add DNS Provider for Domain Offensive (do.de)
- [dnsprovider] Adds information about '_FILE' suffix.
- [cli,dnsprovider] Add 'manual' provider to the output of dnshelp
- [dnsprovider] hostingde: Use provided ZoneName instead of domain
- [dnsprovider] pdns: fix wildcard with SANs

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- [dnsprovider] Add DNS Provider for ClouDNS.net
- [dnsprovider] Add DNS Provider for Oracle Cloud
- [cli] Adds log when no renewal.
- [dnsprovider,lib] Add a mechanism to wrap a PreCheckFunc
- [dnsprovider] oraclecloud: better way to get private key.
- [dnsprovider] exoscale: update library
- [dnsprovider] OVH: Refresh zone after deleting challenge record
- [dnsprovider] oraclecloud: ttl config and timeout
- [dnsprovider] hostingde: fix client fails if customer has no access
  to dns-groups
- [dnsprovider] vscale: getting sub-domain
- [dnsprovider] selectel: getting sub-domain
- [dnsprovider] vscale: fix TXT records clean up
- [dnsprovider] selectel: fix TXT records clean up

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.2.0-0
- [dnsprovider] Add support for Openstack Designate as a DNS provider
- [dnsprovider] gcloud: Option to specify gcloud service account json by
  env as string
- [experimental feature] Resolve CNAME when creating dns-01 challenge. To
  enable: set LEGO_EXPERIMENTAL_CNAME_SUPPORT to true.
- [cli] Applies Let’s Encrypt’s recommendation about renew. The option --days
  of the command renew has a new default value (30)
- [lib] Uses a jittered exponential backoff
- [cli] CLI and key type.
- [dnsprovider] httpreq: Endpoint with path.
- [dnsprovider] fastdns: Do not overwrite existing TXT records
- Log wildcard domain correctly in validation

* Thu Jul 18 2019 Anton Novojilov <andy@essentialkaos.com> - 2.1.0-0
- [dnsprovider] Add support for zone.ee as a DNS provider.
- [dnsprovider] nifcloud: Change DNS base url.
- [dnsprovider] gcloud: More detailed information about Google Cloud DNS.
- [lib] fix: OCSP, set HTTP client.
- [dnsprovider] alicloud: fix pagination.
- [dnsprovider] namecheap: fix panic

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- [cli,lib] Option to disable the complete propagation Requirement
- [lib,cli] Support non-ascii domain name (punnycode)
- [cli,lib] Add configurable timeout when obtaining certificates
- [cli] Archive revoked certificates
- [cli] Add command to list certificates.
- [cli] support for renew with CSR
- [cli] add SAN on renew
- [lib] Adds Remove for challenges
- [lib] Add version to xenolf-acme in User-Agent.
- [dnsprovider] The ability for a DNS provider to solve the challenge
  sequentially
- [dnsprovider] Add DNS provider for "HTTP request".
- [dnsprovider] Add DNS Provider for Vscale
- [dnsprovider] Add DNS Provider for TransIP
- [dnsprovider] Add DNS Provider for inwx
- [dnsprovider] alidns: add support to handle more than 20 domains
- [lib] Check all challenges in a predictable order
- [lib] Poll authz URL instead of challenge URL
- [lib] Check all nameservers in a predictable order
- [lib] Logs every iteration of waiting for the propagation
- [cli] --http: enable HTTP challenge important
- [cli] --http.port: previously named --http
- [cli] --http.webroot: previously named --webroot
- [cli] --http.memcached-host: previously named --memcached-host
- [cli] --tls: enable TLS challenge important
- [cli] --tls.port: previously named --tls
- [cli] --dns.resolvers: previously named --dns-resolvers
- [dnsprovider] gcloud: Use GCE_PROJECT for project always, if specified
- [cli] the option --days of the command renew has default value (15)
- [lib] Remove SetHTTP01Address
- [lib] Remove SetTLSALPN01Address
- [lib] Remove Exclude
- [cli] Remove --exclude, -x
- [lib] Fixes revocation for subdomains and non-ascii domains
- [lib] Disable pending authorizations
- [dnsprovider] transip: concurrent access to the API.
- [dnsprovider] gcloud: fix for wildcard
- [dnsprovider] Azure: Do not overwrite existing TXT records
- [dnsprovider] fix: Cloudflare error.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- fix: Docker image

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- [dnsprovider] Add DNS Provider for ConoHa DNS
- [dnsprovider] Add DNS Provider for MyDNS.jp
- [dnsprovider] Add DNS Provider for Selectel
- [dnsprovider] netcup: make unmarshalling of api-responses more lenient.
- [dnsprovider] aurora: change DNS client
- [dnsprovider] azure: update auth to support instance metadata service
- [dnsprovider] dnsmadeeasy: log response body on error
- [lib] TLS-ALPN-01: Update idPeAcmeIdentifierV1, draft refs.
- [lib] Do not send a JWS body when POSTing challenges.
- [lib] Support POST-as-GET.

* Fri Nov 16 2018 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- [lib] TLS-ALPN-01 Challenge
- [cli] Add filename parameter
- [dnsprovider] Allow to configure TTL, interval and timeout
- [dnsprovider] Add support for reading DNS provider setup from files
- [dnsprovider] Add DNS Provider for ACME-DNS
- [dnsprovider] Add DNS Provider for ALIYUN DNS
- [dnsprovider] Add DNS Provider for DreamHost
- [dnsprovider] Add DNS provider for hosting.de
- [dnsprovider] Add DNS Provider for IIJ
- [dnsprovider] Add DNS Provider for netcup
- [dnsprovider] Add DNS Provider for NIFCLOUD DNS
- [dnsprovider] Add DNS Provider for SAKURA Cloud
- [dnsprovider] Add DNS Provider for Stackpath
- [dnsprovider] Add DNS Provider for VegaDNS
- [dnsprovider] exec: add EXEC_MODE=RAW support.
- [dnsprovider] cloudflare: support for CF_API_KEY and CF_API_EMAIL
- [lib] Don't trust identifiers order.
- [lib] Fix missing issuer certificates from Let's Encrypt
- [dnsprovider] duckdns: fix TXT record update url
- [dnsprovider] duckdns: fix subsubdomain
- [dnsprovider] gcloud: update findTxtRecords to use Name=fqdn and Type=TXT
- [dnsprovider] lightsail: Fix Domain does not exist error
- [dnsprovider] ns1: use the authoritative zone and not the domain name
- [dnsprovider] ovh: check error to avoid panic due to nil client
- [lib] Submit all dns records up front, then validate serially

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.1-0
- cli: Changed default server URL to new V2 endpoint
- lib: Added missing processing status handling

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- lib: ACME v2 Support.
- dnsprovider: Renamed /providers/dns/googlecloud to /providers/dns/gcloud
- dnsprovider: Modified Google Cloud provider
  gcloud.NewDNSProviderServiceAccount function to extract the project id
  directly from the service account file.
- dnsprovider: Made errors more verbose for the Cloudflare provider.

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.1-0
- lib: A new DNS provider for OTC.
- lib: The AWS_HOSTED_ZONE_ID environment variable for the Route53 DNS
  provider to directly specify the zone.
- lib: The RFC2136_TIMEOUT enviroment variable to make the timeout for
  the RFC2136 provider configurable.
- lib: The GCE_SERVICE_ACCOUNT_FILE environment variable to specify a
  service account file for the Google Cloud DNS provider.
- lib: Fixed an authentication issue with the latest Azure SDK.

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
