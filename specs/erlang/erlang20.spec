################################################################################

# rpmbuilder:qa-rpaths 0x0001,0x0002

################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
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

%define __sysctl          %{_bindir}/systemctl

################################################################################

#define __cputoolize true
%define _disable_ld_no_undefined 1

%if 0%{?rhel} >= 7
%{!?systemd_enabled:%global systemd_enabled 1}
%else
%{!?systemd_enabled:%global systemd_enabled 0}
%endif

################################################################################

%define elibdir           %{_libdir}/erlang/lib
%define eprefix           %{_prefix}%{_lib32}
%define ver_maj           20
%define ver_min           3
%define ver_patch         8.25
%define ver_suffix        %{ver_min}.%{ver_patch}
%define ver_string        %{ver_maj}.%{ver_suffix}

%define realname          erlang

%define libre_ver         2.9.2

################################################################################

Summary:           General-purpose programming language and runtime environment
Name:              %{realname}%{ver_maj}
Version:           %{ver_suffix}
Release:           0%{?dist}
Group:             Development/Tools
License:           MPL
URL:               https://www.erlang.org

Source0:           https://github.com/erlang/otp/archive/OTP-%{ver_string}.tar.gz
Source1:           https://www.erlang.org/download/otp_doc_html_%{ver_maj}.%{ver_min}.tar.gz
Source2:           https://www.erlang.org/download/otp_doc_man_%{ver_maj}.%{ver_min}.tar.gz
Source3:           epmd.service
Source4:           epmd.socket
Source5:           epmd@.service
Source6:           epmd@.socket

Source10:          https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-%{libre_ver}.tar.gz

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     ncurses-devel unixODBC-devel tcl-devel make
BuildRequires:     tk-devel flex bison gd-devel gd-devel wxGTK-devel libxslt
BuildRequires:     valgrind-devel fop java-1.8.0-openjdk-devel
BuildRequires:     lksctp-tools-devel

BuildRequires:     devtoolset-3-gcc-c++ devtoolset-3-binutils

Requires:          tk tcl

Requires:          %{name}-base = %{version}-%{release}
Requires:          %{name}-common_test = %{version}
Requires:          %{name}-compiler = %{version}
Requires:          %{name}-crypto = %{version}
Requires:          %{name}-debugger = %{version}
Requires:          %{name}-dialyzer = %{version}
Requires:          %{name}-diameter = %{version}
Requires:          %{name}-edoc = %{version}
Requires:          %{name}-eldap = %{version}
Requires:          %{name}-erl_docgen = %{version}
Requires:          %{name}-erl_interface = %{version}
Requires:          %{name}-et = %{version}
Requires:          %{name}-eunit = %{version}
Requires:          %{name}-hipe = %{version}
Requires:          %{name}-ic = %{version}
Requires:          %{name}-inets = %{version}
Requires:          %{name}-mnesia = %{version}
Requires:          %{name}-observer = %{version}
Requires:          %{name}-os_mon = %{version}
Requires:          %{name}-otp_mibs = %{version}
Requires:          %{name}-parsetools = %{version}
Requires:          %{name}-public_key = %{version}
Requires:          %{name}-reltool = %{version}
Requires:          %{name}-runtime_tools = %{version}
Requires:          %{name}-snmp = %{version}
Requires:          %{name}-ssh = %{version}
Requires:          %{name}-ssl = %{version}
Requires:          %{name}-syntax_tools = %{version}
Requires:          %{name}-tools = %{version}
Requires:          %{name}-typer = %{version}
Requires:          %{name}-xmerl = %{version}

Provides:          %{name} = %{version}-%{release}
Provides:          %{realname} = %{ver_string}-%{release}

Conflicts:         erlang erlangR15 erlangR16 erlang17 erlang18 erlang19 erlang21

################################################################################

%description
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.

################################################################################

%package -n %{name}-stack
Summary:  Erlang bundle
License:  MPL
Group:    Development/Tools

