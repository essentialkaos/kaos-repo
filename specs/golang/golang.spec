################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

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

%global debug_package %{nil}
%global _binaries_in_noarch_packages_terminate_build 0
%global __requires_exclude_from ^(%{_datadir}|/usr/lib)/%{name}/(doc|src)/.*$
%global __strip /bin/true
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths /usr/lib/rpm/check-buildroot /usr/lib/rpm/brp-compress

################################################################################

%global goroot          %{_libdir32}/%{name}
%global gopath          %{_datadir}/gocode

%ifarch x86_64
%global gohostarch  amd64
%endif
%ifarch %{ix86}
%global gohostarch  386
%endif

%global go_api 1.14

################################################################################

Summary:           The Go Programming Language
Name:              golang
Version:           1.14.3
Release:           0%{?dist}
License:           BSD
Group:             Development/Languages
URL:               https://golang.org

Source0:           https://storage.googleapis.com/%{name}/go%{version}.src.tar.gz

Source10:          %{name}-gdbinit
Source11:          %{name}-prelink.conf
Source12:          macros.%{name}

Source100:         checksum.sha512

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     golang >= 1.4.2

Requires:          git
Requires:          %{name}-bin
Requires:          %{name}-src = %{version}-%{release}

ExclusiveArch:     %{ix86} x86_64 %{arm}

Provides:          go = %{version}-%{release}

################################################################################

%description

Go is an open source programming language that makes it easy to build
simple, reliable, and efficient software.

################################################################################

%package src

Summary:           Golang compiler source tree
Group:             Development/Languages
BuildArch:         noarch

%description src
Golang compiler source tree

################################################################################

%ifarch %{ix86}

%package pkg-bin-linux-386

Summary:           Golang compiler tool for linux 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Requires:          golang-pkg-linux-386 = %{version}-%{release}
Requires(post):    golang-pkg-linux-386 = %{version}-%{release}

Requires:          glibc gcc

Provides:          golang-bin = 386
Provides:          go(API)(go) = %{go_api}

Requires(post):    %{_sbindir}/update-alternatives
Requires(postun):  %{_sbindir}/update-alternatives

%description pkg-bin-linux-386
Golang compiler tool for linux 386

%endif

################################################################################

%ifarch x86_64

%package pkg-bin-linux-amd64

Summary:           Golang compiler tool for linux amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Requires:          golang-pkg-linux-amd64 = %{version}-%{release}
Requires(post):    golang-pkg-linux-amd64 = %{version}-%{release}

Requires:          glibc gcc

Provides:          golang-bin = amd64
Provides:          go(API)(go) = %{go_api}

Requires(post):    %{_sbindir}/update-alternatives
Requires(postun):  %{_sbindir}/update-alternatives

%description pkg-bin-linux-amd64
Golang compiler tool for linux amd64

%endif

################################################################################

%ifarch %{arm}

%package pkg-bin-linux-arm

Summary:           Golang compiler tool for linux arm
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Requires:          golang-pkg-linux-arm = %{version}-%{release}
Requires(post):    golang-pkg-linux-arm = %{version}-%{release}

Requires:          glibc gcc

Provides:          golang-bin = arm
Provides:          go(API)(go) = %{go_api}

Requires(post):    %{_sbindir}/update-alternatives
Requires(postun):  %{_sbindir}/update-alternatives

%description pkg-bin-linux-arm
Golang compiler tool for linux arm

%endif

################################################################################

%package pkg-linux-386

Summary:           Golang compiler toolchain to compile for linux 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Provides:          go(API)(cgo) = %{go_api}

BuildArch:         noarch

%description pkg-linux-386
Golang compiler toolchain to compile for linux 386

################################################################################

%package pkg-linux-amd64

Summary:           Golang compiler toolchain to compile for linux amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Provides:          go(API)(cgo) = %{go_api}

BuildArch:         noarch

%description pkg-linux-amd64
Golang compiler toolchain to compile for linux amd64

################################################################################

%package pkg-linux-arm

Summary:           Golang compiler toolchain to compile for linux arm
Group:             Development/Languages
Requires:          go = %{version}-%{release}
Provides:          go(API)(cgo) = %{go_api}

BuildArch:         noarch

%description pkg-linux-arm
Golang compiler toolchain to compile for linux arm

################################################################################

%package pkg-darwin-386

Summary:           Golang compiler toolchain to compile for darwin 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-darwin-386
Golang compiler toolchain to compile for darwin 386

################################################################################

%package pkg-darwin-amd64

