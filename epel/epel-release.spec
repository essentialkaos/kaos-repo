Name:           epel-release
Version:        6
Release:        8
Summary:        Extra Packages for Enterprise Linux repository configuration

Group:          System Environment/Base
License:        GPLv2

# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            http://dl.fedoraproject.org/pub/epel/
Source0:        http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-6
Source1:        GPL
Source2:        epel.repo
Source3:        epel-testing.repo
Source4:        macros.ghc-srpm

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      redhat-release >=  %{version}
Conflicts:     fedora-release

%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum and up2date.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2} %{SOURCE3}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

# rpm macros for koji
install -Dpm 644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.ghc-srpm

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Not needed for el6 as sources has been removed
#echo "# epel repo -- added by epel-release " \
#    >> %{_sysconfdir}/sysconfig/rhn/sources
#echo "yum epel http://download.fedora.redhat.com/pub/epel/%{version}/\$ARCH" \
#    >> %{_sysconfdir}/sysconfig/rhn/sources

%postun
#sed -i '/^yum\ epel/d' %{_sysconfdir}/sysconfig/rhn/sources
#sed -i '/^\#\ epel\ repo\ /d' %{_sysconfdir}/sysconfig/rhn/sources


%files
%defattr(-,root,root,-)
%doc GPL
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*
/etc/rpm/macros.ghc-srpm


%changelog
* Sun Nov 04 2012 <stahnma@fedoraproject.org> - 6-8
- Fix URL bz #870686

* Wed May  9 2012 Jens Petersen <petersen@redhat.com> - 6-7
- add ppc64 to ghc_arches

* Tue Jan 10 2012 Jens Petersen <petersen@redhat.com> - 6-6
- add /etc/rpm/macros.ghc-srpm from fedora redhat-rpm-macros

* Tue Oct 12 2010 Michael Stahnke <stahnma@fedoraproject.org> - 6-5
- Fix bug #627611

* Wed Aug 11 2010 Seth Vidal <skvidal at fedoraproject.org> - 6-4
- conflict fedora-release

* Fri Jul 09 2010 Dennis Gilmore <dennis@ausil.us> - 6-3
- use metalink urls not mirrorlist ones

* Tue Apr 27 2010 Dennis Gilmore <dennis@ausil.us> - 6-1
- setup for EL-6
- new key

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.1
- fix license tag

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 6-0
- Bumped in devel to RHEL 6. (We can dream).

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-4
- Changed description again

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-3
- Removed cp in postun
- Removed the file epel-release - provides no value
- Removed dist tag as per review bug #233236
- Changed description

* Mon Mar 14 2007 Michael Stahnke <mastahnke@gmail.com> - 4-2
- Fixed up2date issues.

* Mon Mar 12 2007 Michael Stahnke <mastahnke@gmail.com> - 4-1
- Initial Package