Requires: %{name} = %{version}-%{release}
Requires: %{name}-base = %{version}-%{release}
Requires: %{name}-asn1 = %{version}
Requires: %{name}-common_test = %{version}
Requires: %{name}-compiler = %{version}
Requires: %{name}-cosEvent = %{version}
Requires: %{name}-cosEventDomain = %{version}
Requires: %{name}-cosFileTransfer = %{version}
Requires: %{name}-cosNotification = %{version}
Requires: %{name}-cosProperty = %{version}
Requires: %{name}-cosTime = %{version}
Requires: %{name}-cosTransactions = %{version}
Requires: %{name}-crypto = %{version}
Requires: %{name}-debugger = %{version}
Requires: %{name}-dialyzer = %{version}
Requires: %{name}-diameter = %{version}
Requires: %{name}-edoc = %{version}
Requires: %{name}-eldap = %{version}
Requires: %{name}-emacs = %{version}
Requires: %{name}-erl_docgen = %{version}
Requires: %{name}-erl_interface = %{version}
Requires: %{name}-et = %{version}
Requires: %{name}-eunit = %{version}
Requires: %{name}-hipe = %{version}
Requires: %{name}-ic = %{version}
Requires: %{name}-inets = %{version}
Requires: %{name}-jinterface = %{version}
Requires: %{name}-megaco = %{version}
Requires: %{name}-mnesia = %{version}
Requires: %{name}-observer = %{version}
Requires: %{name}-odbc = %{version}
Requires: %{name}-orber = %{version}
Requires: %{name}-os_mon = %{version}
Requires: %{name}-otp_mibs = %{version}
Requires: %{name}-parsetools = %{version}
Requires: %{name}-public_key = %{version}
Requires: %{name}-reltool = %{version}
Requires: %{name}-runtime_tools = %{version}
Requires: %{name}-snmp = %{version}
Requires: %{name}-ssh = %{version}
Requires: %{name}-ssl = %{version}
Requires: %{name}-syntax_tools = %{version}
Requires: %{name}-tools = %{version}
Requires: %{name}-typer = %{version}
Requires: %{name}-wx = %{version}
Requires: %{name}-xmerl = %{version}

Obsoletes: %{name}-mnesia_session = %{version}-%{release}
Obsoletes: %{name}-mnemosyne = %{version}-%{release}

%description -n %{name}-stack
Full Erlang bundle.

The Erlang/OTP system --- Erlang is a programming language which
has many features more commonly associated with an operating system
than with a programming language: concurrent processes, scheduling,
memory management, distribution, networking, etc. The development package
in addition contains the Erlang sources for all base libraries.
Includes the Erlang/OTP graphical libraries.

################################################################################

%package -n %{name}-base
Summary:   Erlang architecture independent files
License:   MPL
Group:     Development/Tools
Requires:  lksctp-tools
Provides:  %{name}-base = %{version}-%{release}
Obsoletes: %{name}_otp = %{version}-%{release}
Obsoletes: %{name}-gs_apps = %{version}-%{release}
Obsoletes: %{name}-otp_libs = %{version}-%{release}

%if %{systemd_enabled}
BuildRequires:     systemd systemd-devel

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%endif

%description -n %{name}-base
Erlang architecture independent files

The Erlang/OTP system --- Erlang is a programming language which
has many features more commonly associated with an operating system
than with a programming language: concurrent processes, scheduling,
memory management, distribution, networking, etc. The development package
in addition contains the Erlang sources for all base libraries.
Includes the Erlang/OTP graphical libraries.

################################################################################

%package -n %{name}-devel
Summary:  Erlang header
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{name}-devel
Erlang headers.
This package is used to build some library.

################################################################################

%package -n %{name}-manpages
Summary:  Erlang man pages
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-manpages
Documentation for the Erlang programming language in `man` format. This
documentation can be read using the command `erl -man mod`, where 'mod' is
the name of the module you want documentation on.

