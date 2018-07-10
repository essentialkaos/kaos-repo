################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

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
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd

%define pkgname           pycrypto
%define pypi_subpath      60/db/645aa9af249f059cc3a368b118de33889219e0362141e75d4eaf6f80f163

################################################################################

Summary:          Cryptography library for Python 3.4
Name:             python34-crypto
Version:          2.6.1
Release:          1%{?dist}
License:          Public Domain and Python
Group:            Development/Libraries
URL:              http://www.pycrypto.org

Source0:          https://pypi.python.org/packages/%{pypi_subpath}/%{pkgname}-%{version}.tar.gz

Patch0:           python-crypto-2.4-optflags.patch
Patch1:           python-crypto-2.4-fix-pubkey-size-divisions.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    gcc python34-devel gmp-devel >= 4.1

%{?filter_provides_in: %filter_provides_in %{python3_sitearch}/Crypto/.*\.so}

%{?filter_setup}

Requires:         python34

Provides:         pycrypto34 = %{version}-%{release}

################################################################################

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

################################################################################

%prep
%setup -qn %{pkgname}-%{version}

%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python3} setup.py build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python3_sitearch} -name '*.so' -exec chmod -c g-w {} \;

find %{buildroot} -name '_fastmath.*' -exec rm -f {} \;

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LEGAL/ COPYRIGHT Doc/
%{python3_sitearch}/Crypto/
%{python3_sitearch}/pycrypto-*py3.*.egg-info

################################################################################

%changelog
* Mon Mar 05 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.1-1
- Rebuilt for Python 3.4
