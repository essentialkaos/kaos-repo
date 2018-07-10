################################################################################

%global srcname    pyzmq
%global pypi_path  ab/3a/5826efd93ebbbdc33203f70c6ceebab1b58ac6cb1e1ab131cc6b990b4cfa

################################################################################

Summary:        Software library for fast, message-based applications
Name:           python-zmq
Version:        15.4.0
Release:        0%{?dist}
License:        LGPLv3+ and ASL 2.0 and BSD
Group:          Development/Libraries
URL:            http://zeromq.org/bindings:python

Source:         https://pypi.python.org/packages/%{pypi_path}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  python-devel python-setuptools
BuildRequires:  chrpath Cython zeromq3-devel

Requires:       python

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.

################################################################################

%prep
%setup -qn %{srcname}-%{version}

# remove bundled libraries
rm -rf bundled

# remove excecutable bits
chmod -x examples/pubsub/topics_pub.py
chmod -x examples/pubsub/topics_sub.py

find zmq -name "*.c" -delete
python setup.py cython

%build
CFLAGS="%{optflags}" python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --skip-build --root %{buildroot}

chrpath --delete %{buildroot}%{python_sitearch}/zmq/{backend/cython,devices}/*.so

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md COPYING.* examples/
%{python_sitearch}/%{srcname}-*.egg-info
%{python_sitearch}/zmq

################################################################################

%changelog
* Wed Mar 14 2018 Anton Novojilov <andy@essentialkaos.com> - 15.4.0-0
- Initial build for kaos repository
