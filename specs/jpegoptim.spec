################################################################################

Summary:              Utility for optimizing/compressing JPEG files
Name:                 jpegoptim
Version:              1.4.6
Release:              0%{?dist}
License:              GPL
Group:                Applications/Multimedia
URL:                  https://github.com/tjko/jpegoptim

Source:               https://github.com/tjko/%{name}/archive/RELEASE.%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make gcc libjpeg-turbo-devel

Requires:             libjpeg-turbo

Provides:             %{name} = %{version}-%{release}

################################################################################

%description
Jpegoptim can optimize/compress jpeg files. Program support
lossless optimization, which is based on optimizing the Huffman
tables. So called, "lossy" optimization (compression) is done
by re-encoding the image using user specified image quality factor.

################################################################################

%prep
%setup -qn %{name}-RELEASE.%{version}

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
* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.6-0
- Updated to latest stable release

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.4.5-0
- Updated to latest stable release

* Fri Dec 09 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.4.4-0
- Initial build
