################################################################################

Summary:        Modular Assembler
Name:           yasm
Version:        1.3.0
Release:        0%{?dist}
License:        BSD and (GPLv2+ or Artistic or LGPLv2+) and LGPLv2
Group:          Development/Languages
URL:            http://yasm.tortall.net

Source0:        http://www.tortall.net/projects/%{name}/releases/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc bison byacc xmlto gettext-devel

Provides:       %{name} = %{version}-%{release}
Provides:       bundled(md5-plumb) = %{version}-%{release}

################################################################################

%description
Yasm is a complete rewrite of the NASM assembler under the "new" BSD License
(some portions are under other licenses, see COPYING for details). It is
designed from the ground up to allow for multiple assembler syntaxes to be
supported (eg, NASM, TASM, GAS, etc.) in addition to multiple output object
formats and even multiple instruction sets. Another primary module of the
overall design is an optimizer module.

################################################################################

%package devel
Summary:  Header files and static libraries for the yasm Modular Assembler
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}

Provides:  %{name}-static = %{version}-%{release}
Provides:  bundled(md5-plumb) = %{version}-%{release}

%description devel
Yasm is a complete rewrite of the NASM assembler under the "new" BSD License
(some portions are under other licenses, see COPYING for details). It is
designed from the ground up to allow for multiple assembler syntaxes to be
supported (eg, NASM, TASM, GAS, etc.) in addition to multiple output object
formats and even multiple instruction sets. Another primary module of the
overall design is an optimizer module.
Install this package if you need to rebuild applications that use yasm.

################################################################################

%prep
%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc Artistic.txt AUTHORS BSD.txt COPYING GNU*
%{_bindir}/vsyasm
%{_bindir}/yasm
%{_bindir}/ytasm
%{_mandir}/man1/yasm.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libyasm/
%{_includedir}/libyasm-stdint.h
%{_includedir}/libyasm.h
%{_libdir}/libyasm.a
%{_mandir}/man7/yasm_*.7*

################################################################################

%changelog
* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Initial build for kaos repo