################################################################################

%package -n %{name}-dialyzer
Summary:  Static analysis tool
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-dialyzer
Dialyzer is a static analysis tool that identifies software discrepancies
such as type errors, unreachable code, unnecessary tests, etc in single
Erlang modules or entire (sets of) applications.

################################################################################

%package -n %{name}-diameter
Summary:  An implementation of the Diameter protocol as defined by RFC 3588
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-diameter
An implementation of the Diameter protocol as defined by RFC 3588.

################################################################################

%package -n %{name}-edoc
Summary:  The Erlang program documentation generator
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Requires: %{name}-syntax_tools
Requires: %{name}-xmerl
Group:    Development/Tools

%description -n %{name}-edoc
This module provides the main user interface to EDoc.

################################################################################

%package -n %{name}-eldap
Summary:  The Erlang LDAP library
License:  MPL
Requires: %{name}-asn1 = %{version}-%{release}
Requires: %{name}-base = %{version}-%{release}
Requires: %{name}-hipe = %{version}-%{release}
Requires: %{name}-ssl = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-eldap
Eldap is a module which provides a client API to the Lightweight Directory
Access Protocol (LDAP).

################################################################################

%package -n %{name}-emacs
Summary:  Emacs support for The Erlang language
License:  GPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools
Requires: emacs

%description -n %{name}-emacs
This module provides Erlang support to Emacs.

################################################################################

%package -n %{name}-jinterface
Summary:  Low level interface to Java
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-jinterface
The Jinterface package provides a set of tools for communication with
Erlang processes. It can also be used for communication with other Java
processes using the same package, as well as C processes using the
Erl_Interface library.

################################################################################

%package -n %{name}-asn1
Summary:  Provides support for Abstract Syntax Notation One
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-asn1
Asn1 application contains modules with compile-time and run-time support for
ASN.1.

################################################################################

%package -n %{name}-common_test
Summary:  Portable framework for automatic testing
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-common_test
A portable Erlang framework for automatic testing.

################################################################################

%package -n %{name}-compiler
Summary:  Byte code compiler for Erlang which produces highly compact code
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-compiler
Compiler application compiles Erlang code to byte-code. The highly compact
byte-code is executed by the Erlang emulator.

################################################################################

%package -n %{name}-cosEvent
Summary:  Orber OMG Event Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosEvent
The cosEvent application is an Erlang implementation of a CORBA Service
CosEvent.

################################################################################

%package -n %{name}-cosEventDomain
Summary:  Orber OMG Event Domain Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosEventDomain
The cosEventDomain application is an Erlang implementation of a CORBA
Service CosEventDomainAdmin.

################################################################################

%package -n %{name}-cosFileTransfer
Summary:  Orber OMG File Transfer Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosFileTransfer
The cosFileTransfer Application is an Erlang implementation of the
OMG CORBA File Transfer Service.

################################################################################

%package -n %{name}-cosNotification
Summary:  Orber OMG Notification Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosNotification
The cosNotification application is an Erlang implementation of the OMG
CORBA Notification Service.

################################################################################

%package -n %{name}-cosProperty
Summary:  Orber OMG Property Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosProperty
The cosProperty Application is an Erlang implementation of the OMG
CORBA Property Service.

################################################################################

%package -n %{name}-cosTime
Summary:  Orber OMG Timer and TimerEvent Services
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosTime
The cosTime application is an Erlang implementation of the OMG
CORBA Time and TimerEvent Services.

################################################################################

%package -n %{name}-cosTransactions
Summary:  Orber OMG Transaction Service
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-cosTransactions
The cosTransactions application is an Erlang implementation of the OMG
CORBA Transaction Service.

################################################################################

%package -n %{name}-crypto
Summary:  Cryptographical support
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-crypto
Cryptographical support for erlang.

################################################################################

