###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define shortname         7za

###############################################################################

Summary:           Very high compression ratio file archiver
Name:              p7zip
Version:           16.02
Release:           0%{?dist}
License:           LGPLv2 and (LGPLv2+ or CPL)
Group:             Applications/Archiving
URL:               http://p7zip.sourceforge.net

Source:            %{name}_%{version}_src_all.tar.bz2

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc gcc-c++

%ifarch %{ix86}
BuildRequires:     nasm
%endif
%ifarch x86_64
BuildRequires:     yasm
%endif

Provides:          %{name} = %{version}-%{release}
Provides:          %{shortname} = %{version}-%{release}

###############################################################################

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org.

###############################################################################

%package plugins
Summary:           Additional plugins for p7zip
Group:             Applications/Archiving

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.

###############################################################################

%prep

%setup -qn %{name}_%{version}

%build
mkdir docs

mv DOC/* docs/
mv ChangeLog README TODO docs/

find docs    -type f -exec chmod -x {} \;
find contrib -type f -exec chmod -x {} \;

%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif

%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif

%ifarch ppc ppc64
cp -f makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif

make %{?_smp_mflags} all2 \
    OPTFLAGS="%{optflags}" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/%{name} \
    DEST_MAN=%{_mandir}

%install
rm -rf %{buildroot}

make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/%{name} \
    DEST_MAN=%{_mandir}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc docs/*
%{_bindir}/%{shortname}
%dir %{_libexecdir}/%{name}/
%{_libexecdir}/%{name}/%{shortname}
%{_libexecdir}/%{name}/7zCon.sfx
%{_libexecdir}/%{name}/Codecs/*
%{_mandir}/man1/%{shortname}.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%defattr(-,root,root,-)
%doc contrib/
%{_bindir}/7z
%{_libexecdir}/%{name}/7z
%{_libexecdir}/%{name}/7z.so
%{_mandir}/man1/7z.1*

###############################################################################

%changelog
* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 16.02-0
- Updated to latest stable release

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 15.14.1-0
- Updated to latest stable release

* Wed Jan 13 2016 Anton Novojilov <andy@essentialkaos.com> - 15.09-0
- Updated to latest stable release

* Tue Apr 08 2014 Anton Novojilov <andy@essentialkaos.com> - 9.20.1-3
- Added patch to prevent deadlock if files are deleted while archiving
- Rewrited spec
