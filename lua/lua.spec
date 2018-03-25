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

%define lua_major    5.3
%define lua_release  4

################################################################################

Summary:            Powerful light-weight programming language
Name:               lua
Version:            %{lua_major}.%{lua_release}
Release:            0%{?dist}
License:            MIT
Group:              Development/Languages
URL:                http://www.lua.org

Source0:            http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:            %{name}.pc

Patch0:             %{name}-Makefile.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make gcc readline-devel ncurses-devel

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

################################################################################

%package devel

Summary:            Development files for %{name}
Group:              System Environment/Libraries

Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description devel
This package contains development files for %{name}.

################################################################################

%package static
Summary:        Static library for %{name}
Group:          System Environment/Libraries

Requires:       %{name} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.

################################################################################

%prep
%setup -q

%patch0 -p1

%build
sed -i "s/{{MAJOR_VERSION}}/%{lua_major}/" src/Makefile
sed -i "s/{{RELEASE}}/%{lua_release}/" src/Makefile

make %{?_smp_mflags} LIBS="-lm -ldl -lreadline -lncurses" \
                     luac_LDADD="liblua.la -lm -ldl -lreadline -lncurses" \
                     linux

%install
rm -rf %{buildroot}

%{make_install} INSTALL_TOP=%{buildroot}%{_prefix}

install -dm 755 %{buildroot}%{_libdir}/%{name}/5.3
install -dm 755 %{buildroot}%{_datadir}/%{name}/5.3
install -dm 755 %{buildroot}%{_libdir}/pkgconfig

install -pm 644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/

sed -i "s/{{MAJOR_VERSION}}/%{lua_major}/" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i "s/{{FULL_VERSION}}/%{version}/" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

ln -sf liblua-%{lua_major}.so %{buildroot}%{_libdir}/liblua.so

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua*
%{_libdir}/liblua-*.so
%{_mandir}/man1/lua*.1*
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.3
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.3


%files devel
%defattr(-,root,root,-)
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

################################################################################

%changelog
* Sun Mar 25 2018 Anton Novojilov <andy@essentialkaos.com> - 5.3.4-0
- Initial build for kaos repository
