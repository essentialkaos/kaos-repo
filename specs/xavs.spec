################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:            Audio Video Standard of China
Name:               xavs
Version:            0.1.51
Release:            1%{?dist}
License:            GPL
Group:              System Environment/Libraries
URL:                https://xavs.sourceforge.net

Source0:            %{name}-%{version}.tar.gz
Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ make

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
AVS is the Audio Video Standard of China. This project aims to
implement high quality AVS encoder and decoder.

################################################################################

%package devel
Summary:            Header files and static libraries for xavs
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
These are the header files and static libraries from xavs that are needed
to build programs that use it.

################################################################################

%prep
%{crc_check}

%setup -q

%build
export CFLAGS="%{optflags} -fPIC"

%configure \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --enable-pic \
  --enable-shared

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/bin/ldconfig

%postun
/bin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/xavs
%{_libdir}/lib%{name}.so.*
%{_libdir}/pkgconfig/%{name}.pc

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so

################################################################################

%changelog
* Sat May 25 2019 Anton Novojilov <andy@essentialkaos.com> - 0.1.51-1
- Minor spec fix

* Sun Apr 24 2016 Gleb Goncharov <yum@gongled.ru> - 0.1.51-0
- Initial build
