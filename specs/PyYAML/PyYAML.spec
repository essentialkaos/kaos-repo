################################################################################

Summary:         YAML parser and emitter for Python
Name:            PyYAML
Version:         3.12
Release:         0%{?dist}
Group:           Development/Libraries
License:         MIT
URL:             http://pyyaml.org/wiki/PyYAML

Source0:         http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   gcc python-devel python-setuptools libyaml-devel

Requires:        python

Provides:        python-%{name} = %{version}-%{release}
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
%setup -qn %{name}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

%build
CFLAGS="${RPM_OPT_FLAGS}" python setup.py --with-libyaml build

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python_sitearch}/*

################################################################################

%changelog
* Tue Nov 21 2017 Anton Novojilov <andy@essentialkaos.com> - 3.12-0
- Initial build for kaos repo
