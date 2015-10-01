###############################################################################

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
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ldconfig        %{_sbin}/ldconfig

%define sdk_version       4.6.5
%define sdk_version_raw   465

###############################################################################

Summary:           SDK for lzma compression
Name:              lzma-sdk
Version:           %{sdk_version}
Release:           0%{?dist}
License:           LGPLv2
Group:             Applications/Archiving
URL:               http://upx.sourceforge.net

Source:            http://downloads.sourceforge.net/sevenzip/lzma%{sdk_version_raw}.tar.bz2

Patch0:            %{name}-%{version}-sharedlib.patch

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     make gcc gcc-c++

###############################################################################

%description
LZMA SDK provides the documentation, samples, header files, libraries,
and tools you need to develop applications that use LZMA compression.

LZMA is default and general compression method of 7z format
in 7-Zip compression program (www.7-zip.org). LZMA provides high
compression ratio and very fast decompression.

LZMA is an improved version of famous LZ77 compression algorithm. 
It was improved in way of maximum increasing of compression ratio,
keeping high decompression speed and low memory requirements for
decompressing.

###############################################################################

%package devel
Summary:           Development libraries and headers for %{name}
Requires:          %{name} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

###############################################################################

%prep
%setup -q -c -n lzma465

%patch0 -p1 -b .shared

rm -f lzma.exe

for f in .h .c .cpp .dsw .dsp .java .cs .txt makefile ; do
  find . -iname "*$f" | xargs chmod -x
done

sed -i 's/\r//' *.txt 

for i in \
7zFormat.txt \
CS/7zip/Compress/LzmaAlone/LzmaAlone.sln \
7zC.txt \
CS/7zip/Compress/LzmaAlone/LzmaAlone.csproj \
CPP/7zip/Bundles/Alone7z/resource.rc \
history.txt \
lzma.txt \
CPP/7zip/Compress/LZMA_Alone/makefile.gcc \
CPP/Build.mak \
C/LzmaUtil/makefile.gcc \
CPP/7zip/Bundles/Format7zR/resource.rc \
C/Archive/7z/makefile.gcc \
CPP/7zip/Archive/Archive.def \
CPP/7zip/Bundles/Format7zExtractR/resource.rc \
C/LzmaLib/resource.rc \
CPP/7zip/Archive/Archive2.def \
CPP/7zip/MyVersionInfo.rc \
Methods.txt \
C/LzmaLib/LzmaLib.def; do
    iconv -f iso-8859-1 -t utf-8 $i > $i.utf8
    touch -r $i $i.utf8
    mv $i.utf8 $i
done

%build
pushd CPP/7zip/Compress/LZMA_Alone
CXX="g++ %{optflags} -fPIC" CXX_C="gcc %{optflags} -fPIC" %{__make} %{?_smp_mflags} -f makefile.gcc clean all
popd

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_libdir}
install -dm 755 %{buildroot}%{_includedir}

install -pm 755 CPP/7zip/Compress/LZMA_Alone/liblzmasdk.so.%{sdk_version} %{buildroot}%{_libdir}

pushd %{buildroot}%{_libdir}
ln -s liblzmasdk.so.%{sdk_version} liblzmasdk.so.4
ln -s liblzmasdk.so.%{sdk_version} liblzmasdk.so
popd

find -iname '*.h' | xargs -I {} install -m0644 -D {} %{buildroot}/%{_includedir}/lzma%{sdk_version_raw}/{}

%post 
%{__ldconfig}

%postun 
%{__ldconfig}

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc lzma.txt history.txt
%{_libdir}/liblzmasdk.so.*

%files devel
%defattr(-,root,root,-)
%doc 7z*.txt Methods.txt
%{_includedir}/lzma%{sdk_version_raw}/*
%{_libdir}/liblzmasdk.so

###############################################################################

%changelog
* Tue May 06 2014 Anton Novojilov <andy@essentialkaos.com> - 4.6.5-0
- Initial build
