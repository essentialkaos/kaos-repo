###############################################################################

%define main_version 2.8
%define patch        2

###############################################################################

Summary:         A small text editor
Name:            nano
Version:         %{main_version}.%{patch}
Release:         0%{?dist}
License:         GPLv3+
Group:           Applications/Editors
URL:             http://www.nano-editor.org

Source:          https://www.nano-editor.org/dist/v%{main_version}/%{name}-%{version}.tar.gz

Patch0:          %{name}-nanorc.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc make automake groff ncurses-devel sed

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
GNU nano is a small and friendly text editor.

###############################################################################

%prep
%setup -q

%patch0 -p1

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

install -dm 0755 %{buildroot}%{_sysconfdir}
install -pm 0644 doc/sample.nanorc %{buildroot}%{_sysconfdir}/nanorc

rm -f %{buildroot}%{_infodir}/dir

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
fi

%preun
if [[ $1 -eq 0 ]] ; then
  if [[ -f %{_infodir}/%{name}.info.gz ]] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir &>/dev/null || :
  fi
fi

###############################################################################

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc doc/sample.nanorc
%config(noreplace) %{_sysconfdir}/nanorc
%{_bindir}/nano
%{_bindir}/rnano
%{_mandir}/man1/nano.1.*
%{_mandir}/man1/rnano.1.*
%{_mandir}/man5/nanorc.5.*
%{_infodir}/nano.info*
%{_datadir}/nano
%{_defaultdocdir}/%{name}/*.html

###############################################################################

%changelog
* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.5-0
- Updated to latest stable release

* Fri Jan 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.4-0
- Initial build for kaos repository
