################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define nghttp2_version  %(pkg-config --modversion libnghttp2 2>/dev/null || echo 0)

################################################################################

Summary:        Utility for getting files from remote servers
Name:           curl
Version:        8.11.1
Release:        0%{?dist}
License:        MIT
Group:          Applications/Internet
URL:            https://curl.haxx.se

Source0:        https://curl.haxx.se/download/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc libidn2-devel krb5-devel python3
BuildRequires:  pkgconfig zlib-devel openldap-devel
BuildRequires:  openssh-clients openssh-server stunnel perl
BuildRequires:  perl(Cwd) perl(Digest::MD5) perl(Exporter) perl(vars)
BuildRequires:  perl(File::Basename) perl(File::Copy) perl(File::Spec)
BuildRequires:  perl(IPC::Open2) perl(MIME::Base64) perl(warnings)
BuildRequires:  perl(strict) perl(Time::Local) perl(Time::HiRes)
BuildRequires:  libpsl-devel libzstd-devel libzstd-devel brotli-devel
BuildRequires:  openssl-devel libnghttp2-devel

Requires:       libnghttp2 >= %{nghttp2_version}
Requires:       libcurl%{?_isa} = %{version}-%{release}
Requires:       %{_sysconfdir}/pki/tls/certs/ca-bundle.crt

Provides:       webclient = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}

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
Summary:   A library for getting files from web servers
Group:     System Environment/Libraries

Requires:  libnghttp2 >= %{nghttp2_version}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, HTTP proxy tunneling and more.

################################################################################

%package -n libcurl-devel
Summary:     Files needed for building applications with libcurl
Group:       Development/Libraries

Requires:   libcurl%{?_isa} = %{version}-%{release}
Requires:   openssl-devel libnghttp2-devel >= %{nghttp2_version}

Provides:   curl-devel = %{version}-%{release}
Provides:   curl-devel%{?_isa} = %{version}-%{release}

Obsoletes:  curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs that use the libcurl library. It contains the API
documentation of the library, too.

################################################################################

%prep
%{crc_check}

%setup -qn curl-%{version}

%build
export CPPFLAGS="$(pkg-config --cflags openssl)"

if [[ -x %{_usr}/kerberos/bin/krb5-config ]] ; then
  KRB5_PREFIX="=%{_usr}/kerberos"
fi

