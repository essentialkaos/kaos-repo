################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%{!?_without_nss: %{!?_with_nss: %define _with_nss --with-nss}}
%{?_with_nss:    %define is_nss_enabled 1}
%{?_without_nss: %define is_nss_enabled 0}

%define is_nss_supported  1
%define use_threads_posix 1

%if 0%{?is_nss_supported} && 0%{?is_nss_enabled}
%define use_nss 1
%define ssl_provider nss
%define ssl_version_req >= 3.14.0
%else
%define use_nss 0
%define ssl_provider openssl
%define ssl_version_req %{nil}
%endif

# Require at least the version of libssh2/c-ares that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%define libssh2_version %(pkg-config --modversion libssh2 2>/dev/null || echo 0)
%define cares_version   %(pkg-config --modversion libcares 2>/dev/null || echo 0)

################################################################################

Summary:           Utility for getting files from remote servers
Name:              curl
Version:           7.76.0
Release:           0%{?dist}
License:           MIT
Group:             Applications/Internet
URL:               https://curl.haxx.se

Source0:           https://curl.haxx.se/download/%{name}-%{version}.tar.bz2

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc libidn-devel krb5-devel
BuildRequires:     pkgconfig zlib-devel openldap-devel
BuildRequires:     libmetalink-devel libssh2-devel >= 1.2 groff
BuildRequires:     openssh-clients openssh-server stunnel perl python
BuildRequires:     perl(Cwd) perl(Digest::MD5) perl(Exporter) perl(vars)
BuildRequires:     perl(File::Basename) perl(File::Copy) perl(File::Spec)
BuildRequires:     perl(IPC::Open2) perl(MIME::Base64) perl(warnings)
BuildRequires:     perl(strict) perl(Time::Local) perl(Time::HiRes)
BuildRequires:     libnghttp2-devel nghttp2 libpsl-devel
BuildRequires:     %{ssl_provider}-devel %{ssl_version_req}

%if ! %{use_threads_posix}
BuildRequires:     c-ares-devel >= 1.6.0
%endif

Requires:          c-ares libmetalink >= 0.1.3 libnghttp2 >= 1.16.0
Requires:          libcurl%{?_isa} = %{version}-%{release}

