%global pginstdir /usr/pgsql-9.4
%global pgmajorversion 94
%global _slonconffilter /etc/slon_tools.conf
%global __requires_exclude ^(%{_slonconffilter})$
%global sname slony1
%{!?docs:%global docs 0}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}-%{pgmajorversion}
Version:	2.2.4
Release:	3%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/2.2/source/%{sname}-%{version}.tar.bz2
Source2:	filter-requires-perl-Pg.sh
Source3:	slony1.init
Source4:	slony1-%{pgmajorversion}.sysconfig
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}-server, initscripts, byacc, flex
Requires:	postgresql%{pgmajorversion}-server, perl-DBD-Pg
Conflicts:	slony1

%if %docs
BuildRequires:	docbook-style-dsssl postgresql_autodoc docbook-utils
%endif

%description
Slony-I is a "master to multiple slaves" replication
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Group:		Applications/Databases
Requires:	%{sname}-%{pgmajorversion}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript
Obsoletes:	slony1-docs

%description docs
The slony1-docs package includes some documentation for Slony-I.
%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}
%build

# Fix permissions of docs.
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --prefix=%{pginstdir} --includedir %{pginstdir}/include --with-pgconfigdir=%{pginstdir}/bin --libdir=%{pginstdir}/lib \
	--with-perltools=%{pginstdir}/bin --sysconfdir=%{_sysconfdir}/%{sname}-%{pgmajorversion} \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{sname}-%{version} \
%endif
	--datadir=%{pginstdir}/share --with-pglibdir=%{pginstdir}/lib

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample slon.conf file
install -d %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon.conf
install -m 0644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf

# Fix the log path
sed "s:\([$]LOGDIR = '/var/log/slony1\):\1-%{pgmajorversion}:" -i %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf

# Install default sysconfig file
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/slony1-%{pgmajorversion}

# change file modes of docs.
/bin/chmod 644 COPYRIGHT UPGRADING SAMPLE RELEASE

# Install init script
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{sname}-%{pgmajorversion}

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
# Perform some cleanup
/bin/rm -f %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf-sample
/bin/rm -f %{buildroot}%{_datadir}/pgsql/*.sql
/bin/rm -f %{buildroot}%{_libdir}/slony1_funcs.so

%clean
rm -rf %{buildroot}

%post
chkconfig --add %{sname}-%{pgmajorversion}
if [ ! -e "/var/log/slony1-%{pgmajorversion}" -a ! -h "/var/log/slony1-%{pgmajorversion}" ]
then
        mkdir /var/log/slony1-%{pgmajorversion}
        chown postgres:postgres /var/log/slony1-%{pgmajorversion}
fi
if [ ! -e "/var/run/slony1-%{pgmajorversion}/" -a ! -h "/var/run/slony1-%{pgmajorversion}/" ]
then
        mkdir /var/run/slony1-%{pgmajorversion}
        chown postgres:postgres /var/run/slony1-%{pgmajorversion}
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	chkconfig --del %{sname}-%{pgmajorversion}
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service %{sname}-%{pgmajorversion} condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING INSTALL SAMPLE RELEASE
%{pginstdir}/bin/slon*
%{pginstdir}/lib/slon*
%{pginstdir}/share/slon*
%config(noreplace) %{_sysconfdir}/sysconfig/slony1-%{pgmajorversion}
%config(noreplace) %{_sysconfdir}/%{sname}-%{pgmajorversion}/slon.conf
%config(noreplace) %{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/slony1-%{pgmajorversion}

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Tue Mar 17 2015 Devrim Gunduz <devrim@gunduz.org> 2.2.4-3
- Fix the log directory, so that it points to correct release.
  Per bug report from Guillaume Lelarge.

* Mon Jan 19 2015 Devrim Gunduz <devrim@gunduz.org> 2.2.4-2
- Fix init script so that it reads the conninfo correctly.
  Per Tomonari Katsumata.
- Fix major version number in init script.

* Mon Jan 19 2015 Devrim Gunduz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Wed Jul 9 2014 Devrim Gunduz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Wed Feb 12 2014 Devrim Gunduz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sat Nov 9 2013 Devrim Gunduz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Tue Sep 10 2013 Devrim Gunduz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0
- Trim changelog.

* Fri Aug 23 2013 Xavier Bergade <XavierB@benon.com> 2.1.4-2
- Set --sysconfdir during configure to fix the require list & the CONFIG_FILE path in the Perl scripts
- Set the correct path for LOGDIR in the slon_tools.conf file

* Tue Aug 20 2013 Devrim Gunduz <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Mon Jun 24 2013 Devrim Gunduz <devrim@gunduz.org> 2.1.3-2
- Various fixes for multiple postmaster feature:
 - Install slony config files in separate directories.
 - Update init scripts.
 - Install pid and log files into separate directories.
 - Properly filter dependency to /etc/slon_tools.conf
 - Use default sysconfig file, to be used by init script.

* Tue Feb 19 2013 Devrim Gunduz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3
- Fix init script names in %%postun and %%preun.

* Sat Feb 09 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.2-2
- Rebuilt.

* Sat Sep 1 2012 Devrim Gunduz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Jun 8 2012 Devrim Gunduz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1

* Wed Oct 05 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.7-2
- Use correct pgmajorversion number, per report from Ger Timmens.

* Fri Aug 12 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7.

* Thu Dec 9 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Fri Oct 8 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Sat Sep 18 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.4-1
- Update to 2.0.4, and perform a major cleanup and bugfix.
- Apply changes for 9.0+
- Update source2, to supress weird dependency for slon_tools.conf.

* Sat Apr 10 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3
- Updated doc patch
- Rename log directory to slony, to match upstream default
- Apply many fixes to support multiple postmaster installation.

* Sat May 9 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2
- Removed patch0 -- it is no longer needed.
- Added a temp patch to get rid of sgml error.
- Re-enable doc builds

* Sat Mar 14 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Create log directory, per pgcore #77.

* Thu Jan 29 2009 Devrim Gunduz <devrim@gunduz.org> 2.0.0-3
- Add docbook-utils to BR.

* Sat Dec 13 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.0-2
- Add a patch to fix build errors
- Temporarily update Source2, so that it will silence a dependency error.

* Tue Dec 2 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
