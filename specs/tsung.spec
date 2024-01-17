################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Name:           tsung
Summary:        A distributed multi-protocol load testing tool
Version:        1.8.0
Release:        0%{?dist}
Group:          Development/Tools
License:        GPLv2
URL:            https://github.com/processone/tsung

Source0:        https://github.com/processone/tsung/archive/refs/tags/v1.8.0.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  erlang >= 21 make

Requires:       erlang >= 21 perl(Template)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
tsung is a distributed load testing tool. It is protocol-independent and can
currently be used to stress and benchmark HTTP, Jabber/XMPP, PostgreSQL,
MySQL and LDAP servers.
It simulates user behaviour using an XML description file, reports many
measurements in real time (statistics can be customized with transactions,
and graphics generated using gnuplot).
For HTTP, it supports 1.0 and 1.1, has a proxy mode to record sessions,
supports GET and POST methods, Cookies, and Basic WWW-authentication.
It also has support for SSL.

################################################################################

%prep
%{crc_check}

%setup -q

iconv -f ISO-8859-1 -t UTF-8 CONTRIBUTORS > CONTRIBUTORS.new && \
touch -r CONTRIBUTORS CONTRIBUTORS.new && \
mv CONTRIBUTORS.new CONTRIBUTORS
sed -i 's/\r$//' examples/*

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_defaultdocdir}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING TODO
%{_bindir}/%{name}*
%{_bindir}/tsplot
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/tsplot.1*

################################################################################

%changelog
* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- https://github.com/processone/tsung/blob/v1.8.0/CHANGELOG.md

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to latest stable release

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Updated to latest stable release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-1
- Updated group in spec

* Sun May 25 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Updated to latest stable release

* Wed Oct 30 2013 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-5
- Initial build
