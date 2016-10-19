###############################################################################

%define cpp_driver_name     cpp-driver
%define cpp_driver_version  2.4.3

%define short_name          erlcass

###############################################################################

Summary:              An Erlang Cassandra driver
Name:                 lib%{short_name}
Version:              2.6
Release:              0%{?dist}
License:              APLv2.0
Group:                Development/Libraries
URL:                  https://github.com/silviucpp/erlcass

Source0:              https://github.com/silviucpp/%{short_name}/archive/v%{version}.tar.gz
Source1:              https://github.com/datastax/%{cpp_driver_name}/archive/%{cpp_driver_version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        automake cmake >= 2.6.4 devtoolset-2-gcc-c++ libtool
BuildRequires:        libuv-devel >= 1.9.1 openssl-devel erlang18-devel
BuildRequires:        cassandra-cpp-driver-devel = %{cpp_driver_version}

Requires(post):       /sbin/ldconfig
Requires(postun):     /sbin/ldconfig

###############################################################################

%description
An Erlang Cassandra driver, based on DataStax C++ driver focused on 
performance.

###############################################################################

%prep
%setup -qn %{short_name}-%{version}

mkdir -p _build/deps
%{__tar} xvfz %{SOURCE1} -C _build/deps

# Disable dependencies build
sed -i '/build_deps.sh/d' Makefile

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir}

mv priv/erlcass_nif.so %{buildroot}%{_libdir}/erlcass_nif.so

ln -s %{_libdir}/erlcass_nif.so %{buildroot}%{_libdir}/liberlcass_nif.so

%clean
rm -rf %{buildroot}

###############################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

###############################################################################

%files
%defattr(-,root,root)
%doc README.md
%{_libdir}/*.so

###############################################################################

%changelog
* Wed Oct 19 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.6-0
- Initial build