Summary:           Golang compiler toolchain to compile for darwin amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-darwin-amd64
Golang compiler toolchain to compile for darwin amd64

################################################################################

%package pkg-windows-386

Summary:           Golang compiler toolchain to compile for windows 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-windows-386
Golang compiler toolchain to compile for windows 386

################################################################################

%package pkg-windows-amd64

Summary:           Golang compiler toolchain to compile for windows amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-windows-amd64
Golang compiler toolchain to compile for windows amd64

################################################################################

%package pkg-plan9-386

Summary:           Golang compiler toolchain to compile for plan9 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-plan9-386
Golang compiler toolchain to compile for plan9 386

################################################################################

%package pkg-plan9-amd64

Summary:           Golang compiler toolchain to compile for plan9 amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-plan9-amd64
Golang compiler toolchain to compile for plan9 amd64

################################################################################

%package pkg-freebsd-386

Summary:           Golang compiler toolchain to compile for freebsd 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-freebsd-386
Golang compiler toolchain to compile for freebsd 386

################################################################################

%package pkg-freebsd-amd64

Summary:           Golang compiler toolchain to compile for freebsd amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-freebsd-amd64
Golang compiler toolchain to compile for freebsd amd64

################################################################################

%package pkg-freebsd-arm

Summary:           Golang compiler toolchain to compile for freebsd arm
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-freebsd-arm
Golang compiler toolchain to compile for freebsd arm

################################################################################

%package pkg-netbsd-386

Summary:           Golang compiler toolchain to compile for netbsd 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-netbsd-386
Golang compiler toolchain to compile for netbsd 386

################################################################################

%package pkg-netbsd-amd64

Summary:           Golang compiler toolchain to compile for netbsd amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-netbsd-amd64
Golang compiler toolchain to compile for netbsd amd64

################################################################################

%package pkg-netbsd-arm

Summary:           Golang compiler toolchain to compile for netbsd arm
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-netbsd-arm
Golang compiler toolchain to compile for netbsd arm

################################################################################

%package pkg-openbsd-386

Summary:           Golang compiler toolchain to compile for openbsd 386
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-openbsd-386
Golang compiler toolchain to compile for openbsd 386

################################################################################

%package pkg-openbsd-amd64

Summary:           Golang compiler toolchain to compile for openbsd amd64
Group:             Development/Languages
Requires:          go = %{version}-%{release}

BuildArch:         noarch

%description pkg-openbsd-amd64
Golang compiler toolchain to compile for openbsd amd64

################################################################################

%pretrans -p <lua>
for _,d in pairs({"api", "doc", "include", "lib", "src"}) do
  path = "%{goroot}/" .. d
  if posix.stat(path, "type") == "link" then
    os.remove(path)
    posix.mkdir(path)
  end
end

%prep
%{crc_check}

%setup -qn go

%build

export GOROOT_FINAL=%{goroot}
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{_libdir32}/%{name}

pushd src
  for goos in darwin freebsd linux netbsd openbsd plan9 windows ; do
    for goarch in 386 amd64 arm ; do
      if [[ "${goarch}" == "arm" ]] ; then
        if [[ "${goos}" == "darwin" || "${goos}" == "windows" || "${goos}" == "plan9" || "${goos}" = "openbsd" ]] ; then
          continue
        fi
      fi

      CC="gcc" \
      CC_FOR_TARGET="gcc" \
        GOOS=${goos} \
        GOARCH=${goarch} \
        ./make.bash --no-clean
    done
  done
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{goroot}

cp -ap api bin doc lib pkg src misc VERSION \
       %{buildroot}%{goroot}/

touch %{buildroot}%{goroot}/pkg

find %{buildroot}%{goroot}/src -exec touch -r %{buildroot}%{goroot}/VERSION "{}" \;
find %{buildroot}%{goroot}/pkg -exec touch -r %{buildroot}%{goroot}/pkg "{}" \;

cwd=$(pwd)
src_list=$cwd/go-src.list

rm -f $src_list
touch $src_list

pushd %{buildroot}%{goroot}

  find src/ -type d -printf '%%%dir %{goroot}/%p\n' >> $src_list
  find src/ ! -type d -printf '%{goroot}/%p\n' >> $src_list

  for goos in darwin freebsd linux netbsd openbsd plan9 windows ; do
    for goarch in 386 amd64 arm ; do
      if [[ "${goarch}" == "arm" ]] ; then
        if [[ "${goos}" == "darwin" || "${goos}" == "windows" || "${goos}" == "plan9" || "${goos}" == "openbsd" ]] ; then
          continue
        fi
      fi
      file_list=${cwd}/pkg-${goos}-${goarch}.list
      rm -f $file_list
      touch $file_list
      find pkg/${goos}_${goarch}/ -type d -printf '%%%dir %{goroot}/%p\n' >> $file_list
      find pkg/${goos}_${goarch}/ ! -type d -printf '%{goroot}/%p\n' >> $file_list
    done
  done
