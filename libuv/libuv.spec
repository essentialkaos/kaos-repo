###############################################################################

Summary:              Cross-platform asychronous I/O 
Name:                 libuv
Version:              1.9.1
Release:              0%{?dist}
License:              MIT, BSD and ISC
Group:                Development/Tools
URL:                  http://http://libuv.org/

Source0:              http://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
Source1:              %{name}.pc.in

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        autoconf >= 2.59 automake >= 1.9.6 libtool >= 1.5.22

Requires(post):       /sbin/ldconfig
Requires(postun):     /sbin/ldconfig

###############################################################################

%description
A multi-platform support library with a focus on asynchronous I/O. 
It was primarily developed for use by Node.js, but it’s also used by Luvit, 
Julia, pyuv, and others.

###############################################################################

%package devel
Summary:              Development libraries for libuv
Group:                Development/Tools

Requires:             %{name} = %{version}-%{release}
Requires:             pkgconfig

Requires(post):       /sbin/ldconfig
Requires(postun):     /sbin/ldconfig

%description devel
Development libraries for libuv

###############################################################################

%prep
%setup -qn %{name}-v%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
./autogen.sh
%configure
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
    %SOURCE1 > %{buildroot}/%{_libdir}/pkgconfig/libuv.pc

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
%doc README.md AUTHORS LICENSE
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md AUTHORS LICENSE
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

###############################################################################

%changelog
* Tue Oct 18 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.9.1-0
- Initial build.

