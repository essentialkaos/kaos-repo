################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _lib32            %{_posixroot}lib
%define _libdir32         %{_prefix}%{_lib32}

################################################################################

Summary:           Package replacement plugin for Yum
Name:              yum-plugin-replace
Version:           0.2.7
Release:           0%{?dist}
License:           GPLv2+
Group:             System Environment/Base
URL:               https://github.com/iuscommunity/yum-plugin-replace

Source0:           https://github.com/iuscommunity/%{name}/archive/%{version}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:         noarch

Requires:          yum

Provides:          %{name} = %{version}-%{release}

################################################################################

%description
This plugin enables the ability to replace an installed package, with another
package that provides the same thing.  It was developed specifically for the
IUS Community Project whose packages have alternative names as to not
automatically upgrade stock packages.  They also do not Obsolete the packages
they provide, therefore making upgrading a little bit more tedious.  For
example upgrading 'mysql' to 'mysql50' or 'mysql51' requires first
uninstalling 'mysql' and then installing the alternate package name.

################################################################################

%prep
%{crc_check}

%setup -qn %{name}-%{version}

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir32}/yum-plugins/
install -dm 755 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/

install -pm 0644 etc/yum/pluginconf.d/replace.conf \
                 %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
install -pm 0644 lib/yum-plugins/replace.py \
                 %{buildroot}%{_libdir32}/yum-plugins/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README LICENSE ChangeLog
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/replace.conf
%{_libdir32}/yum-plugins/replace.py*

################################################################################

%changelog
* Wed Sep 03 2014 Anton Novojilov <andy@essentialkaos.com> - 0.2.7-0
- Initial build for kaos repository