popd

rm -rfv %{buildroot}%{goroot}/lib/time
rm -rfv %{buildroot}%{goroot}/doc/Makefile

mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/

pushd %{buildroot}%{goroot}/bin/
  rm -rf darwin_* windows_* freebsd_* netbsd_* openbsd_* plan9_*
  case "%{gohostarch}" in
    amd64) rm -rf linux_386 linux_arm   ;;
    386)   rm -rf linux_arm linux_amd64 ;;
    arm)   rm -rf linux_386 linux_amd64 ;;
  esac
popd

ln -sf %{goroot}/bin/go    %{buildroot}%{_bindir}/go
ln -sf %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt

mkdir -p %{buildroot}%{_sysconfdir}/gdbinit.d
cp -a %{SOURCE10} %{buildroot}%{_sysconfdir}/gdbinit.d/%{name}.gdb

mkdir -p %{buildroot}%{_sysconfdir}/prelink.conf.d
cp -a %{SOURCE11} %{buildroot}%{_sysconfdir}/prelink.conf.d/%{name}.conf

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
cp -av %{SOURCE12} %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name}

################################################################################

%clean
rm -rf %{buildroot}

################################################################################

%ifarch %{ix86}

%post pkg-bin-linux-386

touch -r %{goroot}/pkg/linux_386/runtime.a %{goroot}/pkg/linux_386/runtime/cgo.a

%endif

################################################################################

%ifarch x86_64

%post pkg-bin-linux-amd64

touch -r %{goroot}/pkg/linux_amd64/runtime.a %{goroot}/pkg/linux_amd64/runtime/cgo.a

%endif

################################################################################

%ifarch %{arm}

%post pkg-bin-linux-arm

touch -r %{goroot}/pkg/linux_arm/runtime.a %{goroot}/pkg/linux_arm/runtime/cgo.a

%endif

################################################################################

%ifarch %{ix86}

%posttrans pkg-bin-linux-386

# Rebuild outdated runtime
%{_bindir}/go install std

%endif

################################################################################

%ifarch x86_64

%posttrans pkg-bin-linux-amd64

# Rebuild outdated runtime
%{_bindir}/go install std

%endif

################################################################################

%ifarch %{arm}

%posttrans pkg-bin-linux-arm

# Rebuild outdated runtime
%{_bindir}/go install std

%endif

################################################################################

%files
%defattr(-,root,root,-)

%doc AUTHORS CONTRIBUTORS LICENSE PATENTS
%doc %{goroot}/VERSION
%doc %{goroot}/doc/*

%{goroot}/*

%exclude %{goroot}/VERSION
%exclude %{goroot}/bin/
%exclude %{goroot}/src/

%exclude %{goroot}/pkg/darwin_*/
%exclude %{goroot}/pkg/freebsd_*/
%exclude %{goroot}/pkg/linux_*/
%exclude %{goroot}/pkg/netbsd_*/
%exclude %{goroot}/pkg/openbsd_*/
%exclude %{goroot}/pkg/plan9_*/
%exclude %{goroot}/pkg/windows_*/
%exclude %{goroot}/pkg/tool/
%exclude %{goroot}/pkg/obj/

%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com/
%dir %{gopath}/src/bitbucket.org/
%dir %{gopath}/src/code.google.com/
%dir %{gopath}/src/code.google.com/p/

%{_sysconfdir}/gdbinit.d
%{_sysconfdir}/prelink.conf.d
%{_rpmconfigdir}/macros.d/macros.golang

%files -f go-src.list src
%defattr(-,root,root,-)

%ifarch %{ix86}
%files pkg-bin-linux-386
%defattr(-,root,root,-)

%{goroot}/bin/
%{_bindir}/go
%{_bindir}/gofmt
%{goroot}/pkg/linux_386/runtime/cgo.a

