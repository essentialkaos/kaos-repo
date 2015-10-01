###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __rmdir           %{_bin}/rmdir
%define __ldconfig        %{_sbin}/ldconfig

%define soversion           10
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}
%define multilib_arches     %{ix86} ia64 ppc %{power64} s390 s390x sparcv9 sparc64 x86_64

###############################################################################

Summary:           OpenSSL Toolkit libraries for the "Secure Sockets Layer" (SSL v2/v3)
Name:              openssl
Version:           1.0.1g
Release:           0%{?dist}
License:           Apache-like
Group:             Development/Libraries
URL:               http://www.openssl.org

Source:            http://www.openssl.org/source/%{name}-%{version}.tar.gz
Source1:           hobble-openssl
Source2:           Makefile.certificate
Source6:           make-dummy-cert
Source7:           renew-dummy-cert
Source8:           openssl-thread-test.c
Source9:           opensslconf-new.h
Source10:          opensslconf-new-warning.h
Source11:          README.FIPS

Patch1:            %{name}-1.0.1-beta2-rpmbuild.patch
Patch2:            %{name}-1.0.0f-defaults.patch
Patch4:            %{name}-1.0.0-beta5-enginesdir.patch
Patch5:            %{name}-0.9.8a-no-rpath.patch
Patch6:            %{name}-0.9.8b-test-use-localhost.patch
Patch7:            %{name}-1.0.0-timezone.patch
Patch8:            %{name}-1.0.1c-perlfind.patch
Patch9:            %{name}-1.0.1c-aliasing.patch
Patch10:           %{name}-libcrypto-private-symbols.patch
Patch11:           %{name}-libssl-private-symbols.patch
Patch23:           %{name}-1.0.1c-default-paths.patch
Patch24:           %{name}-1.0.1e-issuer-hash.patch
Patch33:           %{name}-1.0.0-beta4-ca-dir.patch
Patch34:           %{name}-0.9.6-x509.patch
Patch35:           %{name}-0.9.8j-version-add-engines.patch
Patch36:           %{name}-1.0.0e-doc-noeof.patch
Patch39:           %{name}-1.0.1c-ipv6-apps.patch
Patch40:           %{name}-1.0.1e-fips.patch
Patch41:           %{name}-1.0.1e-fips-ec.patch
Patch42:           %{name}-1.0.1e-fips-ctor.patch
Patch43:           %{name}-1.0.1e-new-fips-reqs.patch
Patch45:           %{name}-1.0.1e-env-zlib.patch
Patch47:           %{name}-1.0.0-beta5-readme-warning.patch
Patch49:           %{name}-1.0.1a-algo-doc.patch
Patch50:           %{name}-1.0.1-beta2-dtls1-abi.patch
Patch51:           %{name}-1.0.1-version.patch
Patch56:           %{name}-1.0.0c-rsa-x931.patch
Patch58:           %{name}-1.0.1-beta2-fips-md5-allow.patch
Patch60:           %{name}-1.0.0d-apps-dgst.patch
Patch63:           %{name}-1.0.0d-xmpp-starttls.patch
Patch65:           %{name}-1.0.0e-chil-fixes.patch
Patch66:           %{name}-1.0.1-pkgconfig-krb5.patch
Patch68:           %{name}-1.0.1e-secure-getenv.patch
Patch69:           %{name}-1.0.1c-dh-1024.patch
Patch81:           %{name}-1.0.1-beta2-padlock64.patch
Patch82:           %{name}-1.0.1e-backports.patch
Patch83:           %{name}-1.0.1e-bad-mac.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc coreutils krb5-devel perl sed zlib-devel
BuildRequires:     /usr/bin/rename /usr/bin/cmp

Requires:          coreutils make
Requires:          %{name}-libs = %{version}-%{release}

###############################################################################

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and Open Source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography world-wide. The project
is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its
related documentation.

OpenSSL is based on the excellent SSLeay library developed by Eric A.
Young and Tim J. Hudson. The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get
and use it for commercial and non-commercial purposes subject to some
simple license conditions.

This package contains shared libraries only, install openssl-tools if
you want to use openssl cmdline tool.

###############################################################################

%package libs
Summary:           A general purpose cryptography library with TLS implementation
Group:             System Environment/Libraries
Requires:          ca-certificates >= 2008-5
Obsoletes:         openssl < 1.0.1-0.3.beta3

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

