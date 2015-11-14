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

Summary:            Tool for checking common errors in RPM packages
Name:               rpmlint
Version:            1.8
Release:            0%{?dist}
License:            GPLv2
Group:              Development/Tools
URL:                https://github.com/rpm-software-management/rpmlint

Source0:            https://github.com/rpm-software-management/%{name}/archive/%{name}-%{version}.tar.gz
Source1:            %{name}.config
Source2:            RhelCheck.py

BuildArch:          noarch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      python rpm-python sed

Requires:           python rpm-python python-magic python-enchant cpio binutils
Requires:           desktop-file-utils gzip bzip2 xz

Provides:           %{name} = %{version}-%{release}

###############################################################################

%description

rpmlint is a tool for checking common errors in rpm packages. rpmlint can be 
used to test individual packages before uploading or to check an entire 
distribution. By default all applicable checks are performed but specific 
checks can be performed by using command line parameters.

rpmlint can check binary rpms (files and installed ones), source rpms, and 
plain specfiles, but all checks do not apply to all argument types. For 
best check coverage, run rpmlint on source rpms instead of plain specfiles, 
and installed binary rpms instead of uninstalled binary rpm files.

###############################################################################

%prep
%setup -qn %{name}-%{name}-%{version}

sed -i -e /MenuCheck/d Config.py
cp -p config config.example

install -pm 644 %{SOURCE2} RhelCheck.py

%build
%{__make} %{?_smp_mflags} COMPILE_PYC=1

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot} \
                  ETCDIR=%{_sysconfdir} \
                  MANDIR=%{_mandir} \
                  LIBDIR=%{_datadir}/rpmlint \
                  BINDIR=%{_bindir}

install -pm 644 %{SOURCE1} %{buildroot}%{_datadir}/rpmlint/config

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc COPYING INSTALL config.example
%config(noreplace) %{_sysconfdir}/rpmlint/
%{_sysconfdir}/bash_completion.d/
%{_bindir}/rpmdiff
%{_bindir}/rpmlint
%{_datadir}/rpmlint/
%{_mandir}/man1/rpmlint.1*
%{_mandir}/man1/rpmdiff.1*

###############################################################################

%changelog
* Sat Nov 14 2015 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- Initial build
