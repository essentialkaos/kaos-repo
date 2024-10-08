################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Library for manipulating ID3v1 and ID3v2 tags
Name:           id3lib
Version:        3.8.3
Release:        35%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            https://id3lib.sourceforge.net

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}-no_date_footer.hml
Source2:        id3.pc

Source100:      checksum.sha512

Patch0:         %{name}-dox.patch
Patch11:        %{name}-%{version}-autoreconf.patch
Patch12:        %{name}-%{version}-io_helpers-163101.patch
Patch13:        %{name}-%{version}-mkstemp.patch
Patch14:        %{name}-%{version}-includes.patch
Patch15:        %{name}-vbr_buffer_overflow.diff
Patch16:        20-create-manpages.patch
Patch17:        60-fix_make_check.patch
Patch18:        60-%{name}-missing-nullpointer-check.patch
Patch19:        %{name}-%{version}-fix-utf16-stringlists.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc-c++ autoconf automake libtool zlib-devel doxygen

Provides:       %{name} = %{version}-%{release}

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

Summary:  Development tools for the id3lib library
Group:    Development/Libraries

Requires:  %{name} = %{version}-%{release}
Requires:  zlib-devel

%description devel
This package provides files needed to develop with the id3lib library.

################################################################################

%prep
%crc_check
%autosetup -N
%autopatch -p0 -M 9
%autopatch -p1 -m 10

# perfecto:ignore
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