%configure \
        --with-ssl \
        --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
        --enable-symbol-hiding \
        --enable-ipv6 \
        --enable-ldaps \
        --with-gssapi${KRB5_PREFIX} \
        --with-libidn2 \
        --with-nghttp2 \
        --with-brotli \
        --with-zstd \
        --with-libpsl \
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
%doc CHANGES.md README docs/*.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n libcurl
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example
%{_bindir}/curl-config
%{_includedir}/curl/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcurl.pc
%{_mandir}/man3/*
%{_mandir}/man1/curl-config.1*
%{_datadir}/aclocal/libcurl.m4
%exclude %{_libdir}/libcurl.la

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 8.11.1-0
- https://curl.se/ch/8.11.1.html

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 8.11.0-0
- https://curl.se/ch/8.11.0.html

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 8.10.1-0
- https://curl.se/ch/8.10.1.html

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 8.10.0-0
- https://curl.se/ch/8.10.0.html

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 8.9.1-0
- https://curl.se/ch/8.9.1.html

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 8.9.0-0
- https://curl.se/ch/8.9.0.html

* Wed May 29 2024 Anton Novojilov <andy@essentialkaos.com> - 8.8.0-0
- https://curl.se/changes.html#8_8_0

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 8.7.1-0
- https://curl.se/changes.html#8_7_1

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 8.6.0-0
- https://curl.se/changes.html#8_6_0

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.5.0-0
- https://curl.se/changes.html#8_5_0

* Wed Oct 11 2023 Anton Novojilov <andy@essentialkaos.com> - 8.4.0-0
- https://curl.se/changes.html#8_4_0

* Wed Oct 11 2023 Anton Novojilov <andy@essentialkaos.com> - 8.3.0-0
- https://curl.se/changes.html#8_3_0

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.2.1-0
- https://curl.se/changes.html#8_2_1

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.2.0-0
- https://curl.se/changes.html#8_2_0

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.1.2-0
- https://curl.se/changes.html#8_1_2

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.1.1-0
- https://curl.se/changes.html#8_1_1

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.1.0-0
- https://curl.se/changes.html#8_1_0

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.0.1-0
- https://curl.se/changes.html#8_0_1

* Wed Sep 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.0.0-0
- https://curl.se/changes.html#8_0_0

* Mon Mar 20 2023 Anton Novojilov <andy@essentialkaos.com> - 7.88.1-0
- https://curl.se/changes.html#7_88_1

* Mon Mar 20 2023 Anton Novojilov <andy@essentialkaos.com> - 7.88.0-0
- https://curl.se/changes.html#7_88_0

* Mon Mar 20 2023 Anton Novojilov <andy@essentialkaos.com> - 7.87.0-0
- https://curl.se/changes.html#7_87_0

* Sat Dec 17 2022 Anton Novojilov <andy@essentialkaos.com> - 7.86.0-0
- https://curl.se/changes.html#7_86_0

* Sat Dec 17 2022 Anton Novojilov <andy@essentialkaos.com> - 7.85.0-0
- https://curl.se/changes.html#7_85_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.84.0-0
- https://curl.se/changes.html#7_84_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.83.1-0
- https://curl.se/changes.html#7_83_1

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.83.0-0
- https://curl.se/changes.html#7_83_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.82.0-0
- https://curl.se/changes.html#7_82_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.81.0-0
- https://curl.se/changes.html#7_81_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.80.0-0
- https://curl.se/changes.html#7_80_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.79.1-0
- https://curl.se/changes.html#7_79_1

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.79.0-0
- https://curl.se/changes.html#7_79_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.78.0-0
- https://curl.se/changes.html#7_78_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.77.0-0
- https://curl.se/changes.html#7_77_0

* Tue Aug 23 2022 Anton Novojilov <andy@essentialkaos.com> - 7.76.1-0
- https://curl.se/changes.html#7_76_1

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.76.0-0
- https://curl.se/changes.html#7_76_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.75.0-0
- https://curl.se/changes.html#7_75_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.74.0-0
- https://curl.se/changes.html#7_74_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.73.0-0
- https://curl.se/changes.html#7_73_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.72.0-0
- https://curl.se/changes.html#7_72_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.71.1-0
- https://curl.se/changes.html#7_71_1

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.71.0-0
- https://curl.se/changes.html#7_71_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.70.0-0
- https://curl.se/changes.html#7_70_0

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.69.1-0
- https://curl.se/changes.html#7_69_1

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 7.69.0-0
- https://curl.se/changes.html#7_69_0

* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.68.0-0
- https://curl.se/changes.html#7_68_0

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.67.0-0
- https://curl.se/changes.html#7_67_0

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 7.66.0-0
- https://curl.se/changes.html#7_66_0

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.3-0
- https://curl.se/changes.html#7_65_3

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.2-0
- https://curl.se/changes.html#7_65_2

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.1-0
- https://curl.se/changes.html#7_65_1

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.65.0-0
- https://curl.se/changes.html#7_65_0

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.1-0
- https://curl.se/changes.html#7_64_1

* Thu Jul 04 2019 Anton Novojilov <andy@essentialkaos.com> - 7.64.0-0
- https://curl.se/changes.html#7_64_0

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 7.63.0-0
- https://curl.se/changes.html#7_63_0

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 7.62.0-0
- https://curl.se/changes.html#7_62_0

* Wed Sep 05 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.1-0
- https://curl.se/changes.html#7_61_1

* Thu Aug 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.61.0-0
- https://curl.se/changes.html#7_61_0

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 7.60.0-0
- https://curl.se/changes.html#7_60_0

* Fri Mar 16 2018 Anton Novojilov <andy@essentialkaos.com> - 7.59.0-0
- https://curl.se/changes.html#7_59_0

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 7.58.0-0
- https://curl.se/changes.html#7_58_0

* Wed Nov 29 2017 Anton Novojilov <andy@essentialkaos.com> - 7.57.0-0
- https://curl.se/changes.html#7_57_0

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.1-0
- https://curl.se/changes.html#7_56_1

* Mon Oct 23 2017 Anton Novojilov <andy@essentialkaos.com> - 7.56.0-0
- https://curl.se/changes.html#7_56_0

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.1-0
- https://curl.se/changes.html#7_55_1

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 7.55.0-0
- https://curl.se/changes.html#7_55_0

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.1-0
- https://curl.se/changes.html#7_54_1

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 7.54.0-0
- https://curl.se/changes.html#7_54_0

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.1-0
- https://curl.se/changes.html#7_53_1

* Tue Mar 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.53.0-0
- https://curl.se/changes.html#7_53_0

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.1-0
- https://curl.se/changes.html#7_52_1

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 7.52.0-0
- https://curl.se/changes.html#7_52_0

* Sat Nov 05 2016 Anton Novojilov <andy@essentialkaos.com> - 7.51.0-0
- https://curl.se/changes.html#7_51_0

* Tue Nov 01 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.3-0
- https://curl.se/changes.html#7_50_3

* Thu Sep 08 2016 Anton Novojilov <andy@essentialkaos.com> - 7.50.2-0
- https://curl.se/changes.html#7_50_2

* Thu Aug 04 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 7.50.1-0
- Initial build
