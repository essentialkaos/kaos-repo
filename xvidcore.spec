################################################################################

Summary:            Free reimplementation of the OpenDivX video codec
Name:               xvidcore
Version:            1.3.4
Release:            0%{?dist}
License:            XviD
Group:              System Environment/Libraries
URL:                http://www.xvid.org

Source0:            http://downloads.xvid.org/downloads/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc make nasm

Requires:           lib%{name} = %{version}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Xvid is a high quality MPEG-4 ASP video codec. Xvid encoded MPEG-4 videos can i
be played back by other MPEG-4 implementations decoders such as DivX, FFmpeg
MPEG-4 or standalone DVD players capable of MPEG-4 playback.

################################################################################

%package -n lib%{name}-devel
Summary:            Development files of XviD video codec
Group:              Development/Libraries

Requires:           lib%{name} = %{version}

Provides:           xvid-devel = %{version}

Obsoletes:          xvid-devel < %{version}

%description -n lib%{name}-devel
Xvid is a high quality MPEG-4 ASP video codec. Development files of XviD.

################################################################################

%package -n lib%{name}
Summary:            Shared library libxvidcore
Group:              Development/Libraries

%description -n lib%{name}
Xvid is a high quality MPEG-4 ASP video codec. Shared library of XviD.

################################################################################

%prep
%setup -qn %{name}

%build
pushd build/generic
  %configure
  %{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

pushd build/generic
  %{make_install}
popd

%clean
rm -rf %{buildroot}

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README TODO

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%doc CodingStyle doc examples
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so

%files -n lib%{name}
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*

################################################################################

%changelog
* Sat Nov 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.3.4-0
- Updated to latest release

* Sun Apr 24 2016 Gleb Goncharov <yum@gongled.ru> - 1.3.3-0
- Updated to latest version
