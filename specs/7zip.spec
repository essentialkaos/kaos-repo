################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define major_ver  22
%define minor_ver  01

%define shortname  7z

################################################################################

Summary:    7-Zip is a file archiver with a high compression ratio
Name:       7zip
Version:    %{major_ver}.%{minor_ver}
Release:    0%{?dist}
License:    LGPL 2.0
Group:      Applications/Archiving
URL:        https://7-zip.org

Source0:    https://7-zip.org/a/7z%{major_ver}%{minor_ver}-linux-x64.tar.xz

Source100:  checksum.sha512

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   %{name} = %{version}-%{release}
Provides:   %{shortname} = %{version}-%{release}

################################################################################

%description
7-Zip is a file archiver with a high compression ratio.

################################################################################

%prep
%{crc_check}

%setup -qcn 7z%{major_ver}%{minor_ver}-linux-x64
%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}

install -pm 755 7zz %{buildroot}%{_bindir}/
install -pm 755 7zzs %{buildroot}%{_bindir}/

ln -sf %{_bindir}/7zz %{buildroot}%{_bindir}/%{shortname}

################################################################################

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc History.txt License.txt readme.txt
%{_bindir}/7z
%{_bindir}/7zz
%{_bindir}/7zzs

################################################################################

%changelog
* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 22.01-0
- UDF support was improved to UDF version 2.60.
- HFS and APFS support was improved.
