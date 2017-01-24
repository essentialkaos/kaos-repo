###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state

###############################################################################

Summary:            Modular Assembler
Name:               yasm
Version:            1.3.0
Release:            0%{?dist}
License:            BSD and (GPLv2+ or Artistic or LGPLv2+) and LGPLv2
Group:              Development/Languages
URL:                http://yasm.tortall.net

Source0:            http://www.tortall.net/projects/%{name}/releases/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc bison byacc xmlto gettext-devel

Provides:           %{name} = %{version}-%{release} 
Provides:           bundled(md5-plumb) = %{version}-%{release}

###############################################################################

%description
Yasm is a complete rewrite of the NASM assembler under the "new" BSD License
(some portions are under other licenses, see COPYING for details). It is
designed from the ground up to allow for multiple assembler syntaxes to be
supported (eg, NASM, TASM, GAS, etc.) in addition to multiple output object
formats and even multiple instruction sets. Another primary module of the
overall design is an optimizer module.

###############################################################################

%package devel
Summary:            Header files and static libraries for the yasm Modular Assembler
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

Provides:           %{name}-static = %{version}-%{release}
Provides:           bundled(md5-plumb) = %{version}-%{release}

%description devel
Yasm is a complete rewrite of the NASM assembler under the "new" BSD License
(some portions are under other licenses, see COPYING for details). It is
designed from the ground up to allow for multiple assembler syntaxes to be
supported (eg, NASM, TASM, GAS, etc.) in addition to multiple output object
formats and even multiple instruction sets. Another primary module of the
overall design is an optimizer module.
Install this package if you need to rebuild applications that use yasm.

###############################################################################

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

###############################################################################

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

###############################################################################

%changelog
* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Initial build for kaos repo
