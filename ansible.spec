################################################################################

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?rhel} == 5
%define __python /usr/bin/python26
%endif

################################################################################

Summary:              Radically simple IT automation
Name:                 ansible
Version:              2.0.1.0
Release:              0%{?dist}
URL:                  http://www.ansible.com
License:              GPLv3
Group:                Development/Libraries

Source:               http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch:            noarch

%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires:        python26-devel
BuildRequires:        python26-setuptools

Requires:             python26-PyYAML
Requires:             python26-paramiko
Requires:             python26-jinja2
Requires:             python26-keyczar
Requires:             python26-httplib2
Requires:             python26-setuptools
Requires:             python26-six
%endif

%if 0%{?rhel} == 6
Requires:             python-crypto2.6
%endif

%if 0%{?rhel} && 0%{?rhel} > 5
BuildRequires:        python2-devel
BuildRequires:        python-setuptools

Requires:             PyYAML
Requires:             python-markupsafe
Requires:             python-paramiko
Requires:             python-jinja2
Requires:             python-keyczar
Requires:             python-httplib2
Requires:             python-setuptools
Requires:             python-six
%endif

%if 0%{?fedora} >= 18
BuildRequires:        python-devel
BuildRequires:        python-setuptools

Requires:             PyYAML
Requires:             python-paramiko
Requires:             python-jinja2
Requires:             python-keyczar
Requires:             python-httplib2
Requires:             python-setuptools
Requires:             python-six
%endif

%if 0%{?suse_version}
BuildRequires:        python-devel
BuildRequires:        python-setuptools

Requires:             python-paramiko
Requires:             python-jinja2
Requires:             python-keyczar
Requires:             python-yaml
Requires:             python-httplib2
Requires:             python-setuptools
Requires:             python-six
%endif

Requires:             sshpass

################################################################################

%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and orchestration engine. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

################################################################################

%prep
%setup -q


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

if expr x'%{python_sitelib}' : 'x.*dist-packages/\?' ; then
    DEST_DIR='%{buildroot}%{python_sitelib}'
    SOURCE_DIR=$(echo "$DEST_DIR" | sed 's/dist-packages/site-packages/g')
    if test -d "$SOURCE_DIR" -a ! -d "$DEST_DIR" ; then
        mv $SOURCE_DIR $DEST_DIR
    fi
fi

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}/
%{__mkdir} -p %{buildroot}/%{_mandir}/man1/
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}

%{__cp} examples/hosts %{buildroot}%{_sysconfdir}/%{name}/
%{__cp} examples/ansible.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__cp} -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/


%clean
%{__rm} -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root)
%{python_sitelib}/%{name}*
%{_bindir}/%{name}*
%dir %{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%doc README.md PKG-INFO COPYING
%doc %{_mandir}/man1/%{name}*

################################################################################

%changelog
* Tue Mar 01 2016 Gleb Goncharov <yum@gongled.me> - 2.0.1.0-0
- Updated to latest version

* Sun Jan 31 2016 Gleb Goncharov <yum@gongled.me> - 2.0.0.1-0
- Initial build
