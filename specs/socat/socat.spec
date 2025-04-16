################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Bidirectional data relay between two data channels ('netcat++')
Name:           socat
Version:        1.8.0.3
Release:        0%{?dist}
License:        GPLv2
Group:          Applications/Internet
URL:            http://www.dest-unreach.org/socat

Source0:        http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc make openssl-devel readline-devel ncurses-devel
BuildRequires:  autoconf kernel-headers

%if %{?_with_check:1}%{?_without_check:0}
BuildRequires:  net-tools openssl iputils iproute
%endif

Requires:       openssl readline ncurses

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Socat is a relay for bidirectional data transfer between two independent data
channels. Each of these data channels may be a file, pipe, device (serial line
etc. or a pseudo terminal), a socket (UNIX, IP4, IP6 - raw, UDP, TCP), an
SSL socket, proxy CONNECT connection, a file descriptor (stdin etc.), the GNU
line editor (readline), a program, or a combination of two of these.

################################################################################

%prep
%{crc_check}

%setup -q
iconv -f iso8859-1 -t utf-8 CHANGES > CHANGES.utf8
mv CHANGES.utf8 CHANGES

%build
%configure --enable-help \
           --enable-stdio \
           --enable-fdnum \
           --enable-file \
           --enable-creat \
           --enable-gopen \
           --enable-pipe \
           --enable-termios \
           --enable-unix \
           --enable-ip4 \
           --enable-ip6 \
           --enable-rawip \
           --enable-tcp \
           --enable-udp \
           --enable-listen \
           --enable-proxy \
           --enable-exec \
           --enable-system \
           --enable-pty \
           --enable-readline \
           --enable-openssl \
           --enable-sycls \
           --enable-filan \
           --enable-retry \
           --enable-libwrap \
           --enable-fips

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%check
%if %{?_with_check:1}%{?_without_check:0}
sed -i "s/ DTLS1//" -i test.sh
export TERM=ansi
export OD_C=/usr/bin/od
%{__make} test
%endif

################################################################################

%files
%defattr(-,root,root,-)
%doc BUGREPORTS CHANGES DEVELOPMENT EXAMPLES FAQ PORTING
%doc COPYING* README SECURITY
%doc %attr(0644,root,root) *.sh
%{_bindir}/socat-*.sh
%{_bindir}/socat
%{_bindir}/socat1
%{_bindir}/filan
%{_bindir}/procan
%{_mandir}/man1/socat.1*
%{_mandir}/man1/socat1.1*

################################################################################

%changelog
* Wed Apr 16 2025 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.3-0
- http://www.dest-unreach.org/socat/CHANGES

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.8.0.0-0
- http://www.dest-unreach.org/socat/CHANGES

* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 1.7.4.4-0
- Fixed UDP-RECVFROM failures and a couple of other bugs

* Mon Feb 19 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.3.2-3
- Initial build for kaos repository
