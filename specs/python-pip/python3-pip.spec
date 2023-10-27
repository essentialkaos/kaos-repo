################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_base python36
%global __python3   %{_bindir}/python3.6

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

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

################################################################################

%define pkgname  pip

%define python_wheelname %{pkgname}-%{version}-py3-none-any.whl
%define python_wheeldir  %{_datadir}/python-wheels

################################################################################

Summary:         Tool for installing and managing Python packages
Name:            %{python_base}-%{pkgname}
Version:         21.3.1
Release:         0%{?dist}
License:         MIT
Group:           Development/Tools
URL:             https://github.com/pypa/pip

Source0:         https://github.com/pypa/%{pkgname}/archive/%{version}.tar.gz

Source100:       checksum.sha512

BuildArch:       noarch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   %{python_base}-setuptools %{python_base}-devel

Requires:        %{python_base}-setuptools %{python_base}-devel

Provides:        pip3 = %{version}-%{release}
Provides:        python3-pip = %{version}-%{release}
Provides:        %{name} = %{version}-%{release}

################################################################################

%description
pip is a tool for installing and managing Python packages, such as those found
in the Python Package Index. It’s a replacement for easy_install.

################################################################################

%package wheel
Summary:         The pip wheel

Group:           Development/Tools

BuildRequires:   %{python_base}-pip %{python_base}-wheel

Requires:        %{python_base}-%{pkgname} = %{version}
Requires:        ca-certificates

%description wheel
A Python wheel of pip to use with venv.

################################################################################

%prep
%{crc_check}

%setup -qn %{pkgname}-%{version}

# Remove Windows binaries
rm -f -v src/pip/_vendor/distlib/*.exe
sed -i '/\.exe/d' setup.py

%build
%{__python3} setup.py bdist_wheel

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

rm -rf %{buildroot}%{_bindir}/%{pkgname}-*

pip3 install -I dist/%{python_wheelname} \
             --root %{buildroot} \
             --no-index \
             --no-deps \
             --no-cache-dir \
             --no-warn-script-location \
             --disable-pip-version-check \
             --ignore-installed \
             --find-links dist \
             --verbose

mkdir -p %{buildroot}%{python_wheeldir}
install -p dist/%{python_wheelname} -t %{buildroot}%{python_wheeldir}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-, root, root, -)
%doc docs AUTHORS.txt LICENSE.txt MANIFEST.in README.rst
%attr(755, root, root) %{_bindir}/%{pkgname}*
%{python3_sitelib}/%{pkgname}*

%files wheel
%defattr(-, root, root, -)
%{python_wheeldir}/%{python_wheelname}

################################################################################

%changelog
* Mon Oct 24 2022 Anton Novojilov <andy@essentialkaos.com> - 21.3.1-0
https://pip.pypa.io/en/stable/news/#v21-3-1

* Tue Oct 01 2019 Anton Novojilov <andy@essentialkaos.com> - 18.1-3
- Added patch for stripping prefix from script paths in wheel RECORD
- Added wheel package for CentOS 7

* Thu Sep 19 2019 Anton Novojilov <andy@essentialkaos.com> - 18.1-2
- Fixed compatibility with the latest version of Python 3 package

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 18.1-1
- Updated for compatibility with Python 3.6

* Wed Nov 28 2018 Anton Novojilov <andy@essentialkaos.com> - 18.1-0
- https://pip.pypa.io/en/stable/news/#v18-1

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 18.0-0
- https://pip.pypa.io/en/stable/news/#v18-0

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 10.0.1-0
- https://pip.pypa.io/en/stable/news/#v10-0-1

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 10.0.0-0
- https://pip.pypa.io/en/stable/news/#v10-0-0

* Tue Jun 19 2018 Anton Novojilov <andy@essentialkaos.com> - 9.0.3-0
- https://pip.pypa.io/en/stable/news/#v9-0-3

* Wed Nov 09 2016 Anton Novojilov <andy@essentialkaos.com> - 9.0.1-0
- https://pip.pypa.io/en/stable/news/#v9-0-1

* Sun Jun 19 2016 Anton Novojilov <andy@essentialkaos.com> - 8.1.2-0
- https://pip.pypa.io/en/stable/news/#v8-1-2

* Sun Mar 20 2016 Gleb Goncharov <yum@gongled.ru> - 8.1.1-0
- https://pip.pypa.io/en/stable/news/#v8-1-1