%if ! %{use_nss}
Requires:          %{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%endif

Provides:          webclient = %{version}-%{release}
Provides:          %{name} = %{version}-%{release}

################################################################################

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks.

################################################################################

%package -n libcurl
Summary:           A library for getting files from web servers
Group:             System Environment/Libraries

%if 0%{?rhel} > 7
BuildRequires:     nss-pem
%endif

Requires:          libssh2%{?_isa} >= %{libssh2_version}
Requires:          libmetalink >= 0.1.3 libnghttp2 >= 1.16.0
Requires:          nss-pem

%if ! %{use_threads_posix}
Requires:          c-ares%{?_isa} >= %{cares_version}
%endif

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, HTTP proxy tunneling and more.

################################################################################

%package -n libcurl-devel
Summary:              Files needed for building applications with libcurl
Group:                Development/Libraries

Requires:             libcurl%{?_isa} = %{version}-%{release}
Requires:             %{ssl_provider}-devel %{ssl_version_req}
Requires:             libssh2-devel

Provides:             curl-devel = %{version}-%{release}
Provides:             curl-devel%{?_isa} = %{version}-%{release}

Obsoletes:            curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs that use the libcurl library. It contains the API
documentation of the library, too.

################################################################################

%prep
%{crc_check}

%setup -qn curl-%{version}

%build
%if ! 0%{?use_nss}
export CPPFLAGS="$(pkg-config --cflags openssl)"
%endif

[ -x %{_usr}/kerberos/bin/krb5-config ] && KRB5_PREFIX="=%{_usr}/kerberos"

%configure \
%if 0%{?use_nss}
        --without-ssl \
        --with-nss \
%else
        --with-ssl \
%endif
        --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
%if 0%{?use_threads_posix}
        --enable-threaded-resolver \
%else
        --enable-ares \
%endif
        --enable-symbol-hiding \
        --enable-ipv6 \
        --enable-ldaps \
        --with-gssapi${KRB5_PREFIX} \
        --with-libidn \
        --with-libmetalink \
        --with-nghttp2 \
        --with-libpsl \
        --with-libssh2 \
        --enable-manual \
        --disable-static

sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

install -dm 0755 %{buildroot}%{_datadir}/aclocal
install -pm 0644 docs/libcurl/libcurl.m4 %{buildroot}%{_datadir}/aclocal

%clean
rm -rf %{buildroot}

%post -n libcurl
/sbin/ldconfig

%postun -n libcurl
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES README*
%doc docs/BUGS.md docs/FAQ docs/FEATURES.md docs/TODO docs/HTTP2.md
%doc docs/HTTP3.md docs/SSL-PROBLEMS.md docs/THANKS docs/KNOWN_BUGS
%doc docs/SECURITY-PROCESS.md docs/BUG-BOUNTY.md docs/TheArtOfHttpScripting.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n libcurl
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CHECKSRC.md docs/CONTRIBUTE.md docs/libcurl/ABI.md docs/CODE_STYLE.md
%doc docs/CIPHERS.md docs/DYNBUF.md docs/ECH.md
%{_bindir}/curl-config
%{_includedir}/curl/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcurl.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4
%exclude %{_libdir}/libcurl.la

################################################################################

%changelog
* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.76.0-0
- Changes: https://curl.se/changes.html#7_76_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.75.0-0
- Changes: https://curl.se/changes.html#7_75_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.74.0-0
- Changes: https://curl.se/changes.html#7_74_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.73.0-0
- Changes: https://curl.se/changes.html#7_73_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.72.0-0
- Changes: https://curl.se/changes.html#7_72_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.71.1-0
- Changes: https://curl.se/changes.html#7_71_1

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.71.0-0
- Changes: https://curl.se/changes.html#7_71_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.70.0-0
- Changes: https://curl.se/changes.html#7_70_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.69.1-0
- Changes: https://curl.se/changes.html#7_69_1

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.69.0-0
- Changes: https://curl.se/changes.html#7_69_0

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.68.0-0
- Changes: https://curl.se/changes.html#7_68_0

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.67.0-0
- Changes: https://curl.se/changes.html#7_67_0

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.66.0-0
- Changes: https://curl.se/changes.html#7_66_0

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.3-0
- Changes: https://curl.se/changes.html#7_65_3

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.2-0
- Changes: https://curl.se/changes.html#7_65_2

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.1-0
- Changes: https://curl.se/changes.html#7_65_1

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.0-0
- Changes: https://curl.se/changes.html#7_65_0

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.1-0
- Changes: https://curl.se/changes.html#7_64_1

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.0-0
- Changes: https://curl.se/changes.html#7_64_0

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 7.63.0-0
- Changes: https://curl.se/changes.html#7_63_0

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 7.62.0-0
- Changes: https://curl.se/changes.html#7_62_0

* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.1-0
- Changes: https://curl.se/changes.html#7_61_1

* Thu Aug 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.0-0
- Changes: https://curl.se/changes.html#7_61_0

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.60.0-0
- Changes: https://curl.se/changes.html#7_60_0

* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 7.59.0-0
- Changes: https://curl.se/changes.html#7_59_0

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 7.58.0-0
- Changes: https://curl.se/changes.html#7_58_0

* Wed Nov 29 2017 Anton Novojilov <andy@essentialkaos.com> - 7.57.0-0
- Changes: https://curl.se/changes.html#7_57_0

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.1-0
- Changes: https://curl.se/changes.html#7_56_1

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.0-0
- Changes: https://curl.se/changes.html#7_56_0

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.1-0
- Changes: https://curl.se/changes.html#7_55_1

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.0-0
- Changes: https://curl.se/changes.html#7_55_0

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.1-0
- Changes: https://curl.se/changes.html#7_54_1

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.0-0
- Changes: https://curl.se/changes.html#7_54_0

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.1-0
- Changes: https://curl.se/changes.html#7_53_1

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.0-0
- Changes: https://curl.se/changes.html#7_53_0

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.1-0
- Changes: https://curl.se/changes.html#7_52_1

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.0-0
- Changes: https://curl.se/changes.html#7_52_0

* Sat Nov 05 2016 Anton Novojilov <andy@essentialkaos.com> - 7.51.0-0
- Changes: https://curl.se/changes.html#7_51_0

* Tue Nov 01 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.3-0
- Changes: https://curl.se/changes.html#7_50_3

* Thu Sep 08 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.2-0
- Changes: https://curl.se/changes.html#7_50_2

* Thu Aug 04 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 7.50.1-0
- Initial build
