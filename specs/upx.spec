################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
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
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

################################################################################

Summary:           Ultimate Packer for eXecutables
Name:              upx
Version:           3.94
Release:           0%{?dist}
License:           GPLv2+ and Public Domain
Group:             Applications/Archiving
URL:               https://upx.github.io

Source:            https://github.com/upx/upx/releases/download/v%{version}/%{name}-%{version}-src.tar.xz

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc gcc-c++ ucl-devel zlib-devel

Requires:          ucl zlib

################################################################################

%description
UPX is a free, portable, extendable, high-performance executable
packer for several different executable formats. It achieves an
excellent compression ratio and offers very fast decompression. Your
executables suffer no memory overhead or other drawbacks.

################################################################################

%prep
%setup -qn %{name}-%{version}-src

sed -i -e 's/ -O2/ /' -e 's/ -Werror//' src/Makefile

# Disable check_whitespace script
echo -n > src/stub/scripts/check_whitespace.sh

%build
%{__make} %{?_smp_mflags} -C src
%{__make} -C doc

%install
rm -rf %{buildroot}
install -Dpm 644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -Dpm 755 src/%{name}.out %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc BUGS COPYING LICENSE NEWS PROJECTS README README.1ST THANKS doc/*.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

################################################################################

%changelog
* Mon Jul 10 2017 Anton Novojilov <andy@essentialkaos.com> - 3.94-0
- Updated to latest stable release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 3.93-0
- Updated to latest stable release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.92-0
- Updated to latest stable release

* Tue May 06 2014 Anton Novojilov <andy@essentialkaos.com> - 3.91-0
- Initial build for kaos repository
