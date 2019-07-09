################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
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

################################################################################

%define __ldconfig        %{_sbin}/ldconfig
%define __service         %{_sbin}/service
%define __touch           %{_bin}/touch
%define __chkconfig       %{_sbin}/chkconfig
%define __updalt          %{_sbindir}/update-alternatives
%define __useradd         %{_sbindir}/useradd
%define __groupadd        %{_sbindir}/groupadd
%define __getent          %{_bindir}/getent
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define _noarch_libdir           %{_libdir32}
%define _zookeeper_noarch_libdir %{_noarch_libdir}/zookeeper
%define _maindir                 %{buildroot}%{_zookeeper_noarch_libdir}

%define service_name             zookeeper

%define zookeeper_user           zookeeper
%define zookeeper_group          zookeeper
%define zookeeper_uid            65529
%define zookeeper_gid            65529

################################################################################

Summary:              High-performance coordination service for distributed applications
Name:                 zookeeper
Version:              3.4.10
Release:              0%{?dist}
License:              ASL 2.0
Group:                Applications/Databases
URL:                  https://zookeeper.apache.org

Source0:              http://mirror.cogentco.com/pub/apache/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz

Source1:              %{name}.init
Source2:              %{name}.service
Source3:              zkcli
Source4:              %{name}.logrotate
Source5:              %{name}.sysconfig
Source6:              zoo.cfg
Source7:              log4j.properties
Source8:              log4j-cli.properties
Source9:              java.env

BuildRequires:        java-devel
BuildRequires:        tar wget ant ant-junit cppunit-doc
BuildRequires:        hamcrest-demo hamcrest-javadoc hamcrest patch xz libtool
BuildRequires:        python-devel gcc make libtool autoconf cppunit-devel

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:             logrotate nc libzookeeper

%if 0%{?rhel} <= 6
Requires(post):       chkconfig initscripts
Requires(pre):        chkconfig initscripts
%endif
%if 0%{?rhel} >= 7
Requires(post):       systemd
Requires(pre):        systemd
%endif

Provides:             %{name} = %{version}-%{release}
AutoReqProv:          no

################################################################################

%description
ZooKeeper is a distributed, open-source coordination service for distributed
applications. It exposes a simple set of primitives that distributed
applications can build upon to implement higher level services for
synchronization, configuration maintenance, and groups and naming. It is
designed to be easy to program to, and uses a data model styled after the
familiar directory tree structure of file systems. It runs in Java and has
bindings for both Java and C.

Coordination services are notoriously hard to get right. They are especially
prone to errors such as race conditions and deadlock. The motivation behind
ZooKeeper is to relieve distributed applications the responsibility of
implementing coordination services from scratch.

################################################################################

%package -n libzookeeper
Summary:              C client interface to zookeeper server
Group:                Development/Libraries
BuildRequires:        gcc

%description -n libzookeeper
The client supports two types of APIs -- synchronous and asynchronous.

Asynchronous API provides non-blocking operations with completion callbacks and
relies on the application to implement event multiplexing on its behalf.

On the other hand, Synchronous API provides a blocking flavor of
zookeeper operations and runs its own event loop in a separate thread.

Sync and Async APIs can be mixed and matched within the same appliction.

################################################################################

%package -n libzookeeper-devel
Summary:              Headers and static libraries for libzookeeper
Group:                Development/Libraries
Requires:             gcc

%description -n libzookeeper-devel
This package contains the libraries and header files needed for
developing with libzookeeper.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
ant compile_jute

pushd src/c
  rm -rf aclocal.m4 autom4te.cache/ config.guess config.status config.log \
    config.sub configure depcomp install-sh ltmain.sh libtool \
    Makefile Makefile.in missing stamp-h1 compile
  autoheader
  libtoolize --force
  aclocal
  automake -a
  autoconf
  autoreconf
  %configure
  %{__make} %{?_smp_mflags}
popd

ant jar

%install
rm -rf %{buildroot}

%{make_install} -C src/c

install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_sbindir}
install -dm 0755 %{buildroot}%{_sysconfdir}/zookeeper
install -dm 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -dm 0755 %{buildroot}%{_localstatedir}/log/%{name}
install -dm 0755 %{buildroot}%{_localstatedir}/lib/%{name}
install -dm 0755 %{buildroot}%{_datadir}/%{name}
install -dm 0755 %{buildroot}%{_zookeeper_noarch_libdir}
%if 0%{?rhel} <= 6
install -dm 0755 %{buildroot}%{_initrddir}
%endif

