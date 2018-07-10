################################################################################

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

################################################################################

Summary:            A portable x86 assembler which uses Intel-like syntax
Name:               nasm
Version:            2.13.03
Release:            0%{?dist}
License:            BSD
Group:              Development/Languages
URL:                http://www.nasm.us

Source0:            http://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}.tar.bz2
Source1:            http://www.nasm.us/pub/%{name}/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc perl(Env) autoconf asciidoc xmlto

Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

################################################################################

%package rdoff
Summary:            Tools for the RDOFF binary format, sometimes used with NASM
Group:              Development/Languages

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM). These tools
include linker, library manager, loader, and information dump.

################################################################################

%prep
%setup -q

tar xjf %{SOURCE1} --strip-components 1

%build
autoreconf
%configure

%{__make} all %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%{__make} INSTALLROOT=%{buildroot} install install_rdf

%clean
rm -rf %{buildroot}

%post
if [[ -e %{_infodir}/nasm.info.gz ]] ; then
  /sbin/install-info %{_infodir}/nasm.info.gz  %{_infodir}/dir || :
fi

%preun
if [[ $1 = 0 -a -e %{_infodir}/nasm.info.gz ]] ; then
  /sbin/install-info --delete %{_infodir}/nasm.info.gz %{_infodir}/dir || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES README TODO
%{_bindir}/nasm
%{_bindir}/ndisasm
%{_mandir}/man1/nasm*
%{_mandir}/man1/ndisasm*

%files rdoff
%defattr(-,root,root,-)
%{_bindir}/ldrdf
%{_bindir}/rdf2bin
%{_bindir}/rdf2ihx
%{_bindir}/rdf2com
%{_bindir}/rdfdump
%{_bindir}/rdflib
%{_bindir}/rdx
%{_bindir}/rdf2ith
%{_bindir}/rdf2srec
%{_mandir}/man1/rd*
%{_mandir}/man1/ld*

################################################################################

%changelog
* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 2.13.03-0
- Initial build for kaos-repo
