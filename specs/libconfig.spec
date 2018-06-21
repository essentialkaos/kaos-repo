################################################################################

Name:               libconfig
Summary:            C/C++ configuration file library
Version:            1.7.2
Release:            0%{?dist}
License:            LGPLv2+
Group:              Development/Libraries
URL:                https://hyperrealm.github.io/libconfig

Source0:            https://hyperrealm.github.io/%{name}/dist/%{name}-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      make texinfo-tex bison byacc flex gcc gcc-c++

################################################################################

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.

################################################################################

%package devel
Summary:             Development files for libconfig
Group:               Development/Libraries

Requires:            %{name} = %{version}-%{release}
Requires:            pkgconfig

Requires(post):      /sbin/install-info
Requires(preun):     /sbin/install-info

%description devel
Development libraries and headers for developing software against
libconfig.

################################################################################

%prep
%setup -qn %{name}-%{version}

%build
%configure --disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

################################################################################

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%{_infodir}/libconfig.info*
%{_libdir}/cmake/%{name}++/*.cmake
%{_libdir}/cmake/%{name}/*.cmake

################################################################################

%changelog
* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.2-0
- Fixed a slow memory leak in config_destroy()
- Miscellaneous fixes in build files

* Sun Jun 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- Fixed a bug that caused incorrect processing of strings with escape sequences.
- Added a new 'fsync' configuration option.
- Merged some contributed updates to CMake files.

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.7-0
- Redesigned the directory-include feature to avoid using platform-specific
  directory scanning code, and to fix a bug in the handling of nested includes.
  The application can now do its own directory scanning and/or wildcard
  expansion by registering an include function.
- Added new CONFIG_OPTION_ALLOW_SCIENTIFIC_NOTATION to allow either %%f or
  %%g-style formatting for floating point values.
- Improved the options APIs in both the C and C++ libraries.
- Improved the automatic conversion between int and int64 values.
- Fixed build errors caused by out-of-sync generated lexer and parser source
  files.
- Various internal code cleanup.
- Fixed failing unit tests.
- Fixed a problem where a group or list could be added to an array.
- Changed default float precision from 2 to 6.
- Added an API to clear an existing configuration.
- Upgraded VS2015 solution/project files to VS2017.
- Modified grammar to allow trailing commas in lists and arrays.
- Removed logic that clipped negative values to 0 in (unsigned int) cast
  operator.
- Updated manual and added a new chapter on other libconfig implementations
  and bindings.

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 1.6-0
- Added include_dir feature (support for Debian-style conf.d/ includes)
- Added octal_ints feature (support for integer expressed in octal,
  useful for permissions and masks in UNIX-like systems
- Fixed "Removing a setting removes all siblings"
- Allow specifying the number of decimals wanted when outputting
- Make libconfig usable from CMake
- Documentation fixes

* Thu Aug 06 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5-0
- Updated to version 1.5