%if 0%{?rhel} >= 7
install -dm 0755 %{buildroot}%{_unitdir}
install -dm 0755 %{buildroot}%{_unitdir}/%{name}.service.d
%endif

cp -a bin %{buildroot}%{_zookeeper_noarch_libdir}
cp build/lib/*.jar %{buildroot}%{_zookeeper_noarch_libdir}

install -pm 0644 build/%{name}-%{version}.jar %{buildroot}%{_zookeeper_noarch_libdir}/%{name}-%{version}.jar
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -pm 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}/zoo.cfg
install -pm 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/%{name}/log4j.properties
install -pm 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/%{name}/log4j-cli.properties
install -pm 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/%{name}/java.env
install -pm 0644 conf/configuration.xsl %{buildroot}%{_sysconfdir}/%{name}/configuration.xsl

%if 0%{?rhel} <= 6
install -pm 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{service_name}
%endif

%if 0%{?rhel} >= 7
install -pm 0755 %{SOURCE2} %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE3} %{buildroot}%{_bindir}/zookeeper-client

CLASSPATH=
for i in %{buildroot}%{_zookeeper_noarch_libdir}/*.jar ; do
  CLASSPATH="%{_zookeeper_noarch_libdir}/$(basename ${i}):${CLASSPATH}"
done
echo "[Service]" > %{buildroot}%{_unitdir}/%{name}.service.d/classpath.conf
echo "Environment=CLASSPATH=${CLASSPATH}" >> %{buildroot}%{_unitdir}/%{name}.service.d/classpath.conf
%endif

%clean
rm -rf %{buildroot}

################################################################################

%pre
if [[ $1 -eq 1 ]] ; then
  %{__getent} group %{zookeeper_group} >/dev/null || %{__groupadd} -o -g %{zookeeper_gid} -r %{zookeeper_group}
  %{__getent} passwd %{zookeeper_user} >/dev/null || \
    %{__useradd} -M -n -o -r -d %{_zookeeper_noarch_libdir} -u %{zookeeper_uid} -s /sbin/nologin %{zookeeper_user}
fi

%post
if [[ $1 -eq 1 ]] ; then
%if 0%{?rhel} <= 6
  %{__chkconfig} --add %{service_name} &>/dev/null || :
%endif
%if 0%{?rhel} >= 7
  %{__systemctl} daemon-reload %{name}.service &>/dev/null || :
  %{__systemctl} preset %{name}.service &>/dev/null || :
%endif
fi

%post -n lib%{name}
%{__ldconfig}

%post -n lib%{name}-devel
%{__ldconfig}

%preun
if [[ $1 -eq 0 ]] ; then
%if 0%{?rhel} <= 6
  %{__service} %{service_name} stop &>/dev/null || :
  %{__chkconfig} --del %{service_name} &>/dev/null || :
%endif
%if 0%{?rhel} >= 7
  %{__systemctl} --no-reload disable %{name}.service &>/dev/null || :
  %{__systemctl} stop %{name}.service &>/dev/null || :
%endif
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.txt
%doc docs recipes
%dir %attr(0750,%{zookeeper_user},%{zookeeper_group}) %{_localstatedir}/lib/%{name}
%dir %attr(0750,%{zookeeper_user},%{zookeeper_group}) %{_localstatedir}/log/%{name}
%{_zookeeper_noarch_libdir}
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?rhel} <= 6
%{_initrddir}/%{service_name}
%endif
%if 0%{?rhel} >= 7
%attr(755,root,root) %{_bindir}/zookeeper-client
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.service.d/classpath.conf
%endif

%files -n lib%{name}
%defattr(-, root, root, -)
%doc src/c/README src/c/LICENSE
%{_libdir}/lib%{name}_mt.so.*
%{_libdir}/lib%{name}_st.so.*

%files -n lib%{name}-devel
%defattr(-, root, root, -)
%{_includedir}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

################################################################################

%changelog
* Mon Aug 07 2017 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.4.10-0
- Updated to the latest release
- Improved RPM spec

* Tue Dec 09 2014 Anton Novojilov <andy@essentialkaos.com> - 3.4.6-0
- Initial build