%package -n %{name}-debugger
Summary:  Debugger for debugging and testing of Erlang programs
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-debugger
Debugger is a graphical tool which can be used for debugging and testing
of Erlang programs. For example, breakpoints can be set, code can be single
stepped and variable values can be displayed and changed.

################################################################################

%package -n %{name}-erl_docgen
Summary:  Documentation generator
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-erl_docgen
Documentation generator for erlang.

################################################################################

%package -n %{name}-erl_interface
Summary:  Low level interface to C
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-erl_interface
Low level interface to C for erlang.

################################################################################

%package -n %{name}-et
Summary:  Event Tracer
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-et
The Event Tracer (ET) uses the built-in trace mechanism in Erlang and
provides tools for collection and graphical viewing of trace data.

################################################################################

%package -n %{name}-eunit
Summary:  Erlang support for unit testing
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-eunit
Erlang support for unit testing.

################################################################################

%package -n %{name}-hipe
Summary:  High performance erlang
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-hipe
High-performance erlang.

################################################################################

%package -n %{name}-inviso
Summary:  Erlang trace tool
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-inviso
An Erlang trace tool.

################################################################################

%package -n %{name}-ic
Summary:  IDL compiler
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-ic
The IC application is an Erlang implementation of an IDL compiler.

################################################################################

%package -n %{name}-inets
Summary:  Set of services such as a Web server and a ftp client etc
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-inets
Inets is a container for Internet clients and servers. Currently a HTTP
server and a FTP client has been incorporated in Inets. The HTTP server
is an efficient implementation of HTTP 1.1 as defined in RFC 2616, i.e.
a Web server.

################################################################################

%package -n %{name}-megaco
Summary:  Framework for building applications on top of the Megaco/H.248 protocol
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-megaco
Megaco/H.248 is a protocol for control of elements in a physically decomposed
multimedia gateway, enabling separation of call control from media conversion.

################################################################################

%package -n %{name}-mnesia
Summary:  Heavy duty real-time distributed database
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-mnesia
Mnesia is a distributed DataBase Management System (DBMS), appropriate for
telecommunications applications and other Erlang applications which require
continuous operation and exhibit soft real-time properties.

################################################################################

%package -n %{name}-observer
Summary:  Observer, tools for tracing and investigation of distributed systems
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-observer
The OBSERVER application contains tools for tracing and investigation of
distributed systems.

################################################################################

%package -n %{name}-odbc
Summary:  Interface to relational SQL-databases built on ODBC
License:  MPL
Requires:   %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-odbc
The ODBC application is an interface to relational SQL-databases built
on ODBC (Open Database).

################################################################################

%package -n %{name}-orber
Summary:  CORBA Object Request Broker
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-orber
The Orber application is an Erlang implementation of a CORBA Object Request
Broker.

################################################################################

%package -n %{name}-os_mon
Summary:  Monitor which allows inspection of the underlying operating system
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-os_mon
The operating system monitor OS_Mon monitors operating system disk and memory
usage etc.

################################################################################

%package -n %{name}-otp_mibs
Summary:  Snmp management information base for Erlang
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-otp_mibs
The OTP_Mibs application provides an SNMP management information base for
Erlang nodes.

################################################################################

%package -n %{name}-parsetools
Summary:  Set of parsing and lexical analysis tools
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-parsetools
The Parsetools application contains utilities for parsing, e.g. the yecc
module. Yecc is an LALR-1 parser generator for Erlang, similar to yacc.
Yecc takes a BNF grammar definition as input, and produces Erlang code for
a parser as output.

################################################################################

%package -n %{name}-public_key
Summary:  Erlang API to public key infrastructure
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-public_key
Erlang API to public key infrastructure.

################################################################################

%package -n %{name}-reltool
Summary:  A release management tool for Erlang
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-reltool
It analyses a given Erlang/OTP installation and determines various
dependencies between applications. The graphical frontend depicts
the dependencies and enables interactive customization of a
target system. The backend provides a batch interface for
generation of customized target systems.

