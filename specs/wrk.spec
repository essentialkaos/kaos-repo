################################################################################

%define _smp_mflags  -j1

################################################################################

Summary:        HTTP benchmarking tool
Name:           wrk
Version:        4.2.0
Release:        0%{?dist}
License:        Apache 2.0
Group:          Development/Tools
URL:            https://github.com/wg/wrk

Source:         https://github.com/wg/%{name}/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
wrk is a modern HTTP benchmarking tool capable of generating significant
load when run on a single multi-core CPU. It combines a multithreaded
design with scalable event notification systems such as epoll and kqueue.

An optional LuaJIT script can perform HTTP request generation, response
processing, and custom reporting.

################################################################################

%prep
%setup -q

%build
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_loc_datarootdir}
install -dm 755 %{buildroot}%{_loc_datarootdir}/%{name}/scripts

install -pm 755 %{name} %{buildroot}%{_bindir}/

cp scripts/* %{buildroot}%{_loc_datarootdir}/%{name}/scripts/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, 0755)
%doc LICENSE README.md NOTICE
%{_loc_datarootdir}/%{name}/scripts/*
%{_bindir}/%{name}

################################################################################

%changelog
* Fri Dec 02 2022 Anton Novojilov <andy@essentialkaos.com> - 4.2.0-0
- Updated to the latest release

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 4.1.0-0
- Updated to the latest release

* Sat Apr 09 2016 Anton Novojilov <andy@essentialkaos.com> - 4.0.2-0
- Updated to the latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.1-0
- Updated to the latest release

* Wed Apr 15 2015 Anton Novojilov <andy@essentialkaos.com> - 4.0.0-0
- Updated to the latest release

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 3.1.2-0
- Updated to the latest release

* Wed Oct 01 2014 Anton Novojilov <andy@essentialkaos.com> - 3.1.1-0
- Initial build
