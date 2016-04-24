###############################################################################

Summary:            Free reimplementation of the OpenDivX video codec
Name:               xvidcore
Version:            1.3.3
Release:            0%{?dist}
License:            XviD
Group:              System Environment/Libraries
URL:                http://www.xvid.org/

Source0:            http://downloads.xvid.org/downloads/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc-c++ make nasm 

###############################################################################

%description
Xvid is a high quality MPEG-4 ASP video codec. Xvid encoded MPEG-4 videos can i
be played back by other MPEG-4 implementations decoders such as DivX, FFmpeg 
MPEG-4 or standalone DVD players capable of MPEG-4 playback.

###############################################################################

%package -n lib%{name}-devel
Summary:            Development files of XviD video codec
Group:              Development/Libraries

Requires:           lib%{name} = %{version}

Provides:           xvid-devel = %{version}

Obsoletes:          xvid-devel < %{version}

%description -n lib%{name}-devel
Xvid is a high quality MPEG-4 ASP video codec. Development files of XviD.

###############################################################################

%package -n lib%{name}
Summary:            Shared library libxvidcore
Group:              Development/Libraries

%description -n lib%{name}
Xvid is a high quality MPEG-4 ASP video codec. Shared library of XviD.

###############################################################################

%prep
%setup -qn %{name}

%build
pushd build/generic
    %configure
    make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
pushd build/generic
    make install DESTDIR=%{buildroot}
popd

%clean
rm -rf %{buildroot}

###############################################################################

%post -n lib%{name}
/sbin/ldconfig

%postun -n lib%{name}
/sbin/ldconfig

###############################################################################

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

###############################################################################

%changelog
* Sun Apr 24 2016 Gleb Goncharov <yum@gongled.ru> - 1.3.3-0
- Updated to latest version.

* Wed Sep 11 2013 Paulo Roma <roma@lcg.ufrj.br> - 1.3.2-14
- Update to 1.3.2.

* Fri Oct 23 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.2-13
- Update to 1.2.2.

* Sun Jan 18 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.1-12
- Update to 1.2.1.

* Wed Jul  4 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.3-11
- Update to 1.1.3.

* Wed Nov  8 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.2
- Update to 1.1.2.

* Sun Jan 22 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.1.0.

* Wed Jan 19 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.0.3.

* Thu Oct 14 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.0.2.

* Tue Jun  8 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.0.1.

* Fri May 28 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Upgrade to 1.0.0 final.
- run ldconfig to ensure proper symlink creating at packaging time.

* Mon Apr 12 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Upgrade to 1.0.0-rc4.

* Thu Oct 23 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- rename static to devel package and put include files in there.

* Mon Sep 15 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Added a .so symlink to the lib for proper detection.

* Thu Aug  7 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.9.2.
- The .so file has now a version appended.

* Mon Apr  7 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.9.1.
- Build and install changes since there is now a nice configure script.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Wed Jan 29 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the location of the .h files... doh!

* Sun Jan 12 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Remove the decore.h and encore2.h inks as divx4linux 5.01 will provide them.
- Rename -devel to -static as it seems more logic.

* Fri Dec 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.

