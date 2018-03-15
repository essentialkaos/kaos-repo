################################################################################

%global __python3 %{_bindir}/python3

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

%define pkgname  PyYAML

################################################################################

Summary:         YAML parser and emitter for Python
Name:            python34-PyYAML
Version:         3.12
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             http://pyyaml.org/wiki/PyYAML

Source0:         http://pyyaml.org/download/pyyaml/%{pkgname}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc python34-devel python34-setuptools libyaml-devel

Requires:        python34

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages. PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

################################################################################

%prep
%setup -qn %{pkgname}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

%build
CFLAGS="${RPM_OPT_FLAGS}" %{__python3} setup.py --with-libyaml build

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python3_sitearch}/*

################################################################################

%changelog
* Tue Nov 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.12-0
- Initial build for kaos repo
