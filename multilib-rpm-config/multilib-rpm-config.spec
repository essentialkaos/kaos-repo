################################################################################

%{!?_licensedir:%global license %doc}

%global macrosdir       %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global rrcdir          %_libexecdir

################################################################################

Summary:         Multilib packaging helpers
Name:            multilib-rpm-config
Version:         1.0.0
Release:         6%{?dist}
License:         GPLv2+
Group:           Development/Tools
URL:             https://fedoraproject.org/wiki/PackagingDrafts/MultilibTricks

Source0:         multilib-fix
Source1:         macros.ml
Source2:         README
Source3:         COPYING
Source4:         multilib-library
Source5:         multilib-info

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc

Requires:        redhat-rpm-config

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Set of tools (shell scripts, RPM macro files) to help with multilib packaging
issues.

################################################################################

%prep
%setup -c -T

install -m 644 %{SOURCE2} %{SOURCE3} .

%build
%global ml_fix %rrcdir/multilib-fix
%global ml_info %rrcdir/multilib-info

lib_sed_pattern='/@LIB@/ {
    r %{SOURCE4}
    d
}'

sed -e 's|@ML_FIX@|%ml_fix|g' \
    -e 's|@ML_INFO@|%ml_info|g' \
    %{SOURCE1} > macros.multilib
sed -e "$lib_sed_pattern" \
    %{SOURCE0} > multilib-fix
sed -e "$lib_sed_pattern" \
    %{SOURCE5} > multilib-info

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{rrcdir}
mkdir -p %{buildroot}%{macrosdir}

install -m 644 -p macros.multilib %{buildroot}/%{macrosdir}
install -m 755 -p multilib-fix %{buildroot}/%{ml_fix}
install -m 755 -p multilib-info %{buildroot}/%{ml_info}

%clean
rm -rf %{buildroot}

%check
mkdir tests ; cd tests
ml_fix="sh $(pwd)/../multilib-fix --buildroot $(pwd)"
capable="sh $(pwd)/../multilib-info --multilib-capable"

mkdir template
cat > template/main.c <<EOF
#include "header.h"
int main () { call (); return 0; }
EOF
cat > template/header.h <<EOF
#include <stdio.h>
void call (void) { printf ("works!\n"); }
EOF

cp -r template basic
gcc ./basic/main.c
./a.out

pwd
if $($capable) ; then
    cp -r template really-works
    $ml_fix --file /really-works/header.h
    gcc really-works/main.c
    ./a.out
    test -f really-works/header-*.h
fi

cp -r template other_arch
$ml_fix --file /other_arch/header.h --arch ppc64
test -f other_arch/header-*.h

cp -r template other_arch_fix
$ml_fix --file /other_arch_fix/header.h --arch ppc64p7
test -f other_arch_fix/header-ppc64.h

cp -r template aarch64-no-change
$ml_fix --file /aarch64-no-change/header.h --arch aarch64
test ! -f aarch64-no-change/header-*.h

test $($capable --arch x86_64) = true
test $($capable --arch aarch64) = false
test $($capable --arch ppc64p7) = true

################################################################################

%files
%defattr(-,root,root,-)
%doc README COPYING
%{rrcdir}/*
%{macrosdir}/*

################################################################################

%changelog
* Wed Nov 23 2016 Anton Novojilov <andy@essentialkaos.com> - 1.0.0-6
- Initial build for kaos repo
