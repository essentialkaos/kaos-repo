#################################################################################

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

%define __ldconfig        %{_sbin}/ldconfig

################################################################################

Summary:           Open source video codec
Name:              dirac
Version:           1.0.2
Release:           15%{?dist}
License:           MPLv1.1
Group:             System Environment/Libraries
URL:               http://diracvideo.org

Source0:           http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0:            %{name}-%{version}-backports.patch
Patch1:            0001-Fix-uninitialised-memory-read-that-causes-the-encode.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc gcc-c++ cppunit-devel doxygen graphviz-devel
BuildRequires:     dvipdfm chrpath

%if 0%{?rhel} >= 7
BuildRequires:     tex-latex-bin
%else
BuildRequires:     tetex tetex-latex
%endif

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
Dirac is an open source video codec. It uses a traditional hybrid video codec
architecture, but with the wavelet transform instead of the usual block
transforms.  Motion compensation uses overlapped blocks to reduce block
artefacts that would upset the transform coding stage.

################################################################################

%package libs
Summary:           Libraries for dirac
Group:             System Environment/Libraries

%description libs
This package contains libraries for dirac.

################################################################################

%package devel
Summary:           Development files for dirac
Group:             Development/Libraries

Requires:          %{name}-libs = %{version}-%{release}
Requires:          pkgconfig

%description devel
This package contains development files for dirac.

################################################################################

%package docs
Summary:        Documentation for dirac
Group:          Documentation

%description docs
This package contains documentation files for dirac.

################################################################################

%prep
%setup -q

%patch0 -p0
%patch1 -p1

install -pm 644 README README.Dirac
install -pm 644 util/instrumentation/README README.instrumentation

# Fix permission mode for sources
find doc unit_tests util libdirac_encoder libdirac_byteio -type f -name \* -exec chmod 644 {} \;

# Remove -Werror
sed -i 's/-Werror//g' configure.ac configure

%build
%configure \
  --program-prefix=dirac_ \
  --program-transform-name=s,dirac_dirac_,dirac_, \
  --enable-overlay \
  --disable-static \
%ifarch x86_64 \
  --enable-mmx=yes \
%else \
  --enable-mmx=no \
%endif

# Remove rpath from libtool (may be unneeded)
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}

%{make_install} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Move doc in docdir macro
mv %{buildroot}%{_datadir}/doc/dirac __doc

# Transform-name fix
mv %{buildroot}%{_bindir}/dirac_create_dirac_testfile.pl \
   %{buildroot}%{_bindir}/create_dirac_testfile.pl

sed -i -e 's|"RGBtoYUV"|"dirac_RGBtoYUV"|g' %{buildroot}%{_bindir}/create_dirac_testfile.pl
sed -i -e 's|/home/guest/dirac-0.5.0/util/conversion|%{_bindir}|' %{buildroot}%{_bindir}/create_dirac_testfile.pl

chrpath --delete %{buildroot}%{_bindir}/%{name}*

%post libs
%{__ldconfig}

%postun libs
%{__ldconfig}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.Dirac TODO
%doc README.instrumentation
%{_bindir}/create_dirac_testfile.pl
%{_bindir}/dirac_*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dirac/
%{_libdir}/pkgconfig/dirac.pc
%{_libdir}/libdirac_*.so

%files docs
%defattr(-,root,root,-)
%doc __doc/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libdirac_decoder.so.*
%{_libdir}/libdirac_encoder.so.*

################################################################################

%changelog
* Tue Feb 21 2017 Anton Novojilov <andy@essentialkaos.com> - 1.0.2-15
- Initial build for kaos repository
