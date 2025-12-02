################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global debug_package  %{nil}
%global _binaries_in_noarch_packages_terminate_build  0
%define _use_internal_dependency_generator  0
%global __requires_exclude_from  ^(%{_datadir}|/usr/lib)/%{name}/(doc|src)/.*$
%global __strip  /bin/true
%define __find_requires  %{nil}
%global __spec_install_post  /usr/lib/rpm/check-rpaths /usr/lib/rpm/check-buildroot /usr/lib/rpm/brp-compress

################################################################################

# perfecto:ignore
%global goroot  /usr/lib/%{name}
%global gopath  %{_datadir}/gocode

%ifarch x86_64
%global gohostarch  amd64
%endif
%ifarch %{ix86}
%global gohostarch  386
%endif

%global go_api  1.25

################################################################################

Summary:        The Go Programming Language
Name:           golang
Version:        1.25.5
Release:        0%{?dist}
License:        BSD
Group:          Development/Languages
URL:            https://go.dev

Source0:        https://go.dev/dl/go%{version}.src.tar.gz
Source10:       %{name}-gdbinit
Source11:       %{name}-prelink.conf

Source100:      checksum.sha512

Patch0:         disable-google.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  golang >= 1.24

Requires:       %{name}-bin = %{version}-%{release}
Requires:       %{name}-src = %{version}-%{release}

Provides:       go = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}

################################################################################

%description
Go is an open source programming language that makes it easy to build
simple, reliable, and efficient software.

################################################################################

%package src

Summary:    Golang compiler source tree
Group:      Development/Languages

BuildArch:  noarch

%description src
Golang compiler source tree

################################################################################

%package bin

Summary:   Golang compiler tool
Group:     Development/Languages
Requires:  golang = %{version}-%{release}

Requires:  glibc gcc

Provides:  go(API)(go) = %{go_api}

Obsoletes: golang-pkg-bin-linux-amd64 < 1.20
Obsoletes: golang-pkg-darwin-amd64 < 1.20
Obsoletes: golang-pkg-darwin-arm64 < 1.20
Obsoletes: golang-pkg-freebsd-386 < 1.20
Obsoletes: golang-pkg-freebsd-amd64 < 1.20
Obsoletes: golang-pkg-freebsd-arm < 1.20
Obsoletes: golang-pkg-freebsd-arm64 < 1.20
Obsoletes: golang-pkg-linux-386 < 1.20
Obsoletes: golang-pkg-linux-amd64 < 1.20
Obsoletes: golang-pkg-linux-arm < 1.20
Obsoletes: golang-pkg-linux-arm64 < 1.20
Obsoletes: golang-pkg-netbsd-386 < 1.20
Obsoletes: golang-pkg-netbsd-amd64 < 1.20
Obsoletes: golang-pkg-netbsd-arm < 1.20
Obsoletes: golang-pkg-netbsd-arm64 < 1.20
Obsoletes: golang-pkg-openbsd-386 < 1.20
Obsoletes: golang-pkg-openbsd-amd64 < 1.20
Obsoletes: golang-pkg-openbsd-arm < 1.20
Obsoletes: golang-pkg-openbsd-arm64 < 1.20
Obsoletes: golang-pkg-plan9-386 < 1.20
Obsoletes: golang-pkg-plan9-amd64 < 1.20
Obsoletes: golang-pkg-plan9-arm < 1.20
Obsoletes: golang-pkg-windows-386 < 1.20
Obsoletes: golang-pkg-windows-amd64 < 1.20
Obsoletes: golang-pkg-windows-arm < 1.20
Obsoletes: golang-pkg-windows-arm64 < 1.20

%description bin
Golang compiler tool.

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
%crc_check
%autosetup -p1 -n go

%build
export CC="gcc"
export CC_FOR_TARGET="gcc"
export GOROOT_FINAL=%{goroot}
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}

pushd src
  ./make.bash -v
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{goroot}

cp -ap api bin doc lib pkg src misc VERSION go.env \
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
popd

rm -rfv %{buildroot}%{goroot}/lib/time
rm -rfv %{buildroot}%{goroot}/doc/Makefile

mkdir -p %{buildroot}%{gopath}/src/github.com
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org
mkdir -p %{buildroot}%{gopath}/src/code.google.com
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p
mkdir -p %{buildroot}%{gopath}/src/golang.org
mkdir -p %{buildroot}%{gopath}/src/golang.org/x

