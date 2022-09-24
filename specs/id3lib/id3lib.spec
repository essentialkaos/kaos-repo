################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:            Library for manipulating ID3v1 and ID3v2 tags
Name:               id3lib
Version:            3.8.3
Release:            35%{?dist}
License:            LGPLv2+
Group:              System Environment/Libraries
URL:                https://id3lib.sourceforge.net

Source0:            https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:            %{name}-no_date_footer.hml
Source2:            id3.pc

Source100:          checksum.sha512

Patch0:             %{name}-dox.patch
Patch1:             %{name}-%{version}-autoreconf.patch
Patch2:             %{name}-%{version}-io_helpers-163101.patch
Patch3:             %{name}-%{version}-mkstemp.patch
Patch4:             %{name}-%{version}-includes.patch
Patch5:             %{name}-vbr_buffer_overflow.diff
Patch6:             20-create-manpages.patch
Patch7:             60-fix_make_check.patch
Patch8:             60-%{name}-missing-nullpointer-check.patch
Patch9:             %{name}-%{version}-fix-utf16-stringlists.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc-c++ autoconf automake libtool zlib-devel doxygen

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
This package provides a software library for manipulating ID3v1 and
ID3v2 tags. It provides a convenient interface for software developers
to include standards-compliant ID3v1/2 tagging capabilities in their
applications. Features include identification of valid tags, automatic
size conversions, (re)synchronisation of tag frames, seamless tag
(de)compression, and optional padding facilities. Additionally, it can
tell mp3 header info, like bitrate etc.

################################################################################

%package devel

Summary:            Development tools for the id3lib library
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           zlib-devel

%description devel
This package provides files needed to develop with the id3lib library.

################################################################################

%prep
%{crc_check}

%setup -q

%patch0 -p0
%patch1 -p1 -b .autoreconf
%patch2 -p1 -b .io_helpers-163101
%patch3 -p1 -b .mkstemp
%patch4 -p1 -b .gcc43
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

chmod -x src/*.h src/*.cpp include/id3/*.h

sed -i -e 's/\r//' doc/id3v2.3.0.*
sed -i -e 's|@DOX_DIR_HTML@|%{_docdir}/%{name}-devel-%{version}/api|' doc/index.html.in

iconv -f ISO-8859-1 -t UTF8 ChangeLog > tmp; mv tmp ChangeLog
iconv -f ISO-8859-1 -t UTF8 THANKS > tmp; mv tmp THANKS

sed -i -e "s,HTML_FOOTER.*$,HTML_FOOTER = id3lib-no_date_footer.hml,g" doc/Doxyfile.in

cp %{SOURCE1} doc

%build
autoreconf --force --install
%configure --disable-dependency-tracking --disable-static

%{__make} %{?_smp_mflags} libid3_la_LIBADD=-lz

%install
rm -rf %{buildroot}

%{make_install}
%{__make} docs

for i in txt html ; do
  iconv -f ISO-8859-1 -t UTF8 doc/id3v2.3.0.$i > tmp; mv tmp doc/id3v2.3.0.$i
done

mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p __doc/doc

cp -p doc/*.{gif,jpg,png,html,txt,ico,css} __doc/doc

rm -f %{buildroot}%{_libdir}/libid3.la

install -m 644 doc/man/*.1 %{buildroot}%{_mandir}/man1

install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -pm 644 %{SOURCE2} %{buildroot}%{_libdir}/pkgconfig/id3.pc

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog HISTORY NEWS README THANKS __doc/doc/
%{_bindir}/id3convert
%{_bindir}/id3cp
%{_bindir}/id3info
%{_bindir}/id3tag
%{_libdir}/libid3-3.8.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/id3lib.css doc/api/
%{_includedir}/id3.h
%{_includedir}/id3/
%{_libdir}/libid3.so
%{_libdir}/pkgconfig/id3.pc

################################################################################

%changelog
* Sun Sep 25 2022 Anton Novojilov <andy@essentialkaos.com> - 3.8.3-35
- Package improvements

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 3.8.3-34
- Fixed problems with executing ldconfig

* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 3.8.3-33
- Initial build for kaos repo
