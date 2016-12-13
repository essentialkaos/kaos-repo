###############################################################################

# rpmbuilder:github yandex-load:phantom
# rpmbuilder:revision f703e5113f5801d295ebedc6bbbfb63941014ed4

###############################################################################

Summary:              I/O engine with some modules
Name:                 phantom
Version:              0.14.0
Release:              0%{?dist}
License:              LGPL
Group:                Applications/System
URL:                  https://github.com/yandex-load/phantom

Source:               %{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} <= 6
BuildRequires:        devtoolset-2-gcc-c++ make devtoolset-2-binutils
%else
BuildRequires:        gcc-c++ make
%endif

BuildRequires:        openssl-devel binutils-devel

Requires:             openssl binutils

###############################################################################

%description
I/O engine and load generator for Yandex.Tank.

###############################################################################

%prep
%setup -q

%build
%if 0%{?rhel} <= 6
export PATH="/opt/rh/devtoolset-2/root/usr/bin:$PATH"
%endif
%{__make} %{?_smp_mflags} -R all

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mv bin/%{name} %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING README.ru
%{_bindir}/%{name}

###############################################################################

%changelog
* Mon Dec 12 2016 Gleb Goncharov <ggoncharov@fun-box.ru> - 0.14.0-0
- Initial build.