###############################################################################

%package devel
Summary:           Files for development of applications which will use OpenSSL
Group:             Development/Libraries
Requires:          krb5-devel zlib-devel pkgconfig
Requires:          %{name}-libs = %{version}-%{release}

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

###############################################################################

%package static
Summary:           Libraries for static linking of applications which will use OpenSSL
Group:             Development/Libraries
Requires:          %{name}-libs = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

###############################################################################

%package perl
Summary:           Perl scripts provided with OpenSSL
Group:             Applications/Internet
Requires:          perl
Requires:          %{name}-libs = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

###############################################################################

%prep
%setup -q -n %{name}-%{version}

# The hobble_openssl is called here redundantly, just to be sure,
# the tarball has already the sources removed.
%{SOURCE1} > /dev/null

%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .defaults
%patch4 -p1 -b .enginesdir %{?_rawbuild}
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .perlfind %{?_rawbuild}
%patch9 -p1 -b .aliasing
%patch10 -p1 -b .libcrypto-private-symbols.patch
%patch11 -p1 -b .libssl-private-symbols.patch
%patch23 -p1 -b .default-paths
%patch24 -p1 -b .issuer-hash
%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch36 -p1 -b .doc-noeof
%patch39 -p1 -b .ipv6-apps
%patch40 -p1 -b .fips
%patch41 -p1 -b .fips-ec
%patch42 -p1 -b .fips-ctor
%patch43 -p1 -b .new-fips-reqs
%patch45 -p1 -b .env-zlib
%patch47 -p1 -b .warning
%patch49 -p1 -b .algo-doc
%patch50 -p1 -b .dtls1-abi
%patch51 -p1 -b .version
%patch56 -p1 -b .x931
%patch58 -p1 -b .md5-allow
%patch60 -p1 -b .dgst
%patch63 -p1 -b .starttls
%patch65 -p1 -b .chil
%patch66 -p1 -b .krb5
%patch68 -p1 -b .secure-getenv
%patch69 -p1 -b .dh1024
%patch81 -p1 -b .padlock64
%patch82 -p1 -b .backports
%patch83 -p1 -b .bad-mac

%{__sed} -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
%{__perl} util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
%{__touch} Makefile
%{__make} TABLE PERL=%{__perl}

%build

sslarch=%{_os}-%{_target_cpu}

%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
  sslflags="no-asm 386"
fi
%endif

./Configure \
  --prefix=/usr --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
  zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
  enable-cms enable-md2 no-mdc2 no-rc5 no-ec no-ec2m no-ecdh no-ecdsa no-srp \
  --with-krb5-flavor=MIT --enginesdir=%{_libdir}/openssl/engines \
  --with-krb5-dir=/usr shared  ${sslarch} %{?!nofips:fips}

RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"

%{__make} depend all rehash

# Overwrite FIPS README
%{__cp} -f %{SOURCE11} .

# Verify that what was compiled actually works.
%check

# We must revert patch33 before tests otherwise they will fail
%{__patch} -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH

%{__make} -C test apps tests

%{__cc} -o openssl-thread-test \
  `krb5-config --cflags` \
  -I./include \
  $RPM_OPT_FLAGS \
  %{SOURCE8} \
  -L. \
  -lssl -lcrypto \
  `krb5-config --libs` \
  -lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  crypto/fips/fips_standalone_hmac %{buildroot}%{_libdir}/libcrypto.so.%{version} >%{buildroot}%{_libdir}/.libcrypto.so.%{version}.hmac \
  %{__ln} -sf .libcrypto.so.%{version}.hmac %{buildroot}%{_libdir}/.libcrypto.so.%{soversion}.hmac \
  crypto/fips/fips_standalone_hmac %{buildroot}%{_libdir}/libssl.so.%{version} >%{buildroot}%{_libdir}/.libssl.so.%{version}.hmac \
  %{__ln} -sf .libssl.so.%{version}.hmac %{buildroot}%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

%define __provides_exclude_from %{_libdir}/openssl

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}

%{__make} INSTALL_PREFIX=%{buildroot} install
%{__make} INSTALL_PREFIX=%{buildroot} install_docs

