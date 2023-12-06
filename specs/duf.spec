################################################################################

# rpmbuilder:gopack  github.com/muesli/duf
# rpmbuilder:tag     v0.8.1

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define  debug_package %{nil}

################################################################################

Summary:        Disk usage utility
Name:           duf
Version:        0.8.1
Release:        1%{?dist}
Group:          Development/Tools
License:        MIT
URL:            https://github.com/muesli/duf

Source0:        %{name}-%{version}.tar.bz2

Source100:      checksum.sha512

BuildRequires:  golang >= 1.20

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Disk Usage/Free Utility with a variety of features:

- User-friendly, colorful output
- Adjusts to your terminal's width
- Sort the results according to your needs
- Groups & filters devices
- Can conveniently output JSON

################################################################################

%prep
%{crc_check}

%setup -q

%build
pushd github.com/muesli/%{name}
  go build -ldflags="-X 'main.Version=%{version}' -X main.CommitSHA=HEAD"
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 github.com/muesli/%{name}/%{name} \
                %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

################################################################################

%changelog
* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-1
- Rebuilt with the latest version of Go

* Fri Sep 30 2022 Anton Novojilov <andy@essentialkaos.com> - 0.8.1-0
- Updated to the latest stable release

* Fri Oct 23 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 0.4.0-0
- Initial build for kaos-repo
