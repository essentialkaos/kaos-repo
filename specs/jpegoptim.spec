################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:           Utility for optimizing/compressing JPEG files
Name:              jpegoptim
Version:           1.5.0
Release:           0%{?dist}
License:           GPL
Group:             Applications/Multimedia
URL:               https://github.com/tjko/jpegoptim

Source:            https://github.com/tjko/jpegoptim/archive/refs/tags/v%{version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc libjpeg-turbo-devel

Requires:          libjpeg-turbo

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Jpegoptim can optimize/compress jpeg files. Program support
lossless optimization, which is based on optimizing the Huffman
tables. So called, "lossy" optimization (compression) is done
by re-encoding the image using user specified image quality factor.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

################################################################################

%changelog
* Sun Dec 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- https://github.com/tjko/jpegoptim/releases/tag/v1.5.0

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.6-0
- https://github.com/tjko/jpegoptim/releases/tag/v1.4.6

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- https://github.com/tjko/jpegoptim/releases/tag/v1.4.5

* Fri Dec 09 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.4.4-0
- Initial build
