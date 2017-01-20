###############################################################################

%define main_version 2.7
%define patch        4

###############################################################################

Summary:         A small text editor
Name:            nano
Version:         %{main_version}.%{patch}
Release:         0%{?dist}
License:         GPLv3+
Group:           Applications/Editors
URL:             http://www.nano-editor.org

Source0:         https://www.nano-editor.org/dist/v%{main_version}/%{name}-%{version}.tar.gz
Source1:         nanorc

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc make automake gettext-devel groff ncurses-devel sed

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

Conflicts:       filesystem < 3

Provides:        %{name} = %{version}-%{release}

###############################################################################

%description
GNU nano is a small and friendly text editor.

###############################################################################

%prep
%setup -q

autoreconf -fiv

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

cp %{SOURCE1} nanorc

install -dm 0755 %{buildroot}%{_sysconfdir}

# Improve default config
sed -e 's/^# set nowrap/set nowrap/' \
    -e 's/^#.*set speller.*$/set speller "hunspell"/' \
    -e 's/^# set linenumbers/set linenumbers/' \
    -e 's/^# set smooth/set smooth/' \
    -e 's/^# set softwrap/set softwrap/' \
    -e 's/^# set tabsize 8/set tabsize 2/' \
    -e 's/^# set titlecolor/set titlecolor/' \
    -e 's/^# set statuscolor/set statuscolor/' \
    -e 's/^# set numbercolor cyan/set numbercolor brightblack/' \
    -e 's/^# include "/include "/' \
    doc/sample.nanorc >> %{buildroot}%{_sysconfdir}/nanorc

chmod 644 %{buildroot}%{_sysconfdir}/nanorc

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
* Fri Jan 20 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7.4-0
- Initial build for kaos repository
