################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define shortname  7za

################################################################################

Summary:        Very high compression ratio file archiver
Name:           p7zip
Version:        16.02
Release:        2%{?dist}
License:        LGPLv2 and (LGPLv2+ or CPL)
Group:          Applications/Archiving
URL:            https://p7zip.sourceforge.net

Source0:        https://downloads.sourceforge.net/project/p7zip/%{name}/%{version}/%{name}_%{version}_src_all.tar.bz2

Source100:      checksum.sha512

Patch0:         CVE-2016-9296.patch
Patch1:         CVE-2017-17969.patch
Patch2:         01-hardening-flags.patch
Patch3:         02-fix-g++-warning.patch
Patch4:         03-gcc10-conversion.patch
Patch5:         04-fix-data-null-pointer.patch
Patch6:         05-fix-out-of-mem.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++

%ifarch %{ix86}
BuildRequires:  nasm
%endif
%ifarch x86_64
BuildRequires:  yasm
%endif

Provides:       %{name} = %{version}-%{release}
Provides:       %{shortname} = %{version}-%{release}

################################################################################

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org.

################################################################################

%package plugins
Summary:  Additional plugins for p7zip
Group:    Applications/Archiving

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}_%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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

%{__make} %{?_smp_mflags} all2 \
    OPTFLAGS="%{optflags}" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/%{name} \
    DEST_MAN=%{_mandir}

%install
rm -rf %{buildroot}

%{__make} install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/%{name} \
    DEST_MAN=%{_mandir}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc docs/*
%{_bindir}/%{shortname}
%dir %{_libexecdir}/%{name}/
%{_libexecdir}/%{name}/%{shortname}
%{_libexecdir}/%{name}/7zCon.sfx
%{_mandir}/man1/%{shortname}.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%defattr(-,root,root,-)
%doc contrib/
%{_bindir}/7z
%{_libexecdir}/%{name}/7z
%{_libexecdir}/%{name}/7z.so
%{_libexecdir}/%{name}/Codecs/*
%{_mandir}/man1/7z.1*

################################################################################

%changelog
* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 16.02-2
- Added various patches

* Wed Nov 22 2017 Anton Novojilov <andy@essentialkaos.com> - 16.02-1
- Moved Rar.so from base package to plugins package

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 16.02-0
- 7-Zip now can extract multivolume ZIP archives (z01, z02, ... , zip)
- Some bugs were fixed

* Fri Apr 08 2016 Anton Novojilov <andy@essentialkaos.com> - 15.14.1-0
- Updated to latest stable release

* Wed Jan 13 2016 Anton Novojilov <andy@essentialkaos.com> - 15.09-0
- Updated to latest stable release

* Tue Apr 08 2014 Anton Novojilov <andy@essentialkaos.com> - 9.20.1-3
- Added patch to prevent deadlock if files are deleted while archiving
- Rewrited spec
