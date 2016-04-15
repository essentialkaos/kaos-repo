################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig

###############################################################################

%define lib_name          libmp3%{name}

###############################################################################

Summary:            MP3 encoder and frame analyzer
Name:               lame
Version:            3.99.5
Release:            0%{?dist}
License:            LGPLv2+
Group:              Applications/Multimedia
URL:                http://lame.sourceforge.net/

Source0:            http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:           ncurses >= 5.0

Provides:           lame-libs = %{version}-%{release}
Provides:           mp3encoder = %{version}-%{release}

Obsoletes:          lame-libs < %{version}-%{release}
Obsoletes:          mp3encoder < %{version}-%{release}

BuildRequires:      gcc-c++ make nasm
BuildRequires:      ncurses-devel libsndfile-devel

###############################################################################

%description
LAME is an educational tool to be used for learning about MP3 encoding.
The goal of the LAME project is to use the open source model to improve
the psycho acoustics, noise shaping and speed of MP3. Another goal of
the LAME project is to use these improvements for the basis of a patent
free audio compression codec for the GNU project.

###############################################################################

%package devel
Summary:            Libraries and headers for lame
Group:              Development/Libraries

Requires:           %{name} = %{version}-%{release}

%description devel
Libraries provide the functions necessary to convert raw PCM and WAV files to 
MP3 files.

###############################################################################

%prep
%setup -q
%ifarch %{ix86} x86_64
  sed -i -e '/define sp/s/+/ + /g' libmp3lame/i386/nasm.h
%endif

%build
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86} x86_64
  --enable-nasm \
%endif
  --enable-decoder \
  --enable-mp3x \
  --enable-mp3rtp

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

###############################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING LICENSE README TODO USAGE
%{_bindir}/%{name}
%{_bindir}/mp3rtp
%{_libdir}/%{lib_name}.so.*
%{_docdir}/%{name}/html/*.html
%{_mandir}/man1/lame.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/%{name}.h
%{_libdir}/%{lib_name}.so
%{_libdir}/%{lib_name}.la

###############################################################################

%changelog
* Thu Apr 14 2016 Gleb Goncharov <yum@gongled.ru> - 3.99.5-0
- Spec refactoring.
- Updated to latest version.

* Sun Nov 27 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.99.3-23
- Update to 3.99.3.

* Mon Nov  1 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98.4-22
- Fix build for nasm >= 2.09.x.

* Sun Apr  4 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98.4-21
- Update to 3.98.4.

* Fri Nov 14 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98.2-19
- Providing lame-libs because of rpmfusion.
- Only including the relevant files in doc.

* Tue Sep 23 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98.2-18
- Fixed mp3rtp.
- Using %%check.

* Fri Jul 18 2008 Paulo Roma <roma@lcg.ufrj.br> - 3.98-17
- Removed patch0 (libm).
- Using %%bcond_with mp3rtp (the build fails with it).
- Using nasm for x86_64.
- Disabled rpath.
- Changed license.
- Converted ChangeLog to utf8.

* Thu Jul 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.98-16
- Update to 3.98.

* Wed Dec 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.97-15
- fix unresolved symbols from libm (Rex Dieter).

* Sun Oct 15 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 3.97-14
- Update to 3.97.

* Fri Oct  1 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.96.1.

* Tue Apr 13 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.96.

* Wed Jan 14 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.95.1.

* Mon Nov 17 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.94alpha cvs build.

* Thu Oct  9 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 3.94alpha cvs build.
- Many small fixes.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Mon Jan 13 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.93.1.
- Removed Epoch: tag, upgrade by hand! :-/

* Sat Oct  5 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fix unpackaged doc problem.

* Fri Sep 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0.
- Simplified deps as it now builds VBR code fine with default nasm and gcc 3.2.

* Tue Jul 16 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fix to the lamecc stuff.

* Wed Jul 10 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Changes to now support ppc with no ugly workarounds.

* Thu May  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Wed Apr 24 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.92.

* Mon Apr  8 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Added a symlink from lame.h to lame/lame.h to fix some include file
  detection for most recent programs that use lame.

* Wed Jan  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.91.
- Simplified the compilation optimizations after heavy home-made tests.
- Now build only i386 version but optimized for i686. Don't worry i686
  owners, you loose only 1% in speed but gain about 45% compared to if
  you had no optimizations at all!

* Mon Dec 24 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.90.1.
- Enabled the GTK+ frame analyzer.
- Spec file cleanup (CVS, man page, bindir are now fixed).

* Fri Nov 16 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt with mpg123 decoding support.

* Tue Oct 23 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the %%pre and %%post that should have been %%post and %%postun, silly me!
- Removed -malign-double (it's evil, Yosi told me and I tested, brrr ;-)).
- Now build with gcc3, VBR encoding gets a hell of a boost, impressive!
  I recommend you now use "lame --r3mix", it's the best.
- Tried to re-enable vorbis, but it's a no-go.

* Thu Jul 26 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Build with kgcc to have VBR working.

* Wed Jul 25 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.89beta : Must be built with a non-patched version of nasm
  to work!

* Mon May  7 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat 7.1.
- Disabled the vorbis support since it fails to build with it.
- Added a big optimisation section, thanks to Yosi Markovich
  <senna@camelot.com> for this and other pointers.

* Sun Feb 11 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Split the package, there is now a -devel

* Thu Oct 26 2000 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release for RedHat 7.0 from scratch

