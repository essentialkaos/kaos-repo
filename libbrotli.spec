###############################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
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

###############################################################################

%define realname          brotli

###############################################################################

Summary:             Wrapper around the brotli code base
Name:                lib%{realname}
Version:             0.5.2
Release:             0%{?dist}
License:             BSD
Group:               System Environment/Libraries
URL:                 https://github.com/redis/hiredis

Source0:             https://github.com/bagder/%{name}/archive/master.tar.gz
Source1:             https://github.com/google/%{realname}/releases/download/v0.5.2/Brotli-0.5.2.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       gcc make libtool automake autoconf

###############################################################################

%description 
Wrapper around the brotli code base.

###############################################################################

%package devel
Summary:             Header files and libraries for libbrotli C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel 
The %{name}-devel package contains the header files and 
libraries to develop applications using a Brotli compression.

###############################################################################

%prep
%setup -qn %{name}-master
%{__tar} xzvf %{SOURCE1}

rm -rf brotli
mv Brotli-%{version} %{realname}

%build

# Set paths to headers
sed -i "s#brotli/include/brotli/decode.h#brotli/dec/decode.h#" configure.ac
sed -i 's#brotli/include/brotli/decode.h#brotli/dec/decode.h#' Makefile.am
sed -i 's#brotli/include/brotli/encode.h#brotli/enc/encode.h#' Makefile.am
sed -i 's#brotli/include/brotli/types.h#brotli/common/types.h#' Makefile.am

mkdir m4
autoreconf --install --force --symlink

%{configure}

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -f %{buildroot}%{_libdir}/*.la

%clean 
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}enc.so.1.0.0
%{_libdir}/%{name}dec.so.1.0.0
%{_libdir}/%{name}enc.so.1
%{_libdir}/%{name}dec.so.1

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{realname}/*
%{_libdir}/%{name}enc.so
%{_libdir}/%{name}dec.so
%{_libdir}/%{name}enc.a
%{_libdir}/%{name}dec.a
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Wed Oct 05 2016 Anton Novojilov <andy@essentialkaos.com> - 0.5.2-0
- Initial build for kaos repository
