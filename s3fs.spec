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

Summary:            FUSE-based file system backed by Amazon S3
Name:               s3fs
Version:            1.71
Release:            0%{?dist}
License:            GNU GPL v2
Group:              Development/Tools
URL:                https://code.google.com/p/s3fs/

Source0:            https://s3fs.googlecode.com/files/%{name}-%{version}.tar.gz

BuildArch:          x86_64 i386
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc gcc-c++ libstdc++-devel fuse >= 2.8.4 fuse-devel curl-devel libxml2-devel openssl-devel mailcap

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description

FUSE-based file system backed by Amazon S3. Mount a bucket as a local 
file system read/write. Store files/folders natively and transparently.

###############################################################################

%prep
%setup -q 

%build
%{_configure} --prefix=%{_prefix}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{make_install}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)

###############################################################################

%changelog
* Mon Jun 17 2013 Anton Novojilov <andy@essentialkaos.com> - 1.71-0
- Updated to upstream version