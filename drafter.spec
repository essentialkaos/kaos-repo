###############################################################################

Summary:              Complex builder of API Blueprint
Name:                 drafter
Version:              3.1.3
Release:              0%{?dist}
License:              MIT
Group:                Development/Libraries
URL:                  https://github.com/apiaryio/drafter

Source:               https://github.com/apiaryio/%{name}/releases/download/v%{version}/%{name}-v%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        devtoolset-2-gcc-c++ make

Provides:             %{name} = %{version}-%{release}

###############################################################################

%description
Drafter is complex builder of API Blueprint. Internally it uses Snowcrash
library, reference API Blueprint parser. API Blueprint is Web API documentation 
language. You can find API Blueprint documentation on the API Blueprint site.

Additionally Drafter provide set of Wrappers for serialization, of parsing 
result, via SOS library into JSON and YAML format. Drafter also provides 
the user ability to select the type of the output. 

There are two possible values:

- API Elements Parse Result: 
  Parse Result is defined in API Elements according to Parse Result Namespace.

- Normal AST Parse Result: 
  Parse Result defined by the API Blueprint AST Parse Result. 
  The AST is deprecated and only available in the Drafter command line tool.

By default, Drafter assumes the Refract Parse Result. Both the types of 
Parse Results are available in two different serialization formats, 
YAML and JSON. YAML is the default for the CLI.

###############################################################################

%prep
%setup -qn %{name}-v%{version}

%build

# Use gcc and gcc-c++ from devtoolset for build
export PATH="/opt/rh/devtoolset-2/root/usr/bin:$PATH"

./configure
make %{name}

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -pm 755 bin/%{name} %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc README.md LICENSE 
%{_bindir}/%{name}

###############################################################################

%changelog
* Mon Oct 17 2016 Gleb Goncharov <g.goncharov@fun-box.ru> - 3.1.3-0
- Initial build
