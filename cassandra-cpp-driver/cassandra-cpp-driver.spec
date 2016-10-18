###############################################################################

%define short_name    cpp-driver

###############################################################################

Summary:              DataStax C/C++ Driver for Apache Cassandra
Name:                 cassandra-cpp-driver
Version:              2.4.3
Release:              0%{?dist}
License:              APLv2.0
Group:                Development/Libraries
URL:                  http://datastax.github.io/cpp-driver

Source0:              https://github.com/datastax/%{short_name}/archive/%{version}.tar.gz
Source1:              cassandra.pc.in
Source2:              cassandra_static.pc.in

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        cmake >= 2.6.4 libuv-devel >= 1.9.1

Requires(post):       /sbin/ldconfig
Requires(postun):     /sbin/ldconfig

###############################################################################

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra using exclusively Cassandra's native protocol and Cassandra Query
Language.

###############################################################################

%package devel
Summary:              Development libraries for ${name}
Group:                Development/Tools

Requires:             %{name} = %{version}-%{release}
Requires:             libuv >= 1.9.1 
Requires:             pkgconfig

%description devel
Development libraries for %{name}

###############################################################################

%prep
%setup -qn %{short_name}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
cmake -DCMAKE_BUILD_TYPE=RELEASE \
      -DCASS_BUILD_STATIC=ON \
      -DCASS_INSTALL_PKG_CONFIG=OFF \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} .

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{make_install} DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_libdir}/pkgconfig

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}/%{_libdir}/pkgconfig/cassandra.pc

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}/%{_libdir}/pkgconfig/cassandra_static.pc

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
%doc README.md LICENSE.txt
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 2.4.3-0 
- Initial build. 

