################################################################################

%define pkgname    msgpack
%define pypi_path  8a/20/6eca772d1a5830336f84aca1d8198e5a3f4715cd1c7fc36d3cc7f7185091

################################################################################

Summary:        A Python MessagePack (de)serializer
Name:           python-%{pkgname}
Version:        0.5.6
Release:        1%{?dist}
License:        ASL 2.0
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/msgpack-python/

Source:         https://pypi.python.org/packages/%{pypi_path}/%{pkgname}-python-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel python-setuptools gcc gcc-c++

Requires:       python

Provides:       %{name} = %{verion}-%{release}
Provides:       python2-%{pkgname} = %{verion}-%{release}

################################################################################

%description
MessagePack is a binary-based efficient data interchange format that is
focused on high performance. It is like JSON, but very fast and small.
This is a Python (de)serializer for MessagePack.

################################################################################

%prep
%setup -qn %{pkgname}-python-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.rst COPYING
%{python_sitearch}/%{pkgname}/
%{python_sitearch}/%{pkgname}*.egg-info

################################################################################

%changelog
* Sat Mar 17 2018 Anton Novojilov <andy@essentialkaos.com> - 0.5.6-0
- Initial build for kaos repository
