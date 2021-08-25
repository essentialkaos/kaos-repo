################################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0002

################################################################################

%define _smp_mflags -j1

################################################################################

Summary:         Data Acquisition Library
Name:            daq
Version:         2.0.7
Release:         0%{?dist}
License:         GPL
Group:           Development/Libraries
URL:             https://www.snort.org

Source0:         https://www.snort.org/downloads/snort/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   autoconf automake >= 1.16 make gcc libtool flex
BuildRequires:   libpcap-devel libdnet-devel bison zlib-devel

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Data Acquisition library for Snort.

%package devel

Summary:         Header files and static libraries for Data Acquisition Library
Group:           System Environment/Libraries

Requires:        %{name} = %{version}-%{release}

%description devel
Header files and static libraries for Data Acquisition Library.

################################################################################

%prep
%setup -q

%build

# Change hardcoded automake version to 1.16.x
sed -i "s/am__api_version='1.15'/am__api_version='1.16'/" configure

%configure --prefix=%{_prefix} \
           --enable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%doc README COPYING ChangeLog
%{_libdir}/lib%{name}.so
%{_libdir}/%{name}/%{name}_*.so
%{_libdir}/libsfbpf.so.0.0.1
%{_libdir}/libsfbpf.so.0
%{_libdir}/lib%{name}.so.*
%{_libdir}/libsfbpf.so
%{_bindir}/%{name}-modules-config

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_includedir}/%{name}_common.h
%{_includedir}/sfbpf_dlt.h
%{_includedir}/%{name}_api.h
%{_includedir}/sfbpf.h
%{_libdir}/lib%{name}_static_modules.la
%{_libdir}/lib%{name}_static_modules.a
%{_libdir}/libsfbpf.a
%{_libdir}/libsfbpf.la
%{_libdir}/lib%{name}.la
%{_libdir}/%{name}/%{name}_*.la
%{_libdir}/lib%{name}_static.la
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}_static.a

################################################################################

%changelog
* Fri May 15 2020 Anton Novojilov <andy@essentialkaos.com> - 2.0.7-0
- Updated to the latest version
- Removed unsafe owner change

* Tue Sep 06 2016 Anton Novojilov <andy@essentialkaos.com> - 2.0.6-1
- Added post install ldconfig execution
- Fixed mutlithread build problems

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 2.0.6-0
- Updated to the latest version

* Wed Dec 17 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.4-0
- Updated to the latest version

* Fri Oct 03 2014 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- Initial build
