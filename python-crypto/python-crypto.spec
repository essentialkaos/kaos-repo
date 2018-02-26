################################################################################

%global pythonver %(python -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}

# Python3 introduced in Fedora 13
%global with_python3 %([ 0%{?fedora} -gt 12 ] && echo 1 || echo 0)

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

################################################################################

Summary:          Cryptography library for Python
Name:             python-crypto
Version:          2.6.1
Release:          0%{?dist}
License:          Public Domain and Python
Group:            Development/Libraries
URL:              http://www.pycrypto.org

Source0:          http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz

Patch0:           python-crypto-2.4-optflags.patch
Patch1:           python-crypto-2.4-fix-pubkey-size-divisions.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    python2-devel >= 2.2 gmp-devel >= 4.1

%if %{with_python3}
BuildRequires:    python-tools python3-devel
%endif

%{?filter_provides_in: %filter_provides_in %{python_sitearch}/Crypto/.*\.so}
%if %{with_python3}
%{?filter_provides_in: %filter_provides_in %{python3_sitearch}/Crypto/.*\.so}
%endif
%{?filter_setup}

Provides:         pycrypto = %{version}-%{release}

################################################################################

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

################################################################################

%if %{with_python3}
%package -n python3-crypto
Summary:          Cryptography library for Python 3
Group:            Development/Libraries

%description -n python3-crypto
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This is the Python 3 build of the package.
%endif

################################################################################

%prep
%setup -n pycrypto-%{version} -q

%patch0 -p1
%patch1 -p1

%if %{with_python3}
cp -a . %{py3dir}
2to3 -wn %{py3dir}/pct-speedtest.py
%endif

%build
CFLAGS="%{optflags} -fno-strict-aliasing" python setup.py build

%if %{with_python3}
pushd %{py3dir}
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
python setup.py install -O1 --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python_sitearch} -name '*.so' -exec chmod -c g-w {} \;

%if %{with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
find %{buildroot}%{python3_sitearch} -name '*.so' -exec chmod -c g-w {} \;
%endif

# See if there's any egg-info
if [[ -f %{buildroot}%{python_sitearch}/pycrypto-%{version}-py%{pythonver}.egg-info ]] ; then
  echo %{python_sitearch}/pycrypto-%{version}-py%{pythonver}.egg-info > egg-info
fi

find %{buildroot} -name '_fastmath.*' -exec rm -f {} \;

%clean
rm -rf %{buildroot}

################################################################################

%files -f egg-info
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LEGAL/ COPYRIGHT Doc/
%{python_sitearch}/Crypto/

%if %{with_python3}
%files -n python3-crypto
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LEGAL/ COPYRIGHT Doc/
%{python3_sitearch}/Crypto/
%{python3_sitearch}/pycrypto-*py3.*.egg-info
%endif

################################################################################

%changelog
* Thu Oct 22 2015 Gleb Goncharov <inbox@gongled.ru> - 2.6.1-0
- Initial build
