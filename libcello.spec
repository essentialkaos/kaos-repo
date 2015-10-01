###############################################################################

%define __ldconfig    /sbin/ldconfig

###############################################################################

%define custname      libCello

###############################################################################

Summary:              High level programming library for C
Name:                 libcello
Version:              2.0.3
Release:              0%{?dist}
License:              BSD
Group:                System Environment/Libraries
URL:                  http://libcello.org/home

Source:               http://libcello.org/static/%{custname}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc >= 3.0 make

Provides:             %{name} = %{version}-%{release}
Provides:             cello = %{version}-%{release}

###############################################################################

%description
Cello is a GNU99 C library which brings higher level programming to C.

###############################################################################

%package devel
Summary:              Header files and static libraries for libcello
Group:                System Environment/Libraries

Requires:             %{name} = %{version}-%{release}

%description devel
Header files and static libraries for libcello.

###############################################################################

%prep
%setup -q -n %{custname}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir}
install -dm 755 %{buildroot}%{_includedir}

install -pm 644 %{custname}.a %{buildroot}%{_libdir}/
install -pm 755 %{custname}.so %{buildroot}%{_libdir}/

cp -r include/* %{buildroot}%{_includedir}

%post -p %{__ldconfig}

%postun -p %{__ldconfig}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc LICENSE.md README.md
%{_libdir}/%{custname}.so

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/%{custname}.a
%{_includedir}

###############################################################################

%changelog
* Sun Nov 17 2013 Anton Novojilov <andy@essentialkaos.com> - 1.1.5-0
- Improved spec file
- Updated to latest version

* Tue Jul 30 2013 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-0
- Updated to version 1.0.0

* Mon Jul 22 2013 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Updated to version 0.9.3
