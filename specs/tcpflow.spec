################################################################################

Summary:              Network traffic recorder
Name:                 tcpflow
Version:              1.5.0
Release:              0%{?dist}
License:              GPLv3
Group:                Development/Tools
URL:                  https://github.com/simsong/tcpflow

Source:               http://digitalcorpora.org/downloads/%{name}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             boost >= 1.53.0 libpcap openssl zlib

BuildRequires:        make gcc-c++ autoconf m4 >= 1.4 openssl-devel cairo-devel
BuildRequires:        boost-devel >= 1.53.0 libpcap-devel zlib-devel

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
tcpflow is a program that captures data transmitted as part of TCP
connections (flows), and stores the data in a way that is convenient for
protocol analysis or debugging. A program like 'tcpdump' shows a summary of
packets seen on the wire, but usually doesn't store the data that's actually
being transmitted. In contrast, tcpflow reconstructs the actual data streams
and stores each flow in a separate file for later analysis.

################################################################################

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} PREFIX=%{buildroot}%{prefix}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

################################################################################

%changelog
* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Updated to latest stable release

* Wed Dec 07 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.4.5-0
- Initial build
