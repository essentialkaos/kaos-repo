################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Name:           vips
Summary:        C/C++ library for processing large images
Version:        8.16.0
Release:        0%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            https://libvips.github.io/libvips/

Source0:        https://github.com/libvips/libvips/releases/download/v%{version}/%{name}-%{version}.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  meson cmake pkgconfig gettext libarchive
BuildRequires:  gcc gcc-c++ libjpeg-turbo-devel libtiff-devel zlib-devel
BuildRequires:  glib2-devel libxml2-devel expat-devel orc-devel libpng-devel
BuildRequires:  libexif-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.

################################################################################

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries

Requires:  libjpeg-turbo-devel libtiff-devel zlib-devel
Requires:  vips = %{version}-%{release}

%description devel
Package contains the header files and libraries necessary for developing
programs using VIPS. It also contains a C++ API and development man pages.

################################################################################

%package tools
Summary:   Command-line tools for %{name}
Group:     Applications/Multimedia

Requires:  vips = %{version}-%{release}

%if 0%{?rhel} <= 8
Requires:  python2
%else
Requires:  python3
%endif

%description tools
Package contains command-line tools for working with VIPS.

################################################################################

%package doc
Summary:  Documentation for %{name}
Group:    Documentation

Conflicts:  %{name} < %{version}-%{release}
Conflicts:  %{name} > %{version}-%{release}

%description doc
Package contains extensive documentation about VIPS in both HTML and
PDF formats.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{meson} \
         -Darchive=disabled \
         -Dcfitsio=disabled \
         -Dfftw=disabled \
         -Dfontconfig=disabled \
         -Dheif=disabled \
         -Dhighway=disabled \
         -Dimagequant=disabled \
         -Dintrospection=disabled \
         -Djpeg-xl=disabled \
         -Dlcms=disabled \
         -Dmagick=disabled \
         -Dmatio=disabled \
         -Dnifti=disabled \
         -Dopenexr=disabled \
         -Dopenjpeg=disabled \
         -Dopenslide=disabled \
         -Dpangocairo=disabled \
         -Dpdfium=disabled \
         -Dpoppler=disabled \
         -Dquantizr=disabled \
         -Drsvg=disabled \
         -Dspng=disabled \
         -Dwebp=disabled

%{meson_build}

%install
rm -rf %{buildroot}

%{meson_install}

%if 0%{?rhel} <= 8
  sed -i "s#/usr/bin/python#/usr/bin/python2#" %{buildroot}%{_bindir}/vipsprofile
%else
  sed -i "s#/usr/bin/python#/usr/bin/python3#" %{buildroot}%{_bindir}/vipsprofile
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc README.md LICENSE ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*

################################################################################

%changelog
* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 8.16.0-0
- https://github.com/libvips/libvips/releases/tag/v8.16.0

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 8.15.3-0
- https://github.com/libvips/libvips/releases/tag/v8.15.3

* Tue Apr 16 2024 Anton Novojilov <andy@essentialkaos.com> - 8.15.2-0
- https://github.com/libvips/libvips/releases/tag/v8.15.2

* Wed Jan 17 2024 Anton Novojilov <andy@essentialkaos.com> - 8.15.1-0
- https://github.com/libvips/libvips/releases/tag/v8.15.1

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.15.0-0
- https://github.com/libvips/libvips/releases/tag/v8.15.0

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 8.14.5-0
- https://github.com/libvips/libvips/releases/tag/v8.14.5

* Fri Dec 09 2022 Anton Novojilov <andy@essentialkaos.com> - 8.13.3-0
- https://github.com/libvips/libvips/releases/tag/v8.13.3

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.9.1-0
- https://github.com/libvips/libvips/releases/tag/v8.9.1

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.9.0-0
- https://github.com/libvips/libvips/releases/tag/v8.9.0

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.4-0
- https://github.com/libvips/libvips/releases/tag/v8.8.4

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.3-0
- https://github.com/libvips/libvips/releases/tag/v8.8.3

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.2-0
- https://github.com/libvips/libvips/releases/tag/v8.8.2

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.1-0
- https://github.com/libvips/libvips/releases/tag/v8.8.1

* Tue Jan 28 2020 Anton Novojilov <andy@essentialkaos.com> - 8.8.0-0
- https://github.com/libvips/libvips/releases/tag/v8.8.0

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 8.7.4-0
- https://github.com/libvips/libvips/releases/tag/v8.7.4

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 8.7.3-0
- https://github.com/libvips/libvips/releases/tag/v8.7.3

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.2-0
- https://github.com/libvips/libvips/releases/tag/v8.7.2

* Fri Dec 07 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.1-0
- https://github.com/libvips/libvips/releases/tag/v8.7.1

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 8.7.0-0
- https://github.com/libvips/libvips/releases/tag/v8.7.0

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.5-0
- https://github.com/libvips/libvips/releases/tag/v8.6.5

* Thu Jun 21 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.4-0
- https://github.com/libvips/libvips/releases/tag/v8.6.4

* Mon Mar 26 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.3-0
- https://github.com/libvips/libvips/releases/tag/v8.6.3

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.2-0
- https://github.com/libvips/libvips/releases/tag/v8.6.2

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.1-0
- https://github.com/libvips/libvips/releases/tag/v8.6.1

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 8.6.0-0
- https://github.com/libvips/libvips/releases/tag/v8.6.0

* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 8.5.9-0
- https://github.com/libvips/libvips/releases/tag/v8.5.9

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 8.4.5-0
- https://github.com/libvips/libvips/releases/tag/v8.4.5

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 8.4.2-0
- https://github.com/libvips/libvips/releases/tag/v8.4.2

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.3-0
- https://github.com/libvips/libvips/releases/tag/v8.3.3

* Sat Jul 23 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.1-0
- https://github.com/libvips/libvips/releases/tag/v8.3.1

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 7.42.1-0
- https://github.com/libvips/libvips/releases/tag/v8.13.3

* Thu Aug 28 2014 Anton Novojilov <andy@essentialkaos.com> - 7.40.6-0
- Initial build
