################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define major_ver  25
%define minor_ver  00

%define shortname  7z

################################################################################

Summary:        7-Zip is a file archiver with a high compression ratio
Name:           7zip
Version:        %{major_ver}.%{minor_ver}
Release:        0%{?dist}
License:        LGPL 2.0
Group:          Applications/Archiving
URL:            https://7-zip.org

Source0:        https://7-zip.org/a/7z%{major_ver}%{minor_ver}-src.tar.xz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  make gcc-c++ asmc dos2unix

Provides:       %{name} = %{version}-%{release}
Provides:       %{shortname} = %{version}-%{release}

################################################################################

%description
7-Zip is a file archiver with a high compression ratio.

################################################################################

%prep
%crc_check
%autosetup -cn 7z%{major_ver}%{minor_ver}-linux

dos2unix DOC/*.txt

# perfecto:ignore
chmod -x DOC/*.txt

%if 0%{?rhel} < 9
sed -i -e 's/-Waddress-of-packed-member//' -e 's/-Wcast-align=strict//' C/warn_gcc.mak CPP/7zip/warn_gcc.mak
%endif

sed -i 's#^ -fPIC# -fPIC %{optflags}#' CPP/7zip/7zip_gcc.mak
sed -i 's#LFLAGS_ALL = -s#LFLAGS_ALL =#' CPP/7zip/7zip_gcc.mak
sed -i 's/$(CXX) -o $(PROGPATH)/$(CXX) -Wl,-z,noexecstack -o $(PROGPATH)/' CPP/7zip/7zip_gcc.mak

%build
pushd CPP/7zip/Bundles/Alone2
%{make_build} -f ../../cmpl_gcc_x64.mak
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 CPP/7zip/Bundles/Alone2/b/g_x64/7zz %{buildroot}%{_bindir}/

ln -sf %{_bindir}/7zz %{buildroot}%{_bindir}/%{shortname}

################################################################################

%files
%defattr(-,root,root,-)
%doc DOC/*.txt
%{_bindir}/7z
%{_bindir}/7zz

################################################################################

%changelog
* Sat Jul 19 2025 Anton Novojilov <andy@essentialkaos.com> - 25.00-0
- https://sourceforge.net/p/sevenzip/discussion/45797/thread/4ed0e379f4/

* Fri Jan 24 2025 Anton Novojilov <andy@essentialkaos.com> - 24.09-0
- https://sourceforge.net/p/sevenzip/discussion/45797/thread/b95432c7ac/

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 24.08-0
- https://sourceforge.net/p/sevenzip/discussion/45797/thread/f162d68dcd/

* Fri Dec 16 2022 Anton Novojilov <andy@essentialkaos.com> - 22.01-0
- UDF support was improved to UDF version 2.60.
- HFS and APFS support was improved.
