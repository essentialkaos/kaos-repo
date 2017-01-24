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
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
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
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

%define major_version     8
%define minor_version     4
%define patch_level       2


###############################################################################

Name:              vips
Summary:           C/C++ library for processing large images
Version:           %{major_version}.%{minor_version}.%{patch_level}
Release:           0%{?dist}
License:           LGPLv2+
Group:             System Environment/Libraries
URL:               http://www.vips.ecs.soton.ac.uk

Source:            http://www.vips.ecs.soton.ac.uk/supported/%{major_version}.%{minor_version}/%{name}-%{version}.tar.gz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make pkgconfig gettext libtool python-devel swig gtk-doc
BuildRequires:     gcc gcc-c++ libjpeg-turbo-devel libtiff-devel zlib-devel
BuildRequires:     glib2-devel libxml2-devel libexif-devel

Provides:          %{name} = %{version}-%{release}

###############################################################################

%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.

###############################################################################

%package devel
Summary:           Development files for %{name}
Group:             Development/Libraries
Requires:          libjpeg-turbo-devel libtiff-devel zlib-devel
Requires:          vips = %{version}-%{release}

%description devel
Package contains the header files and libraries necessary for developing 
programs using VIPS. It also contains a C++ API and development man pages.

###############################################################################

%package tools
Summary:           Command-line tools for %{name}
Group:             Applications/Multimedia
Requires:          vips = %{version}-%{release}

%description tools
Package contains command-line tools for working with VIPS.

###############################################################################

%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Conflicts:         %{name} < %{version}-%{release}
Conflicts:         %{name} > %{version}-%{release}

%description doc
Package contains extensive documentation about VIPS in both HTML and 
PDF formats.

###############################################################################

%prep
%setup -q

find . -name 'CVS' -type d -print0 | xargs -0 rm -rf

export FAKE_BUILD_DATE=$(date -r %{SOURCE0})
sed -i "s/\\(IM_VERSION_STRING=\\)\$IM_VERSION-\`date\`/\\1\"\$IM_VERSION-$FAKE_BUILD_DATE\"/g" \
  configure
unset FAKE_BUILD_DATE

%build
%configure --disable-static --disable-gtk-doc --without-python
%{__make} %{?_smp_mflags} LIBTOOL=libtool

%install
%{__rm} -rf %{buildroot}

%{make_install}

find %{buildroot} \( -name '*.la' -o -name '*.a' \) -exec rm -f {} ';'

rm -rf %{buildroot}%{_datadir}/doc/%{name}
rm -rf %{buildroot}%{_datadir}/locale

%post -p %{__ldconfig}

%postun -p %{__ldconfig}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root)
%doc AUTHORS NEWS THANKS TODO COPYING ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

###############################################################################

%changelog
* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 8.4.2-0
- Updated to latest release

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.3-0
- Updated to latest release

* Sat Jul 23 2016 Anton Novojilov <andy@essentialkaos.com> - 8.3.1-0
- Updated to latest release

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 7.42.1-0
- Updated to latest release

* Thu Aug 28 2014 Anton Novojilov <andy@essentialkaos.com> - 7.40.6-0
- Initial build