%{__mv} %{buildroot}%{_libdir}/engines %{buildroot}%{_libdir}/openssl
%{__mv} %{buildroot}%{_sysconfdir}/pki/tls/man/* %{buildroot}%{_mandir}/

%{__rmdir} %{buildroot}%{_sysconfdir}/pki/tls/man
rename so.%{soversion} so.%{version} %{buildroot}%{_libdir}/*.so.%{soversion}

%{__mkdir} %{buildroot}/%{_lib}

for lib in %{buildroot}%{_libdir}/*.so.%{version} ; do
  %{__chmod} 0755 ${lib}
  %{__ln} -sf `basename ${lib}` %{buildroot}%{_libdir}/`basename ${lib} .%{version}`
  %{__ln} -sf `basename ${lib}` %{buildroot}%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
%{__mkdir_p} %{buildroot}%{_sysconfdir}/pki/tls/certs
%{__install} -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/tls/certs/Makefile
%{__install} -pm 755 %{SOURCE6} %{buildroot}%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{__install} -pm 755 %{SOURCE7} %{buildroot}%{_sysconfdir}/pki/tls/certs/renew-dummy-cert

# Make sure we actually include the headers we built against.
for header in %{buildroot}%{_includedir}/openssl/* ; do
  if [[ -f ${header} && -f include/openssl/$(basename ${header}) ]] ; then
    %{__install} -m 644 include/openssl/`basename ${header}` ${header}
  fi
done

# Rename man pages so that they don't conflict with other system man pages.
pushd %{buildroot}%{_mandir}
  for manpage in man*/* ; do
    if [[ -L ${manpage} ]]; then
      TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
      %{__ln} -snf ${TARGET}ssl ${manpage}ssl
      %{__rm} -f ${manpage}
    else
      %{__mv} ${manpage} ${manpage}ssl
    fi
  done
  for conflict in passwd rand ; do
    rename ${conflict} ssl${conflict} man*/${conflict}*
  done
popd

# Pick a CA script.
pushd %{buildroot}%{_sysconfdir}/pki/tls/misc
  %{__mv} CA.sh CA
popd

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/pki/CA
%{__install} -dm 700 %{buildroot}%{_sysconfdir}/pki/CA/private
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/pki/CA/certs
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/pki/CA/crl
%{__install} -dm 755 %{buildroot}%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
%{__touch} -r %{SOURCE2} %{buildroot}%{_sysconfdir}/pki/tls/openssl.cnf

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
%{__install} -pm 644 %{SOURCE10} \
  %{buildroot}%{_prefix}/include/openssl/opensslconf-%{_arch}.h
%{__cat} %{buildroot}%{_prefix}/include/openssl/opensslconf.h >> \
  %{buildroot}%{_prefix}/include/openssl/opensslconf-%{_arch}.h
%{__install} -pm 644 %{SOURCE9} \
  %{buildroot}%{_prefix}/include/openssl/opensslconf.h
%endif

# Remove unused files from upstream fips support
%{__rm} -rf %{buildroot}%{_bindir}/openssl_fips_fingerprint
%{__rm} -rf %{buildroot}%{_libdir}/fips_premain.*
%{__rm} -rf %{buildroot}%{_libdir}/fipscanister.*

%clean
%{__rm} -rf %{buildroot}

%post libs   -p %{__ldconfig}
%postun libs -p %{__ldconfig}

###############################################################################

%files
%defattr(-,root,root)
%doc FAQ LICENSE CHANGES NEWS INSTALL README
%doc doc/c-indentation.el doc/openssl.txt
%doc doc/openssl_button.html doc/openssl_button.gif
%doc doc/ssleay.txt
%doc README.FIPS
%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{_sysconfdir}/pki/tls/certs/renew-dummy-cert
%{_sysconfdir}/pki/tls/certs/Makefile
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%attr(0755,root,root) %{_bindir}/openssl
%attr(0644,root,root) %{_mandir}/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{_mandir}/man5*/*
%attr(0644,root,root) %{_mandir}/man7*/*

%files libs
%defattr(-,root,root)
%doc LICENSE
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac
%attr(0755,root,root) %{_libdir}/openssl

%files devel
%defattr(-,root,root)
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*.a

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0644,root,root) %{_mandir}/man1*/*.pl*
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

###############################################################################

%changelog
* Tue Apr 08 2014 Anton Novojilov <andy@essentialkaos.com> - 1.0.1g-0
- Updated to latest stable release

* Mon Sep 23 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.1e-0
- Rewrited spec from Fedora
