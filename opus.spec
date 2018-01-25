################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:         An audio codec for use in low-delay speech and audio communication
Name:            opus
Version:         1.2.1
Release:         0%{?dist}
Group:           System Environment/Libraries
License:         BSD
URL:             http://www.opus-codec.org

Source0:         https://archive.mozilla.org/pub/%{name}/%{name}-%{version}.tar.gz
Source1:         http://tools.ietf.org/rfc/rfc6716.txt

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   make gcc doxygen

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

################################################################################

%package devel

Summary:         Development package for opus
Group:           Development/Libraries

Requires:        libogg-devel
Requires:        opus = %{version}-%{release}

%description devel
Files for development with opus.

################################################################################

%prep
%setup -qn %{name}-%{version}

cp %{SOURCE1} .

%build
%configure --enable-custom-modes --disable-static

%{__make} %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}

%{make_install}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-, root, root, -)
%doc COPYING
%{_libdir}/libopus.so.*

%files devel
%defattr(-, root, root, -)
%doc README doc/html rfc6716.txt
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

################################################################################

%changelog
* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 1.1.5-0
- Initial build for kaos repository
