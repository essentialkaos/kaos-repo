################################################################################

%define cpp_driver_name     cpp-driver
%define cpp_driver_version  2.6.0

%define short_name          erlcass

################################################################################

Summary:              An Erlang Cassandra driver
Name:                 lib%{short_name}
Version:              2.7
Release:              0%{?dist}
License:              APLv2.0
Group:                Development/Libraries
URL:                  https://github.com/silviucpp/erlcass

Source0:              https://github.com/silviucpp/%{short_name}/archive/v%{version}.tar.gz
Source1:              https://github.com/datastax/%{cpp_driver_name}/archive/%{cpp_driver_version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        make cmake libuv-devel >= 1.9.1
BuildRequires:        erlang18-erl_interface erlang18-devel openssl-devel
BuildRequires:        cassandra-cpp-driver-devel = %{cpp_driver_version}

%if 0%{?rhel} >= 7
BuildRequires:        gcc-c++
%else
BuildRequires:        devtoolset-2-gcc-c++
%endif

Requires(post):       /sbin/ldconfig
Requires(postun):     /sbin/ldconfig

################################################################################

%description
An Erlang Cassandra driver, based on DataStax C++ driver focused on
performance.

################################################################################

%prep
%setup -qn %{short_name}-%{version}

mkdir -p _build/deps
tar xvfz %{SOURCE1} -C _build/deps

# Fix build error with non existent header file
sed -i '/#include "external_types.hpp"/d' c_src/nif_cass_statement.cc

%build
export PATH="/opt/rh/devtoolset-2/root/usr/bin:$PATH"

mv _build/deps/%{cpp_driver_name}-%{cpp_driver_version} _build/deps/%{cpp_driver_name}

# Generate cassconfig.hpp
pushd _build/deps/%{cpp_driver_name}
cmake .
popd

%{__make} -C c_src %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir}

mv priv/erlcass_nif.so %{buildroot}%{_libdir}/erlcass_nif.so

ln -s %{_libdir}/erlcass_nif.so %{buildroot}%{_libdir}/liberlcass_nif.so

%clean
rm -rf %{buildroot}

################################################################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root)
%doc README.md
%{_libdir}/*.so

################################################################################

%changelog
* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 2.7-0
- Updated to latest stable release

* Wed Oct 19 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.6-0
- Initial build
