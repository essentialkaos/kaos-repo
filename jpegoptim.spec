###############################################################################

Summary:              Utility for optimizing/compressing JPEG files
Name:                 jpegoptim
Version:              1.4.4
Release:              0%{?dist}
License:              GPL
Group:                Applications/Multimedia
URL:                  http://www.iki.fi/tjko/projects.html

Source:               http://www.kokkonen.net/tjko/src/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        gcc >= 3.0 make libjpeg-turbo-devel

Requires:             libjpeg-turbo

###############################################################################

%description
Jpegoptim can optimize/compress jpeg files. Program support
lossless optimization, which is based on optimizing the Huffman
tables. So called, "lossy" optimization (compression) is done
by re-encoding the image using user specified image quality factor.

###############################################################################

%prep
%setup -q

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc README COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

###############################################################################

%changelog
* Fri Dec 09 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 1.4.4-0
- Initial build.

