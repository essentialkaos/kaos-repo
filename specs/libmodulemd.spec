################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

################################################################################

%global _vpath_srcdir   .
%global _vpath_builddir %{_target_platform}

################################################################################

Summary:            C Library for manipulating module metadata files
Name:               libmodulemd
Version:            2.8.2
Release:            0%{?dist}
License:            MIT
Group:              Development/Tools
URL:                https://github.com/fedora-modularity/libmodulemd

Source0:            https://github.com/fedora-modularity/libmodulemd/releases/download/%{name}-%{version}/modulemd-%{version}.tar.xz
Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc gcc-c++ meson glib2-doc rpm-devel rpm-libs file-devel
BuildRequires:      pkgconfig(gobject-2.0) pkgconfig(gobject-introspection-1.0)
BuildRequires:      pkgconfig(yaml-0.1) pkgconfig(gtk-doc)
BuildRequires:      valgrind clang

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
C Library for manipulating module metadata files.

################################################################################

%package devel

Summary:            Development files for libmodulemd
Group:              Development/Libraries

Requires:           pkgconfig >= 1:0.14
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for libmodulemd.

################################################################################

%prep
%{crc_check}

%setup -qn modulemd-%{version}

%build
%meson -Ddeveloper_build=false \
       -Dbuild_api_v1=false \
       -Dbuild_api_v2=true \
       -Dwith_py3_overrides=false

%meson_build

%install
rm -rf %{buildroot}

%meson_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING
%dir %{_libdir}/girepository-1.0
%{_bindir}/modulemd-validator
%{_libdir}/%{name}.so.*
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{python_sitearch}/gi/overrides/Modulemd.*

%files devel
%defattr(-,root,root,-)
%dir %{_datadir}/gir-1.0
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/modulemd-2.0.pc
%{_includedir}/modulemd-2.0/
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{_datadir}/gtk-doc/html/modulemd-2.0/

################################################################################

%changelog
* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.2-0
- Fix missing error return
- Validate in the ModuleStream parent class
- ModuleStream: Properly override names when asked to
- Use podman instead of docker where possible
- Use safer version of dup()
- subdocument: match the argument name in the header
- Fix invalid nested_error usage
- Reformat python code with black
- Auto-format python with black
- Add clang_tidy autoformatter
- Apply clang-tidy formatting
- Alphabetize meson_options.txt
- Travis: Add --layers=true to buildah for Dockerfile.deps
- Travis: Add F31 as a test target
- Travis: Run Fedora tests on aarch64
- Separate Travis builds into stages
- Skip clang-tidy in CI
- Skip formatters when building RPMs

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.1-0
- Made GTK docs non-mandatory
- Removal of extraneous test data
- Fix formatting
- Improvements to ModuleIndex.update_from_defaults_dir()
- Rework defaults merging logic
- Update .gitignore file
- Refactor common test routines
- Travis: Fix documentation generation test
- Travis: Fix copy-paste error
- Travis: Yet more copy-paste fixes
- Include .pyc files in .gitignore
- Drop SCANBUILD environment variable
- allow to disable docs when building it

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.8.0-0
- A final batch of documentation updates for private functions.
- Refactor stream copy/upgrade helper macros. Another final batch of
  documentation updates for private functions.
- Make Module.get_translation() public
- Valgrind: Don't rebuild tests before running
- Add helpers for reading compressed files
- ModuleIndex: add compressed file loading support
- Add debugging information to the Coverity scan
- Add ModuleIndex.update_from_defaults_directory()
- Revert "Add debugging information to the Coverity scan"
- Temporarily switch Coverity to F30
- Coverity: Fix Dockerfile FROM
- TESTS: Check a return value
- Compression: Handle a failed dup()
- Compression: don't leak file descriptors on error
- Compression: Fix incorrect pointer comparison
- Coverity: work around "copy-paste" false positive

* Fri Dec 20 2019 Anton Novojilov <andy@essentialkaos.com> - 2.7.0-0
- Type tweaks to be more friendly to gtk-doc documentation generation
- Move modulemd_module_stream_v2_replace_*() method definitions to correct
  header file and add documentation.
- Another batch of documentation updates for private functions, along with other
  minor corrections.
- Add documentation for private utility functions for use within libmodulemd.
- Synchronize the user docs in the main header file and the repo's README.
- Correct several "may be used uninitialized" compiler warnings.
- Make ModulemdErrorEnum and ModulemdYamlErrorEnum into public enums.
- Fix modulemd_yaml_parse_bool() comparisons so return value is correct. Fix bad
  test that was masking the above bug.
- Correct bugs where component buildonly and buildorder properties are getting
  mixed up.
- Update modulemd spec for new component rpm "buildroot" and "srpm-buildroot"
  flags, implement new properties, and add tests.
- Another batch of documentation updates for private functions.
- TESTS: Check the return value of get_buildtime_streams()
- DOCS: Fix references to common GLib objects
- CI: Fix xref.sh path
- Split Coverity scan into a separate test
- CI: Reflow docker commands to improve readability
- Drop v1 code and refactor build system
- Drop unused test_data
- Emitter: Throw validation error for empty ModuleIndex
- Merge pull request #343 from mmathesius/doc-sync-readme
- Fix emitting translations
- Dependencies: Emit empty dependencies
- Dependencies: Add tests for one or the other requirements
- spec: Fix typo in python2-libmodulemd subpackage
- Stop using deprecated build_always
- CI: Quieter logs
- Print ninja dist logs if it fails
- Drop ModulemdTranslationHelpers
- Add translations in Modulemd.Index from Babel Catalog
- Added more translation files for consistency check
- Retrieve metadata from koji and feed into translation helpers

* Sat Jul 27 2019 Anton Novojilov <andy@essentialkaos.com> - 2.6.0-0
- Fixes to internal document linking by using correct object names, etc.
- Add descriptions for a few undocumented enums and correct a few mis-documented
  parameters.
- Correct a few typos and omissions in C code examples in README so copy/paste
  of code has a chance of working.
- Add gtk-doc descriptions for ModulemdModuleStream object properties.
- Update meson.build to convince gtk-doc to produce documentation for object
  properties.
- Correct typo in ModulemdModuleStream.arch property nick name.
- Remove unnecessary gtk-doc documentation blocks added by commit 76aecdf.
- Documentation updates
- Bump version to 2.5.1dev
- Double valgrind timeout
- Parallelize the valgrind tests
- Print git diff when dirty_repo test fails
- Fix transfer type for Module.search_streams()
- Extend timeout for header test
- Return translated profile descriptions
- CI: Add IRC notifications
- Add ModuleIndexMerger.resolve_ext()
- Simplify test setup
- Improve valgrind test setup
- add get_stream_names from module
- Create python binding for get_stream_names
- Convert from Modulemd.ModuleIndex to babel catalog

* Wed Jul 03 2019 Anton Novojilov <andy@essentialkaos.com> - 2.5.0-0
- Initial build for kaos repository