%dir %{goroot}/pkg/tool/linux_386
%{goroot}/pkg/tool/linux_386/addr2line
%{goroot}/pkg/tool/linux_386/api
%{goroot}/pkg/tool/linux_386/asm
%{goroot}/pkg/tool/linux_386/buildid
%{goroot}/pkg/tool/linux_386/compile
%{goroot}/pkg/tool/linux_386/cover
%{goroot}/pkg/tool/linux_386/dist
%{goroot}/pkg/tool/linux_386/doc
%{goroot}/pkg/tool/linux_386/link
%{goroot}/pkg/tool/linux_386/nm
%{goroot}/pkg/tool/linux_386/objdump
%{goroot}/pkg/tool/linux_386/pack
%{goroot}/pkg/tool/linux_386/pprof
%{goroot}/pkg/tool/linux_386/test2json
%{goroot}/pkg/tool/linux_386/trace
%{goroot}/pkg/tool/linux_386/vet
%endif

%ifarch x86_64
%files pkg-bin-linux-amd64
%defattr(-,root,root,-)

%{goroot}/bin/
%{_bindir}/go
%{_bindir}/gofmt
%{goroot}/pkg/linux_amd64/runtime/cgo.a

%dir %{goroot}/pkg/tool/linux_amd64
%{goroot}/pkg/tool/linux_amd64/addr2line
%{goroot}/pkg/tool/linux_amd64/api
%{goroot}/pkg/tool/linux_amd64/asm
%{goroot}/pkg/tool/linux_amd64/buildid
%{goroot}/pkg/tool/linux_amd64/compile
%{goroot}/pkg/tool/linux_amd64/cover
%{goroot}/pkg/tool/linux_amd64/dist
%{goroot}/pkg/tool/linux_amd64/doc
%{goroot}/pkg/tool/linux_amd64/link
%{goroot}/pkg/tool/linux_amd64/nm
%{goroot}/pkg/tool/linux_amd64/objdump
%{goroot}/pkg/tool/linux_amd64/pack
%{goroot}/pkg/tool/linux_amd64/pprof
%{goroot}/pkg/tool/linux_amd64/test2json
%{goroot}/pkg/tool/linux_amd64/trace
%{goroot}/pkg/tool/linux_amd64/vet
%endif

%ifarch %{arm}
%files pkg-bin-linux-arm
%defattr(-,root,root,-)

%{goroot}/bin/
%{_bindir}/go
%{_bindir}/gofmt
%{goroot}/pkg/linux_arm/runtime/cgo.a

%dir %{goroot}/pkg/tool/linux_arm
%{goroot}/pkg/tool/linux_arm/addr2line
%{goroot}/pkg/tool/linux_arm/api
%{goroot}/pkg/tool/linux_arm/asm
%{goroot}/pkg/tool/linux_arm/buildid
%{goroot}/pkg/tool/linux_arm/compile
%{goroot}/pkg/tool/linux_arm/cover
%{goroot}/pkg/tool/linux_arm/dist
%{goroot}/pkg/tool/linux_arm/doc
%{goroot}/pkg/tool/linux_arm/link
%{goroot}/pkg/tool/linux_arm/nm
%{goroot}/pkg/tool/linux_arm/objdump
%{goroot}/pkg/tool/linux_arm/pack
%{goroot}/pkg/tool/linux_arm/pprof
%{goroot}/pkg/tool/linux_arm/test2json
%{goroot}/pkg/tool/linux_arm/trace
%{goroot}/pkg/tool/linux_arm/vet
%endif

%files pkg-linux-386 -f pkg-linux-386.list
%defattr(-,root,root,-)

%{goroot}/pkg/linux_386/
%ifarch %{ix86}
%exclude %{goroot}/pkg/linux_386/runtime/cgo.a
%endif
%{goroot}/pkg/tool/linux_386/cgo
%{goroot}/pkg/tool/linux_386/fix

%files pkg-linux-amd64 -f pkg-linux-amd64.list
%defattr(-,root,root,-)

%{goroot}/pkg/linux_amd64/
%ifarch x86_64
%exclude %{goroot}/pkg/linux_amd64/runtime/cgo.a
%endif
%{goroot}/pkg/tool/linux_amd64/cgo
%{goroot}/pkg/tool/linux_amd64/fix

%files pkg-linux-arm -f pkg-linux-arm.list
%defattr(-,root,root,-)

%{goroot}/pkg/linux_arm/
%ifarch %{arm}
%exclude %{goroot}/pkg/linux_arm/runtime/cgo.a
%endif
%{goroot}/pkg/tool/linux_arm/cgo
%{goroot}/pkg/tool/linux_arm/fix

%files pkg-darwin-386 -f pkg-darwin-386.list
%defattr(-,root,root,-)

%files pkg-darwin-amd64 -f pkg-darwin-amd64.list
%defattr(-,root,root,-)

%files pkg-windows-386 -f pkg-windows-386.list
%defattr(-,root,root,-)