################################################################################

%package -n %{name}-runtime_tools
Summary:  Runtime tools, tools to include in a production system
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-runtime_tools
Runtime tools, tools to include in a production system.

################################################################################

%package -n %{name}-snmp
Summary:  Simple Network Management Protocol (SNMP) support
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-snmp
A multilingual Simple Network Management Protocol Extensible Agent, featuring
a MIB compiler and facilities for implementing SNMP MIBs etc.

################################################################################

%package -n %{name}-ssh
Summary:  Secure Shell application with ssh and sftp support
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-ssh
Secure Shell application with ssh and sftp support.

################################################################################

%package -n %{name}-ssl
Summary:  Interface to UNIX BSD sockets with Secure Sockets Layer
License:  MPL
Requires: %{name}-base = %{version}-%{release}
Group:    Development/Tools

%description -n %{name}-ssl
The SSL application provides secure communication over sockets.

################################################################################

%package -n %{name}-syntax_tools
Summary:  Set of modules for working with Erlang source code
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-syntax_tools
This package defines an abstract datatype that is compatible with the
erl_parse data structures, and provides modules for analysis and
manipulation, flexible pretty printing, and preservation of source-code
comments. Now includes erl_tidy: automatic code tidying and checking.

################################################################################

%package -n %{name}-tools
Summary:  Set of programming tools including a coverage analyzer etc
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-tools
The Tools application contains a number of stand-alone tools, which are
useful when developing Erlang programs.

################################################################################

%package -n %{name}-typer
Summary:  Type annotator of Erlang code
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-typer
A type annotator of Erlang code.

################################################################################

%package -n %{name}-wx
Summary:  Graphic system for Erlang
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-wx
A Graphics System used to write platform independent user interfaces
for Erlang.

################################################################################

%package -n %{name}-xmerl
Summary:  XML processing tools
License:  MPL
Group:    Development/Tools
Requires: %{name}-base = %{version}-%{release}

%description -n %{name}-xmerl
Implements a set of tools for processing XML documents, as well as working
with XML-like structures in Erlang. The main attraction so far is a
single-pass, highly customizable XML processor. Other components are an
export/translation facility and an XPATH query engine. This version fixes
a few bugs in the scanner, and improves HTML export.

################################################################################

%prep
%{crc_check}

%setup -qn otp-OTP-%{ver_string}

tar xzvf %{SOURCE10}

%build

export CFLAGS="%{optflags} -fPIC"
export CXXLAGS=$CFLAGS

# Use gcc and gcc-c++ from devtoolset
export PATH="/opt/rh/devtoolset-3/root/usr/bin:$PATH"

export BUILDDIR=$(pwd)

### Static LibreSSL build start ###

pushd libressl-%{libre_ver}
  mkdir build
  ./configure --prefix=$(pwd)/build --enable-shared=no
  %{__make} %{?_smp_mflags}
  %{__make} install
popd

### Static LibreSSL build complete ###

export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXLAGS=$CFLAGS
ERL_TOP=`pwd`; export ERL_TOP

./otp_build autoconf

%configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --datadir=%{_datadir} \
  %ifarch x86_64
  --enable-m64-build \
  %endif
  --enable-threads \
  --enable-kernel-poll \
  --enable-hipe \
  --enable-smp-support \
  --enable-sctp \
  %if %{systemd_enabled}
  --enable-systemd \
  %endif
  --enable-builtin-zlib \
  --with-ssl \
  --disable-erlang-mandir \
  --disable-dynamic-ssl-lib \
  --with-ssl=$BUILDDIR/libressl-%{libre_ver}/build \
  --with-ssl-rpath=no

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install} INSTALL_PREFIX=%{buildroot}

