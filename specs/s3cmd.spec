################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global python_ver %(%{__python3} -c "import sys; print('{0}.{1}'.format(sys.version_info.major,sys.version_info.minor))" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 2>/dev/null)}

################################################################################

Summary:        Command line tool for managing Amazon S3 and CloudFront services
Name:           s3cmd
Version:        2.3.0
Release:        0%{?dist}
Group:          Applications/System
License:        GPL
URL:            https://github.com/s3tools/s3cmd

Source0:        https://github.com/s3tools/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python3-devel

Requires:       python3 python3-dateutil python3-magic

Provides:       %{name} = %{version}-%{release}

################################################################################

%description
S3cmd lets you copy files from/to Amazon S3 (Simple Storage Service) using a
simple to use command line client. Supports rsync-like backup, GPG encryption,
and more. Also supports management of Amazons CloudFront content delivery
network.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
export S3CMD_PACKAGING=1
%{__python3} setup.py build

%install
rm -rf %{buildroot}

export S3CMD_PACKAGING=1
%{__python3} setup.py install --root=%{buildroot} --prefix=%{_prefix}

ln -sf %{name} %{buildroot}%{_bindir}/s3

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md NEWS LICENSE
%{_bindir}/s3
%{_bindir}/s3cmd
%{python3_sitelib}/*

################################################################################

%changelog
* Sun Dec 04 2022 Anton Novojilov <andy@essentialkaos.com> - 2.3.0-0
- https://github.com/s3tools/s3cmd/releases/tag/v2.3.0

* Wed Sep 12 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.2-0
- https://github.com/s3tools/s3cmd/releases/tag/v2.0.2

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 2.0.1-0
- https://github.com/s3tools/s3cmd/releases/tag/v2.0.1

* Thu Mar 10 2016 Gleb Goncharov <yum@gongled.ru> - 1.6.1-1
- Fixed incompatibility with CentOS/RHEL 7.x

* Thu Feb 04 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.1-0
- https://github.com/s3tools/s3cmd/releases/tag/v1.6.1

* Thu Oct 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- https://github.com/s3tools/s3cmd/releases/tag/v1.6.0

* Thu Mar 05 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- https://github.com/s3tools/s3cmd/releases/tag/v1.5.2

* Tue Jan 27 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- https://github.com/s3tools/s3cmd/releases/tag/v1.5.0

* Wed Aug 20 2014 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-rc1
- Updated to release candidate 1

* Sat Dec 21 2013 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-b1
- Initial build
