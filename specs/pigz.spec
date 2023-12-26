################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?_without_check: %define _with_check 1}

################################################################################

Summary:        Parallel implementation of gzip
Name:           pigz
Version:        2.8
Release:        0%{?dist}
License:        zlib
Group:          Applications/Archiving
URL:            https://www.zlib.net/pigz/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://www.zlib.net/%{name}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRequires:  make gcc ncompress zlib-devel

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
pigz, which stands for parallel implementation of gzip, is a fully functional
replacement for gzip that exploits multiple processors and multiple cores to the
hilt when compressing data.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{make_build}

%install
rm -rf %{buildroot}

install -pDm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -pDm 0644 %{name}.1 %{buildroot}%{_datadir}/man/man1/%{name}.1

ln -sf %{name} %{buildroot}%{_bindir}/un%{name}

%check
%if %{?_with_check:1}%{?_without_check:0}
%{__make} tests CFLAGS="$RPM_OPT_FLAGS"
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc %{name}.pdf README
%{_bindir}/%{name}
%{_bindir}/un%{name}
%{_datadir}/man/man1/%{name}.*

################################################################################

%changelog
* Tue Dec 26 2023 Anton Novojilov <andy@essentialkaos.com> - 2.8-0
- Initial build for kaos-repo