ln -sf %{goroot}/bin/go    %{buildroot}%{_bindir}/go
ln -sf %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt

mkdir -p %{buildroot}%{_sysconfdir}/gdbinit.d
cp -a %{SOURCE10} %{buildroot}%{_sysconfdir}/gdbinit.d/%{name}.gdb

mkdir -p %{buildroot}%{_sysconfdir}/prelink.conf.d
cp -a %{SOURCE11} %{buildroot}%{_sysconfdir}/prelink.conf.d/%{name}.conf

%posttrans bin
# Rebuild outdated runtime
%{_bindir}/go install std

################################################################################

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md README.md SECURITY.md LICENSE PATENTS

%{goroot}/*

%exclude %{goroot}/bin/
%exclude %{goroot}/pkg/tool/
%exclude %{goroot}/src/

%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com/
%dir %{gopath}/src/bitbucket.org/
%dir %{gopath}/src/code.google.com/
%dir %{gopath}/src/code.google.com/p/

%{_sysconfdir}/gdbinit.d
%{_sysconfdir}/prelink.conf.d

%files bin
%defattr(-,root,root,-)
%{_bindir}/go
%{_bindir}/gofmt
%{goroot}/bin/
%{goroot}/pkg/tool/linux_amd64/

%files -f go-src.list src
%defattr(-,root,root,-)

################################################################################

%changelog
* Tue Dec 02 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.25.5+label:CherryPickApproved

* Thu Nov 06 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.25.4+label:CherryPickApproved

* Tue Oct 14 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.25.3+label:CherryPickApproved

* Tue Oct 07 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.25.2+label:CherryPickApproved

* Thu Sep 04 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.25.1+label:CherryPickApproved

* Fri Aug 15 2025 Anton Novojilov <andy@essentialkaos.com> - 1.25.0-0
- https://go.dev/doc/go1.25

* Tue Aug 12 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.6+label:CherryPickApproved

* Wed Jul 09 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.5+label:CherryPickApproved

* Thu Jun 05 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.4+label:CherryPickApproved

* Wed May 07 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.3+label:CherryPickApproved

* Thu Apr 03 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.2+label:CherryPickApproved

* Wed Mar 05 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.24.1+label:CherryPickApproved

* Wed Feb 12 2025 Anton Novojilov <andy@essentialkaos.com> - 1.24.0-0
- https://go.dev/doc/go1.24

* Wed Feb 05 2025 Anton Novojilov <andy@essentialkaos.com> - 1.23.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.6+label:CherryPickApproved

* Wed Jan 22 2025 Anton Novojilov <andy@essentialkaos.com> - 1.23.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.5+label:CherryPickApproved

* Wed Dec 04 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.4+label:CherryPickApproved

* Fri Nov 08 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.3+label:CherryPickApproved

* Sat Oct 05 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.2+label:CherryPickApproved

* Fri Sep 06 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.23.1+label:CherryPickApproved

* Thu Aug 15 2024 Anton Novojilov <andy@essentialkaos.com> - 1.23.0-0
- https://go.dev/doc/go1.23

* Sun Aug 11 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.6+label:CherryPickApproved

* Wed Jul 03 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.5+label:CherryPickApproved

* Wed Jun 05 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.4+label:CherryPickApproved

* Sun May 12 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.3+label:CherryPickApproved

* Thu Apr 04 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.2+label:CherryPickApproved

* Tue Mar 05 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.22.1+label:CherryPickApproved

* Wed Feb 07 2024 Anton Novojilov <andy@essentialkaos.com> - 1.22.0-0
- https://go.dev/doc/go1.22

* Wed Jan 10 2024 Anton Novojilov <andy@essentialkaos.com> - 1.21.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.6+label:CherryPickApproved

* Wed Dec 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.5+label:CherryPickApproved

* Wed Nov 08 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.4+label:CherryPickApproved

* Wed Oct 11 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.3+label:CherryPickApproved

* Fri Oct 06 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.2+label:CherryPickApproved

* Wed Sep 13 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.21.1+label:CherryPickApproved

* Wed Aug 09 2023 Anton Novojilov <andy@essentialkaos.com> - 1.21.0-0
- https://go.dev/doc/go1.21

* Wed Aug 02 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.7+label:CherryPickApproved

* Tue Jul 18 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.6+label:CherryPickApproved

* Wed Jun 21 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.5+label:CherryPickApproved

* Thu May 04 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.4+label:CherryPickApproved

* Fri Apr 07 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.3+label:CherryPickApproved

* Fri Mar 31 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.2+label:CherryPickApproved

* Mon Mar 20 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.1-1
- Fixed update from Golang < 1.20

* Fri Feb 17 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.20.1+label:CherryPickApproved

* Sat Feb 04 2023 Anton Novojilov <andy@essentialkaos.com> - 1.20-0
- https://go.dev/doc/go1.20

* Thu Jan 12 2023 Anton Novojilov <andy@essentialkaos.com> - 1.19.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.19.5+label:CherryPickApproved

* Wed Dec 07 2022 Anton Novojilov <andy@essentialkaos.com> - 1.19.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.19.4+label:CherryPickApproved

* Sun Dec 04 2022 Anton Novojilov <andy@essentialkaos.com> - 1.19.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.19.3+label:CherryPickApproved

* Sun Oct 09 2022 Anton Novojilov <andy@essentialkaos.com> - 1.19.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.19.2+label:CherryPickApproved

* Mon Sep 12 2022 Anton Novojilov <andy@essentialkaos.com> - 1.19.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.19.1+label:CherryPickApproved

* Wed Aug 17 2022 Anton Novojilov <andy@essentialkaos.com> - 1.19-0
- https://go.dev/doc/go1.19

* Tue Aug 02 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.5+label:CherryPickApproved

* Tue Aug 02 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.4+label:CherryPickApproved

* Tue Jun 21 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.3+label:CherryPickApproved

* Tue Jun 21 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.2+label:CherryPickApproved

* Mon Apr 25 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.1+label:CherryPickApproved

* Fri Apr 01 2022 Anton Novojilov <andy@essentialkaos.com> - 1.18-0
- https://go.dev/doc/go1.18

* Fri Mar 04 2022 Anton Novojilov <andy@essentialkaos.com> - 1.17.8-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.8+label:CherryPickApproved

* Fri Feb 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.17.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.7+label:CherryPickApproved

* Fri Feb 11 2022 Anton Novojilov <andy@essentialkaos.com> - 1.17.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.6+label:CherryPickApproved

* Sat Dec 11 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.5+label:CherryPickApproved

* Sat Dec 04 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.4+label:CherryPickApproved

* Sat Nov 06 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.3+label:CherryPickApproved

* Fri Oct 08 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.2+label:CherryPickApproved

* Fri Sep 10 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.17.1+label:CherryPickApproved

* Tue Aug 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.17-0
- https://golang.org/doc/go1.17

* Tue Aug 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.7+label:CherryPickApproved

* Fri Jul 16 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.6+label:CherryPickApproved

* Fri Jul 16 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.5+label:CherryPickApproved

* Fri Jul 16 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.4+label:CherryPickApproved

* Fri Apr 02 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.3+label:CherryPickApproved

* Fri Mar 12 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.16.2+label:CherryPickApproved

* Wed Feb 17 2021 Anton Novojilov <andy@essentialkaos.com> - 1.16-0
- https://golang.org/doc/go1.16

* Wed Feb 10 2021 Anton Novojilov <andy@essentialkaos.com> - 1.15.8-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.8+label:CherryPickApproved

* Wed Jan 20 2021 Anton Novojilov <andy@essentialkaos.com> - 1.15.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.7+label:CherryPickApproved

* Tue Dec 08 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.6+label:CherryPickApproved

* Mon Dec 07 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.5+label:CherryPickApproved

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.4+label:CherryPickApproved

* Mon Oct 26 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.3+label:CherryPickApproved

* Mon Oct 26 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved

* Thu Sep 03 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.15.1+label:CherryPickApproved

* Wed Aug 12 2020 Anton Novojilov <andy@essentialkaos.com> - 1.15-0
- https://golang.org/doc/go1.15

* Tue Aug 11 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.7+label:CherryPickApproved

* Wed Jul 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.6+label:CherryPickApproved

* Wed Jul 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.5+label:CherryPickApproved

* Wed Jul 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.4+label:CherryPickApproved

* Fri May 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.3+label:CherryPickApproved

* Thu Apr 09 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.2+label:CherryPickApproved

* Fri Mar 20 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.14.1+label:CherryPickApproved

* Wed Feb 26 2020 Anton Novojilov <andy@essentialkaos.com> - 1.14-0
- https://golang.org/doc/go1.14

* Wed Jan 29 2020 Anton Novojilov <andy@essentialkaos.com> - 1.13.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Mon Jan 20 2020 Anton Novojilov <andy@essentialkaos.com> - 1.13.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Thu Dec 12 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Fri Nov 01 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Sat Oct 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Sat Oct 19 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Thu Sep 26 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.13.1+label:CherryPickApproved

* Wed Sep 04 2019 Anton Novojilov <andy@essentialkaos.com> - 1.13-0
- https://golang.org/doc/go1.13

* Tue Aug 20 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.9-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.9+label:CherryPickApproved

* Thu Aug 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.8-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.8+label:CherryPickApproved

* Tue Jul 09 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.7-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.7+label:CherryPickApproved

* Wed Jun 12 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.6-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.6+label:CherryPickApproved

* Wed May 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.5+label:CherryPickApproved

* Wed May 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.4+label:CherryPickApproved

* Tue Apr 09 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.3+label:CherryPickApproved

* Sat Apr 06 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.2+label:CherryPickApproved

* Fri Mar 15 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.12.1+label:CherryPickApproved

* Tue Feb 26 2019 Anton Novojilov <andy@essentialkaos.com> - 1.12-0
- https://golang.org/doc/go1.12

* Thu Jan 24 2019 Anton Novojilov <andy@essentialkaos.com> - 1.11.5-0
- https://github.com/golang/go/issues?q=milestone:Go1.11.5+label:CherryPickApproved

* Sat Dec 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.11.4+label:CherryPickApproved

* Sat Dec 15 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.11.3+label:CherryPickApproved

* Sat Nov 03 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.11.2+label:CherryPickApproved

* Tue Oct 02 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.11.1+label:CherryPickApproved

* Tue Oct 02 2018 Anton Novojilov <andy@essentialkaos.com> - 1.11-0
- https://golang.org/doc/go1.11

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.10.3+label:CherryPickApproved

* Wed Jun 13 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.10.2+label:CherryPickApproved

* Fri Mar 30 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.10.1+label:CherryPickApproved

* Thu Mar 22 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10-1
- Added missing tools (buildid, test2json)

* Sat Feb 17 2018 Anton Novojilov <andy@essentialkaos.com> - 1.10-0
- https://golang.org/doc/go1.10

* Thu Feb 08 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.9.4+label:CherryPickApproved

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 1.9.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.9.3+label:CherryPickApproved

* Thu Oct 26 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.9.2+label:CherryPickApproved

* Thu Oct 05 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.9.1+label:CherryPickApproved

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 1.9-0
- https://golang.org/doc/go1.9

* Thu May 25 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.3+label:CherryPickApproved

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.18.1+label:CherryPickApproved

* Fri Mar 10 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8-1
- Improved spec

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 1.8-0
- https://golang.org/doc/go1.8

* Mon Dec 05 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.4-0
- https://github.com/golang/go/issues?q=milestone:Go1.7.4+label:CherryPickApproved

* Thu Oct 20 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.7.3+label:CherryPickApproved

* Thu Sep 08 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.7.1+label:CherryPickApproved

* Tue Aug 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.7.0-0
- https://golang.org/doc/go1.7

* Fri Jul 22 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.6.3+label:CherryPickApproved

* Thu Apr 21 2016 Gleb Goncharov <yum@gongled.ru> - 1.6.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.6.2+label:CherryPickApproved

* Fri Feb 19 2016 Anton Novojilov <andy@essentialkaos.com> - 1.6-0
- https://golang.org/doc/go1.6

* Thu Feb 18 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-1
- Improved spec

* Fri Jan 15 2016 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- https://github.com/golang/go/issues?q=milestone:Go1.5.3+label:CherryPickApproved

* Fri Dec 04 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.2-0
- https://github.com/golang/go/issues?q=milestone:Go1.5.2+label:CherryPickApproved

* Sat Nov 21 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-1
- Added git to dependencies

* Thu Oct 22 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.1-0
- https://github.com/golang/go/issues?q=milestone:Go1.5.1+label:CherryPickApproved

* Tue Sep 01 2015 Anton Novojilov <andy@essentialkaos.com> - 1.5.0-0
- Initial build