%if %{systemd_enabled}
install -d %{buildroot}%{_unitdir}
install -pm 644 %{SOURCE3} %{buildroot}%{_unitdir}/epmd.service
install -pm 644 %{SOURCE4} %{buildroot}%{_unitdir}/epmd.socket
install -pm 644 %{SOURCE5} %{buildroot}%{_unitdir}/epmd@.service
install -pm 644 %{SOURCE6} %{buildroot}%{_unitdir}/epmd@.socket
%endif

# clean up
find %{buildroot}%{_libdir}/erlang -perm 0775 | xargs chmod 755
find %{buildroot}%{_libdir}/erlang -name Makefile | xargs chmod 644
find %{buildroot}%{_libdir}/erlang -name \*.bat | xargs rm -f
find %{buildroot}%{_libdir}/erlang -name index.txt.old | xargs rm -f

# doc
mkdir -p erlang_doc
mkdir -p %{buildroot}%{_mandir}/erlang
tar -C erlang_doc -xf %{SOURCE1}
tar -C %{buildroot}%{_datadir} -xf %{SOURCE2}

# make links to binaries
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
for file in erl erlc escript run_erl ; do
  ln -sf ../%{_lib}/erlang/bin/$file .
done
popd

# (tpg) fixes bug #32318
mkdir -p %{buildroot}%{_sysconfdir}/emacs/site-start.d
cat > %{buildroot}%{_sysconfdir}/emacs/site-start.d/erlang.el << EOF
(setq load-path (cons "%{_libdir}/%{name}/lib/tools-*/emacs" load-path))
(add-to-list 'load-path "%{_datadir}/emacs/site-lisp/ess")
(load-library "erlang-start")
EOF

# remove buildroot from installed files
pushd %{buildroot}%{_libdir}/erlang
sed -i "s|%{buildroot}||" erts*/bin/{erl,start} releases/RELEASES bin/{erl,start}
popd

# (tpg) remove not needed files
rm -rf %{buildroot}%{_datadir}/COPYRIGHT
rm -rf %{buildroot}%{_datadir}/PR.template
rm -rf %{buildroot}%{_datadir}/README.md

# (tpg) remove this manpages as they conflicts with openssl
rm -rf %{buildroot}%{_mandir}/man3/ssl.3.*
rm -rf %{buildroot}%{_mandir}/man3/crypto.3.*
rm -rf %{buildroot}%{_mandir}/man3/zlib.3.*

%pre -n %{name}-base
%if %{systemd_enabled}
getent group epmd &> /dev/null || groupadd -r epmd &>/dev/null || :
getent passwd epmd &> /dev/null || \
  useradd -r -g epmd -d /dev/null -s /sbin/nologin \
          -c "Erlang Port Mapper Daemon" epmd &>/dev/null || :
%endif

%post -n %{name}-base
%{_libdir}/erlang/Install -minimal %{_libdir}/erlang &>/dev/null || :
%if %{systemd_enabled}
%{__sysctl} enable epmd.service &>/dev/null || :
%endif

%preun -n %{name}-base
%if %{systemd_enabled}
if [[ $1 -eq 0 ]] ; then
  %{__sysctl} --no-reload disable epmd.service &>/dev/null || :
  %{__sysctl} stop epmd.service &>/dev/null || :
fi
%endif

%postun -n %{name}-base
%if %{systemd_enabled}
if [[ $1 -ge 1 ]] ; then
  %{__sysctl} daemon-reload &>/dev/null || :
fi
%endif

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS README.md

%files -n %{name}-stack
%defattr(-,root,root,-)
%doc LICENSE.txt

%files -n %{name}-base
%defattr(-,root,root,-)
%dir %{_libdir}/erlang
%dir %{_libdir}/erlang/bin
%dir %{_libdir}/erlang/lib
%dir %{_libdir}/erlang/misc
%if %{systemd_enabled}
%{_unitdir}/epmd.service
%{_unitdir}/epmd.socket
%{_unitdir}/epmd@.service
%{_unitdir}/epmd@.socket
%endif
%{_bindir}/*
%{_libdir}/erlang/Install
%{_libdir}/erlang/bin/ct_run
%{_libdir}/erlang/bin/epmd
%{_libdir}/erlang/bin/erl
%{_libdir}/erlang/bin/erlc
%{_libdir}/erlang/bin/escript
%{_libdir}/erlang/bin/no_dot_erlang.boot
%{_libdir}/erlang/bin/start.boot
%{_libdir}/erlang/bin/start.script
%{_libdir}/erlang/bin/start_clean.boot
%{_libdir}/erlang/bin/start_sasl.boot
%{_libdir}/erlang/erts-*
%{_libdir}/erlang/misc/format_man_pages
%{_libdir}/erlang/misc/makewhatis
%{_libdir}/erlang/releases
%{_libdir}/erlang/bin/run_erl
%{_libdir}/erlang/bin/start
%{_libdir}/erlang/bin/start_erl
%{_libdir}/erlang/bin/to_erl
%{elibdir}/erts-*
%{elibdir}/kernel-*
%{elibdir}/stdlib-*
%{elibdir}/sasl-*

%files -n %{name}-devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{realname}/%{_includedir}
%dir %{_libdir}/%{realname}/%{eprefix}
%{_libdir}/%{realname}/%{_includedir}/*
%{_libdir}/%{realname}/%{eprefix}/*

%files -n %{name}-asn1
%defattr(-,root,root,-)
%{elibdir}/asn1-*

%files -n %{name}-compiler
%defattr(-,root,root,-)
%{elibdir}/compiler-*

%files -n %{name}-common_test
%defattr(-,root,root,-)
%{elibdir}/common_test-*

%files -n %{name}-cosEvent
%defattr(-,root,root,-)
%{elibdir}/cosEvent-*

%files -n %{name}-cosEventDomain
%defattr(-,root,root,-)
%{elibdir}/cosEventDomain-*

%files -n %{name}-cosFileTransfer
%defattr(-,root,root,-)
%{elibdir}/cosFileTransfer-*

%files -n %{name}-cosNotification
%defattr(-,root,root,-)
%{elibdir}/cosNotification-*

%files -n %{name}-cosProperty
%defattr(-,root,root,-)
%{elibdir}/cosProperty-*

%files -n %{name}-cosTime
%defattr(-,root,root,-)
%{elibdir}/cosTime-*

%files -n %{name}-cosTransactions
%defattr(-,root,root,-)
%{elibdir}/cosTransactions-*

%files -n %{name}-crypto
%defattr(-,root,root,-)
%{elibdir}/crypto-*

%files -n %{name}-debugger
%defattr(-,root,root,-)
%{elibdir}/debugger-*

%files -n %{name}-dialyzer
%defattr(-,root,root,-)
%{elibdir}/dialyzer-*
%{_libdir}/%{realname}/bin/dialyzer

%files -n %{name}-diameter
%defattr(-,root,root,-)
%{elibdir}/diameter-*

%files -n %{name}-edoc
%defattr(-,root,root,-)
%{elibdir}/edoc-*

%files -n %{name}-eldap
%defattr(-,root,root,-)
%{elibdir}/eldap-*

%files -n %{name}-emacs
%defattr(-,root,root,-)
%{_sysconfdir}/emacs/site-start.d/erlang.el

%files -n %{name}-erl_docgen
%defattr(-,root,root,-)
%{elibdir}/erl_docgen-*

%files -n %{name}-erl_interface
%defattr(-,root,root,-)
%{elibdir}/erl_interface-*

%files -n %{name}-et
%defattr(-,root,root,-)
%{elibdir}/et-*

%files -n %{name}-eunit
%defattr(-,root,root,-)
%{elibdir}/eunit-*

%files -n %{name}-hipe
%defattr(-,root,root,-)
%{elibdir}/hipe-*

%files -n %{name}-ic
%defattr(-,root,root,-)
%{elibdir}/ic-*

%files -n %{name}-inets
%defattr(-,root,root,-)
%{elibdir}/inets-*

%files -n %{name}-jinterface
%defattr(-,root,root,-)
%{elibdir}/jinterface-*

%files -n %{name}-manpages
%defattr(-,root,root,-)
%{_mandir}/*/*

%files -n %{name}-megaco
%defattr(-,root,root,-)
%{elibdir}/megaco-*

%files -n %{name}-mnesia
%defattr(-,root,root,-)
%{elibdir}/mnesia-*

%files -n %{name}-observer
%defattr(-,root,root,-)
%{elibdir}/observer-*

%files -n %{name}-odbc
%defattr(-,root,root,-)
%{elibdir}/odbc-*

%files -n %{name}-orber
%defattr(-,root,root,-)
%{elibdir}/orber-*

%files -n %{name}-os_mon
%defattr(-,root,root,-)
%{elibdir}/os_mon-*

%files -n %{name}-otp_mibs
%defattr(-,root,root,-)
%{elibdir}/otp_mibs-*

%files -n %{name}-parsetools
%defattr(-,root,root,-)
%{elibdir}/parsetools-*

%files -n %{name}-public_key
%defattr(-,root,root,-)
%{elibdir}/public_key-*

%files -n %{name}-reltool
%defattr(-,root,root,-)
%{elibdir}/reltool-*

%files -n %{name}-runtime_tools
%defattr(-,root,root,-)
%{elibdir}/runtime_tools-*

%files -n %{name}-snmp
%defattr(-,root,root,-)
%{elibdir}/snmp-*

%files -n %{name}-ssh
%defattr(-,root,root,-)
%{elibdir}/ssh-*

%files -n %{name}-ssl
%defattr(-,root,root,-)
%{elibdir}/ssl-*

%files -n %{name}-syntax_tools
%defattr(-,root,root,-)
%{elibdir}/syntax_tools-*

%files -n %{name}-tools
%defattr(-,root,root,-)
%{elibdir}/tools-*

%files -n %{name}-typer
%defattr(-,root,root,-)
%{_libdir}/%{realname}/bin/typer

%files -n %{name}-wx
%defattr(-,root,root,-)
%{elibdir}/wx-*

%files -n %{name}-xmerl
%defattr(-,root,root,-)
%{elibdir}/xmerl-*

################################################################################

%changelog
* Fri Jan 24 2020 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.25-0
- Updated to the latest release

* Tue Dec 10 2019 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.24-0
- Updated to the latest release

* Fri Jul 05 2019 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.22-0
- Updated to the latest release
- Added sctp support
- Rebuilt with built-in zlib

* Mon Jun 03 2019 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.21-0
- Updated to the latest release
- LibreSSL updated to 2.9.2

* Wed Jan 23 2019 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.18-0
- Updated to the latest release

* Thu Jan 10 2019 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.17-0
- Updated to the latest release
- LibreSSL updated to 2.9.0

* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.13-0
- Updated to the latest release

* Thu Oct 25 2018 Anton Novojilov <andy@essentialkaos.com> - 20.3.8.10-0
- Updated to the latest release
- LibreSSL updated to 2.8.2

* Sat Jul 28 2018 Gleb Goncharov <g.goncharov@fun-box.ru> - 20.3.8.3-0
- Updated to the latest release

* Tue Apr 03 2018 Anton Novojilov <andy@essentialkaos.com> - 20.3-1
- Using GCC from devtoolset-3 for build

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 20.3-0
- Updated to latest stable release
- LibreSSL updated to 2.7.0

* Fri Feb 16 2018 Anton Novojilov <andy@essentialkaos.com> - 20.1-1
- Rebuilt with EC support
- Rebuilt with statically linked LibreSSL

* Thu Oct 05 2017 Anton Novojilov <andy@essentialkaos.com> - 20.1-0
- Updated to latest stable release

* Thu Jun 22 2017 Anton Novojilov <andy@essentialkaos.com> - 20.0-0
- Initial build
