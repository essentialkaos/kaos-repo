################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define pkg_name  frei0r-plugins

################################################################################

Summary:        A minimalistic plugin API for video effects
Name:           frei0r
Version:        1.8.0
Release:        0%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
URL:            https://frei0r.dyne.org

Source0:        https://github.com/dyne/%{name}/archive/v%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc gcc-c++ automake libtool
BuildRequires:  autoconf opencv-devel gavl-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Frei0r is a minimalistic plugin API for video effects.

The main emphasis is on simplicity for an API that will round up the
most common video effects into simple filters, sources and mixers that
can be controlled by parameters.

################################################################################

%prep
%{crc_check}

%setup -q

# Fix autotools build fails on removed TODO
touch TODO

%build
libtoolize --force
aclocal
autoheader
automake --force-missing --add-missing
autoconf

%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README.md
%{_includedir}/%{name}.h
%{_docdir}/%{pkg_name}/*
%{_libdir}/%{name}-1/*.so
%{_libdir}/pkgconfig/%{name}.pc

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.8.0-0
- https://github.com/dyne/frei0r/releases/tag/v1.8.0

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-1
- Fixed problems with executing ldconfig

* Fri Dec 13 2019 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- https://github.com/dyne/frei0r/releases/tag/v1.7.0

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/dyne/frei0r/releases/tag/v1.6.1

* Wed Apr 13 2016 Gleb Goncharov <yum@gongled.ru> - 1.5-0
- https://github.com/dyne/frei0r/releases/tag/v1.5

* Mon Mar 17 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.4-0
- https://github.com/dyne/frei0r/releases/tag/v1.4

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3-0
- Initial build
