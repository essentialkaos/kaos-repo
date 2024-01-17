################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _smp_mflags  -j1

################################################################################

Summary:          A GNU general-purpose parser generator
Name:             bison
Version:          3.8.2
Release:          0%{?dist}
License:          GPLv3+
Group:            Development/Tools
URL:              https://www.gnu.org/software/bison/

Source0:          https://ftp.gnu.org/pub/gnu/bison/bison-%{version}.tar.xz

Source100:        checksum.sha512

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    autoconf m4 >= 1.4 make gcc

Requires:         m4 >= 1.4

Requires(post):   /sbin/install-info
Requires(preun):  /sbin/install-info

Provides:         bundled(gnulib) = %{name}-%{version}
Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you should not have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

If your system will be used for C development, you should install
Bison.

################################################################################

%package devel

Summary:  Library for development using Bison-generated parsers
Group:    Development/Libraries

Provides: bison-static = %{version}-%{release}

%description devel
The bison-devel package contains the -ly library sometimes used by
programs using Bison-generated parsers.  If you are developing programs
using Bison, you might want to link with this library.  This library
is not required by all Bison-generated parsers, but may be employed by
simple programs to supply minimal support for the generated parsers.

################################################################################

%package runtime

Summary:  Runtime support files used by Bison-generated parsers
Group:    Development/Libraries

%description runtime
The bison-runtime package contains files used at runtime by parsers
that Bison generates.  Packages whose binaries contain parsers
generated by Bison should depend on bison-runtime to ensure that
these files are available.  See the Internationalization in the
Bison manual section for more information.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_bindir}/yacc
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_mandir}/man1/yacc*
rm -rf %{buildroot}%{_docdir}/%{name}/examples

%find_lang %{name}
%find_lang %{name}-runtime

gzip -9nf %{buildroot}%{_infodir}/%{name}.info*

%clean
rm -rf %{buildroot}

################################################################################

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_docdir}/%{name}
%{_mandir}/*/%{name}*
%{_datadir}/%{name}
%{_infodir}/%{name}.info*
%{_bindir}/%{name}
%{_datadir}/aclocal/%{name}*.m4

%files -f %{name}-runtime.lang runtime
%defattr(-,root,root)
%doc COPYING
%{_datarootdir}/locale/*/LC_MESSAGES/%{name}-gnulib.mo

%files devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/liby.a

################################################################################

%changelog
* Fri Sep 30 2022 Anton Novojilov <andy@essentialkaos.com> - 3.8.2-0
- Updated to the latest stable release

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 3.5-0
- Updated to the latest stable release

* Thu Dec 12 2019 Anton Novojilov <andy@essentialkaos.com> - 3.4.2-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 3.4.1-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 3.4-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 3.3.2-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 3.3.1-0
- Updated to the latest stable release

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 3.3-0
- Updated to the latest stable release

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 3.2.4-0
- Updated to the latest stable release

* Wed Jan 09 2019 Anton Novojilov <andy@essentialkaos.com> - 3.2.3-0
- Updated to the latest stable release

* Sat Dec 08 2018 Anton Novojilov <andy@essentialkaos.com> - 3.2.2-0
- Updated to the latest stable release

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 3.2.1-0
- Updated to the latest stable release

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 3.1-0
- Updated to the latest stable release

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 3.0.5-0
- Updated to the latest stable release

* Wed Feb 24 2016 Gleb Goncharov <yum@gongled.ru> - 3.0.4-0
- Initial build
