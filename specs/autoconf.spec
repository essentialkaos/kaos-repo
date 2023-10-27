################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:        A GNU tool for automatically configuring source code
Name:           autoconf
Version:        2.71
Release:        0%{?dist}
License:        GPLv2+ and GFDL
Group:          Development/Tools
URL:            https://www.gnu.org/software/automake/

Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       m4 perl-interpreter perl(File::Compare)

BuildRequires:  make m4 perl perl-generators perl-macros
BuildRequires:  perl(Data::Dumper) perl(Text::ParseWords)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

################################################################################

%prep
%{crc_check}

%setup -q

%build
export EMACS=%{_bindir}/false

%{configure}
%{make_build}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_infodir}/standards.*

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_infodir}/autoconf.info*
%{_datadir}/autoconf/
%{_mandir}/man1/*
%{_bindir}/*

################################################################################

%changelog
* Sat Jul 08 2023 Anton Novojilov <andy@essentialkaos.com> - 2.71-0
- Initial build for EK repository
