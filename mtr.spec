###############################################################################

Summary:              A network diagnostic tool
Name:                 mtr
Version:              0.92
Release:              0%{?dist}
Epoch:                10
License:              GPLv2+
Group:                Applications/Internet
URL:                  http://www.bitwizard.nl/mtr/

Source:               https://github.com/traviscross/mtr/archive/v%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        autoconf automake libtool ncurses-devel

###############################################################################

%description
Mtr is a network diagnostic tool that combines ping and traceroute
into one program.

###############################################################################

%prep
%setup -qn %{name}-%{version}

%build
export CFLAGS="%{optflags} -fPIE"
export LDFLAGS="-z now -pie"

echo "%{version}" > .tarball-version

autoreconf -fi

%configure --without-gtk
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

install -dm 755 %{buildroot}%{_sysconfdir}/bash_completion.d

ln -sf %{_datadir}/bash-completion/completions/%{name} \
       %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING FORMATS NEWS README SECURITY
%{_sbindir}/%{name}
%{_sbindir}/%{name}-packet
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/%{name}
%{_sysconfdir}/bash_completion.d/%{name}

###############################################################################

%changelog
* Wed Oct 04 2017 Anton Novojilov <andy@essentialkaos.com> - 0.92-0
- Initial build for kaos repository
