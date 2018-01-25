################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         The Oil Run-time Compiler
Name:            orc
Version:         0.4.26
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         BSD
URL:             http://code.entropywave.com/orc/

Source0:         https://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc libtool chrpath

Provides:        %{name} = %{version}-%{release}

################################################################################

%package doc
Summary:         Documentation for Orc
Group:           Development/Languages

BuildArch:       noarch

Requires:        %{name} = %{version}-%{release}

%description doc
Documentation for Orc.

################################################################################

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

################################################################################

%package devel
Summary:         Development files and static libraries for Orc
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}
Requires:        %{name}-compiler pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

################################################################################

%package compiler
Summary:         Orc compiler
Group:           Development/Libraries

Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

%description compiler
The Orc compiler, to produce optimized code.

################################################################################

%prep
%setup -q

%build
%configure --disable-static \
           --disable-gtk-doc \
           --enable-user-codemem

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -or -name \*.la -delete

rm -rf %{buildroot}/%{_libdir}/orc

touch -r stamp-h1 %{buildroot}%{_includedir}/%{name}-0.4/orc/orc-stdint.h

chrpath --delete %{buildroot}%{_bindir}/orcc
chrpath --delete %{buildroot}%{_bindir}/orc-bugreport
chrpath --delete %{buildroot}%{_libdir}/liborc-*.so.*

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
%doc COPYING README
%{_libdir}/liborc-*.so.*
%{_bindir}/orc-bugreport

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/orc-0.4.pc
%{_datadir}/aclocal/orc.m4

%files compiler
%defattr(-,root,root,-)
%{_bindir}/orcc

################################################################################

%changelog
* Fri Mar 24 2017 Anton Novojilov <andy@essentialkaos.com> - 0.4.26-0
- Initial build for kaos repository