%files pkg-windows-amd64 -f pkg-windows-amd64.list
%defattr(-,root,root,-)

%files pkg-plan9-386 -f pkg-plan9-386.list
%defattr(-,root,root,-)

%files pkg-plan9-amd64 -f pkg-plan9-amd64.list
%defattr(-,root,root,-)

%files pkg-freebsd-386 -f pkg-freebsd-386.list
%defattr(-,root,root,-)

%files pkg-freebsd-amd64 -f pkg-freebsd-amd64.list
%defattr(-,root,root,-)

%files pkg-freebsd-arm -f pkg-freebsd-arm.list
%defattr(-,root,root,-)

%files pkg-netbsd-386 -f pkg-netbsd-386.list
%defattr(-,root,root,-)

%files pkg-netbsd-amd64 -f pkg-netbsd-amd64.list
%defattr(-,root,root,-)

%files pkg-netbsd-arm -f pkg-netbsd-arm.list
%defattr(-,root,root,-)

%files pkg-openbsd-386 -f pkg-openbsd-386.list
%defattr(-,root,root,-)

%files pkg-openbsd-amd64 -f pkg-openbsd-amd64.list
%defattr(-,root,root,-)

################################################################################

%changelog
* Fri May 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.3-0
- Updated to the latest stable release

* Thu Apr 09 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.2-0
- Updated to the latest stable release

* Fri Mar 20 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.1-0
- Updated to the latest stable release

* Wed Feb 26 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14-0
- Updated to the latest stable release

* Wed Jan 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.13.7-0
- Updated to the latest stable release

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 1.13.6-0
- Updated to the latest stable release

* Thu Dec 12 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.5-0
- Updated to the latest stable release

* Fri Nov 01 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.4-0
- Updated to the latest stable release

* Sat Oct 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.3-0
- Updated to the latest stable release

* Sat Oct 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.2-0
- Updated to the latest stable release

* Thu Sep 26 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.1-0
- Updated to the latest stable release

* Wed Sep 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13-0
- Updated to the latest stable release

* Tue Aug 20 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.9-0
- Updated to the latest stable release

* Thu Aug 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.8-0
- Updated to the latest stable release

* Tue Jul 09 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.7-0
- Updated to the latest stable release

* Wed Jun 12 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.6-0
- Updated to the latest stable release

* Wed May 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.5-0
- Updated to the latest stable release

* Wed May 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.4-0
- Updated to the latest stable release

* Tue Apr 09 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.3-0
- Updated to the latest stable release

* Sat Apr 06 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.2-0
- Updated to the latest stable release

* Fri Mar 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.1-0
- Updated to the latest stable release

* Tue Feb 26 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12-0
- Updated to the latest stable release

* Thu Jan 24 2019 Anton Novojilov <andy@essentialkaos.com> - 1.11.5-0
- Updated to the latest stable release

* Sat Dec 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.4-0
- Updated to the latest stable release

* Sat Dec 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.3-0
- Updated to the latest stable release

* Sat Nov 03 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.2-0
- Updated to the latest stable release

* Tue Oct 02 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.1-0
- Updated to the latest stable release

* Tue Oct 02 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11-0
- Updated to the latest stable release

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.3-0
- Updated to the latest stable release

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- Updated to the latest stable release

* Fri Mar 30 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.1-0
- Updated to the latest stable release

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10-1
- Added missing tools (buildid, test2json)

* Sat Feb 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10-0
- Updated to the latest stable release

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- Updated to the latest stable release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- Updated to the latest stable release

* Thu Oct 26 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- Updated to the latest stable release

* Thu Oct 05 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- Updated to the latest stable release

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9-0
- Updated to the latest stable release

* Thu May 25 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-0
- Updated to the latest stable release

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- Updated to the latest stable release

* Fri Mar 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8-1
- Improved spec

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- Updated to the latest stable release

* Mon Dec 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- Updated to the latest stable release

* Thu Oct 20 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- Updated to the latest stable release

* Thu Sep 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- Updated to the latest stable release

* Tue Aug 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- Updated to the latest stable release

* Fri Jul 22 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.3-0
- Updated to the latest stable release

* Thu Apr 21 2016 Gleb Goncharov <yum@gongled.ru> - 1.6.2-0
- Updated to the latest stable release

* Fri Feb 19 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6-0
- Updated to the latest stable release

* Thu Feb 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-1
- Improved spec

* Fri Jan 15 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- Updated to the latest stable release

* Fri Dec 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- Updated to the latest stable release

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-1
- Added git to dependencies

* Thu Oct 22 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- Updated to the latest stable release

* Tue Sep 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Initial build
